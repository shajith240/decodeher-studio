"""CLIP BANK (owner 10-15: "we're using repetitive footage; a very vast database"): a growing, de-duplicated bank of 2D-animation clips,
harvested from Pinterest, filtered, tagged by sight (CLIP) and stored in Google Drive (gdrive:DecodeHer/clip-library/bank/<category>/).
Index format = tools/cliplib.py's (library/clips/index.json + emb.json), extended with:
  pin_id, sha256, phash [3 dHash hex @20/50/80 %], phash_flip, width, height, aspect, crop_safe, crop_offset (0-1 best horizontal pan for a 9:16 crop),
  lowres (short side < 480), tags [[label, score] x5], category, query, path (Drive path under clip-library), used_in [reel slugs], last_used.
Run (needs torch/transformers/gallery-dl; tesseract on PATH):
  UV="uv run --with torch --with transformers --with pillow --with numpy --with gallery-dl --with yt-dlp --with secretstorage python"
  $UV tools/clipbank.py harvest [--queries N] [--per K]    next N queries from brain/content/clip-queries.txt, K clips each (state: library/clips/harvest-state.json)
  $UV tools/clipbank.py search "<text>" [k] [--fresh]       text->image ranking minus a recent/frequent-use penalty
  $UV tools/clipbank.py get <name> <dest_dir>               download one clip from Drive
  $UV tools/clipbank.py mark <reel_slug> <name> [<name>..]  record use (used_in, last_used, usage.json reel order)
  $UV tools/clipbank.py stats                               totals, per category / label, Drive size
  $UV tools/clipbank.py dedupe [--apply]                    scan the whole library for duplicates (dry-run unless --apply; keeps the best copy)
Zero-duplicate rules (a clip is a duplicate if ANY): same Pinterest pin id; same sha256; dHash Hamming <= 6 on 2 of 3 frames (original or mirrored);
CLIP mean-embedding cosine >= 0.95.
Rejects: short < 2 s, short side < 240, on-screen text/watermark (tesseract > 6 alnum chars), photoreal / live action (CLIP zero-shot).
Any aspect ratio is kept (clipcut.py crops to 9:16); stored at native aspect, long side <= 1280, crf 27, no audio.
Gentle with the owner's account: one query at a time, 20-40 s sleep, stops for the day on 429 / login errors (state.stopped_day).
Temp files live in library/clips/_bank_tmp (one query's clips at a time, < 500 MB) and are always removed."""
import datetime, hashlib, json, os, random, re, shutil, subprocess, sys, tempfile, time, urllib.parse
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); LIB = f"{ROOT}/library/clips"; os.makedirs(LIB, exist_ok=True)
RC = os.path.expanduser("~/.local/bin/rclone"); REMOTE = "gdrive:DecodeHer/clip-library"
IDX, EMB, STATE, USAGE = f"{LIB}/index.json", f"{LIB}/emb.json", f"{LIB}/harvest-state.json", f"{LIB}/usage.json"
QFILE = f"{ROOT}/brain/content/clip-queries.txt"; TMP = f"{LIB}/_bank_tmp"; LOG = f"{ROOT}/logs/clipbank.log"
COOKIES = ["--cookies", os.environ["PINTEREST_COOKIES_FILE"]] if os.environ.get("PINTEREST_COOKIES_FILE") else ["--cookies-from-browser", "brave+gnomekeyring"]
today = lambda: datetime.date.today().isoformat()
jl = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
def jsave(p, o, **kw):
    t = p + ".tmp"; json.dump(o, open(t, "w"), **kw); os.replace(t, p)
def log(s):
    os.makedirs(os.path.dirname(LOG), exist_ok=True); open(LOG, "a").write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {s}\n"); print(s, flush=True)
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]

index = jl(IDX, []); emb = jl(EMB, {})
def save(): jsave(IDX, index, indent=1); jsave(EMB, emb)
byname = lambda: {e["name"]: e for e in index}

# ---------- CLIP ----------
m = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval(); P = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
def ie(ims):
    with torch.no_grad(): e = m.get_image_features(**P(images=ims, return_tensors="pt"))
    return torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1)
