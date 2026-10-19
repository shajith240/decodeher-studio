"""VIRAL BANK, YouTube Shorts half (owner rule 10-19, "steal like an artist": every reel remixes a short that already went viral
in our niche). Finds niche Shorts with >= 1M views and appends them to brain/research/viral-bank/yt-tiktok.jsonl.

Sources: brain/research/viral-bank/sources-yt.txt, one per line:
  search: <query>          a YouTube Shorts search (each run takes a rotating slice of these, all-time + uploaded this
                           year, so NEW viral shorts turn up; --all-searches = every line, all time)
  https://www.youtube.com/@handle  or  .../channel/UC...   a channel; its /shorts tab is read (newest first, every run)
Every niche short ever seen is remembered in .yt-candidates.json (YouTube's results change run to run), so a short found
once can still be added later; --cache-only picks from that memory without searching.
  skip: <id> <id> ...      video ids never to add (off-niche hits the title filter let through)
  # comment
Incremental: URLs already in the bank are skipped; only new videos with >= 1M views are added (biggest first, --max-new).
Each new entry gets "added" (today) and "used_by": null (set it to the reel id when a reel remixes it, so ideas aren't reused).
The analysis fields (hook/concept/structure/visual/why_it_worked/fits_us) are left null for a Claude pass to fill in, except
"hook" which is taken from the transcript's first sentence when --transcribe is on.

Anonymous only: no login, no cookies. Polite pacing (--sleep between requests). If YouTube starts refusing (429 / sign-in /
bot check), the run stops cleanly and keeps what it already found.
TikTok: yt-dlp cannot read TikTok user/tag/search pages anonymously (checked 10-19: "Unable to extract secondary user ID",
tag extractor broken), so it is not collected here.

Usage:
  python3 tools/viral_bank_yt.py                       # new entries, metadata only
  python3 tools/viral_bank_yt.py --max-new 40 --transcribe   # + download 360p to library/research/viral/yt/<id>.mp4,
                                                       #   faster-whisper transcript, 3-frame strip <id>.jpg
  python3 tools/viral_bank_yt.py --fill                # transcribe rows that were added without --transcribe
  python3 tools/viral_bank_yt.py --add <id|url> ... --transcribe   # add specific shorts (any view count)
  python3 tools/viral_bank_yt.py --mark <id>=<reel> ...  # record which reel remixed a short (used_by)
  options: --searches N (search lines per run, default 8) --pages N (result pages per search, default 3) --min-views N
           --channel-depth N --list (print candidates only) --all-searches
"""
import argparse, datetime, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
BANK = "brain/research/viral-bank/yt-tiktok.jsonl"
SOURCES = "brain/research/viral-bank/sources-yt.txt"
STATE = "brain/research/viral-bank/.yt-rotation.json"
CACHE = "brain/research/viral-bank/.yt-candidates.json"   # every niche short seen so far (search results vary run to run)
MEDIA = "library/research/viral/yt"
YTDLP = "/usr/bin/yt-dlp"
BLOCKED = re.compile(r"HTTP Error 429|Sign in to confirm|not a bot|captcha", re.I)
# niche filter on titles: dating/women/texting/attraction words in, music/film/kids noise out
NICHE = re.compile(r"\b(she|her|girl|girls|woman|women|female|crush|text|texting|dating|date|attract\w*|flirt\w*|likes? you|"
                   r"ignore\w*|ex|relationship|red flags?|mixed signals|chase|miss you|psycholog\w*|interest|ghost\w*|"
                   r"girlfriend|wife|love|signs?|body language|eye contact|rejection|approach)\b", re.I)
NOISE = re.compile(r"lyrics|official (music )?video|sped up|remix|trailer|song|cover|gacha|minecraft|roblox|fortnite|"
                   r"animatic|kdrama|horror|prank|subliminal|\bfmv\b|visualizer", re.I)

SKIP = set()   # "skip: <id> <id> ..." lines in the sources file: off-niche shorts that should never be proposed again

class Blocked(Exception): pass

