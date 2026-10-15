"""The clip library (owner, 10-14): every good Zoltium-style clip we find is kept — named by what it shows — in Google Drive
(gdrive:DecodeHer/clip-library, via rclone), with a small local index so a new reel searches our own library first.
  uv run --with transformers --with torch --with pillow python tools/cliplib.py add <reel_dir>      keep a reel's good clips
  uv run ... python tools/cliplib.py search "<what the line shows>" [k]                            best matches (by sight)
  uv run ... python tools/cliplib.py get <name> <dest_dir>                                         download one clip from Drive
Kept: every clip the reel used + clips the Haiku judges passed (style ≥ 6, quality ≥ 6, no text), named by the judges' description
of what happens. Stored lighter (720p, crf 27).
Index: library/clips/index.json [{name, desc, line, meaning, quality, style, source, used_in}] + library/clips/emb.json (CLIP image fingerprints)."""
import glob, json, os, re, subprocess, sys
import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); LIB = f"{ROOT}/library/clips"; os.makedirs(LIB, exist_ok=True)
RC = os.path.expanduser("~/.local/bin/rclone"); REMOTE = "gdrive:DecodeHer/clip-library"
IDX, EMB = f"{LIB}/index.json", f"{LIB}/emb.json"
index = json.load(open(IDX)) if os.path.exists(IDX) else []; emb = json.load(open(EMB)) if os.path.exists(EMB) else {}
m = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval(); p = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
def ie(ims):
    with torch.no_grad(): e = m.get_image_features(**p(images=ims, return_tensors="pt"))
    return torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1)
def te(t):
    with torch.no_grad(): e = m.get_text_features(**p(text=[t], return_tensors="pt", padding=True))
    return torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1)[0]
def frames(f, k=4):
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode().strip() or 0)
    ims = []
    for i in range(k):
        tmp = f"{LIB}/_f.jpg"
        if os.path.exists(tmp): os.remove(tmp)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{d * (i + .5) / k:.2f}", "-i", f, "-frames:v", "1", "-vf", "scale=336:-1", tmp])
        if os.path.exists(tmp): ims.append(Image.open(tmp).convert("RGB"))
    return d, ims
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]
save = lambda: (json.dump(index, open(IDX, "w"), indent=1), json.dump(emb, open(EMB, "w")))

cmd = sys.argv[1]
if cmd == "add":   # keep what the Haiku judges passed (style ≥ 6, quality ≥ 6, no text) + every clip the reel used, named by what HAPPENS
    R = os.path.abspath(sys.argv[2]); pick = json.load(open(f"{R}/clips/pick.json")); sheets = json.load(open(f"{R}/clips/sheets/index.json"))
    Z = torch.nn.functional.normalize(ie([Image.open(f).convert("RGB") for f in sorted(glob.glob(f"{ROOT}/library/style/zoltium/*.jpg"))]).mean(0), dim=-1)
    have = {e["source"] for e in index}; staged = f"{LIB}/_up"; os.makedirs(staged, exist_ok=True); added = 0
    used = {os.path.basename(p_["file"]) for p_ in pick.values()}
    for nn, e in sheets.items():
        jf = f"{R}/clips/judge/{nn}.json"; j = json.load(open(jf))["clips"] if os.path.exists(jf) else {}
        for letter, c in e["clips"].items():
            v = j.get(letter); f = f"{R}/clips/cand/{c['file']}"; src = os.path.basename(f)
            if src in have or not os.path.exists(f) or not v: continue
            picked = src in used
            if not picked and (v.get("style", 0) < 6 or v.get("quality", 6) < 6 or v.get("text")): continue
            try: d, ims = frames(f)
            except Exception: continue
            if not ims: continue
            E = ie(ims); name = f"{slug(v['shows'])}__{c['pin']}.mp4"; have.add(src)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f, "-vf", "scale=-2:'min(720,ih)'", "-c:v", "libx264", "-crf", "27", "-preset", "medium", "-an", f"{staged}/{name}"], check=True)
            index.append({"name": name, "desc": v["shows"], "line": e["say"], "meaning": v.get("meaning"), "judged_style": v.get("style"), "quality": v.get("quality"),
                          "style": round(float((E @ Z).mean()), 3), "picked": picked, "source": src, "pin": f"https://www.pinterest.com/pin/{c['pin']}/",
                          "dur": round(d, 2), "used_in": [os.path.basename(R)] if picked else []})
            emb[name] = [round(x, 5) for x in E.mean(0).tolist()]; added += 1
    subprocess.run([RC, "copy", staged, REMOTE, "-q"], check=True)
    for x in glob.glob(f"{staged}/*.mp4"): os.remove(x)
    save(); print(f"added {added} clips to {REMOTE} (library now {len(index)})")
elif cmd == "search":
    q = sys.argv[2]; k = int(sys.argv[3]) if len(sys.argv) > 3 else 5; T = te(f"a 2D cartoon animation of {q}")
    rows = sorted(((float(torch.tensor(emb[e["name"]]) @ T) + 0.3 * e["style"], e) for e in index if e["name"] in emb), key=lambda r: -r[0])[:k]
    for sc, e in rows: print(f"{sc:.3f}  {e['name']}  (style {e['style']}, {e['dur']}s)")
elif cmd == "get":
    subprocess.run([RC, "copy", f"{REMOTE}/{sys.argv[2]}", sys.argv[3], "-q"], check=True); print("ok")