def te(ts):
    with torch.no_grad(): e = m.get_text_features(**P(text=ts, return_tensors="pt", padding=True))
    return torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1)

VOCAB = {  # fixed vocabulary: ~80 labels
 "scene": ["a cafe", "a restaurant table", "a bedroom at night", "a city street at night", "a rainy window", "a rooftop", "a gym", "a park", "a bar", "a car interior",
           "a train or subway", "a living room", "a kitchen", "a beach or sea", "a party", "a phone screen close up", "a dark empty room", "a city skyline with neon lights",
           "a bus stop", "a balcony", "a mirror", "a chess board", "an abstract background"],
 "people": ["a lonely man", "a woman", "a couple", "a group of friends", "two people talking", "a man in a suit", "a girl with long hair", "a silhouette", "no people, an object", "a crowd"],
 "emotion": ["sadness", "anxiety and overthinking", "happiness and laughter", "jealousy", "anger", "confidence and power", "loneliness", "romance and love", "heartbreak",
             "boredom", "suspicion", "awkward nervousness", "mystery and darkness", "celebration", "longing and waiting", "flirty teasing"],
 "action": ["texting on a phone", "looking at a phone", "waiting", "walking away", "walking alone", "laughing", "crying", "kissing", "hugging", "arguing", "dancing",
            "working out", "drinking coffee", "drinking alcohol", "smoking", "thinking", "staring", "eye contact", "looking over the shoulder", "running", "driving",
            "ignoring someone", "flirting", "sleeping or lying awake", "reading", "writing", "taking a selfie", "holding hands", "pushing away", "listening to music",
            "a clock ticking", "breaking up", "rain falling", "typing", "dressing up or makeup", "sitting alone"],
}
LABELS = [(g, l) for g, ls in VOCAB.items() for l in ls]
LT = None
def label_scores(E):  # E: mean-normalised image embedding -> top 5 [(label, p)] over the whole vocab (softmax x100) and the best scene
    global LT
    if LT is None: LT = te([f"an animated illustration of {l}" if g != "emotion" else f"an animated illustration expressing {l}" for g, l in LABELS])
    p = torch.softmax(100 * (LT @ E), dim=0)
    top = torch.topk(p, 5); tags = [(LABELS[i][1], round(float(v), 3)) for v, i in zip(top.values, top.indices)]
    sc = [(float(p[i]), LABELS[i][1]) for i, (g, l) in enumerate(LABELS) if g == "scene"]
    return tags, max(sc)[1]
STY = None
def illustrated(E):
    global STY
    if STY is None: STY = te(["a 2D illustration or cartoon animation", "a flat vector or hand drawn animation", "a real photo or live action video footage", "a 3D render or video game"])
    p = torch.softmax(100 * (STY @ E), dim=0); return float(p[0] + p[1])

# ---------- media helpers ----------
def probe(f):
    o = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", f]).decode()
    j = json.loads(o); s = j["streams"][0]; return float(j["format"].get("duration") or 0), int(s["width"]), int(s["height"])
def get_frames(f, d, out):  # 3 frames at 20/50/80 %
    ims = []
    for i, t in enumerate((.2, .5, .8)):
        fp = f"{out}/f{i}.png"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{d * t:.2f}", "-i", f, "-frames:v", "1", "-vf", "scale='min(iw,720)':-2", fp])
        if os.path.exists(fp): ims.append(fp)
    return ims
def dhash(im, flip=False):
    g = im.convert("L").resize((9, 8), Image.LANCZOS)
    if flip: g = g.transpose(Image.FLIP_LEFT_RIGHT)
    px = list(g.getdata()); v = 0
    for r in range(8):
        for c in range(8): v = (v << 1) | (px[r * 9 + c] > px[r * 9 + c + 1])
    return f"{v:016x}"