def run(args, timeout=300):
    r = subprocess.run([YTDLP, "--no-warnings", "--ignore-config", *args], capture_output=True, text=True, timeout=timeout)
    if BLOCKED.search(r.stderr or ""): raise Blocked(r.stderr.strip().splitlines()[-1])
    return r

def flat(url, n):
    r = run(["--flat-playlist", "-J", "--playlist-end", str(n), url])
    try: return [e for e in (json.loads(r.stdout).get("entries") or []) if e]
    except Exception: return []

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
SP_ALL, SP_YEAR = "EgIQCQ%3D%3D", "EgQIBRAJ"   # search filter: type=Shorts (all time) / type=Shorts + uploaded this year

def _walk(o, k):
    if isinstance(o, dict):
        if k in o: yield o[k]
        for v in o.values(): yield from _walk(v, k)
    elif isinstance(o, list):
        for v in o: yield from _walk(v, k)

def _views(t):   # "4.6 million views" / "820 thousand views" / "1,234 views" → int
    m = re.search(r"([\d.,]+)\s*(billion|million|thousand|[KMB])?\s*views", t or "", re.I)
    if not m: return 0
    n = float(m.group(1).replace(",", "")); u = (m.group(2) or "").lower()[:1]
    return int(n * {"b": 1e9, "m": 1e6, "t": 1e3, "k": 1e3}.get(u, 1))

def _lockups(d):
    out = []
    for s in _walk(d, "shortsLockupViewModel"):
        vid = (s.get("entityId") or "").replace("shorts-shelf-item-", "")
        acc = s.get("accessibilityText") or ""
        title = re.sub(r",\s*[\d.,]+\s*(billion|million|thousand)?\s*views.*$", "", acc)
        if re.fullmatch(r"[\w-]{11}", vid): out.append({"id": vid, "title": title, "view_count": _views(acc), "duration": None})
    return out

def shorts_search(q, sp, pages=3):
    """YouTube's own Shorts search results (yt-dlp's ytsearch skips the Shorts shelf). Public page, no login, no cookies."""
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote_plus(q)}&sp={sp}"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"})
    try: h = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        if e.code == 429: raise Blocked("HTTP 429 on search")
        return []
    if "consent.youtube.com" in h[:5000] or "/sorry/" in h[:5000]: raise Blocked("consent/bot page on search")
    m = re.search(r"var ytInitialData = (\{.*?\});</script>", h, re.S)
    if not m: return []
    d = json.loads(m.group(1)); out = _lockups(d)
    ver = (re.search(r'"INNERTUBE_CONTEXT_CLIENT_VERSION":"([^"]+)"', h) or [None, "2.20261016.01.00"])[1]
    for _ in range(pages - 1):
        tok = next((c["token"] for c in _walk(d, "continuationCommand") if c.get("request") == "CONTINUATION_REQUEST_TYPE_SEARCH"), None)
        if not tok: break
        time.sleep(1.5)
        body = json.dumps({"context": {"client": {"clientName": "WEB", "clientVersion": ver, "hl": "en", "gl": "US"}}, "continuation": tok}).encode()
        req = urllib.request.Request("https://www.youtube.com/youtubei/v1/search?prettyPrint=false", data=body,
                                     headers={"User-Agent": UA, "Content-Type": "application/json"})
        try: d = json.loads(urllib.request.urlopen(req, timeout=60).read())
        except urllib.error.HTTPError as e:
            if e.code == 429: raise Blocked("HTTP 429 on search continuation")
            break
        except Exception: break
        out += _lockups(d)
    return out

def bank_urls():
    if not os.path.exists(BANK): return set()
    out = set()
    for l in open(BANK, encoding="utf-8"):
        try: out.add(vid_of(json.loads(l).get("url", "")))
        except Exception: pass
    return out

def vid_of(url):
    m = re.search(r"(?:v=|shorts/|youtu\.be/)([\w-]{11})", url or ""); return m.group(1) if m else url

def sources():
    s, c = [], []
    global SKIP
    for l in open(SOURCES, encoding="utf-8"):
        l = l.strip()
        if not l or l.startswith("#"): continue
        if l.lower().startswith("search:"): s.append(l.split(":", 1)[1].strip())
        elif l.lower().startswith("skip:"): SKIP.update(l.split(":", 1)[1].split())
        else: c.append(l.split()[0].rstrip("/"))   # a channel URL, optionally followed by "  # name"
    return s, c

