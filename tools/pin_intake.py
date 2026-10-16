"""Pinterest links from Telegram -> the clip library (owner 10-16: "I send pins from bed, the manager downloads, checks we don't
have it, files it and chats back").
Usage: python3 tools/pin_intake.py            (run by tools/manager.py every 2 min; safe to run by hand)
       python3 tools/pin_intake.py index      (only (re)build the fingerprint registry of what we already have)
Flow: GET $HQ/api/inbox (items the owner sent; kind "hook" = AI-girl hook, "dark" = dark-psychology clip) -> for each link:
gallery-dl (owner's Brave login) -> video only -> duplicate check -> file it -> Google Drive copy -> POST $HQ/api/inbox with a
plain-words report (+ a preview frame of the first new clip) that HQ forwards to the owner's Telegram.
Duplicate = ANY of: same Pinterest pin id; same sha256; dHash of 3 frames (20/50/80 %) within Hamming 6 on 2 of 3 frames,
original or mirrored. Registry: library/pin-registry.json (also fingerprints what we already had: hook-pool, reels/_pool).
Files: hook -> library/hook-pool/ai/ai-<ai-slug>-<pin6>.mp4 (+ .json with ai_description + tags; pin-number name if Claude is unavailable); dark -> library/clips/inbox/dark-<pin>.mp4 (+ .json).
Drive: gdrive:DecodeHer/clip-library/hooks|dark/. Credentials: .secrets/HQ_URL, .secrets/HQ_KEY (never printed)."""
import base64, glob, hashlib, json, os, re, shutil, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
REG = "library/pin-registry.json"; DEST = {"hook": "library/hook-pool/ai", "dark": "library/clips/inbox"}
DRIVE = {"hook": "gdrive:DecodeHer/clip-library/hooks", "dark": "gdrive:DecodeHer/clip-library/dark"}
NAME = {"hook": "AI-girl hook", "dark": "dark-psychology clip"}
COOKIES = ["--cookies", os.environ["PINTEREST_COOKIES_FILE"]] if os.environ.get("PINTEREST_COOKIES_FILE") else ["--cookies-from-browser", "brave+gnomekeyring"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try: from activity import log
except Exception: log = lambda m: None

def secret(n):
    p = os.path.join(ROOT, ".secrets", n); return open(p).read().strip() if os.path.exists(p) else os.environ.get(n, "")
def hq(method, path, body=None):
    url, key = secret("HQ_URL").rstrip("/"), secret("HQ_KEY")
    if not url or not key: return None
    req = urllib.request.Request(url + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "decodeher-pin-intake/1.0"})   # Cloudflare 403s the default Python-urllib agent
    try: return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except Exception: return None

def dur(f):
    try: return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
    except Exception: return 0.0
def size(f):
    try: w, h = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", f]).decode().strip().split(",")[:2]; return int(w), int(h)
    except Exception: return 0, 0
