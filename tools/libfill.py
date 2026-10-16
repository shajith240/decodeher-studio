"""Fill a reel's clip candidates from OUR OWN clips, no Pinterest (owner 10-17: Pinterest search went down; "use the clips we have").
Usage: uv run -q --with torch --with transformers --with pillow python tools/libfill.py <reel_dir> [per_shot=8]
Our clips = the shared pool reels/_pool (every past search, fingerprinted in reels/_pool/emb.json by tools/clipsheet.py) + the
owner's Telegram clips (library/clips/inbox/dark-*.mp4, linked into reels/_pool/telegram-dark/ so they get fingerprinted too).
For every shot that has NO candidates yet: rank the pool's style-passed clips by how well they show the shot's picture (CLIP text
vs image), skip clips OCR already marked as having text (library/clip-text.json), hard-link the best per_shot into clips/cand/NN/.
Shots that already have candidates are left alone, so this also works as the fallback after a Pinterest fetch that came back empty.
tools/clipsheet.py, the judges and tools/clippick.py then run exactly as usual (the whole pool is still offered per shot)."""
import glob, json, os, subprocess, sys
import torch
from transformers import CLIPModel, CLIPProcessor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
R = os.path.abspath(sys.argv[1]); PER = int(sys.argv[2]) if len(sys.argv) > 2 else 8
POOL = f"{ROOT}/reels/_pool"; PCACHE = f"{POOL}/emb.json"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from activity import log

# owner's Telegram clips join the pool (hard links: no extra disk); clipsheet fingerprints new pool files on its next run
tg = f"{POOL}/telegram-dark"; os.makedirs(tg, exist_ok=True)
for f in glob.glob(f"{ROOT}/library/clips/inbox/dark-*.mp4"):
    dst = f"{tg}/{os.path.basename(f)}"
    if not os.path.exists(dst):
        try: os.link(f, dst)
        except OSError: pass

shots = json.load(open(f"{R}/shots.json"))
todo = [n for n, s in enumerate(shots) if s["q"] != "OUTRO" and not glob.glob(f"{R}/clips/cand/{n:02d}/*.mp4")]
if not todo: print("every shot already has candidates"); sys.exit(0)

pcache = json.load(open(PCACHE)) if os.path.exists(PCACHE) else {}
# pool files without a fingerprint yet (e.g. new Telegram clips) are fingerprinted by clipsheet.py at the sheets step and offered
# pool-wide there; here we rank only what is already fingerprinted
ok = [v for v in pcache.values() if v and v.get("ok") and os.path.exists(v["file"])]
TX = json.load(open(f"{ROOT}/library/clip-text.json")) if os.path.exists(f"{ROOT}/library/clip-text.json") else {}
ok = [v for v in ok if not TX.get(os.path.basename(v["file"]), [False])[0]]
if not ok: sys.exit("no fingerprinted pool clips to choose from")
E = torch.tensor([v["emb"] for v in ok])
m = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").eval(); p = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
def te(t):
    with torch.no_grad(): e = m.get_text_features(**p(text=[t], return_tensors="pt", padding=True))
    return torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1)[0]

used = {}   # a pool clip goes to at most 2 shots of this reel (clippick later uses each pin once)
for n in todo:
    s = shots[n]; T = te(f"a 2D cartoon animation of {s['q']}")
    score = (E @ T) + 0.15 * torch.tensor([v["style"] for v in ok])
    d = f"{R}/clips/cand/{n:02d}"; os.makedirs(d, exist_ok=True); k = 0
    for i in torch.argsort(score, descending=True).tolist():
        f = ok[i]["file"]
        if used.get(f, 0) >= 2: continue
        dst = f"{d}/{os.path.basename(f)}"
        try: os.link(f, dst)
        except FileExistsError: pass
        except OSError: subprocess.run(["cp", "--reflink=auto", f, dst], check=True)
        used[f] = used.get(f, 0) + 1; k += 1
        if k >= PER: break
    print(f"line {n:02d}: {k} clips from our pool  ({s['q']})", flush=True)
log(f"Clips from our own library · {os.path.basename(R)} · {len(todo)} shots (no Pinterest)")
