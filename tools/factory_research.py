"""Factory step: the automatic second clip search for a reel whose judges found too many weak shots (owner 10-14: "automate it").
Usage: python3 tools/factory_research.py reels/<reel> 3,7,9
1. Claude (headless, Haiku) writes a sharper, concrete Pinterest phrase for each weak shot from its words + what the judges saw.
2. tools/pinfetch.py searches those shots again (adding to what is there), 3. their contact sheets are rebuilt,
4. their old verdicts are deleted, so the factory judges them again. The factory then marks the reel clip_round 2 (no third round)."""
import json, os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
R, weak = sys.argv[1], [int(x) for x in sys.argv[2].split(",") if x]
S = json.load(open(f"{R}/shots.json"))
rows = []
for n in weak:
    j = json.load(open(f"{R}/clips/judge/{n:02d}.json")) if os.path.exists(f"{R}/clips/judge/{n:02d}.json") else {"clips": {}}
    seen = "; ".join(v.get("shows", "") for v in list(j["clips"].values())[:4])
    rows.append(f'{n} | words: "{S[n]["say"]}" | old search: "{S[n]["q"]}" | judges only found: {seen}')
prompt = ("For each shot below of an Instagram reel (dating psychology for men, 2D cartoon clips), write ONE new Pinterest search phrase "
          "(3-6 plain words, a concrete 2D cartoon scene of people doing something visible, gender right: I/you = man, she = woman, "
          "no abstract words, different from the old search). Reply with ONLY a JSON object mapping the shot number to the phrase, "
          'e.g. {"3": "nervous man sweating explaining"}.\n\n' + "\n".join(rows))
out = subprocess.run(["claude", "-p", prompt, "--model", "haiku", "--output-format", "text"], capture_output=True, text=True, timeout=600, stdin=subprocess.DEVNULL).stdout
if "{" not in out: sys.exit("claude gave no JSON: " + out.strip()[:300])   # 10-15: show Claude's message ("session limit"...) in the log so factory.py pauses instead of parking
new = json.loads(out[out.index("{"):out.rindex("}") + 1])
for k, q in new.items():
    if int(k) in weak and q.strip(): S[int(k)]["q"] = q.strip().lower()
json.dump(S, open(f"{R}/shots.json", "w"), indent=1, ensure_ascii=False)
print("new searches:", new, flush=True)
lines = ",".join(str(n) for n in weak)
env = dict(os.environ, LINES=lines, PLAIN="1")   # 10-19: plain "<scene> animation" search for the weak lines
subprocess.run(["uv", "run", "-q", "--with", "gallery-dl", "--with", "yt-dlp", "--with", "secretstorage", "python", "tools/pinfetch.py", R, "10"], env=env, check=True)
subprocess.run(["uv", "run", "-q", "--python", "3.11", "--with", "transformers", "--with", "torch", "--with", "pillow", "python", "-W", "ignore",
                "tools/clipsheet.py", R], env=dict(env, HF_HUB_OFFLINE="1"), check=True)
for n in weak:
    p = f"{R}/clips/judge/{n:02d}.json"
    if os.path.exists(p): os.remove(p)
print("re-searched shots", lines)
