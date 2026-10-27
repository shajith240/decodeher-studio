# DecodeHer: project handbook (read first)

Last rewritten 2026-10-27. One page, current. Depth lives in `brain/` (rules, research, growth) and the memory notes;
where an older note disagrees with this page, this page wins.

## What this is
@thedecodeher: a faceless Instagram page about dating psychology for men (decoding women's behaviour and texting).
Goal: 10,000 followers (10-27: 74 followers; reels land at ~120 or ~1,200 views, nothing higher yet).
The owner gave Claude full control of content and growth: **decide, don't ask**; report what changed and why.

## How it runs: cloud first, laptop not needed
| Part | Where | What it does |
|---|---|---|
| Posting relay | Cloudflare `relay/worker.js` | posts booked reels (08:30, 18:30, 22:00 IST) and carousels (04:30, 20:00) |
| Factory | GitHub `.github/workflows/factory.yml` (every 3 h) → `tools/factory.py` | voice → plan → clips → mix → sheets → judge → render → book |
| Planner | GitHub `planner.yml` (05:30 + 17:30 IST) | growth stats + notes, viral bank collectors, next reel batch (`tools/auto_planner.py`), carousels |
| Claude in the cloud | GitHub `claude.yml` → `tools/cloud/claude_task.sh` | any Telegram message from the owner = a full Claude session; replies on Telegram |
| Self-repair | last steps of `factory.yml` | failed run / newly parked reels → starts `claude.yml` (kind=repair), max once per 6 h |
| HQ + Telegram bot | Cloudflare `hq/worker.js` | the owner's phone interface, /status /queue /stats, board at https://decodeher-hq.shajith240.workers.dev |
| Files | Google Drive `gdrive:decodeher/` via `tools/cloud/sync.sh` | reels, library, deliverables, logs (code is in git; the repo is PUBLIC, so no secrets or private notes in git) |

`node tools/ig_queue.js ids` shows the queue. Never read or print `.env`, `.relay.json` or any secret.
Laptop services (factory, manager, growth timers) are switched off on purpose; only the Clip Library board (localhost:4317) runs there.

## The content rules (owner-approved, 10-27)
- **Copy what is viral now (95/5).** Every reel/carousel remixes a proven viral post: same hook, points, order, examples.
  Ours: "Listen." beat, closing line, our voice, AI-woman opener, our look. Prefer posts from the **last 60 days** in **our
  faceless format** (face-to-camera, skits, podcasts don't carry over). `tools/pick_sources.py` ranks this way.
- **Short:** max 85 spoken words (~30 s), max 3 points, no pause before "Listen." (`tools/script_polish.py` enforces it).
- **Hook:** name her exact behaviour or a type of man, so the viewer asks "is that me?". Rulebook: `brain/growth/content-rules.md`.
- **Narration:** complete, connected, framed sentences, never fragments. English only.
- **Look:** colour Pinterest clips, lens frame, small white serif captions, AI-woman opener with no text on her face,
  sound only from `library/rebel-pack`, music ≥ 12 dB under the voice, bronze-bust outro.
- **Carousels:** 2 a day, AI-woman face cover matched to the message, text never on the face; the owner adds music in the app.
- Ethics: decode / defend / honest attraction; only real abuse is off-limits.

## How to work with this owner
- Non-technical, dictates by voice (rough, sometimes angry): read for intent, answer short and plain, no jargon.
- **Show before you ship:** anything visual and new goes to the owner as a preview first.
- Verify the whole result (frames, levels, ending, ffprobe) before saying anything is done. They hate repeated bugs.
- Codex image generation only when the owner asks. Products: simple PDFs only, private-friendly.

## Open work (10-27)
- Trend scan of reels viral in the last 14 days (spare Instagram account via Agent Reach, laptop only for now).
- Named series instead of "Dark psychology #N"; on-screen hook text above/below her face (needs the owner's OK on a sample).
- Trial reels through the API (unverified); rclone's shared Drive client id is being retired in 2026 (needs our own id).

## Gotchas
- A killed queue job double-books posts: never cancel a factory run mid-render/queue.
- `pkill -f <pattern>` can match its own shell command; use exact process names.
- Drive has no hard links: `sync.sh` keeps them as `reels/.hardlinks.tsv`; deleting reel folders on Drive means filtering it.
- Old reels/renders were archived to `gdrive:decodeher-archive/2026-10-27/` (not deleted).
- Instagram rate-limits fast: one slow attempt, then wait; never loop.
