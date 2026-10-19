"""Viral bank, Instagram half (owner rule 10-19 "steal like an artist": every reel/carousel remixes a post that already went viral).
Collects outlier posts from the accounts and topic pages in brain/research/viral-bank/accounts-ig.txt into
brain/research/viral-bank/ig.jsonl.

ANONYMOUS ONLY. It uses only what Instagram serves to a logged-out browser: the public reels tab and /popular/<topic>/ pages
(they carry the real play count), the profile-timeline GraphQL query (50-100 posts with likes), and the public /embed/ page
of a single post (caption, likes, video). Never a login, never browser cookies, never @thedecodeher. Slow on purpose:
8-14 s between profile requests, 5-9 s between embed pages. On a rate limit (401/429/"wait a few minutes") it saves what it
has and exits 0; the next run resumes (accounts listed in the last 20 h come from the cache, URLs already in ig.jsonl are
skipped).

Views: "views" is Instagram's play count when Instagram shows it to logged-out visitors (reels tab = the 12 newest + pinned
reels, topic pages). For older reels it is unknown; then "views_est" = likes x that account's own plays-per-like ratio
(measured on its reels tab) and "views_estimated": true. Accounts that hide likes fall back to the embed page's legacy
video_view_count x 2.8 (measured: 1,106,127 plays vs 398,746 embed views on DMmMBERIvUV).
Kept: reels with >= 1M views (or estimate), or >= 3x the account's median and >= 300k; carousels in the account's top 10% by
likes; topic-page reels with >= 1M plays. Entries <= 30 days old get their counts refreshed each run.
Every new entry gets "added" (date) and "used_by": null (set it to our reel id when an idea is used, so it is not reused).
The analysis fields (concept, structure, visual, why_it_worked, fits_us) are written by a Claude session reading the
transcript and contact sheet; the script leaves them null and sets "analysed": false.

Usage:
  uv run -q --with curl_cffi python tools/viral_bank_ig.py                 # add up to 30 new outliers, refresh recent counts
  uv run -q --with curl_cffi python tools/viral_bank_ig.py --max-new 50 --transcribe
      --transcribe: for NEW reels with >= 1M views, download the mp4 to library/research/viral/ig/<code>.mp4, transcribe it
      with faster-whisper, and save 3 frames (0.5 s, 3 s, middle) as <code>_sheet.jpg; new carousels get slides 1-3 saved.
  --per-account N (default 72 posts)   --accounts FILE   --relist (ignore the 20 h listing cache)
  --media-only CODE...  (download/transcribe/sheet the given bank entries, e.g. after a rate-limited run)"""
import argparse, datetime as dt, json, os, random, re, statistics, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
BANK = "brain/research/viral-bank/ig.jsonl"
ACCOUNTS = "brain/research/viral-bank/accounts-ig.txt"
MEDIA = "library/research/viral/ig"            # git-ignored (library/)
CACHE = "library/research/viral/ig/_cache"
APP_ID = "936619743392459"
TIMELINE_DOC = "28975909992013618"
EMBED_TO_PLAYS = 2.8
# a topic-page reel must be about women / dating / attraction to enter the bank (topic pages also surface travel "attractions")
NICHE = re.compile(r"(psycholog|attract|texting|text her|female|she likes|likes you|crush|girls?\b|wom[ae]n\b|dating|mixed signal|"
                   r"red flag|manipulat|ghost|flirt|obsess|chase|girlfriend|\bher\b|\bshe\b)", re.I)
B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"


class RateLimited(Exception):
    pass


def now():
    return dt.datetime.now(dt.timezone.utc)


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def nap(lo, hi):
    time.sleep(random.uniform(lo, hi))


def session():
    from curl_cffi import requests
    s = requests.Session(impersonate="chrome")
    s.get("https://www.instagram.com/", timeout=30)
    return s


def limited(r):
    head = r.text[:600]
    return r.status_code in (401, 429) or "wait a few minutes" in head or '"require_login":true' in head


def code_time(code):
    """Post time from the shortcode: the media id's top bits are ms since Instagram's 2011-08-24 epoch."""
    i = 0
    for ch in code[:11]:
        i = i * 64 + B64.index(ch)
    return int((i >> 23) / 1000 + 1314220507)


