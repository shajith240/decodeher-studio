"""Find clips with baked-in text (owner 10-17: the judges' contact sheets miss it, and any text in a clip pulls attention off our
captions). OCR reads 8 frames spread over each candidate clip; a clip HAS TEXT when a word of 3+ letters/digits is read with
confidence >= 0.75 on at least 2 of those frames (one stray letter is a shape, e.g. a cartoon head read as "B").
Usage: uv run -q --with rapidocr_onnxruntime python tools/clip_text.py <reel_dir> [more files.mp4 ...]
A reel dir means the clips its judges passed (the only ones clippick can use) + its hook clip; all candidates before judging.
Results are remembered per clip file in library/clip-text.json {file name: [has_text, "words seen"]}, so a pin is read only once.
tools/clippick.py and tools/pick_hook.py skip every clip marked true."""
import glob, json, os, re, subprocess, sys, tempfile

R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = f"{R0}/library/clip-text.json"
FRAMES, MIN_HITS, CONF = 8, 2, 0.75
WORD = re.compile(r"[A-Za-z0-9ऀ-ॿ]{3,}")


def duration(f):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout
    try: return float(o.strip())
    except ValueError: return 0.0


def has_text(ocr, f):
    d = min(duration(f), 30.0)   # clips are trimmed to their useful 30 s head
    if d <= 0: return False, ""
    hits, seen = 0, []
    with tempfile.TemporaryDirectory() as td:
        for k in range(FRAMES):
            t = d * (k + 0.5) / FRAMES; img = f"{td}/{k}.jpg"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-vf", "scale=720:-2", img])
            if not os.path.exists(img): continue
            res, _ = ocr(img)
            words = [w for _, txt, c in (res or []) if c >= CONF for w in WORD.findall(txt)]
            if words: hits += 1; seen += words
    return hits >= MIN_HITS, " ".join(dict.fromkeys(seen))[:120]


def pickable(R):
    """only the clips clippick.py could still use (judges passed them); every candidate if the judges haven't run yet"""
    idx_f = f"{R}/clips/sheets/index.json"
    if not os.path.exists(idx_f): return sorted(glob.glob(f"{R}/clips/cand/*/*.mp4"))
    out = []
    for nn, e in json.load(open(idx_f)).items():
        jf = f"{R}/clips/judge/{nn}.json"
        j = (json.load(open(jf)) if os.path.exists(jf) else {}).get("clips", {})
        for letter, c in e.get("clips", {}).items():
            v = j.get(letter)
            if v and not v.get("text") and v.get("meaning", 0) >= 4 and v.get("style", 0) >= 5 and v.get("quality", 0) >= 4 \
                    and os.path.exists(f"{R}/clips/cand/{c['file']}"):
                out.append(f"{R}/clips/cand/{c['file']}")
    return sorted(set(out))


def main():
    from rapidocr_onnxruntime import RapidOCR
    files = []
    for a in sys.argv[1:]:
        if os.path.isdir(a): files += pickable(a) + sorted(glob.glob(f"{a}/clips/hook/*.mp4"))
        else: files.append(a)
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    todo = [f for f in files if os.path.basename(f) not in cache]
    ocr = RapidOCR() if todo else None
    for i, f in enumerate(todo, 1):
        cache[os.path.basename(f)] = list(has_text(ocr, f))
        if i % 10 == 0 or i == len(todo):   # save as we go: a killed run keeps what it read
            json.dump(cache, open(CACHE + ".part", "w"), ensure_ascii=False); os.replace(CACHE + ".part", CACHE)
    flagged = [f for f in files if cache.get(os.path.basename(f), [False])[0]]
    print(f"text check: {len(files)} clips ({len(todo)} new), {len(flagged)} with text")
    for f in flagged: print("  TEXT", os.path.relpath(f, R0), "·", cache[os.path.basename(f)][1])


if __name__ == "__main__":
    main()
