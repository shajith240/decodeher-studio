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

## 10-17 03:20 IST: text-in-clips redo PAUSED (Pinterest search down, owner saw it in the app)
6 booked reels need new clips (OCR found baked-in text): w7-02, w7-04, w7-05, w7-06, w8-02, w8-04. Each reel.json has
requeue:true + parked. Their current videos stay booked. When Pinterest search works again (test: gallery-dl --simulate a
search returns results), for each: remove "parked", move logs/queued/<slug> aside; the factory re-searches, renders
(OCR-checked) and swaps the new video into the same slot. Old pieces: scratchpad redo-1017 (temporary).

## 10-18 ~08:00 IST: state when the owner went to sleep
- Production running: w9, w10, w11 (18 reels, AI-woman openers, keyword rule) fill Tue 10-20 → Sun 10-25. Remakes of w8-02
  "Three hours" (18:30 today) and w8-04 "Double text" (22:00 today) re-searching clips; they swap into their slots.
- s1 / s2 test reels: approval pending (owner).
- Visual hooks: 25 clips on the shelf (library/hook-pool/visual), OFF (config reels.visualHooks=false) until the owner plans it.
- Zoltium study: blocked. Brave is logged in as @thedecodeher (do NOT scrape with our own account); Instagram refuses all
  tools for @zoltium anyway. Owner will send saved Zoltium reel VIDEOS on Telegram. TODO: the bot only takes Pinterest links
  DONE 10-18: videos sent to the bot → Drive only (gdrive:DecodeHer/research/zoltium, laptop keeps no copy);
  (never used in reels), then run the measure script (scratchpad tools/measure.py, rewrite into tools/) + analysis + skill.
- PLANNED (owner OK'd 10-18, build ~Tue after w9-w11 are produced): Drive as the clip database. Laptop keeps only
  fingerprints (reels/_pool/emb.json + clip .json); factory ranks by fingerprint, downloads the ~100 candidates per reel,
  deletes after render. Frees ~700 MB. FIRST: owner's own Google Drive client_id for rclone (shared one is retiring in 2026);
  keep laptop copies of owner clips until the Drive path has made a few reels cleanly.