def whisper(path):   # same approach as tools/tip_intake.py: ffmpeg → 16 kHz mono PCM, then faster-whisper small int8
    code = ("import sys, subprocess, numpy as np; from faster_whisper import WhisperModel; "
            "pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout; "
            "a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768; m = WhisperModel('small', device='cpu', compute_type='int8'); "
            "s, i = m.transcribe(a, vad_filter=True); print(i.language); print(' '.join(x.text.strip() for x in s))")
    r = subprocess.run(["uv", "run", "-q", "--with", "faster-whisper", "--with", "numpy", "python", "-c", code, path],
                       capture_output=True, text=True, timeout=1800)
    lines = r.stdout.strip().split("\n", 1)
    return (lines[0].strip() if lines else ""), (lines[1].strip() if len(lines) > 1 else "")

def translate(path):   # non-English shorts: whisper "medium" translating straight to English (small garbles Hindi)
    code = ("import sys, subprocess, numpy as np; from faster_whisper import WhisperModel; "
            "pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', sys.argv[1], '-ac', '1', '-ar', '16000', '-f', 's16le', '-'], capture_output=True).stdout; "
            "a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768; m = WhisperModel('medium', device='cpu', compute_type='int8'); "
            "s, i = m.transcribe(a, vad_filter=True, task='translate'); print(' '.join(x.text.strip() for x in s))")
    r = subprocess.run(["uv", "run", "-q", "--with", "faster-whisper", "--with", "numpy", "python", "-c", code, path],
                       capture_output=True, text=True, timeout=3600)
    return r.stdout.strip()

def ocr(mp4):   # on-screen text (text-only "fact" shorts, chat screenshots): 2 frames/s, tesseract on white-text and plain passes
    import tempfile, glob as _g
    keep, seen = [], []
    with tempfile.TemporaryDirectory() as d:
        for i, vf in enumerate(["fps=2,scale=900:-2,format=gray,lutyuv=y='if(gt(val\\,185)\\,0\\,255)'", "fps=1,scale=900:-2,format=gray"]):
            subprocess.run(["ffmpeg", "-v", "error", "-i", mp4, "-vf", vf, f"{d}/{i}_%04d.png"], capture_output=True, timeout=300)
        for f in sorted(_g.glob(f"{d}/*.png"), key=lambda x: (x.split("_")[-1], x)):
            t = subprocess.run(["tesseract", f, "-", "--psm", "6"], capture_output=True, text=True).stdout
            for line in t.splitlines():
                line = re.sub(r"^[^A-Za-z0-9#\"']+|[^A-Za-z0-9.!?…'\")]+$", "", line.strip())
                words = re.findall(r"[A-Za-z]{3,}", line)
                if len(words) < 2 or sum(len(w) for w in words) < 0.6 * len(line.replace(" ", "")): continue
                k = re.sub(r"[^a-z]", "", line.lower())
                if any(k in s_ or s_ in k for s_ in seen):
                    j = next(n for n, s_ in enumerate(seen) if k in s_ or s_ in k)
                    if len(k) > len(seen[j]): seen[j], keep[j] = k, line   # keep the most complete reading
                    continue
                seen.append(k); keep.append(line)
    return " / ".join(keep)

def frames(mp4, out, dur):   # 3 frames (20 / 50 / 80 %) side by side → one strip image for the visual note
    ts = [max(0.5, dur * p) for p in (0.2, 0.5, 0.8)]
    ins = sum([["-ss", f"{t:.2f}", "-i", mp4] for t in ts], [])
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex",
                    "[0:v]scale=-2:480,setsar=1[a];[1:v]scale=-2:480,setsar=1[b];[2:v]scale=-2:480,setsar=1[c];[a][b][c]hstack=3",
                    "-frames:v", "1", out], capture_output=True, timeout=120)

