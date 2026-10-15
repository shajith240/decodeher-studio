"""Fetch clips for a whole batch at once (owner 10-14: "get the work fast"): every distinct picture ("q") across all the reels is
searched on Pinterest ONCE, into a shared pool (reels/_pool/<q>/), then hard-linked into each reel's clips/cand/NN/ (no extra disk).
Usage: uv run --with gallery-dl --with yt-dlp --with secretstorage python tools/fetch_pool.py <reel_dir> [<reel_dir> ...] [--per 12]
Gentle with the owner's account: two searches at a time, a pause between searches, pins already fetched are skipped (download archive)."""
import glob, json, os, re, subprocess, sys, time, urllib.parse
from concurrent.futures import ThreadPoolExecutor
# Pinterest login: the Brave keyring on the laptop; in the cloud (no browser) a cookies.txt from env PINTEREST_COOKIES_FILE (10-15)
COOKIES = ["--cookies", os.environ["PINTEREST_COOKIES_FILE"]] if os.environ.get("PINTEREST_COOKIES_FILE") else ["--cookies-from-browser", "brave+gnomekeyring"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from activity import log

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); POOL = os.path.join(ROOT, "reels/_pool"); os.makedirs(POOL, exist_ok=True)
args = sys.argv[1:]; per = 12
if "--per" in args: i = args.index("--per"); per = int(args[i + 1]); args = args[:i] + args[i + 2:]
slug = lambda q: re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:60]
need = {}
for R in map(os.path.abspath, args):
    for n, s in enumerate(json.load(open(f"{R}/shots.json"))):
        if s["q"] != "OUTRO": need.setdefault(s["q"].strip().lower(), []).append((R, n))
print(f"{len(need)} distinct pictures for {sum(len(v) for v in need.values())} shots", flush=True)
def one(item):
    k, (q, users) = item; d = os.path.join(POOL, slug(q))
    if not glob.glob(f"{d}/*.mp4"):
        os.makedirs(d, exist_ok=True)
        subprocess.run(["gallery-dl", *COOKIES, "-o", "extractor.pinterest.videos=ytdl",
                        "--range", f"1-{per * 4}", "--download-archive", f"{POOL}/seen-{k % 2}.sqlite3", "--filter", "extension in ('mp4','m3u8')", "-D", d,
                        "https://www.pinterest.com/search/pins/?q=" + urllib.parse.quote(f"{q} flat 2d animation")], capture_output=True, timeout=600)
        for x in sorted(glob.glob(f"{d}/*.mp4"))[per:]: os.remove(x)
        time.sleep(4)
    vids = sorted(glob.glob(f"{d}/*.mp4"))
    for R, n in users:
        cd = f"{R}/clips/cand/{n:02d}"; os.makedirs(cd, exist_ok=True)
        for v in vids:
            dst = f"{cd}/{os.path.basename(v)}"
            if not os.path.exists(dst): os.link(v, dst)
    log(f"Clip search · {q} · {len(vids)} clips · {k + 1} of {len(need)}")
    print(f"[{k + 1}/{len(need)}] {len(vids):2d} clips  {q}  → {len(users)} shot(s)", flush=True)
# two searches at a time (owner 10-14: faster), still paced; each worker keeps its own download archive (no shared-db lock)
with ThreadPoolExecutor(2) as ex: list(ex.map(one, enumerate(sorted(need.items()))))
