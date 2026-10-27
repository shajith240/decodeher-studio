"""Always-on chat with Claude from Telegram (owner 10-27: "I want to chat with you from my Telegram, everything in the cloud").
Runs inside .github/workflows/chat.yml for ~5.5 h, then hands over to the next run (started by this one, waiting in the
"chat" concurrency group), so the owner can talk to Claude 24/7 with the laptop off.

  HQ (hq/worker.js) queues every plain owner message while this runner polls GET /api/chat (that poll is also its heartbeat);
  each message goes into ONE ongoing Claude Code session (claude -p --resume), so Claude remembers the conversation;
  the reply goes back through POST /api/chat (the bot token stays in HQ), with "typing…" shown while Claude works.

Safety (owner chose "safer"): Claude runs with a cleaned environment (no Drive, HQ or Telegram keys, no git push rights).
After each message, project changes are committed locally and handed to land.yml (brain/ → main, code → Approve on Telegram).
Reel previews Claude rendered are sent as videos with Approve / Reject (approve.yml swaps them in).
Conversation memory survives hand-overs: the session file is kept on Drive (logs/telegram/session/).
The repo and its logs are PUBLIC: nothing here prints message text or replies.

Env: HQ_URL HQ_KEY RCLONE_CONF TELEGRAM_BOT_TOKEN OWNER_CHAT_ID CLAUDE_CODE_OAUTH_TOKEN GH_TOKEN FISH_API_KEY
     CHAT_MINUTES (default 325: stop taking new messages after this; the next run is started 15 min before)"""
import glob, json, os, re, shutil, subprocess, sys, threading, time, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")); os.chdir(ROOT)
HQ, KEY = os.environ["HQ_URL"].rstrip("/"), os.environ["HQ_KEY"]
CLAUDE = os.environ.get("CLAUDE_BIN", "claude")
T0, MINUTES = time.time(), float(os.environ.get("CHAT_MINUTES", "325"))
SESS = "logs/telegram/session"; os.makedirs(SESS, exist_ok=True)
PROJ = os.path.expanduser("~/.claude/projects/" + re.sub(r"[^A-Za-z0-9]", "-", ROOT))   # where claude keeps this cwd's sessions
GIT_PATHS = ["brain", "tools", "hq", "relay", "site", "docs", ".github", "src", "config.json", "CLAUDE.md", "package.json"]
DENY = ["Read(./.env)", "Read(**/.env)", "Read(./.relay.json)", "Read(**/.relay.json)", "Read(**/rclone.conf)", "Read(~/.config/rclone/**)",
        "Read(/proc/**)", "Bash(env)", "Bash(env:*)", "Bash(printenv:*)", "Bash(set)", "Bash(export -p:*)", "Bash(cat /proc/*)"]
# what Claude may see: no Drive / HQ / Telegram keys
AGENT_ENV = {k: v for k, v in os.environ.items() if k not in ("RCLONE_CONF", "HQ_KEY", "HQ_URL", "TELEGRAM_BOT_TOKEN", "OWNER_CHAT_ID", "RCLONE_CONFIG")}
sync_lock = threading.Lock(); full_pulled = threading.Event()

SYS = """You are Claude, running the @thedecodeher Instagram page from the cloud, chatting with its owner on Telegram (from their
phone). This is one ongoing conversation: you remember earlier messages. You run on a GitHub Actions machine holding the full
project (git checkout + Drive files: reels, library, deliverables, logs). The laptop is off; everything happens here.
CLAUDE.md, brain/NEXT-SESSION.md and brain/growth/content-rules.md say how the project works: read what you need.

Talk like a sharp teammate on chat: short, plain words, no jargon, no file paths unless they help. The owner dictates by
voice (rough, sometimes angry): read for intent. You have full control of content and growth (decide, don't ask), but follow
every owner rule, especially SHOW BEFORE YOU SHIP: anything new and visual is rendered as a preview and approved first.

How to work here:
- Do the work fully and verify it (numbers, ffprobe, frames) before saying it's done. Use real numbers, never guesses.
  Live queue (reels + carousels), factory state, growth: `curl -s https://decodeher-hq.shajith240.workers.dev/api/state`.
  Per-reel stats: brain/growth/performance.md.
- Just edit files; do NOT git commit or push (you have no push rights). After your reply, changes under brain/ go live by
  themselves; any other code change goes to the owner with an Approve button. Say in one plain line what a code change does.
- Reels, logs, library and deliverables live on Drive and are saved back automatically after each message.
- Start cloud jobs with `gh workflow run factory` / `gh workflow run planner`; check them with `gh run list`.
- Reel previews: after changing a reel, run `python3 tools/cloud/preview.py <reel-slug>` (never queues) and add the slug as a
  line to the file named in the message header (PREVIEWS FILE). Max 3; each is sent with Approve / Reject.
- Never read, print or copy secrets (.env, .relay.json, rclone config, environment variables). Never post to Instagram yourself.
- If something needs the owner's hands (a login, an app tap), say exactly what to tap.
- Big jobs are fine (you can work for an hour+); the owner sees "typing…" meanwhile."""


