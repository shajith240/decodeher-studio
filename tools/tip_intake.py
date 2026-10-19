"""Growth tips the owner shares on Telegram (owner 10-18: "when I see a YouTube video or a reel about growing on Instagram, I share
it — research it, say what actually works, what is a myth or hype, and use the good tips to grow the page").
Called by tools/pin_intake.py for HQ inbox items of kind "tip": {"urls": [youtube / instagram links], "files": [telegram videos]}.
For each source:
  1. transcript: YouTube captions (yt-dlp, no login), else the audio through faster-whisper. Instagram links are fetched WITHOUT
     any login (never with @thedecodeher's session: scraping with our own account risks it); if Instagram blocks it, the owner
     is asked to send the video file instead. Telegram video files come through HQ /api/tgfile. Nothing is kept on the laptop.
  2. a Claude agent (Sonnet, web search allowed) checks every claim against Instagram's own statements and solid sources and
     against OUR numbers: works / exaggerated / outdated / myth / unproven, and what it means for @thedecodeher.
  3. the verdict goes to brain/growth/inbox/ (the daily growth session turns it into tactics, playbook and experiments) and a
     short plain-words reply goes to the owner on Telegram.
Usage (by hand): python3 tools/tip_intake.py <url> [...]       → prints the Telegram text, writes the inbox note"""
import glob, json, os, re, subprocess, sys, tempfile, time, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
INBOX = "brain/growth/inbox"
YT = re.compile(r"(youtube\.com|youtu\.be)", re.I); IG = re.compile(r"instagram\.com", re.I)

def secret(n):
    p = os.path.join(ROOT, ".secrets", n); return open(p).read().strip() if os.path.exists(p) else os.environ.get(n, "")

def vtt_text(path):   # caption file → plain text without timestamps or the repeated rolling lines YouTube auto-captions have
    out, last = [], ""
    for l in open(path, encoding="utf-8", errors="ignore"):
        l = re.sub(r"<[^>]+>", "", l).strip()
        if not l or "-->" in l or l.startswith(("WEBVTT", "Kind:", "Language:")) or l.isdigit() or l == last: continue
        out.append(l); last = l
    return re.sub(r"\s+", " ", " ".join(out)).strip()

def whisper(path):
    # 10-18: ffmpeg decodes to raw 16 kHz mono first — faster-whisper's own decoder (PyAV) broke on a version mismatch
    code = ("import sys, subprocess, numpy as np; from faster_whisper import WhisperModel; "
            "pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout; "
            "a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768; m = WhisperModel('small', device='cpu', compute_type='int8'); "
            "s, i = m.transcribe(a, vad_filter=True); print(i.language); print(' '.join(x.text.strip() for x in s))")
    r = subprocess.run(["uv", "run", "-q", "--with", "faster-whisper", "--with", "numpy", "python", "-c", code, path], capture_output=True, text=True, timeout=1800)
    lines = r.stdout.strip().split("\n", 1)
    return lines[1].strip() if len(lines) > 1 else ""

def from_url(url, tmp):
    """→ (meta, transcript, problem)"""
    ytdlp = ["uv", "run", "-q", "--with", "yt-dlp", "yt-dlp", "--no-playlist", "--no-warnings"]
    info = subprocess.run(ytdlp + ["-J", url], capture_output=True, text=True, timeout=180)
    try: j = json.loads(info.stdout)
    except Exception: j = {}
    meta = {"title": j.get("title") or "", "by": j.get("channel") or j.get("uploader") or "", "duration": j.get("duration") or 0,
            "description": (j.get("description") or "")[:1500], "views": j.get("view_count"), "date": j.get("upload_date") or ""}
    if not j:
        if IG.search(url): return meta, "", "Instagram didn't let me download that reel without logging in. Please send the video file itself to the bot and tap 💡 Growth tip."
        return meta, "", "I couldn't open that link."
    if (meta["duration"] or 0) > 3 * 3600: return meta, "", "That video is over 3 hours, too long to study."
    if YT.search(url):   # captions first: fast, no audio download
        subprocess.run(ytdlp + ["--skip-download", "--write-subs", "--write-auto-subs", "--sub-langs", "en.*,en", "--sub-format", "vtt",
                                "-o", f"{tmp}/sub.%(ext)s", url], capture_output=True, timeout=180)
        subs = sorted(glob.glob(f"{tmp}/sub*.vtt"), key=lambda p: ("orig" not in p, len(p)))
        if subs:
            t = vtt_text(subs[0])
            if len(t.split()) > 40: return meta, t, ""
    subprocess.run(ytdlp + ["-f", "bestaudio/best", "-x", "--audio-format", "m4a", "-o", f"{tmp}/a.%(ext)s", url], capture_output=True, timeout=900)
    a = glob.glob(f"{tmp}/a.*")
    if not a: return meta, "", ("Instagram didn't let me download that reel. Please send the video file to the bot and tap 💡 Growth tip."
                                if IG.search(url) else "I couldn't download that video.")
    return meta, whisper(a[0]), ""

