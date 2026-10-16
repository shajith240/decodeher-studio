"""Growth brain, part 2: READ the expert sources (no Claude). Usage: python3 tools/growth_fetch.py [max_items=4]
Sources = the ```json block in brain/growth/expert-sources.md ([{name, type, url, rss, channel_id, topics, trust}]).
For each feed (RSS/Atom) it finds items newer than the last run (state: brain/growth/data/fetch-state.json), newest and
high-trust first, and saves up to max_items as text in brain/growth/inbox/<date>-<source>-<id>.txt:
  YouTube -> English captions (yt-dlp, auto or manual), cleaned to plain text; blogs -> article text (tags stripped).
Each file starts with a header (source, title, url, published). Long texts are cut at 30k characters.
Gentle: one request at a time with pauses; YouTube 429s just skip that item until tomorrow."""
import datetime, glob, hashlib, html, json, os, re, subprocess, sys, tempfile, time, urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
G = "brain/growth"; INBOX = f"{G}/inbox"; STATE = f"{G}/data/fetch-state.json"; os.makedirs(INBOX, exist_ok=True); os.makedirs(f"{G}/data", exist_ok=True)
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 4
RELEVANT = re.compile(r"\b(reels?|short[- ]?form|shorts|tiktok|instagram|hooks?|retention|watch time|views?|viral|algorithm|followers?|grow(th|ing)?|engagement|"
                      r"storytell\w*|scripts?|content strateg\w*|creators?|audience|shares?|saves?|captions?|thumbnails?|analytics|benchmarks?|best time|attention|"
                      r"dating|relationships?|psycholog\w*|attraction)\b", re.I)
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) decodeher-growth-brain/1.0"}

def sources():
    t = open(f"{G}/expert-sources.md").read() if os.path.exists(f"{G}/expert-sources.md") else ""
    m = re.findall(r"```json\s*(\[.*?\])\s*```", t, re.S)
    try: return [s for s in json.loads(m[-1]) if s.get("rss")] if m else []
    except json.JSONDecodeError: return []
def get(url, timeout=30):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
def items(src):   # (id, title, link, published datetime) from RSS 2.0 or Atom
    try: root = ET.fromstring(get(src["rss"]))
    except Exception: return []
    ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}
    out = []
    for e in root.findall("a:entry", ns):   # Atom (YouTube)
        link = (e.find("a:link", ns).get("href") if e.find("a:link", ns) is not None else "")
        vid = e.findtext("yt:videoId", default="", namespaces=ns)
        out.append((vid or link, e.findtext("a:title", default="", namespaces=ns), link, e.findtext("a:published", default="", namespaces=ns)))
    for e in root.iter("item"):             # RSS 2.0 (blogs)
        link = e.findtext("link", default=""); out.append((e.findtext("guid", default=link) or link, e.findtext("title", default=""), link, e.findtext("pubDate", default="")))
    return out
def when(s):
    for f in ("%Y-%m-%dT%H:%M:%S%z", "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"):
        try: return datetime.datetime.strptime(s.replace("+00:00", "+0000"), f).replace(tzinfo=None)
        except Exception: pass
    return datetime.datetime(2000, 1, 1)
def youtube_text(url):
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["uv", "run", "-q", "--with", "yt-dlp", "yt-dlp", "--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "en.*,en",
                        "--sub-format", "vtt", "--extractor-args", "youtube:player_client=mweb", "-o", f"{d}/v.%(ext)s", url], capture_output=True, timeout=240)
        vtt = sorted(glob.glob(f"{d}/*.vtt"))
        if not vtt: return ""
        lines, last = [], ""
        for l in open(vtt[0], errors="ignore"):
            l = re.sub(r"<[^>]+>", "", l).strip()
            if not l or "-->" in l or l.startswith(("WEBVTT", "Kind:", "Language:")) or l == last: continue
            lines.append(l); last = l
        return " ".join(lines)
def blog_text(url):
    try: h = get(url).decode("utf-8", "ignore")
    except Exception: return ""
    h = re.sub(r"(?is)<(script|style|nav|header|footer|aside|form)[^>]*>.*?</\1>", " ", h)
    m = re.search(r"(?is)<article[^>]*>(.*?)</article>", h); h = m.group(1) if m else h
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"(?s)<[^>]+>", " ", h))).strip()

st = json.load(open(STATE)) if os.path.exists(STATE) else {"seen": []}
seen = set(st["seen"]); cands = []
for s in sources():
    for iid, title, link, pub in items(s)[:6]:
        key = hashlib.sha1(f"{s['name']}|{iid}".encode()).hexdigest()[:12]
        if key in seen or not link: continue
        if (datetime.datetime.now() - when(pub)).days > 45: continue    # only recent material
        if not RELEVANT.search(title or ""):                              # 10-16: skip off-topic posts (API awards, image sizes, AI news)
            seen.add(key); continue
        cands.append((s.get("trust") == "high", when(pub), s, key, title, link, pub))
    time.sleep(1)
cands.sort(key=lambda c: (c[0], c[1]), reverse=True)
got = 0
for _, _, s, key, title, link, pub in cands:
    if got >= MAX: break
    yt = "youtube.com" in link or "youtu.be" in link
    text = youtube_text(link) if yt else blog_text(link)
    if len(text) < 800: seen.add(key) if not yt else None; continue   # YouTube may just be rate-limited: retry another day
    slug = re.sub(r"[^a-z0-9]+", "-", s["name"].lower()).strip("-")[:24]
    open(f"{INBOX}/{datetime.date.today()}-{slug}-{key}.txt", "w").write(
        f"SOURCE: {s['name']} ({s.get('type','')}, trust {s.get('trust','')})\nTITLE: {title}\nURL: {link}\nPUBLISHED: {pub}\n\n{text[:30000]}\n")
    seen.add(key); got += 1; time.sleep(8 if yt else 2)
st["seen"] = sorted(seen)[-3000:]; st["last"] = datetime.datetime.now().isoformat(timespec="seconds")
json.dump(st, open(STATE, "w"), indent=1)
print(f"{len(sources())} sources, {len(cands)} new items, saved {got} to {INBOX}")
