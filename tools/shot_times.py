"""Re-time a clip reel's shots after the voice changes: each shot in <reel>/shots.json starts on the first word of its
"say" phrase, read from the aligned assets/timing.js. The OUTRO shot ("And follow for more.") is timed the same way.
Usage: python3 tools/shot_times.py <reel_dir>      (run after reel_timing.py + align_words.py, before clipcut.py)"""
import json, os, re, sys

R = os.path.abspath(sys.argv[1]); s = open(f"{R}/assets/timing.js").read(); T = json.loads(s[s.index("{"):s.rindex("}") + 1])
shots = json.load(open(f"{R}/shots.json"))
norm = lambda w: re.sub(r"[^a-z0-9']", "", w.lower())
W = [(norm(w), a) for line in T["words"] for w, a, b in line]
i = 0
for sh in shots:
    first = [norm(w) for w in sh["say"].split()][:2]
    j = next((k for k in range(i, len(W)) if W[k][0] == first[0] and (len(first) < 2 or k + 1 >= len(W) or W[k + 1][0] == first[1])), None)
    if j is None and sh.get("q") == "OUTRO" and T["words"]:   # 10-15: the OUTRO always times to the LAST spoken line (the brand tagline),
        j = next(k for k in range(len(W)) if W[k][1] == T["words"][-1][0][1])   # even if the plan still says an old CTA
    if j is None: sys.exit(f"shot not found in the voice: {sh['say']!r}")
    sh["t"] = round(W[j][1], 2); i = j + 1
json.dump(shots, open(f"{R}/shots.json", "w"), indent=1, ensure_ascii=False)
print(" ".join(f"{sh['t']}" for sh in shots))
# keep the composition in step: the outro (logo bust) starts 0.18 s before "And follow for more.", the clip film ends there
o = next((sh["t"] for sh in shots if sh["q"] == "OUTRO"), None); H = f"{R}/index.html"
if o is not None and os.path.exists(H):
    end = round(o - 0.18, 2); h = open(H).read()
    h = re.sub(r'(id="outro"[^>]*data-start=")[\d.]+', rf"\g<1>{end}", h)
    h = re.sub(r'(id="bg"[^>]*data-duration=")[\d.]+', rf"\g<1>{o}", h)
    h = re.sub(r"END = [\d.]+;", f"END = {end};", h)
    h = re.sub(r'(id="root"[^>]*data-duration=")[\d.]+', rf"\g<1>{T['total']}", h); h = re.sub(r"tl\.set\(\{\}, \{\}, [\d.]+\)", f"tl.set({{}}, {{}}, {T['total']})", h)
    open(H, "w").write(h); print(f"outro at {end}")
