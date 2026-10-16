"""Voiceover for a Spot the Con reel with Fish Audio (free model). Usage: python3 tools/reel_vo.py <reel_dir> [voice_id]
Reads <reel>/assets/vo/script.json, writes <reel>/assets/vo/lNN.wav (48 kHz mono) with CLEAN EDGES:
  - silence trimmed at -50 dB but 70 ms of room tone kept before the first word and 180 ms after the last,
  - 25 ms fade-in, 80 ms of silence before the first word (some voices start speaking at sample 0), 90 ms fade-out,
  - each file is verified: edges must be quiet (< -30 dBFS peak in the first/last 10 ms) and no clipping.
FISH_API_KEY comes from the environment or the nearest .env (never printed).

WHOLE-TAKE MODE (config reels.voiceMode "whole", the default for Fish; reel.json "voice_mode" overrides; owner-approved 10-15 "Take 1"):
  every separate Fish call re-samples the voice ("sounds like another person"), so the WHOLE script goes out as ONE call and is then cut
  back into lNN.wav, because the rest of the pipeline (reel_timing, align_words, mix) works per line.
  - script.json lines may carry inline delivery tags in [square brackets] ("Here's why. [lower voice] A meme..."). Fish performs them and
    does not speak them. TTS text = voiceStyle + line1 + " [pause] " + line2 ... ; a WHY line (reel.json "drops", 0-based) with no tag gets
    "[lower voice]"; the "rehookAt" line is preceded by "[long pause]"; the last line (tagline) gets "[confident]" when it has no tag.
  - tags are stripped from everything else: spoken.json, speak()/check(), captions (reel_timing), alignment.
  - ONE wav (cache: raw/take-<sha1 of text+voice+settings>.wav, REDO=1 forces), leveled ONCE to -18 LUFS, then cut at the midpoint of the silence
    between lines (tools/vo_split.py: faster-whisper word times matched to the clean script, proportional fallback with a warning).
    Pieces keep their natural pauses (no silence trim, no extra pad), so the lNN.wav laid back to back reproduce the take.
  - reel.json "gaps" is set to 0.05 (the pauses are inside the take). Sidecar: assets/vo/take.json.
  - fishSpeed (absolute, config) is NOT multiplied by reel.json speed in whole mode; temperature/top_p from config."""
import hashlib, json, os, re, subprocess, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from speakable import speak, check
from activity import log

R = os.path.abspath(sys.argv[1])
RC = json.load(open(os.path.join(os.path.dirname(__file__), "..", "config.json"))).get("reels", {})
DEFAULT_VOICE = RC.get("voice", "536d3a5e000945adb7038665781a4aca")
SPEED = float(RC.get("speed", 1.0))
VOICE = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_VOICE


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
    body = json.dumps({"text": text, "reference_id": VOICE, "format": "wav", "latency": "normal", "normalize": True,
                       "prosody": {"speed": round(FISH_SPEED if WHOLE else SPEED * REEL_SPEED, 3), "volume": 0},
                       **({"temperature": RC["voiceTemperature"]} if "voiceTemperature" in RC else {}), **({"top_p": RC["voiceTopP"]} if "voiceTopP" in RC else {})}).encode()
    for attempt in range(4):
        try:
            req = urllib.request.Request("https://api.fish.audio/v1/tts", method="POST", data=body,
                                         headers={"Authorization": f"Bearer {K}", "Content-Type": "application/json", "model": "s2.1-pro-free"})
            data = urllib.request.urlopen(req, timeout=180).read()   # audit H6: fetch FIRST; a failure never leaves a 0-byte file in the cache
            if len(data) < 4000: raise ValueError(f"Fish returned only {len(data)} bytes")
            open(out + ".part", "wb").write(data); os.replace(out + ".part", out); return
        except Exception as e:
            if attempt == 3: raise
            time.sleep(5 * (attempt + 1))


def peak_db(f, args):
    o = subprocess.run(["ffmpeg", "-hide_banner", *args, "-i", f, "-af", "astats", "-f", "null", "-"], capture_output=True, text=True).stderr
    for line in o.splitlines():
        if "Peak level dB" in line: return float(line.split()[-1])
    return -99.0


