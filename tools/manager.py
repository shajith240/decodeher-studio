"""The MANAGER (owner 10-14: "add a manager that figures out what's going wrong and fixes it, so the flow keeps running").
Runs as the systemd user service decodeher-manager. Every 2 minutes it walks the line:
  1. fixed checks it repairs on its own: a dead service, a frozen factory (no heartbeat), a full disk, a stuck job,
     a post that is late on the relay, the same reel booked twice;
  2. anything that needs thinking (a crash, a reel parked after 3 failures, a stage failing again and again, a post the relay
     could not publish) becomes an INCIDENT for a Claude agent (headless, tools/manager_prompt.txt) that reads the logs,
     fixes the cause in tools/ and lets the reel retry. One agent at a time, each incident at most once per 2 h, 8 per day.
Writes logs/manager.json (the studio's Manager desk) and "Manager · ..." lines in logs/activity.log."""
import datetime, fcntl, glob, json, os, re, shutil, signal, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
LOGS = os.path.join(ROOT, "logs"); os.makedirs(f"{LOGS}/manager", exist_ok=True)
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
EVERY, DISK_LOW_GB, STUCK_MIN, AGENT_PER_DAY = 120, 6, 45, 8
# where each problem lives in the studio (the Manager walks there)
STATION = {"voice": "voice", "plan": "scout", "clips": "scout", "research": "scout", "mix": "judge", "sheets": "judge",
           "judge": "judge", "render": "edit", "queue": "post", "post": "post"}

def log(msg):
    with open(f"{LOGS}/activity.log", "a") as f: f.write(time.strftime("%H:%M:%S") + "  Manager · " + msg + "\n")
def jload(p, d=None):
    try: return json.load(open(p))
    except Exception: return d
def sh(cmd, timeout=120):
    try: return subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, timeout=timeout, cwd=ROOT).stdout
    except Exception: return ""

S = jload(f"{LOGS}/manager.json", {}) or {}
S.setdefault("history", []); S.setdefault("seen", {}); S.setdefault("agents_today", [time.strftime("%F"), 0])
agent = None   # the running Claude agent: (Popen, key, target, started)

def save(status, text, target=""):
    S.update(at=time.strftime("%F %T"), status=status, text=text, target=target, agent=bool(agent))
    tmp = f"{LOGS}/manager.json.tmp"; json.dump(S, open(tmp, "w"), indent=1); os.replace(tmp, f"{LOGS}/manager.json")
def did(text, target=""):
    log(text); S["history"] = ([{"at": time.strftime("%H:%M"), "text": text, "target": target}] + S["history"])[:30]

# ── fixed checks ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def services():
    for svc in ("decodeher-factory", "decodeher-board"):
        if sh(["systemctl", "--user", "is-active", svc]).strip() != "active":
            sh(["systemctl", "--user", "restart", svc]); did(f"{svc.split('-')[1]} service was down · restarted it")

def heartbeat():
    b = f"{LOGS}/factory.beat"
    if os.path.exists(b) and time.time() - os.path.getmtime(b) > 300:
        sh(["systemctl", "--user", "restart", "decodeher-factory"]); did("factory froze (no heartbeat for 5 min) · restarted it")

def pin_inbox():   # 10-16: Pinterest links the owner sends in Telegram → tools/pin_intake.py (in the background, one at a time)
    try:
        subprocess.Popen(["flock", "-n", f"{LOGS}/pin_intake.lock", "python3", "tools/pin_intake.py"], cwd=ROOT,
                         stdout=open(f"{LOGS}/pin_intake.log", "a"), stderr=subprocess.STDOUT, start_new_session=True)
    except Exception as e: log(f"pin intake could not start: {e}")

def tmp_space():   # 10-16: RAM-backed /tmp filled (HyperFrames frame cache, 3.8 GB) and a render failed — keep it clear
    free = shutil.disk_usage("/tmp").free / 1e9
    if free >= 1.5: return
    if any(st == "render" for st in ((jload(f"{LOGS}/factory.json", {}) or {}).get("running", {}) or {}).values()): return   # never under a running render
    c = f"/tmp/hyperframes-extract-cache-{os.getuid()}"
    gone = sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(c) for f in fs) if os.path.isdir(c) else 0
    shutil.rmtree(c, ignore_errors=True)
    did(f"temp space low ({free:.1f} GB free in /tmp) · cleared the render cache ({gone / 1e9:.1f} GB) · now {shutil.disk_usage('/tmp').free / 1e9:.1f} GB")

