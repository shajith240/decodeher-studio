"""Music shortlist (owner 10-14: "15-20 tracks used at random, dark psychology / tense narration, no rock, not too upbeat").
Scores candidate beds against the automatable checklist in brain/research/sound-design-v2.md §3:
  fit by EAR (LAION CLAP: dark/tense/cinematic vs rock, pop, EDM, vocals, lo-fi, trailer brass) on 3 windows of the track,
  tempo (60-95 / 105-128, or half-time 130-150), minor mode (Krumhansl), brightness (centroid < 1.5 kHz),
  no sudden jumps (> 6 dB in 1 s), length ≥ 45 s.
Usage: uv run --python 3.11 --with transformers --with torch --with librosa --with soundfile python tools/music_rank.py <files...>
Prints a ranked table and writes library/music/candidates/ranked.json. The owner still picks by ear."""
import json, os, sys
import numpy as np, librosa, torch
from transformers import ClapModel, ClapProcessor

MODEL = "laion/larger_clap_general"; proc = ClapProcessor.from_pretrained(MODEL); model = ClapModel.from_pretrained(MODEL).eval()
GOOD = ["dark tense cinematic ambient music", "an ominous suspense underscore with a slow pulse", "a dark minimal trap instrumental with deep 808 bass",
        "mysterious dark piano with low strings", "a dark psychological thriller soundtrack"]
BAD = {"rock": "a rock band with electric guitars and drums", "vocals": "a person singing or rapping", "pop": "happy upbeat pop music",
       "edm": "energetic EDM dance music with a big drop", "lofi": "lofi chill hip hop with jazzy chords", "trailer": "an epic orchestral trailer with loud brass",
       "comedy": "funny cartoon comedy music", "metal": "heavy metal music"}
def temb(t):
    with torch.no_grad(): e = model.get_text_features(**proc(text=t, return_tensors="pt", padding=True))
    return torch.nn.functional.normalize(getattr(e, "pooler_output", e), dim=-1)
G, B = temb(GOOD), temb(list(BAD.values()))
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88]); MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

rows = []
for f in sys.argv[1:]:
    try: y, sr = librosa.load(f, sr=48000, mono=True)
    except Exception as e: print("skip", f, e); continue
    dur = len(y) / sr
    if dur < 20: continue
    wins = [y[int(s * sr): int(s * sr) + 10 * sr] for s in np.linspace(min(5, dur * 0.1), max(0, dur - 11), 3)]
    with torch.no_grad(): A = torch.nn.functional.normalize(getattr(e := model.get_audio_features(**proc(audio=wins, sampling_rate=48000, return_tensors="pt")), "pooler_output", e), dim=-1)
    good = float((A @ G.T).max(1).values.mean()); bads = (A @ B.T).mean(0).numpy(); worst = int(np.argmax(bads))
    y22 = librosa.resample(y, orig_sr=sr, target_sr=22050)
    tempo = float(np.atleast_1d(librosa.beat.beat_track(y=y22, sr=22050)[0])[0])
    chroma = librosa.feature.chroma_cqt(y=y22, sr=22050).mean(1)
    kmaj = max(np.corrcoef(chroma, np.roll(MAJ, k))[0, 1] for k in range(12)); kmin = max(np.corrcoef(chroma, np.roll(MIN, k))[0, 1] for k in range(12))
    cent = float(np.median(librosa.feature.spectral_centroid(y=y22, sr=22050)))
    rms = librosa.feature.rms(y=y22, frame_length=22050, hop_length=22050)[0]; ldb = 20 * np.log10(rms + 1e-6)
    jump = float(np.max(np.diff(ldb[ldb > ldb.max() - 40]))) if len(ldb) > 2 else 0
    tempo_ok = 60 <= tempo <= 95 or 105 <= tempo <= 128 or 130 <= tempo <= 150
    score = (good - float(bads.max())) * 10 + (0.6 if kmin > kmaj else -0.6) + (0.4 if tempo_ok else -0.8) \
            + (0.4 if cent < 1500 else -0.4 if cent < 2200 else -1.2) + (-0.8 if jump > 6 else 0) + (-2 if dur < 45 else 0)
    flags = [n for n, v in zip(BAD, bads) if v > good - 0.02]
    rows.append({"file": os.path.relpath(f), "score": round(score, 2), "dark_fit": round(good, 3), "worst": list(BAD)[worst], "worst_sim": round(float(bads.max()), 3),
                 "flags": flags, "tempo": round(tempo), "minor": bool(kmin > kmaj), "centroid": round(cent), "jump_db": round(jump, 1), "dur": round(dur)})
    print(f"{rows[-1]['score']:6.2f}  {os.path.basename(f)[:46]:46} fit {good:.2f} worst {list(BAD)[worst]} {bads.max():.2f} {round(tempo)}bpm "
          f"{'minor' if kmin > kmaj else 'MAJOR'} {round(cent)}Hz {'FLAGS ' + ','.join(flags) if flags else ''}", flush=True)
rows.sort(key=lambda r: -r["score"])
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../library/music/candidates/ranked.json"); os.makedirs(os.path.dirname(out), exist_ok=True)
json.dump(rows, open(out, "w"), indent=1)
print("\nRANKED:"); [print(f"{i + 1:2d}. {r['score']:5.2f}  {os.path.basename(r['file'])}  {r['flags'] or ''}") for i, r in enumerate(rows)]
