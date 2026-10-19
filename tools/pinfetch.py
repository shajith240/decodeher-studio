"""Zoltium-style clip finder (owner, 10-14): per spoken line, Pinterest 2D-animation clips that look like Zoltium AND show the line.
Usage: uv run --with gallery-dl --with yt-dlp --with secretstorage \
         python tools/pinfetch.py <reel_dir> [per_line=15]
Reads <reel>/shots.json [{t, say, q}] ("OUTRO" skipped). For each line: Pinterest search "<q> dark psychology" (owner 10-16: that suffix gives the moody, on-topic look) with the
owner's Brave login (gallery-dl; ≤ per_line results, pauses between searches) into <reel>/clips/cand/NN/.
FETCH ONLY (10-14): picking is tools/clipsheet.py (style gate + contact sheets) → Haiku judges → tools/clippick.py.
LINES=4,16 re-searches just those lines with their (new) q, ADDING to what is there; pins seen before are skipped."""
import glob, json, os, subprocess, sys, time, urllib.parse
# Pinterest login: the Brave keyring on the laptop; in the cloud (no browser) a cookies.txt from env PINTEREST_COOKIES_FILE (10-15)
COOKIES = ["--cookies", os.environ["PINTEREST_COOKIES_FILE"]] if os.environ.get("PINTEREST_COOKIES_FILE") else ["--cookies-from-browser", "brave+gnomekeyring"]

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
R = os.path.abspath(sys.argv[1]); N = int(sys.argv[2]) if len(sys.argv) > 2 else 15
shots = json.load(open(f"{R}/shots.json")); C = f"{R}/clips/cand"; os.makedirs(C, exist_ok=True)

# fetch
for n, s in enumerate(shots):
    if s["q"] == "OUTRO": continue
    d = f"{C}/{n:02d}"; again = os.environ.get("LINES")
    if again and n not in {int(x) for x in again.split(",")}: continue
    if not again and glob.glob(f"{d}/*.mp4"): continue
    before = set(glob.glob(f"{d}/*.mp4"))
    # 10-19 owner ("why isn't it pulling clips?"): the second search (factory_research, env PLAIN=1) drops the moody suffix — for literal
    # lines ("man doing push ups") "dark psychology" returns moody clips that don't show the action, and the judges reject them all
    q = urllib.parse.quote(f'{s["q"]} animation' if os.environ.get("PLAIN") else f'{s["q"]} dark psychology')
    # --download-archive: a pin already fetched for an earlier line is not fetched again (owner 10-14: duplicates)
    subprocess.run(["gallery-dl", *COOKIES, "-o", "extractor.pinterest.videos=ytdl",
                    "--range", f"1-{N * 4}", "--download-archive", f"{R}/clips/seen.sqlite3", "--filter", "extension in ('mp4','m3u8')", "-D", d,
                    f"https://www.pinterest.com/search/pins/?q={q}"], capture_output=True, timeout=600)
    new = sorted(set(glob.glob(f"{d}/*.mp4")) - before); vids = new[: N]
    for x in new[N:]: os.remove(x)
    print(f"line {n:02d}: {len(vids)} clips  ({s['q']})", flush=True); time.sleep(4)
