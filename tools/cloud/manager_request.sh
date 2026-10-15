#!/usr/bin/env bash
# Owner change request (Telegram → HQ → GitHub "manager-request"): a restricted Claude agent edits ONE reel, then this prints
# which reel changed. The preview render is tools/cloud/preview.py; nothing here touches posting.
# Env: REQUEST_ID, REQUEST_TEXT (from the dispatch payload — passed as env, never pasted into a shell line), CLAUDE_CODE_OAUTH_TOKEN.
# Writes reel=<slug> and summary=<2 lines> to $GITHUB_OUTPUT (or prints them). Exit 0 with reel= empty when nothing was changed.
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${REQUEST_ID:?}" "${REQUEST_TEXT:?}"
[[ "$REQUEST_ID" =~ ^[A-Za-z0-9_-]{1,64}$ ]] || { echo "bad request id" >&2; exit 2; }
OUTDIR="${RUNNER_TEMP:-/tmp}/request-$REQUEST_ID"; mkdir -p "$OUTDIR" logs/manager
touch "$OUTDIR/start"; sleep 1

# the prompt: placeholders filled in Python (the owner's text is data, never shell)
python3 - "$OUTDIR/prompt.txt" <<'PY'
import glob, json, os, sys
root = os.getcwd(); rows = []
for b in json.load(open("config.json")).get("factory", {}).get("batches", ["reels/w2-batch.json"]):
    for r in (json.load(open(b)) if os.path.exists(b) else []):
        if not os.path.isdir(r): continue
        cfg = json.load(open(f"{r}/reel.json")) if os.path.exists(f"{r}/reel.json") else {}
        slug = os.path.basename(r)
        st = "booked/posted" if os.path.exists(f"logs/queued/{slug}") else "parked" if cfg.get("parked") else "in production"
        rows.append(f"- {slug} · {cfg.get('title', '')} · {st}")
p = open("tools/manager_request_prompt.txt").read()
p = p.replace("{ROOT}", root).replace("{REQUEST_ID}", os.environ["REQUEST_ID"]).replace("{REELS}", "\n".join(rows) or "(none)")
open(sys.argv[1], "w").write(p.replace("{REQUEST}", os.environ["REQUEST_TEXT"].strip()[:4000]))
PY

ALLOW=(Read Glob Grep "Edit(reels/**)" "Write(reels/**)" "Edit(brain/content/captions/**)" "Write(brain/content/captions/**)"
       "Bash(ls:*)" "Bash(ffprobe:*)" "Bash(ffmpeg:*)" "Bash(python3 tools/fill_page.py:*)" "Bash(python3 tools/shot_times.py:*)"
       "Bash(python3 tools/word_cues.py:*)" "Bash(python3 -m json.tool:*)")
DENY=("Read(./.env)" "Read(**/.env)" "Read(./.relay.json)" "Read(**/.relay.json)" "Read(**/rclone.conf)" "Read(~/.config/rclone/**)"
      "Read(.git/**)" "Read(/proc/**)" "Edit(tools/**)" "Write(tools/**)" "Edit(.github/**)" "Write(.github/**)" "Edit(config.json)"
      "Write(config.json)" "Bash(node:*)" "Bash(curl:*)" "Bash(wget:*)" "Bash(env:*)" "Bash(printenv:*)" "Bash(rclone:*)" "Bash(cat:*)")
set +e
timeout 1500 "${CLAUDE_BIN:-claude}" -p "$(cat "$OUTDIR/prompt.txt")" --model "${REQUEST_MODEL:-sonnet}" --max-turns 40 \
  --allowedTools "${ALLOW[@]}" --disallowedTools "${DENY[@]}" --output-format text < /dev/null > "$OUTDIR/answer.txt" 2> "$OUTDIR/err.txt"
rc=$?; set -e
{ echo "request $REQUEST_ID · exit $rc"; cat "$OUTDIR/answer.txt"; } > "logs/manager/request-$REQUEST_ID.log"
[ $rc = 0 ] || { echo "claude failed (exit $rc): $(tail -c 300 "$OUTDIR/err.txt")" >&2; exit 1; }

# which reel: the agent's REEL: line, checked against what really changed on disk
said=$(grep -m1 -oE '^REEL: *[A-Za-z0-9_-]+' "$OUTDIR/answer.txt" | sed 's/^REEL: *//' || true)
changed=$(find reels -newer "$OUTDIR/start" -type f 2>/dev/null | cut -d/ -f2 | sort -u | grep -v '^_pool$' || true)
reel=""
if [ -n "$said" ] && [ "$said" != none ] && [ -d "reels/$said" ]; then reel="$said"
elif [ "$(echo "$changed" | grep -c .)" = 1 ]; then reel="$changed"; fi
summary=$(grep -v '^REEL:' "$OUTDIR/answer.txt" | grep . | head -2 | cut -c1-400)
echo "reel: ${reel:-none} · changed on disk: ${changed:-nothing}"; echo "$summary"
if [ -n "${GITHUB_OUTPUT:-}" ]; then
  { echo "reel=$reel"; echo "summary<<EOF_SUMMARY"; echo "$summary"; echo "EOF_SUMMARY"; } >> "$GITHUB_OUTPUT"
fi
