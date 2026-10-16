# Growth brain (owner 10-16: "Claude runs the page by itself — learn daily from expert sources, adapt to the numbers")

A small knowledge graph in plain markdown (Obsidian-style `[[links]]`), updated every day by `tools/growth_daily.sh`
(systemd timer, 05:30 IST). Goal: 1,000 followers by 2026-10-26, then keep growing.

## Daily loop
1. **Measure** — `tools/growth_analyze.py` (no Claude): per-reel reach, views, avg watch, watch %, likes/comments/shares/saves
   per 1k, followers → `performance.md`, raw history in `data/`.
2. **Read** — `tools/growth_fetch.py` (no Claude): new videos/posts from the vetted sources in `expert-sources.md` (JSON block)
   → transcripts/text in `inbox/` (max 4 items a day, to keep the Claude plan safe).
3. **Think** — one Sonnet session (`tools/growth_prompt.txt`): turns the inbox into notes and tactic nodes, compares tactics
   with OUR numbers, updates `playbook.md`, logs the decision in `strategy-log.md`, and writes `next-batch-plan.md`
   (hook formats, topics, opening clips, post slots, ONE experiment) that the script writer follows.

## Node types
- `notes/YYYY-MM-DD-<source>-<slug>.md` — what one video/article taught (source, link, date, claims with evidence quality).
- `tactics/<slug>.md` — one tactic: what, why it should work, how it maps to OUR pipeline (which tool/field), evidence
  (links to notes), status `idea | testing | works | failed`, linked experiments.
- `experiments/<date>-<slug>.md` — hypothesis, the ONE change, metric, start/end, result → updates the tactic's status.
- `playbook.md` — the current rules, ranked; only `works` tactics (and the owner's fixed rules) are rules.
- `strategy-log.md` — one entry per day: numbers seen, what changed, why.

## Rules for the brain
- The owner's decisions in CLAUDE.md, memory and `brain/rules/` beat any tactic. No bots, follow-for-follow, buying, pods,
  misleading bait, or content that coaches making a woman insecure/dependent.
- A tactic becomes a rule only after OUR numbers support it (or it is official Meta guidance). One experiment at a time,
  ≥ 3 reels per arm; small samples are called small.
- Vendor numbers are marked unverified.
