"""Find where each script line sits inside ONE whole-take narration (voiceMode "whole", tools/reel_vo.py).
Usage: uv run -q --with faster-whisper --with numpy --with soundfile python -W ignore tools/vo_split.py <take.wav> <lines.json> <out.json> [lang]
lines.json = the CLEAN script lines (no [tags]). faster-whisper (small) transcribes the take with word timestamps; heard words are aligned to
the script letters line by line (character-level difflib, so a word whisper split or merged still lands right); each cut is the midpoint
of the silence between the last word of line k and the first word of line k+1. A boundary that cannot be aligned falls back to a cut
proportional to character count (warning in "warnings"); this never raises for a bad match.
out.json = {"dur", "cuts":[t1..t(n-1)], "first":start of first word, "last":end of last word, "words":[[w,start,end]...], "warnings":[...]}"""
import difflib, json, re, subprocess, sys, tempfile, os
import numpy as np, soundfile as sf
from faster_whisper import WhisperModel

take, lines_f, out_f = sys.argv[1:4]; LANG = sys.argv[4] if len(sys.argv) > 4 else "en"
lines = json.load(open(lines_f))
tmp = tempfile.mktemp(suffix=".wav")   # av has a metadata bug on some wavs: decode with ffmpeg, read with soundfile
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", take, "-ac", "1", "-ar", "16000", tmp], check=True)
a, _ = sf.read(tmp, dtype="float32"); os.remove(tmp)
dur = len(a) / 16000
segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(a, language=LANG, word_timestamps=True)
heard = [w for sg in segs for w in sg.words]
norm = lambda x: re.sub(r"[^a-z0-9ऄ-हक़-य़]", "", x.lower())
warn = []
cuts = [None] * (len(lines) - 1)
hn = [norm(h.word) for h in heard]
hchars = "".join(hn); hmap = [i for i, w in enumerate(hn) for _ in w]          # heard char -> heard word index
sl = [norm(l) for l in lines]; schars = "".join(sl)
ends = np.cumsum([len(s) for s in sl]).tolist()                                # script char index after each line
first = heard[0].start if heard else 0.0; last = heard[-1].end if heard else dur
sm = difflib.SequenceMatcher(None, schars, hchars, autojunk=False)
blocks = [b for b in sm.get_matching_blocks() if b.size]
matched = sum(b.size for b in blocks) / max(1, len(schars))
if matched < 0.6: warn.append(f"only {matched:.0%} of the script letters matched the heard take; cutting by character count")

def at_char(p):   # script char position p (last char of a line) -> heard word index, via the nearest matched block at/before it
    best = None
    for b in blocks:
        if b.a <= p < b.a + b.size: return hmap[min(len(hmap) - 1, b.b + p - b.a)], True
        if b.a + b.size <= p: best = b
    if best is None: return None, False
    return hmap[min(len(hmap) - 1, best.b + best.size - 1)], False

# whisper word times are loose (a word's start is often smeared back over the pause before it), so the cut is placed from the audio itself:
# the middle of the quietest stretch between the middle of the last word of line k and the middle of the first word of line k+1.
FR = 160   # 10 ms frames at 16 kHz
rms = np.sqrt(np.convolve(a * a, np.ones(FR) / FR, mode="same"))[::FR // 2]   # one value per 5 ms
def quiet_mid(w0, w1):
    i0 = int((w0.start + w0.end) / 2 * 200); i1 = max(i0 + 2, int((w1.start + w1.end) / 2 * 200)); seg = rms[i0:i1]
    if len(seg) == 0: return (w0.end + w1.start) / 2
    thr = max(float(seg.min()) * 1.5, 0.004)
    quiet = seg <= thr; best, cur, bs = (0, 0), 0, 0
    for j, q in enumerate(quiet):
        if q:
            if cur == 0: bs = j
            cur += 1
            if cur > best[1]: best = (bs, cur)
        else: cur = 0
    return (i0 + best[0] + best[1] / 2) / 200

for k in range(len(lines) - 1):
    p = ends[k] - 1; wi, exact = (None, False) if matched < 0.6 or p < 0 else at_char(p)
    if wi is not None and not exact:
        warn.append(f"boundary {k + 1}/{k + 2}: last word of line {k + 1} not matched exactly; used the nearest matched word")
    if wi is None or wi + 1 >= len(heard):
        t = first + (last - first) * ends[k] / max(1, ends[-1])
        warn.append(f"boundary {k + 1}/{k + 2}: no alignment, cut proportionally at {t:.2f}s"); cuts[k] = t; continue
    cuts[k] = quiet_mid(heard[wi], heard[wi + 1])
for k in range(1, len(cuts)):   # monotonic, never a zero-length piece
    if cuts[k] < cuts[k - 1] + 0.3:
        warn.append(f"boundary {k + 1}/{k + 2}: cut out of order, moved"); cuts[k] = cuts[k - 1] + 0.3
json.dump({"dur": dur, "cuts": [round(c, 3) for c in cuts], "first": first, "last": last, "matched": round(matched, 3),
           "words": [[h.word, h.start, h.end] for h in heard], "warnings": warn}, open(out_f, "w"))
print(f"split: {len(lines)} lines, {matched:.0%} letters matched, {len(warn)} warnings")
