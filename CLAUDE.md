# DecodeHer: project handoff (read first)

Last updated 2026-10-16 06:45 IST. This file is the starting point for every new session. Use `brain/` (rules, pipeline, research) and the memory notes for depth.

**10-16 RESUME POINT: read `brain/NEXT-SESSION.md` first** (live hand-off plan; auto-resume after a Claude limit = `tools/resume_after_limit.sh at "YYYY-MM-DD HH:MM"`, a one-shot systemd timer that runs a headless Sonnet session on that plan).

## The project in one paragraph
@thedecodeher is a faceless Instagram Reels page about dating psychology for men: decoding women's behaviour and texting.
Reels are ~45–60 s (no length cap; value first). An AI narrator (Fish 86ac) runs over colour clips from Pinterest ("dark psychology"
searches), one new image per 2–4-word caption group, opening on a realistic AI-woman hook clip (format: see Current state). Everything runs unattended on this laptop as three systemd **user** services:
- `decodeher-factory` (`tools/factory.py`) moves each reel through voice → plan → clips → mix → sheets → judge → (research) → render → queue.
- `decodeher-manager` (`tools/manager.py`) checks the line every 2 min. It fixes routine faults and runs a `claude -p` agent for real
  incidents (`tools/manager_prompt.txt`).
- `decodeher-board` (`tools/dashboard.js`) is the live studio board at http://localhost:4317 (cloud copy at https://decodeher-hq.shajith240.workers.dev; Telegram bot = the manager you talk to).

Posting goes through our own Cloudflare relay (`relay/worker.js`) at 3 posts a day, 08:30, 18:30 and 22:00 IST (changed 10-16 to reach US mornings/lunch; brain/research/audience-location.md). `node tools/ig_queue.js ids|status|captions`
shows the queue. Never read or print `.env` or `.relay.json`.

## How to work with this owner
- They're non-technical and dictate by voice, so messages are rough and sometimes angry. Read for intent and answer in plain words.
  Their bar is premium and readable, with no "AI slop".
- **Show before you ship.** Never attach anything visual to a live post (covers, outros, new styles) before the owner has seen it.
  A generated cover went onto a post unseen on 10-15 and they were furious.
- **Codex image generation is rationed.** Use it only when the owner explicitly asks. Generated covers were rejected outright.
- They watch the competitor **Zoltium** and the Rebelvids "viral dark psychology reels" course closely (transcript:
  brain/research/rebelvids-dark-psych-course-transcript.txt). Match that craft; our signature lives only in the outro.
- Every message you send: short, plain words, clickable links to files, no jargon. They hate repeated bugs — verify the WHOLE
  result (frame grid of the full reel, levels, ending) before showing anything.
- Plan first and confirm the plan, then execute. Batch the work, use cheap subagents for research, and verify results
  (frames, transcripts, ffprobe) before saying anything is done.

## Current state (10-16, 06:45) — supersedes everything written on 10-15
- **Owner gave Claude full control** to run and grow the channel — DECIDE, don't ask for advice or permission on growth/content
  choices (10-16: "this is your responsibility"); just report what changed and why. Still ask only for things that need the
  owner's hands (logins, Instagram app actions like archiving). Target: **1,000 followers by 2026-10-26**. 3 posts/day
  (08:30, 14:00, 21:00 IST) via the Cloudflare relay (posts with the PC off). Baseline: ~6 followers, ~120 views/reel.
- **Queue:** the old w2/w3/w4 reels were removed (owner) and their folders deleted. Booked: w6-01 "Hot and cold" (10-16 08:30).
  Batch **w7** (6 reels, scripts approved, `brain/content/drafts/week7-rebel-scripts.md`) is in the factory and books itself
  into the next free slots. Factory batches: reels/w6-batch.json, reels/w7-batch.json.
- **Approved reel format** (owner, 10-16, after many corrections; memory rebel-format.md):
  - Script shape from the Rebelvids course: hook (her specific behaviour + tension, `brain/research/hooks-2026.md`) → "Listen"
    → named psychology → numbered moves → why → a natural closing line (a reason to follow/send/save; never begging).
    English only. No length cap; never rush the voice (memory value-over-length). Ethics: decode/defend/honest attraction,
    never coach making her insecure or dependent.
  - Voice: Fish **86ac939163784775a38c14912a8de9d9** (config reels.voice), whole take, 80 ms lead silence.
  - Look: **colour** clips full-screen with the cinematic grade, black paper as a soft-light **texture**, corners fading out
    (feathered vignette, `library/rebel-pack/edge-mask-soft.png`), small white serif captions, title card with NO box.
    reel.json `frame: "lens"`, `colour: true` (new_reels_v3.py sets these when config reels.frame = "lens").
  - Opening shot: a realistic **AI woman** clip (reel.json `hookClip`; pool `library/hook-pool/ai/`, only pins labelled AI,
    adult, no nudity, no real/famous faces). Clips from Pinterest with the suffix "dark psychology"; clips with baked-in text
    are banned (clippick.py).
  - Sound: ONLY the owner's pack `library/rebel-pack` (config reels.sfxSet). Snaps RARE, only at narration peaks, laughs only
    after a dark/mocking line (`tools/peak_points.py` → reel.json snaps/laughs). Music: only smooth horror/piano, measured gate
    in `brain/rules/music-rule.md` (10 approved tracks); bed always ≥ 12 dB under the voice.
  - Outro (bronze bust) rises during the closing words and ends with the reel; the clip film runs until then.
- **Board:** pixel studio (boxes = reels, no film-reel icons, no plants/pictures, rugs only), one-sentence summary bar,
  "In production" progress bars by real pipeline step. Cloud copy: https://decodeher-hq.shajith240.workers.dev
- **Claude limit:** posting/comment replies never use Claude; the factory pauses a reel 30 min on a limit. Before the owner's
  limit runs out, write `brain/NEXT-SESSION.md` and schedule `tools/resume_after_limit.sh at "<reset + 5 min>"`.
- **PC off:** posting continues; production needs the laptop until the GitHub factory is enabled (blocked on the owner
  setting `gh secret set PINTEREST_COOKIES`).
- **Growth brain** (`brain/growth/README.md`): daily 05:30 timer measures our stats (tools/growth_analyze.py), reads vetted
  expert sources (tools/growth_fetch.py, brain/growth/expert-sources.md), then one Sonnet session updates tactics/playbook/
  experiments and writes `brain/growth/next-batch-plan.md` — the script writer follows it. Running experiment: closing line
  SEND vs SAVE (w8 batch, read ~10-23).
- **Batches:** w7 (6, producing/booking), w8 (6, send/save experiment, producing). Telegram pin intake is live
  (tools/pin_intake.py via manager; AI names each clip). Laptop-offline alert on Telegram after 15 min (campus Wi-Fi login).
- Open work: see `brain/NEXT-SESSION.md`.

## Gotchas learned the hard way
- Restarting the factory kills running jobs. Wait until no render or queue job is running (a killed queue job double-booked posts on 10-14).
- On btrfs, `du` of ~/.cache/uv overstates its size (reflinks). Don't run `uv cache prune` in automation, because it blocks on the lock.
- Claude's usage limit (resets 1 am IST) used to park reels. The factory now pauses them for 30 min instead.
- Headless screenshots: `~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome --headless=new --timeout=9000` for the
  live board (it never goes idle), and `--virtual-time-budget=9000` for static pages that need web fonts.
- Low RAM (15 GB): Chrome screenshots during a render can be OOM-killed (exit 137). Retry one at a time.
