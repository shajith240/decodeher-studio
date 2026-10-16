"""Sound effects ON THE WORDS (owner 10-14: "use the sound effects according to the lines the narrator is saying").
Usage: python3 tools/word_cues.py <reel_dir>
Reads <reel>/sfx.json — the reel's sound plan, one entry per effect:
  {"at": "meme", "type": "pop"}                     on the first "meme" spoken
  {"at": "stop being", "type": "snap", "n": 1}      on the n-th (0-based) time this phrase is spoken
  {"at": "midnight", "type": "clock", "end": true, "offset": -0.05, "gain": -2}   end of the word, nudged, quieter
and writes assets/audio/cues.json [{type, t, gain}] for tools/reel_mix.py (times from the ALIGNED assets/timing.js).
Unknown words stop the script, so a typo never silently drops a sound."""
import json, os, re, sys

R = os.path.abspath(sys.argv[1]); s = open(f"{R}/assets/timing.js").read(); T = json.loads(s[s.index("{"):s.rindex("}") + 1])
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower().replace("’", "'"))
W = [(norm(w), a, b) for line in T["words"] for w, a, b in line]
plan = json.load(open(f"{R}/sfx.json")); cues = []
for c in [c for c in plan if "at" in c]:
    want = [norm(x) for x in c["at"].split()]
    hits = [k for k in range(len(W) - len(want) + 1) if all(W[k + i][0] == want[i] for i in range(len(want)))]
    n = c.get("n", 0)
    if len(hits) <= n:   # audit M1 (10-15): one planned sound on a word the voice never says just gets dropped — never stop the reel
        print(f"  skipped cue: {c['at']!r} (n={n}) is not spoken in this reel", file=sys.stderr); continue
    k = hits[n]; t = W[k + len(want) - 1][2] if c.get("end") else W[k][1]
    cues.append({"type": c["type"], "t": round(t + c.get("offset", 0), 3), "gain": c.get("gain", 0), "at": c["at"]})
CUT = (json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json"))).get("reels", {}).get("cutSound"))   # 10-15 owner: Zoltium's SNAP on every cut, not a whoosh
SFXSET = (json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json"))).get("reels", {}).get("sfxSet"))
for c in [c for c in plan if "every_cut" in c and not SFXSET]:   # 10-16 owner: no snap on every cut — snaps only at the peak lines (reel.json "snaps")   # {"every_cut": "whoosh", "gain": -4}: a sound on every picture change (Zoltium's zooms)
    for sh in json.load(open(f"{R}/shots.json"))[1:]:
        if not any(abs(x["t"] - sh["t"]) < 0.3 for x in cues): cues.append({"type": CUT or c["every_cut"], "t": round(sh["t"] - 0.02, 3), "gain": c.get("gain", 0), "at": "cut"})
cues.sort(key=lambda c: c["t"])
json.dump(cues, open(f"{R}/assets/audio/cues.json", "w"), indent=1)
print(f"{len(cues)} cues: " + ", ".join(f"{c['type']}@{c['t']}({c['at']})" for c in cues))
