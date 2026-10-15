"""Contact sheets for the clip judges (owner 10-14: "CLIP sees the style, not what is going on — make sure the clip SHOWS the line").
Usage: uv run --with transformers --with torch --with pillow python tools/clipsheet.py <reel_dir> [per_sheet=8]
For each shot line in <reel>/shots.json: the candidates in clips/cand/NN that pass the Zoltium style gate (same gate as
pinfetch.py), best CLIP line-match first, top 8 → clips/sheets/NN.jpg (each clip = a labelled strip of 3 frames, A-H).
clips/sheets/index.json maps {NN: {say, q, clips: {A: {file, pin, start, style, clip_line}}}} for tools/clippick.py.
A Haiku judge then reads each sheet and writes clips/judge/NN.json (meaning + style scores per letter).
LINES=0,4 rebuilds only those sheets (after a re-search) and keeps the rest of index.json."""
import glob, json, os, re, subprocess, sys, tempfile
import torch
from PIL import Image, ImageDraw, ImageFont
from transformers import CLIPModel, CLIPProcessor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from activity import log

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
R = os.path.abspath(sys.argv[1]); K = int(sys.argv[2]) if len(sys.argv) > 2 else 8
shots = json.load(open(f"{R}/shots.json")); C = f"{R}/clips/cand"; S = f"{R}/clips/sheets"; os.makedirs(S, exist_ok=True)
m = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval(); p = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
def ie(ims):
    with torch.no_grad(): e = m.get_image_features(**p(images=ims, return_tensors="pt"))
    return torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1)
def te(t):
    with torch.no_grad(): e = m.get_text_features(**p(text=[t], return_tensors="pt", padding=True))
    return torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1)[0]
Z = torch.nn.functional.normalize(ie([Image.open(f).convert("RGB") for f in sorted(glob.glob(f"{ROOT}/library/style/zoltium/*.jpg"))]).mean(0), dim=-1)
BAD = te("a real photograph of a person, live action video, a watermark, text overlay, a logo")
pin = lambda f: (re.findall(r"pinterest_(\d+)", os.path.basename(f)) or [os.path.basename(f)])[0]

cache = {}   # one look per unique clip, even when Pinterest returned it for several lines
def look(f):
    if pin(f) in cache: return cache[pin(f)]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode().strip() or 0)
    fr = []
    with tempfile.TemporaryDirectory() as d:
        for k in range(6):
            t = dur * (k + 0.5) / 6
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-vf", "scale=400:-1", f"{d}/{k}.jpg"])
            if os.path.exists(f"{d}/{k}.jpg"): fr.append((t, Image.open(f"{d}/{k}.jpg").convert("RGB")))
    E = ie([im for _, im in fr]) if fr else None
    cache[pin(f)] = (dur, fr, E); return cache[pin(f)]

def keyed(fr):
    """share of the frame that is chroma-key green (saturated, bright, flat): an unfinished asset, not a scene"""
    out = []
    for _, im in fr:
        h, s_, v = [list(c.getdata()) for c in im.convert("HSV").split()]
        out.append(sum(1 for a, b, c in zip(h, s_, v) if 60 <= a <= 110 and b > 140 and c > 110) / len(h))
    return max(out) if out else 0