def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]))


TAG = re.compile(r"\[[^\]]*\]")
untag = lambda t: re.sub(r"\s+", " ", TAG.sub(" ", t)).strip()
LOCAL = VOICE.startswith("chatterbox")   # local open-source narrator (tools/vo_chatterbox.py), no API key
K = None if LOCAL else key()
REEL_SPEED = float(json.load(open(f"{R}/reel.json")).get("speed", 1.0)) if os.path.exists(f"{R}/reel.json") else 1.0
# voice chain (owner 10-14: v1 sounded echoey + hollow on a phone speaker). v2 = Rubber Band ONCE with formants kept (the shift no longer
# makes the mouth sound bigger/boxier), speed folded into that pass, phone EQ (mud cut, presence lift) + light compression, and NO room
# in the mix. A reel keeps the chain it was voiced with (reel.json "voice_chain"); new reels take config.json reels.voiceChain.
RJ = json.load(open(f"{R}/reel.json")) if os.path.exists(f"{R}/reel.json") else {}
CHAIN = int(RJ.get("voice_chain", RC.get("voiceChain", 1)))
SEMIS = float(os.environ.get("VO_SEMIS", RC.get("semis", -1.5)))
PHONE_EQ = ("equalizer=f=300:t=q:w=1.0:g=-2.5,equalizer=f=3000:t=q:w=0.9:g=2.5,"
            "acompressor=threshold=0.1:ratio=2.5:attack=8:release=90:knee=4")
if os.path.exists(f"{R}/reel.json") and RJ.get("voice_chain") != CHAIN:
    RJ["voice_chain"] = CHAIN; json.dump(RJ, open(f"{R}/reel.json", "w"), indent=1, ensure_ascii=False)
LANG = RJ.get("lang", "en")   # "hi": Hinglish in Devanagari (Fish reads it correctly only in Devanagari; Latin loanwords stay Latin)
WHOLE = (not LOCAL) and RJ.get("voice_mode", RC.get("voiceMode", "whole")) == "whole"
FISH_SPEED = float(RC.get("fishSpeed", 1.0))
lines = json.load(open(f"{R}/assets/vo/script.json"))
# STRICT voiceover rule: the voice never sees digits or symbols. Every line is converted to how a person would say it,
# and the reel stops here if anything unspeakable is left (see tools/speakable.py and BRAND.md → Voiceover).
# a line may carry its own delivery (brain/research/narration-emphasis.md): {"text": "...", "ex": 0.7, "cfg": 0.3} — punch and
# reveal lines get more emotion (exaggeration) and more weight (lower cfg); plain strings use the narrator default
style = [(l.get("ex"), l.get("cfg")) if isinstance(l, dict) else (None, None) for l in lines]
lines = [l["text"] if isinstance(l, dict) else l for l in lines]
tagged = lines                      # lines as written, with any [delivery tags]
lines = [untag(l) for l in lines]   # clean text: what is checked, aligned and captioned
spoken, spoken_tagged = [], []
_keep_end = lambda t: (lambda r: r + t[-1] if t and t[-1] in ",;:" and not r.endswith(t[-1]) else r)(_sp(t))   # speak() drops a trailing comma; a tag may follow it
_sp = lambda t: speak(t, LANG) if LANG != "en" else speak(t)
# owner 10-17: texting words nobody says aloud ("haha", "lol") sound weird and awkward when the AI reads them; never voiced
TEXTSPEAK = re.compile(r"(?<![\w\u0900-\u097f])(h+a+h+a+[ha]*|he+he+[he]*|lol+|lmao+|rofl|omg|idk|tbh|smh|brb|ikr|kk|xd|हा+हा+[हा]*|लोल)(?![\w\u0900-\u097f])", re.I)
for i, text in enumerate(lines, 1):
    if TEXTSPEAK.search(text): sys.exit(f"line {i} has a texting word nobody says out loud ({TEXTSPEAK.search(text).group(0)!r}): {text!r} (brain/rules/spoken-script-rules.md)")
    s_ = _sp(text); bad = check(s_, LANG) if LANG != "en" else check(s_)
    if bad: sys.exit(f"line {i} still has unspeakable characters {bad!r} after conversion: {s_!r}")
    spoken.append(s_)
    # same line with its tags kept: speak() only the text between tags
    spoken_tagged.append(" ".join(x.strip() if TAG.fullmatch(x) else _keep_end(x.strip()) for x in re.split(r"(\[[^\]]*\])", tagged[i - 1]) if x.strip()))
