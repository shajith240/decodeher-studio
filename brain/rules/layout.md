# Layout (strict) — composition for Instagram Reels (1080×1920)

Evidence: [[research/reels-composition]]. Instagram's UI covers the top ~270 px and the bottom ~670 px (caption, audio, buttons);
the right rail x 850–1080 is covered from about y 1100 down. The profile grid shows only the middle (y ≈ 240–1680, safest 420–1500).

- **People**: a standing person is **640 px** tall (`DN.cast` default), feet at **y 1330**, so the head top is ~690.
  Him at x 340 facing right, her at x 740 facing left (≥ 150 px gap); lead room ≥ 300 px in the direction a person faces.
  One person alone: x 420–540, facing into the empty side. Never crop feet or heads. Stills with furniture: width 640–760.
- **Three layers that never fight** (owner, 10-13: "add padding so they don't fight for attention"):
  story text **y 250–380** (60 px, ≤ 2 lines) → ~90 px air → dialogue notif **y 480–640** → ~50 px air → heads from **y ~690**.
  With no notif on screen the text may take 3 lines.
  A line alone on the dark (no figures on screen): 90–110 px, y 640–1000.
- **Graphics/UI**: notifs, tags and arrows sit between y 500 and 1250, never in x ≥ 850 below y 1100.
- **Nothing** but glow/background below y 1300.
- Arrows start and end at measured anchors: `DN.ahead(id)` / `DN.point(id, "eye"|"head"|"top")` — never guessed coordinates.
- Gates: `page_errors.js`, `reel_check.js` (overlap + safe area), `transition_check.js` and `repeat_check.js` must pass.
