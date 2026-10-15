# Pinterest refs B: two "premium edit" reference reels (videos 3 and 4)

Sent by the owner as the premium style to copy and as a source of editing and content tips.
Method: yt-dlp download, faster-whisper `small` word timestamps, 1 fps contact sheets, 30 fps strips around 12 text/transition
moments, and RMS levels of the audio in 50–100 ms windows. All times are seconds from the start. Whisper word starts are
accurate to roughly ±0.1 s, so "lag" figures under 0.15 s count as "on the word".
Scratch evidence (not kept in the vault): `scratchpad/pins/b/` (v3/v4 mp4, `*.pcm.words.txt`, `v3-sheet.jpg`, `v4-sheet.jpg`, `strip-*.jpg`, `cap-*.jpg`).

| | Video 3 | Video 4 |
|---|---|---|
| URL | https://pin.it/1msYsie4r | https://pin.it/4VpBYcHN1 |
| Length / format | 60.1 s, 720×1280, 23.98 fps | 98.6 s, 720×1280, 23.98 fps |
| Speech | 228 words, **3.8 words/s** | 399 words, **4.1 words/s** |
| Pauses ≥ 0.3 s | 10 (0.30–0.40 s) | 14 (0.30–0.64 s) |

Both come from the same creator: a talking head in a dark room with coloured practical light, aimed at content creators.
We copy the **grammar** only, never their words, face or artwork.

---

## Video 3: "Turn one idea into 7 hooks"

### 1. What it is and who it is for
A content-strategy reel for creators. It takes one dull topic (protein powder) and voices it as 7 different hook types.
Each type gets a numbered chapter card on a black/purple void, followed by a short demo. A "commercial break" in the middle
holds a comment-keyword lead magnet. The last line ("Here's how.") loops seamlessly into the first line ("Here's how to turn…").

**The tips it teaches, paraphrased:**
1. One idea can carry many hooks. Don't hunt for new topics; re-angle the same one.
2. **Set the scenario**: drop the viewer into a specific moment ("you just left the gym, no time…") and then offer the fix.
3. **If/then**: "If you struggle with X, it's because you don't know about Y."
4. **Social proof (your own)**: a result plus a timeframe ("30 days of this took me from this to this"), with a before/after.
5. **Borrowed social proof**: name people the viewer already respects who do or believe the thing.
6. **Cost narration**: open with what you spent or tried ("$2,000 and 47 kinds later, this one wins"), then "here's why".
7. **Relate to the viewer**: "Just like you, I used to struggle with X… until I found Y."
8. **The classic**: a plain "here's how / here's why" promise.
9. (Shown, not said) Put the CTA in the **middle** as a framed "commercial break" with a keyword to comment, not at the end.
   Then **end on a line that loops** into the opening.

### 2. Caption system
- **Font feel:** heavy extended grotesk (Black weight), ALL CAPS, upright by default. **Italic is reserved for emphasis.**
  The hook's second line (0–7 s), "PROTEIN SHAKE" in teal at 18.3 s and the glitched "YOU SHOULD TOO" at 33 s are italic;
  ordinary groups are upright. The fill is a subtle vertical gradient, with a soft dark drop shadow and no outline.
- **Size and position:** centred, the block's centre at about y = 50–54 % of the frame (chest height, below the face).
  The block is about 60–65 % of the frame width, cap height about 48 px on 720 px (≈ 70 px on a 1080 canvas).
  Numbers are about 2× the size of the word under them ("30 / DAYS" at 20.7 s, "$2,000 / THIS MONTH" at 43.1 s).
- **Colour:** two colours per group: white plus **one section accent** that matches the room light of that section
  (red hook / blue-violet title / teal scenarios / red relate section / yellow ad break). **The accent moves between the two lines
  as each line is spoken.** "JUST LEFT" is teal at 9.23 s, then at 9.60 s "THE GYM" turns teal and "JUST LEFT" turns white.
  Same at 52.60→52.80 ("JUST" / "LIKE YOU"), 53.10→53.40 ("I USED TO" / "STRUGGLE") and 53.73→53.93 ("WITH" / "GETTING IN").
  This is **line-level karaoke**: the whole phrase is visible, and colour tells you where the voice is.
