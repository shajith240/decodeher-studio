# Mistakes log

Every mistake that reached the owner. Each one is a rule now; the fix is in the code or the rules.

| Date | What the owner saw | Cause | Rule / fix |
|---|---|---|---|
| 10-12 | Hand-drawn illustrations rejected | Claude drew the visuals itself | Visuals come from the asset library, never improvised SVG art → [[rules/visuals-and-motion]] |
| 10-12 | Stock-footage montage rejected | Random Pinterest clips | Black void + cast + graphics only |
| 10-12 | 3D mannequins "look like robots" | Bald mannequin bodies | Cast = photographic silhouettes with real hair/clothes |
| 10-12 | Captions vanished after 22 s | >12 `<video>` tags: HyperFrames drew video over overlays | One footage element max (we use none now) |
| 10-12 | Page froze in tests | Returning the GSAP timeline from `page.evaluate` | Always `{ tl.seek(t); }` with braces |
| 10-12 | Walk-away figure faced the wrong way | CSS flip on a GSAP-animated wrapper | Mirror the inner `<img>`; check the source's facing first |
| 10-12 | Blank render | Hand-counted caption chunks didn't match the words | Captions are chunked automatically |
| 10-13 | Small texts unreadable | 30 px grey labels | Min 38 px, white or purple → [[rules/captions]] |
| 10-13 | White captions looked grey | Vignette layer above the text | Text layers always above grain/vignette |
| 10-13 | Man smaller than woman | One shared scale | Per-character scale: him 1.0, her 0.93 |
| 10-13 | Suspense drone music | Synthesised drone | Calm, non-suspense music only → [[rules/audio]] |
| 10-13 | **Stray dots on screen** | Hidden SVG arrows with round line caps show a dot at dash-offset = length | Graphics are image assets revealed by a wipe; never stroke-dash SVG |
| 10-13 | **Rectangle coming from his crotch** | Message bubble started at a guessed (x, y) | Anything that emits from a body part uses the asset's anchor point, checked on a snapshot |
| 10-13 | "Last words cut" | Final line shown only as 3 big words ("Because" never on screen); cards left before the word ended | Every spoken word appears on screen; a card stays until its last word ends + 0.25 s |
| 10-13 | Thick marker arrows, flat black, floor reflections — "not Dark Needle style" | Guessed his look instead of watching it | Watch his frames first ([[research/darkneedle-visual-grammar]]); stage = `library/stage` components |
| 10-13 | Hidden figures reappeared | `focus/unfocus` changed the wrapper opacity | Visibility on the wrapper, dimming on the inner image (stage.js) |
| 10-13 | Two text blocks on screen together | A block's hold ran into the next line | `DN.say` always clears 0.17 s before the next line starts |
| 10-13 | Long line wrapped to 4 lines into the meters | Fixed font size | Max 3 lines: pass a smaller `size` for long lines (≥ 13 words → 64 px) |
| 10-13 | Investment beat cluttered: sentence + 2 meters + citation + 2 figures at once | Everything placed on one line's time | Breathing rule: one focus at a time, graphics leave when done → [[rules/visuals-and-motion]] |
| 10-13 | Background music "looks like shit" (hip-hop beat) | Picked from search results without hearing it | Owner picks music by ear from rendered options → [[rules/audio]] |
| 10-13 | Citation flashed for 60 ms | Tied to two words 0.46 s apart | Graphics are timed to the phrase, and a hold is ≥ 1 s |
| 10-13 | Captions "look AI-generated" | Oswald + purple glow + rise/pop motion | His font (Barlow Semi Condensed 700), plain white, flat purple accent, words just appear |
| 10-13 | Assets overlapping for fractions of a second | Crossfaded pose swaps; 0.45 s exits overlapping entrances; notif swaps one frame late | Cuts for poses, `DN.change`/`DN.replace`, and the frame-by-frame transition gate |
| 10-13 | Facing labels wrong for 7 stills (agents caught it) | Judged from 300 px thumbnails | Check facing on a head close-up (top 22% crop, large) before labelling; agents verify, don't trust the index blindly |
| 10-13 | Week 1 felt like "a facts channel / random ChatGPT advice" | Every reel built around "a study found…" | Relatable story structure, no study framing → [[rules/script-and-hooks]] |
| 10-13 | Characters too big for the frame | 1350 px figures, feet cropped, in Instagram's bottom UI zone | 760 px, feet at y 1300, text above heads → [[rules/layout]] |
| 10-13 | Arrows placed oddly | Coordinates guessed by eye | Measured anchors (`tools/anchors.py`) + `DN.point/DN.ahead` |
| 10-13 | Same words 3× at once (voice + caption + tag/notif) | Captions carried every word while tags/notifs repeated them | Text appears once: quotes only in notifs, lists only as tags; `tools/repeat_check.js` gate |
| 10-13 | Narrator spoke her line as if it were his ("This week is crazy, sorry") | Unattributed dialogue in the script | Attribute every quote: "She says, …" |
| 10-13 | Caption, message box and figure crowded together | 40 px gaps | Layers y 250–380 / 480–640 / 690+ (`DN.LAYOUT`) |
| 10-13 | Reels ended with no spoken call to action | CTA only as a small end-card tag (follow prompts avoided on research) | Every script ends with a spoken CTA line incl. "follow for more" |
| 10-13 | Captions "look generated, not edited" | Uniform-size word build-up | Lockups: one phrase at a time, one dominant word 1.8× |
| 10-13 | Spotlight lit the captions — "looks artificial" | Light cone from the top of the frame | Light starts above the heads and pools on the people; caption band dark |
| 10-13 | Lockup captions with a bounce "look like shit" | Tried a premium-editor trend the owner didn't want | Plain word-by-word captions stay (lockup off) |
| 10-13 | Spotlight on during text-only moments | Light was always on | Light follows the figures (`DN.finish`) and starts at the caption's bottom edge |
| 10-13 | "1:07 AM" tag repeated the caption | Decorative tag with the same info | Put times where they live: in the chat bubble's timestamp |
| 10-13 | Shimmer too fast and on every accent | Auto sweep, 0.6 s | Opt-in, 1.4 s, punch word + "follow" only |
| 10-13 | Invented notification cards | Made-up UI | Exact WhatsApp dark-mode bubbles |
| 10-13 | Captions slightly ahead of the voice | Word times estimated from character counts | Times measured from the audio (align_words.py) + 30 ms |
| 10-13 | CTA shown as one paragraph | One text block for two sentences | `DN.cta`: share line, then FOLLOW FOR MORE alone |
| 10-13 | Chat bubbles on the wrong side (hers above him) | Copied WhatsApp's left/right literally while he stands left, she right | Bubbles sit on the speaker's side; tail toward the speaker |
| 10-13 | "AN" flickered at the end of Monday | A punch word spoken in 0.14 s got its own card | Punch cards hold ≥ 0.4 s (fast words merge); `tools/flicker_check.js` gate |
| 10-13 | Tuesday's ❤️ bubble never left | My sed put a `// comment` mid-line, which disabled the next statement; gates flagged a layout issue but the batch rendered anyway | Never put comments inside a one-line replacement; `flicker_check` now fails STUCK bubbles/tags (> 8 s); `tools/build_reel.sh` refuses to render on any failed gate |
| 10-13 | Emoji "not animating, too big over her head" | Lottie player not loaded under HyperFrames' virtual clock → frame 0; 130 px floating emoji | Baked sprite sheets driven by the clock; small reaction pills on bubbles |
| 10-13 | Gate false-alarm on counters | flicker_check keyed elements by text | Track elements by id |

## 10-13 — animations cut short, story not shown
- The "she's just busy" strike was hidden 0.18 s after it began, so the viewer never saw it finish. Exits now sit in voice pauses.
- "She's sending you memes" showed no memes. Visuals now show what the voice says.

## 10-14
- **A camera cut pushed the bed figure into the meme.** The camera measured clearance before the photo had loaded, so the bubble was 0 px tall.
  - Photo size is now reserved in CSS.
  - The camera now checks clearance over the next 2 s.
  - New gate: tools/figure_ui_check.js.
- **The outro video was frozen.** It was injected at runtime, and HyperFrames never saw it. Media must be static in the HTML.
- **The outro title sat 430 px off-centre.** For centred `DN.say`, x is the CENTRE (540), not the left edge.
