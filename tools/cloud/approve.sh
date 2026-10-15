#!/usr/bin/env bash
# Owner tapped Approve on a preview: swap it into the reel's EXISTING post slot through tools/queue_reel.sh's requeue path
# (same caption, same slot; a reel not booked yet is booked normally; a reel already posted is left alone).
# Usage: tools/cloud/approve.sh <slug>      Needs deliverables/preview/<slug>.mp4 (rendered by manager-request, synced via Drive).
set -euo pipefail
cd "$(dirname "$0")/../.."
slug="${1:-}"; [[ "$slug" =~ ^[a-z0-9][a-z0-9-]{2,80}$ ]] && [ -d "reels/$slug" ] || { echo "no such reel: '$slug'" >&2; exit 2; }
P="deliverables/preview/$slug.mp4"; M="deliverables/week-2/$slug.mp4"
[ -s "$P" ] || { echo "no preview for $slug ($P)" >&2; exit 1; }
ffprobe -v error -show_entries format=duration -of csv=p=0 "$P" | grep -q . || { echo "preview does not decode: $P" >&2; exit 1; }
mkdir -p deliverables/week-2; cp -f "$P" "$M.part"; mv -f "$M.part" "$M"           # the master queue_reel.sh encodes from
python3 -c "import json,sys; p=sys.argv[1]; c=json.load(open(p)); c['requeue']=True; json.dump(c,open(p,'w'),indent=1,ensure_ascii=False)" "reels/$slug/reel.json"
rm -f "logs/queued/$slug"                                                          # else queue_reel.sh stops at "already queued"
echo "$(date +%H:%M:%S)  Approved preview · $slug" >> logs/activity.log
out=$(bash tools/queue_reel.sh "reels/$slug" 2>&1) || { echo "$out" >&2; exit 1; }; echo "$out"
[ -f "logs/queued/$slug" ] || { echo "queue_reel did not confirm $slug" >&2; exit 1; }
if echo "$out" | grep -q "already on the relay"; then   # it was posted meanwhile: nothing to swap
  python3 -c "import json,sys; p=sys.argv[1]; c=json.load(open(p)); c.pop('requeue',None); json.dump(c,open(p,'w'),indent=1,ensure_ascii=False)" "reels/$slug/reel.json"
  rm -f "$M"; echo "NOT swapped: $slug is already posted (or no longer queued)"; exit 3; fi
rm -f "$M" "$P"   # the relay holds the post now; the 300 MB masters would only fill Drive (the small -tg copy stays)
echo "approved: $slug"
