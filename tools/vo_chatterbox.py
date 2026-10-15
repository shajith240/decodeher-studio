"""Local narrator voice (owner pick 10-14): Chatterbox "natural" (exaggeration 0.5, cfg 0.5) cloned from
library/voice/narrator-ref.wav, then 1.5 semitones deeper with Rubber Band R3 (clean — librosa's shift sounded hollow).
Called by tools/reel_vo.py when config.json reels.voice is "chatterbox-deep15"; not run by hand normally:
  uv run --python 3.11 --with chatterbox-tts --with torchaudio --with "setuptools<81" --with faster-whisper --with librosa \
    python -I tools/vo_chatterbox.py <job.json>        job = [[text, raw_out_path, ex|None, cfg|None], ...]
Every line is checked by whisper; a take that drops a word is regenerated (best of up to 5 takes is kept)."""
import json, os, re, shutil, subprocess, sys, tempfile
import librosa, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from activity import log
from chatterbox.tts import ChatterboxTTS
from faster_whisper import WhisperModel

REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../library/voice/narrator-ref.wav")
EX, CFG, SEMIS = 0.5, 0.5, -1.5
CHAIN = int(os.environ.get("VO_CHAIN", "1"))   # 2 = clean take out, pitch/tempo done by reel_vo.py
# pace (owner 10-14: "fast but natural, not forced" — Zoltium lines run 160-200 wpm, slower only on the CTA):
# each take's spoken rate is measured and Rubber Band speeds it up in the SAME pass as the pitch shift, never > 15 %
WPM, WPM_LAST, MAX_TEMPO = 172, 150, 1.15
job = json.load(open(sys.argv[1]))
m = ChatterboxTTS.from_pretrained(device="cuda"); asr = WhisperModel("small", device="cpu", compute_type="int8")
NUM = dict(zip("0123456789", "zero one two three four five six seven eight nine".split()))
words = lambda s: re.sub(r"[^a-z ]", " ", re.sub(r"'s\b|'", "", re.sub(r"\d", lambda d: f" {NUM[d.group()]} ", s.lower().replace("’", "'")))).split()   # whisper writes "1 a.m.", "guys" for "guy's"
FILLER = {"ahh", "ah", "uh", "um", "hmm", "oh"}

def missed(wav, text):
    y = librosa.resample(wav, orig_sr=m.sr, target_sr=16000)
    heard = set(words(" ".join(s.text for s in asr.transcribe(y, language="en")[0])))
    return [w for w in words(text) if not ({w, w + "s", w[:-1] if w.endswith("s") else w} & heard) and w not in FILLER]

for k, (text, out, *st) in enumerate(job):
    ex = st[0] if st and st[0] is not None else EX; cfg = st[1] if len(st) > 1 and st[1] is not None else CFG
    best = None; log(f"Recording voice · line {k + 1} of {len(job)} · {text[:48]}")
    for take in range(5):
        w = m.generate(text, audio_prompt_path=REF, exaggeration=ex, cfg_weight=cfg).squeeze().numpy()
        miss = missed(w, text)
        # owner 10-14 heard "Follow for more" twice: on short lines the model can REPEAT itself (whisper merges the repeat, so the word
        # check passes). A take far longer than its words allow is a repeat — reject it outright.
        if len(w) / m.sr > 0.42 * len(words(text)) + 1.0:
            print(f"  take {take + 1} too long ({len(w) / m.sr:.1f}s, likely a repeat): {text}", flush=True); continue
        if best is None or len(miss) < len(best[1]): best = (w, miss)
        if not miss: break
        print(f"  take {take + 1} missed {miss}: {text}", flush=True)
    if best is None: sys.exit(f"no clean take after 5 tries: {text}")
    with tempfile.TemporaryDirectory() as d:
        sf.write(f"{d}/a.wav", best[0], m.sr)
        iv = librosa.effects.split(best[0], top_db=40); speech = (iv[-1][1] - iv[0][0]) / m.sr   # first to last word, pauses included (how Zoltium was measured)
        wpm = len(words(text)) / max(speech, 0.3) * 60; target = WPM_LAST if k == len(job) - 1 and os.environ.get("VO_LAST_IS_CTA", "1") == "1" else WPM
        tempo = min(MAX_TEMPO, max(1.0, target / wpm))
        if len(re.findall(r"[.?!]+(?=\s|$)", text.strip())) > 1: tempo = 1.0   # punchy fragments: the pauses ARE the delivery (owner 10-14)
        print(f"  pace {wpm:.0f} wpm -> x{tempo:.2f}", flush=True)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if CHAIN >= 2:   # voice v2 (owner 10-14 "echoey, hollow on the phone"): keep the CLEAN take; reel_vo.py shifts + speeds it in ONE pass
            json.dump({"tempo": round(tempo, 4)}, open(out + ".json", "w")); shutil.move(f"{d}/a.wav", out)
        else:
            subprocess.run(["rubberband", "-3", "-p", str(SEMIS), "-T", f"{tempo:.3f}", f"{d}/a.wav", f"{d}/b.wav"], check=True, capture_output=True)
            shutil.move(f"{d}/b.wav", out)
    print(f"voiced{' (best take, still missing ' + str(best[1]) + ')' if best[1] else ''}: {text}", flush=True)
