"""DecodeHer factory (owner 10-14: "I don't want to sit all day fixing bugs — automate it, that's the whole idea").
One conductor runs the whole line for every approved reel, on its own, with no chat session needed:

  voice → plan (shots + sounds) → clips → mix → sheets → judge → quality gate (one automatic re-search) → render → queue

* Each reel moves to its next stage the moment the previous one finishes; reels never wait for each other.
* State is read from the files on disk every loop, so a crash, a reboot or a manual fix just resumes where it was.
* Lanes with limits (6 GB GPU, 16 cores, a gentle Pinterest account): voice 1 · plan 2 · clips 1 · mix 2 · sheets 2 · judge 3 · render 1 · queue 1.
* The two thinking steps (planning a reel, judging its clips) call Claude headless (`claude -p`): Sonnet plans, Haiku judges.
* A failing step is retried twice (with a pause), then the reel is parked with the reason in logs/reels/<reel>.log and on the board.
* Renders take turns through logs/render.lock (shared with tools/render_line.sh); no process-name scanning anywhere.
* Writes logs/factory.json (lanes, per-reel stage, errors) for the pixel studio, and plain lines to logs/activity.log.

Run:   python3 tools/factory.py            (or as the systemd user service decodeher-factory, see tools/factory.service)
Cloud: python3 tools/factory.py --once --max-minutes 300   (GitHub Actions, brain/cloud-architecture.md): --once exits 0 when no job
       runs and nothing can start; --max-minutes N stops STARTING jobs after N min, waits for the running ones (never kills a
       render or queue job) and exits 0. No flag = the service: runs forever, exactly as before.
Reels: every folder listed in the batch files of config.json "factory.batches" (default: reels/w2-batch.json)."""
import shutil, fcntl, glob, json, os, re, signal, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
LOGS = os.path.join(ROOT, "logs"); os.makedirs(f"{LOGS}/reels", exist_ok=True)
CFG = json.load(open("config.json")).get("factory", {}) if os.path.exists("config.json") else {}
BATCHES = CFG.get("batches", ["reels/w2-batch.json"])
LANES = {"voice": 1, "plan": 2, "clips": 1, "mix": 2, "sheets": 2, "judge": 3, "render": 1, "queue": 1}
UV_PY = ["uv", "run", "-q", "--python", "3.11"]
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
def _arg(name):   # cloud flags (10-15); the systemd service passes none
    a = sys.argv[1:]
    if name not in a: return None
    try: return float(a[a.index(name) + 1])
    except (IndexError, ValueError): sys.exit(f"usage: factory.py [--once] [{name} N]")
ONCE, MAX_MIN = "--once" in sys.argv[1:], _arg("--max-minutes")
BOUNDED = ONCE or MAX_MIN is not None   # False for the systemd service: every check below that uses it is skipped

def log(msg):
    with open(f"{LOGS}/activity.log", "a") as f: f.write(time.strftime("%H:%M:%S") + "  " + msg + "\n")
def jload(p, d=None):
    try: return json.load(open(p))
    except Exception: return d
def title(R): return (jload(f"{R}/reel.json", {}) or {}).get("title") or os.path.basename(R)
def clips_have(R, shots, n): return bool(glob.glob(f"{R}/clips/cand/{n:02d}/*.mp4"))