json.dump(spoken, open(f"{R}/assets/vo/spoken.json", "w"), indent=1, ensure_ascii=False)
os.makedirs(f"{R}/assets/vo/raw", exist_ok=True)
def tag_of(i):   # cache key = voice + exact text (+ the line's own delivery, if any)
    st = f"|{style[i][0]}|{style[i][1]}" if style[i] != (None, None) else ""
    return hashlib.sha1(f"{VOICE}|{SPEED}|{spoken[i]}{st}{'|v2' if CHAIN >= 2 else ''}".encode()).hexdigest()[:12]
raw_of = lambda i: f"{R}/assets/vo/raw/l{i + 1:02d}-{tag_of(i)}.wav"
if LOCAL:   # voice every missing line in one model load (GPU), then the normal trim/level/edge checks below
    todo = [[spoken[i], raw_of(i), *style[i]] for i in range(len(spoken)) if os.environ.get("REDO") or not os.path.exists(raw_of(i))]
    if todo:
        jf = f"{R}/assets/vo/raw/_job.json"; json.dump(todo, open(jf, "w"))
        subprocess.run(["uv", "run", "-q", "--python", "3.11", "--with", "chatterbox-tts", "--with", "torchaudio", "--with", "setuptools<81",
                        "--with", "faster-whisper", "--with", "librosa", "python", "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "vo_chatterbox.py"), jf], check=True,
                       env=dict(os.environ, VO_CHAIN=str(CHAIN)))
        os.remove(jf)

def level(src, dst):   # one leveling pass to -18 LUFS with a true-peak-safe limiter (same chain the per-line path uses)
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    li = float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-af", f"volume={-18 - li:.2f}dB,aresample=192000,alimiter=limit=0.89:attack=1:release=40:level=disabled,aresample=48000", dst], check=True)


def whole_take():
    """ONE Fish call for the whole script, then cut into lNN.wav. Returns nothing; writes l01..lNN.wav + take.json."""
    n = len(spoken); drops = set(RJ.get("drops", []) or []); rehook = RJ.get("rehookAt")
    parts = []
    for i, t in enumerate(spoken_tagged):
        if i == n - 1 and not TAG.search(tagged[i]): t = "[confident] " + t
        elif i in drops and not TAG.search(tagged[i]): t = "[lower voice] " + t
        parts.append(("[long pause] " if (isinstance(rehook, int) and i == rehook and i > 0) else ("[pause] " if i else "")) + t)
    text = (RC.get("voiceStyle", "").strip() + " " + " ".join(parts)).strip()
    sha = hashlib.sha1(json.dumps([text, VOICE, FISH_SPEED, RC.get("voiceTemperature"), RC.get("voiceTopP")]).encode()).hexdigest()[:12]
    take = f"{R}/assets/vo/raw/take-{sha}.wav"
    if not os.path.exists(take) or os.environ.get("REDO"): tts(text, take)
    cj = take + ".cuts.json"
    if not os.path.exists(cj) or os.environ.get("REDO"):
        lf = f"{R}/assets/vo/raw/_lines.json"; json.dump(spoken, open(lf, "w"), ensure_ascii=False)
        r = subprocess.run(["uv", "run", "-q", "--with", "faster-whisper", "--with", "numpy", "--with", "soundfile", "python", "-W", "ignore",
                            os.path.join(os.path.dirname(os.path.abspath(__file__)), "vo_split.py"), take, lf, cj + ".part", LANG], capture_output=True, text=True)
        os.remove(lf)
        if r.returncode == 0 and os.path.exists(cj + ".part"): os.replace(cj + ".part", cj)
        else:   # never crash: proportional cut by character count
            print("WARNING: alignment step failed, cutting by character count:", r.stderr.strip()[-300:])
            d0 = dur(take); tot = sum(len(x) for x in spoken); acc = 0; cuts_ = []
            for x in spoken[:-1]: acc += len(x); cuts_.append(round(d0 * acc / tot, 3))
            json.dump({"dur": d0, "cuts": cuts_, "first": 0.0, "last": d0, "words": [], "warnings": ["alignment failed: cut by character count"]}, open(cj, "w"))
    C = json.load(open(cj))
    for w in C.get("warnings", []): print("WARNING:", w)
    lv = take + ".lvl.wav"
    # owner 10-14 buzz: steep 70 Hz low-cut + gentle gate (same as the per-line path), then level the WHOLE take once so every line matches
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", take, "-af", "highpass=f=70:poles=2,highpass=f=70:poles=2,agate=threshold=0.008:ratio=3:attack=5:release=120:range=0.25",
                    "-ar", "48000", "-ac", "1", lv + ".g.wav"], check=True)
    level(lv + ".g.wav", lv); os.remove(lv + ".g.wav")
    D = dur(lv); b = [max(0.0, C["first"] - 0.07)] + C["cuts"] + [min(D, C["last"] + 0.18)]
    spans = []
    for i in range(n):
        s0, e0 = b[i], b[i + 1]; out = f"{R}/assets/vo/l{i + 1:02d}.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{s0:.4f}", "-t", f"{e0 - s0:.4f}", "-i", lv, "-af",
                        f"afade=t=in:d=0.025,afade=t=out:st={max(0, e0 - s0 - 0.09):.3f}:d=0.09" + (",adelay=80|80" if i == 0 else ""), "-ar", "48000", "-ac", "1", out], check=True)   # 10-16: voice 86ac speaks at sample 0 — 80 ms of silence before line 1
        spans.append([round(s0, 3), round(e0, 3)])
    os.remove(lv)
    json.dump({"mode": "whole", "sha": sha, "take": os.path.relpath(take, R), "tts_text": text, "dur": round(D, 3), "spans": spans,
               "cuts": C["cuts"], "warnings": C.get("warnings", [])}, open(f"{R}/assets/vo/take.json", "w"), indent=1, ensure_ascii=False)
    if os.path.exists(f"{R}/reel.json"):   # the pauses live inside the take now: lines go back to back
        RJ["gaps"] = [0.05] * (n - 1) + [0]; RJ["voice_mode"] = "whole"
        json.dump(RJ, open(f"{R}/reel.json.new", "w"), indent=1, ensure_ascii=False); os.replace(f"{R}/reel.json.new", f"{R}/reel.json")
    return D


