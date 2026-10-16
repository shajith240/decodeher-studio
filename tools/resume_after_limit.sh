#!/usr/bin/env bash
# Resume the work automatically after the owner's Claude plan limit resets (owner 10-16: "the work shouldn't pause when I'm out").
# Starts a headless Claude session that reads brain/NEXT-SESSION.md (the hand-off plan) and carries on.
# If Claude is still capped, it re-schedules itself in 20 min (max 6 tries per hand-off).
# Schedule:  bash tools/resume_after_limit.sh at "2026-10-16 08:06"     (a one-shot systemd user timer)
# Run now:   bash tools/resume_after_limit.sh
set -uo pipefail
cd "$(dirname "$0")/.."; ROOT=$(pwd); mkdir -p logs
CLAUDE_BIN=$(command -v claude || echo "$HOME/.local/share/mise/installs/claude/latest/claude")
if [ "${1:-}" = "at" ]; then
  systemd-run --user --unit="decodeher-resume-$(date +%s)" --on-calendar="$2" --timer-property=AccuracySec=30s \
    --setenv=PATH="$PATH" --working-directory="$ROOT" /bin/bash "$ROOT/tools/resume_after_limit.sh"
  echo "$(date +%H:%M:%S)  Auto-resume scheduled · Claude restarts the work at $2" >> logs/activity.log; exit 0
fi
exec 9>logs/resume.lock; flock -n 9 || { echo "already running"; exit 0; }
TRIES_F=logs/resume.tries; tries=$(cat "$TRIES_F" 2>/dev/null || echo 0)
LOG="logs/resume-$(date +%F-%H%M).log"
echo "$(date +%H:%M:%S)  Auto-resume · Claude limit reset, picking up the plan in brain/NEXT-SESSION.md" >> logs/activity.log
PROMPT="You are resuming unattended work on this project. Read brain/NEXT-SESSION.md and CLAUDE.md, then do the tasks in NEXT-SESSION.md in order. Be economical. When done (or if you hit the usage limit), update brain/NEXT-SESSION.md with what is left and stop."
"$CLAUDE_BIN" -p "$PROMPT" --model sonnet --allowedTools "Bash" "Read" "Edit" "Write" "Glob" "Grep" --output-format text > "$LOG" 2>&1
if tail -c 2000 "$LOG" | grep -qiE "usage limit|session limit|hit your limit|rate limit|limit reached"; then
  if [ "$tries" -lt 6 ]; then
    echo $((tries + 1)) > "$TRIES_F"
    systemd-run --user --unit="decodeher-resume-$(date +%s)" --on-active=20m --setenv=PATH="$PATH" --working-directory="$ROOT" /bin/bash "$ROOT/tools/resume_after_limit.sh" >/dev/null 2>&1
    echo "$(date +%H:%M:%S)  Auto-resume · Claude still capped, trying again in 20 min ($((tries + 1))/6)" >> logs/activity.log
  else echo "$(date +%H:%M:%S)  Auto-resume · gave up after 6 tries (Claude still capped)" >> logs/activity.log; rm -f "$TRIES_F"; fi
else
  rm -f "$TRIES_F"
  echo "$(date +%H:%M:%S)  Auto-resume done · see $LOG" >> logs/activity.log
fi
