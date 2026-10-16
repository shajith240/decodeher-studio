STATUS: OPEN
# NEXT SESSION — start here (written 2026-10-16 22:35 IST; owner away, laptop on)

Read CLAUDE.md first. Never read/print .env, .relay.json, .secrets/*. Decide yourself (owner's order); be economical.
When ALL tasks below are done, change the first line of this file to `STATUS: DONE` (the resume watcher then stops).

## Context
- Owner's order (10-16 22:30): "make sure production is running in the CLOUD." A cutover script stopped the laptop
  factory/manager/report/growth timer (disabled on purpose), uploaded reels/library/deliverables/logs to Drive, enabled the
  GitHub workflows `factory` (every 3 h, gate step) and `planner` (05:30 IST daily) and started a first factory run.
  Activity lines start with "Cloud cutover ·" in logs/activity.log.
- Booked: w7-02 (10-17 18:30) and w7-04 (10-17 22:00); w7-05 at 10-17 08:30. Unfinished: w7-06, w8-01..06.

## Tasks
1. Watch the cloud run: `gh run list --workflow factory -L 3`, `gh run view <id> --log-failed`. Success = it pulled Drive,
   moved w7-06 / w8 reels forward (voice, plan, clips, judge, render), pushed Drive, reported to HQ, and booked reels when
   finished (`node tools/ig_queue.js ids`). If a step fails: read the log, fix the real cause in the code, commit + push,
   `gh workflow run factory -f max_minutes=160`, watch again. Typical risks: missing files on Drive (push them with
   tools/cloud/sync.sh using SYNC_PATHS), Pinterest cookies (secret PINTEREST_COOKIES), Claude auth (secret
   CLAUDE_CODE_OAUTH_TOKEN), disk on the runner, HyperFrames render time.
2. Never run the laptop factory at the same time as a cloud run (both write the same reels on Drive).
3. When one cloud run finished cleanly: note it in CLAUDE.md "Current state" (cloud is live; laptop optional), then set
   STATUS: DONE.
