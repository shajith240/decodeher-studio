#!/usr/bin/env bash
# Land one cloud-Claude change (claude.yml land job, land.yml for the chat runner). Owner 10-27 chose "safer": Claude never pushes.
#   brain/-only change → committed to main.
#   any other file     → branch claude/<request_id> + Approve / Reject on Telegram (code.yml merges or drops it).
# Usage: tools/cloud/land.sh <dir>     <dir> holds change.patch, files.txt, and optionally commit.txt / reply.txt
# Env: REQUEST_ID, HQ_URL, HQ_KEY. Needs a checkout with push rights (contents: write).
set -euo pipefail
cd "$(dirname "$0")/../.."
L="$1"; : "${REQUEST_ID:?}"
[[ "$REQUEST_ID" =~ ^[A-Za-z0-9_-]{1,64}$ ]] || { echo "bad request id" >&2; exit 2; }
[ -s "$L/change.patch" ] || { echo "no git changes"; exit 0; }
git config user.name "decodeher-cloud"; git config user.email "cloud@users.noreply.github.com"
msg="$(head -1 "$L/commit.txt" 2>/dev/null | head -c 200 || true)"
[ -n "$msg" ] || msg="$(grep -m1 . "$L/reply.txt" 2>/dev/null | head -c 200 || true)"; msg="${msg:-A change to how the system works}"
if grep -qv '^brain/' "$L/files.txt"; then
  git checkout -q -b "claude/$REQUEST_ID"
  git apply --3way --index "$L/change.patch" && git commit -q -m "$msg" && git push -q origin "claude/$REQUEST_ID"
  n=$(grep -vc '^brain/' "$L/files.txt" || true)
  python3 tools/cloud/report.py event preview "$msg ($n file$([ "$n" = 1 ] || echo s) of the system's code)" --request-id "$REQUEST_ID" --code
else
  git apply --3way --index "$L/change.patch" && git commit -q -m "$msg"
  for i in 1 2 3; do git pull -q --rebase origin main && git push -q origin HEAD:main && break; sleep 5; done
fi
