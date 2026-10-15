# @zoltium: storytelling and pacing, reverse-engineered (2 reels, 2026-10-14)

Competitor: @zoltium (1.2M followers). A faceless dark-psychology / self-improvement page with a cracked-porcelain-mask logo; it sells an ebook ("The Power Code").
Sources: `z1.mp4` (54.5 s, 1080×1920, 60 fps) is a "brain fact" explainer. `z2.mp4` (37.2 s, 30 fps) is an ad for their ebook.
Evidence lives in the session scratchpad `zol/v/`: 2 fps contact sheets (`z1_sheet0-3.jpg`, `z2_sheet0-2.jpg`), 10 fps strips (`strip_*.jpg`),
transcripts with word timestamps (`z1.json`, `z2.json`, faster-whisper small), and our own `w1-01-busy` FINAL at 1 fps (`ours_sheet.jpg`) for comparison.
Audio and sound design are out of scope here; the lead is covering them.
Whisper mishearings fixed by reading the on-screen text: "Zolteum" is ZOLTIUM, and "Invisible. Too irresistible." is the book subtitle "Invisible to Irresistible".

**The finding in one line:** Zoltium's narrator does **not** talk faster than ours (138–147 wpm against our 140 wpm on w1-01). What changes is the picture.
**The whole frame changes every ~1.5 s, on every 2–4-word caption group, and each new image is a literal or metaphorical picture of that group.**
Ours keeps one wide composition for 4–8 s and changes only small elements inside it (a bubble, a tag). The viewer has to supply the pictures in their own head,
and that is the "needs high concentration" feeling the owner describes.

---

## Video 1: "Your brain fools you" (z1, 54.5 s)

### 1. Transcript (segment start–end, s)
| t | line |
|---|---|
| 0.00–6.24 | Your brain fools you into telling your plans to others, so you don't actually have to achieve them. |
| 7.40–7.90 | Sound weird? |
| 9.02–12.32 | Believe it or not, your brain doesn't care about your success. |
| 13.28–16.12 | It's wired to keep you alive and save energy. |
| 17.34–23.82 | When you tell someone your plans, your brain releases the same chemicals as when you have already achieved them. |
| 24.60–28.04 | Your brain can't tell the difference between reality and imagination. |
| 28.76–37.68 | This makes you feel like the job is done, and you subconsciously lose the motivation to finish it without even realizing it. |
| 38.78–43.50 | And this is how you get fooled, wondering why you can't achieve anything in life. |
| 44.96–48.52 | Now listen carefully, you may not see us again. |
| 49.66–52.26 | Join ZOLTIUM and learn to become powerful. |

### Story beats
| beat | t | content | device |
|---|---|---|---|
| **Hook** | 0–6.2 | A counter-intuitive accusation: your own brain is tricking you, and the motive is a payoff you would never admit to ("so you don't have to achieve them") | Gives the effect and withholds the mechanism, which opens a curiosity gap ("how? why?") |
| **Pattern interrupt** | 7.4–7.9 | "Sound weird?" on pure black | Says the viewer's objection for them; the frame empties so the question lands |
| **Setup** | 9.0–16.1 | "Believe it or not" → your brain doesn't care about success; it is wired for survival and saving energy | Personifies the brain as an agent with its own motives, the villain inside you |
| **Tension / mechanism** | 17.3–28.0 | Telling people releases "the same chemicals" as achieving; the brain can't tell reality from imagination | The mechanism comes in two steps, each a short declarative claim |
| **Reveal / twist** | 28.8–37.7 | So you feel done, and you lose motivation "without even realizing it" | Makes it invisible and unconscious, which is the "dark" part: it happens to you |
| **Payoff (callback)** | 38.8–43.5 | "And this is how you get fooled, wondering why you can't achieve anything in life." | Closes the hook's loop word for word ("fools" → "fooled") and raises the stakes from a small habit to your whole life |
| **Ending / CTA** | 45.0–52.3 | "Now listen carefully, you may not see us again. Join ZOLTIUM…" | Scarcity / threat CTA with a secret-society tone |