def page_nodes(html, want):
    """Every dict in the page's preloaded JSON that has all keys in `want`."""
    acc = []

    def walk(o):
        if isinstance(o, dict):
            if all(k in o for k in want):
                acc.append(o)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
    for b in re.findall(r'<script type="application/json"[^>]*>(.*?)</script>', html, re.S):
        if want[-1] in b:
            try:
                walk(json.loads(b))
            except Exception:
                pass
    return acc


def best_video(vv):
    vv = vv or []
    return max(vv, key=lambda c: c.get("width", 0) * c.get("height", 0)).get("url") if vv else None


# ---------- sources ----------
def reels_tab(s, user):
    """Public reels tab: the 12 newest + pinned reels with their real play counts. {code: {...}}"""
    r = s.get(f"https://www.instagram.com/{user}/reels/", timeout=30)
    if limited(r):
        raise RateLimited(f"reels tab {user}: {r.status_code}")
    out = {}
    for m in page_nodes(r.text, ["code", "play_count"]):
        out[m["code"]] = {"plays": m.get("play_count"), "likes": m.get("like_count"), "comments": m.get("comment_count"),
                          "pinned": bool(m.get("clips_tab_pinned_user_ids")), "video_url": best_video(m.get("video_versions"))}
    return out


def list_account(s, user, maxn):
    """Profile timeline via the logged-out GraphQL query. Returns nodes, or None if Instagram hides the user when logged out."""
    csrf = s.cookies.get("csrftoken") or ""
    nodes, after = [], None
    while len(nodes) < maxn:
        v = {"data": {"count": 12, "include_reel_media_seen_timestamp": True, "include_relationship_info": True,
                      "latest_besties_reel_media": True, "latest_reel_media": True},
             "username": user, "include_multi_captions": True,
             "__relay_internal__pv__PolarisMultiCaptionCarouselEnabledrelayprovider": True,
             "__relay_internal__pv__PolarisShortDramaEnabledrelayprovider": False,
             "__relay_internal__pv__PolarisReelsRecoDebugOverlayEnabledrelayprovider": False}
        if after:
            v.update({"after": after, "before": None, "first": 12, "last": None})
        else:
            v["first"] = 12
        r = s.post("https://www.instagram.com/graphql/query",
                   data={"variables": json.dumps(v, separators=(",", ":")), "doc_id": TIMELINE_DOC, "server_timestamps": "true"},
                   headers={"x-csrftoken": csrf, "x-ig-app-id": APP_ID, "referer": f"https://www.instagram.com/{user}/",
                            "x-requested-with": "XMLHttpRequest"}, timeout=30)
        if limited(r):
            raise RateLimited(f"timeline {user}: {r.status_code}")
        try:
            d = r.json()
        except Exception:
            raise RateLimited(f"timeline {user}: non-JSON {r.status_code}")
        conn = (d.get("data") or {}).get("xdt_api__v1__feed__user_timeline_graphql_connection")
        if not conn:
            if "User lookup returned null" in r.text:
                return nodes or None
            raise RateLimited(f"timeline {user}: {r.text[:200]}")
        nodes += [e["node"] for e in conn["edges"]]
        log(f"  {user}: {len(nodes)} posts")
        pi = conn.get("page_info", {})
        if not pi.get("has_next_page"):
            break
        after = pi.get("end_cursor")
        nap(8, 14)
    return nodes


def topic_page(s, slug):
    """Public /popular/<topic>/ page: ~12 top reels for the topic with real play counts."""
    r = s.get(f"https://www.instagram.com/popular/{slug}/", timeout=30)
    if limited(r):
        raise RateLimited(f"topic {slug}: {r.status_code}")
    out = []
    for m in page_nodes(r.text, ["code", "play_count"]):
        out.append({"code": m["code"], "account": (m.get("user") or {}).get("username"), "type": "reel",
                    "taken_at": code_time(m["code"]), "likes": None, "comments": None,
                    "caption": (m.get("caption") or {}).get("text") or "", "video_url": best_video(m.get("video_versions")),
                    "slide_urls": [m.get("display_uri")], "alts": [], "slides": None, "views": m.get("play_count"),
                    "duration_s": None, "topic": slug})
    return out