ham = lambda a, b: bin(int(a, 16) ^ int(b, 16)).count("1")
def sha256(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
def ocr_chars(paths):
    worst = 0
    for fp in paths:
        r = subprocess.run(["tesseract", fp, "-", "--psm", "11", "tsv"], capture_output=True, text=True).stdout.splitlines()[1:]; n = 0
        for ln in r:
            c = ln.split("\t")
            if len(c) < 12: continue
            try: conf = float(c[10])
            except ValueError: continue
            w = re.sub(r"[^A-Za-z0-9]", "", c[11])
            if conf >= 70 and len(w) >= 2 and re.search(r"[A-Za-z0-9]{2}", w): n += len(w)
        worst = max(worst, n)
    return worst
def crop_info(paths, w, h):
    """9:16 crop survival: CLIP similarity of the crop vs the full frame. -> (crop_safe 0-1 centre crop, best horizontal offset 0-1)"""
    if w / h <= 9 / 16 + .02: return 1.0, 0.5
    cw = int(h * 9 / 16); offs = [0, .25, .5, .75, 1]; cs = []; bo = []
    for fp in paths:
        im = Image.open(fp).convert("RGB"); W, H = im.size; cw = int(H * 9 / 16)
        crops = [im.crop((int((W - cw) * o), 0, int((W - cw) * o) + cw, H)) for o in offs]
        E = ie([im] + crops); s = (E[1:] @ E[0]).tolist(); cs.append(s[2]); bo.append(offs[max(range(5), key=lambda i: s[i])])
    return round(sum(cs) / len(cs), 3), round(sum(bo) / len(bo), 2)

def is_dup(c, e, Ec=None, Ee=None):
    """c: candidate dict (pin_id, sha256, phash, phash_flip), e: index entry -> reason or None"""
    if c.get("pin_id") and c["pin_id"] == e.get("pin_id"): return "same_pin"
    if c.get("sha256") and c["sha256"] == e.get("sha256"): return "same_file"
    if e.get("phash"):
        n = sum(1 for i in range(3) if min(ham(c["phash"][i], e["phash"][i]), ham(c["phash_flip"][i], e["phash"][i])) <= 6)
        if n >= 2: return "visual_phash"
    if Ec is not None and Ee is not None and float(Ec @ Ee) >= 0.95: return "visual_clip"
    return None
def pin_of(s):
    mm = re.search(r"(?:pinterest_|/pin/)(\d{6,})", s or ""); return mm.group(1) if mm else None
def analyse(f, work):
    """-> dict with all fingerprints (sha, phash, dims, E mean embedding, frames) or raises"""
    d, w, h = probe(f); fr = get_frames(f, d, work)
    if len(fr) < 3: raise RuntimeError("frames")
    ims = [Image.open(x).convert("RGB") for x in fr]
    return {"dur": round(d, 2), "width": w, "height": h, "aspect": round(w / h, 3), "sha256": sha256(f), "frames": fr, "ims": ims,
            "phash": [dhash(i) for i in ims], "phash_flip": [dhash(i, True) for i in ims]}
def mean_emb(ims): return torch.nn.functional.normalize(ie(ims).mean(0), dim=-1)
def emb_matrix():
    names = [e["name"] for e in index if e["name"] in emb]
    return names, (torch.tensor([emb[n] for n in names]) if names else torch.zeros(0, 512))
def tmpsize(): return sum(os.path.getsize(os.path.join(a, b)) for a, _, fs in os.walk(TMP) for b in fs) if os.path.exists(TMP) else 0

# ---------- harvest ----------
def process(f, query, pin, st, names, M, bn):
    """one downloaded file -> (kept entry | None, reason)"""
    work = tempfile.mkdtemp(dir=TMP)
    try:
        try: a = analyse(f, work)
        except Exception as ex: return None, "unreadable"
        if a["dur"] < 2: return None, "too_short"
        if min(a["width"], a["height"]) < 240: return None, "too_small"
        a["pin_id"] = pin
        for e in index:   # cheap exact checks first
            r = is_dup(a, e)
            if r: return None, r
        E = mean_emb(a["ims"])
        if M.shape[0]:
            s = M @ E; j = int(torch.argmax(s))
            if float(s[j]) >= 0.95: return None, "visual_clip"
        if illustrated(E) < 0.5: return None, "photoreal"
        if ocr_chars(a["frames"]) > 6: return None, "text_watermark"
        tags, cat = label_scores(E); cs, co = crop_info(a["frames"], a["width"], a["height"])
        name = f"{slug('-'.join(t[0] for t in tags[:3]))}__{a['sha256'][:8]}.mp4"; cat = slug(cat)
        out = f"{work}/{name}"; w, h = a["width"], a["height"]
        sc = "scale='if(gt(iw,ih),min(1280,iw),-2)':'if(gt(iw,ih),-2,min(1280,ih))'"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f, "-vf", sc, "-c:v", "libx264", "-crf", "27", "-preset", "medium", "-pix_fmt", "yuv420p", "-an", out], check=True)
        path = f"bank/{cat}/{name}"
        subprocess.run([RC, "copyto", out, f"{REMOTE}/{path}", "-q"], check=True)
        chk = subprocess.run([RC, "lsf", f"{REMOTE}/{path}"], capture_output=True, text=True).stdout.strip()
        if not chk: raise RuntimeError("upload not visible")
        ent = {"name": name, "desc": ", ".join(t[0] for t in tags[:3]), "query": query, "source": os.path.basename(f), "pin_id": pin, "pin": f"https://www.pinterest.com/pin/{pin}/",
               "sha256": a["sha256"], "phash": a["phash"], "phash_flip": a["phash_flip"], "dur": a["dur"], "width": w, "height": h, "aspect": a["aspect"],
               "crop_safe": cs, "crop_offset": co, "lowres": min(w, h) < 480, "tags": tags, "category": cat, "path": path, "illustrated": round(illustrated(E), 3),
               "style": round(illustrated(E), 3), "used_in": [], "last_used": None, "added": today(), "size": os.path.getsize(out)}
        index.append(ent); emb[name] = [round(x, 5) for x in E.tolist()]; save()
        return ent, "kept"
    except Exception as ex:
        return None, f"error:{type(ex).__name__}"
    finally: shutil.rmtree(work, ignore_errors=True)

