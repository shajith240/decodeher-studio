"""Find a sound effect by DESCRIPTION across every sound we own (owner 10-14: "use the sound effects according to the lines
the narrator is saying" — a snap, a phone buzz, typing, a clock — not one whoosh).
  uv run --python 3.11 --with transformers --with torch --with librosa --with soundfile python tools/sfx_find.py index
      listens once (LAION CLAP) to every file in library/sfx-user/raw, library/sfx-pro, library/sfx → library/sfx-index/
  ... python tools/sfx_find.py find "a single finger snap" [k] [--not "applause,a person speaking"]
  ... python tools/sfx_find.py role <name> "<description>" [k] [--not "..."]
      adds the top k as a new role in library/sfx-brand/ranked.json (copied, trimmed to ≤ 6 s, 48 kHz) for tools/reel_mix.py"""
import glob, json, os, subprocess, sys
import numpy as np, librosa, torch
from transformers import ClapModel, ClapProcessor

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); IDX = os.path.join(ROOT, "library/sfx-index")
MODEL = "laion/larger_clap_general"; dev = "cuda" if torch.cuda.is_available() else "cpu"
proc = ClapProcessor.from_pretrained(MODEL); model = ClapModel.from_pretrained(MODEL).eval().to(dev)
def temb(t):
    with torch.no_grad(): e = model.get_text_features(**{k: v.to(dev) for k, v in proc(text=t, return_tensors="pt", padding=True).items()})
    return torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1).cpu().numpy()

cmd = sys.argv[1]
if cmd == "index":
    files = sorted(f for d in ("library/sfx-user/raw", "library/sfx-pro", "library/sfx") for f in glob.glob(os.path.join(ROOT, d, "**/*"), recursive=True)
                   if f.lower().endswith((".wav", ".mp3", ".ogg", ".flac", ".aif", ".aiff", ".m4a")) and os.path.getsize(f) > 2000)
    os.makedirs(IDX, exist_ok=True); keep, embs, durs = [], [], []
    for i, f in enumerate(files):
        try: y, _ = librosa.load(f, sr=48000, mono=True, duration=10)
        except Exception: continue
        if len(y) < 2400: continue
        with torch.no_grad(): e = model.get_audio_features(**{k: v.to(dev) for k, v in proc(audio=[y], sampling_rate=48000, return_tensors="pt").items()})
        embs.append(torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1).cpu().numpy()[0]); keep.append(os.path.relpath(f, ROOT))
        durs.append(round(librosa.get_duration(path=f), 2))
        if i % 250 == 0: print(f"{i}/{len(files)}", flush=True)
    np.save(os.path.join(IDX, "emb.npy"), np.array(embs, np.float32)); json.dump({"files": keep, "dur": durs}, open(os.path.join(IDX, "files.json"), "w"))
    print(f"indexed {len(keep)} sounds"); sys.exit()

E = np.load(os.path.join(IDX, "emb.npy")); meta = json.load(open(os.path.join(IDX, "files.json"))); F, D = meta["files"], meta["dur"]
args = sys.argv[2:]; neg = []
if "--not" in args: i = args.index("--not"); neg = [x.strip() for x in args[i + 1].split(",")]; args = args[:i] + args[i + 2:]
def rank(desc, k, max_dur=8.0):
    P = temb([desc])[0]; s = E @ P
    if neg: s = s - 0.6 * np.clip((E @ temb(neg).T).max(1) - 0.1, 0, None)
    order = [j for j in np.argsort(-s) if D[j] <= max_dur]
    out, seen = [], set()
    for j in order:   # skip the same sound saved twice ("Copy of X", x.wav and x.mp3)
        key = os.path.splitext(os.path.basename(F[j]))[0].lower().replace("copy of ", "").strip()
        if key in seen: continue
        seen.add(key); out.append((float(s[j]), F[j]))
        if len(out) >= k: break
    return out
if cmd == "find":
    for sc, f in rank(args[0], int(args[1]) if len(args) > 1 else 8): print(f"{sc:.3f}  {f}")
elif cmd == "role":
    name, desc, k = args[0], args[1], int(args[2]) if len(args) > 2 else 6
    rk = os.path.join(ROOT, "library/sfx-brand/ranked.json"); ranked = json.load(open(rk)); d = os.path.join(ROOT, "library/sfx-brand", name)
    os.makedirs(d, exist_ok=True); ranked[name] = []
    for i, (sc, f) in enumerate(rank(desc, k)):
        dst = os.path.join(d, f"{i + 1:02d}-{os.path.splitext(os.path.basename(f))[0][:40].replace(' ', '-')}.wav")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", os.path.join(ROOT, f), "-t", "6", "-ar", "48000", "-ac", "2", dst], check=True)
        ranked[name].append(os.path.relpath(dst, ROOT)); print(f"{sc:.3f}  {f}")
    json.dump(ranked, open(rk, "w"), indent=1); print(f"role {name}: {len(ranked[name])} sounds")
