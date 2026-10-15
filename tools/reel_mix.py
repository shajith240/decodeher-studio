"""Sound design + final mix, v2 (owner 10-14: "this sound design is the worst" — rebuilt to brain/research/sound-design-v2.md).
Usage: uv run --with numpy --with scipy --with soundfile --with pyloudnorm --with librosa python tools/reel_mix.py <reel_dir>
Needs: assets/timing.js (aligned), assets/vo/lNN.wav, assets/audio/cues.json, reel.json:
  "music": library id | path | "auto" (random from library/music/approved, never one of the last 3 used)
  "drops": [line, ...] the reveal(s) — riser, 0.35 s near-silence, impact + sub on the line's first word (max 2, ≥ 8 s apart)
  optional "music_offset" (s into the track; default: the bar start whose first 3 s are calmest)
  env MUSIC=<file> OUT=<wav> renders an audition of another track without touching the reel's final.wav
What changed from v1 (each was a "cheap" tell):
  - music is never looped: it starts on a bar and runs once (a bar-aligned 2 s crossfade only if the track is too short)
  - energy curve: low-passed drone-like bed until the first reveal, full bed after it, thinned under the CTA line, 2.5 s tail
  - the bed is CARVED while the voice talks (-2.5 dB @200-300 Hz, -3.5 dB @2.5-5 kHz) and DUCKED 9 dB (attack 30 ms, release 400 ms)
  - SFX: density cap (≤ 5 per 10 s, big hits ≥ 5 s apart), rotation over 6-8 files per role + ±1.5 semitone jitter,
    levels set by LOUDNESS not peak, whooshes high-passed at 250 Hz, impacts layered with a mono sub; no braam at the end
  - master: -14 LUFS integrated, true peak ≤ -1 dBTP through an oversampled limiter (was a hard clip)"""
import json, os, random, subprocess, sys, tempfile, zlib
import numpy as np, soundfile as sf, pyloudnorm as pyln, librosa
from scipy.signal import butter, sosfilt, fftconvolve, resample_poly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from activity import log

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
R = os.path.abspath(sys.argv[1]); SR = 48000
s = open(os.path.join(R, "assets/timing.js")).read(); T = json.loads(s[s.index("{"):s.rindex("}") + 1])
cfg = json.load(open(os.path.join(R, "reel.json")))
cues = json.load(open(os.path.join(R, "assets/audio/cues.json")))
N = int((T["total"] + 0.5) * SR); meter = pyln.Meter(SR)