def from_file(f, tmp):
    url, key = secret("HQ_URL").rstrip("/"), secret("HQ_KEY")
    req = urllib.request.Request(f"{url}/api/tgfile?file_id={f['file_id']}", headers={"Authorization": f"Bearer {key}", "User-Agent": "decodeher-tips/1.0"})
    p = f"{tmp}/v.mp4"; open(p, "wb").write(urllib.request.urlopen(req, timeout=180).read())
    return {"title": f.get("caption") or f.get("name") or "video sent on Telegram", "by": "", "duration": 0, "description": f.get("caption", "")}, whisper(p), ""

PROMPT = """You are the growth analyst of the Instagram page @thedecodeher (faceless English reels: dating psychology for men; goal 1,000
followers fast, then keep growing). The owner watched a video about Instagram growth and wants to know what in it is TRUE and USEFUL
for us. Work in /home/shajith/Projects/dark-psycology. Read first: brain/growth/playbook.md, brain/growth/performance.md (our real
numbers), the file names in brain/growth/tactics/, and CLAUDE.md "Current state" (the owner's fixed decisions win over any tip).
Never read .env, .relay.json or .secrets/. Do not edit any file.

Check each concrete claim in the transcript. Use web search to verify against Instagram/Meta's own statements first (Adam Mosseri,
@creators, about.instagram.com, help.instagram.com, Meta transparency "Our approach to explaining ranking"), then reputable research
(Later, Hootsuite, Buffer, Sprout Social, Metricool, Social Media Examiner, Dash Hudson). Be strict: creators often present opinion as
fact, sell courses, or repeat 2021-era advice. Verdicts: "works" (official or strong data), "partly" (true but exaggerated or
conditional), "outdated", "myth", "unproven" (no evidence either way). Then judge it for OUR page specifically.

SOURCE: {title} — {by} — {url}
DESCRIPTION: {description}
TRANSCRIPT ({words} words):
{transcript}

Answer with JSON only:
{{"slug": "3-6 words, hyphens", "topic": "one line", "hype": "low|medium|high (how much the video oversells)",
 "claims": [{{"claim": "short", "verdict": "works|partly|outdated|myth|unproven", "why": "one sentence with the evidence", "source": "url or ''"}}],
 "for_us": [{{"action": "what we change in OUR pipeline (script hook, title card, opening clip, length, caption, CTA, post time, cover, profile...)",
             "why": "short", "priority": "high|medium|low", "already_doing": true|false}}],
 "skip": ["tips that don't fit us or break the owner's rules, with a 4-word reason"],
 "one_line": "the single most useful takeaway, plain words"}}"""

def analyse(meta, url, transcript):
    words = transcript.split(); tx = " ".join(words[:12000])
    prompt = PROMPT.format(title=meta.get("title", ""), by=meta.get("by", ""), url=url, description=meta.get("description", "")[:1500],
                           words=len(words), transcript=tx)
    r = subprocess.run([os.environ.get("CLAUDE_BIN", "claude"), "-p", prompt, "--model", "sonnet", "--allowedTools", "Read,Glob,Grep,WebSearch,WebFetch",
                        "--output-format", "text"], capture_output=True, text=True, timeout=1500, cwd=ROOT)
    m = re.search(r"\{.*\}", r.stdout, re.S)
    if not m: return None, (r.stdout + r.stderr)[-300:]
    try: return json.loads(m.group(0)), ""
    except Exception as e: return None, f"bad JSON: {e}"

