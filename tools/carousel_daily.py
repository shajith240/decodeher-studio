"""Daily carousel maker (owner 10-19: "2 carousels a day, add it to the pipeline"). Keeps >= 4 carousels booked (2 days).
For each new carousel:
  1. source = the next unused viral carousel by likes from library/research/<creator>/<date>_<code>/ (full slides 01.jpg… + meta.json),
     e.g. @manly_pinnacle (tools/clone_page.py / the IG viral bank add more creators)
  2. Claude (Sonnet) reads the slides and writes our spec at 95/5 (same points, same order; plain fixed-size title, max 4 lines;
     highlights = at most 2 single non-adjacent words that carry the promise; our closing line) → brain/content/carousels/<slug>.json
     It refuses (skip) posts that are ads, pure sex/biology, or off our niche.
  3. tools/pick_cover.py picks a cover whose look + expression fits (owner's Telegram covers first, then the AI-women pool;
     never a dark-psychology clip), tools/carousel_render.py renders it, the slides go to JPEG, tools/ig_queue.js carousel books it.
Usage: python3 tools/carousel_daily.py [--n 2] [--min-booked 4]      (run daily by the decodeher-carousels timer)"""
import argparse, glob, json, os, re, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
USED = "brain/content/carousels/sources-used.json"
CV = ["uv", "run", "-q", "--with", "opencv-python-headless==4.10.0.84"]
log = lambda m: open("logs/activity.log", "a").write(f"{time.strftime('%H:%M:%S')}  Carousels · {m}\n")


def booked():
    out = subprocess.run(["node", "tools/ig_queue.js", "ids"], capture_output=True, text=True).stdout
    return sum(1 for l in out.splitlines() if l.startswith("c-") and " queued " in f" {l} ")


def sources():
    used = json.load(open(USED)) if os.path.exists(USED) else []
    rows = []
    for d in glob.glob("library/research/*/20*_*"):
        slides = sorted(glob.glob(f"{d}/[0-9][0-9].jpg"))
        if len(slides) < 3 or d in used: continue
        m = json.load(open(f"{d}/meta.json")) if os.path.exists(f"{d}/meta.json") else {}
        rows.append((int(m.get("likes") or 0), d, slides, m))
    return sorted(rows, key=lambda r: -r[0]), used


def write_spec(d, slides, meta, n):
    slug = f"c{n}-" + re.sub(r"[^a-z0-9]+", "-", (meta.get("caption") or os.path.basename(d)).lower())[:28].strip("-")
    out = f"brain/content/carousels/{slug}.json"
    example = open("brain/content/carousels/c2-girls-to-avoid.json").read()
    prompt = f"""You are remaking a viral Instagram carousel for @thedecodeher (dating psychology for men, faceless, plain English).
Read these slide images in order: {', '.join(os.path.join(ROOT, s) for s in slides)}
Original caption: {(meta.get('caption') or '')[:1500]}
Original likes: {meta.get('likes')} · url: {meta.get('url') or meta.get('permalink') or d}

If this post is an ad, pure sex/biology content, or not about women/dating/attraction/relationships for men, reply with exactly SKIP.
Otherwise write ONLY a JSON file to {os.path.join(ROOT, out)} with the same shape as this example:
{example}
Rules (owner):
- 95/5: keep the SAME points in the SAME order with the same meaning and examples, reworded sentence by sentence (never word for word).
  Drop his ad / book / "link in bio" slides. One or two points per slide (two when they are short), at most 10 points total.
- slug "{slug}", source = creator + title + likes + url + "(95/5)".
- cover.headline: plain, dead-simple English that says what the carousel gives, 6-10 words (it must fit 3-4 lines at a fixed size).
  Put [brackets] around AT MOST 2 single words, never next to each other, that carry the promise (the number + the key action/outcome).
  cover.sub: a short line in brackets style "(…)" with the payoff or stakes. cover.image: "" (picked later).
- closing: our line, "Save this …" or "Send this to the friend who …". caption: hook line, 1-2 short lines, a question, then 3 hashtags.
Reply DONE when the file is written."""
    r = subprocess.run([os.environ.get("CLAUDE_BIN", "claude"), "-p", prompt, "--model", "sonnet", "--allowedTools", "Read", "Write",
                        "--output-format", "text"], capture_output=True, text=True, timeout=900).stdout
    if "SKIP" in r and not os.path.exists(out): return None
    return out if os.path.exists(out) else None


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=2); ap.add_argument("--min-booked", type=int, default=4)
    a = ap.parse_args()
    have = booked(); need = max(0, a.min_booked - have)
    if not need: return print(f"{have} carousels booked, nothing to do")
    rows, used = sources(); made = 0; n0 = len(glob.glob("brain/content/carousels/c*-*.json")) + 1
    for likes, d, slides, meta in rows:
        if made >= min(need, a.n): break
        used.append(d); json.dump(used, open(USED, "w"), indent=1)
        spec = write_spec(d, slides, meta, n0 + made)
        if not spec: log(f"skipped {os.path.basename(d)} (ad / off-niche / no spec)"); continue
        slug = json.load(open(spec))["slug"]; out = f"deliverables/carousels/{slug}"
        try:
            subprocess.run(CV + ["python", "tools/pick_cover.py", spec], check=True, timeout=900)
            r = subprocess.run(CV + ["--with", "playwright", "python", "tools/carousel_render.py", spec], check=True, capture_output=True, text=True, timeout=900)
            if "warn" in r.stdout or "OVERFLOW" in r.stdout: log(f"{slug}: render warning ({r.stdout.strip().splitlines()[0][:120]}) — not booked"); continue
            for f in sorted(glob.glob(f"{out}/[0-9][0-9].png")):
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-q:v", "2", f[:-4] + ".jpg"], check=True)
            b = subprocess.run(["node", "tools/ig_queue.js", "carousel", out], capture_output=True, text=True, timeout=900)
            log(f"{slug} from {os.path.basename(d)} ({likes} likes) → {b.stdout.strip() or b.stderr.strip()[:120]}"); made += 1
        except Exception as e: log(f"{slug}: failed ({str(e)[:120]})")
    print(f"made {made}")


if __name__ == "__main__":
    main()