def embed_media(s, code):
    """The public /embed/ page carries the post's JSON (legacy video_view_count, likes, caption, owner, video_url)."""
    r = s.get(f"https://www.instagram.com/p/{code}/embed/captioned/", timeout=30)
    if r.status_code in (401, 429):
        raise RateLimited(f"embed {code}: {r.status_code}")
    t = r.text
    i = t.find('"contextJSON":')
    if i < 0:
        return None
    try:
        raw, _ = json.JSONDecoder().raw_decode(t[i + len('"contextJSON":'):])
        m = (json.loads(raw).get("gql_data") or {}).get("shortcode_media")
    except Exception:
        return None
    if not m:
        return None
    cap = (m.get("edge_media_to_caption") or {}).get("edges") or []
    side = [e["node"] for e in (m.get("edge_sidecar_to_children") or {}).get("edges", [])]
    return {"code": code, "account": (m.get("owner") or {}).get("username"),
            "type": "reel" if m.get("is_video") else ("carousel" if side else "image"),
            "taken_at": code_time(code), "likes": (m.get("edge_liked_by") or {}).get("count"),
            "comments": (m.get("edge_media_to_comment") or {}).get("count"),
            "caption": cap[0]["node"]["text"] if cap else "", "video_url": m.get("video_url"),
            "slide_urls": [n.get("display_url") for n in (side or [m])[:3]],
            "alts": [n.get("accessibility_caption") for n in (side or [m])[:3]], "slides": len(side) or None,
            "views_embed": m.get("video_view_count"), "duration_s": m.get("video_duration")}


def ddg_codes(s, user):
    """For accounts Instagram hides from logged-out visitors: find their post URLs through DuckDuckGo (slow, polite)."""
    import urllib.parse
    codes = []
    for q in (f'site:instagram.com "{user}" reel', f'site:instagram.com "{user}"'):
        r = s.post("https://html.duckduckgo.com/html/", data={"q": q}, timeout=30)
        if r.status_code == 200:
            for c in re.findall(r"instagram\.com/(?:[A-Za-z0-9_.]+/)?(?:reel|p)/([A-Za-z0-9_-]{9,12})", urllib.parse.unquote(r.text)):
                if c not in codes:
                    codes.append(c)
        nap(20, 30)
    return codes


def slim(n, user):
    """Keep only what the bank needs from a timeline node (media URLs expire after a few days)."""
    is_reel = n.get("product_type") == "clips" or n.get("media_type") == 2
    imgs = []
    for it in (n.get("carousel_media") or [n])[:3]:
        c = (it.get("image_versions2") or {}).get("candidates") or []
        if c:
            imgs.append(max(c, key=lambda c: c["width"] * c["height"])["url"])
    return {"code": n["code"], "account": user, "type": "reel" if is_reel else ("carousel" if n.get("carousel_media") else "image"),
            "taken_at": n["taken_at"], "likes": n.get("like_count"), "comments": n.get("comment_count"),
            "caption": (n.get("caption") or {}).get("text", ""), "video_url": best_video(n.get("video_versions")),
            "slide_urls": imgs, "alts": [it.get("accessibility_caption") for it in (n.get("carousel_media") or [n])[:3]],
            "slides": n.get("carousel_media_count"), "views": None, "duration_s": None,
            "pinned": bool(n.get("timeline_pinned_user_ids"))}


