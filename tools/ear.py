"""The ear: judge sounds by what they ARE, not by their waveform statistics (owner, 10-14: "you should be able to hear it and
understand the psychology and the use of that particular sound"). Uses LAION CLAP (audio↔text embeddings) to score each
sound against descriptions of what it should be and what it must not be.
  uv run --with transformers --with torch --with librosa --with soundfile python tools/ear.py rank <category> <files...>
  uv run ... python tools/ear.py describe <file> [start end]         → the best-matching descriptions from a vocabulary
The category prompts live in ROLES below; each pairs the sound's JOB (its psychological use) with quality anti-prompts."""
import json, sys, numpy as np, librosa, torch
from transformers import ClapModel, ClapProcessor

MODEL = "laion/larger_clap_general"
ROLES = {   # job → (what it should sound like, what it must not sound like)
    "whoosh-soft": (["a smooth soft airy whoosh transition sound", "a subtle cinematic swish"], ["a cartoon swoosh", "wind noise", "harsh distorted noise", "a person speaking"]),
    "whoosh-heavy": (["a heavy deep cinematic whoosh", "a powerful dark swoosh transition"], ["a cartoon swoosh", "a car passing by", "a person speaking"]),
    "riser": (["a cinematic tension riser building up", "a rising suspense sound effect"], ["a siren", "a happy upbeat sound", "a person speaking"]),
    "reverse-swell": (["a reverse cymbal swell into a hit", "a reversed reverb swell"], ["a cartoon sound", "a person speaking"]),
    "impact": (["a deep cinematic impact boom with a long tail", "a dark trailer hit"], ["a door slam", "a gunshot", "a cartoon bonk", "a person speaking"]),
    "sub-drop": (["a deep sub bass drop", "an 808 bass drop"], ["a cartoon sound", "a person speaking"]),
    "braam": (["a dark cinematic braam", "an ominous low brass hit"], ["a car horn", "a person speaking"]),
    "drone": (["a dark ominous tension drone", "an eerie ambient drone"], ["a happy melody", "an engine", "a person speaking"]),
    "glitch": (["a short digital glitch stutter", "an electronic glitch transition"], ["a person speaking", "a cartoon sound"]),
    "ui-tick": (["a subtle premium user interface click", "a soft clean tick sound"], ["a loud bang", "a person speaking"]),
    "notification": (["a soft phone message notification sound", "a gentle chat message pop", "a soft bubble pop user interface sound"], ["an alarm", "a ringtone melody", "a person speaking"]),
    "heartbeat": (["a slow tense heartbeat"], ["a drum beat", "a person speaking"]),
    "clock": (["a clock ticking"], ["a metronome beep", "a person speaking"]),
    "breath": (["a quiet tense breath"], ["a person speaking", "a cough"]),
    "stinger": (["a short dark cinematic stinger hit", "a tense musical sting"], ["a cartoon jingle", "a person speaking"]),
    "room-tone": (["a quiet night room ambience", "a soft city night ambience"], ["loud traffic", "music", "a person speaking"]),
    "paper-cloth": (["soft cloth movement", "a paper rustle"], ["a person speaking", "a loud bang"]),
    "glass": (["a sharp glass window shattering into pieces", "glass breaking"], ["a bottle clinking", "wind chimes", "a lightbulb popping", "a person speaking", "a cartoon sound"]),
    "music-dark": (["a dark tense trap beat with deep 808 bass", "an ominous cinematic hip hop instrumental"], ["happy upbeat pop music", "a person singing", "lofi chill music"]),
}
VOCAB = sorted({p for pos, neg in ROLES.values() for p in pos + neg} | {"silence", "music", "a man speaking with a deep voice", "a whoosh", "an explosion", "a deep male voice narrating over a dark tense beat", "a deep male voice over calm ambient music", "a dramatic cinematic moment", "a messy cluttered noisy mix", "a cheap amateur video soundtrack", "a premium cinematic trailer"})

proc = ClapProcessor.from_pretrained(MODEL); model = ClapModel.from_pretrained(MODEL).eval()
def audio_emb(path, a=None, b=None):
    y, _ = librosa.load(path, sr=48000, mono=True, offset=a or 0, duration=(b - a) if a is not None and b else None)
    y = y[: 48000 * 10] if len(y) else np.zeros(48000, np.float32)
    with torch.no_grad():
        e = model.get_audio_features(**proc(audio=[y], sampling_rate=48000, return_tensors="pt"))
    e = getattr(e, "pooler_output", e)
    return torch.nn.functional.normalize(e, dim=-1)[0]
