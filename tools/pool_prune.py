"""Keep the shared clip pool (reels/_pool) to clips we can actually use (owner 10-18: "the factory's clips aren't our style and eat
my space"). Every Pinterest search downloads ~8 clips per line; tools/clipsheet.py fingerprints each one and marks it on-style or not
(reels/_pool/emb.json "ok"). A clip that FAILED that style check is never offered to any reel, and a clip with overlaid text
(library/clip-text.json) is never picked — so both are deleted here, unless a reel already used it. Clips not checked yet stay.
The owner's Telegram clips (reels/_pool/telegram-dark) are never touched.
10-18 owner ("a permanent solution for the disk"): the pool is also CAPPED (default 900 MB, --cap MB). Above the cap the oldest
clips go first — never one a reel used, never the owner's, never one an unfinished reel still holds (a hard link in its clips/cand).
Usage: python3 tools/pool_prune.py [--dry] [--cap MB]   (after each reel, and by tools/manager.py whenever the disk runs low)"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
DRY = "--dry" in sys.argv
CAP = float(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 900.0
emb = json.load(open("reels/_pool/emb.json")) if os.path.exists("reels/_pool/emb.json") else {}
TX = json.load(open("library/clip-text.json")) if os.path.exists("library/clip-text.json") else {}
usage = json.load(open("library/clip-usage.json")) if os.path.exists("library/clip-usage.json") else {"reels": []}
used = {p for r in usage["reels"] for p in r["pins"]}
pin = lambda f: (re.search(r"(\d{12,})", os.path.basename(f)) or [None, None])[1]
n, mb = 0, 0.0
for f in glob.glob("reels/_pool/*/*.mp4"):
    if "/telegram-dark/" in f: continue
    p = pin(f); e = emb.get(p or "", "missing")
    if p in used or e == "missing": continue   # used in a reel, or not fingerprinted yet
    if e is None or not e.get("ok") or TX.get(os.path.basename(f), [False])[0]:
        mb += os.path.getsize(f) / 1e6; n += 1
        if not DRY: os.remove(f)
# the cap: oldest first, only clips no reel used and no unfinished reel is holding (st_nlink == 1)
left = [f for f in glob.glob("reels/_pool/*/*.mp4") if os.path.exists(f) and "/telegram-dark/" not in f]
size = sum(os.path.getsize(f) for f in left) / 1e6
for f in sorted(left, key=os.path.getmtime):
    if size <= CAP: break
    st = os.stat(f)
    if pin(f) in used or st.st_nlink > 1: continue
    size -= st.st_size / 1e6; mb += st.st_size / 1e6; n += 1
    if not DRY: os.remove(f)
for d in glob.glob("reels/_pool/*/"):
    if not DRY and not os.listdir(d): os.rmdir(d)
print(f"{'would remove' if DRY else 'removed'} {n} unusable pool clips ({mb:.0f} MB)")