# ---------- one account ----------
def scan(s, user, per_account, relist):
    """List (or read the cached list of) one account, attach play counts / estimates. Cache is saved as it goes."""
    os.makedirs(CACHE, exist_ok=True)
    cp = f"{CACHE}/{user}.json"
    cache = json.load(open(cp)) if os.path.exists(cp) else None
    if cache and not relist and (now().timestamp() - cache["listed_at"]) < 20 * 3600:
        return cache["posts"]
    old = {p["code"]: p for p in (cache or {}).get("posts", [])}
    tab = reels_tab(s, user)
    nap(8, 14)
    nodes = list_account(s, user, per_account)
    if nodes is None:
        # hidden from logged-out visitors: find post URLs on DuckDuckGo, read each through its public embed page
        log(f"  {user}: hidden from logged-out profile view; using search + embed pages")
        posts = []
        for c in ddg_codes(s, user)[:per_account]:
            p = old.get(c) or embed_media(s, c)
            nap(5, 9)
            if p and p.get("account") == user:
                if p["type"] == "reel" and not p.get("views") and p.get("views_embed"):
                    p["views_est"] = int(p["views_embed"] * EMBED_TO_PLAYS); p["views_estimated"] = True
                posts.append(p)
        json.dump({"listed_at": now().timestamp(), "via": "search+embed", "posts": posts}, open(cp, "w"), ensure_ascii=False)
        return posts
    posts = [slim(n, user) for n in nodes]
    have = {p["code"] for p in posts}
    for code, t in tab.items():                       # pinned old hits are often not in the newest 72 posts
        if code not in have:
            m = embed_media(s, code); nap(5, 9)
            if m:
                posts.append(m)
    ratios = []
    for p in posts:
        t = tab.get(p["code"])
        if t:
            p["views"] = t["plays"]; p["pinned"] = p.get("pinned") or t["pinned"]
            if t["likes"] and t["likes"] > 3:
                p["likes"], p["comments"] = t["likes"], t["comments"]
                if t["plays"]:
                    ratios.append(t["plays"] / t["likes"])
            p["video_url"] = p.get("video_url") or t["video_url"]
    ratio = statistics.median(ratios) if len(ratios) >= 3 else 18.0
    hidden = max([p["likes"] or 0 for p in posts if p["type"] == "reel"] or [99]) <= 3
    looked = 0
    for p in sorted(posts, key=lambda p: -(p["likes"] or 0)):
        if p["type"] != "reel" or p.get("views"):
            continue
        if not hidden:
            p["views_est"] = int((p["likes"] or 0) * ratio); p["views_estimated"] = True
        elif looked < 40:                               # likes hidden: the embed page's legacy view count is all we get
            prev = old.get(p["code"]) or {}
            m = prev if prev.get("views_embed") else embed_media(s, p["code"])
            if not prev.get("views_embed"):
                looked += 1; nap(5, 9)
            if m and m.get("views_embed"):
                p["views_embed"] = m["views_embed"]; p["views_est"] = int(m["views_embed"] * EMBED_TO_PLAYS)
                p["views_estimated"] = True; p["duration_s"] = m.get("duration_s")
    json.dump({"listed_at": now().timestamp(), "ratio": ratio, "posts": posts}, open(cp, "w"), ensure_ascii=False)
    log(f"  {user}: {len(posts)} posts, {len(tab)} with play counts, plays/like {ratio:.1f}")
    return posts


def vkey(p):
    return p.get("views") or p.get("views_est") or 0


def outliers(posts):
    keep = []
    reels = [p for p in posts if p["type"] == "reel"]
    vs = [vkey(p) for p in reels if vkey(p)]
    med = statistics.median(vs) if vs else None
    for p in reels:
        v = vkey(p)
        if v and (v >= 1_000_000 or (med and v >= 3 * med and v >= 300_000)):
            keep.append(p)
    cars = [p for p in posts if p["type"] == "carousel"]
    if cars:
        ls = sorted((p["likes"] or 0 for p in cars), reverse=True)
        cut = ls[max(0, int(len(ls) * 0.1) - 1)] if len(ls) >= 10 else ls[0]
        keep += [p for p in cars if (p["likes"] or 0) >= cut and (p["likes"] or 0) > 3]
    return keep


# ---------- bank file ----------
def load_bank():
    rows = []
    if os.path.exists(BANK):
        for l in open(BANK, encoding="utf-8"):
            if l.strip():
                rows.append(json.loads(l))
    return rows


def save_bank(rows):
    os.makedirs(os.path.dirname(BANK), exist_ok=True)
    rows.sort(key=lambda r: -(r.get("views") or r.get("views_est") or 0) if r["type"] == "reel" else 0)
    tmp = BANK + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for r in rows:
            if r.get("media"):                          # CDN links expire; once media is saved they are dead weight
                r.pop("_video_url", None); r.pop("_slide_urls", None)
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, BANK)


def sources(path):
    """accounts-ig.txt: one handle per line; 'topic: <slug>' lines read instagram.com/popular/<slug>/."""
    acc, topics = [], []
    for l in open(path, encoding="utf-8"):
        l = l.split("#", 1)[0].strip()
        if l.lower().startswith("topic:"):
            topics.append(l.split(":", 1)[1].strip())
        elif l:
            acc.append(l.lstrip("@"))
    return acc, topics