def harvest(nq, per):
    st = jl(STATE, {"next": 0, "done": [], "stopped_day": None}); qs = [l.strip() for l in open(QFILE) if l.strip() and not l.startswith("#")]
    if st.get("stopped_day") == today(): log("harvest: stopped for today (earlier 429/login error); try tomorrow"); return
    totals = {}; kept_n = 0
    for _ in range(nq):
        if st["next"] >= len(qs): st["next"] = 0; log("harvest: query list finished, wrapping around (pins already seen are skipped)")
        q = qs[st["next"]]; shutil.rmtree(TMP, ignore_errors=True); os.makedirs(TMP, exist_ok=True); d = f"{TMP}/dl"; os.makedirs(d)
        known = sorted({e["pin_id"] for e in index if e.get("pin_id")} | set(st.get("seen_pins", [])))
        filt = "extension in ('mp4','m3u8')" + (f" and str(id) not in {tuple(known)!r}" if 0 < len(known) < 3000 else "")
        if len(known) == 1: filt = filt.replace(repr(tuple(known)), f"({known[0]!r},)")
        cmd = ["gallery-dl", *COOKIES, "-o", "extractor.pinterest.videos=ytdl", "--range", f"1-{per * 4}", "--filesize-max", "60M", "--filter", filt, "-D", d,
               "https://www.pinterest.com/search/pins/?q=" + urllib.parse.quote(q)]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=900); err = (r.stderr or "")[-1500:]
        files = sorted(os.path.join(d, x) for x in os.listdir(d) if x.endswith(".mp4"))
        if not files and re.search(r"429|too many requests|login|401|403|authenticat|cookie", err, re.I):
            st["stopped_day"] = today(); jsave(STATE, st, indent=1); log(f"harvest: STOP for today on '{q}': {err.strip()[-300:]}"); break
        files = files[: per * 2]; names, M = emb_matrix(); bn = byname(); res = {}; kept = 0
        for f in files:
            if kept >= per: break
            pin = pin_of(os.path.basename(f))
            if pin and pin in st.setdefault("seen_pins", []): res["known_pin"] = res.get("known_pin", 0) + 1; continue
            if tmpsize() > 450e6: log("temp > 450 MB, stop this query"); break
            ent, why = process(f, q, pin, st, names, M, bn); res[why] = res.get(why, 0) + 1
            if pin and why not in ("kept",) and not why.startswith("error") and why != "unreadable": st["seen_pins"].append(pin)
            if ent: kept += 1; names, M = emb_matrix()
            os.remove(f)
        shutil.rmtree(TMP, ignore_errors=True)
        for k, v in res.items(): totals[k] = totals.get(k, 0) + v
        kept_n += kept; st["done"].append({"q": q, "date": today(), "downloaded": len(files), "kept": kept, "results": res}); st["next"] += 1; jsave(STATE, st, indent=1)
        log(f"query '{q}': downloaded {len(files)}, kept {kept}, {res}")
        if _ < nq - 1: time.sleep(random.uniform(20, 40))
    log(f"harvest summary: kept {kept_n}, outcomes {totals}, bank now {len(index)} clips")

