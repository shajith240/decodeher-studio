"""Real word timing: replace the estimated word times in a reel's assets/timing.js with times measured from the voice audio,
so every caption word appears exactly when it is spoken (owner, 10-13: "the caption comes a bit fast, the voice a bit slow").
Usage: uv run --with faster-whisper --with numpy python tools/align_words.py <reel_dir> [...]
Each line's wav is transcribed with word timestamps; if the recognised word count matches the script line, those times are
used (offset by the line's start in the mix); otherwise the line keeps its estimate and is reported."""
import json, os, re, subprocess, sys, unicodedata
import numpy as np
from faster_whisper import WhisperModel

model = WhisperModel("small", device="cpu", compute_type="int8")
for R in map(os.path.abspath, sys.argv[1:]):
    LANG = json.load(open(os.path.join(R, "reel.json"))).get("lang", "en") if os.path.exists(os.path.join(R, "reel.json")) else "en"
    tj = os.path.join(R, "assets/timing.js"); s = open(tj).read(); T = json.loads(s[s.index("{"):s.rindex("}") + 1])
    fixed, kept = 0, []
    for i, words in enumerate(T["words"]):
        wav = os.path.join(R, f"assets/vo/l{i + 1:02d}.wav")
        a = np.frombuffer(subprocess.run(["ffmpeg", "-loglevel", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"],
                                         capture_output=True).stdout, np.float32)
        segs, _ = model.transcribe(a, language=LANG, word_timestamps=True)
        heard = [w for sg in segs for w in sg.words]
        # map recognised words onto script words; a script word the recogniser split ("a.m." → "a." "m.", "late-night" →
        # "late" "night") absorbs heard words until their letters match it
        norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
        if LANG == "hi":   # loose Devanagari match: drop nukta, matras, virama, anusvara/chandrabindu (a consonant skeleton), keep Latin/digits
            norm = lambda x: re.sub(r"[^a-z0-9\u0904-\u0939\u0958-\u095F]", "", re.sub(r"[\u093C\u093E-\u094D\u0900-\u0903]", "", unicodedata.normalize("NFD", x).lower()))
            if len(heard) == len(words):   # same word count (Latin loanwords come back in Devanagari, so letters can't match): take them in order
                for w, h in zip(words, heard): w[1], w[2] = round(T["vo"][i] + h.start, 3), round(T["vo"][i] + h.end, 3)
                fixed += 1; continue
        spans, j, ok = [], 0, True
        for w in words:
            if j >= len(heard): ok = False; break
            acc, h0 = norm(heard[j].word), heard[j]
            while norm(w[0]) != acc and len(acc) < len(norm(w[0])) and j + 1 < len(heard):
                j += 1; acc += norm(heard[j].word)
            spans.append((h0.start, heard[j].end)); j += 1
        if not ok or j != len(heard):
            # fallback: align the two word sequences (difflib) and interpolate the few script words the recogniser merged/split
            import difflib
            hn, sn = [norm(h.word) for h in heard], [norm(w[0]) for w in words]
            sm = difflib.SequenceMatcher(None, sn, hn, autojunk=False); got = {}
            for blk in sm.get_matching_blocks():
                for q in range(blk.size): got[blk.a + q] = (heard[blk.b + q].start, heard[blk.b + q].end)
            if len(got) < 0.6 * len(words):
                kept.append(f"line {i + 1}: heard {len(heard)} words, script has {len(words)} — kept the estimate"); continue
            spans = []
            for q in range(len(words)):
                if q in got: spans.append(got[q]); continue
                prv = max([k for k in got if k < q], default=None); nxt = min([k for k in got if k > q], default=None)
                a0 = got[prv][1] if prv is not None else 0.0; b0 = got[nxt][0] if nxt is not None else (heard[-1].end if heard else a0 + 0.3)
                lo = [k for k in range(q, len(words)) if k not in got and (nxt is None or k < nxt)]; nn = len(lo) + (q - (prv if prv is not None else -1) - 1)
                spans.append((a0 + (b0 - a0) * 0.1, a0 + (b0 - a0) * 0.9) if not spans or spans[-1][1] <= a0 else (spans[-1][1], spans[-1][1] + max(0.08, (b0 - spans[-1][1]) / max(1, len(lo)))))
            kept.append(f"line {i + 1}: aligned by sequence ({len(got)}/{len(words)} words matched)")
        start = T["vo"][i]
        for w, (a0, a1) in zip(words, spans):
            w[1], w[2] = round(start + a0, 3), round(start + a1, 3)
        fixed += 1
    open(tj, "w").write("window.T = " + json.dumps(T) + ";\n")
    print(f"{os.path.basename(R)}: {fixed}/{len(T['words'])} lines aligned to the voice" + ("".join("\n  " + k for k in kept)))