Narration devices, with evidence:
- **Second person:** 17 of 122 words are "you/your" (14 %). The brain is "your brain" four times, so the viewer is both the victim and the culprit.
- **Curiosity gap / open loop:** opened at 0–6 s ("fools you"), deliberately not explained for 11 s, mechanism at 17–28 s, loop closed at 38.8 s with the same verb.
- **Objection voicing:** "Sound weird?" / "Believe it or not". The reel argues with the viewer's doubt before the doubt hardens into a swipe.
- **Personification as metaphor:** the brain "fools", "doesn't care", is "wired". It is the only metaphor, and it carries the whole reel.
- **Stakes ladder:** plans → motivation → "anything in life". Each beat is a bigger loss than the last.
- **Dark / forbidden framing:** "fooled", "subconsciously", "without even realizing it", "you may not see us again", "become powerful".
- **Accuracy:** loose. The real finding (Gollwitzer et al. 2009, "symbolic self-completion" for *identity* goals) does not say "same chemicals", and it does not say the brain "can't tell reality from imagination".
  We do not copy that level of claim ([[rules/script-and-hooks]] rule 7: honest and narrow).

### 2. Hook (0–3 s), from the 10 fps strip
- 0.0–0.2: fade up from black.
- 0.2–1.7: a hand-drawn scribbly black brain with a **toothy mouth and a lolling red tongue**, red lightning strokes, on grey paper. The lines "boil" (redrawn every frame).
  It morphs into a normal brain with a scribble storm-cloud circling above it. Caption "Your brain fools you" appears at 0.3 s, on the first word.
- 1.72: hard cut to a green cartoon monster mouth **chomping** (open and closed alternate every ~0.2–0.4 s) under "into telling your".
- 2.7: the caption swaps to "plans to others,". 3.15: hard cut to a yellow card where a crowd of cartoon people **pop in one by one** on "others".
- Why it stops the scroll: the first picture is a grotesque *living* brain (motion and a face in frame one), and the first words are an accusation about *you*.
  Three different images in 3 s. The open question ("fools me into what?") is not answered until the end of the sentence.

### 3. Shot log (z1)
Cut times come from ffmpeg scene detection plus the frames. Voice times come from the word timestamps.
| # | start–end | on screen | voice | in / transition |
|---|---|---|---|---|
| 1 | 0.0–1.72 | scribble brain with mouth/tongue → plain brain + scribble cloud (frame-by-frame morph) | Your brain fools you | fade from black |
| 2 | 1.72–3.15 | green monster mouth chomping on red paper | into telling your / plans to others, | hard cut (tiny crossfade 2.6) |
| 3 | 3.15–4.0 | crowd of cartoon people popping in, yellow | plans to others, | hard cut |
| 4 | 4.0–6.8 | blue creature lounging upside-down, Rubik's cube, pencil | so you don't actually / have to achieve them! | cut |
| 5 | 6.8–6.95 | **image overexposes to white paper (2 frames)** | (silence starts 7.0) | flash |
| 6 | 6.95–8.85 | pure black, text only: "Sound" → "weird?" | Sound weird? | cut to black (voice ~0.4 s after) |
| 7 | 8.85–10.25 | bear on a pool float sipping a drink, rubber duck | Believe it or not, | hard cut |
| 8 | 10.25–11.88 | brain wearing sunglasses sunbathing; birds fly past | your brain doesn't / care about | cut |
| 9 | 11.88–13.23 | gold "#1" trophy; a creature pops out of it | your success. | cut |
| 10 | 13.23–15.62 | one man with phone: on toilet → couch → plate of steak → bed (background swaps ~0.5 s) | It's wired to / keep you alive | in-shot montage |
| 11 | 15.62–17.05 | pale sleepy man slumped at laptop | and save energy. | cut |
| 12 | 17.05–17.3 | black | — | cut |
| 13 | 17.3–18.4 | two mirrored line-drawn figures | When you tell / someone your plans, | cut |
| 14 | 18.4–19.48 | red figure spinning into a swirl | someone your plans, | morph |
| 15 | 19.48–20.83 | woman with glasses lying sideways, green drip from her hand | your brain releases | cut |
| 16 | 20.83–22.2 | green ooze dripping down black | the same chemicals | cut |
| 17 | 22.2–23.13 | cartoon cat in a storm of money | as when you have | cut |
| 18 | 23.13–24.55 | cat lying blissed out | already achieved them. | cut |
| 19 | 24.55–26.7 | man in suit gripping head, angry, scribble cloud | Your brain can't tell / the difference | cut |
| 20 | 26.7–27.9 | eye whose iris is a flame; the flame shrinks | between reality | cut |
| 21 | 27.9–29.42 | dreamy green/red ghost figure | and imagination. | cut |
| 22 | 29.42–30.95 | cartoon duck clutching a money pile | This makes you feel | cut |
| 23 | 30.95–32.47 | boy asleep in bed, content smile | like the job is done, | cut |
| 24 | 32.47–36.43 | big round face (rotated 90°); expression changes every ~0.5 s (squint, crossed eyes, wide eyes) | and you / subconsciously / lose the motivation / to finish it. | cut (**longest image hold, 3.96 s**, but it animates throughout) |
| 25 | 36.43–38.38 | grey detective with cigarette; grin droops to dread | without even / realizing it. | cut |
| 26 | 38.38–38.95 | **white paper flash → black** | (silence 38.6–39.1) | flash |
| 27 | 38.95–40.15 | red void with a black lens-eye that blinks/morphs | And this is how | cut |
| 28 | 40.15–41.2 | skull | you get fooled, | cut |
| 29 | 41.2–42.4 | painterly figure engulfed in flame | wondering why / you can't achieve | cut |
| 30 | 42.4–44.35 | face in a cone of light, shrinking away into the dark (zoom-out) | anything in life. | cut, exits by shrinking to nothing |
| 31 | 44.35–47.4 | pure black, text only: "Now," / "listen" / "carefully!" | Now listen carefully, | black hold 3.0 s |
| 32 | 47.4–49.35 | line-art hand with an eye in the palm, animated snake coiling | You may not / see us again! | cut |
| 33 | 49.35–54.4 | purple paper; porcelain-mask shards fly in and assemble with purple lightning (logo build); fades out | Join / ZOLTIUM / and learn to / become powerful! | cut, fade out 54.0–54.4 |

