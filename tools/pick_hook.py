"""Pick the AI-woman opening clip that MATCHES the reel's first spoken line (owner 10-16: "the starting line should align with the
hook so the viewer relates to what he's watching — but don't change the template").
Usage: python3 tools/pick_hook.py reels/<reel> [--force]       (skips a reel that already has reel.json "hookSrc" unless --force)
Pool: library/hook-pool/ai/*.mp4. Each clip gets an AI description once (tools/pin_intake.describe, cached in its .json as
ai_description + tags). One cheap Haiku call ranks the pool against the first line; clips used as an opener in the last 12 reels
are skipped. Writes reels/<reel>/clips/hook/hook.mp4 and reel.json hookClip {file, start} + hookSrc (the pool file)."""
import glob, json, os, re, shutil, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
R = sys.argv[1].rstrip("/"); FORCE = "--force" in sys.argv
cfg = json.load(open(f"{R}/reel.json"))
if cfg.get("hookSrc") and not FORCE: sys.exit(0)
script = json.load(open(f"{R}/assets/vo/script.json"))
first = re.sub(r"\[[^\]]*\]\s*", "", script[0]["text"] if isinstance(script[0], dict) else script[0]).strip()

import importlib.util
spec = importlib.util.spec_from_file_location("pin_intake", os.path.join(ROOT, "tools", "pin_intake.py"))
pi = importlib.util.module_from_spec(spec); sys.argv = [sys.argv[0], "none"]; spec.loader.exec_module(pi)

pool = []
for mp4 in sorted(glob.glob("library/hook-pool/ai/*.mp4")):
    js = mp4[:-4] + ".json"; meta = json.load(open(js)) if os.path.exists(js) else {}
    if not meta.get("ai_description"):
        d = pi.describe(mp4, "hook")
        if d: meta.update({"ai_description": d["description"], "tags": d["tags"]}); json.dump(meta, open(js, "w"), indent=1, ensure_ascii=False)
    pool.append((mp4, meta.get("ai_description", ""), meta.get("tags", [])))
recent = []
for rj in sorted(glob.glob("reels/*/reel.json"), key=os.path.getmtime)[-13:]:
    if os.path.dirname(rj) != R:
        src = (json.load(open(rj)) or {}).get("hookSrc")
        if src: recent.append(src)
cands = [p for p in pool if p[0] not in recent and p[1]] or [p for p in pool if p[1]] or pool
listing = "\n".join(f"{i}: {d} [{', '.join(t)}]" for i, (_, d, t) in enumerate(cands))
prompt = (f"A dating-psychology reel opens on a short clip of a woman while the narrator says: \"{first}\"\n"
          f"Pick the clip whose expression, action and mood best MATCH that line, so the viewer instantly relates (e.g. a line about "
          f"her texting -> a woman with or near a phone; ignoring -> looking away; teasing -> a playful smirk).\nClips:\n{listing}\n"
          'Answer with JSON only: {"pick": <number>, "why": "a few words"}')
choice, why = 0, "first available"
try:
    out = subprocess.run([os.environ.get("CLAUDE_BIN", "claude"), "-p", prompt, "--model", "haiku", "--output-format", "text"],
                         capture_output=True, text=True, timeout=120).stdout
    m = re.search(r"\{.*\}", out, re.S); j = json.loads(m.group(0)) if m else {}
    if isinstance(j.get("pick"), int) and 0 <= j["pick"] < len(cands): choice, why = j["pick"], j.get("why", "")
except Exception: pass
src = cands[choice][0]
os.makedirs(f"{R}/clips/hook", exist_ok=True); shutil.copy(src, f"{R}/clips/hook/hook.mp4")
cfg = json.load(open(f"{R}/reel.json")); cfg["hookClip"] = {"file": "clips/hook/hook.mp4", "start": 0.3}; cfg["hookSrc"] = src
json.dump(cfg, open(f"{R}/reel.json", "w"), indent=1, ensure_ascii=False)
print(f"{os.path.basename(R)}: \"{first[:60]}\" -> {os.path.basename(src)} ({why})")