# ---------- search / usage ----------
def search(q, k, fresh):
    order = jl(USAGE, []); recent = set(order[-30:]); T = te([f"a 2D cartoon animation of {q}"])[0]; names, M = emb_matrix(); bn = byname()
    sims = (M @ T).tolist(); rows = []
    for n, s in zip(names, sims):
        e = bn[n]; u = e.get("used_in", []); pen = 0.01 * min(len(u), 5)
        isrecent = bool(set(u) & recent); rows.append((s - pen, n, isrecent, bool(u)))
    rows.sort(reverse=True)
    pool = [r for r in rows if not r[2] and not (fresh and r[3])]
    out = pool[:k]
    if len(out) < k or (rows and pool and rows[0][2] and rows[0][0] > pool[0][0] + 0.03):   # recent clips only if nothing else is within 0.03
        thr = (pool[0][0] if pool else -9) + 0.03
        extra = [r for r in rows if r[2] and r[0] > thr and not (fresh and r[3])]
        out = sorted(out + extra, reverse=True)[:k]
        if len(out) < k: out += [r for r in rows if r not in out and not (fresh and r[3])][: k - len(out)]
    for sc, n, rec, u in out:
        e = bn[n]; print(f"{sc:.3f}  {n}  ({e.get('width','?')}x{e.get('height','?')}, {e['dur']}s{', recent-use' if rec else ''}{', lowres' if e.get('lowres') else ''}, crop_safe {e.get('crop_safe','-')}, offset {e.get('crop_offset','-')})")
def get(name, dest):
    e = byname().get(name); path = (e or {}).get("path") or name; os.makedirs(dest, exist_ok=True)
    subprocess.run([RC, "copyto", f"{REMOTE}/{path}", f"{dest}/{name}", "-q"], check=True); print(f"{dest}/{name}")
def mark(reel, ns):
    bn = byname(); order = jl(USAGE, [])
    if reel in order: order.remove(reel)
    order.append(reel); jsave(USAGE, order)
    for n in ns:
        e = bn[n];
        if reel not in e.setdefault("used_in", []): e["used_in"].append(reel)
        e["last_used"] = today()
    save(); print(f"marked {len(ns)} clips used in {reel}")

# ---------- stats ----------
def stats():
    print(f"total clips: {len(index)}  (with fingerprints: {sum(1 for e in index if e.get('phash'))})")
    cats = {}; labs = {}
    for e in index:
        cats[e.get("category", "legacy")] = cats.get(e.get("category", "legacy"), 0) + 1
        for t in e.get("tags", [])[:1]: labs[t[0]] = labs.get(t[0], 0) + 1
    print("per category:", dict(sorted(cats.items(), key=lambda x: -x[1])))
    print("top label counts:", dict(sorted(labs.items(), key=lambda x: -x[1])[:25]))
    print("lowres:", sum(1 for e in index if e.get("lowres")), " used at least once:", sum(1 for e in index if e.get("used_in")))
    r = subprocess.run([RC, "size", "--json", REMOTE], capture_output=True, text=True)
    try: j = json.loads(r.stdout); print(f"Drive: {j['count']} files, {j['bytes'] / 1e6:.1f} MB")
    except Exception: print("Drive size unavailable", r.stderr[-200:])

