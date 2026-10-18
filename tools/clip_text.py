"""Find clips with baked-in text (owner 10-17: the judges' contact sheets miss it, and any text in a clip pulls attention off our
captions). OCR reads 8 frames spread over each candidate clip; a clip HAS TEXT when a word of 3+ letters/digits is read with
confidence >= 0.75 — only watermarks and overlaid captions count (rules at has_text; 10-18: tattoos and room numbers don't).
Usage: uv run -q --with rapidocr_onnxruntime python tools/clip_text.py <reel_dir> [more files.mp4 ...]
A reel dir means the clips its judges passed (the only ones clippick can use) + its hook clip; all candidates before judging.
Results are remembered per clip file in library/clip-text.json {file name: [has_text, "words seen"]}, so a pin is read only once.
tools/clippick.py and tools/pick_hook.py skip every clip marked true."""
import glob, json, os, re, subprocess, sys, tempfile

R0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = f"{R0}/library/clip-text.json"
FRAMES, MIN_HITS, CONF = 8, 2, 0.75


def duration(f):
    o = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True).stdout
    try: return float(o.strip())
    except ValueError: return 0.0


# 10-18 owner: "the text I mean is watermarks and overlaid captions, not a tattoo or a room number in a hallway". A clip now
# HAS TEXT only when, on 2+ of the 8 frames, OCR reads one of:
#   - a caption / sentence: 3+ different words (letters, 3+ long) on the frame
#   - a watermark word: @handle, a web address, or a platform / credit word (tiktok, capcut, veo, follow, subscribe, link ...)
#   - a STATIC mark: the same word at the same spot on 3+ frames, in the top/bottom edge (signatures, channel names)
#   - a word-by-word caption: 6+ different words across 3+ frames (kinetic text shows 1-2 words at a time)
# Numbers alone (room numbers, clocks) and single words inside the scene (a tattoo, a label on a cup) no longer count.
MARK = re.compile(r"@\w|\w\.(com|net|org|co|io|tv)\b|www|https?|tiktok|tik tok|capcut|instagram|youtube|reels?\b|veo\b|sora\b|"
                  r"watermark|subscribe|follow|link in|tap link|thanks for watching|credit|animations?\b", re.I)
LETTERS = re.compile(r"[A-Za-zऀ-ॿ]{3,}")


def has_text(ocr, f):
    d = min(duration(f), 30.0)   # clips are trimmed to their useful 30 s head
    if d <= 0: return False, ""
    hits, seen, spots, allw, wframes = 0, [], {}, set(), 0
    with tempfile.TemporaryDirectory() as td:
        for k in range(FRAMES):
            t = d * (k + 0.5) / FRAMES; img = f"{td}/{k}.jpg"
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{t:.2f}", "-i", f, "-frames:v", "1", "-vf", "scale=720:-2", "-q:v", "2", img])
            if not os.path.exists(img): continue
            res, _ = ocr(img)
            # 10-17: a dark watermark on a dark clip ("...club" at the bottom) read as nothing; a contrast-equalised copy finds it
            # small watermarks hide in the top/bottom edges ("The Libros Club", tiny dark serif): read those bands enlarged 2.5x
            boxes = [(("full", b), txt, c) for b, txt, c in (res or [])]
            for band, crop in (("bot", "crop=iw:ih*0.22:0:ih*0.78"), ("top", "crop=iw:ih*0.16:0:0")):
                bf = f"{img}.{band}.jpg"
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", img, "-vf", f"{crop},scale=iw*2.5:-2:flags=lanczos,histeq=strength=0.8,eq=contrast=1.6", bf])
                if os.path.exists(bf): boxes += [((band, b), txt, c) for b, txt, c in (ocr(bf)[0] or [])]
            good = [(where, txt) for where, txt, c in boxes if c >= CONF]
            words = {w.lower() for _, txt in good for w in LETTERS.findall(txt)}
            mark = any(MARK.search(txt) for _, txt in good)
            if words: wframes += 1; allw |= words
            for (band, b), txt in good:   # where each word sits (box centre, rounded to ~6 % of the 720-px-wide frame)
                cx, cy = sum(p[0] for p in b) / 4, sum(p[1] for p in b) / 4
                for w in LETTERS.findall(txt): spots.setdefault((band, w.lower()[:5], round(cx / 43), round(cy / 43)), set()).add(k)
            if len(words) >= 3 or mark: hits += 1; seen += [txt for _, txt in good]
    static = [key[1] for key, ks in spots.items() if len(ks) >= 3 and key[0] in ("top", "bot")]   # a still shot's tattoo or label isn't one
    kinetic = wframes >= 3 and len(allw) >= 6
    if static: seen += static
    if kinetic and hits < MIN_HITS: seen += sorted(allw)
    return (hits >= MIN_HITS or bool(static) or kinetic), " ".join(dict.fromkeys(seen))[:120]


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