- **Words per group:** 1–4 (2 lines of 1–3 words). Measured from 13.4–22.3 s at 10 fps:
  IF YOU 0.2 s · HAVE A HARD TIME 0.7 · GETTING YOUR 0.3 · PROTEIN IN 0.5 · THEN IT BECAUSE 0.5 · YOU 0.3 · DON'T 0.2 · KNOW 0.3 ·
  ABOUT 0.2 · THIS 0.2 · PROTEIN SHAKE 0.8 · 30 DAYS 0.4 · AND THIS PROTEIN SHAKE 1.1.
  Mean **0.44 s per group, about 2 words per group**. Content phrases (nouns, payoffs) hold 0.7–1.1 s; lone function words flash for 0.2–0.3 s.
- **Words per second:** shown ≈ spoken (≈ 4.5 shown vs 3.8 spoken in that window). Every word appears; nothing is summarised,
  **except under chapter cards**: 7.27–8.9 s and 24.9–26.9 s show no captions while the voice speaks. The card's 2–4 words stand in for the sentence.
- **Unit:** per phrase. The whole group appears at once and is never built word by word.
- **Lead/lag:** groups land 0.0–0.17 s after the spoken word ("I"@52.94 → 53.10; "$2,000"@43.12 → 43.10; "30"@20.54 → 20.70).
  They are **on the word or slightly behind, never ahead**.
- **Context-mimic style switch:** during the "commercial break" (33.7–36 s) the captions turn into small lowercase white italic,
  one word at a time ("quick", "commercial", "break"), over a fake YouTube ad bar with "Skip Ad". The caption style changes with the fiction.

### 3. Text animation vocabulary (Video 3)
| # | Entrance / exit | Frames (evidence) | Used for |
|---|---|---|---|
| A | **Opposed horizontal slide-in**: line 1 from the left, line 2 from the right, strong ease-out, no overshoot. Line 1 also fades pale pink→red | 0.00→0.20 s, ~6 frames | The hook title only. It stays up about 5 s while the hook is spoken |
| B | **Hard cut on** (1 frame), hard cut off | 9.20→9.23, 43.07→43.10, 53.07→53.10 | ~90 % of caption groups |
| C | **Colour pass between lines** (white↔accent, 1 frame) | 9.60, 52.80, 53.40, 53.93 | Tracks which line is being said: line-level karaoke |
| D | **Colour-scheme swap** of the same title (red/white → white/blue) together with a grade change | 2.30→2.33 on "seven" | A keyword turning point in the hook |
| E | **Number settle**: numeral slightly big and low, scales down and rises into place, ease-out, no overshoot | 20.70→20.87, ~5 frames | Numbers and stats ("30 DAYS") |
| F | **Flash-in card**: white frame for 2 frames, then the photo fades up out of white | 24.30→24.43 | Proof image ("AFTER") |
| G | **Chapter card**: hard cut to a black-purple void. The numbered wheel segment fades in while rotating into place, power3-like settle | 7.27→7.47 fade, settles by ~7.9 (≈0.6 s); holds ~1.6–2.0 s | Section/list item ("1 SET THE SCENARIO" … "7 THE CLASSIC") |
| H | **Glitch transition**: RGB split plus slice displacement over the whole frame | 33.23→33.67, 13 frames | Once only: a tonal break into the ad segment |
| I | Annotation graphics: a hand-drawn teal circle around the product (22 s); B&W cut-out celebrities behind the speaker (26.9–30 s), already in place on the cut | 22, 26.92 | Pointing at a thing / naming people |

### 4. Premium signals (Video 3)
- **The chapter cards are our house style already:** near-black void, a radial purple glow, one glowing object (a light bulb),
  one bold label. They hold **0.7–1.1 s past the end of their words** (card 1: words end at 7.78, card holds to ~8.9;
  card 4: words end 26.16, card to 26.88). Breathing room comes from holding a still frame, not from slowing the voice.
- **J-cuts:** the next section's voice starts under the card ("Sam"@26.56 is spoken while card 4 is still up, and the picture cuts at 26.92).
- **The colour world changes per section.** Grade and caption accent change together, so each hook type feels like its own room.
- **Camera:** slow push-ins on the talking head (26.92→27.02 the face grows), jump punch-ins (43.0→43.1) and a camcorder "REC"
  viewfinder overlay with timecode on the demo sections.
