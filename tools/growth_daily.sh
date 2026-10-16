#!/usr/bin/env bash
# Growth brain, daily loop (owner 10-16): measure (no Claude) -> read expert sources (no Claude) -> think (one Sonnet session).
# Runs from the systemd user timer decodeher-growth.timer at 05:30 IST. If Claude is capped, the think step retries in 60 min (3x).
# By hand: bash tools/growth_daily.sh        (THINK_ONLY=1 skips measure/read, used by the retries)
set -uo pipefail
cd "$(dirname "$0")/.."; ROOT=$(pwd); mkdir -p logs brain/growth
CLAUDE_BIN=$(command -v claude || echo "$HOME/.local/share/mise/installs/claude/latest/claude")
say(){ echo "$(date +%H:%M:%S)  Growth brain · $*" >> logs/activity.log; }
exec 9>logs/growth.lock; flock -n 9 || exit 0
if [ -z "${THINK_ONLY:-}" ]; then
  python3 tools/growth_analyze.py >> logs/growth.log 2>&1 && say "numbers updated (brain/growth/performance.md)" || say "could not read Instagram stats today"
  python3 tools/growth_fetch.py 4 >> logs/growth.log 2>&1; say "$(tail -1 logs/growth.log | cut -c1-120)"
fi
LOG="logs/growth-$(date +%F-%H%M).log"
"$CLAUDE_BIN" -p "$(cat tools/growth_prompt.txt)" --model sonnet --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Bash(ls:*)" "Bash(cat:*)" --output-format text > "$LOG" 2>&1
TRIES_F=logs/growth.tries; tries=$(cat "$TRIES_F" 2>/dev/null || echo 0)
if tail -c 2000 "$LOG" | grep -qiE "usage limit|session limit|hit your limit|rate limit|limit reached"; then
  if [ "$tries" -lt 3 ]; then
    echo $((tries + 1)) > "$TRIES_F"
    systemd-run --user --unit="decodeher-growth-retry-$(date +%s)" --on-active=60m --setenv=PATH="$PATH" --setenv=THINK_ONLY=1 --working-directory="$ROOT" /bin/bash "$ROOT/tools/growth_daily.sh" >/dev/null 2>&1
    say "Claude is capped — thinking again in 60 min ($((tries + 1))/3)"
  else rm -f "$TRIES_F"; say "skipped thinking today (Claude capped all morning)"; fi
else
  rm -f "$TRIES_F"; mkdir -p brain/growth/data/read; mv brain/growth/inbox/*.txt brain/growth/data/read/ 2>/dev/null   # read items are archived by the script (Claude has no rm)
  say "today's plan written (brain/growth/next-batch-plan.md) — $(grep -v '^\s*$' "$LOG" | head -1 | cut -c1-140)"
  if [ -f .secrets/HQ_URL ]; then HQ_URL=$(cat .secrets/HQ_URL) HQ_KEY=$(cat .secrets/HQ_KEY) python3 tools/cloud/report.py event activity "Growth brain: $(grep -v '^\s*$' "$LOG" | head -5 | tr '\n' ' ' | cut -c1-600)" >/dev/null 2>&1 || true; fi
fi