def text_emb(texts):
    with torch.no_grad():
        e = model.get_text_features(**proc(text=texts, return_tensors="pt", padding=True))
    e = getattr(e, "pooler_output", e)
    return torch.nn.functional.normalize(e, dim=-1)

cmd = sys.argv[1]
if cmd == "curate":   # build library/sfx-brand: per job, audition candidates from every source, keep the best K by ear
    import glob, os, shutil, subprocess
    root = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")); L = lambda *g: [f for x in g for f in glob.glob(os.path.join(root, x), recursive=True)]
    U5, UT, PRO = "library/sfx-user/raw/pack500/500+ Sound Effects ", "library/sfx-user/raw/packtg/SFX Pack", "library/sfx-pro"
    AUD = lambda d: [f for f in L(d + "/**/*") if f.lower().endswith((".wav", ".mp3", ".m4a", ".aif", ".aiff", ".ogg", ".flac"))]
    name_has = lambda files, *keys: [f for f in files if any(k in os.path.basename(f).lower() for k in keys)]
    ALL_USER = AUD(U5) + AUD(UT)
    POOL = {
      "whoosh-soft": AUD(U5 + "/Whoosh") + AUD(U5 + "/Transition SFX") + name_has(AUD(U5 + "/Other"), "whoosh", "swoosh") + AUD(UT + "/Whoosh") + AUD(PRO + "/whoosh-soft"),
      "whoosh-heavy": AUD(U5 + "/Whoosh") + AUD(U5 + "/Transition SFX") + AUD(U5 + "/Cinematic SFX") + name_has(AUD(U5 + "/Other"), "whoosh") + AUD(PRO + "/whoosh-heavy"),
      "riser": AUD(U5 + "/Risers") + AUD(UT + "/Risers") + AUD(PRO + "/riser"),
      "reverse-swell": name_has(ALL_USER, "reverse", "swell", "suck") + AUD(PRO + "/reverse-swell"),
      "impact": AUD(U5 + "/Hits") + AUD(U5 + "/Cinematic SFX") + name_has(ALL_USER, "impact", "boom", "hit") + AUD(PRO + "/impact-cinematic"),
      "braam": AUD(U5 + "/Cinematic SFX") + name_has(ALL_USER, "braam", "brass", "horn hit", "trailer") + AUD(PRO + "/braam"),
      "sub-drop": name_has(ALL_USER, "sub", "808", "bass drop", "drop") + AUD(PRO + "/sub-drop"),
      "glitch": AUD(U5 + "/Glitch") + AUD(UT + "/Digital") + AUD(PRO + "/glitch"),
      "glass": name_has(ALL_USER, "glass", "shatter", "break") + AUD("library/sfx-pro/glass"),
      "notification": AUD(UT + "/Notifications") + AUD(UT + "/Phone") + name_has(ALL_USER, "message", "notif", "pop") + L("library/sfx/notification-*.mp3"),
      "ui-tick": AUD(U5 + "/User Interface (UI)") + AUD(UT + "/Button") + AUD(UT + "/Switch") + AUD(PRO + "/ui-tick"),
      "drone": AUD(U5 + "/Atmosphere") + name_has(AUD(UT + "/Ambience"), "drone", "dark", "tension", "eerie") + AUD(PRO + "/tension-drone"),
      "room-tone": AUD(UT + "/Ambience") + name_has(AUD(U5 + "/Atmosphere"), "room", "night", "city") + AUD(PRO + "/room-tone"),
      "stinger": AUD(U5 + "/Cinematic SFX") + AUD(PRO + "/stinger"),
      "camera": AUD(U5 + "/Camera Effects") + AUD(UT + "/Camera"),
      "heartbeat": name_has(ALL_USER, "heart") + AUD(PRO + "/heartbeat"),
      "clock": name_has(ALL_USER, "clock", "tick tock") + AUD(PRO + "/clock"),
    }
    ROLES.setdefault("camera", (["a camera shutter click"], ["a gunshot", "a person speaking"]))
    K = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    out_dir = os.path.join(root, "library/sfx-brand"); os.makedirs(out_dir, exist_ok=True)
    ranked, index, report = {}, [], {}
    for role, files in POOL.items():
        files = sorted(set(f for f in files if os.path.getsize(f) > 2000))[:400]
        pos, neg = ROLES[role]; P, N = text_emb(pos), text_emb(neg); rows = []
        for f in files:
            try: a = audio_emb(f)
            except Exception: continue
            sp = float((P @ a).max()); sn = float((N @ a).max())
            if sp > sn: rows.append((sp - 0.6 * max(0, sn - 0.1), sp, sn, f))
        rows.sort(reverse=True); keep = rows[:K]; os.makedirs(os.path.join(out_dir, role), exist_ok=True); ranked[role] = []
        for i, (sc, sp, sn, f) in enumerate(keep):
            src = "user-pack (licence unknown)" if "sfx-user" in f else ("Sonniss GDC / Mixkit (commercial, no credit)" if "sfx-pro" in f else "freesound CC0")
            base = os.path.splitext(os.path.basename(f))[0].replace("Copy of ", "")[:48].strip().replace(" ", "-")
            dst = os.path.join(out_dir, role, f"{i + 1:02d}-{base}.wav")
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f, "-t", "20", "-ar", "48000", "-ac", "2", dst], check=True)
            rel = os.path.relpath(dst, root); ranked[role].append(rel)
            index.append({"role": role, "file": rel, "score": round(sc, 3), "fit": round(sp, 3), "worst_negative": round(sn, 3), "source": src, "original": os.path.relpath(f, root)})
        report[role] = f"{len(files)} auditioned, {len(rows)} fit, kept {len(keep)}: " + ", ".join(f"{os.path.basename(r[3])[:30]} ({r[1]:.2f})" for r in keep)
    json.dump(ranked, open(os.path.join(out_dir, "ranked.json"), "w"), indent=1); json.dump(index, open(os.path.join(out_dir, "index.json"), "w"), indent=1)
    print("\n".join(f"{k}: {v}" for k, v in report.items())); sys.exit()
