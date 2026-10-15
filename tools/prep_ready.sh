#!/usr/bin/env bash
# Contact sheets for every reel in a batch that is ready: voice timed + clips for its shots (one missing shot is fine — it
# continues the previous clip). Runs 3 reels at a time. Usage: tools/prep_ready.sh reels/w2-batch.json [skip-reel ...]
cd "$(dirname "$0")/.."; B="$1"; shift
ready=$(python3 - "$B" "$@" <<'PY'
import json, glob, os, sys
skip = set(sys.argv[2:])
for r in json.load(open(sys.argv[1])):
    if os.path.basename(r) in skip or glob.glob(f"{r}/clips/judge/*.json") or not (os.path.exists(r + "/shots.json") and os.path.exists(r + "/assets/timing.js")): continue
    S = json.load(open(r + "/shots.json")); need = [n for n, s in enumerate(S) if s["q"] != "OUTRO"]
    have = sum(1 for n in need if glob.glob(f"{r}/clips/cand/{n:02d}/*.mp4"))
    if have >= len(need) - 1 and glob.glob(f"{r}/clips/cand/00/*.mp4"): print(r)
PY
)
echo "$ready" | xargs -P 3 -I{} sh -c 'tools/reel_prep.sh {} >/dev/null 2>&1; echo "sheets ready: {}"'
