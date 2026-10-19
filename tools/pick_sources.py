"""Pick the next sources for new reels (owner 10-19). Order:
  1. the VIRAL BANK (brain/research/viral-bank/yt-tiktok.jsonl + ig.jsonl): reels/shorts not yet used (used_by null), not marked
     off-niche (fits_us false), with a real script (>= 60 words of transcript), >= 1M views (or estimate), biggest first
  2. ONLY when the bank has run dry: the Dark Needle brain (Obsidian vault "YouTube Brains/The Dark Needle/Videos"), one KEY IDEA
     per reel — his videos are long, so a reel keeps one idea and his framing of it. Only the Videos notes are read, never the
     vault's personal files (Memory.md, Conversations, Character, Relationship).
Usage:
  python3 tools/pick_sources.py 6            # print the next 6 sources as JSON lines (does not mark anything)
  python3 tools/pick_sources.py --mark <url>=<reel-prefix> ...   # record use (bank: used_by; Dark Needle: darkneedle-used.json)
  python3 tools/pick_sources.py --left       # how many unused sources are left in each pool"""
import glob, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
BANK = ["brain/research/viral-bank/yt-tiktok.jsonl", "brain/research/viral-bank/ig.jsonl"]
DN = os.path.expanduser("~/Documents/YouTube Brains/The Dark Needle/Videos")
DN_USED = "brain/research/viral-bank/darkneedle-used.json"
MIN_VIEWS = 1_000_000


def rows(p):
    return [json.loads(l) for l in open(p) if l.strip()] if os.path.exists(p) else []


def views(r):
    for k in ("views", "views_est"):
        try:
            v = int(float(r.get(k) or 0))
            if v: return v
        except (TypeError, ValueError): pass
    return 0


def bank_pool():
    out = []
    for p in BANK:
        for r in rows(p):
            text = r.get("transcript_en") or r.get("transcript") or ""
            if r.get("used_by") or r.get("fits_us") is False or len(text.split()) < 60 or views(r) < MIN_VIEWS: continue
            if r.get("type") == "carousel": continue
            out.append({"source": "bank", "url": r["url"], "views": views(r), "title": r.get("title") or r.get("hook"),
                        "by": r.get("channel") or r.get("account"), "text": text})
    return sorted(out, key=lambda x: -x["views"])


def dn_used():
    return json.load(open(DN_USED)) if os.path.exists(DN_USED) else {}


def dn_pool():
    used, out = dn_used(), []
    for f in sorted(glob.glob(f"{DN}/*.md"), reverse=True):   # newest first (file names start with the publish date)
        t = open(f, encoding="utf-8").read()
        url = (re.search(r'^url:\s*"?([^"\n]+)', t, re.M) or [None, ""])[1]
        title = (re.search(r'^title:\s*"?([^"\n]+)', t, re.M) or [None, os.path.basename(f)])[1]
        ideas = re.findall(r"^- (.+?)(?: \(\[\d|$)", t.split("## Key ideas", 1)[-1].split("\n## ", 1)[0], re.M)
        for i, idea in enumerate(ideas):
            key = f"{url}#{i}"
            if key in used: continue
            out.append({"source": "darkneedle", "url": key, "views": None, "title": title, "by": "The Dark Needle", "text": idea.strip()})
    return out


def main():
    a = sys.argv[1:]
    if a and a[0] == "--left":
        print(f"viral bank: {len(bank_pool())} unused ≥1M with a script · Dark Needle: {len(dn_pool())} unused key ideas"); return
    if a and a[0] == "--mark":
        used = dn_used(); bank_marks = {}
        for m in a[1:]:
            url, reel = m.rsplit("=", 1)
            if "#" in url and "youtube.com/watch" in url: used[url] = reel
            else: bank_marks[url] = reel
        json.dump(used, open(DN_USED, "w"), indent=1)
        for p in BANK:
            rs = rows(p); hit = False
            for r in rs:
                if r.get("url") in bank_marks: r["used_by"] = bank_marks[r["url"]]; hit = True
            if hit: open(p, "w").write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs))
        print(f"marked {len(a) - 1}"); return
    n = int(a[0]) if a else 6
    pool = bank_pool()
    if len(pool) < n: pool += dn_pool()   # backup only when the bank can't fill the batch
    for s in pool[:n]: print(json.dumps(s, ensure_ascii=False))


if __name__ == "__main__":
    main()