def url_of(p):
    return f"https://www.instagram.com/{'reel' if p['type'] == 'reel' else 'p'}/{p['code']}/"


def entry(p):
    return {"platform": "instagram", "account": p["account"], "url": url_of(p), "type": p["type"],
            "date": dt.datetime.fromtimestamp(p["taken_at"], dt.timezone.utc).date().isoformat(),
            "views": p.get("views"), "views_est": p.get("views_est"), "views_estimated": bool(p.get("views_estimated")),
            "likes": p.get("likes"), "comments": p.get("comments"), "duration_s": p.get("duration_s"),
            "pinned": bool(p.get("pinned")), "found_via": f"topic:{p['topic']}" if p.get("topic") else "account",
            "caption": p.get("caption"), "hook": None, "transcript": None, "slides": None, "concept": None,
            "structure": None, "visual": None, "why_it_worked": None, "fits_us": None,
            "added": dt.date.today().isoformat(), "used_by": None, "analysed": False, "media": None,
            "_video_url": p.get("video_url"), "_slide_urls": p.get("slide_urls")}


# ---------- media: download, transcribe, frames ----------
def fetch(s, url, path):
    if not url:
        return False
    r = s.get(url, timeout=180)
    if r.status_code != 200 or len(r.content) < 1000:
        return False
    open(path, "wb").write(r.content)
    return True


def whisper_many(paths):
    """Same approach as tools/tip_intake.py whisper(): ffmpeg -> 16 kHz mono PCM, faster-whisper 'small' int8, one model load."""
    code = ("import sys, json, subprocess, numpy as np; from faster_whisper import WhisperModel\n"
            "m = WhisperModel('small', device='cpu', compute_type='int8')\n"
            "for p in sys.argv[1:]:\n"
            "    pcm = subprocess.run(['ffmpeg','-v','error','-i',p,'-ac','1','-ar','16000','-f','s16le','-'], capture_output=True).stdout\n"
            "    a = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768\n"
            "    s, i = m.transcribe(a, vad_filter=True)\n"
            "    print(json.dumps({p: {'lang': i.language, 'text': ' '.join(x.text.strip() for x in s)}}), flush=True)\n")
    r = subprocess.run(["uv", "run", "-q", "--with", "faster-whisper", "--with", "numpy", "python", "-c", code, *paths],
                       capture_output=True, text=True, timeout=4 * 3600)
    res = {}
    for l in r.stdout.splitlines():
        try:
            res.update(json.loads(l))
        except Exception:
            pass
    return res


def contact_sheet(mp4, out_jpg, dur):
    ts = [0.5, min(3.0, max(dur - 0.2, 0.6)), max(dur / 2, 0.6)]
    frames = []
    for i, t in enumerate(ts):
        f = out_jpg.replace("_sheet.jpg", f"_f{i}.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", mp4, "-frames:v", "1", "-vf", "scale=360:-2", f])
        if os.path.exists(f):
            frames.append(f)
    if len(frames) == 3:
        subprocess.run(["ffmpeg", "-v", "error", "-y", *sum([["-i", f] for f in frames], []), "-filter_complex",
                        "[0]scale=360:640[a];[1]scale=360:640[b];[2]scale=360:640[c];[a][b][c]hstack=inputs=3", out_jpg])
    return frames


def first_sentence(t):
    t = (t or "").strip()
    m = re.match(r"(.{12,}?[.?!])(\s|$)", t)
    return (m.group(1) if m else t[:140]).strip()