def disk():
    free = shutil.disk_usage(ROOT).free / 1e9
    if free >= DISK_LOW_GB: return
    busy = set((jload(f"{LOGS}/factory.json", {}) or {}).get("running", {}))
    gone = 0
    for bg in glob.glob("reels/*/assets/bg.mp4"):   # the ~600 MB cut film of a reel that is already rendered (every render re-cuts it)
        slug = bg.split("/")[1]; out = f"deliverables/week-2/{slug}.mp4"
        if slug not in busy and os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(bg):
            gone += os.path.getsize(bg); os.remove(bg)
    # 10-15 (owner: "why didn't the manager resolve it?"): bg.mp4 films are no longer the big files — also clear, for reels that are
    # BOOKED or POSTED (logs/queued marker) and not running: the 350 MB master (the posting copy stays in deliverables/queue/booked),
    # raw Pinterest candidates + contact sheets (the cut clips/seg stay, so a redo can still re-render), and raw voice takes
    import shutil as _sh
    for mk in glob.glob(f"{LOGS}/queued/*"):
        slug = os.path.basename(mk)
        if slug in busy: continue
        for f in [f"deliverables/week-2/{slug}.mp4"]:
            if os.path.exists(f): gone += os.path.getsize(f); os.remove(f)
        for d in (f"reels/{slug}/clips/cand", f"reels/{slug}/clips/sheets", f"reels/{slug}/assets/vo/raw"):
            if os.path.isdir(d):
                gone += sum(os.path.getsize(os.path.join(a, x)) for a, _, fs in os.walk(d) for x in fs if os.path.isfile(os.path.join(a, x)))
                _sh.rmtree(d, ignore_errors=True)
    sh("python3 tools/pool_prune.py --cap 900", timeout=300)   # 10-18: unusable + oldest unused pool clips (permanent disk fix)
    sh("npm cache clean --force", timeout=120)   # the npm download cache refills to ~0.5 GB
    sh("rm -rf ~/.cache/hyperframes/history/*", timeout=120)   # not `uv cache prune`: it waits on the lock running jobs hold, and on btrfs frees ~nothing
    now = shutil.disk_usage(ROOT).free / 1e9
    if now < DISK_LOW_GB - 2 and time.time() - S.get("disk_told", 0) > 6 * 3600:   # still too low: tell the owner (Telegram via HQ), max every 6 h
        S["disk_told"] = time.time()
        sh(f"HQ_URL=$(cat .secrets/HQ_URL) HQ_KEY=$(cat .secrets/HQ_KEY) python3 tools/cloud/report.py event error 'Disk almost full on the laptop ({now:.1f} GB free) — I cleared what I safely could; the factory pauses until there is room.'", timeout=60)
    if not gone and time.time() - S.get("disk_said", 0) < 1800: return   # nothing to clear: say so at most every 30 min
    S["disk_said"] = time.time()
    did(f"disk low ({free:.1f} GB free) · cleared {gone / 1e9:.1f} GB (masters of booked reels, raw clips, takes, caches) · now {now:.1f} GB")

def stuck():
    st = jload(f"{LOGS}/factory.json", {}) or {}
    pid = sh(["systemctl", "--user", "show", "-p", "MainPID", "--value", "decodeher-factory"]).strip()
    for slug, stage in st.get("running", {}).items():
        lf = f"{LOGS}/reels/{slug}.log"
        if not os.path.exists(lf) or time.time() - os.path.getmtime(lf) < STUCK_MIN * 60: continue
        if stage == "render" and os.path.exists(f"reels/{slug}/renders"): continue   # the render writes no log; its own 25 min timeout ends it
        for p in glob.glob("/proc/[0-9]*"):   # the job's leader: a child of the factory whose command names this reel
            try:
                stat = open(f"{p}/stat").read().rsplit(")", 1)[1].split()
                if stat[1] == pid and f"reels/{slug}" in open(f"{p}/cmdline").read().replace("\0", " "):
                    os.killpg(int(p.split("/")[-1]), signal.SIGTERM)
                    did(f"{slug} · {stage} hung {STUCK_MIN}+ min with no output · stopped it, the factory retries", STATION.get(stage, ""))
            except Exception: pass

