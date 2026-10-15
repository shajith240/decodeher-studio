# Brain — dating-psychology reels

> **Status (2026-10-13):** @thedecodeher is live and posts 2 reels a day (08:30 and 21:00 IST) through the decodeher-relay.
> The week-1 editing style is approved and LOCKED: change it only when the owner asks. The queue ends 2026-10-16 21:00, so queue the next batch before then.
> Start each session with `node tools/ig_queue.js status`, then `node tools/content_sync.js`.

The single source of truth for every agent working on this page. **Read the rules before touching a reel.**
A rule here beats habit, defaults, or anything a playbook suggests.

## Rules (strict)
- [[rules/script-and-hooks]] — what we say, how the first 2 seconds stop the scroll
- [[rules/captions]] — brand caption system
- [[rules/visuals-and-motion]] — the stage, the cast, graphics, motion
- [[rules/audio]] — voice, music, sound effects
- [[rules/layout]] — safe areas, sizes, overlaps
- [[rules/assets]] — reuse-first asset system
- [[mistakes]] — every bug we shipped once; each is now a rule

## How a reel is made
- [[pipeline]] — step by step, with the commands

## Libraries
- [[assets/cast]] — every character still (auto-generated)
- [[assets/fx]] — arrows, circles, marks (auto-generated)
- [[assets/music]] — tracks and licences

## Research
- **Market (10-13):** [[research/competitors-2026-10]] (who's winning and why) · [[research/profile-premium-2026-10]] (bio, highlights, grid, avatar, algorithm) · [[research/competitor-tracking-options]] (auto-follow competitors)
- [[research/darkneedle-visual-grammar]] (main reference) · [[research/playbook-darkneedle]] · [[research/playbook-motion]] · [[research/playbook-shorts]] (weak: stock listicles)

## Content memory (what we made, how it did, what's next)
- [[content/00-content]] — posted reels with numbers, the queue, the part-2 board and variety tallies (refresh: `node tools/content_sync.js`)
- [[content/ideas]] — backlog, part 2s and unused source topics
- `content/reels/<slug>.md` — one note per reel: topic, hook style, story shape, visuals, CTA, results, part 2
**Before planning any batch:** run `node tools/content_sync.js`, read 00-content, and fill the variety ledger.
