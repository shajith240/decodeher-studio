#!/usr/bin/env bash
# Render + queue reels ONE AT A TIME. Turns are taken with a lock file (logs/render.lock) — never by scanning process names
# (that matched its own parent command and deadlocked on 10-14). Usage: tools/render_line.sh reels/<reel> [reels/<reel> ...]
cd "$(dirname "$0")/.."; mkdir -p logs
for R in "$@"; do
  [ -f "deliverables/week-2/$(basename $R).mp4" ] && { echo "already rendered: $R"; continue; }
  (
    flock 9
    tools/reel_finish.sh "$R" 2>&1 | tail -1 && tools/queue_reel.sh "$R" 2>&1 | tail -2
  ) 9>logs/render.lock
done