def first_sentence(t):
    m = re.match(r"(.+?[.?!])(\s|$)", t or ""); return (m.group(1) if m else (t or "")[:160]).strip()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-new", type=int, default=30); ap.add_argument("--transcribe", action="store_true")
    ap.add_argument("--searches", type=int, default=8); ap.add_argument("--pages", type=int, default=3, help="result pages per search")
    ap.add_argument("--channel-depth", type=int, default=150); ap.add_argument("--min-views", type=int, default=1_000_000)
    ap.add_argument("--cache-only", action="store_true", help="don't search; pick from shorts already seen in earlier runs")
    ap.add_argument("--list", action="store_true", help="only print the new candidates, write nothing")
    ap.add_argument("--sleep", type=float, default=2.0); ap.add_argument("--all-searches", action="store_true",
                    help="use every search line over all time instead of a rotating this-month slice")
    ap.add_argument("--fill", action="store_true", help="transcribe bank rows that have no transcript yet, then exit")
    ap.add_argument("--add", nargs="+", metavar="ID", help="add these shorts (id or URL) whatever their views, then exit")
    ap.add_argument("--mark", nargs="+", metavar="ID=REEL", help="set used_by on bank rows (e.g. vStlPMAxG1U=v4), then exit")
    a = ap.parse_args()
    if a.mark: return mark(dict(x.split("=", 1) for x in a.mark))
    if a.add:
        cand = {vid_of(x): {"id": vid_of(x), "_src": "manual"} for x in a.add}; a.min_views = 0
        return add_rows([e for k, e in cand.items() if k not in bank_urls()], a)
    if a.fill: return fill(a.sleep)
    os.makedirs(os.path.dirname(BANK), exist_ok=True); os.makedirs(MEDIA, exist_ok=True)
    have = bank_urls(); queries, channels = sources()
    st = json.load(open(STATE)) if os.path.exists(STATE) else {"next": 0}
    if a.all_searches: pick, sps = queries, [SP_ALL]
    else:   # rotating slice of the searches, each run both all-time and uploaded-this-year, so NEW viral shorts surface
        i = st["next"] % max(1, len(queries)); pick = (queries + queries)[i:i + min(a.searches, len(queries))]
        st["next"] = i + len(pick); sps = [SP_ALL, SP_YEAR]
    cand, blocked = {}, None
    if a.cache_only: pick, channels = [], []
    try:
        for q in pick:
            for sp in sps:
                for e in shorts_search(q, sp, pages=a.pages):
                    if NICHE.search(e.get("title") or "") and not NOISE.search(e.get("title") or ""): e["_src"] = "search: " + q; cand.setdefault(e["id"], e)
                time.sleep(a.sleep)
        for c in channels:
            for e in flat(c + "/shorts", a.channel_depth):
                if NICHE.search(e.get("title") or "") and not NOISE.search(e.get("title") or ""): e["_src"] = c; cand.setdefault(e["id"], e)
            time.sleep(a.sleep)
    except Blocked as b: blocked = str(b)
    if not a.list: json.dump(st, open(STATE, "w"))
    seen = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    for k, e in cand.items():   # keep the freshest view count, remember everything ever seen
        seen[k] = {"id": k, "title": e.get("title"), "view_count": e.get("view_count"), "channel": e.get("channel"),
                   "duration": e.get("duration"), "_src": e.get("_src")}
    json.dump(seen, open(CACHE, "w"), ensure_ascii=False)
    new = sorted([e for e in seen.values() if (e.get("view_count") or 0) >= a.min_views and e["id"] not in have and e["id"] not in SKIP],
                 key=lambda e: -(e.get("view_count") or 0))[:a.max_new]
    print(f"scanned {len(cand)} niche shorts this run ({len(seen)} known), {len(new)} new at >= {a.min_views:,} views" + (f" (stopped early: {blocked})" if blocked else ""))
    if a.list:
        for e in new: print(f"  {e.get('view_count'):>12,}  {e['id']}  {(e.get('channel') or '')[:24]:24}  {(e.get('title') or '')[:80]}")
        return
    add_rows(new, a)