- **Sound (measured, not heard):** a continuous bed sits ~20 dB under the voice (gaps rest at −27 to −35 dBFS). It **drops to near
  silence (−44 to −55 dBFS) for 150–250 ms right before key lines**: 33.25–33.40 (before the ad break), 46.25–46.40 (before
  "this protein shake… by far the best"), 49.25–49.45 (before "Here's why") and 58.95–59.05 (before the loop line "Here's how").
  Loud transients at 7.25 s and 13.3 s, as each card lands, fit a hit or whoosh, but this cannot be confirmed without listening.
- **Ending loops** into the opening sentence, so there is no "outro" feeling.

---

## Video 4: "Stop using call-to-actions"

### 1. What it is and who it is for
A tutorial for creators. Generic end CTAs ("follow for more", "like", "save") tell the viewer the video is ending, so they scroll.
Watch time drops, and so does ranking. The fix is a **seamless loop**, shown with a screen recording of a script doc and an
editing timeline. The video loops itself: the last words "…then you should" run into the first words "Stop using call to actions".

**The tips it teaches, paraphrased:**
1. Don't end on a generic CTA (follow / like / save). It announces "the video is over" and cuts average watch time.
   On screen at 8.1–10.0 s, a red progress bar with a marker labelled **"FOLLOW FOR MORE"** sits at the very end of the bar.
2. End on a **loop** instead. The viewer never knows when the video ends, and a rewatch starts by itself.
3. How to write the loop: take your hook, put a comma in front of it and write a **linking phrase** so that
   "[linking phrase], [hook]" reads as one sentence.
4. Record that full sentence in one take with a **slight pause at the comma**.
5. In the edit, cut at the comma. The second half stays as the opening hook; the first half moves to the very end.
6. A CTA is fine **if it has a real purpose**, e.g. "comment WORD to get X" (a lead magnet). Random habitual CTAs should go.

### 2. Caption system
- **Font feel:** the same heavy extended grotesk, ALL CAPS, **upright**. The title's bottom line is red with a gradient
  (red → pink); white lines have a top-to-bottom silver gradient and a soft shadow.
- **Size and position:** centred, y ≈ 48–54 %, cap height about 45–50 px on 720.
- **Colour:** white plus a section accent tied to the grade: **red** for the problem section (0–30 s), **yellow-green** for the
  how-to/editing section, **purple** for the "important purpose" exception (88–90 s).
- **Words per group:** 2–3. Measured 4.9–12.0 s: EVERY SINGLE CTA 0.9 s · LIKE THIS 0.6 · SHOULD SCROLL 0.8 · AND BECAUSE 0.6 · OF THAT 0.5.
  Mean **0.68 s per group, ~2.2 words**. Between them, **graphics replace captions**: the views counter (1.6 s), the progress
  bar (2.0 s) and the audience-retention graph (12.0 s → ~17 s) are shown with **no caption**.
- **Long stretches without captions:** 37–56 s (doc screen recording; the text being typed is the caption) and 70–86 s (editing timeline).
- **Ghost-karaoke quote (61.77–63.6 s):** the whole quoted sentence is laid out at once in a lighter sentence-case sans
  (Medium weight, white, with quote marks) at about **20 % opacity**. Each word steps to 100 % as it is spoken:
  "If"@61.76 → lit 61.90 · "your"@61.90 → 62.03 · "trying"@62.06 → 62.20 · "to"@62.24 → 62.30 · "get"@62.38 → 62.47 ·
  "more"@62.52 → 62.60 · "views"@62.72 → 62.80. Each step takes 1 frame and lags ~0.1 s. **The reader can read ahead, and the voice is tracked.**
- **Unit:** per phrase (main captions) or per word lit inside a visible sentence (quotes).
- **Lead/lag:** "Every"@4.86 → text on screen from 5.02 (~0.15 s); everything else on the word.