def short_side(f):
    w, h = map(int, subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", f]).decode().split(",")[:2])
    return min(w, h)

# POOL-WIDE search (owner 10-14: judges kept finding nothing on-meaning AND on-style in a shot's own 8 clips): every clip in
# reels/_pool is fingerprinted once (cached in _pool/emb.json) and each shot also gets the best matches from the WHOLE pool
POOLDIR = os.path.join(ROOT, "reels/_pool"); PCACHE = os.path.join(POOLDIR, "emb.json")
pcache = json.load(open(PCACHE)) if os.path.exists(PCACHE) else {}
def pool_index():
    changed = False
    for f in sorted(glob.glob(f"{POOLDIR}/*/*.mp4")):
        if pin(f) in pcache: continue
        try: dur, fr, E = look(f)
        except Exception: continue
        if not fr or dur < 1.2: pcache[pin(f)] = None; changed = True; continue
        style = float((E @ Z).mean()); bad = float((E @ BAD).mean())
        ok = style >= 0.70 and bad <= 0.27 and keyed(fr) <= 0.25 and short_side(f) >= 480
        pcache[pin(f)] = {"file": f, "dur": dur, "style": style, "ok": ok, "emb": [round(x, 4) for x in torch.nn.functional.normalize(E.mean(0), dim=-1).tolist()]}
        changed = True
    if changed: json.dump(pcache, open(PCACHE, "w"))
    return [v for v in pcache.values() if v and v["ok"] and os.path.exists(v["file"])]
POOL_OK = pool_index() if os.environ.get("POOLWIDE", "1") == "1" and os.path.isdir(POOLDIR) else []
PE = torch.tensor([v["emb"] for v in POOL_OK]) if POOL_OK else None
OFFERED = {}   # owner 10-14: one generic clip was the 'best match' for 9 shots — spread the pool across shots

FW, FH, LAB = 180, 240, 30
try: font = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", 24)
except OSError: font = ImageFont.load_default()
only = {int(x) for x in os.environ["LINES"].split(",")} if os.environ.get("LINES") else None   # re-judge just these lines
index = json.load(open(f"{S}/index.json")) if only and os.path.exists(f"{S}/index.json") else {}
for n, s in enumerate(shots):
    if s["q"] == "OUTRO" or (only and n not in only): continue
    L = te(f"a 2D cartoon animation of {s['q']}"); rows = []; seen = set()
    for f in sorted(glob.glob(f"{C}/{n:02d}/*.mp4")):
        if pin(f) in seen: continue
        seen.add(pin(f))
        try: dur, fr, E = look(f)
        except Exception: continue
        if not fr or dur < 1.2: continue
        style = float((E @ Z).mean()); bad = float((E @ BAD).mean())
        if style < 0.70 or bad > 0.27: continue
        if keyed(fr) > 0.25 or short_side(f) < 480: continue   # green-screen asset or a low-res source (owner 10-14)
        line = E @ L; i = int(torch.argmax(line))
        rows.append((float(line[i]) + 0.5 * (style - 0.70), f, fr, max(0.0, fr[i][0] - 0.6), style, float(line[i])))
    if PE is not None:   # + the best on-style matches from the whole pool (linked into this shot's folder, so the cutter finds them)
        sc = PE @ L + 0.5 * (torch.tensor([v["style"] for v in POOL_OK]) - 0.70)
        for j in torch.argsort(sc, descending=True).tolist()[:40]:
            v = POOL_OK[j]; f = v["file"]
            if pin(f) in seen or OFFERED.get(pin(f), 0) >= 2: continue   # a pool clip is offered to at most 2 shots per reel
            OFFERED[pin(f)] = OFFERED.get(pin(f), 0) + 1
            seen.add(pin(f)); dst = f"{C}/{n:02d}/{os.path.basename(f)}"
            if not os.path.exists(dst): os.makedirs(os.path.dirname(dst), exist_ok=True); os.link(f, dst)
            try: dur, fr, E = look(dst)
            except Exception: continue
            line = E @ L; i = int(torch.argmax(line))
            rows.append((float(line[i]) + 0.5 * (v["style"] - 0.70), dst, fr, max(0.0, fr[i][0] - 0.6), v["style"], float(line[i])))
            if sum(1 for r in rows if r[1].startswith(f"{C}/{n:02d}/")) >= 18: break
    rows.sort(key=lambda r: -r[0]); rows = rows[:K]
    entry = {"say": s["say"], "q": s["q"], "clips": {}}
    sheet = Image.new("RGB", (2 * 3 * FW + 20, ((len(rows) + 1) // 2) * (FH + LAB) or 10), (40, 40, 40)); dr = ImageDraw.Draw(sheet)
    for j, (_, f, fr, start, style, cl) in enumerate(rows):
        letter = "ABCDEFGH"[j]; x0, y0 = (j % 2) * (3 * FW + 20), (j // 2) * (FH + LAB)
        dr.text((x0 + 6, y0 + 2), f"{letter}", fill=(255, 220, 60), font=font)
        for k, idx in enumerate((0, len(fr) // 2, len(fr) - 1)):
            im = fr[idx][1].copy(); im.thumbnail((FW, FH))
            sheet.paste(im, (x0 + k * FW + (FW - im.width) // 2, y0 + LAB + (FH - im.height) // 2))
        entry["clips"][letter] = {"file": os.path.relpath(f, C), "pin": pin(f), "start": round(start, 2), "style": round(style, 3), "clip_line": round(cl, 3)}
    if rows: sheet.save(f"{S}/{n:02d}.jpg", quality=88)
    index[f"{n:02d}"] = entry
    log(f"Contact sheet · {os.path.basename(R)} · shot {n + 1} · {len(rows)} on-style clips")
    print(f"line {n:02d}: {len(rows)} on-style clips on the sheet  ({s['say']})", flush=True)
json.dump(index, open(f"{S}/index.json", "w"), indent=1, ensure_ascii=False)
