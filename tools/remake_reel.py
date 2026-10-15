"""Re-make a finished reel with the approved voice v2 and the brand ending (owner 10-15: "follow for more" sounds like begging —
end like Zoltium: the narrator says the name while the logo forms). Same script, same clips, same edit; the factory then re-runs
voice → mix → render → queue, and queue_reel.sh swaps the new video into the reel's EXISTING slot (reel.json "requeue").
Usage: python3 tools/remake_reel.py reels/<reel> "TITLE CARD TEXT"      (old voice timing kept under <reel>/v1/; the old master is deleted)"""
import json, os, shutil, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
R, card = sys.argv[1].rstrip("/"), (sys.argv[2] if len(sys.argv) > 2 else "")
slug, END = os.path.basename(R), json.load(open("config.json")).get("reels", {}).get("tagline", "Decode her.")   # owner 10-15: the fixed spoken tagline
j = lambda p: json.load(open(p))
def put(p, d): json.dump(d, open(p, "w"), indent=1, ensure_ascii=False)

# 1. the last spoken line becomes the brand name (script, and the OUTRO shot that times the logo to it)
script = j(f"{R}/assets/vo/script.json")
last = script[-1]["text"] if isinstance(script[-1], dict) else script[-1]
if "follow" in last.lower() or last.strip() in ("Decode her.", "Decode her") and last != END:
    script[-1] = {**script[-1], "text": END} if isinstance(script[-1], dict) else END
    put(f"{R}/assets/vo/script.json", script)
shots = j(f"{R}/shots.json")
for s in shots:
    if s["q"] == "OUTRO": s["say"] = END
put(f"{R}/shots.json", shots)

# 2. reel settings: voice v2, title card, and "swap into the slot it already has"
cfg = j(f"{R}/reel.json"); cfg["tail"] = 0.6; cfg["voice_chain"] = 2; cfg["requeue"] = True; cfg["clip_round"] = max(2, cfg.get("clip_round", 1))   # keep the footage: no new clip search; tail 0.6 = the reel ends with the 3.9 s bronze outro
if card: cfg["titleCard"] = card
put(f"{R}/reel.json", cfg)

# 3. no "FOLLOW FOR MORE" text on screen (fill_page.py also strips it from every new page)
H = f"{R}/index.html"; h = open(H).read().replace('<div id="title"><b>FOLLOW</b> FOR MORE</div>', '<div id="title"></div>'); open(H, "w").write(h)

# 4. make the factory redo voice → mix → render → queue: move the old outputs aside (never delete)
bk = f"{R}/v1"; os.makedirs(bk, exist_ok=True)
for f in ("assets/timing.js", "assets/audio/final.wav"):
    if os.path.exists(f"{R}/{f}"): shutil.move(f"{R}/{f}", f"{bk}/{os.path.basename(f)}")
vid = f"deliverables/week-2/{slug}.mp4"
if os.path.exists(vid): os.remove(vid)   # owner: replace the old reels (a 300 MB master each; the disk is tight)
if os.path.exists(f"logs/queued/{slug}"): os.remove(f"logs/queued/{slug}")
print(f"{slug}: ending '{END}', voice v2, title card {card or cfg.get('titleCard') or 'none'} — the factory takes it from here")