if WHOLE:
    D = whole_take()
    for i, text in enumerate(spoken, 1):
        out = f"{R}/assets/vo/l{i:02d}.wav"
        head, tail, full = peak_db(out, ["-t", "0.01"]), peak_db(out, ["-sseof", "-0.01"]), peak_db(out, [])
        problems = [p for p, bad in (("loud start", head > -30), ("loud end", tail > -30), ("clipping", full > -0.1)) if bad]
        log(f"Voice ready · {RJ.get('title', os.path.basename(R))} · line {i} of {len(spoken)}")
        print(f"l{i:02d} {dur(out):.2f}s edges {head:.0f}/{tail:.0f} dB {'OK' if not problems else 'CHECK: ' + ', '.join(problems)}  {text}")
        if problems: sys.exit(f"voice line {i} failed edge checks: {problems}")
    print(f"whole take {D:.2f}s, {len(spoken)} lines (assets/vo/take.json)")
    sys.exit(0)
for i, text in enumerate(spoken, 1):
    # cache key = voice + exact text: changing either always re-records (a stale cache once mixed two voices)
    raw, out = raw_of(i - 1), f"{R}/assets/vo/l{i:02d}.wav"
    if not LOCAL and (not os.path.exists(raw) or os.environ.get("REDO")):
        tts(text, raw)
    # owner 10-14 heard a buzz: the voice model leaves a steady low tone (47-59 Hz, measured) in the quiet parts. A steep 70 Hz
    # low-cut removes it (the narrator sits at 80 Hz+), and a gentle gate pulls the gaps between words down 12 dB.
    trim = ("highpass=f=70:poles=2,highpass=f=70:poles=2,agate=threshold=0.008:ratio=3:attack=5:release=120:range=0.25,"
            "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.07,"
            "areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.18,areverse")
    src = raw
    if not LOCAL:   # owner 10-15 (Fish voice "sounds slow, like a drunk"): Fish speaks at the right pace itself (reels.speed x reel speed,
        pass        # sent as prosody) — no pitch shift and no Rubber Band stretch on top, which smeared it
    elif CHAIN >= 2:   # one Rubber Band pass: pitch (formants kept) + the take's pace + the reel speed
        pace = json.load(open(raw + ".json"))["tempo"] if os.path.exists(raw + ".json") else 1.0
        src = out + ".s.wav"
        subprocess.run(["rubberband", "-3", "-F", "-p", str(SEMIS), "-T", f"{pace * REEL_SPEED:.4f}", raw, src], check=True, capture_output=True)
    elif REEL_SPEED != 1.0 and LOCAL:   # reel.json "speed": the whole narration a touch faster, Rubber Band (clean, pitch kept) — owner 10-14
        trim += f",rubberband=tempo={REEL_SPEED}"
    tmp = out + ".t.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", src, "-af", trim, "-ar", "48000", "-ac", "1", tmp], check=True)
    if src != raw: os.remove(src)
    if CHAIN >= 2 and RC.get("phoneEq"):   # off by default — owner 10-14: EQ + compression made it sound "like radio"; phone EQ at a known level (-18 LUFS in), then the normal leveling below
        o = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
        l0 = float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
        eq = tmp + ".e.wav"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", f"volume={-18 - l0:.2f}dB,{PHONE_EQ}", eq], check=True); os.replace(eq, tmp)
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", tmp, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    li = float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])
    lev = tmp + ".l.wav"   # every line at the same loudness: -18 LUFS (one voice, one level, the whole reel)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af", f"volume={-18 - li:.2f}dB,aresample=192000,alimiter=limit=0.89:attack=1:release=40:level=disabled,aresample=48000", lev], check=True); os.replace(lev, tmp)
    d = dur(tmp)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", tmp, "-af",
                    f"afade=t=in:d=0.025,afade=t=out:st={max(0, d - 0.09):.3f}:d=0.09,adelay=80|80,apad=pad_dur=0.06", "-ar", "48000", "-ac", "1", out], check=True)
    os.remove(tmp)
    head, tail = peak_db(out, ["-t", "0.01"]), peak_db(out, ["-sseof", "-0.01"])
    full = peak_db(out, [])
    problems = [p for p, bad in (("loud start", head > -30), ("loud end", tail > -30), ("clipping", full > -0.1)) if bad]
    ok_level = abs(-18 - float([l for l in subprocess.run(["ffmpeg", "-hide_banner", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr.splitlines() if l.strip().startswith("I:")][-1].split()[1])) <= (2.0 if dur(out) < 2.5 else 1.0)   # short gated lines read ~1 LU off without being off
    if not ok_level: problems.append("level off target")
    log(f"Voice ready · {json.load(open(f'{R}/reel.json')).get('title', os.path.basename(R)) if os.path.exists(f'{R}/reel.json') else os.path.basename(R)} · line {i} of {len(spoken)}")
    print(f"l{i:02d} {dur(out):.2f}s edges {head:.0f}/{tail:.0f} dB {'OK' if not problems else 'CHECK: ' + ', '.join(problems)}  {text}")
    if problems: sys.exit(f"voice line {i} failed edge checks: {problems}")
