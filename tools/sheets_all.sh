#!/usr/bin/env bash
# Build contact sheets (with the pool-wide search) for every reel of a batch that has no judgements yet.
# The first reel runs alone so the pool fingerprints (reels/_pool/emb.json) are computed once; the rest run 3 at a time.
# Usage: tools/sheets_all.sh reels/w2-batch.json [skip-reel ...]
cd "$(dirname "$0")/.."; B="$1"; shift
mapfile -t todo < <(python3 - "$B" "$@" <<'PY'
import json, glob, os, sys
skip = set(sys.argv[2:])
for r in json.load(open(sys.argv[1])):
    if os.path.basename(r) in skip or glob.glob(f"{r}/clips/judge/*.json"): continue
    if os.path.exists(r + "/shots.json") and os.path.exists(r + "/assets/timing.js") and glob.glob(f"{r}/clips/cand/00/*.mp4"): print(r)
PY
)
[ ${#todo[@]} -eq 0 ] && exit 0
tools/reel_prep.sh "${todo[0]}" >/dev/null 2>&1; echo "sheets ready: ${todo[0]}"
printf '%s\n' "${todo[@]:1}" | xargs -P 3 -I{} sh -c 'tools/reel_prep.sh {} >/dev/null 2>&1; echo "sheets ready: {}"'