def load(path, offset=0.0, dur=None):
    a = ["ffmpeg", "-loglevel", "error", "-ss", str(offset), "-i", path] + (["-t", str(dur)] if dur else []) + ["-ac", "2", "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(a, capture_output=True, check=True).stdout, np.float32).reshape(-1, 2).copy()
db = lambda g: 10 ** (g / 20)
def lufs(x):
    if len(x) < int(0.5 * SR): x = np.concatenate([x, np.zeros((int(0.5 * SR) - len(x), 2), np.float32)])
    l = meter.integrated_loudness(x); return l if np.isfinite(l) else -70.0
to_lufs = lambda x, target: x * db(target - lufs(x))
filt = lambda x, *a: sosfilt(butter(*a, fs=SR, output="sos"), x, axis=0)
def place(buf, x, t, g=0.0):
    i = int(round(t * SR))
    if i < 0: x, i = x[-i:], 0
    n = min(len(x), len(buf) - i)
    if n > 0: buf[i:i + n] += x[:n] * db(g)
def follower(active, att, rel, step=48):
    """smooth 0..1 envelope of a 0/1 gate (attack/release in s), 1 ms steps"""
    out = np.zeros(len(active), np.float32); g = 0.0; aa, ar = step / (att * SR), step / (rel * SR)
    for k in range(0, len(active), step):
        tgt = active[k]; g += (tgt - g) * min(1, aa if tgt > g else ar); out[k:k + step] = g
    return out

# ── voice: HPF 75 Hz, +1.5 dB presence @3 kHz, short room (RT 0.6 s, 10 % wet, 15 ms pre-delay) → -17 LUFS
def room(x, rt=0.6, wet=0.10):
    n = int(rt * SR); ir = np.random.default_rng(7).standard_normal((n, 2)) * np.exp(-6.9 * np.arange(n) / n)[:, None]
    ir = filt(ir, 2, 5000, "low"); ir[: int(0.015 * SR)] = 0; ir /= np.sqrt((ir ** 2).sum(axis=0, keepdims=True))
    return x * (1 - wet) + np.stack([fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], axis=1) * wet * 1.6
voice = np.zeros((N, 2), np.float32)
for i in range(len(T["vo"])):
    v = filt(load(os.path.join(R, f"assets/vo/l{i + 1:02d}.wav")), 2, 75, "high")
    v = v + filt(v, 2, [2400, 3800], "band") * (db(1.5) - 1)
    place(voice, v if int(cfg.get("voice_chain", 1)) >= 2 else room(v), T["vo"][i])   # v2: dry, no room (owner 10-14: echo on phone)
# owner 10-15 (Fish voice): "add some room, a small room, not that much" — one short room over the whole voice track (so no line's
# tail is cut), set by config.json reels.voiceRoom {"rt": s, "wet": share}; absent = dry
VR = json.load(open(os.path.join(ROOT, "config.json"))).get("reels", {}).get("voiceRoom")
if VR and int(cfg.get("voice_chain", 1)) >= 2: voice = room(voice, VR.get("rt", 0.35), VR.get("wet", 0.07))
voice = to_lufs(voice, -17.0)
vr = np.sqrt(np.convolve((voice ** 2).mean(axis=1), np.ones(480) / 480, "same"))
talk = (20 * np.log10(vr + 1e-9) > -45).astype(np.float32)
hold = int(0.1 * SR); talk = np.convolve(talk, np.ones(hold), "same").clip(0, 1)            # 100 ms hold: no pumping between words
duck = follower(talk, 0.03, 0.4)                                                             # 0 = pause, 1 = voice talking

# ── music: pick, place on a bar, never loop
MUS = os.path.join(ROOT, "library/music")
def resolve(m):
    if m == "auto":
        appr = json.load(open(os.path.join(MUS, "approved/index.json"))); log_f = os.path.join(MUS, "approved/rotation.json")
        recent = json.load(open(log_f)) if os.path.exists(log_f) else []
        pool = [k for k in appr if k not in recent[-3:]] or list(appr)
        k = random.Random(os.path.basename(R)).choice(sorted(pool))
        if not os.environ.get("OUT"): json.dump((recent + [k])[-20:], open(log_f, "w"))   # previews don't count as a use
        return os.path.join(MUS, "approved", appr[k]["file"]), k
    if os.path.isabs(m) or os.path.exists(os.path.join(R, m)): return (m if os.path.isabs(m) else os.path.join(R, m)), m
    for d in ("approved", ""):
        f = os.path.join(MUS, d, "index.json")
        if os.path.exists(f) and m in json.load(open(f)): return os.path.join(MUS, d, json.load(open(f))[m]["file"]), m
    sys.exit(f"music {m!r} not found")
mpath, mid = resolve(os.environ.get("MUSIC") or cfg.get("music", "auto"))   # MUSIC=… auditions a track
if cfg.get("music", "auto") == "auto" and not os.environ.get("OUT"):   # pin the pick: a re-mix keeps the same track (and credit)
    cfg["music"] = mid; json.dump(cfg, open(os.path.join(R, "reel.json"), "w"), indent=1, ensure_ascii=False)
if not os.environ.get("OUT"):   # the caption must carry the CC-BY credit of the track this reel uses
    appr = os.path.join(MUS, "approved/index.json"); credit = json.load(open(appr)).get(mid, {}).get("attribution", "") if os.path.exists(appr) else ""
    open(os.path.join(R, "assets/audio/credit.txt"), "w").write(credit + ("\n" if credit else ""))
y, _ = librosa.load(mpath, sr=22050, mono=True)
tempo, beats = librosa.beat.beat_track(y=y, sr=22050, units="time"); bars = beats[::4]
need = T["total"] + 3.0
if "music_offset" in cfg and not os.environ.get("MUSIC"): off = float(cfg["music_offset"])
else:   # calmest bar start that still leaves the whole reel: the hook opens quiet, the beat comes in by itself
    on = librosa.onset.onset_strength(y=y, sr=22050); ot = librosa.times_like(on, sr=22050)
    ok = [b for b in bars if b + need <= len(y) / 22050] or [0.0]
    off = float(min(ok, key=lambda b: on[(ot >= b) & (ot < b + 3)].mean() if ((ot >= b) & (ot < b + 3)).any() else 9))
m = load(mpath, off)
if len(m) < N:   # too short: continue from an earlier bar with a 2 s equal-power crossfade (never a hard loop seam)
    x = int(2 * SR); back = load(mpath, float(bars[min(4, len(bars) - 1)]) if len(bars) else 0.0); t = np.linspace(0, np.pi / 2, x)[:, None]
    while len(m) < N:
        m = np.concatenate([m[:-x], m[-x:] * np.cos(t) + back[:x] * np.sin(t), back[x:]])
m = m[:N]
drops = sorted({T["vo"][l] for l in cfg.get("drops", [])})[:2]
if len(drops) == 2 and drops[1] - drops[0] < 8: drops = drops[:1]
turn = drops[0] if drops else T["vo"][min(2, len(T["vo"]) - 1)]
cta = T["vo"][cfg["ctaLine"]] if "ctaLine" in cfg else T["vo"][-1]
dark = filt(m, 4, 420, "low") * db(3)                                    # before the turn: the bed's low end only (drone + pulse)
thin = filt(m, 4, 1200, "low")                                            # under the CTA: thinner, no hats
ramp = lambda t0, d=0.6: np.clip((np.arange(N) / SR - t0) / d, 0, 1)[:, None]   # 0 → 1 over d seconds from t0
bed = dark * (1 - ramp(turn)) + m * ramp(turn)
bed = bed * (1 - ramp(cta - 0.3, 1.0)) + thin * ramp(cta - 0.3, 1.0)
bed = to_lufs(bed, -22.0)                                                # un-ducked; ducked 6 dB → about -28 under speech (owner 10-14: punchy, but the bed 3 dB under the first try)
pre = int(turn * SR); bed[:pre] *= db(-3)                                # the hook bed sits lower still
env = np.ones(N, np.float32); f = int(0.03 * SR)
for D in drops:                                                           # 0.35 s NEAR-silence (-24 dB) before each reveal word
    a, b = int((D - 0.37) * SR), int((D - 0.02) * SR); env[a:b] = db(-24); env[a - f:a] = np.linspace(1, db(-24), f); env[b:b + f] = np.linspace(db(-24), 1, f)
tail = int(2.5 * SR); env[-tail:] *= np.linspace(1, 0, tail) ** 1.5
bed *= env[:, None]
carved = filt(bed, 2, [200, 300], "band") * (db(-2.5) - 1) + filt(bed, 2, [2500, 5000], "band") * (db(-3.5) - 1) + bed
bed = (bed * (1 - duck[:, None]) + carved * duck[:, None]) * (1 - duck * (1 - db(-6)))[:, None]

# ── sfx: by ear (library/sfx-brand/ranked.json), rotated, jittered, levelled by loudness
ranked = json.load(open(os.path.join(ROOT, "library/sfx-brand/ranked.json")))
used = {}
def pick(role, salt):
    files = ranked.get(role, [])[:8]
    if not files: return None
    left = [f for f in files if f not in used.get(role, set())] or files    # no repeat inside a reel until the role runs out
    f = left[zlib.crc32(f"{role}{salt}".encode()) % len(left)]; used.setdefault(role, set()).add(f)
    x = load(os.path.join(ROOT, f), dur=6.0)
    semis = (zlib.crc32(f"j{salt}".encode()) % 31 - 15) / 10                  # ±1.5 semitones: no two hits sound identical
    if abs(semis) > 0.05: x = resample_poly(x, 1000, int(1000 * 2 ** (semis / 12)), axis=0).astype(np.float32)
    return x
LOUD = {   # LUFS of each sound in the mix (voice = -17): a hierarchy instead of everything near one level
    "whoosh": ("whoosh-soft", -31, 2), "whoosh-heavy": ("whoosh-heavy", -26, 3), "pop": ("notification", -32, 1),
    "swipe": ("glitch", -29, 2), "glitch": ("glitch", -29, 2), "tick": ("ui-tick", -36, 1), "hit": ("impact", -24, 3),
    "impact": ("impact", -23, 3), "shatter": ("glass", -26, 3), "heartbeat": ("heartbeat", -30, 2),
    "clock": ("clock", -32, 1),
    # word-synced foley (owner 10-14: sounds that follow what the narrator says; placed by tools/word_cues.py)
    "snap": ("snap", -27, 2), "typing": ("typing", -33, 1), "buzz": ("phone-buzz", -31, 1), "scratch": ("record-scratch", -26, 2),
    "camera": ("camera", -31, 1), "sting": ("stinger", -27, 2), "reverse": ("reverse-swell", -30, 2), "braam": ("braam", -24, 3),
    "sub": ("sub-drop", -27, 2)}
# the brand OUTRO HIT (owner 10-14: "the outro should always end with the same sound effect" as REEL-01): one fixed file,
# never rotated or pitched, always kept, and added at the end of the last spoken line if a reel's cues forget it
SIG = os.path.join(ROOT, "library/sfx-brand/signature/outro-hit.wav")
outro_t = next((c["t"] for c in cues if c["type"] == "outro-hit"), T["voEnd"][-1])
cues = [c for c in cues if c["type"] != "outro-hit"]
cue = sorted(({**c, "rank": LOUD.get(c["type"], ("", 0, 1))[2]} for c in cues), key=lambda c: (-c["rank"], c["t"]))
big = [outro_t]
kept = []
for c in cue:   # density cap: ≤ 7 per any 10 s window (owner wants sounds on the lines), big hits ≥ 4 s apart and not on a reveal
    if c["rank"] == 3 and (any(abs(c["t"] - b) < 4 for b in big) or any(abs(c["t"] - D) < 1.0 for D in drops)): continue
    if sum(1 for k in kept if abs(k["t"] - c["t"]) < 5) >= 12: continue
    if any(abs(k["t"] - c["t"]) < 0.25 for k in kept): continue           # never two sounds on the same syllable
    kept.append(c); big += [c["t"]] if c["rank"] == 3 else []
fx = np.zeros((N, 2), np.float32); soft = np.zeros((N, 2), np.float32)
sub_layer = lambda salt: (lambda s_: None if s_ is None else filt(filt(s_.mean(axis=1, keepdims=True).repeat(2, 1), 2, 30, "high"), 4, 100, "low"))(pick("sub-drop", salt))
for c in sorted(kept, key=lambda c: c["t"]):
    role, L, rank = LOUD.get(c["type"], ("whoosh-soft", -31, 1)); x = pick(role, c["t"])
    if x is None: continue
    x = to_lufs(x, L + 5 + c.get("gain", 0))   # +5 dB: effects drive the reel (owner 10-14)
    if role.startswith("whoosh"):   # high-passed off the voice body; its PEAK lands on the cut
        x = filt(x[: int(2 * SR)], 2, 250, "high"); pk = int(np.argmax(np.convolve(np.abs(x).mean(axis=1), np.ones(480) / 480, "same"))) / SR
        place(soft, x * np.minimum(1, np.linspace(4, 0, len(x)))[:, None], c["t"] - pk)
    elif rank == 3:
        place(fx, x[: int(3 * SR)], c["t"] - 0.005); sb = sub_layer(c["t"])
        if sb is not None: place(fx, to_lufs(sb, L - 3), c["t"])
    else: place(soft, x[: int(2.5 * SR)], c["t"])
OS = json.load(open(os.path.join(ROOT, "config.json"))).get("reels", {}).get("outroSound")
if OS:   # owner 10-15: a mysterious piano under the spoken tagline instead of the hit — from 1 s before the tagline, under the voice
    place(fx, to_lufs(load(os.path.join(ROOT, OS)), -24.0), max(0, T["vo"][-1] - 1.0))
else:
    place(fx, load(SIG), outro_t - 0.005)                                   # signature, at the level it had in REEL-01
for D in drops:   # the reveal: riser grows into the silence, then impact + mono sub on the word
    r = pick("riser", D)
    if r is not None: r = to_lufs(r[: int(2.0 * SR)], -27) * np.linspace(0, 1, int(2.0 * SR))[: len(r)][:, None] ** 2; place(fx, r, D - 0.37 - len(r) / SR)
    x = pick("impact", D); sb = sub_layer(D)
    if x is not None: place(fx, to_lufs(x[: int(3 * SR)], -22), D - 0.005)
    if sb is not None: place(fx, to_lufs(sb, -25), D)
soft *= (1 - duck * (1 - db(-3)))[:, None]                                 # small sounds tuck 3 dB under the voice
dr = None   # owner 10-14: a background "buzz" — the hook drone is off (the music bed carries the tension)
if dr is not None:
    end = int(max(1.0, turn - 0.4) * SR); dr = np.concatenate([dr] * int(np.ceil(end / len(dr))))[:end]
    dr[: int(0.3 * SR)] *= np.linspace(0, 1, int(0.3 * SR))[:, None]; dr[-int(0.8 * SR):] *= np.linspace(1, 0, int(0.8 * SR))[:, None]
    place(fx, to_lufs(dr, -33), 0)

# ── master: sum → -14 LUFS → oversampled limiter (true peak ≤ -1 dBTP)
mix = voice + bed + fx + soft
def master(x, gain_db):
    with tempfile.TemporaryDirectory() as d:
        sf.write(f"{d}/a.wav", x * db(gain_db), SR, subtype="FLOAT")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{d}/a.wav", "-af",
                        "aresample=192000,alimiter=limit=0.84:attack=1.5:release=80:level=disabled,aresample=48000", "-c:a", "pcm_f32le", f"{d}/b.wav"], check=True)
        out, _ = sf.read(f"{d}/b.wav", dtype="float32")
        tp = [l for l in subprocess.run(["ffmpeg", "-hide_banner", "-i", f"{d}/b.wav", "-af", "ebur128=peak=true", "-f", "null", "-"],
                                         capture_output=True, text=True).stderr.splitlines() if l.strip().startswith("Peak:")]
    return out[:N], float(tp[-1].split()[1]) if tp else 0.0
