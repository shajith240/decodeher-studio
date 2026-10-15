# DecodeHer: project handoff (read first)

Last updated 2026-10-15 03:20 IST, at the end of a very long session. The owner opened a new chat on purpose, so this file is the
starting point. Use `brain/` (rules, pipeline, research) and the memory notes for depth.

## The project in one paragraph
@thedecodeher is a faceless Instagram Reels page about dating psychology for men: decoding women's behaviour and texting.
Reels are ~32–40 s. An AI narrator voice runs over 2D illustrated clips taken from Pinterest, one new image per 2–4-word caption group,
in the Zoltium style. Everything runs unattended on this laptop as three systemd **user** services:
- `decodeher-factory` (`tools/factory.py`) moves each reel through voice → plan → clips → mix → sheets → judge → (research) → render → queue.
- `decodeher-manager` (`tools/manager.py`) checks the line every 2 min. It fixes routine faults and runs a `claude -p` agent for real
  incidents (`tools/manager_prompt.txt`).
- `decodeher-board` (`tools/dashboard.js`) is the live studio board at http://localhost:4317 (`/v2` is the isometric version, `/table` a plain table).

Posting goes through our own Cloudflare relay (`relay/worker.js`) at 2 posts a day, 08:30 and 21:00 IST. `node tools/ig_queue.js ids|status|captions`
shows the queue. Never read or print `.env` or `.relay.json`.

## How to work with this owner
- They're non-technical and dictate by voice, so messages are rough and sometimes angry. Read for intent and answer in plain words.
  Their bar is premium and readable, with no "AI slop".
- **Show before you ship.** Never attach anything visual to a live post (covers, outros, new styles) before the owner has seen it.
  A generated cover went onto a post unseen on 10-15 and they were furious.
- **Codex image generation is rationed.** Use it only when the owner explicitly asks. Generated covers were rejected outright.
- They watch the competitor **Zoltium** closely and want to match that level. When in doubt, copy Zoltium's craft and keep our
  signature only in the outro.
- Plan first and confirm the plan, then execute. Batch the work, use cheap subagents for research, and verify results
  (frames, transcripts, ffprobe) before saying anything is done.

## Current state (10-15, 03:20)
- **Queue:** 10 reels booked, 10-15 08:30 → 10-19 21:00, no duplicates (`ig_queue.js ids`). 2 already posted. Views are stuck at ~120–130 per reel.
- **Remake in progress** (`tools/remake_reel.py`). All week-2 reels are being re-voiced with voice v2, end on the spoken line
  **"Decode her."** instead of "Follow for more.", lose the "FOLLOW FOR MORE" text, and gain a 0–2 s **title card**
  (reel.json `titleCard`, drawn by `tools/fill_page.py`). The factory does this on its own: `tools/queue_reel.sh` sees
  reel.json `"requeue": true` and swaps the new video into the reel's **existing** slot. Done: w2-01, w2-03, w2-04, w2-05.
  Still running: w2-07, 08, 09, 10, 16, 17. Not booked yet: w2-11, 13, 15, which get booked normally when finished.
  Check progress with `grep "Re-made video swapped" logs/activity.log`.
- **Captions on all booked posts were rewritten 10-15** in a keyword-first format with ≤ 5 hashtags (`ig_queue.js recaption`).
  Old ones are in `deliverables/queue/old-captions-1014/`.
- **Covers:** booked posts currently use the frame at 600 ms (the title card) as the cover. Two sample covers in the new style
  are in `deliverables/covers/` and are **not attached**. The owner said the font is good but too cramped to read (see Plan, step 3).
- Disk is tight (~6 GB free on 98 GB). The factory pauses new jobs below 4 GB and the manager cleans up below 6 GB.

## Decisions already made (don't reopen them)
- **No spoken "follow for more"** (10-15, it sounds like begging). Reels end on "Decode her." over the existing logo-bust outro.
  The owner LIKES the current ending and doesn't want a new Flow outro for now. Zoltium sometimes closes with
  "Join Zoltium and become a powerful man" and sometimes has no outro at all. A similar line for us is an option to propose, not a decision.
- **No AI-generated covers.** A cover is a frame of OUR OWN clip, given a single-colour tint, paper grain and a vignette, plus one centred italic
  serif line in sentence case ("Is she testing you?"), like Zoltium's grid (`tools/make_cover.sh`).
- **Views rules** (approved 10-15, top of `brain/rules/script-and-hooks.md`): line 1 names her behaviour plus a verdict in ≤ 10 words;
  topics come from the search bank; title card 0–2 s; one send or comment prompt; keyword-first caption; at most 5 hashtags.
  Full diagnosis: `brain/growth/views-diagnosis-2026-10-15.md`.
- **Studio board:** the owner picked the **32-bit pixel style** (`deliverables/studio-concepts/board-redesign/1-pixel32.png`). They want
  the characters to MOVE like real people (typing, working, walking), as in v1, which is the live `studio.html`. `/v2` (isometric static plate)
  was rejected for having no motion. Portraits must be visibly different people, each generated in its own call.

