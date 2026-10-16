"""Final clip pick from the judges' verdicts (owner 10-14: meaning first, Zoltium style, never the same clip twice).
Usage: python3 tools/clippick.py <reel_dir>
Reads clips/sheets/index.json (tools/clipsheet.py) + clips/judge/NN.json written by the Haiku judges:
  {"clips": {"A": {"shows": "...", "meaning": 0-10, "style": 0-10, "text": true|false}, ...}, "better_query": "..."}
Score = meaning (counts most) + 0.4 x judged style + 0.3 x judged quality (owner 10-14: "good quality and good looking"); meaning < 5 or judged style < 5 is never used; text/watermarks cost 3 points.
Best (line, clip) match is assigned first across the reel, and a pin used once is gone for the rest of the reel —
and (10-16) for the next 30 reels too (library/clip-usage.json).
Writes clips/pick.json (the format tools/clipcut.py reads) and lists weak lines with the judge's better search phrase."""
import json, os, sys

R = os.path.abspath(sys.argv[1]); idx = json.load(open(f"{R}/clips/sheets/index.json"))
opts, weak = {}, []
for nn, e in idx.items():
    jf = f"{R}/clips/judge/{nn}.json"
    j = json.load(open(jf)) if os.path.exists(jf) else {"clips": {}}
    ok = []
    for letter, c in e["clips"].items():
        v = j["clips"].get(letter)
        if not v or v.get("meaning", 0) < 5 or v.get("style", 0) < 5 or v.get("quality", 10) < 6: continue   # off-line, live action / 3D, or cheap-looking
        if v.get("text") or not os.path.exists(f"{R}/clips/cand/{c['file']}"): continue   # 10-16 owner: NO clips with baked-in text, ever; a removed file can't be picked
        # on-screen text costs 3 points (watermarks lose to clean clips) but is not banned: a chat bubble can BE the line
        ok.append((v["meaning"] + 0.4 * v.get("style", 5) + 0.3 * v.get("quality", 6) + c["style"] - (3 if v.get("text") else 0), letter, c, v))
    ok.sort(key=lambda r: -r[0]); opts[nn] = ok
    if not ok or ok[0][3]["meaning"] < 7: weak.append((nn, e["say"], j.get("better_query", "")))
# 10-16 owner: "1000+ clips but the same ones in every reel" — a pin used in any of the last 30 reels is off-limits (cross-reel
# memory in library/clip-usage.json, synced to Drive). Only if a line has nothing else does a recent pin come back (last pass).
USAGE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "library", "clip-usage.json")
usage = json.load(open(USAGE)) if os.path.exists(USAGE) else {"reels": []}   # [{"reel": slug, "pins": [...]}] newest last
me = os.path.basename(R)
recent = {p for u in usage["reels"][-30:] if u["reel"] != me for p in u["pins"]}
pick, used = {}, set(recent)
for nn, e in idx.items():   # an editor's choice ("force": "E" in the judge file) is placed first and wins its pin
    jf = f"{R}/clips/judge/{nn}.json"; f_ = json.load(open(jf)).get("force") if os.path.exists(jf) else None
    if f_ and f_ in e["clips"]:
        c = e["clips"][f_]; v = json.load(open(jf))["clips"].get(f_, {"meaning": 0, "shows": ""}); used.add(c["pin"])
        pick[str(int(nn))] = {"file": c["file"], "start": c["start"], "style": c["style"], "meaning": v.get("meaning", 0), "shows": v.get("shows", "") + "  [editor]", "q": e["q"]}
# best match first across the whole reel: a clip goes to the line it fits BEST (a 7/10 for one line beats a 5/10 elsewhere)
for sc, nn, letter, c, v in sorted(((r[0], nn) + r[1:] for nn, rows in opts.items() for r in rows), key=lambda r: -r[0]):
    if str(int(nn)) in pick or c["pin"] in used: continue
    used.add(c["pin"])
    pick[str(int(nn))] = {"file": c["file"], "start": c["start"], "style": c["style"], "meaning": v["meaning"], "shows": v["shows"], "q": idx[nn]["q"]}
# fallback (owner 10-14: "make it faster"): a shot with nothing that clears every bar takes the best clip that still SHOWS the line
# in our style (meaning ≥ 4, style ≥ 5, quality ≥ 4, no text), flagged weak so a later search can replace it
for nn, e in idx.items():
    if str(int(nn)) in pick: continue
    jf = f"{R}/clips/judge/{nn}.json"; j = json.load(open(jf))["clips"] if os.path.exists(jf) else {}
    rows = sorted(((v["meaning"] + 0.4 * v.get("style", 5) + 0.3 * v.get("quality", 5), c, v) for L, c in e["clips"].items() if (v := j.get(L))
                   and v.get("meaning", 0) >= 4 and v.get("style", 0) >= 5 and v.get("quality", 0) >= 4 and not v.get("text") and os.path.exists(f"{R}/clips/cand/{c['file']}") and c["pin"] not in used), key=lambda r: -r[0])
    if rows:
        sc, c, v = rows[0]; used.add(c["pin"])
        pick[str(int(nn))] = {"file": c["file"], "start": c["start"], "style": c["style"], "meaning": v["meaning"], "shows": v["shows"] + "  [fallback]", "q": idx[nn]["q"]}
# 10-15: the OPENING shot can't continue a previous clip and an empty one stops the render, so it takes the best-looking clean clip it has
for nn, e in idx.items():
    if int(nn) != 0 or "0" in pick: continue
    jf = f"{R}/clips/judge/{nn}.json"; j = json.load(open(jf))["clips"] if os.path.exists(jf) else {}
    rows = sorted(((v.get("meaning", 0) + 0.4 * v.get("style", 5), c, v) for L, c in e["clips"].items() if (v := j.get(L))
                   and v.get("style", 0) >= 5 and not v.get("text") and os.path.exists(f"{R}/clips/cand/{c['file']}") and c["pin"] not in used), key=lambda r: -r[0])
    if rows:
        sc, c, v = rows[0]; used.add(c["pin"])
        pick["0"] = {"file": c["file"], "start": c["start"], "style": c["style"], "meaning": v.get("meaning", 0), "shows": v.get("shows", "") + "  [fallback]", "q": e["q"]}
# last pass: a line still empty may reuse a recent pin rather than hold the previous shot for too long
for nn, rows in opts.items():
    if str(int(nn)) in pick: continue
    for sc, letter, c, v in rows:
        if c["pin"] in recent and c["pin"] not in {p_["file"] for p_ in pick.values()}:
            pick[str(int(nn))] = {"file": c["file"], "start": c["start"], "style": c["style"], "meaning": v["meaning"], "shows": v["shows"] + "  [reused: nothing new fit]", "q": idx[nn]["q"]}
            break
json.dump(pick, open(f"{R}/clips/pick.json", "w"), indent=1, ensure_ascii=False)
pins = sorted({c["pin"] for nn, e in idx.items() for L, c in e["clips"].items() if c["file"] in {p_["file"] for p_ in pick.values()}})
usage["reels"] = [u for u in usage["reels"] if u["reel"] != me] + [{"reel": me, "pins": pins}]
json.dump(usage, open(USAGE + ".part", "w")); os.replace(USAGE + ".part", USAGE)
for nn in sorted(idx):
    p = pick.get(str(int(nn)))
    print(f"line {nn}: {('meaning ' + str(p['meaning']) + '  ' + p['shows']) if p else 'NO CLIP (black hold)'}   <- {idx[nn]['say']}")
for nn, say, q in weak: print(f"WEAK {nn}: {say!r}  try: {q!r}")
