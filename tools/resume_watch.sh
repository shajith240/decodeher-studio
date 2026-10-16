#!/usr/bin/env bash
# Resume watcher (owner 10-16: "the work must continue by itself while I sleep; Claude starts again when the limit resets").
# Runs every 30 min (systemd user timer decodeher-resume-watch.timer). If brain/NEXT-SESSION.md starts with "STATUS: OPEN",
# no resume session is running, and the last one finished > 40 min ago, it starts tools/resume_after_limit.sh (which itself
# waits out a Claude usage limit and retries). A session that finishes everything sets "STATUS: DONE" and the watcher idles.
set -uo pipefail
cd "$(dirname "$0")/.."
head -1 brain/NEXT-SESSION.md 2>/dev/null | grep -q "STATUS: OPEN" || exit 0
flock -n logs/resume.lock true || exit 0                       # a resume session is running right now
last=$(ls -t logs/resume-*.log 2>/dev/null | head -1)
if [ -n "$last" ] && [ $(( $(date +%s) - $(stat -c %Y "$last") )) -lt 2400 ]; then exit 0; fi
pgrep -f "tools/resume_after_limit.sh" >/dev/null && exit 0
exec bash tools/resume_after_limit.sh