# ---------- dedupe ----------
def backfill():
    """legacy entries lack fingerprints: download each from Drive one at a time, fingerprint, delete"""
    n = 0
    for e in index:
        if e.get("phash") and e.get("sha256"): continue
        os.makedirs(TMP, exist_ok=True); work = tempfile.mkdtemp(dir=TMP); f = f"{work}/{e['name']}"
        try:
            subprocess.run([RC, "copyto", f"{REMOTE}/{e.get('path') or e['name']}", f, "-q"], check=True); a = analyse(f, work)
            e.update({"sha256": a["sha256"], "phash": a["phash"], "phash_flip": a["phash_flip"], "width": a["width"], "height": a["height"], "aspect": a["aspect"],
                      "pin_id": e.get("pin_id") or pin_of(e.get("pin") or e.get("source")), "size": os.path.getsize(f), "lowres": min(a["width"], a["height"]) < 480})
            if "crop_safe" not in e: e["crop_safe"], e["crop_offset"] = crop_info(a["frames"], a["width"], a["height"])
            if e["name"] not in emb: emb[e["name"]] = [round(x, 5) for x in mean_emb(a["ims"]).tolist()]
            n += 1
        except Exception as ex: print("backfill failed", e["name"], ex)
        finally: shutil.rmtree(work, ignore_errors=True)
    if n: save()
    shutil.rmtree(TMP, ignore_errors=True); return n
def dedupe(apply):
    nb = backfill(); print(f"fingerprinted {nb} legacy clips")
    names, M = emb_matrix(); pos = {n: i for i, n in enumerate(names)}; bn = byname(); drop = {}   # name -> (kept, reason)
    quality = lambda e: (bool(e.get("used_in")), e.get("quality") or 0, e.get("judged_style") or 0, e.get("size") or 0, e.get("dur", 0))
    for i, a in enumerate(index):
        for b in index[i + 1:]:
            if a["name"] in drop or b["name"] in drop: continue
            Ea = Eb = None
            if a["name"] in pos and b["name"] in pos: Ea, Eb = M[pos[a["name"]]], M[pos[b["name"]]]
            r = is_dup({"pin_id": a.get("pin_id"), "sha256": a.get("sha256"), "phash": a.get("phash") or ["0" * 16] * 3, "phash_flip": a.get("phash_flip") or ["0" * 16] * 3}, b, Ea, Eb) \
                if a.get("phash") else is_dup({"pin_id": a.get("pin_id"), "sha256": a.get("sha256")}, b, Ea, Eb)
            if r:
                keep, lose = (a, b) if quality(a) >= quality(b) else (b, a); drop[lose["name"]] = (keep["name"], r)
    print(f"duplicates found: {len(drop)} of {len(index)} clips")
    for n, (k, r) in drop.items(): print(f"  {n}\n    dup of {k}  [{r}]")
    if apply and drop:
        for n, (k, r) in drop.items():
            e = bn[n]; kk = bn[k]
            for u in e.get("used_in", []):
                if u not in kk.setdefault("used_in", []): kk["used_in"].append(u)
            subprocess.run([RC, "deletefile", f"{REMOTE}/{e.get('path') or n}", "-q"]); emb.pop(n, None)
        index[:] = [e for e in index if e["name"] not in drop]; save(); print(f"removed {len(drop)} duplicates from Drive + index")
    elif drop: print("(dry run: pass --apply to delete the extra copies)")

if __name__ == "__main__":
    a = sys.argv[1:]; cmd = a[0] if a else ""
    opt = lambda f, dflt: int(a[a.index(f) + 1]) if f in a else dflt
    if cmd == "harvest": harvest(opt("--queries", 3), opt("--per", 10))
    elif cmd == "search":
        rest = [x for x in a[2:] if not x.startswith("--")]; search(a[1], int(rest[0]) if rest else 5, "--fresh" in a)
    elif cmd == "get": get(a[1], a[2])
    elif cmd == "mark": mark(a[1], a[2:])
    elif cmd == "stats": stats()
    elif cmd == "dedupe": dedupe("--apply" in a)
    else: print(__doc__)