Measurements (z1):
- **33 shots + 2 flash frames, so 35 visual changes in 54.5 s.** Average shot **1.55 s**. **6.4 changes per 10 s.** By window: 0–10 s: 6 · 10–20: 11 · 20–30: 7 · 30–40: 6 · 40–54.5: 6.
- **Longest hold:** shot 24, 3.96 s, an animating face. The longest *static* hold is the black text-only beat, 3.0 s (31).
- **Image vs idea:** 8 sentences = 8 ideas, so one idea every ~6.6 s against one image every ~1.5 s. That is **≈ 4.4 images per idea**.
  The image changes **on every caption group** (2–4 words). The idea changes on every sentence.
- **Cut timing:** cuts land **0–0.25 s before** the first word of the phrase they illustrate (8.85 → "Believe" 9.02; 11.88 → "your success" 12.10; 24.55 → "Your" 24.60; 47.4 → "you" 47.54).
  The picture leads the word slightly.
- **Section markers:** the only non-cut transitions are the white-flash-to-black at 6.8 and 38.4 and the black hold at 44.4. They divide the reel into hook | body | payoff | CTA.

### 4. Visual vocabulary (z1)
- **Assets:** a grab-bag of 2D cartoon clips in many unrelated styles: scribbled brain, indie flat-vector characters, and what look like classic studio cartoon characters (cat, duck).
  The mix is unified by the grade, not by the style. Symbolic objects: trophy (success), green ooze (chemicals), flame eye (imagination), skull (fooled), money (achievement), bed (job done).
- **How each picture relates to its words:**
  - Mostly **literal-ish illustration of the phrase's key noun or verb**: "success" → trophy, "chemicals" → ooze, "fooled" → skull.
  - Sometimes a **mood stand-in**: "doesn't care" → brain in sunglasses sunbathing.
  - At least one **literal lifestyle montage**: "keep you alive" → toilet, couch, food, bed.
- **Animation:**
  - Almost no camera work. The *clips themselves* move: frame-by-frame boil, chomp loops, pop-ins, expression changes.
  - One shrink/zoom-out exit (42.4–44.3) and one logo assembly (49.4–54).
  - No shakes, no speed ramps, no glitches in z1.
- **Text:**
  - Small white **serif** (Times-like), ~40 px cap height on 1080 wide, **dead centre of the frame (y ≈ 50 %)**, sentence case, punctuation kept.
  - **2–4 words per card**, hard swap with no animation; text changes with the voice. Brand name in bold caps ("ZOLTIUM").
  - Tiny mask watermark bottom-centre (~y 86 %) on every frame.
