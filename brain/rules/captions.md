# On-screen text (strict) — The Dark Needle grammar + purple

1. **Every spoken word appears on screen once** — narration in the caption, built word by word as it is said;
   **quoted dialogue only in its notif/speech** (the caption stops before the quote: `DN.say(li, { range })`);
   **list items only as tags** (the caption carries the sentence that introduces the list).
   A tag never repeats words that are in the caption at the same moment — `node tools/repeat_check.js` enforces it.
2. Each voice line is one text block, placed **in the scene next to its subject** (anchor set per beat), never over a figure's head/face.
3. Type (block in the y 270–500 band, see [[rules/layout]]): **Barlow Semi Condensed 700** (matched to his frames, [[research/darkneedle-visual-grammar]]), uppercase, 64–100 px, line-height 1.08,
   plain white with a small shadow — **no glow, no gradients, no bounce** (those read as AI-generated). Max 3 lines per block; left-aligned when built word by word.
4. Words appear **30 ms after** they start being spoken — word times are measured from the voice (`tools/align_words.py`), never estimated; captions must never run ahead of the voice. 0.08 s fade, no movement. A block stays until its last word ends + 0.3 s, then fades 0.15 s.
5. **Accent**: 1–2 key words per line are flat purple `#B26BFF` (no glow). Nothing else is coloured.
6. Punch lines: one word at a time, 150–190 px, centred, alone on the dark.
7. Labels / notif text / citations: min 38 px, white or purple only.
8. Text layers are above grain and vignette.

## Lockup captions — TRIED AND REJECTED (owner, 10-13: "bounce effect looks like shit… stick to the previous style")
Kept only as history; `DN.say` defaults to the plain word-by-word build. Do not enable `lockup: true`.
Research: [Captions.ai keyword emphasis](https://captions.ai/help/guides/engagement/highlight-keywords),
[phrase vs word captions](https://blitzcutai.com/blog/word-by-word-captions-vs-full-sentence-captions),
[kinetic typography & hierarchy](https://www.influencers-time.com/use-kinetic-typography-to-boost-short-form-video-retention/).
- `DN.say` is a lockup by default: one phrase (punctuation or ≤ 4 words) on screen at a time; phrases CUT, never crossfade.
- Each phrase has ONE dominant word ~1.8× (auto: the accent word, else the longest content word), 700 weight, landing with
  a small scale-in; supporting words 0.78× at 600 weight. The big word is clamped so it never exceeds the block width.
- Purple only for the accent words you pass (1–2 per line). The dominant word is white unless it's an accent.
- Choose `accent` so the punch of each line becomes the big purple word.

## Metallic finish (approved 10-13)
White text = soft satin-silver gradient (no hard horizon line); accent words = purple chrome with a soft glow.
**Shimmer only after landing**, on the payoff punch word and FOLLOW. No flicker. CTA: FOLLOW purple, FOR MORE white (`keyOnly`).

## CTA
`DN.cta(ctaLine)` — two moments: the share line, then **FOLLOW FOR MORE** alone and bigger. Never one paragraph.

## Two-tier mode (owner reference, 10-13 — preview pending approval)
`DN.TIERS = true` right after `DN.init(tl)`. Each phrase becomes a small white top line plus a big purple key line (the accent word
and what follows it), in Montserrat 900 italic, with each word EASING in (slides from the right, fades grey→white; `DN.easeIn`) — NOT a wipe. NO flicker (tried and rejected, owner 10-13). The accent is ONE slow shimmer pass AFTER the word lands: `shine: ["word"]`, on the payoff word and FOLLOW only
(owner, 10-13). Flat, not metallic. Caption display drops . , ; : (`DN.clean`); ? and ! stay. The CTA key line wraps big: FOLLOW / FOR MORE.
Load the font: `&family=Montserrat:ital,wght@1,800;1,900`. See [[editing-reference-cheatcode]].

## The visual is the caption (owner, 10-13)
While a WhatsApp bubble or tag is on screen, the caption phrase spoken at that moment is NOT shown. Two things saying the same
words split the eye. This is automatic: `DN.finish()` measures when bubbles and tags are visible and drops the overlapping
two-tier phrases. Captions carry only the narration that has no visual of its own.

## Readable captions (owner, 10-14: "captions move so fast it's not easy to read")
Research: [[research/pinterest-refs-a]], [[research/pinterest-refs-b]], [[research/pinterest-refs-c]]. Measured problem: 12 of 29 phrases
were fully visible for under 0.8 s.
- **Reading time:** the added sentence pauses were REJECTED (owner, 10-14: "slow and boring"); the tool is archived. Readability comes from groups + ghost-karaoke instead.
- **Groups:**
  - Split where the meaning breaks; 4 words, up to 6 so a group never ends on "to/the/whose…".
  - Merge any group that would be up < 0.9 s.
  - The WHOLE group appears at once. Unspoken words sit at 35 % and light up on the voice (ghost-karaoke).
- **Entrance by role, never one animation for everything** (`fx:` overrides):
  - **slide:** every group of a question; top line from the left, key line from the right, 0.24 s.
  - **dissolve:** soft words such as date, love, miss, wonder, comfortable; blur 10→0 and scale 1.04→1, 0.45 s.
  - **rise:** the first group of a line; y 34 and blur 8→0, 0.3 s.
  - **cut:** a 0.08 s fade, for the rest.
- **Exit:** a cut. Out 0.07 s before the next group starts in. The last group of a line fades at the line's end.
- **Top line upright 800, key line italic 900.** In the refs, italic is reserved for emphasis.
- The build sets `data-duration` from timing.js, so a longer voice is never cut off.

## Clip reels: captions over footage (10-14, measured on Zoltium's own frames)
- Plain white serif (Cormorant Garamond 700), centred, 2–4 words; break at sentence ends (quotes included).
- Readability comes from **two tricks used together**, never a box or bar:
  1. The footage grade caps highlights at about 80 % (`curves 1/0.80` in tools/clipcut.py), so the caption is the brightest thing on screen.
  2. A tight dark shadow hugging the letters (1–3 px) plus a faint wide halo.