def queue_rows():
    rows = []
    for l in sh(["node", "tools/ig_queue.js", "ids"]).splitlines():
        m = re.match(r"(\S+)\s+(\S+)\s+(\d{4}-\d\d-\d\d \d\d:\d\d) IST\s+(.+)", l)
        if m: rows.append({"id": m[1], "status": m[2], "at": datetime.datetime.strptime(m[3], "%Y-%m-%d %H:%M"), "title": m[4].strip()})
    return rows

def posts(incidents):
    rows = queue_rows(); now = datetime.datetime.now()
    seen = {}
    for r in rows:   # the same reel booked twice (10-14): keep the earlier slot, drop the later one, close the gap
        if r["status"] != "queued": continue
        key = re.sub(r"^\d+-", "", r["title"])
        if key in seen:
            sh(["node", "tools/ig_queue.js", "remove", r["id"]]); sh(["node", "tools/ig_queue.js", "reslot"])
            did(f"'{key}' was booked twice · removed the second booking, moved the rest up", "post"); return
        seen[key] = r
    for r in rows:
        late = (now - r["at"]).total_seconds() / 60
        if r["status"] in ("queued", "processing") and late > 15:
            sh(["node", "tools/relay_tick.js"])
            if late > 45: incidents.append((f"post-late-{r['id']}", "post", f"Instagram post '{r['title']}' was due at {r['at']:%F %H:%M} IST and is still "
                                             f"'{r['status']}' {late:.0f} min later. Find out why (node tools/ig_queue.js status shows the relay log)."))
        if r["status"] in ("failed", "error"):
            incidents.append((f"post-failed-{r['id']}", "post", f"The relay marked post '{r['title']}' ({r['at']:%F %H:%M}) as {r['status']}. "
                                                                 "Look at `node tools/ig_queue.js status` and say what is needed."))
    for f in glob.glob("deliverables/queue/*-FINAL.mp4") + glob.glob("deliverables/queue/booked/*-FINAL.mp4"):   # 10-15: a cut-off file got booked and nearly posted — every queued video must decode
        title = os.path.basename(f)[:-10]
        if not any(r["title"] == title and r["status"] == "queued" for r in rows): continue
        ok = S.setdefault("probed", {}).get(f) == os.path.getmtime(f)
        if not ok and sh(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).strip():
            S["probed"][f] = os.path.getmtime(f); continue
        if not ok: incidents.append((f"broken-video-{title}", "post", f"The queued post '{title}' has a BROKEN local video ({f} does not decode). "
                                     "Re-encode it from deliverables/week-2/<reel>.mp4 exactly like tools/queue_reel.sh does, into a new empty folder, and run "
                                     "`node tools/ig_queue.js replace <that folder>` (same slot, same caption). You may run that one replace command."))
    upcoming = [r for r in rows if r["status"] == "queued"]
    S["queue_until"] = max(r["at"] for r in upcoming).strftime("%a %d %H:%M") if upcoming else ""

