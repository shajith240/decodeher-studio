# Visuals & motion (strict) — The Dark Needle grammar + purple

Evidence: [[research/darkneedle-visual-grammar]]. Components: `library/stage/` (use them; don't hand-roll graphics).

## Stage
- **Dark studio** (owner-approved 10-13, `library/stage`): near-black with a faint purple tint; ONE soft light that falls from just
  under the caption (y ~400) onto the people and pools at their feet. The light is ON only while people are on screen —
  `DN.finish()` (call it last in every reel) measures figure visibility per frame; text-only moments are pure dark.
  Dust drifts only inside the light. No wavy lines, never light over the text.
- No floor, no reflections, no light pools.

## Figures (the cast — [[assets/cast]])
- White silhouettes with a soft white glow. Big (a standing figure 1100–1500 px tall), may be cropped by the frame edge,
  off-centre; depth by size (foreground big, background small).
- **Focus**: the subject of the line gets a purple rim glow; the other figure goes dim (opacity .35) and soft (blur 3 px).
- Pose changes: 0.15 s crossfade. Entrances: slide in from the frame edge 120 px + fade, 0.5 s. Exits: the reverse.
- Never: improvised drawings, clip-art, stock footage, 3D bodies, thick marker strokes.

## Graphics (components)
- `arrow`: thin (4 px) curved line, solid or dashed, small open head, white or purple; revealed by a wipe along its path — never stroke-dash animation.
- `box`: thin outlined rectangle (3 px) framing a group; `strike`: purple line through words; `equation`: text = icon → icon.
- Dialogue = **real WhatsApp dark-mode bubbles** (`DN.notif`), each on its SPEAKER's side of the scene: hers grey on the right (above her), his green (`who: "You"`) on the left (above him), tail toward the speaker, blue read ticks on his; realistic `time`. Never invent a UI. "She went quiet" = your bubble read (blue ticks) with no reply — never a fake "Read" message.
- One idea per beat: max 1 arrow + 1 box/notif on screen at a time.

## Camera
- Build in place. The camera may push (≤ 10%) or pan to reveal a wider layout; one push per beat max.
- A hard cut only when the location changes.

## Breathing — one focus at a time (owner, 10-13: "the elements should breathe… this is an art")
- At any moment there is **one** focal element: a text phrase, a graphic, or a figure's action. Everything else is dim or gone.
- A graphic stays only while it is being talked about; when its point is made it **leaves before the next idea arrives**.
- Split dense lines into moments with `DN.say(..., { range })`: e.g. the name of an idea alone → the idea alone → the picture of it.
- Definitions, names of studies and big claims get the screen to themselves (figures exit first).
- Built text is left-aligned so it grows naturally left to right.
- Before rendering, scrub the snapshots and ask of every frame: "where does the eye go?" If there are two answers, cut one.

## Transitions — on time, never overlapping (owner, 10-13)
- A pose change is a **cut** (`DN.swap`), never a crossfade (a crossfade shows a ghost double).
- One thing replacing another: `DN.change(outs, ins, t)` — the old is fully gone (0.22 s) before the new arrives at `t`.
  Notifications: `DN.replace(old, new, t)`. Exits are 0.25 s.
- Scene clears finish ≥ 0.1 s before the next line's first word.
- Gate: `node tools/transition_check.js reels/<reel>` must print `transitions clean` — it scrubs every frame and reports any
  element mid-fade overlapping another. Intended overlaps (a box framing a meter, a figure stepping into a scene, an arrow
  joining two figures) are declared with `DN.allow(a, b)`; nothing else is excused.

## Animated emoji (Google Noto, CC BY 4.0 — credit "Animated emoji: Google Noto Emoji (CC BY 4.0)")
- Baked to sprite sheets (`node tools/emoji_sprites.js <code>` → library/emoji/<code>.png + .sprite.js); never run a Lottie
  player in a reel (it stays on frame 0 under HyperFrames' virtual clock).
- Use inside chat bubbles (`DN.notif(..., { emoji })`) or as a small WhatsApp reaction pill on a bubble (`DN.react(id, code, t)`).
  Never a big emoji floating over a person. Max 1–2 per reel, where a real chat would have them.

## Ins and outs follow the voice (owner, 10-13)
- A visual lands ON the word it shows, and stays up long enough to read: at least about 1 s.
- An exit happens in a PAUSE of the voice, never mid-sentence, and never before the visual's own animation has finished.
  A strike, for example, completes and is held struck for at least 0.4 s before it leaves.
- Show the real thing the voice names. "Sending you memes" means a real meme in her chat; "a real day, a real place" means
  two messages, day then place, each on its word.
- Memes are our own images, generated into library/memes (photo only, no text in the image). The meme text goes on top
  via `DN.notif(id, { img, meme: "top text" })`, in Anton, white with a black stroke. Never use downloaded meme templates.
- Build the story beat by beat before writing code: what the viewer sees on each phrase, and why.

## Glow is restrained (owner, 10-13: "the glow is too much, we're losing the premium-ness")
- Focus rim = a tight purple edge (4 px + 16 px + a faint 34 px). Never the old 60 px purple haze.
- Body halo = 1.5 px + 10 px at low alpha.
- Focus is shown by the rim and by dimming the others, not by a bloom.

## Exit timing: E[li] is NOT when the voice stops
`T.voEnd` (E) includes about 0.35–0.55 s of trailing silence. Time pause exits from the last word's end time:
`T.words[li].at(-1)[2]`. Exits timed from E land after the next line has started.
