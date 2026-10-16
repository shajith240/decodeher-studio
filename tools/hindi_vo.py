"""Hindi narration with the LOCKED recipe (owner approved 10-16, brain/rules/hindi-script-rules.md).
Usage: uv run -q --with numpy --with soundfile python tools/hindi_vo.py <lines.txt> <out_base> [--redo]
lines.txt = one sentence per line in Devanagari; a BLANK line marks a section break (after the hook turn, the verdict, each move,
the payoff) and gets the longer pause. Writes <out_base>.wav, <out_base>.mp3 and <out_base>.json (each line's start/end in seconds).
Steps: ONE whole Fish take (janam, no tags, speed 1.0, temp 0.6, top_p 0.7, normalize off, chunk 300) -> tools/vo_split.py (lang hi)
finds each sentence -> light pauses added in post (~0.2 s in a section, ~0.45 s at a break, +-40 ms jitter, none inside the opening
question) -> every silence capped at 0.6 s -> 70 Hz low-cut (Fish hum) -> compressor + limiter to about -11.5 LUFS, true peak <= -1 dBTP.
FISH_API_KEY comes from the environment or the nearest .env (never printed)."""
import hashlib, json, os, random, re, subprocess, sys, tempfile, time, urllib.request
import numpy as np, soundfile as sf

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICE = "2f4654989a3147b0a775db4f9a13ae74"   # Fish "janam"
SR = 48000
IN_SECTION, AT_BREAK, JITTER, CAP = 0.20, 0.45, 0.04, 0.60
CACHE = f"{R}/library/vo-cache/hindi"


def key():
    if os.environ.get("FISH_API_KEY"): return os.environ["FISH_API_KEY"]
    d = R
    while d != "/":
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            for line in open(p):
                if line.startswith("FISH_API_KEY="): return line.split("=", 1)[1].strip().strip('"')
        d = os.path.dirname(d)
    sys.exit("FISH_API_KEY not found")


def tts(text, out):
    body = json.dumps({"text": text, "reference_id": VOICE, "format": "wav", "latency": "normal", "normalize": False,
                       "chunk_length": 300, "temperature": 0.6, "top_p": 0.7, "prosody": {"speed": 1.0, "volume": 0}}).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request("https://api.fish.audio/v1/tts", method="POST", data=body,
                                         headers={"Authorization": f"Bearer {key()}", "Content-Type": "application/json", "model": "s2.1-pro-free"})
            data = urllib.request.urlopen(req, timeout=240).read()   # fetch first: a failure never leaves a broken file in the cache
            if len(data) < 4000: raise ValueError(f"Fish returned only {len(data)} bytes")
            open(out + ".part", "wb").write(data); os.replace(out + ".part", out); return
        except Exception:
            if attempt == 3: raise
            time.sleep(5 * (attempt + 1))


def loudness(f):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    tail = o[o.rfind("Summary:"):]
    return float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1)), float(re.search(r"Peak:\s+(-?[\d.inf]+) dBFS", tail).group(1))