## THE PLAN (owner asked for these, 10-15; confirm order with them, then do it)
1. **Captions → Zoltium's exact style.** The owner finds our purple accent words, glow and shadows cheap and wants them gone.
   - Zoltium (`brain/research/zoltium-story-visuals.md` l.122): a **small white serif (Times-like), ~40 px cap height on 1080 wide,
     dead centre (y ≈ 50 %), sentence case, punctuation kept, 2–4 words per card, hard swaps, no colour, no glow**.
   - Identify the font as exactly as possible. Pull frames from a Zoltium reel (watch skill or yt-dlp) and compare against
     Times New Roman / Tinos / Liberation Serif / Libre Caslon / EB Garamond at the same size, then show the owner a side-by-side.
   - Change the caption block in the reel template (`reels/p1c-hookb/index.html`, copied by `tools/new_reels.py`; each reel's
     own `index.html`; `.cap`/`.a`/`#haze` CSS and the GSAP entrance), and make `fill_page.py` apply it to existing reels.
   - Our signature (purple, the bust) stays ONLY in the outro.
   - Render ONE reel and show the owner before re-rendering the rest.
2. **New narrator voice: seductive, dark, horror and dark-psychology storytelling.** The owner says the current one doesn't fit.
   - Today's voice: local Chatterbox, cloned from `library/voice/narrator-ref.wav`, -1.5 st, chain v2 (see the narrator-voice memory, `tools/reel_vo.py`,
     `tools/vo_chatterbox.py`, `config.json` reels.voice/voiceChain).
   - Research first: `brain/research/voices.md`, `open-source-tts-2026.md`, `narrator-voice-analysis.md`, `zoltium-sound.md`.
   - Build 3–4 short previews of the SAME script line (new reference clips for Chatterbox, Fish Audio voices; Fish's commercial
     terms are unclear, see the voice-licensing memory). Make them MP3, because the owner can't play m4a.
   - The owner picks one, then it gets wired in through config.json and every queued reel is re-voiced. Do this together with step 1, so the reels render only once.
3. **Covers, readable and premium.** The owner likes the look and the font (Playfair Display Bold Italic in `tools/make_cover.sh`)
   but says there's "no spacing, not readable".
   - Add line height (≈1.15–1.2), letter spacing, a larger size, a stronger dark band behind the text, and a max of ~16 characters per line.
   - Consider a more readable premium face, and A/B two fonts on one cover for the owner.
   - Pick the strongest single-subject frame per reel from `reels/<r>/clips/seg/NN.mp4`: make a contact grid and choose by eye.
   - Rotate tints (navy #2a3f7a, maroon #6b1f33, purple, B&W).
   - Show all covers as one grid, then attach with `node tools/ig_queue.js cover <id> deliverables/covers/<slug>.jpg` (or `frame=600` to revert).
4. **"Save the workflow as a bundle."** Package the current reusable workflow as a skill or one documented script:
   remake a reel → title card → cover → caption → swap into its slot. Use `tools/remake_reel.py`, `make_cover.sh`, `queue_reel.sh`, and
   `ig_queue.js recaption|cover|replace`. Write it up in `brain/pipeline.md`.
5. **Studio board v3 (pixel art with motion)**, only after the owner OKs a few Codex images for character sprite sheets (they
   rationed Codex). Keep v1's behaviour and engine (`tools/board/studio.html`), swap in 32-bit art, and keep the
   SSE live push (`/events` in dashboard.js, ~80 ms). Generated art from earlier is in `tools/board/art/` (plate.webp, manager.png,
   box.png, faces/*.png).
6. Then the next batch of scripts, following the VIEWS RULES and the new voice and captions. The owner approves scripts before voicing.

## Tools added on 10-15 (all documented in their headers)
- `tools/remake_reel.py <reel> "TITLE CARD"`: re-voice plus brand ending for an already-made reel. It keeps the clips (clip_round 2).
- `tools/make_cover.sh <reel> <shot> <pos> "<line>" <tint>`: a cover made from our own clip frame. No AI.
- `tools/ig_queue.js`: new commands `recaption <dir>`, `captions`, `cover <id> <jpg>|frame=<ms>`. Captions are now matched by reel
  name, not by number; two reels numbered 08 exist.
- `tools/queue_reel.sh`: the requeue path (swaps into the same slot), the new caption builder (≤ 5 tags), and the THUMB_MS cover.
- `tools/manager.py`: bundled incidents, backs off on Claude's usage limit and on API errors, checks that every queued video decodes,
  `python3 tools/manager.py dry` to look only.
- `tools/fill_page.py`: title card injection (idempotent) and strips FOLLOW FOR MORE.

## Gotchas learned the hard way
- Restarting the factory kills running jobs. Wait until no render or queue job is running (a killed queue job double-booked posts on 10-14).
- On btrfs, `du` of ~/.cache/uv overstates its size (reflinks). Don't run `uv cache prune` in automation, because it blocks on the lock.
- Claude's usage limit (resets 1 am IST) used to park reels. The factory now pauses them for 30 min instead.
- Headless screenshots: `~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome --headless=new --timeout=9000` for the
  live board (it never goes idle), and `--virtual-time-budget=9000` for static pages that need web fonts.
- Low RAM (15 GB): Chrome screenshots during a render can be OOM-killed (exit 137). Retry one at a time.