### 3. Text animation vocabulary (Video 4)
| # | Entrance / exit | Frames (evidence) | Used for |
|---|---|---|---|
| A | **Static title from frame 0** (no animation), held ~2 s | 0.00–2.0 | The hook title |
| B | **Blur-rise**: the new shot and the text rise from below with heavy vertical motion blur and settle with ease-out. Line 1 leads line 2 by ~2 frames. No overshoot | 4.85→5.12 (~8 frames); same at 10.05→10.25 "SHOULD SCROLL" | The first phrase of a new beat or point after a graphic |
| C | **Hard cut** on/off | 5.80→5.90 "LIKE THIS", 10.9 "AND BECAUSE" | Ordinary follow-on phrases |
| D | **Number roll-down**: an eye icon plus a big number counting 60,981→175 while sliding down with vertical blur, then locking | 6.47→6.87 (12 frames) | Stats / "this is what happens to your numbers" |
| E | **Progress bar fill** with a pointer and a small label | 8.1→10.0 | Showing a concept ("the end of the video") |
| F | **Ghost then light-up per word** | 61.77→63.6 | A quoted sentence / an example line that must be read in full |
| G | **Handwritten-style yellow annotation word** ("slight pause"), fades out in ~4 frames | 61.60→61.73 | Meta note / instruction |
| H | **Shimmer sheen**: a light band sweeps through the purple word repeatedly, ~0.35 s per pass | 88.40→89.6 "IMPORTANT" | The single emotional/payoff word of the exception |
| I | **Cross-dissolve** (~6 frames) | 55.90→56.07 (doc → face) | Leaving a screen recording |
| J | **Dip to black** (~5 frames), the caption dips with the picture; the grade changes across it (purple → yellow) | 56.77→56.93 | A section change inside one thought |

### 4. Premium signals (Video 4)
- **Graphics replace text instead of doubling it.** Counter, progress bar and retention graph each carry a 1.6–5 s stretch with no caption.
  This matches our rule "the visual is the caption".
- **Grade = meaning:** red = problem, yellow = how-to, purple = the important exception. The caption accent follows the grade.
- **Device mock-ups:** the reel's own title shown on a phone (2–5 s), then the final video on a phone (82–86 s). The proof is the thing itself.
- **Screen recordings are zoomed** to the line being edited (39–56 s): the camera pushes toward the cursor, so the frame stays legible.
- **Sound (measured):** the bed rests around −30 to −40 dBFS in gaps (less dynamic than video 3). Deepest dips (−40 to −45) at
  67.3, 74.6, 83.4 s, just before the demo repeats the loop sentence.
- **The ending is the loop it teaches.**

---

## Cross-video findings: why the refs read "premium" and still feel readable

1. **Short, whole phrases, never words flying in one by one.** 1–4 words, the whole group at once, in one fixed place.
   Their groups are often *shorter* on screen (0.2–1.1 s) than ours. They read anyway because (a) the eye never chases motion,
   (b) the font is huge and centred, and (c) colour, not movement, marks the spoken word. **Our problem (a) is not only speed.
   Building each phrase word by word, with every word sliding in, keeps the text moving and unfinished, so the eye never gets a resting frame.**
2. **Motion is rare and means something.** About 90 % of caption changes are hard cuts. Animated entrances are kept for: the hook title,
   the first phrase of a new beat (blur-rise), numbers (roll / settle), section cards, and one shimmer on one key word.
3. **Holds come from cards and graphics, not from slow captions.** A card or graphic holds 1.5–5 s while the voice keeps going,
   then captions resume. These are the reels' breathing points.
4. **The colour world is tied to the section.** The accent colour and the grade change together at each new section.
5. **Silence before the payoff:** 150–250 ms drops in the bed right before key lines.
6. **No bounce or overshoot anywhere.** Every settle is a clean ease-out, which fits the owner's 10-13 rejection of bounce.

---

## 5. Recommendations for OUR reels (@thedecodeher)

### 5a. Readability fix (complaint a)
- **Show the whole phrase at once.** Stop building it word by word. Keep two-tier: small white top line plus big purple key line,
  both appearing together.
- **Track the voice with opacity, not motion (ghost-karaoke from v4 61.8 s):** words not yet spoken sit at **35 % opacity**
  (20 % in the ref is too faint on pure black with thin type) and step to 100 % as spoken: `opacity .35→1, 0.08 s, "none"`, keyed to
  `tools/align_words.py` times + 30 ms. The phrase is readable early, and the "never ahead of the voice" rule still holds for the *lit* words.
  Alternative: v3 line-level karaoke, where the key line is white until it is spoken and then turns purple.
