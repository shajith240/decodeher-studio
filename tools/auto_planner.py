"""Automatic reel planner (owner 10-26: the page went 3 days without a reel because nobody wrote the next batch).
Daily: if fewer than --min-days of reels are booked or in production (3 a day), write the next batch of 6 at 95/5:
  sources = tools/pick_sources.py (owner shares first, then the viral bank ≥1M, Dark Needle only when the bank is empty)
  Claude (Sonnet) writes the draft in the exact format of the newest brain/content/drafts/viral*-scripts.md, following
  brain/growth/content-rules.md; it skips skits / street interviews / creator advice / broken transcripts.
  tools/new_reels_v3.py turns it into reels (it also picks each AI-woman opener); the factory makes and books them.
Usage: python3 tools/auto_planner.py [--min-days 4] [--n 6]      (run daily by the decodeher-planner timer)"""
import argparse, glob, json, os, re, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
log = lambda m: open("logs/activity.log", "a").write(f"{time.strftime('%H:%M:%S')}  Planner · {m}\n")


def reels_ahead():
    out = subprocess.run(["node", "tools/ig_queue.js", "ids"], capture_output=True, text=True).stdout
    booked = sum(1 for l in out.splitlines() if " queued " in f" {l} " and not l.startswith("c-"))
    making = 0
    for b in glob.glob("reels/*-batch.json"):
        for r in json.load(open(b)):
            slug = os.path.basename(r); cfg = json.load(open(f"{r}/reel.json")) if os.path.exists(f"{r}/reel.json") else {}
            if not os.path.exists(f"logs/queued/{slug}") and not cfg.get("parked"): making += 1
    return booked, making


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--min-days", type=float, default=4); ap.add_argument("--n", type=int, default=6)
    a = ap.parse_args()
    booked, making = reels_ahead()
    if booked + making >= a.min_days * 3: return print(f"{booked} booked + {making} in production: enough")
    srcs = [json.loads(l) for l in subprocess.run([sys.executable, "tools/pick_sources.py", str(a.n * 2)], capture_output=True, text=True).stdout.splitlines() if l.strip()]
    if not srcs: log("no sources left"); return
    drafts = sorted(glob.glob("brain/content/drafts/viral*-scripts.md"), key=lambda p: int(re.search(r"viral(\d+)", p).group(1)))
    last = drafts[-1]; k = int(re.search(r"viral(\d+)", last).group(1)) + 1
    series = max(int(x) for x in re.findall(r"Dark psychology #(\d+)", "".join(open(d).read() for d in drafts))) + 1
    out = f"brain/content/drafts/viral{k}-scripts.md"
    src_txt = "\n\n".join(f"SOURCE {i} | {s['source']} | {s.get('by')} | {s.get('views')} views | {s['url']}\nTITLE: {s.get('title')}\nTRANSCRIPT: {s['text'][:2500]}"
                          for i, s in enumerate(srcs))
    prompt = f"""You write reel scripts for @thedecodeher (faceless dating psychology for men, narrated by an AI voice).
Read {os.path.join(ROOT, last)} (the exact format to copy) and {os.path.join(ROOT, 'brain/growth/content-rules.md')} (rules to follow).
From the sources below, pick the best {a.n} that are a single narratable message for men (SKIP skits, street interviews, dialogues,
advice for creators, off-niche topics, and broken / garbled / cut-off transcripts). Owner sources (source = owner) come first if usable.
For each, write a reel at 95/5: same hook, same points in the same order, same examples, similar length — reworded sentence by
sentence, never word for word, translated to plain English if needed. Ours: "Listen." right after the hook sentence (no pause),
and our closing line ("[lower voice] Save this …" or "[lower voice] Send this to the friend who …"). HARD LIMIT 85 spoken words
(about 30 s; 10-27 data: longer reels die at ~120 views); if a source is longer, keep its hook and strongest 3 points in order. No texting slang (lol, haha).
Number the sections 01..{a.n:02d}, series "Dark psychology #{series}" upward, each with the <!-- source: … --> line (creator, views, url),
a <!-- keyword: … --> line and the "## NN meta" block exactly like the example.
Write the file {os.path.join(ROOT, out)}. Then reply with one line per reel: "<url>" only.

{src_txt}"""
    r = subprocess.run([os.environ.get("CLAUDE_BIN", "claude"), "-p", prompt, "--model", "sonnet", "--allowedTools", "Read", "Write",
                        "--output-format", "text"], capture_output=True, text=True, timeout=1800)
    if not os.path.exists(out): log(f"no draft written ({(r.stdout or r.stderr)[-160:]})"); return
    used = re.findall(r"<!-- source:[^>]*?(https?://[^\s)]+)", open(out).read())   # the draft's own source lines (the reply format varies)
    pol = subprocess.run([sys.executable, "tools/script_polish.py", out], capture_output=True, text=True, timeout=2000)   # 10-26: narration editor, mandatory
    if pol.returncode != 0: log(f"draft v{k} not voiced: narration editor failed ({(pol.stdout + pol.stderr)[-160:]})"); return
    mk = subprocess.run([sys.executable, "tools/new_reels_v3.py", out, f"v{k}"], capture_output=True, text=True, timeout=1800)
    if mk.returncode != 0: log(f"batch v{k} failed: {mk.stderr[-200:]}"); return
    marks = [f"{u.rstrip('.,)')}=v{k}" for u in used if any(u.rstrip('.,)') == s["url"] for s in srcs)]
    if marks: subprocess.run([sys.executable, "tools/pick_sources.py", "--mark", *marks])
    log(f"batch v{k} written ({len(marks)} sources) — {booked} booked + {making} in production before it")
    print(mk.stdout[-600:])


if __name__ == "__main__":
    main()