def thinking_problems(incidents):
    st = jload(f"{LOGS}/factory.json", {}) or {}
    parked = {k: v for k, v in (st.get("parked") or {}).items() if (jload(f"reels/{k}/reel.json", {}) or {}).get("parked")}   # the snapshot can lag
    parked = {k: v for k, v in parked.items() if not str(v).lower().startswith("owner")}   # 10-15: held ON PURPOSE by the owner — not an incident (it burned agent runs)
    if parked:   # ONE agent for all of them (10-15: 6 reels parked by one shared cause used up all 8 agent runs by 2 am)
        rows = "\n".join(f"- reels/{slug}: {why}" for slug, why in parked.items())
        incidents.append(("parked-" + ",".join(sorted(parked)), next(iter(parked.values())).split()[0] if len(parked) == 1 else "",
                          f"{len(parked)} reel(s) are PARKED (often one shared cause — look for it first):\n{rows}\n"
                          "Fix the cause, then remove 'parked' from each reel.json."))
    since = S.get("checked", time.strftime("%F %T", time.localtime(time.time() - EVERY)))
    j = sh(["journalctl", "--user", "-u", "decodeher-factory", "--since", since, "--no-pager", "-o", "cat"])
    if "Traceback" in j:
        tb = j[j.rindex("Traceback"):][-1500:]
        incidents.append(("crash-" + re.sub(r"\W", "", tb.splitlines()[-1])[:60], "", "The factory process CRASHED:\n" + tb))
    fail2 = []
    try:   # only lines written since the last check: remember the byte offset (comparing "HH:MM" text broke after midnight, 10-15)
        with open(f"{LOGS}/activity.log", "rb") as f:
            size = f.seek(0, 2); pos = S.get("act_pos", size)
            f.seek(pos if pos <= size else 0); new = f.read().decode("utf-8", "replace"); S["act_pos"] = f.tell()
        for l in new.splitlines():
            m = re.match(r"(\d\d:\d\d:\d\d)\s+(.+?) failed · (.+?) · retry 2/2", l)
            if m: fail2.append(f"stage '{m[2]}' for reel '{m[3]}'")
        if fail2:
            incidents.append(("fail2-" + ",".join(sorted(set(fail2)))[:80], "", "These failed twice in a row (one try left before they park):\n- " + "\n- ".join(sorted(set(fail2)))
                              + "\nFind each reel in reels/ by the title in its reel.json, read its log and fix the cause now (often one shared cause)."))
    except OSError: pass

# ── the agent ────────────────────────────────────────────────────────────────────────────────────────────────────────────
TOOLS = ["Read", "Edit", "Write", "Glob", "Grep", "Bash(python3:*)", "Bash(uv run:*)", "Bash(systemctl --user:*)", "Bash(journalctl --user:*)",
         "Bash(tail:*)", "Bash(head:*)", "Bash(ls:*)", "Bash(grep:*)", "Bash(cat logs/:*)", "Bash(ffprobe:*)", "Bash(df:*)", "Bash(du:*)",
         "Bash(bash -n:*)", "Bash(node --check:*)", "Bash(node tools/ig_queue.js status)", "Bash(node tools/ig_queue.js ids)", "Bash(node tools/ig_queue.js replace:*)", "Bash(ffmpeg:*)"]
DENY = ["Read(./.env)", "Read(**/.env)", "Read(./.relay.json)", "Read(**/.relay.json)", "Read(~/.config/rclone/**)", "Bash(cat .env:*)"]