if cmd == "rankall":   # rank every category folder in library/sfx-pro by ear → library/sfx-pro/ranked.json (best first, misfits dropped)
    import glob, os
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); base = os.path.join(root, "library/sfx-pro")
    ALIAS = {"impact-cinematic": "impact", "tension-drone": "drone", "phone": "notification", "reverse-swell": "reverse-swell"}
    out, report = {}, {}
    for d in sorted(os.listdir(base)):
        if not os.path.isdir(os.path.join(base, d)): continue
        role = ALIAS.get(d, d)
        if role not in ROLES: continue
        pos, neg = ROLES[role]; P, N = text_emb(pos), text_emb(neg); rows = []
        for f in sorted(glob.glob(os.path.join(base, d, "*"))):
            a = audio_emb(f); sp = float((P @ a).max()); sn = float((N @ a).max())
            rows.append((sp - 0.6 * max(0, sn - 0.1), sp, sn, os.path.relpath(f, root)))
        rows.sort(reverse=True)
        out[role] = [r[3] for r in rows if r[1] > r[2]]   # a sound that matches a must-not description better than its job is dropped
        report[role] = [[os.path.basename(r[3]), round(r[1], 2), round(r[2], 2)] for r in rows]
    json.dump(out, open(os.path.join(base, "ranked.json"), "w"), indent=1)
    print(json.dumps(report, indent=0)); sys.exit()
if cmd == "moments":   # listen to several windows of one file: describe <file> a-b a-b ...
    f = sys.argv[2]; T_ = text_emb(VOCAB)
    for w in sys.argv[3:]:
        a, b = map(float, w.split("-")); sims = (T_ @ audio_emb(f, a, b)).numpy(); top = np.argsort(-sims)[:4]
        print(f"{w:>9}  " + " | ".join(f"{VOCAB[i]} {sims[i]:.2f}" for i in top))
    sys.exit()
if cmd == "rank":
    cat, files = sys.argv[2], sys.argv[3:]
    pos, neg = ROLES[cat]; P, N = text_emb(pos), text_emb(neg)
    rows = []
    for f in files:
        a = audio_emb(f); sp = float((P @ a).max()); sn = float((N @ a).max())
        rows.append({"file": f, "fit": round(sp, 3), "worst_negative": round(sn, 3), "score": round(sp - 0.6 * max(0, sn - 0.1), 3)})
    rows.sort(key=lambda r: -r["score"]); print(json.dumps(rows, indent=1))
elif cmd == "describe":
    f = sys.argv[2]; a = float(sys.argv[3]) if len(sys.argv) > 3 else None; b = float(sys.argv[4]) if len(sys.argv) > 4 else None
    sims = (text_emb(VOCAB) @ audio_emb(f, a, b)).numpy(); top = np.argsort(-sims)[:5]
    print(json.dumps([[VOCAB[i], round(float(sims[i]), 3)] for i in top]))
