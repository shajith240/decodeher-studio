"""Deep-dive one or more creator pages so we can replicate them (owner 10-19: "give you a page link → get its content, find the
patterns, save it in our bank"). Does all the heavy work locally so a Claude session only has to read one short digest.

Usage:
  python3 tools/clone_page.py <page> [<page> ...] [--top 15]
    <page> = a YouTube channel (https://www.youtube.com/@handle, /channel/UC..., /shorts tab)  or  an Instagram account
             (https://www.instagram.com/<user>/ or @user). TikTok pages can't be read anonymously (see viral_bank_yt.py).
For each page:
  1. lists its posts with view counts and keeps the --top N by views (YouTube: the /shorts tab; Instagram: the outliers that
     tools/viral_bank_ig.py keeps — >= 1M views or >= 3x the account's median)
  2. downloads + transcribes them into the viral bank (tools/viral_bank_yt.py --add / tools/viral_bank_ig.py --accounts),
     so every post becomes a normal bank entry with "used_by": null
  3. measures each one: duration, words per second, cuts per 10 s (ffmpeg scene changes), hook (first sentence), first words
  4. writes brain/research/channels/<name>/posts.json + digest.md (the ONLY thing Claude needs to read) + sheet.jpg
     (opening frames of the top 8)
Anonymous only (no login, no cookies, never @thedecodeher) — the collectors enforce it and stop cleanly on a rate limit."""
import argparse, glob, json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
BANK = "brain/research/viral-bank"; OUT = "brain/research/channels"


def run(cmd, timeout=3600):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)


def page_kind(p):
    p = p.strip()
    if "youtube.com" in p or "youtu.be" in p: return "yt", p
    if "tiktok.com" in p: return "tt", p
    m = re.search(r"instagram\.com/([A-Za-z0-9_.]+)", p) or re.match(r"@?([A-Za-z0-9_.]+)$", p)
    return ("ig", m.group(1)) if m else (None, p)


def yt_top(url, top):
    base = re.sub(r"/(shorts|videos|featured|streams)/?$", "", url.rstrip("/")).split("?")[0]
    r = run(["yt-dlp", "--flat-playlist", "-J", "--playlist-end", "400", base + "/shorts"], 600)
    try: d = json.loads(r.stdout)
    except ValueError: sys.exit(f"could not list {base}/shorts: {r.stderr[-300:]}")
    es = [e for e in d.get("entries", []) if e.get("view_count")]
    es.sort(key=lambda e: -e["view_count"])
    name = re.sub(r"[^a-z0-9]+", "-", (d.get("channel") or d.get("uploader") or base.split("/")[-1]).lower()).strip("-")
    return name, [e["id"] for e in es[:top]], len(es)


def bank_rows(path):
    return [json.loads(l) for l in open(path) if l.strip()] if os.path.exists(path) else []


def measure(mp4, dur, text):
    cuts = None
    if mp4 and os.path.exists(mp4):
        r = run(["ffmpeg", "-nostats", "-i", mp4, "-vf", "select='gt(scene,0.32)',showinfo", "-an", "-f", "null", "-"], 300)
        cuts = len(re.findall(r"pts_time:", r.stderr))
    words = len((text or "").split())
    return {"wps": round(words / dur, 2) if dur else None, "cuts_per_10s": round(cuts / dur * 10, 1) if (cuts is not None and dur) else None,
            "words": words}


def sheet(mp4s, out):
    tiles = []
    for i, m in enumerate(mp4s[:8]):
        t = f"/tmp/clone_tile_{i}.jpg"
        if run(["ffmpeg", "-v", "error", "-y", "-ss", "0", "-t", "3", "-i", m, "-vf", "fps=1,scale=180:-1,tile=3x1", "-frames:v", "1", t]).returncode == 0:
            tiles.append(t)
    if tiles:
        args = ["ffmpeg", "-v", "error", "-y"] + sum((["-i", t] for t in tiles), []) + ["-filter_complex", f"vstack=inputs={len(tiles)}" if len(tiles) > 1 else "null", out]
        run(args)