- **Max 4 words per group** (2 lines: top ≤ 3, key ≤ 2). Break at punctuation or breath; never split an article or "her" from its noun.
- **Minimum on screen: 0.9 s per group.** Merge any group that would be shorter into its neighbour. The refs' 0.2–0.3 s single-word flashes are
  function words, and we should merge them, not copy them. Our deep narrator at speed 1.1 is slower than the refs (≈ 2.5–3 vs 3.8–4.1 words/s),
  so 2–4-word groups naturally last 1–1.6 s.
- **Payoff / key phrase: hold ≥ 1.4 s**, until the last word ends + 0.4 s. On the beat's last group, hold through the following pause.
- **Max ~1.2 caption changes per second** averaged over any 5 s window (refs reach ~2/s, but they talk faster and use more cards).
- **Let visuals carry stretches:** while a chat bubble, tag or chapter card is up, no caption (already a rule). Aim for ≥ 1 caption-free stretch of
  1.5 s+ every ~10 s.

### 5b. Animation vocabulary to add (complaint b): one meaning per animation, no bounce
| Moment / word type | Animation | GSAP |
|---|---|---|
| Ordinary follow-on phrase (default, ~70 %) | **Cut in, cut out** (v3/v4 B/C) | `tl.set(el,{autoAlpha:1}, t)`; out: `tl.set(el,{autoAlpha:0}, t2)`. Optional 2-frame soften: `autoAlpha 0→1, 0.07 s, "none"` |
| **Question / setup line** ("why would she…") and the first phrase of a new beat | **Blur-rise** (v4 4.85→5.12) | `fromTo(lines,{y:40, filter:"blur(10px)", autoAlpha:0},{y:0, filter:"blur(0px)", autoAlpha:1, duration:0.28, ease:"power3.out", stagger:0.06})` |
| Owner's **"slide" for "why would she…"** | **Short horizontal slide, no overshoot**, line 1 from the left and the key line from the right (v3 hook, 6 frames) | `fromTo(top,{x:-60,autoAlpha:0},{x:0,autoAlpha:1,duration:0.22,ease:"power3.out"})` + key line from `x:+60`, 0.04 s later. Use it on questions only, never on every word |
| **Soft / emotional word** ("date", "love", "miss") | **Fade + de-blur in place** (not in the refs; our answer to the owner's "fade for date") | `fromTo(word,{autoAlpha:0, filter:"blur(8px)", scale:1.04},{autoAlpha:1, filter:"blur(0px)", scale:1, duration:0.45, ease:"power2.out"})` |
| **Numbers / stats** ("3 seconds", "80 %") | **Number roll** (v4 D) or **settle** (v3 E). The numeral is 2× the word under it | roll: `to(obj,{val:target, duration:0.45, ease:"power2.out", snap:{val:1}, onUpdate})` with `y:-24→0` and `blur(6px)→0` over the first 0.3 s. Settle: `fromTo(num,{scale:1.12,y:12},{scale:1,y:0,duration:0.18,ease:"power2.out"})` |
| **Payoff / punch word** | Cut in, then **one shimmer pass** after it lands (v4 H, slowed to one pass) | existing `shine`, ~0.6 s, `"sine.inOut"`, starts 0.25 s after landing |
| **List item / section** ("sign #2") | **Chapter card** on the void (v3 G): number + 2–3-word label, glow builds | card in: `autoAlpha 0→1 + rotation -8→0, 0.5 s, "power3.out"`; hold ≥ 1.6 s and ≥ 0.7 s past its words; captions off while it is up |
| Quoted line she/he says (no bubble) | **Ghost-karaoke** (v4 F) in a lighter weight, sentence case, with quote marks | words `opacity .25→1, 0.06 s` on each word start |
| Exits at a beat change | **Dip** (v4 J) or a fast fade | `autoAlpha→0, 0.15 s, "power1.in"`; between beats, a 5-frame dip of the whole stage |
| Proof / screenshot / chat bubble appearance | **Flash-in** (v3 F) | `fromTo(card,{filter:"brightness(3)"},{filter:"brightness(1)", duration:0.12, ease:"power1.out"})` + `autoAlpha 0→1, 0.06 s` |

Do **not** adopt: the glitch (v3 H). It is used once for a joke; it would read cheap on our page and break "no flashy transitions" (audio rule, owner).

### 5c. Premium polish (complaint c)
- **Breathing room:** each chapter card or key graphic holds 0.7–1.1 s past its words. Add a 0.3–0.5 s held frame (picture still,
  bed only) before the payoff line.
- **Bed drop before the payoff:** duck the music to near silence for 150–250 ms just before the punch line, then back up under the voice.
  This needs no new SFX, so it fits the "no whooshes" rule. The owner should approve it by ear.
- **Camera:** a slow 3–4 % push-in on the silhouette stage across each beat (`scale 1→1.04, beat length, "none"`), and a 6–8 % punch-in
  (cut, not tween) on the punch line. The refs never zoom out mid-sentence.
- **Section colour:** keep purple as the brand accent but allow **one alternate accent per beat type**, e.g. a deep red for "red flag" beats,
  with the rim light of the silhouettes changing with it. In the refs this does most of the "designed" feeling. Owner decision.
- **Italic as emphasis:** the refs set ordinary lines upright and only emphasis italic. Our Montserrat Black Italic everywhere removes
  that contrast. Option: top line upright Montserrat 800, key line italic 900.

### 5d. Script / structure tips to adopt
- **Hook formulas from v3, mapped to dating psychology:** set the scenario ("You text her good morning, she replies 6 hours later…"),
  if/then ("If she does X, it's because…"), borrowed authority (a named study or psychologist rather than celebrities),
  cost narration ("I read 40 studies on attraction, this one matters most"), relate ("Just like you, I used to…") and the plain "here's why".
  Rotate them across the week instead of one formula.
- **Loop endings (v4):** write the last line as a linking phrase that runs into the hook. Example: "…and that's exactly why, / she stops replying
  after the second date." Record or generate it as one TTS sentence with a slight pause at the comma, then cut at the comma.
- **⚠ CTA conflict, for the owner to decide:** our rule [[rules/captions]] / memory "CTA rule" says every reel ends with a spoken
  "follow for more". Video 4's main tip is the opposite. It shows "FOLLOW FOR MORE" at the end of a progress bar as the thing that makes
  people scroll (8.1–10.0 s), and video 3 places its CTA mid-video as a "commercial break" with a comment keyword.
  Options: (1) keep the end CTA (current rule); (2) move "follow for more" to a mid-roll beat at ~60 % and end on a loop; (3) end with a
  purposeful CTA only ("comment SIGNS and I'll send you the list"), which v4 explicitly allows. Do not change the rule without the owner.

## Storyboard template (from v3's structure, our cast)
1. Hook title, 0–3 s: two-line title, opposed slide-in 0.22 s, held while the hook is spoken.
2. Chapter card "1 · <label>", 1.6–2.0 s: void, glow, no captions.
3. Demo beat, 4–7 s: phrase captions (cut-in default, blur-rise on the first phrase), one graphic that replaces captions for ≥ 1.5 s.
4. Repeat 2–3 per item. Number or emotional word gets its own animation.
5. Mid-roll purposeful CTA (if the owner chooses option 2/3).
6. Last line = linking phrase that loops into beat 1.

## Proposed rules (for the main agent to merge after owner approval)
1. Captions: the whole phrase appears at once (≤ 4 words, 2 lines). The spoken position is shown by opacity (35 %→100 %) or a colour pass,
   never by sliding each word. This replaces "built word by word" and the per-word slide from the right in two-tier mode.
2. Captions: min 0.9 s on screen per group; payoff groups ≥ 1.4 s; merge shorter groups.
3. Text animation follows meaning: cut-in (default) · blur-rise (question / new beat) · fade+de-blur (soft emotional word) ·
   number roll/settle (numbers) · shimmer once (payoff) · ghost-karaoke (quoted line). No bounce or overshoot in any of them.
4. Chapter cards for list items hold ≥ 0.7 s past their words, with captions off.
5. Audio: a 150–250 ms bed drop before the payoff line (owner to approve by ear).
6. Script: rotate the 7 hook formulas; write a loop line. The CTA placement question goes to the owner (see ⚠ above).