# ── what a reel needs next, read from disk ────────────────────────────────────────────────────────────────────────────────
def stage_of(R):
    slug = os.path.basename(R); cfg = jload(f"{R}/reel.json", {}) or {}
    if cfg.get("parked"): return "parked"
    queued = os.path.exists(f"logs/queued/{slug}")   # written by queue_reel.sh only after the relay confirmed the post
    if queued: return "done"
    if os.path.exists(f"deliverables/week-2/{slug}.mp4"): return "queue"
    tj = f"{R}/assets/timing.js"
    if not (os.path.exists(tj) and '"words"' in open(tj).read()): return "voice"
    shots = jload(f"{R}/shots.json")
    if not shots or not os.path.exists(f"{R}/sfx.json") or not cfg.get("accent"): return "plan"
    body = [n for n, s in enumerate(shots) if s["q"] != "OUTRO"]
    if not clips_have(R, shots, 0) or sum(clips_have(R, shots, n) for n in body) < len(body) - 1: return "clips"
    if not os.path.exists(f"{R}/assets/audio/final.wav"): return "mix"
    idx = jload(f"{R}/clips/sheets/index.json", {}) or {}
    if not idx or any(not os.path.exists(f"{R}/clips/sheets/{k}.jpg") for k, e in idx.items() if e.get("clips")): return "sheets"
    need = [k for k, e in idx.items() if e.get("clips")]
    if any(jload(f"{R}/clips/judge/{k}.json") is None for k in need): return "judge"   # 10-15: a judge file Haiku wrote as BROKEN json counts as missing (it parked w2-11)
    if weak_shots(R) and cfg.get("clip_round", 1) < 2: return "research"
    return "render"

def weak_shots(R):
    """shots whose best usable clip (style ≥ 5, quality ≥ 4, no text) shows the words poorly (meaning < 5)"""
    idx = jload(f"{R}/clips/sheets/index.json", {}) or {}; out = []
    for k, e in idx.items():
        j = (jload(f"{R}/clips/judge/{k}.json", {}) or {}).get("clips", {})
        best = max([v.get("meaning", 0) for v in j.values() if v.get("style", 0) >= 5 and v.get("quality", 0) >= 4 and not v.get("text")] or [0])
        if best < 5: out.append(int(k))
    if 0 in out: return out   # 10-15: an empty OPENING shot has no previous clip to continue and stops the render, so always re-search it
    return out if len(out) >= 4 else []   # a few weak shots just continue the previous clip; many means re-search

# ── the commands each stage runs ─────────────────────────────────────────────────────────────────────────────────────────
def claude(prompt, model, tools):
    return [CLAUDE, "-p", prompt, "--model", model, "--allowedTools", *tools, "--output-format", "text"]

PLAN_PROMPT = open(os.path.join(os.path.dirname(__file__), "factory_plan_prompt.txt")).read() if os.path.exists(os.path.join(os.path.dirname(__file__), "factory_plan_prompt.txt")) else ""

def commands(R, stage):
    py, rel = sys.executable, os.path.relpath(R, ROOT)
    if stage == "voice":
        return [[py, "tools/reel_vo.py", rel], [py, "tools/reel_timing.py", rel],
                ["uv", "run", "-q", "--with", "faster-whisper", "--with", "numpy", "python", "-W", "ignore", "tools/align_words.py", rel]]
    if stage == "plan":
        return [claude(PLAN_PROMPT.replace("{REEL}", os.path.join(ROOT, rel)), "sonnet", ["Read", "Write", "Bash(python3:*)"])]
    if stage == "clips":
        return [["uv", "run", "-q", "--with", "gallery-dl", "--with", "yt-dlp", "--with", "secretstorage", "python", "tools/fetch_pool.py", rel, "--per", "8"]]
    if stage == "mix":
        return [[py, "tools/shot_times.py", rel], [py, "tools/word_cues.py", rel], [py, "tools/fill_page.py", rel],
                ["uv", "run", "-q", "--with", "numpy", "--with", "scipy", "--with", "soundfile", "--with", "pyloudnorm", "--with", "librosa",
                 "python", "-W", "ignore", "tools/reel_mix.py", rel]]
    if stage == "sheets":
        return [["bash", "tools/reel_prep.sh", rel]]
    if stage == "judge":
        prompt = subprocess.run([py, "tools/judge_prompt.py", rel], capture_output=True, text=True, check=True).stdout
        return [claude(prompt, "haiku", ["Read", "Write"])]
    if stage == "research":
        weak = weak_shots(R)
        return [[py, "tools/factory_research.py", rel, ",".join(map(str, weak))]]
    if stage == "render":
        return [["bash", "-c", f"exec 9>logs/render.lock; flock 9; bash tools/reel_finish.sh {rel}"]]
    if stage == "queue":
        return [["bash", "tools/queue_reel.sh", rel]]
    return []

