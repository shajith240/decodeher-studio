"""Where the SNAP and the LAUGH go (owner 10-16: "snaps only at the peak points, according to the explanation — the agent should
understand the psychology of narration"; "laughs only according to the context, not random").
Usage: python3 tools/peak_points.py reels/<reel> [--force]
Reads assets/vo/script.json, asks Claude (Haiku, cheap) which LINES carry the narration's peaks, writes reel.json
"snaps": [line, ...] (2-4, at the START of the line) and "laughs": [line] or [] (after the END of the line).
tools/reel_mix.py places only these (in sfxSet mode it drops every other snap/sting cue). Skips a reel that already has "snaps"."""
import json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); R = os.path.abspath(sys.argv[1])
cfg_p = f"{R}/reel.json"; cfg = json.load(open(cfg_p))
if "snaps" in cfg and "--force" not in sys.argv: sys.exit(0)
TAG = re.compile(r"\[[^\]]*\]\s*")
lines = [TAG.sub("", x["text"] if isinstance(x, dict) else x).strip() for x in json.load(open(f"{R}/assets/vo/script.json"))]
numbered = "\n".join(f"{i}: {l}" for i, l in enumerate(lines))
prompt = f"""You are the sound editor of a dark-psychology Instagram reel. A SNAP is a sharp finger-snap hit that resets attention.
It only works if it is RARE, so place 2 to 4 snaps, at the START of the lines where the narration PEAKS:
- the line right after the hook ends (the moment the viewer is pulled in, e.g. after "Listen carefully")
- the line that names the psychology (the reveal of the term or mechanism)
- the punchline / verdict line (e.g. "It's not love. It's a loop.")
- the turn to the solution (e.g. "Here's how you break it.")
Never snap on line 0, never on two consecutive lines, never on the last line, never on calm explanation lines.
An evil LAUGH is only allowed after a line that is itself dark, mocking or describes someone winning a manipulation game.
Most reels have NO laugh. When in doubt, no laugh.

Script lines (index: text):
{numbered}

Answer with JSON only: {{"snaps": [line indexes], "laughs": [line indexes], "why": "one short sentence"}}"""
try:
    out = subprocess.run([os.environ.get("CLAUDE_BIN", "claude"), "-p", prompt, "--model", "haiku", "--output-format", "text"],
                         capture_output=True, text=True, timeout=180).stdout
except (subprocess.TimeoutExpired, OSError): out = ""   # 10-16: a slow or capped Claude crashed the render — fall back to the safe snap below
m = re.search(r"\{.*\}", out, re.S)
try: ans = json.loads(m.group(0)) if m else {}
except json.JSONDecodeError: ans = {}
n = len(lines)
snaps = sorted({int(i) for i in ans.get("snaps", []) if str(i).lstrip("-").isdigit() and 0 < int(i) < n - 1})
snaps = [i for k, i in enumerate(snaps) if k == 0 or i - snaps[k - 1] > 1][:4]
laughs = [int(i) for i in ans.get("laughs", []) if str(i).isdigit() and 0 <= int(i) < n][:1]
if not snaps: snaps = [1]   # fallback: at least the hook-end snap
cfg = json.load(open(cfg_p)); cfg["snaps"], cfg["laughs"] = snaps, laughs
json.dump(cfg, open(cfg_p, "w"), indent=1, ensure_ascii=False)
print(f"snaps on lines {snaps}, laughs {laughs or 'none'} — {ans.get('why', '')}")