- **Grade:** everything is pushed dark, with heavy vignette, desaturation and a **paper-grain texture over every clip**. That texture is what makes 20+ unrelated cartoons feel like one world.
  The white flashes reveal the texture as blank paper.

### 5. Pacing (z1)
- **138 wpm over the speech span** (122 words, 53 s). Per sentence: 164 · 144 · 162 · 165 · 144 · 139 · **179** · 118 wpm.
- **Pauses:** at sentence ends **0.34–1.14 s, mean 0.53 s**. The longest are 0.82 s before "Sound weird?" and 1.14 s before "Now listen carefully".
  Mid-sentence: no measurable pauses. Whisper word edges abut, so commas get ~0.35–0.46 s and phrases inside a clause run on.
- **Speed-ups:** the mechanism (17–24 s, 165 wpm) and the payoff "And this is how you get fooled…" (**179 wpm, the fastest line**). The pace rises into the reveal, like a rush of realisation.
- **Slow-downs:**
  - "Sound weird?" is isolated on black.
  - "This … makes you feel" (28.76 → 29.76: "This" is held ~1 s).
  - "subconsciously" is stretched (32.88–33.96).
  - The CTA drops to 118 wpm, slow and ominous.
- The slow spots sit on the *dark* words. The fast spots sit on the explanations.

### 6. Ending (z1)
A **CTA, not a loop.** The story loop closes at 43.5 ("fooled" callback). Then black, "Now listen carefully", a threat/scarcity line, and a logo build on purple.
The last line ("become powerful") does not feed the first line. The callback to the hook happens *before* the CTA, so the story feels finished and the CTA reads as a separate coda.

---

## Video 2: "The Power Code" ebook ad (z2, 37.2 s)

### 1. Transcript
| t | line |
|---|---|
| 0.00–2.20 | Want to be the man every woman craves? |
| 3.18–6.08 | Tired of getting ghosted, friend-zoned, and overlooked? |
| 7.08–9.94 | What if you could rewire your dating life in 90 days? |
| 11.10–13.10 | This is where real men found the solution. |
| 14.12–16.26 | The Power Code. Invisible to irresistible. |
| 17.74–18.82 | It's not just a dating guide. |
| 19.66–26.28 | It's a 90-day transformation plan built on dark psychology, proven by legendary seducers and trusted researchers. |
| 26.88–30.06 | The translation of every hidden signal you've been missing. |
| 30.88–32.80 | Stop playing Go Fish in a poker game. |
| 33.58–36.02 | Get The Power Code now. Link in bio. |

### Story beats
| beat | t | content | device |
|---|---|---|---|
| **Hook (desire)** | 0–2.2 | Identity question: become "the man every woman craves" | Aspirational "you" as a question |
| **Setup (pain)** | 3.2–6.1 | Three-item pain list: ghosted, friend-zoned, overlooked | A rule of three in rising order, each item said by the viewer's own dating vocabulary |
| **Tension (promise)** | 7.1–9.9 | "What if you could rewire … in 90 days?" | Hypothetical + mechanism metaphor ("rewire") + deadline |
| **Reveal** | 11.1–16.3 | "This is where real men found the solution" → product title + "Invisible to irresistible" | Tribe framing ("real men"); a before→after in three words |
| **Lesson / reframe** | 17.7–30.1 | "It's not just X, it's Y"; authority stack (dark psychology, seducers, researchers); "every hidden signal you've been missing" | Not-X-but-Y; hidden-knowledge framing |
| **Payoff / CTA** | 30.9–36.0 | "Stop playing Go Fish in a poker game." → "Get it now. Link in bio." | One concrete metaphor as the closer, then the CTA |

Devices: only 3 explicit second-person words, but every line before the product is implied "you": questions and imperatives.
The **metaphors are visualised literally**: "rewire" → gears, "90 days" → hypnotic spiral clock, "Go Fish" → betta fish, "poker" → chips and cards.
The dark framing is heavy ("dark psychology", "legendary seducers", "hidden signal"). It is an ad, so there is no curiosity loop beyond "what's the solution?" (opened at 7 s, closed at 14 s).