def start_agent(key, target, text):
    global agent
    day = time.strftime("%F")
    if S["agents_today"][0] != day: S["agents_today"] = [day, 0]
    if S["agents_today"][1] >= AGENT_PER_DAY:
        if S["seen"].get("cap") != day: S["seen"]["cap"] = day; did("daily limit of agent fixes reached · problems wait for the owner")
        return
    S["agents_today"][1] += 1; S["seen"][key] = time.time()
    prompt = open("tools/manager_prompt.txt").read().replace("{ROOT}", ROOT).replace("{INCIDENT}", text)
    out = open(f"{LOGS}/manager/{time.strftime('%m%d-%H%M%S')}-{re.sub(r'[^a-z0-9-]', '', key.lower())[:40]}.log", "w")
    out.write(text + "\n\n---\n"); out.flush()
    p = subprocess.Popen([CLAUDE, "-p", prompt, "--model", "sonnet", "--allowedTools", *TOOLS, "--disallowedTools", *DENY, "--output-format", "text"],
                         cwd=ROOT, stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
    agent = (p, key, target, time.time(), out)
    did("looking into: " + text.splitlines()[0][:110], target)

def check_agent():
    global agent
    if not agent: return
    p, key, target, t0, out = agent
    if p.poll() is None:
        if time.time() - t0 > 1500:
            os.killpg(p.pid, signal.SIGTERM); out.close(); agent = None; did("fix took over 25 min · stopped it, will look again later", target)
        return
    out.close(); agent = None
    body = open(out.name).read().split("---", 1)[-1]
    if any(w in body.lower() for w in ("session limit", "usage limit", "hit your limit", "rate limit")):   # 10-14 21:44: agents died silently on the cap
        S["agents_today"][1] = max(0, S["agents_today"][1] - 1); S["seen"].pop(key, None); S["claude_wait"] = time.time() + 1800
        did("Claude is at its usage limit · the problem waits, I'll try again in 30 min", target); return
    if "api error" in body.lower() or not any(l.strip().startswith(("FIXED", "NEEDS OWNER")) for l in body.splitlines()):   # 10-15: a dropped
        S["agents_today"][1] = max(0, S["agents_today"][1] - 1); S["seen"].pop(key, None); S["claude_wait"] = time.time() + 600   # connection is not a fix
        did("couldn't reach Claude (connection error) · I'll try that problem again in 10 min", target); return
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    res = next((l for l in reversed(lines) if l.startswith(("FIXED", "NEEDS OWNER"))), lines[-1] if lines else "no answer")
    did(res[:220], target)
    if res.startswith("NEEDS OWNER"): S["needs_owner"] = ([{"at": time.strftime("%F %H:%M"), "text": res}] + S.get("needs_owner", []))[:10]

def main():
    lock = open(f"{LOGS}/manager.lock", "w")
    try: fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError: sys.exit("manager already running")
    log("on duty · checking the line every 2 min")
    while True:
        try:
            save("checking", "walking the line")
            check_agent()
            services(); heartbeat(); disk(); tmp_space(); pin_inbox(); stuck()
            incidents = []; posts(incidents); thinking_problems(incidents)
            # 10-18 owner ("the manager isn't even working"): the disk sat under 4 GB, the routine cleanup freed 0 GB and the whole
            # factory waited 20 min with nobody acting. If the cleanup can't get it over 4 GB, a Claude agent finds and frees space.
            free_gb = shutil.disk_usage(ROOT).free / 1e9
            if free_gb < 4:
                incidents.append(("disk-full", "", f"The laptop disk has {free_gb:.1f} GB free; the factory pauses all new work under 4 GB and the "
                                  "routine cleanup (tools/manager.py disk(), tools/pool_prune.py) could not fix it. Find what is using space "
                                  "(du on reels/, deliverables/, library/, ~/.cache, ~/.npm, /tmp; on btrfs `du` of ~/.cache/uv is not real) and free "
                                  "at least 1.5 GB SAFELY: caches, re-downloadable files, finished reels' working files. Never delete the owner's "
                                  "files, booked/queued videos, library/hook-pool, library/clips, logs/queued markers or anything in brain/. Moving "
                                  "old archives to Drive with `rclone move` is fine. Then make the fix permanent in tools/ so it doesn't recur."))
            S["checked"] = time.strftime("%F %T")
            fresh = [i for i in incidents if time.time() - S["seen"].get(i[0], 0) > 7200]
            if fresh and not agent and time.time() > S.get("claude_wait", 0): start_agent(*fresh[0])
            if agent: save("fixing", S["history"][0]["text"] if S["history"] else "fixing", agent[2])
            elif incidents: save("watching", f"{len(incidents)} problem(s) seen, already handled recently")
            else: save("ok", "all clear · line flowing" + (f" · posts booked until {S['queue_until']}" if S.get("queue_until") else ""))
        except Exception as e:
            try: log(f"check error: {e}")
            except OSError: pass
        for _ in range(EVERY // 5):   # wake early when the agent finishes
            time.sleep(5)
            if agent and agent[0].poll() is not None: break

if __name__ == "__main__":
    if sys.argv[1:] == ["dry"]:   # look only: print what it sees, fix nothing (testing)
        real_sh = sh
        sh = lambda cmd, timeout=120: real_sh(cmd, timeout) if not any(w in str(cmd) for w in ("remove", "reslot", "restart", "relay_tick", "prune")) else ""
        did = lambda t, target="": print("would do:", t)
        inc = []; posts(inc); thinking_problems(inc)
        print("disk free GB", round(shutil.disk_usage(ROOT).free / 1e9, 1), "| queue until", S.get("queue_until"), "| incidents:", inc)
    else: main()
