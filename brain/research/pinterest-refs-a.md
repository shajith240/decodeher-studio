# Pinterest refs A: two "premium edit" references from the owner (2026-10-13)

Sources: owner-sent Pinterest pins
- **V1** https://pin.it/5SbOQPH72 : 16.9 s, 720×1280, 30 fps. Talking head (woman, NY cap, dark office).
- **V2** https://pin.it/1lCs85rrQ : 30.6 s, 720×1280, 30 fps. "BEFORE / AFTER" showcase by the editor **@aslan.visuals** (male creator, beige hoodie, RGB mic).

Method: yt-dlp download, faster-whisper `small` word timestamps (±0.05–0.1 s), ffmpeg 2 fps contact sheets for the flow, and 30 fps crops of 8 text entrances in V1 and 9 in V2. Frame numbers `fNNN` are **absolute frames at 30 fps** (f30 = 1.00 s). Audio levels are per-0.1 s RMS from `astats`.
Working files: `/tmp/claude-1000/-home-shajith-Projects-dark-psycology/ef3cc9ee-9e91-4d22-92ae-2fcdd6dc41de/scratchpad/pins/a/` (strips/*.png, v*-sheet*.png).

> **Key finding:** V1 already uses our **two-tier caption** system: a small white top line plus a big coloured key line. It is almost certainly the reference behind `DN.TIERS`. What V1 does and we don't is **timing and motion**. Each two-tier group stays on screen **1.5–2.1 s** and its words *build in place* with a 3–5-frame fade or focus-pull. Nothing slides. The group leaves all at once on a cut or blur. V2 shows the opposite approach: 0.74 s chunks that hard-cut. It looks punchy, but it is the "too fast to read" pattern the owner is complaining about. **Use V1 for caption timing. Use V2 for literal visual metaphors, per-beat colour worlds and UI-card motion.**

---

## V1: "If prospects have to meet you…" (content-agency ad)

### 1. What it is, who it's for
A 17-second direct-response ad for a done-for-you video content service. It speaks to coaches and service businesses who know they should post but avoid the camera. The structure is a conditional hook, two pains, then the offer.

**Tips it teaches (paraphrased):**
1. Your content should prove your value *before* a sales call. If people only "get it" after meeting you, the content isn't doing its job.
2. Name the real blockers: camera anxiety, and not knowing what to say.
3. Content has to connect to revenue, not just to views.
4. The fix is to hand the production off (this is the offer).

**Editing lessons it shows (what the owner means by "tips"):**
1. Two tiers: small connective words in white, the *one* meaningful word huge and coloured.
2. Build the group word by word, but **keep the whole group on screen** until the thought is finished.
3. Put the key word **behind the subject's head** (depth) when the subject is framed high.
4. When the voice names a problem, **swap the caption for a UI object** (red error toast).
5. Change the "world" of the frame on a new idea: REC viewfinder overlay, ring highlight, punch-in.
6. Use a cross-out to show negation, timed just before the negative word is spoken.

### 2. Caption system
| Property | Evidence |
|---|---|
| Font feel | Heavy neo-grotesk (Helvetica-Now/SF-Display-Black feel), **sentence case**, **not italic**, tight tracking. Top line is medium-bold. |
| Size | Key word ≈ 70–85 % of frame width ("Prospects" f11, "Understand" f55, "content" f155). Top line ≈ 30–35 % of key-word cap height. |
| Colour | Key line lime `~#D8F24A` with a soft same-colour outer glow. Top line white. Accent red only for the cross-out (f103–109) and the error UI. |
| Position | Changes per shot. Chest band y ≈ 40–48 % (G1–G3, G6, G8). Top band y ≈ 8–15 %, *behind the head*, on the high framing (G4 f154–186, G5 f197–240). Left-of-centre block. Small words sit offset up-left or down-right of the key word. |
| Words on screen | 4–7 per group (G1 "If the Prospects have to meet you" = 7; G3 "your Content is failing" = 4). |
| Group durations | G1 0.03→~1.45 s · G2 ~1.5→3.10 s (1.6 s) · G3 3.13→4.40 (1.3 s) · G4 4.50→6.20 (1.7 s) · G5 6.53→~8.0 (1.5 s) · G6 ~8.0→10.13 (2.1 s) · G7 error toasts 10.2→14.9 (4.7 s; 2nd toast 11.9→14.9) · G8 14.9→16.9 (2.0 s). **Median group ≈ 1.7 s; minimum 1.3 s.** |
| Group rate | 8 groups / 16.9 s = **28 groups/min**, one every ~2.1 s. |
| Words/sec | Spoken 52 words / 16.3 s = **3.2 wps**. Shown ≈ 2.9 wps: the toasts shorten "unsure of what to say and how it actually turns into real revenue" to "what to say?" / "how it turn to revenue?". The *screen* changes only ~0.5 times/s. |
| Unit | **Per word inside a per-phrase group.** Each word appears as it is spoken and stays. The group clears all at once. |
| Lead/lag | Key words land **0–5 frames before** the voice: "You" f259 vs spoken f264 · "record" f262→266 vs f267 · "content" f154 vs f155 · "Content" f98 vs f98 · "Your" f472 vs ~f476. Top-line words land on the word or 1–2 f before. Never late. |
| Pauses | Caption holds through the speech gaps (digital silence −72 dB at 7.9–8.1 s and 13.7–14.0 s). The group stays up during the breath. |

### 3. Text-animation vocabulary (V1)
| # | Animation | Frames (dur) | Easing feel | Used for | Evidence |
|---|---|---|---|---|---|
| A | **Grey→white fade** (opacity ~35 %→100 %, no movement) | 3–4 f (0.10–0.13 s) | ease-out, no overshoot | small top-line connective words ("the", "have to", "your value", "we take it off", "being on") | f4–7, f16–20, f68–74, f447–460, f197–201 |
| B | **Focus-pull pop**: starts ~40 % opacity, blurred/glowy, ~5 % oversized, then sharpens to settle | 3–5 f (0.10–0.17 s) | fast ease-out, no bounce | key line words: nouns and the "you" of the hook ("Prospects", "You record", "Your plate") | f8–11, f259–266, f472–478 |
| C | **Hard pop** (1 frame, full opacity) | 1 f | none | key word that lands on a stressed beat ("Understand", "content" behind head) | f55, f154 |
| D | **Per-word key-line build**: each big word fades in on its own, left to right | 4–5 f each | ease-out | multi-word key line ("Camera Stresses") | f202–206, f207–210 |
| E | **Strike-through draw**: red 3-px line scales L→R across the key word | ~7 f (0.23 s) | ease-in-out | negation: content *failing*. Starts 7 f **before** "failing" | f103–109, "failing" @ f116 |
| F | **Icon draw-on** (outline arrow fades and scales in next to "your value") | ~6 f | ease-out | meaning-icon beside a key phrase | f72–78 |
| G | **Group exit = whole-frame blur-out** on a punch-in cut | 2 f | snap | ending a thought and switching framing | f92–94 |
| H | **Group exit = hard cut** with the shot | 0 f | — | most exits | f186, f304, f447 |
| I | **Light-leak blinds transition**: white vertical-stripe wipe over the cut, plus an SFX burst | 9 f (0.30 s) | — | new section ("You know content matters") | f132–140; audio peaks −5 dB at 4.7–4.9 s |
| J | **UI toast reveal**: red error toast blurs and fades in, then its text types in per word ("what"→"to"→"say?", ~4 f apart) | toast 4 f; words 4–5 f each | ease-out | pain points or questions that live as UI | f306–317, 2nd toast ~f357 |
| K | **Ring zoom**: thin glowing ring scales down onto the face after a cut to a new angle | ~8 f (0.27 s) | ease-out | emotional-state close-up ("stresses you out") | f186–194 |
| L | **Chat-bubble grow**: pill expands from the right edge with text | ~6 f | ease-out | the inner voice ("Please turn off…") | f208–214 |
| M | **REC viewfinder overlay**: corner brackets, REC dot, red dot after "record" | cut on | — | world change: "even if you record" | 9.0–14.8 s |

### 4. Premium signals (V1)
- **Few, held groups.** 8 caption groups in 17 s, each held 1.3–2.1 s. The motion is fast (3–5 f) but the holds are long. This is the main reason it reads as calm and expensive.
- **Breathing room.** Real silences of 0.2–0.4 s between sentences (2.94–3.16, 7.85–8.26, 13.69–14.12 s). No music bed: the floor drops to −72…−77 dB. One SFX hit, on the blinds transition (4.5–5.1 s, louder than the voice).
- **Depth.** The key word sits *behind* the head (f154–186). The type lives in the scene rather than on top of it.
- **Grade.** Low-key, near-black shadows, warm skin, green-teal background. The lime key colour is the only saturated element, so it pops.
- **World changes, not effects.** Each new idea gets a new frame treatment (blinds flash, then ring and close angle, then REC viewfinder, then clean). There are 5 visual states in 17 s, each held 1.5–4.7 s.
- **Negative space.** Usually one block of text plus one subject. While the toasts are up, there is no caption at all (10.2–14.8 s).
- **Camera.** Punch-in cuts between medium and close (f93 blur-cut). Cut to a different camera angle for the "stress" beat (f186).

---

## V2: "Mastering video editing…" (before/after editor showcase)

### 1. What it is, who it's for
A 30.5-second portfolio reel by the editor @aslan.visuals. It shows a creator's raw talking head ("BEFORE", small, left) next to the edited version ("AFTER", larger rounded card, right) on a soft grey studio gradient. It is aimed at creators who want to hire an editor and at editors learning the style. The script inside the clip is a creator's pitch for editing mentorship.

**Tips it teaches (paraphrased):**
1. Editing is more learnable now than ever. Start by understanding your tools.
2. Pick your main program deliberately (timeline editor vs motion-graphics tool). It is a big fork in your path.
3. Step back and choose the path that pays more later, not the easiest one today.
4. When you don't know which way to go, get guidance (the CTA).

**Editing lessons it shows (the before/after is the lesson):**
1. **Visualise the literal words.** "Step back": the frame shrinks into a dark border. "Shatter … roadmap": the word ROADMAP cracks apart. "Decision": two glass choice cards with START buttons and a cursor clicking. "Income": a stack of payment notifications.
2. **A new colour world per beat.** The background grade jumps on every new point: neutral → purple (FIRST, 5.47 s) → navy (STEP BACK) → red (DON'T WANT / SHATTER) → charcoal (INSTEAD / INCOME) → lime (the objection "BUT JOSEPH") → neutral (the answer). The RGB mic changes colour with it.
3. **Key-word colour matches the world**: red ROADMAP on red, lime JOSEPH on lime, cyan INCOME/PREMIERE PRO on dark.
4. **Voice the viewer's objection** and give it its own colour world ("But Joseph, I don't know…", lime, 25.4 s).
5. **SFX on world changes**, over a quiet music bed.

### 2. Caption system
| Property | Evidence |
|---|---|
| Font feel | Condensed heavy sans (Bebas/Anton feel), **ALL CAPS**, upright. White-to-grey vertical gradient with a slight bevel and dark drop shadow. Key words cyan/blue gradient with an outer glow. |
| Size | Modest: ~45–60 % of the AFTER card width. The key word ("2025", "EXPLAIN", "ROADMAP") is ~1.3–1.6× the support words. |
| Position | Fixed chest band, ≈ 62–68 % of card height, centred. Moves only when a UI card occupies the lower third. |
| Words on screen | 1–5, typically 2–3 ("HAS NEVER", "LET ME / EXPLAIN", "TAKE A DECISION"). |
| Chunk durations | ~41 chunks in 30.5 s → **avg 0.74 s**. Shortest ~0.35 s ("FIRST" 5.47→5.80, "NOW TAKE" 13.4→13.8). Longest ~1.3 s ("AS EASY AS IT / IS IN 2025" 2.0→4.7, held over the 0.7 s pause). |
| Words/sec | Spoken 104 words / 30.2 s = **3.4 wps**. Shown is verbatim, so also ≈ 3.4 wps. The screen changes ~1.35 times/s, **2.6× V1's change rate**. |
| Unit | Per phrase chunk (2–3 words). Sometimes a second line builds under it ("HAS NEVER" f37 → "+BEEN" f48; "AS EASY AS IT" → "+IS IN 2025" f100/f105). |
| Lead/lag | Leads: "HAS NEVER" whole at f37 while "never" is spoken at f45. "BEEN" f48 vs f54 (6 f early). "2025" f105 vs f106. Leads 1–8 frames, never lags. |

### 3. Text-animation vocabulary (V2)
| # | Animation | Frames | Used for | Evidence |
|---|---|---|---|---|
| N | **Hard cut on/off** (no tween) for every normal chunk | 1 f | default narration | f37, f60, f164, f644, f778 |
| O | **Number/keyword + icon pop**: "2025" in blue gradient with a 3D calendar-pages icon, hard on | 1 f | numbers and dates | f105 |
| P | **Coloured glow word** (red ROADMAP with a red bloom behind it) | 1 f on | the negative noun | f619 |
| Q | **Shatter**: the word cracks into shards on the verb "shatter" and holds broken | cracks over 3–4 f (f624–627), holds 0.5 s | destructive verbs, punchline | f619–643 |
| R | **Glass-card fade+blur in**, staggered: left card ~10 f, right card starts ~6 f later, inner icon/title/button build next, then a cursor clicks START | 10 f per card, 6 f stagger | choices / A-vs-B | f303–331 |
| S | **Pill toolbar expand** from a dot (scale-X from centre) | 5 f | UI accent under a keyword ("FIRST", "YOU NEED") | f169–173 |
| T | **Notification stack**: payment toasts fade+blur in, one every ~5–7 f, stacking downward | ~6 f each | money / proof | f649–668 |
| U | **Stack exit**: blur + fade out together | ~7 f | clearing UI before the next beat | f756–763 |
| V | **Frame shrink ("step back")**: the whole video scales to ~85 % into a dark navy border, eased | ~14 f (0.47 s), ease-out | literal metaphor | f414–428 |
| W | **Grade jump** on a hard cut, with an SFX burst | 1 f | new point / new speaker voice | 5.47 s, 13.8 s, 17.5 s, 21.4 s, 25.5 s; audio bumps 8.8–9.1, 13.6–13.8, 17.8, 20.9, 21.5, 25.8 s |

### 4. Premium signals (V2)
- **Packaging.** The before/after split on a soft grey gradient with a rounded, shadowed card reads like a product shot. The same footage looks more expensive when it is framed.
- **Colour as structure.** One saturated grade per beat (6 worlds in 30 s, held 2–8 s each). The caption accent colour matches the world.
- **Literal metaphors** (step back, shatter, decision cards, income notifications) make the edit look designed rather than templated.
- **Glassmorphism UI** with soft blur and staggered builds. No bouncy easing anywhere.
- **Sound.** A continuous quiet music bed (floor never drops below ~−39 dB, ~15 dB under the voice) plus short SFX bumps on the world changes.
- **Weakness for our purpose.** 0.74 s chunks force rapid reading. That works for this style but is exactly the owner's complaint (a).

---

## 5. Recommendations for OUR reels (black void, glowing silhouettes, Montserrat Black Italic two-tier, WhatsApp bubbles)

### 5.1 Readability fix (complaint a). Copy V1's timing, not V2's
- **Group = one two-tier block** (top line + key line), sized to one thought. **Max 6 words** per group: top ≤ 4, key ≤ 3. Split longer lines at the natural comma.
- **Minimum on screen: 1.2 s. Target: 1.6–2.0 s.** If a phrase is spoken in under 1.2 s, merge it with the next phrase or extend the hold into the following pause. Never clear a group just because its last word ended.
- **Target ≤ 30 groups/min** (V1 = 28/min). With our ~3 wps narrator that works out to ~6 words per group. The change rate falls from ~1.3/s to ~0.5/s while still showing every word.
- **Build, don't replace.** Words appear in place as they are spoken (V1 A/B/D) and *stay*. The group leaves all at once, on the scene change or 0.25–0.4 s after the last word, never mid-thought.
- **Hold through pauses.** Keep the last group up during breaths. Add real 0.25–0.4 s silences between sentences in the voice track (V1 has three of them in 17 s).
- **Timing.** Land the key word **on the spoken onset, up to 2 frames before** (−0.07…0 s). Both references lead; neither lags. Top-line words: 0…+30 ms.
- Keep the existing rule "the visual is the caption": V1 drops captions entirely for 4.7 s while its toasts carry the words.

### 5.2 Animation vocabulary to add (complaint b): one move per *kind* of moment
All values in GSAP terms. No `back`/`elastic` (bounce was rejected 10-13). Overshoot is never used in either reference.

| Moment | Move | GSAP | Ref |
|---|---|---|---|
| Top-line connective words (default) | grey→white fade, no motion | `fromTo(w,{opacity:0.35,color:'#8a8a8a'},{opacity:1,color:'#fff',duration:0.12,ease:'power1.out'})` | V1-A |
| Key word (noun, emotional word, "you") | **focus-pull**: blur + slight oversize settling in | `fromTo(w,{opacity:0.3,filter:'blur(8px)',scale:1.06},{opacity:1,filter:'blur(0px)',scale:1,duration:0.18,ease:'power2.out'})` | V1-B |
| Multi-word key line | the same focus-pull per word, each on its own onset | per word, as above | V1-D |
| Question top line ("why would she…") | **mask rise** (word rises out of a clip box), the premium cousin of a slide | parent `overflow:hidden`; `from(w,{yPercent:100,duration:0.3,ease:'expo.out'})`. Or, if the owner wants a literal slide: `from(w,{x:40,opacity:0,duration:0.35,ease:'power3.out'})` on the **question line only** | owner's ask; not seen in refs |
| Soft/romantic word ("date", "miss", "love") | **slow dissolve**: opacity and blur with a longer duration, nothing else | `fromTo(w,{opacity:0,filter:'blur(6px)'},{opacity:1,filter:'blur(0px)',duration:0.45,ease:'sine.out'})` | variant of V1-B |
| Stressed punch word on a beat | **hard pop** (1 frame), let the size do the work | `set(w,{opacity:1})` at the onset frame | V1-C, V2-N |
| Negation / "she's NOT…" / wrong belief | **strike-through draw** (purple or red line over the word) | line `fromTo({scaleX:0},{scaleX:1,transformOrigin:'0% 50%',duration:0.23,ease:'power2.inOut'})`, starting 0.2 s before the negating word | V1-E |
| Number / stat ("3 seconds", "80 %") | hard pop in purple + small icon beside it | `set` on + icon `from({opacity:0,scale:0.9,duration:0.2,ease:'power2.out'})` | V2-O, V1-F |
| Destructive verb (break, ruin, ghost, shatter) | **crack/shatter**: the word splits into 3–5 clip-path shards that drift 4–8 px and hold | shards `to({x:'random(-8,8)',y:'random(-6,6)',rotation:'random(-4,4)',duration:0.12,ease:'power2.out'})` on the verb onset | V2-Q |
| List item / choice (A vs B) | staggered glass/silhouette cards | `from(cards,{opacity:0,filter:'blur(10px)',y:12,duration:0.33,ease:'power2.out',stagger:0.2})` | V2-R |
| WhatsApp bubble | blur-in shell, then text in per word | shell `from({opacity:0,filter:'blur(8px)',scale:0.96,duration:0.14,ease:'power2.out'})`; words `stagger:0.14` | V1-J, V1-L |
| Group exit (thought ends) | whole block blurs out in 2–3 frames, ideally on a scene change | `to(group,{opacity:0,filter:'blur(12px)',duration:0.1,ease:'power1.in'})` | V1-G |
| Exit at a hard cut | just cut | — | V1-H |
| Emotional close-up beat | thin glowing purple ring scales down onto the silhouette's head | `from(ring,{scale:1.35,opacity:0,duration:0.3,ease:'power2.out'})` | V1-K |
| "Step back" / perspective shift | the whole stage scales to 0.88 into black | `to(stage,{scale:0.88,duration:0.47,ease:'power2.out'})` | V2-V |

Rule of thumb: **one motion verb per word class**. Narration words fade. Key words focus-pull. Questions rise. Soft words dissolve. Negations get struck. Numbers pop. Destruction shatters. No word ever slides in from the right by default.

### 5.3 Premium, for our black void (complaint c)
- **Fewer, longer states.** Aim for 4–6 visual "worlds" per 30 s, each held 2–5 s. A world can be a different silhouette pose, a ring close-up, a bubble screen, or a purple-tinted beat. Don't add more effects.
- **One colour per world.** Our void stays black, but the purple rim and glow can shift intensity per beat: dim on setup, full purple glow on the reveal. Match the key-word purple to it. (V2's per-beat grade, translated to our palette.)
- **Depth.** Let the big key word sit *behind* a silhouette's head when the figure is framed high (V1 f154). It is cheap to do with a z-index sandwich and it reads as premium.
- **Sound.** Silence between sentences (V1), *or* a quiet bed at about −15 dB under the voice (V2). One SFX per world change, never per word.
- **Negative space.** Show one text block or one UI object, never both (already our rule). Leave the key line alone on black for the punchline.

### 5.4 Script and structure tips to adopt
1. **Conditional hook**: "If ___, your ___ is failing." This is V1's 0–4 s structure. Ours: "If she has to *see you* to feel it, your texting is failing."
2. **Write visualisable verbs** into the script (step back, shatter, cross out, pull away, go cold) so an animation can carry the line. V2 builds its best moments on these.
3. **Voice the viewer's objection** as its own beat ("But why would she…?") with its own world: the mask-rise question line plus a tint change (V2 25.4 s).
4. **Turn pain points into UI**: put the doubts she has as WhatsApp bubbles or "error" toasts instead of captions (V1 10.2–14.9 s).
5. Add a real pause before the payoff line. Keep the "follow for more" CTA (house rule).

## Proposed rules (for the main agent to merge into `brain/rules/captions.md`)
1. Two-tier group: max 6 words (top ≤ 4, key ≤ 3); **on screen ≥ 1.2 s, target 1.6–2.0 s; ≤ 30 groups/min**. Words build in place and the group clears all at once.
2. Replace the default "slide from the right" (`DN.easeIn`) with: top line = grey→white fade 0.12 s; key line = focus-pull (blur 8→0, scale 1.06→1, 0.18 s, power2.out).
3. Animation is chosen by word class (table 5.2). The question line may rise or slide; nothing else slides.
4. Change rule 4 ("captions must never run ahead"): the key word may land **0–2 frames before** its onset. Both references lead by 0–6 frames, and a late key word reads as lag.
5. A group exit is a 0.1 s blur-out or a hard cut on a scene change, never a per-word exit.