### 2. Hook (0–3 s)
- 0.0–0.45: from black, two hands working **puppet strings** (control metaphor) under "Want to be the man".
- 0.5–1.4: a white-haired dark-fantasy man with a **red lightning crack across his face** that flickers.
- 1.43–3.05: a red-haired woman, a purple lens-flare streak across her, slow push-in, on "every woman craves."
- 3.05–3.4: **CRT power-off** (white flash → horizontal line → dot → black) ends the hook.
- Why it stops the scroll: a desire question, three images in 3 s, a face in frame by 0.5 s, and a high-contrast saturated render.

### 3. Shot log (z2)
| # | start–end | on screen | voice | in / transition |
|---|---|---|---|---|
| 1 | 0.0–0.45 | puppeteer hands with strings, dark | Want to be the man | fade up |
| 2 | 0.45–1.43 | white-haired man, red lightning over face | (the man) | cut |
| 3 | 1.43–3.05 | red-haired woman, purple streak, push-in | every woman craves. | cut |
| 4 | 3.05–3.4 | CRT switch-off: white → line → dot | — | effect transition |
| 5 | 3.4–4.5 | silhouette at a red computer reading "TIRED"; window blinds strobe colours | Tired of getting | cut |
| 6 | 4.5–6.0 | figure in fire with burning money | ghosted, / friendzoned, | cut |
| 7 | 6.0–6.93 | glitchy glass head in an "I LOVE YOU / I HATE YOU" text collage | and overlooked. | cut |
| 8 | 6.93–7.87 | man at a train window, galaxy outside | What if you could | cut |
| 9 | 7.87–9.43 | rotating clockwork gears | rewire your dating life | cut |
| 10 | 9.43–10.9 | spiral (hypnotic) clock zooming in; white flash at 10.5 | in 90 days? | cut |
| 11 | 10.9–12.7 | skeleton in a top hat bound in chains | This is where / real men | cut |
| 12 | 12.7–13.93 | red archway, giant hands reaching down at a tiny figure | found the solution. | cut |
| 13 | 13.93–17.3 | ebook cover in a purple-lightning frame; glass cracks (14.2), spreads, **shatters** (15.0–15.4) | The Power Code. Invisible to irresistible. | cut; no caption (the cover is the text) |
| 14 | 17.3–17.55 | CRT switch-off | — | effect transition |
| 15 | 17.55–19.5 | golden dragon claw holding an orb | It's not just a / dating guide. | cut |
| 16 | 19.5–20.77 | ornate gold clock face | It's a 90-day | cut |
| 17 | 20.77–23.73 | horned demon reaching toward camera | transformation plan / built on / dark psychology, | cut (longest live-action hold, 2.96 s) |
| 18 | 23.73–24.8 | android whose face-screen flips sad → smile emoji | proven by / legendary | cut |
| 19 | 24.8–25.8 | close-up of glowing teal eyes | legendary seducers | cut |
| 20 | 25.8–27.3 | veiled cloaked figure | and trusted researchers. | cut |
| 21 | 27.3–28.2 | grid room of screens with a giant eye | The translation of | cut |
| 22 | 28.2–29.8 | woman in an ornate mirror, colours cycling | every hidden signal | cut |
| 23 | 29.8–30.8 | silhouette before a wall of CRTs | you've been missing. | cut |
| 24 | 30.8–32.27 | two betta fish | Stop playing go fish, | cut |
| 25 | 32.27–33.53 | poker chips and cards falling | in a poker game. | cut |
| 26 | 33.53–35.37 | ebook cover again, lightning | Get The Power Code now. | cut |
| 27 | 35.37–37.2 | black, "Link in bio!" | Link in bio. | cut |

Measurements (z2):
- **27 shots in 37.2 s, average 1.38 s** (1.49 s excluding the two CRT effects). **7.0 changes per 10 s.** By window: 0–10: 9 · 10–20: 6 · 20–30: 7 · 30–37: 4.
- **Longest hold:** the product cover, 3.4 s, kept alive by the crack-and-shatter animation. Then the demon at 2.96 s.
- **Image vs idea:** 10 ideas against 27 images, ≈ 2.7 images per idea, again one per caption group.
- **Section markers:** CRT power-off at 3.05 (end of hook) and 17.3 (end of product reveal).