TARGET = -11.0   # owner 10-14: Zoltium reels are louder and punchier on earphones; -11 LUFS, true peak still ≤ -1 dBTP
g = TARGET - lufs(mix); out, tp = master(mix, g)
g += TARGET - lufs(out); out, tp = master(mix, g)                          # one correction pass for what the limiter took
log(f"Audio mixed · {cfg.get('title', os.path.basename(R))} · music {mid}") if not os.environ.get("OUT") else None
fo = int(0.9 * SR); out[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 2     # owner 10-15: the reel ends clean with its outro clip — no hard cut of the piano
sf.write(os.environ.get("OUT") or os.path.join(R, "assets/audio/final.wav"), out, SR, subtype="PCM_24")
L = lambda x: round(lufs(x), 1)
print(json.dumps({"total": T["total"], "music": mid, "music_offset": round(off, 2), "tempo": round(float(np.atleast_1d(tempo)[0])), "drops": drops,
                  "LUFS": L(out), "truepeak_dBTP": tp, "voice": L(voice), "bed": L(bed), "voice_minus_bed_dB": round(L(voice) - L(bed), 1),
                  "sfx_kept": f"{len(kept)}/{len(cues)} + outro signature", "audio_ok": bool(abs(L(out) - TARGET) <= 0.8 and tp <= -0.9)}))