def digest(name, page, rows, total, kind):
    d = f"{OUT}/{name}"; os.makedirs(d, exist_ok=True)
    posts = []
    for r in rows:
        dur = r.get("duration_s") or 0
        text = r.get("transcript_en") or r.get("transcript") or ""
        vid = r.get("id") or r.get("code") or (r.get("url") or "").rstrip("/").split("/")[-1]
        mp4 = next(iter(glob.glob(f"library/research/viral/*/{vid}.mp4")), None)
        posts.append({"url": r.get("url"), "views": r.get("views") or r.get("views_est"), "likes": r.get("likes"), "duration_s": dur,
                      "type": r.get("type", "short"), "hook": r.get("hook"), "onscreen": (r.get("onscreen_text") or "")[:160],
                      "text": text, "mp4": mp4, **measure(mp4, dur, text)})
    posts.sort(key=lambda p: -(p["views"] or 0))
    json.dump(posts, open(f"{d}/posts.json", "w"), indent=1, ensure_ascii=False)
    num = lambda k: sorted(p[k] for p in posts if p.get(k) is not None)
    med = lambda k: (num(k)[len(num(k)) // 2] if num(k) else None)
    L = [f"# {name}: page digest ({kind}, {page})", "",
         f"Scanned {total} posts; kept the top {len(posts)} by views. Median: {med('duration_s')} s long, {med('wps')} words/s, "
         f"{med('cuts_per_10s')} cuts per 10 s, {med('words')} words.", "",
         "| # | views | sec | w/s | cuts/10s | hook |", "|---|---|---|---|---|---|"]
    for i, p in enumerate(posts, 1):
        L.append(f"| {i} | {(p['views'] or 0) / 1e6:.1f}M | {p['duration_s']} | {p['wps']} | {p['cuts_per_10s']} | {(p['hook'] or p['onscreen'] or '')[:90]} |")
    L += ["", "## Full scripts of the top 6 (for the rulebook; the rest are in posts.json)"]
    for i, p in enumerate(posts[:6], 1):
        L += ["", f"**{i}. {(p['views'] or 0) / 1e6:.1f}M · {p['url']}**", (p["text"] or p["onscreen"] or "(no speech)")[:1400]]
    open(f"{d}/digest.md", "w").write("\n".join(L) + "\n")
    sheet([p["mp4"] for p in posts if p["mp4"]], f"{d}/sheet.jpg")
    return d


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("pages", nargs="+"); ap.add_argument("--top", type=int, default=15)
    a = ap.parse_args()
    for page in a.pages:
        kind, ref = page_kind(page)
        if kind == "yt":
            name, ids, total = yt_top(ref, a.top)
            if not ids: print(f"{page}: no shorts with view counts"); continue
            r = run([sys.executable, "tools/viral_bank_yt.py", "--add", *[f"https://www.youtube.com/shorts/{i}" for i in ids], "--transcribe"], 7200)
            print(r.stdout[-600:], r.stderr[-300:])
            rows = [x for x in bank_rows(f"{BANK}/yt-tiktok.jsonl") if (x.get("id") or "") in ids]
        elif kind == "ig":
            acc = f"/tmp/clone_accounts_{ref}.txt"; open(acc, "w").write(ref + "\n")
            r = run(["uv", "run", "-q", "--with", "curl_cffi", "python", "tools/viral_bank_ig.py", "--accounts", acc, "--max-new", str(a.top),
                     "--transcribe", "--relist"], 7200)
            print(r.stdout[-600:], r.stderr[-300:])
            rows = [x for x in bank_rows(f"{BANK}/ig.jsonl") if (x.get("account") or "").lower().lstrip("@") == ref.lower()]
            rows.sort(key=lambda x: -((x.get("views") or x.get("views_est") or 0))); rows = rows[:a.top]; name, total = ref.lower(), len(rows)
        elif kind == "tt":
            print(f"{page}: TikTok pages can't be read anonymously — send the videos' links one by one or use the YouTube/IG mirror"); continue
        else:
            print(f"{page}: not a YouTube or Instagram page"); continue
        if not rows: print(f"{page}: nothing collected (rate limit? run again later)"); continue
        d = digest(name, page, rows, total, kind)
        print(f"{page}: {len(rows)} posts → {d}/digest.md, {d}/posts.json, {d}/sheet.jpg")


if __name__ == "__main__":
    main()
