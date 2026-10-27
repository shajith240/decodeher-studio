#!/usr/bin/env bash
# Send a video (≤ 50 MB) or, with no file, a text message to the owner on Telegram. The bot token never reaches the log.
# Usage: tools/cloud/tg_send.sh <video.mp4|-> "<caption>"      Env: TELEGRAM_BOT_TOKEN, OWNER_CHAT_ID (TELEGRAM_API: tests only)
set -euo pipefail
f="$1"; cap="${2:-}"; : "${TELEGRAM_BOT_TOKEN:?}" "${OWNER_CHAT_ID:?}"
API="${TELEGRAM_API:-https://api.telegram.org}"; resp=$(mktemp); trap 'rm -f "$resp"' EXIT
if [ "$f" = - ]; then cap="${cap:0:4000}"; else cap="${cap:0:1000}"; fi   # Telegram: 4096 for a message, 1024 for a caption
if [ "$f" = - ]; then
  code=$(curl -sS -o "$resp" -w '%{http_code}' --form-string chat_id="$OWNER_CHAT_ID" --form-string text="$cap" \
    "$API/bot${TELEGRAM_BOT_TOKEN}/sendMessage") || code=000
else
  [ -f "$f" ] || { echo "no file: $f" >&2; exit 1; }
  size=$(stat -c %s "$f"); [ "$size" -le 52428800 ] || { echo "too big for Telegram: $size bytes" >&2; exit 1; }
  code=$(curl -sS -o "$resp" -w '%{http_code}' --max-time 600 --form-string chat_id="$OWNER_CHAT_ID" -F "video=@$f;type=video/mp4" \
    --form-string caption="$cap" --form-string supports_streaming=true "$API/bot${TELEGRAM_BOT_TOKEN}/sendVideo") || code=000
fi
if [ "$code" = 200 ] && python3 -c "import json,sys; r=json.load(open(sys.argv[1])); sys.exit(0 if r.get('ok') else 1)" "$resp" 2>/dev/null; then
  python3 -c "import json,sys; m=json.load(open(sys.argv[1]))['result']; print('telegram: sent message', m['message_id'])" "$resp"
else echo "telegram send failed: HTTP $code $(head -c 300 "$resp")" >&2; exit 1; fi