ICON = {"works": "✅", "partly": "⚠️", "outdated": "🕰", "myth": "❌", "unproven": "❓"}
def write_note(meta, url, a, transcript):
    os.makedirs(INBOX, exist_ok=True)
    slug = re.sub(r"[^a-z0-9-]+", "-", str(a.get("slug", "tip")).lower()).strip("-")[:50] or "tip"
    p = f"{INBOX}/{time.strftime('%F')}-owner-tip-{slug}.md"
    L = [f"# Owner-shared growth tip: {meta.get('title') or slug}", "",
         f"Source: {url or 'video file sent on Telegram'} · by {meta.get('by') or '?'} · shared {time.strftime('%F %H:%M')} · hype: {a.get('hype', '?')}",
         "Fact-checked by tools/tip_intake.py (Claude + web). The growth session decides what we adopt.", "",
         f"**Takeaway:** {a.get('one_line', '')}", "", "## Claims checked"]
    L += [f"- {ICON.get(c.get('verdict'), '•')} **{c.get('verdict', '?')}**: {c.get('claim', '')} — {c.get('why', '')}" + (f" ({c['source']})" if c.get("source") else "") for c in a.get("claims", [])]
    L += ["", "## For @thedecodeher"]
    L += [f"- [{x.get('priority', '?')}]{' (already doing)' if x.get('already_doing') else ''} {x.get('action', '')} — {x.get('why', '')}" for x in a.get("for_us", [])]
    if a.get("skip"): L += ["", "## Skipped"] + [f"- {s}" for s in a["skip"]]
    L += ["", "## Transcript (start)", " ".join(transcript.split()[:200]) + " …"]
    open(p, "w").write("\n".join(L) + "\n"); return p

def telegram_text(meta, a, note):
    esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    c = a.get("claims", []); cnt = {k: sum(1 for x in c if x.get("verdict") == k) for k in ICON}
    L = [f"💡 <b>{esc(meta.get('title') or 'Growth tip')[:90]}</b>", f"Hype level: {esc(a.get('hype', '?'))} · "
         + " ".join(f"{ICON[k]} {v}" for k, v in cnt.items() if v), "", f"<b>Takeaway:</b> {esc(a.get('one_line', ''))}"]
    real = [x for x in c if x.get("verdict") in ("works", "partly")][:4]; fake = [x for x in c if x.get("verdict") in ("myth", "outdated")][:3]
    if real: L += ["", "<b>What's real</b>"] + [f"{ICON[x['verdict']]} {esc(x.get('claim', ''))}" for x in real]
    if fake: L += ["", "<b>Hype / myths</b>"] + [f"{ICON[x['verdict']]} {esc(x.get('claim', ''))}: {esc(x.get('why', ''))[:120]}" for x in fake]
    acts = [x for x in a.get("for_us", []) if not x.get("already_doing")][:3]
    if acts: L += ["", "<b>What we'll try</b>"] + [f"• {esc(x.get('action', ''))}" for x in acts]
    elif a.get("for_us"): L += ["", "We already do the useful parts."]
    L += ["", "Saved to the growth brain; tomorrow's 05:30 growth session folds it into the playbook."]
    return "\n".join(L)

def handle(item, progress=lambda t: None):
    """item: {"urls": [...], "files": [...]} → list of (ok, telegram_text)"""
    out = []
    srcs = [("url", u) for u in item.get("urls", [])] + [("file", f) for f in item.get("files", [])]
    for i, (kind, src) in enumerate(srcs):
        label = f"{i + 1}/{len(srcs)}"
        with tempfile.TemporaryDirectory() as tmp:
            progress(f"⏳ {label} 🎧 getting the transcript…")
            try: meta, tx, problem = from_url(src, tmp) if kind == "url" else from_file(src, tmp)
            except Exception as e: meta, tx, problem = {}, "", f"couldn't get that video ({str(e)[:80]})"
        if problem or len(tx.split()) < 25:
            out.append((False, f"⚠️ {problem or 'That video has almost no speech, so there is nothing to fact-check.'}")); continue
        progress(f"⏳ {label} 🔎 fact-checking {len(tx.split())} words of advice (a few minutes)…")
        a, err = analyse(meta, src if kind == "url" else "", tx)
        if not a: out.append((False, f"⚠️ The fact-check didn't finish ({err[:120]}). I'll keep the link; send it again later.")); continue
        note = write_note(meta, src if kind == "url" else "", a, tx)
        out.append((True, telegram_text(meta, a, note)))
    return out

if __name__ == "__main__":
    for ok, t in handle({"urls": sys.argv[1:]}, progress=print): print(t, "\n")
