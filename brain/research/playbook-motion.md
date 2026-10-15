# Motion playbook for dark-background explainer Reels

**Sources watched (6, all under 60 s):**
- A = `hWo11lQmaBo` Text-Based Explainer Video (34 s, teal/grey word cards)
- B = `Q_ROGVLc4TA` "comma" motion graphics (26 s, minimal black/grey/white)
- C = `zn1WRcQb4vI` "I'M LOST." (15 s, flat illustration: hand, compass, arrows, numbers)
- D = `0qdPcFDLwP0` "[Motion Graphic] GATE" (21 s, green light sweeps, long shadows)
- E = `u68Q9hyMz4U` Minimalist Motion Graphics, compound interest (31 s, black/white text and line)
- F = `-VCxTi8sJ-s` Smooth Text Animation in After Effects (56 s, screen-recorded tutorial with captions)

Caveat: timings are read from sparse frame samples, so they are approximate. Only F has captions and exact numbers. Figure techniques come from C only. Match cuts, whip or zoom transitions, and focus pulls were not visible, so they are left out.

## 1. Transitions

- **Brush or paint wipe between words.** A teal brush stroke sweeps across, reveals the next word, and the old word stays underneath (A, 00:04 to 00:07). Good for a mask reveal that feels hand-made.
- **Colour-field swap as the scene change.** The background changes colour while the inset panel stays put, for example blue to cream (C, 00:06 to 00:07).
- **Light band sweep.** A bright vertical strip passes across a dark field (D, 00:14). Reads as a light flare more than a hard cut.
- **Horizontal white bar wipe.** A white band slides across with the curve line trailing it, then the next calendar card appears (E, 00:15 to 00:16).
- **Noise or glitch wipe.** Static bursts cover the cut and then clear, used on the closing word (A, 00:10 and 00:16). Use it at most once per video, since it looks dated when repeated.
- **Hard cut to black.** B uses black holds between beats (00:18 to 00:22).

Wipes in A and E look roughly 0.5 to 1 s. Cuts are not eased.

## 2. Making static figures feel alive

- **Scale push across frames.** The compass in C grows from small to close-up between 00:02 and 00:04. Slow, one-directional, sells weight.
- **Inset frame held still, content moves.** The arrows and numbers in C (00:06 to 00:10) sit in a fixed rectangle while the background and text change around it. Gives depth without real parallax.
- **Long cast shadow.** D (00:02 and 00:04) puts a clean long shadow under a clock and a ruler. Shadows give a plain shape a light source.
- **Glow as a light source.** C (00:05) has a red edge glow on a dark shape. One accent light on a black field is enough.
- **Motion blur on text moves.** F (00:53) turns motion blur on for the text layer. This is the cheapest fix for choppy captions.
- **Figure swaps.** C swaps whole shapes (hand, compass, number card) rather than morphing them.

Not seen in these clips: particles, camera drift, focus pulls, flicker.

## 3. Explainer devices

- **Line draws on, ends on a dot.** E (00:19 to 00:21) draws a curve that ends in a dot, then the calendar card comes in. Use this for a growth line or a timeline.
- **Rising bars.** E (00:10) shows vertical bars growing left to right. Simple, legible on a phone.
- **Cards that pop into the frame.** E shows a phone card with "DO THE MATH" (00:13) and calendar cards for dates (00:17 to 00:19). One card per beat, centred.
- **Floating dot as a pointer.** E (00:11 to 00:12) moves a small dot along a line.
- **Split-tone panel.** D (00:14) uses a dark side and a light centre band to focus one element.

Not seen: arrows that draw on, meters, counters, connection lines, split screen.

## 4. Caption typography

- **Word-by-word, one line at a time.** A puts one or two words on screen, each on its own beat (00:05 "COMMUNICATE", 00:06 "EASILY", 00:07 "EFFECTIVELY"). Each word gets roughly one second.
- **Rise and fade.** F's recipe: text starts 100% down with opacity 0, then rises to its place (F, 00:13 to 00:19). A plain fade is not enough on its own.
- **Tracked caps for a single line.** E (00:14 to 00:15) sets "YOUR MONEY CAN GROW EXPONENTIALLY OVER TIME" in wide-tracked caps with one short line per beat.
- **Highlight behind the word.** A's brush strip sits behind white bold type (00:05).

On a phone: one line, bold sans, a few words at a time. The thin captions in B (00:15) and C (00:06) are too small at phone scale.

## 5. Timing numbers

- **Text entrance:** F sets a range-selector offset that runs from -100% to +100% over one second ("move a second forward", F 00:24 to 00:35), with the ease shape set to ramp up, ease high 25%, ease low 100%.
- **Word hold:** each word in A holds about 1 s. Single-line captions in E hold about 1 to 2 s.
- **Scene wipes:** roughly 0.5 to 1 s (A, E).
- **Entrances of 0.3 to 0.5 s:** not measured in these clips; a guess to test, not a finding.

## 6. What looks cheap or amateur (from these clips)

- Screen-recorded tutorial footage used as the final look (F is a studio screen recording, not a finished piece).
- Tiny, thin captions that become unreadable on a phone (B, C).
- Noise or glitch overlays on every scene (A, 00:16 fills the whole frame).
- Long blank holds with no motion (E, 00:00 to 00:02 is a blank frame; D, 00:00 is black).
- Several effects in one beat. Keep one motion per beat.