LANE_OF = {"voice": "voice", "plan": "plan", "clips": "clips", "mix": "mix", "sheets": "sheets", "judge": "judge", "research": "clips",
           "render": "render", "queue": "queue"}
SAY = {"voice": "Recording voice", "plan": "Planning shots + sounds", "clips": "Clip search", "mix": "Audio mixing",
       "sheets": "Contact sheets", "judge": "Judging", "research": "Second clip search", "render": "Rendering", "queue": "Queuing post"}

# ── the conductor ──────────────────────────────────────────────────────────────────────────────────────────────────────────
class Job:
    def __init__(self, R, stage):
        self.R, self.stage, self.cmds, self.i, self.p, self.started = R, stage, commands(R, stage), 0, None, time.time()
        self.logf = open(f"{LOGS}/reels/{os.path.basename(R)}.log", "a")
        self.logf.write(f"\n=== {time.strftime('%F %T')} {stage}\n"); self.next()
    def next(self):
        if self.i >= len(self.cmds): self.p = None; return False
        self.logf.write("$ " + " ".join(self.cmds[self.i])[:400] + "\n"); self.logf.flush()
        self.p = subprocess.Popen(self.cmds[self.i], cwd=ROOT, stdout=self.logf, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
        self.i += 1; return True
    def poll(self):   # None = running, True = finished ok, False = failed
        rc = self.p.poll()
        if rc is None: return None
        if rc != 0:
            self.logf.flush(); self.limit = any(w in open(self.logf.name).read()[-600:].lower() for w in ("session limit", "usage limit", "hit your limit", "rate limit"))   # 10-15: Claude words its cap several ways
            self.logf.write(f"exit {rc}\n"); self.logf.close(); return False
        if self.next(): return None
        self.logf.close(); return True

def reels():
    out = []
    for b in BATCHES:
        for r in jload(b, []) or []:
            if os.path.isdir(r) and r not in out: out.append(r)
    return out

def main():
    lock = open(f"{LOGS}/factory.lock", "w")
    try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError: sys.exit("factory already running")
    running, fails, cool, last_state, last_tick, last_clean = {}, {}, {}, {}, 0, 0
    def stop(*_):
        for j in running.values():
            try: os.killpg(j.p.pid, signal.SIGTERM)
            except Exception: pass
        sys.exit(0)
    signal.signal(signal.SIGTERM, stop); signal.signal(signal.SIGINT, stop)
    log("Factory started · watching " + ", ".join(BATCHES) + (f" · cloud run{' --once' if ONCE else ''}{f' · {MAX_MIN:g} min' if MAX_MIN is not None else ''}" if BOUNDED else ""))
    t0 = time.time()
    def time_up(): return MAX_MIN is not None and time.time() - t0 > MAX_MIN * 60
    def finish(why):   # cloud run only, and only when nothing is running (a running render/queue job is never killed)
        log(f"Factory run ends · {why}"); sys.exit(0)
    while True:
        # finished jobs
        for R, j in list(running.items()):
            res = j.poll()
            if res is None: continue
            del running[R]; slug = os.path.basename(R)
            if res:
                fails.pop((R, j.stage), None); log(f"{SAY[j.stage]} done · {title(R)}")
                if j.stage == "research":
                    cfg = jload(f"{R}/reel.json", {}); cfg["clip_round"] = 2; json.dump(cfg, open(f"{R}/reel.json", "w"), indent=1, ensure_ascii=False)
            elif getattr(j, "limit", False):   # 10-15: Claude "session limit" is not a reel fault (w2-07 got parked by it) — wait 30 min, don't count a failure
                cool[R] = time.time() + 1800; log(f"{SAY[j.stage]} paused · {title(R)} · Claude session limit, retry in 30 min")
            else:
                n = fails.get((R, j.stage), 0) + 1; fails[(R, j.stage)] = n
                if n >= 3:
                    cfg = jload(f"{R}/reel.json", {}); cfg["parked"] = f"{j.stage} failed 3 times — see logs/reels/{slug}.log"
                    json.dump(cfg, open(f"{R}/reel.json", "w"), indent=1, ensure_ascii=False)
                    log(f"PARKED · {title(R)} · {j.stage} failed 3× (logs/reels/{slug}.log)")
                else:
                    cool[R] = time.time() + 120 * n; log(f"{SAY[j.stage]} failed · {title(R)} · retry {n}/2 in {2 * n} min")
        # disk guard (10-14 the disk filled up mid-render and killed the factory): below 4 GB free, clean caches and start nothing new
        free = shutil.disk_usage(ROOT).free / 1e9
        draining = time_up()   # time is up: start nothing new, let running jobs finish
        if BOUNDED and not running and free < 4: finish(f"disk low ({free:.1f} GB free), nothing running")
        if free < 4:
            if time.time() - last_clean > 600:
                last_clean = time.time(); log(f"Disk low · {free:.1f} GB free · cleaning caches, new jobs wait")
                subprocess.run("rm -rf ~/.cache/hyperframes/history/*", shell=True, cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            # 10-15: still beat (the Manager restarted a merely-waiting factory every 5 min) and still nudge the relay (posts stay on time)
            try: open(f"{LOGS}/factory.beat", "w").write(time.strftime("%F %T"))
            except OSError: pass
            if time.time() - last_tick > 60:
                last_tick = time.time(); subprocess.Popen(["node", "tools/relay_tick.js"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            time.sleep(15); continue
        # start what can start
        used = {}
        for j in running.values(): used[LANE_OF[j.stage]] = used.get(LANE_OF[j.stage], 0) + 1
        state, waiting = {}, []
        for R in reels():
            st = stage_of(R); state[os.path.basename(R)] = st
            if BOUNDED and R not in running and st not in ("done", "parked"): waiting.append(R)
            if draining or R in running or st in ("done", "parked") or cool.get(R, 0) > time.time(): continue
            lane = LANE_OF[st]
            if used.get(lane, 0) >= LANES[lane]: continue
            try: running[R] = Job(R, st)
            except Exception as e:
                log(f"{SAY[st]} could not start · {title(R)} · {e}"); cool[R] = time.time() + 300; continue
            used[lane] = used.get(lane, 0) + 1; log(f"{SAY[st]} · {title(R)}")
        snap = {"at": time.strftime("%F %T"), "reels": state, "running": {os.path.basename(R): j.stage for R, j in running.items()},
                "lanes": {k: [os.path.basename(R) for R, j in running.items() if LANE_OF[j.stage] == k] for k in LANES},
                "parked": {os.path.basename(R): (jload(f"{R}/reel.json", {}) or {}).get("parked") for R in reels() if (jload(f"{R}/reel.json", {}) or {}).get("parked")}}
        if snap["reels"] != last_state.get("reels") or snap["running"] != last_state.get("running"):
            json.dump(snap, open(f"{LOGS}/factory.json", "w"), indent=1); last_state = snap
        if time.time() - last_tick > 60:   # posts land on time: nudge the relay while a post is due or processing
            last_tick = time.time(); subprocess.Popen(["node", "tools/relay_tick.js"], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
        try: open(f"{LOGS}/factory.beat", "w").write(time.strftime("%F %T"))   # heartbeat for the Manager (tools/manager.py)
        except OSError: pass
        if BOUNDED and not running:
            if draining: finish(f"time is up ({MAX_MIN:g} min)")
            # nothing runs, so every reel that could start just did; the rest are done, parked or cooling. Wait out a short retry
            # pause (2-5 min); a long one (Claude's 30-min usage limit) ends the run, the next run picks the reel up.
            if ONCE and not any(cool.get(R, 0) <= time.time() + 600 for R in waiting):
                finish("nothing left to start" + (f" · {len(waiting)} reel(s) waiting on a long pause" if waiting else ""))
        time.sleep(15)

if __name__ == "__main__":
    main()