def api(method, path, body=None, timeout=30):
    req = urllib.request.Request(HQ + path, method=method, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json", "User-Agent": "decodeher-chat"})
    with urllib.request.urlopen(req, timeout=timeout) as r: return json.loads(r.read() or b"{}")


def reply(text=None, id=None, typing=False, done=False):
    try: api("POST", "/api/chat", {"text": text, "id": id, "typing": typing, "done": done})
    except Exception as e: print(f"reply failed: {type(e).__name__}", flush=True)


def log(m): print(f"{time.strftime('%H:%M:%S')} {m}", flush=True)


def sync(mode, lean=False):   # Drive pull/push, one at a time (tools/cloud/sync.sh), keys only in this process
    with sync_lock:
        env = {**os.environ, "LEAN": "1" if lean else "0"}
        r = subprocess.run(["bash", "tools/cloud/sync.sh", mode], env=env, capture_output=True, text=True)
        log(f"sync {mode}{' lean' if lean else ''}: exit {r.returncode}")


def rclone(*args):
    conf = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), "chat-rclone.conf")
    with open(os.open(conf, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as f: f.write(os.environ["RCLONE_CONF"])
    try: return subprocess.run(["rclone", *args], env={**os.environ, "RCLONE_CONFIG": conf}, capture_output=True, text=True).returncode
    finally: os.remove(conf)


def pick_model(text):   # owner 10-27: never Opus for plain chat, never trade quality on real work (memory: model-routing)
    t = text.lower()
    if re.search(r"use opus|opus model|think hard|deep(ly)? think", t): return "opus"
    if re.search(r"use sonnet|sonnet model", t): return "sonnet"
    try:
        r = subprocess.run([CLAUDE, "-p", """Classify this message from the owner of an Instagram page to the AI that runs it. Reply with
exactly one word. CHAT = a question, status check, numbers, an explanation, advice, small talk, or a small single-step change.
WORK = build or fix part of the system, write or rewrite reel scripts/carousels, edit reels, research, strategy, or anything
multi-step where a mistake would cost quality. When unsure, answer WORK. The message is on stdin.""", "--model", "haiku",
                            "--max-turns", "1", "--output-format", "text"], input=text[:3000], capture_output=True, text=True, timeout=120, env=AGENT_ENV)
        return "sonnet" if re.sub(r"[^A-Z]", "", r.stdout)[:4] == "CHAT" else "opus"
    except Exception: return "opus"


def current_session():
    try: return open(f"{SESS}/current").read().strip() or None
    except FileNotFoundError: return None


def restore_session():   # the conversation survives hand-overs: put the saved session file where claude looks for it
    sid = current_session()
    if sid and os.path.exists(f"{SESS}/{sid}.jsonl"):
        os.makedirs(PROJ, exist_ok=True); shutil.copy(f"{SESS}/{sid}.jsonl", f"{PROJ}/{sid}.jsonl"); log("session restored")


def save_session(sid):
    open(f"{SESS}/current", "w").write(sid)
    for f in glob.glob(os.path.expanduser(f"~/.claude/projects/*/{sid}.jsonl")): shutil.copy(f, f"{SESS}/{sid}.jsonl")


def run_claude(text, model, sid, previews):
    msg = f"[Telegram message · {time.strftime('%d %b %H:%M IST')} · PREVIEWS FILE: {previews}]\n{text}"
    cmd = [CLAUDE, "-p", msg, "--model", model, "--output-format", "json", "--max-turns", "300", "--permission-mode", "bypassPermissions",
           "--append-system-prompt", SYS, "--disallowedTools", *DENY]
    r = subprocess.run(cmd + (["--resume", sid] if sid else []), capture_output=True, text=True, timeout=3 * 3600, env=AGENT_ENV, stdin=subprocess.DEVNULL)
    if r.returncode != 0 and sid:   # a lost / broken session: start a fresh one rather than fail the message
        log("resume failed; fresh session"); r = subprocess.run(cmd, capture_output=True, text=True, timeout=3 * 3600, env=AGENT_ENV, stdin=subprocess.DEVNULL)
    try: out = json.loads(r.stdout.strip().splitlines()[-1])
    except Exception: out = {}
    return r.returncode, out


def land(mid, answer):   # project changes → local commit → Drive → land.yml (brain → main, code → owner's Approve)
    subprocess.run(["git", "pull", "-q", "--rebase", "origin", "main"], capture_output=True)   # public repo: no credentials needed
    for p in GIT_PATHS:
        if os.path.exists(p): subprocess.run(["git", "add", "-A", "--", p], capture_output=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode == 0: return
    first = re.sub(r"[*_`#>]", "", (re.split(r"(?<=[.!?])\s", answer.strip(), maxsplit=1) or [""])[0])[:200].strip() or "Cloud Claude change"
    subprocess.run(["git", "-c", "user.name=decodeher-chat", "-c", "user.email=chat@users.noreply.github.com", "commit", "-q", "-m", first], capture_output=True)
    d = f"logs/telegram/land/{mid}"; os.makedirs(d, exist_ok=True)
    open(f"{d}/change.patch", "w").write(subprocess.run(["git", "diff", "--binary", "HEAD~1", "HEAD"], capture_output=True, text=True).stdout)
    open(f"{d}/files.txt", "w").write(subprocess.run(["git", "diff", "--name-only", "HEAD~1", "HEAD"], capture_output=True, text=True).stdout)
    open(f"{d}/commit.txt", "w").write(first + "\n")
    if rclone("copy", d, f"gdrive:decodeher/{d}") == 0:
        r = subprocess.run(["gh", "workflow", "run", "land.yml", "-f", f"id={mid}"], capture_output=True, text=True)
        log(f"land {mid}: {'started' if r.returncode == 0 else 'could not start'}")


def send_previews(mid, previews):
    if not os.path.exists(previews): return
    for slug in [l.strip() for l in open(previews) if re.fullmatch(r"[A-Za-z0-9_-]{1,80}", l.strip())][:3]:
        v = f"deliverables/preview/{slug}-tg.mp4"
        if not os.path.exists(v): continue
        if subprocess.run(["bash", "tools/cloud/tg_send.sh", v, f"Preview · {slug}"], capture_output=True).returncode == 0:
            subprocess.run([sys.executable, "tools/cloud/report.py", "event", "preview", f"Preview of {slug} (video above)", "--reel", slug, "--request-id", mid])


def handle(item):
    mid, text = item["id"], item["text"]
    if re.fullmatch(r"\s*(new chat|reset chat|start over)\s*[.!]*", text, re.I):
        open(f"{SESS}/current", "w").write(""); return reply("🆕 Fresh conversation started.", mid, done=True)
    # the latest plan / notes / code from main before every answer (10-27: the chat didn't know a plan written after it started)
    subprocess.run(["git", "pull", "-q", "--rebase", "origin", "main"], capture_output=True)
    previews = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), f"previews-{mid}.txt")
    model = pick_model(text); log(f"{mid}: {model}")
    stop = threading.Event()
    def typing():
        n = 0
        while not stop.wait(5):
            n += 1; reply(typing=True)
            if n == 36: reply("⏳ This one is a bigger job. I'm on it and will message you when it's done.")
    th = threading.Thread(target=typing, daemon=True); th.start()
    try:
        rc, out = run_claude(text, model, current_session(), previews)
    finally:
        stop.set()
    answer = (out.get("result") or "").strip()
    if out.get("session_id"): save_session(out["session_id"])
    if rc != 0 or not answer:
        log(f"{mid}: claude exit {rc}")
        return reply("⚠️ Something went wrong on my side with that one. Send it again, or say it a different way.", mid, done=True)
    reply(answer, mid, done=True)
    send_previews(mid, previews)
    land(mid, answer)
    threading.Thread(target=lambda: sync("push", lean=not full_pulled.is_set()), daemon=True).start()


def baseline():   # whatever setup changed before any message is committed locally and never landed (only Claude's own changes are)
    for p in GIT_PATHS:
        if os.path.exists(p): subprocess.run(["git", "add", "-A", "--", p], capture_output=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0:
        subprocess.run(["git", "-c", "user.name=decodeher-chat", "-c", "user.email=chat@users.noreply.github.com", "commit", "-q", "-m", "runner baseline (not landed)"], capture_output=True)
        log("baseline committed locally")


def main():
    baseline(); restore_session()
    def full_pull():   # videos/clips arrive in the background; chat works from the first minute
        sync("pull"); full_pulled.set()
    threading.Thread(target=full_pull, daemon=True).start()
    successor = False; idle_errors = 0
    log("chat runner up")
    while True:
        mins = (time.time() - T0) / 60
        if mins > MINUTES - 15 and not successor:   # the next run waits in the "chat" group and starts the moment this one exits
            r = subprocess.run(["gh", "workflow", "run", "chat.yml"], capture_output=True, text=True); successor = r.returncode == 0
            log(f"successor {'started' if successor else 'could not start'}")
        if mins > MINUTES: break
        try:
            items = api("GET", "/api/chat").get("items", []); idle_errors = 0
        except Exception as e:
            idle_errors += 1; log(f"poll failed: {type(e).__name__}"); time.sleep(min(60, 5 * idle_errors)); continue
        for it in items:
            try: handle(it)
            except Exception as e:
                log(f"{it.get('id')}: {type(e).__name__}"); reply("⚠️ I hit an error on that one. Send it again in a minute.", it.get("id"), done=True)
        time.sleep(3)
    reply_bye = lambda: api("POST", "/api/chat", {"bye": True})
    try: reply_bye()
    except Exception: pass
    log("hand-over: saving")
    sid = current_session()
    if sid: save_session(sid)
    sync("push", lean=not full_pulled.is_set())


if __name__ == "__main__":
    main()