def media_for(s, rows, transcribe=True):
    """Download + frames (+ transcript) for reel rows; slides 1-3 for carousel rows. Refreshes expired URLs via embed."""
    os.makedirs(MEDIA, exist_ok=True)
    todo = []
    for e in rows:
        code = e["url"].rstrip("/").split("/")[-1]
        if e["type"] == "reel":
            mp4 = f"{MEDIA}/{code}.mp4"
            if not os.path.exists(mp4) and not fetch(s, e.get("_video_url"), mp4):
                m = embed_media(s, code); nap(5, 9)          # CDN links expire: get a fresh one
                if not (m and fetch(s, m.get("video_url"), mp4)):   # (links are not kept in the bank)
                    log(f"  no video for {code}"); continue
            nap(1, 3)
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp4],
                                       capture_output=True, text=True).stdout.strip() or 0)
            sheet = f"{MEDIA}/{code}_sheet.jpg"
            if not os.path.exists(sheet):
                contact_sheet(mp4, sheet, dur)
            e["duration_s"] = round(dur, 1); e["media"] = {"video": mp4, "sheet": sheet}
            if transcribe and not e.get("transcript"):
                todo.append((mp4, e))
        elif e["type"] == "carousel":
            files = []
            urls = e.get("_slide_urls") or []
            for i, u in enumerate(urls[:3], 1):
                f = f"{MEDIA}/{code}_s{i}.jpg"
                if os.path.exists(f) or fetch(s, u, f):
                    files.append(f)
                nap(0.6, 1.5)
            if len(files) < min(3, len(urls) or 3):
                m = embed_media(s, code); nap(5, 9)
                for i, u in enumerate((m or {}).get("slide_urls") or [], 1):
                    f = f"{MEDIA}/{code}_s{i}.jpg"
                    if not os.path.exists(f) and fetch(s, u, f):
                        files.append(f)
            e["media"] = {"slides": sorted(set(files))}
    if todo:
        res = whisper_many([m for m, _ in todo])
        for m, e in todo:
            if m in res:
                e["transcript"] = res[m]["text"]; e["lang"] = res[m]["lang"]
                e["hook"] = first_sentence(res[m]["text"]) or None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-new", type=int, default=30)
    ap.add_argument("--transcribe", action="store_true")
    ap.add_argument("--per-account", type=int, default=72)
    ap.add_argument("--accounts", default=ACCOUNTS)
    ap.add_argument("--relist", action="store_true")
    ap.add_argument("--media-only", nargs="*")
    a = ap.parse_args()

    rows = load_bank()
    by_url = {r["url"]: r for r in rows}
    s = session()
    if a.media_only is not None:
        want = set(a.media_only)
        media_for(s, [r for r in rows if r["url"].rstrip("/").split("/")[-1] in want], transcribe=True)
        save_bank(rows)
        return
    accs, topics = sources(a.accounts)
    new, scanned, stopped = [], 0, None

    def add(p):
        e = by_url.get(url_of(p))
        if e:                                            # refresh counts on recent entries
            if (now() - dt.datetime.fromisoformat(e["date"]).replace(tzinfo=dt.timezone.utc)).days <= 30:
                for k in ("views", "views_est", "likes", "comments"):
                    if p.get(k):
                        e[k] = p[k]
            return
        if len(new) < a.max_new:
            e = entry(p); rows.append(e); by_url[e["url"]] = e; new.append(e)

    try:
        for user in accs:
            log(f"account {user}")
            posts = scan(s, user, a.per_account, a.relist)
            scanned += len(posts)
            for p in sorted(outliers(posts), key=lambda p: -(vkey(p) or p["likes"] or 0)):
                add(p)
            nap(8, 14)
        for slug in topics:
            log(f"topic {slug}")
            items = topic_page(s, slug)
            scanned += len(items)
            for p in items:
                if not NICHE.search(p["caption"] or "") or (p.get("views") or 0) < 1_000_000:
                    continue
                if url_of(p) not in by_url and len(new) < a.max_new:
                    m = embed_media(s, p["code"]); nap(5, 9)     # likes, comments, full caption, duration
                    if m:
                        p.update({k: m[k] for k in ("likes", "comments", "caption", "duration_s") if m.get(k) is not None})
                        p["video_url"] = p.get("video_url") or m.get("video_url")
                add(p)
            nap(7, 11)
    except RateLimited as ex:
        stopped = str(ex)
        log(f"rate-limited ({ex}); saving and stopping. Run again later to resume.")
    save_bank(rows)
    if a.transcribe and new:
        try:
            media_for(s, [e for e in new if e["type"] == "carousel" or (e.get("views") or e.get("views_est") or 0) >= 1_000_000])
        except RateLimited as ex:
            stopped = stopped or str(ex)
        save_bank(rows)
    print(json.dumps({"scanned": scanned, "new": len(new), "bank": len(rows), "rate_limited": stopped}))


if __name__ == "__main__":
    main()