def cap_silences(a, cap=CAP, thr_db=-45.0, win=0.02):
    """Shorten every quiet run longer than `cap` seconds to `cap` (cut from its middle, so word tails and breaths stay)."""
    n = int(win * SR); frames = len(a) // n
    rms = np.sqrt(np.mean(a[:frames * n].reshape(frames, n) ** 2, axis=1) + 1e-12)
    quiet = 20 * np.log10(rms) < thr_db
    keep = np.ones(len(a), bool); f = 0
    while f < frames:
        if quiet[f]:
            g = f
            while g < frames and quiet[g]: g += 1
            s, e = f * n, g * n
            if (e - s) / SR > cap and s > 0 and g < frames:   # leave the very start/end to the trim
                drop = (e - s) - int(cap * SR); m = (s + e) // 2
                keep[m - drop // 2: m - drop // 2 + drop] = False
            f = g
        else: f += 1
    return a[keep], np.cumsum(keep)       # cumsum maps an old sample index to its new index


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    lines_f, base = args[0], args[1]
    raw_lines = open(lines_f, encoding="utf-8").read().splitlines()
    lines, breaks = [], set()             # breaks = index of the line AFTER which a section break falls
    for l in raw_lines:
        l = l.strip()
        if not l:
            if lines: breaks.add(len(lines) - 1)
            continue
        if "…" in l or "..." in l: sys.exit(f"no '…' inside a Hindi line (Fish makes dead air): {l}")
        if "[" in l: sys.exit(f"no [tags] in Hindi (they sound robotic): {l}")
        lines.append(l)
    text = " ".join(lines)
    os.makedirs(CACHE, exist_ok=True)
    sha = hashlib.sha1(json.dumps([text, VOICE, 1.0, 0.6, 0.7, 300]).encode()).hexdigest()[:12]
    take = f"{CACHE}/{sha}.wav"
    if not os.path.exists(take) or "--redo" in sys.argv:
        print("recording the whole take with Fish (janam)…", flush=True); tts(text, take)

    with tempfile.TemporaryDirectory() as td:
        json.dump(lines, open(f"{td}/lines.json", "w"), ensure_ascii=False)
        subprocess.run(["uv", "run", "-q", "--with", "faster-whisper", "--with", "numpy", "--with", "soundfile", "python", "-W", "ignore",
                        f"{R}/tools/vo_split.py", take, f"{td}/lines.json", f"{td}/split.json", "hi"], check=True)
        sp = json.load(open(f"{td}/split.json"))
        for w in sp.get("warnings", []): print("WARNING:", w)
        clean = f"{td}/take48.wav"   # 70 Hz low-cut twice: the model's steady 47-59 Hz hum (same fix as the English voice)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", take, "-af", "highpass=f=70:poles=2,highpass=f=70:poles=2",
                        "-ar", str(SR), "-ac", "1", clean], check=True)
        a, _ = sf.read(clean, dtype="float32")

        # pieces between the cuts; head/tail trimmed to the first/last heard word (+ small pads)
        edges = [max(0.0, sp["first"] - 0.08)] + sp["cuts"] + [min(len(a) / SR, sp["last"] + 0.25)]
        rnd = random.Random(sha)          # same script -> same pauses every run
        opening_q = 0                     # the opening question runs over the first lines until one ends in "?"
        while opening_q < len(lines) - 1 and not lines[opening_q].rstrip().endswith("?"): opening_q += 1
        out, spans = [np.zeros(int(0.08 * SR), np.float32)], []   # 80 ms lead silence (same as English)
        heard = [sp["first"]] + sp["cuts"] + [sp["last"]]        # each line's sound inside the take
        for i in range(len(lines)):
            s0 = int(edges[i] * SR); seg = a[s0: int(edges[i + 1] * SR)]
            at = sum(len(x) for x in out)
            spans.append((at + int((max(heard[i], edges[i]) - edges[i]) * SR), at + int((min(heard[i + 1], edges[i + 1]) - edges[i]) * SR)))
            out.append(seg)
            if i == len(lines) - 1: break
            if i < opening_q: continue
            p = (AT_BREAK if i in breaks else IN_SECTION) + rnd.uniform(-JITTER, JITTER)
            sil = np.zeros(int(p * SR), np.float32)
            out.append(sil)
        joined = np.concatenate(out)
        capped, newpos = cap_silences(joined)
        spans = [(newpos[min(x, len(newpos) - 1)] / SR, newpos[min(y, len(newpos) - 1)] / SR) for x, y in spans]
        sf.write(f"{td}/paused.wav", capped, SR)

        master = ("acompressor=threshold=-20dB:ratio=3:attack=8:release=120:makeup=4,volume=1.5dB,"
                  "aresample=192000,alimiter=limit=0.89:level=false,aresample=48000")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{td}/paused.wav", "-af", master, "-ar", str(SR), "-ac", "1",
                        f"{base}.wav"], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{base}.wav", "-b:a", "192k", f"{base}.mp3"], check=True)

    lufs, peak = loudness(f"{base}.wav")
    meta = {"voice": VOICE, "take": take, "dur": round(len(capped) / SR, 3), "lufs": lufs, "truePeak": peak,
            "lines": [{"text": l, "start": round(spans[i][0], 3), "end": round(spans[i][1], 3), "breakAfter": i in breaks}
                      for i, l in enumerate(lines)], "warnings": sp.get("warnings", [])}
    json.dump(meta, open(f"{base}.json", "w"), ensure_ascii=False, indent=1)
    print(f"done: {base}.mp3  {meta['dur']:.1f} s  {lufs} LUFS  true peak {peak} dBTP")


if __name__ == "__main__":
    main()
