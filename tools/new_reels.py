"""Create clip reels from an approved script file (owner 10-14: build the week fast, in the v1 recipe — brain/pipeline.md).
Usage: python3 tools/new_reels.py brain/content/drafts/week2-scripts.md w2
Each "## NN · Topic · "Title"" section becomes reels/<prefix>-NN-<slug>/ with:
  assets/vo/script.json — lines with DELIVERY marks (brain/research/narration-emphasis.md): the hook a little more expressive, the WHY
    line and the motivational close heavier (exaggeration up, cfg down), fragments < 20 characters merged into the next line
    (Chatterbox garbles very short generations), "Follow for more." always its own line;
  reel.json — gaps (real pauses before the turn, the close and the CTA), the reveal ("drops") on the WHY line, speed 1.07, music auto;
  index.html + assets/brand from the v1 reference build (reels/p1c-hookb), with this reel's accent words and reveal filled in later."""
import json, os, re, shutil, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); REF = os.path.join(ROOT, "reels/p1c-hookb")
src, prefix = sys.argv[1], sys.argv[2]
text = open(os.path.join(ROOT, src)).read()
TURN = re.compile(r"^(but )?here'?s (what|the|why|the part|the thing)", re.I)
made = []
for m in re.finditer(r"^## (\d+) · ([^·\n]+?) · \"([^\"]+)\"\n(.*?)(?=^## |\Z)", text, re.S | re.M):
    num, topic, title, body = m.group(1), m.group(2).strip(), m.group(3), m.group(4)
    raw = [l.strip() for l in body.strip().splitlines() if l.strip() and not l.startswith("---")]
    lines = []
    for l in raw:   # merge fragments under 20 characters into the NEXT line (except the CTA)
        if lines and isinstance(lines[-1], str) and len(lines[-1]) < 20 and l != "Follow for more.":
            lines[-1] = lines[-1] + " " + l
        else: lines.append(l)
    if lines[-1] != "Follow for more.": sys.exit(f"{num}: last line must be 'Follow for more.'")
    n = len(lines); turn = next((i for i, l in enumerate(lines) if TURN.match(l)), max(2, n // 2 - 1))
    why = min(turn + 1, n - 3); close = n - 2
    script = []
    for i, l in enumerate(lines):
        if i == 0: script.append({"text": l, "ex": 0.62, "cfg": 0.42})                 # hook: a touch more alive
        elif i in (why, close): script.append({"text": l, "ex": 0.68, "cfg": 0.32})     # punch lines: emotion + weight
        else: script.append(l)
    gaps = [0.15] * n
    gaps[turn - 1] = 0.4; gaps[close - 1] = 0.35; gaps[n - 2] = 0.55; gaps[n - 1] = 0
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:24]
    R = os.path.join(ROOT, "reels", f"{prefix}-{num}-{slug}")
    os.makedirs(f"{R}/assets/vo", exist_ok=True); os.makedirs(f"{R}/assets/audio", exist_ok=True)
    json.dump(script, open(f"{R}/assets/vo/script.json", "w"), indent=1, ensure_ascii=False)
    json.dump({"gaps": gaps, "tail": 2.6, "lead": 0.08, "music": "auto", "drops": [why], "ctaLine": n - 1, "speed": 1.07,
               "topic": topic, "title": title, "accent": []}, open(f"{R}/reel.json", "w"), indent=1, ensure_ascii=False)
    shutil.copy(f"{REF}/index.html", f"{R}/index.html")
    if not os.path.exists(f"{R}/assets/brand"): shutil.copytree(f"{REF}/assets/brand", f"{R}/assets/brand")
    made.append(os.path.relpath(R, ROOT)); print(f"{made[-1]}: {n} lines, turn {turn + 1}, reveal on line {why + 1}")
json.dump(made, open(os.path.join(ROOT, f"reels/{prefix}-batch.json"), "w"), indent=1)