### 4. Visual vocabulary (z2)
- **Assets:** dark-fantasy and sci-fi 3D/AI-art renders (demons, skeleton, android, mirror portrait), plus symbolic objects: puppet strings, gears, clocks, chains, fish, poker chips, burning money.
- **Animation:** slow push-ins on every render; animated loops (lightning, gears, fire, colour strobe, emoji face swap); glitch text collage (shot 7); glass crack and shatter; two CRT switch-off transitions; one white flash (10.5).
- **Text:** identical system to z1: small centred white serif, 2–4 words per card, hard swaps, at y ≈ 50 %. Suppressed when the image *is* the text (book cover).
- **Grade:** deep blacks, vignette, saturated accent colours (red, purple, teal, gold). It is less unified than z1, but the black frame edges hold it together.

### 5. Pacing (z2)
- **147 wpm over the speech span** (89 words). Per line: 173 · 148 · **202** · **192** · 220 (title) · 125 ("Invisible.") · 143 · **250** ("It's not just a dating guide.") · 158 · 135 · 152 · **205** · 208 · 200.
- **Pauses** at sentence ends: 0.30–0.76 s, mean 0.42 s. Tighter than z1, as an ad would be.
- **Fastest:** the promise ("What if you could…", 202), the reframe ("not just a dating guide", 250), and the closer and CTA (≥ 200).
- **Slowest:** "Invisible." (125, said alone) and the authority list (135). The slow words are the words they want remembered.

### 6. Ending (z2)
A **hard CTA** ("Get the Power Code now. Link in bio.") on black. There is no loop. The metaphor line just before it ("Go Fish in a poker game") is the real closer.

---

## Combined findings

1. **Change the picture on every caption group, not on every idea.** Both reels: one new full-frame image every **1.4–1.6 s** (6.4–7.0 per 10 s), 2.7–4.4 images per idea, each landing **0–0.25 s before** its words.
   Our w1-01 (`ours_sheet.jpg`) keeps the same wide two-figure composition for **15–22 s (7 s, her on the bed)** and **25–33 s (8 s, both standing)**.
   The base frame changes only ~8 times in 43 s (one per ~5 s), and in between, only a small bubble or tag changes in the upper corner.
2. **Every image is a picture of the words being spoken**, literal or metaphorical. The viewer never has to imagine. That removes the "high concentration" load.
3. **The words are not faster.** Their wpm (138 / 147) equals ours (133 overall / 140 over the speech span). Their sentence-end pauses (0.53 / 0.42 s) are a little *shorter* than ours (~0.6 s mean, many 0.7–0.96 s).
   The perceived speed comes from visual change plus slightly tighter gaps, with the voice *speeding up into reveals* and *slowing on the dark keywords*.
4. **Three punctuation transitions per reel** (white flash → black, CRT-off, or a black text-only hold) mark the section boundaries: hook | body | payoff | CTA. Everything else is a hard cut.
5. **Every shot moves inside itself**: a loop, a boil, a push-in, a pop-in, a crack. There are no static frames except deliberate black text beats.
6. **The hook gives the effect and withholds the mechanism.** The loop closes with a verbal callback (z1: "fools you" → "this is how you get fooled") *before* the CTA.
7. **One unifying grade over everything** (dark, vignette, paper grain) lets them use wildly different assets without looking messy. We already have that: our void and silhouettes.

---

## 7. Recommendations: Zoltium's storytelling and pacing inside OUR style

Our look is fixed: black void, white silhouettes with a purple rim, two-tier captions, WhatsApp bubbles, calm music, spoken CTA with "follow for more".
What we borrow is the *grammar*: cut rhythm, phrase-locked images, loop structure. We do not borrow their art, words or framing.

### A. Script structure template (30–40 s, ~85–95 words, stays inside [[rules/script-and-hooks]])
| beat | time | job | Zoltium move it copies |
|---|---|---|---|
| HOOK | 0–3 s | The relatable moment in 2nd person, plus the *effect* stated with the *mechanism* withheld ("She replied in 4 seconds, and that's exactly why she's losing interest.") | z1 0–6 s |
| OBJECTION | 3–5 s | Voice his doubt in 2–4 words, alone on black ("Sounds backwards?") | z1 "Sound weird?" |
| SCENE + TENSION | 5–15 s | Two concrete details, one WhatsApp line, his inner excuse | ours |
| MECHANISM | 15–24 s | Plain-words "why", in two short steps, pace up | z1 17–28 s |
| TWIST | 24–30 s | It happens without him noticing / the opposite of what he thought | z1 "without even realizing it" |
| CALLBACK PAYOFF | 30–34 s | Reuse the hook's key word ("…and that's how a fast reply turns into no reply.") | z1 "fools" → "fooled" |
| CTA | last 4 s | Spoken: share/save line + "follow for more" | ours ([[cta-rule]]) |

