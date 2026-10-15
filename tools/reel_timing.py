"""Timing + audio mix for a Spot the Con reel. Usage: python3 tools/reel_timing.py <reel_dir>
Reads <reel>/assets/vo/lNN.wav + script.json (+ optional <reel>/reel.json "gaps"), writes
  assets/timing.js   window.T = { total, vo:[start], voEnd:[end], words:[[ [word,start,end], ...], ...] }
  assets/audio/mix.wav  voice + one continuous music bed, smooth ducking envelope, peak-limited, -14 LUFS / -1 dBTP
Voice starts at frame 0 (hook rule). Word times are spread over each line by character length (good enough for
captions that highlight the spoken word; no forced alignment needed)."""
import json, os, re, subprocess, sys

R = os.path.abspath(sys.argv[1]); os.chdir(R)
cfg = json.load(open("reel.json")) if os.path.exists("reel.json") else {}
lines = [l["text"] if isinstance(l, dict) else l for l in json.load(open("assets/vo/script.json"))]   # lines may carry delivery marks
dur = lambda f: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))
n = len(lines)
vo_len = [round(dur(f"assets/vo/l{i+1:02d}.wav"), 3) for i in range(n)]
gaps = cfg.get("gaps", [0.45] * n)          # pause after each line (scene changes live in these gaps)
start, t = [], cfg.get("lead", 0.12)
for i in range(n):
    start.append(round(t, 3)); t += vo_len[i] + gaps[i]
end = [round(s + d, 3) for s, d in zip(start, vo_len)]
TOTAL = round(end[-1] + cfg.get("tail", 2.2), 2)

words = []
for i, text in enumerate(lines):
    ws = re.findall(r"\S+", text)
    weights = [len(w) + 2 for w in ws]; tot = sum(weights); a = start[i]
    row = []
    for w, k in zip(ws, weights):
        b = a + vo_len[i] * k / tot
        row.append([w, round(a, 3), round(b, 3)]); a = b
    words.append(row)

T = {"total": TOTAL, "vo": start, "voEnd": end, "words": words}
open("assets/timing.js", "w").write("window.T = " + json.dumps(T) + ";\n")
# clip reels (owner 10-14): the real sound is tools/reel_mix.py → assets/audio/final.wav. The old rough preview (premix/mix.wav,
# an undifferentiated music + voice sum) only confused people ("mix.wav has a hum"), so it is no longer written.
print(json.dumps({"total": T["total"], "lines": [[a, b] for a, b in zip(T["vo"], T["voEnd"])]})); sys.exit(0)

music = cfg.get("music", "assets/audio/music.mp3")
if not os.path.exists(music):   # a library id (new pipeline: tools/reel_mix.py does the real mix) → rough premix uses the file it names
    _idx = json.load(open(os.path.join(os.path.dirname(__file__), "../library/music/index.json")))
    music = os.path.join(os.path.dirname(__file__), "../library/music", _idx[music]["file"]) if music in _idx else music
if not os.path.exists(music):   # "auto" / approved-library pick: the rough premix uses any approved track (reel_mix.py picks the real one)
    _ap = os.path.join(os.path.dirname(__file__), "../library/music/approved"); _a = json.load(open(os.path.join(_ap, "index.json")))
    music = os.path.join(_ap, _a[music]["file"] if music in _a else sorted(_a.values(), key=lambda v: v["file"])[0]["file"])
m_in = cfg.get("music_in", 0); vol = cfg.get("music_vol", 0.42)
inp, fc = [], []
for i, s in enumerate(start):
    inp += ["-i", f"assets/vo/l{i+1:02d}.wav"]
    fc.append(f"[{i}]adelay={int(s*1000)}|{int(s*1000)},apad=whole_dur={TOTAL}[v{i}]")
fc.append("".join(f"[v{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,atrim=0:{TOTAL}[vo]")
# music bed: ONE continuous take; its volume follows a smooth envelope from the speech windows (no sidechain pumping).
# Speech windows closer than 1.2 s are merged, so the music stays down through a run of lines and only lifts in real pauses.
segs = []
for s0, e0 in zip(start, end):
    if segs and s0 - segs[-1][1] < 1.2: segs[-1][1] = e0
    else: segs.append([s0, e0])
duck = "+".join(f"clip((t-{a-0.35:.3f})/0.35,0,1)*clip(({b+0.5:.3f}-t)/0.5,0,1)" for a, b in segs) or "0"
lo, hi = cfg.get("music_duck", 0.16), vol
inp += ["-ss", str(m_in), "-t", str(TOTAL), "-i", music]
fc.append(f"[{n}]volume='{hi}-({hi}-{lo})*min(1,{duck})':eval=frame,afade=t=in:d=0.4,afade=t=out:st={TOTAL-1.8}:d=1.8[duck]")
fc.append(f"[vo][duck]amix=inputs=2:normalize=0,atrim=0:{TOTAL}[mix]")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", *inp, "-filter_complex", ";".join(fc), "-map", "[mix]", "-ar", "48000", "assets/audio/premix.wav"], check=True)
# master: measure, gain to -14 LUFS, then a true-peak limiter at -1.5 dBFS (oversampled). Repeat once if the limiter
# pulled the loudness down by more than 0.5 LU.
def integrated(f):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
gain = -14.0 - integrated("assets/audio/premix.wav")
for _ in range(3):
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", "assets/audio/premix.wav", "-af",
                    f"volume={gain:.2f}dB,aresample=192000,alimiter=limit=0.84:attack=2:release=50:level=disabled,aresample=48000",
                    "assets/audio/mix.wav"], check=True)
    miss = -14.0 - integrated("assets/audio/mix.wav")
    if abs(miss) <= 0.5: break
    gain += miss
def qa(f):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "silencedetect=n=-50dB:d=0.12,ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    drop = [l for l in o.splitlines() if "silence_start" in l and float(l.split()[-1]) < TOTAL - 2.5]
    I = float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    peak = float([l for l in o.splitlines() if l.strip().startswith("Peak:")][-1].split()[1])
    bad = (["audio drops out mid-reel"] if drop else []) + ([f"loudness {I} LUFS"] if abs(I + 14) > 1 else []) + ([f"true peak {peak} dBFS"] if peak > -0.8 else [])
    return I, peak, bad
I, peak, bad = qa("assets/audio/mix.wav")
print(json.dumps({"total": TOTAL, "lines": list(zip(start, end)), "loudness": I, "truepeak": peak, "audio_ok": not bad}))
if bad: sys.exit("audio QA failed: " + "; ".join(bad))
