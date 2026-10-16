STATUS: DONE
# 10-17 00:20 IST: owner back; laptop production restarted. Cloud cutover NOT done (factory/planner workflows still disabled).
# Do the cutover only when the owner leaves again; never run both at once.
# NEXT SESSION — start here (written 2026-10-16 22:35 IST; owner away, laptop on)

Read CLAUDE.md first. Never read/print .env, .relay.json, .secrets/*. Decide yourself (owner's order); be economical.
When ALL tasks below are done, change the first line of this file to `STATUS: DONE` (the resume watcher then stops).

## RESUME FIRST (10-16 22:40): the owner had to leave; the Drive upload was stopped half-way and the workflows were NOT enabled.
Re-run the switch-over: `bash /tmp/claude-1000/-home-shajith-Projects-dark-psycology/7c7b3dfe-a307-40c8-817f-b198e2428639/scratchpad/cutover.sh` if it still exists, otherwise:
`SYNC_PATHS="reels library/hook-pool library/clips deliverables logs brain/content/captions" bash tools/cloud/sync.sh push`, rclone copy library/clip-usage.json + library/pin-registry.json to gdrive:decodeher/library/, then `gh workflow enable factory && gh workflow enable planner && gh workflow run factory -f max_minutes=160`.

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