### B. Hook formulas (our wording, dating topics)
1. **Effect-without-cause, in second person:** "Your texts are making her lose interest, and it's not what you're saying."
2. **Counter-intuitive accusation:** "Being always available is the fastest way to get left on read."
3. **Desire question → pain triad** (z2), for list reels only: "Want her to text first? Tired of double-texting, waiting, and guessing?"
4. **The viewer's own lived moment + a twist marker:** "It's 1 a.m., she's laughing at your memes, and that's exactly the problem."

Rule: the first sentence must leave a "why?" that is answered only after second 15.

### C. Narration devices to adopt
- **Open loop + verbatim callback.** Pick one hook verb or noun and repeat it in the payoff.
- **Objection voicing.** One 2-word line on black after the hook ("Sounds weird?", "Harsh?", "Backwards, right?").
- **Personify the blind spot**, not the woman: "your nervousness", "your need to fix it". Never "her brain"; we never mock her.
- **Stakes ladder:** one text → the date → how she sees you. Each beat costs a bit more.
- **One concrete metaphor per reel, visualised literally** (z2's Go Fish line): "You're answering a question she never asked."
- **Pace contour:** say the mechanism sentences tight (sentence gap 0.35 s), and slow down only on 1–2 dark keywords. Do not slow down everywhere.

### D. Cut rhythm, targets and how to get them without clutter
**Targets:**
- A visual change every **1.2–2.0 s** (≥ 5 per 10 s; today we are at ~1 major change per 5 s).
- No static frame longer than **2.5 s** unless it is a deliberate text-only beat.
- Every visual change lands on a caption group, **0.1–0.2 s before** its first word.

**Ways to change the picture using only what we already own (one focal element at a time, so [[rules/visuals-and-motion]] "breathing" still holds):**
1. **Shot size as the cut.** The same silhouette scene, re-framed per caption group:
   - wide (both figures) → **close-up of his head and phone** (camera push 40–60 %, hard cut, not a slow push) → **extreme close-up of the WhatsApp bubble** filling the frame → back to wide.
   This is three to four "new images" from one still. Today, camera push ≤ 10 % and "hard cut only on location change" forbid it (see Proposed rules).
2. **Reframe left/right.** Cut from a two-shot to a single of *her* (him off-frame). That gives a new image and a clear focus.
3. **Pose swaps on the verb.** Cut to a different pose still of the same figure on the action word (texting → phone down → turned away).
4. **Symbol inserts on the key noun.** A full-frame glowing white line-art object with a purple rim, alone on the void, for 0.8–1.5 s, then back to the people. See E.
5. **Black text beats as section punctuation.** We already have "line alone on the dark". Use it 2–3× per reel exactly at section boundaries (after the hook, before the payoff), not randomly.
6. **One section transition device.** A quick purple-white flash to black (2 frames) or a light-off (the spotlight snaps off, 0.15 s), used only at those 2–3 boundaries.
   Their white-paper flash and CRT-off are the model. Keep ours on-brand and subtle.
7. **Movement inside every hold.** Keep a slow drift (≤ 3 %/s) or a pose micro-change on any frame held > 1.5 s, so no frame is ever dead (Zoltium shot 24 holds 4 s but changes expression every 0.5 s).

### E. Their abstraction devices, translated to silhouettes and purple glow
| Zoltium device | where | our version |
|---|---|---|
| Symbolic object on the key noun (trophy = success, skull = fooled, ooze = chemicals) | z1 9, 16, 28 | A **white line-art symbol with a purple rim, centred alone on the void**, cut in on the noun: hourglass ("waiting"), hook ("hooked"), open door / closing door ("chance"), chess piece ("move"), crown ("value"), unread-dot or blue ticks enlarged ("left on read"), broken chain, magnet ("attraction"), scale ("effort"). Generated by our own pipeline as `fx/<name>` stills. |
| Personified villain (brain with a mouth) | z1 1 | His silhouette with a **purple-lit "inner" silhouette stepping out of him** (his anxiety) or a purple shadow that moves on its own. |
| Lifestyle montage on one phrase (toilet → couch → food → bed) | z1 10 | **3-pose staccato**: his silhouette in three quick poses/places (bed texting → desk → car), 0.4–0.5 s each, on "every day / all day / at 1 a.m.". |
| Metaphor shown literally (gears = "rewire", fish = "Go Fish") | z2 9, 24 | Draw the one metaphor line as a symbol insert (e.g. "playing checkers when she's playing chess" → glowing checker vs chess piece). |
| Face expression change during a hold | z1 24 | Purple rim **pulses / dims** on the figure as the feeling changes, or a pose swap mid-line. |
| Shrink-to-nothing exit | z1 30 | A figure shrinks and fades into the void on "you disappear to her", which also serves as the section exit. |
| Black text-only interrupt | z1 6, 31 | The objection line and the payoff punch alone on black (we have this; time it to section boundaries). |
| Logo assembly CTA | z1 33 | Not needed. Our CTA stays a spoken line + FOLLOW FOR MORE card. |

### F. Do NOT copy
- Their exact words, hooks or slogans ("Your brain fools you…", "Sound weird?" as-is, "you may not see us again", "become powerful", "Invisible to irresistible", "Go Fish in a poker game").
- **Manipulation and seduction framing**: "dark psychology", "legendary seducers", "every woman craves", "real men", "become powerful". Our page explains *her* signals and *his* blind spot. It does not teach control.
- **Scarcity / threat CTAs** ("you may not see us again"). Ours stays a friendly "save/send this … and follow for more".
- **Loose science** ("same chemicals", "brain can't tell reality from imagination"). Accuracy first ([[rules/script-and-hooks]] rule 7).
- **Their assets**: the z1 clips appear to include copyrighted studio cartoon characters, and z2 is third-party / AI 3D art. We use only our own cast and fx ([[rules/assets]]).
- Their tiny centred serif captions and horror audio. Our captions and calm music stay as they are.

---

## Storyboard template (beat → visual device → duration)
1. HOOK line, groups 1–3 → wide moment → CU his phone → ECU bubble · 3 × ~1.0 s
2. OBJECTION → line alone on black (section break #1: flash/light-off) · 1.0–1.5 s
3. SCENE → two-shot → single of her → pose swap on the verb · 3 × 1.5 s
4. TENSION (excuse + WhatsApp line) → ECU bubble → his CU (purple rim) · 2 × 1.5 s
5. MECHANISM, 2 steps → symbol insert on each key noun, between figure shots · 4 × 1.2–1.5 s
6. TWIST → 3-pose staccato or figure shrinks into the void · 1.5–2 s
7. PAYOFF callback → punch words alone on dark (section break #2) · 2 s
8. CTA → spoken share/save line + FOLLOW FOR MORE · 3–4 s

## Proposed rules (for the main agent to accept or reject)
1. **visuals-and-motion / Camera:** replace "push ≤ 10 %, one per beat; hard cut only when location changes" with: *"A hard cut to a new shot size (wide / CU / ECU of the bubble or phone) is allowed on any caption group. Target one visual change every 1.2–2.0 s; no static frame > 2.5 s except deliberate text-only beats."*
2. **visuals-and-motion / new:** *"Symbol insert: on the key noun of the mechanism or payoff, cut to one white line-art symbol with a purple rim, alone on the void, 0.8–1.5 s. Max 3 per reel. Own generated assets only (`fx/`)."*
3. **visuals-and-motion / new:** *"Visual changes land 0.1–0.2 s before the first word of their caption group."*
4. **visuals-and-motion / transitions:** *"Section punctuation (a 2-frame flash to black, or a light-off) only at 2–3 section boundaries: after the hook, before the payoff, and optionally before the CTA."*
5. **script-and-hooks:** add the OBJECTION beat (2–4 words on black after the hook) and *"the payoff reuses the hook's key word verbatim"*. Make the hook state an effect and withhold its cause until after 15 s.
6. **audio / pacing (wording only, not sound design):** sentence pauses 0.35–0.5 s in the mechanism, longer (0.7–1.0 s) only before the objection line and the payoff.