def dhash(f, t, flip=False):   # 64-bit difference hash of the frame at t
    vf = ("hflip," if flip else "") + "scale=9:8,format=gray"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-vf", vf, "-f", "rawvideo", "-"], capture_output=True).stdout
    if len(raw) < 72: return None
    return sum(1 << i for i in range(64) if raw[(i // 8) * 9 + i % 8] > raw[(i // 8) * 9 + i % 8 + 1])
def prints(f):
    d = dur(f); ts = [d * k for k in (0.2, 0.5, 0.8)] if d > 0.5 else [0, 0, 0]
    return {"dh": [dhash(f, t) for t in ts], "dhf": [dhash(f, t, True) for t in ts],
            "sha": hashlib.sha256(open(f, "rb").read()).hexdigest(), "dur": round(d, 1)}
ham = lambda a, b: bin(a ^ b).count("1") if a is not None and b is not None else 99
def near(p, q):   # 2 of 3 frames within 6 bits, straight or mirrored
    return sum(ham(a, b) <= 6 for a, b in zip(p["dh"], q["dh"])) >= 2 or sum(ham(a, b) <= 6 for a, b in zip(p["dh"], q["dhf"])) >= 2
pin_of = lambda path: (re.search(r"(\d{12,})", os.path.basename(path)) or [None, None])[1]

def load_reg():
    return json.load(open(REG)) if os.path.exists(REG) else {"items": {}}
def save_reg(r):
    json.dump(r, open(REG + ".part", "w")); os.replace(REG + ".part", REG)
def index(reg):   # fingerprint what we already have (once per file)
    have = {v["file"] for v in reg["items"].values()}
    files = glob.glob("library/hook-pool/*.mp4") + glob.glob("library/hook-pool/ai/*.mp4") + glob.glob("reels/_pool/**/*.mp4", recursive=True) + glob.glob("library/clips/inbox/*.mp4")
    n = 0
    for f in files:
        if f in have: continue
        key = pin_of(f) or "file:" + f
        if key in reg["items"]: continue
        reg["items"][key] = {"file": f, "kind": "hook" if "hook-pool" in f else "dark", **prints(f), "at": time.strftime("%F")}; n += 1
        if n % 25 == 0: save_reg(reg)
    save_reg(reg); return n

def dup_of(reg, pin, fp):
    if pin and pin in reg["items"]: return reg["items"][pin]
    for v in reg["items"].values():
        if v.get("sha") == fp["sha"] or (v.get("dh") and near(fp, v)): return v
    return None

def fetch(url, tmp):
    subprocess.run(["uv", "run", "-q", "--with", "gallery-dl", "--with", "yt-dlp", "--with", "secretstorage", "gallery-dl", *COOKIES,
                    "--write-metadata", "-o", "extractor.pinterest.videos=ytdl", "-D", tmp, url], capture_output=True, timeout=300)
    vids = sorted(glob.glob(f"{tmp}/*.mp4")); imgs = [f for f in glob.glob(f"{tmp}/*") if re.search(r"\.(jpe?g|png|webp|gif)$", f, re.I)]
    meta = {}
    if vids and os.path.exists(vids[0] + ".json"):
        try: meta = json.load(open(vids[0] + ".json"))
        except Exception: meta = {}
    return (vids[0] if vids else None), bool(imgs), meta

def frame_b64(f):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{min(2.0, dur(f) / 2):.2f}", "-i", f, "-frames:v", "1", "-vf", "scale=360:-2", "-q:v", "4", f"{d}/a.jpg"])
        return base64.b64encode(open(f"{d}/a.jpg", "rb").read()).decode() if os.path.exists(f"{d}/a.jpg") else None

def describe(vid, kind):   # 10-16 owner: "the AI sees the clip, names it and adds it to the database" — one cheap Haiku call on one frame
    """Returns {"slug": "black-dress-night-city", "description": "...", "tags": [...]} or None (Claude capped / not available -> caller keeps the pin-number name)."""
    try:
        with tempfile.TemporaryDirectory(dir=os.path.join(ROOT, "library")) as d:
            jpg = os.path.join(d, "f.jpg")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{min(2.0, dur(vid) / 2):.2f}", "-i", vid, "-frames:v", "1", "-vf", "scale=480:-2", "-q:v", "4", jpg])
            if not os.path.exists(jpg): return None
            what = ("a realistic AI-generated woman used as a scroll-stopping hook (note hair, outfit, setting, mood, camera framing)"
                    if kind == "hook" else "a dark-psychology style clip (note subject, mood, setting, what situation or emotion it could illustrate in a dating-psychology reel)")
            prompt = (f"Read the image {jpg}. It is a frame from {what}. Answer with JSON only: "
                      '{"slug": "3-5 lowercase words joined by hyphens, no names", "description": "one plain sentence", "tags": ["5-8 short tags"]}')
            out = subprocess.run([os.environ.get("CLAUDE_BIN", "claude"), "-p", prompt, "--model", "haiku", "--allowedTools", "Read", "--output-format", "text"],
                                 capture_output=True, text=True, timeout=120).stdout
            m = re.search(r"\{.*\}", out, re.S); j = json.loads(m.group(0)) if m else {}
            slug = re.sub(r"[^a-z0-9]+", "-", str(j.get("slug", "")).lower()).strip("-")[:40]
            if not slug: return None
            return {"slug": slug, "description": str(j.get("description", ""))[:300], "tags": [str(t)[:30] for t in j.get("tags", [])][:8]}
    except Exception: return None

def run():
    box = hq("GET", "/api/inbox")
    if not box or not box.get("items"): return 0
    reg = load_reg(); index(reg)
    for it in box["items"]:
        kind = it.get("kind") or "dark"; hq("POST", "/api/inbox", {"id": it["id"], "state": "working"})
        added, dups, bad, photo = [], [], [], None
        for url in it["urls"]:
            with tempfile.TemporaryDirectory(dir=os.path.join(ROOT, "library")) as tmp:
                try: vid, img, meta = fetch(url, tmp)
                except Exception: vid, img, meta = None, False, {}
                if not vid: bad.append(f"{url} ({'a photo, not a video' if img else 'could not download'})"); continue
                pin = str(meta.get("id") or pin_of(vid) or ""); fp = prints(vid); d = dup_of(reg, pin, fp)
                if d: dups.append(f"{url} (already have it: {os.path.basename(d['file'])}, since {d.get('at', '?')})"); continue
                w, h = size(vid)
                if fp["dur"] < 2 or min(w, h) < 240: bad.append(f"{url} (too short or too small: {fp['dur']} s, {w}x{h})"); continue
                os.makedirs(DEST[kind], exist_ok=True); ds = describe(vid, kind); pre = "ai" if kind == "hook" else "dark"
                name = f"{pre}-{ds['slug']}-{(pin or fp['sha'])[-6:]}" if ds else f"{pre}-{pin or fp['sha'][:12]}"
                out = f"{DEST[kind]}/{name}.mp4"; shutil.copy(vid, out)
                json.dump({"pin": pin, "url": url, "title": meta.get("title") or meta.get("grid_title") or "", "description": (meta.get("description") or "")[:300],
                           "from": "owner via Telegram", "at": time.strftime("%F %T"), **({"ai_description": ds["description"], "tags": ds["tags"]} if ds else {})}, open(f"{DEST[kind]}/{name}.json", "w"), indent=1, ensure_ascii=False)
                reg["items"][pin or "file:" + out] = {"file": out, "kind": kind, **fp, "at": time.strftime("%F")}; save_reg(reg)
                subprocess.run(["rclone", "copy", out, DRIVE[kind], "-q"], capture_output=True, timeout=600)
                added.append(f"{name} ({fp['dur']:.0f} s, {w}x{h})" + (f" — {ds['description']}" if ds else " — (no AI description: Claude was busy, named by pin number)")); photo = photo or frame_b64(out)
        lines = [f"✅ <b>{len(added)} new {NAME[kind]}{'s' if len(added) != 1 else ''}</b> added and backed up to Drive."] if added else [f"No new {NAME[kind]}s from those links."]
        lines += [f"• {a}" for a in added[:10]]
        if dups: lines += ["", f"♻️ Already in the library ({len(dups)}):"] + [f"• {d}" for d in dups[:10]]
        if bad: lines += ["", f"⚠️ Skipped ({len(bad)}):"] + [f"• {b}" for b in bad[:10]]
        total = sum(1 for v in reg["items"].values() if v.get("kind") == kind)
        lines += ["", f"Library now has {total} {NAME[kind]}s."]
        hq("POST", "/api/inbox", {"id": it["id"], "state": "done" if (added or dups) else "failed", "text": "\n".join(lines), **({"photo_b64": photo} if photo else {})})
        log(f"Pinterest links · {len(added)} new {NAME[kind]}, {len(dups)} duplicates, {len(bad)} skipped")
    return len(box["items"])

if __name__ == "__main__":
    if sys.argv[1:] == ["index"]: r = load_reg(); print("fingerprinted", index(r), "files; registry has", len(r["items"]))
    else: print("handled", run(), "inbox items")