def add_rows(new, a):
    added = 0
    for e in new:
        url = f"https://www.youtube.com/shorts/{e['id']}"
        try:
            r = run(["-J", "--no-playlist", url], timeout=180)
            j = json.loads(r.stdout) if r.stdout.strip() else {}
        except Blocked as b: print("blocked, stopping:", b); break
        except Exception: j = {}
        row = {"platform": "youtube_shorts", "id": e["id"], "channel": j.get("channel") or e.get("channel") or "", "url": url,
               "title": j.get("title") or e.get("title") or "", "source": e.get("_src"),
               "date": j.get("upload_date") or "", "views": j.get("view_count") or e.get("view_count"),
               "likes": j.get("like_count"), "duration_s": j.get("duration") or e.get("duration"),
               "hook": None, "transcript": None, "language": None, "transcript_en": None, "onscreen_text": None,
               "concept": None, "structure": None, "visual": None, "why_it_worked": None, "fits_us": None,   # fits_us: {"ok", "reason"}
               "our_version": None, "added": datetime.date.today().isoformat(), "used_by": None}
        if a.transcribe:
            try: media(row)
            except Blocked as b: print("blocked, stopping:", b); break
        with open(BANK, "a", encoding="utf-8") as f: f.write(json.dumps(row, ensure_ascii=False) + "\n")
        added += 1; print(f"  + {(row['views'] or 0):>12,}  {row['channel'][:24]:24}  {row['title'][:70]}"); time.sleep(a.sleep)
    print(f"added {added} to {BANK}")

def media(row):   # 360p download → whisper transcript + first-sentence hook + 3-frame strip
    mp4 = f"{MEDIA}/{row['id']}.mp4"
    if not os.path.exists(mp4):   # Shorts have no muxed 360p stream any more: merge 360-480p video + m4a audio
        run(["-f", "bv*[height>=360][height<=480][vcodec^=avc1]+ba[ext=m4a]/bv*[height>=360][height<=480]+ba/b[height>=360]/worst",
             "--merge-output-format", "mp4", "--no-playlist", "-o", mp4, row["url"]], timeout=600)
    if os.path.exists(mp4):
        row["language"], row["transcript"] = whisper(mp4); row["hook"] = row.get("hook") or first_sentence(row["transcript"])
        enrich(row, mp4)
        frames(mp4, f"{MEDIA}/{row['id']}.jpg", float(row["duration_s"] or 30))

def enrich(row, mp4):   # English translation for non-English talk; on-screen text when the audio says little (music/text shorts)
    if row.get("language") not in (None, "", "en") and len((row.get("transcript") or "").split()) >= 12 and not row.get("transcript_en"):
        row["transcript_en"] = translate(mp4)
    if len((row.get("transcript") or "").split()) < 40 and not row.get("onscreen_text"):
        row["onscreen_text"] = ocr(mp4)

def rewrite(rows):
    with open(BANK + ".tmp", "w", encoding="utf-8") as f: f.write("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in rows))
    os.replace(BANK + ".tmp", BANK)

def mark(m):   # used_by = the reel that remixed this short, so the idea isn't reused
    rows = [json.loads(l) for l in open(BANK, encoding="utf-8") if l.strip()]
    for r in rows:
        if r["id"] in m: r["used_by"] = m.pop(r["id"])
    rewrite(rows); print("marked" + (f"; not in bank: {', '.join(m)}" if m else ""))

def fill(sleep):   # --fill: add transcripts/frames to bank rows that were added without --transcribe, and translation /
    rows = [json.loads(l) for l in open(BANK, encoding="utf-8") if l.strip()]   # on-screen text to rows that lack them
    todo = [r for r in rows if r.get("platform") == "youtube_shorts" and (r.get("transcript") is None or "onscreen_text" not in r
            and len((r.get("transcript") or "").split()) < 40 or r.get("language") not in (None, "", "en") and "transcript_en" not in r)]
    print(f"filling {len(todo)} rows")
    try:
        for r in todo:
            mp4 = f"{MEDIA}/{r['id']}.mp4"
            if r.get("transcript") is None or not os.path.exists(mp4): media(r)
            else: enrich(r, mp4)
            print(f"  ~ {r['id']}  {r['title'][:70]}")
            rewrite(rows); time.sleep(sleep)
    except Blocked as b: print("blocked, stopping:", b)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: sys.exit(130)
