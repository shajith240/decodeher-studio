# Hooks 2026: engineering the first 1-3 seconds (@thedecodeher)

Written 2026-10-16. Purpose: 43-67% of viewers swipe in the first 3 s, reach is ~120 views/reel, so the hook is the lever.

**Evidence warning.** Web search returned mostly marketing/tool blogs that repeat each other. Meta's own words I could confirm
are few (Mosseri: first 3 s are "the hook"; ranking = watch time, sends per reach, likes per reach). Every number
tagged (vendor) below is an unverified rule of thumb, not Meta data. Format names and templates are craft synthesis (mine) built on
those sources plus our own rules in `brain/rules/script-and-hooks.md`. Treat all of it as hypotheses to A/B on our own retention graph.

---

## 1. Hook formats that work now (and our versions)

Common mechanism across sources: open a loop (a gap between what viewer knows and wants to know), start mid-action
instead of setup, state the strongest thing first, and make the first frame readable with sound off.
Our niche rules for every example: men's perspective, specific behaviour of hers, no PUA sleaze, no insulting women, the verdict is about
the BEHAVIOUR or the situation, not "women are X".

### F1. Behaviour + Verdict ("The Decode")
- Pattern: `When she [specific behaviour], it means [verdict].` / `She [behaviour]. That's not [what you think].`
- Why it stops the scroll: the viewer recognises a moment from their own life in 3 words, and a verdict promises a decoded answer.
  This is our core format and matches the approved Views Rule (behaviour + verdict, <= 10 words).
- Ex 1: "When she replies in one word, it's not boredom."
- Ex 2: "She takes three hours to answer, then sends a meme."

### F2. Wrong-Belief Flip (contrarian)
- Pattern: `You think [common read]. It's actually [opposite].`
- Why: contradicts what the viewer currently believes; the brain wants the correction. Contrarian/hard-opinion openers are
  repeatedly listed as working (vendor sources).
- Ex 1: "You think she's playing hard to get. She's deciding."
- Ex 2: "Slow replies aren't disinterest. Look at what she does after."

### F3. "Seen it, here's the cost" (Mistake callout)
- Pattern: `The [reply/move] that quietly kills her interest.`
- Why: loss-framing plus "mistake frame" (open on something visibly wrong). Men fear the unknown mistake more than they want a tip.
- Ex 1: "The text that makes her lose interest in minutes."
- Ex 2: "Stop sending this after she goes quiet."

### F4. Mid-Scene Cold Open (story in progress)
- Pattern: Start inside the moment, no setup: `She said "haha" and I knew it was over.`
- Why: mid-action openings read as an unfinished sequence; the viewer wants the resolution. Fits our storyteller voice
  (hooks-and-story memory: open on personal stakes).
- Ex 1: "She typed for a minute, then just sent 'haha'."
- Ex 2: "Her last text said 'sometime'. I waited six days."

### F5. Specific-Number Tension
- Pattern: `[Oddly specific number] + [behaviour] + [consequence].`
- Why: odd specifics (3 hours, 4 words, 2 days) feel observed rather than invented, so they feel true and credible.
- Ex 1: "If she waits exactly one hour to reply, read this."
- Ex 2: "Four words she uses when she's already gone."

### F6. Private-Moment Reveal ("what she's doing while you wait")
- Pattern: `What she's actually doing while [your text] sits on read.`
- Why: curiosity about the hidden side of a moment every man has sat through. It is empathetic, not creepy, if the
  payoff is about her real reasons (busy, unsure, testing, comparing).
- Ex 1: "What she's doing while your text sits on 'seen'."
- Ex 2: "She read it twice before replying 'lol'. Here's why."

### F7. Test / Verdict question
- Pattern: `Is she [interested / testing you / being polite]?` plus a promise of a rule to tell.
- Why: question hooks pull a mental answer; the viewer holds on to check theirs. Works as a comment/send prompt later ("send this to
  the friend who needs it"). Use ONLY with a clear 1-line answer in sec 3-6, or it is clickbait.
- Ex 1: "Is she testing you, or just being polite?"
- Ex 2: "Three signs she's still deciding about you."

### F8. Direct address / "if you've ever"
- Pattern: `If she [behaviour], stop [reflex] and do this instead.`
- Why: second person plus a pre-stated reflex (replying fast, double-texting) names the viewer's own habit.
- Ex 1: "If she goes quiet, don't double text. Do this."
- Ex 2: "If she says 'we should hang sometime', listen closely."

### F9. Translation Format ("What she says / what she means")
- Pattern: `She says "[phrase]". She means [meaning].`
- Why: a decoder promise with a built-in structure; very shareable (sends) because people forward a translation to a friend.
- Ex 1: "She says 'I'm just busy'. Here's what it can mean."
- Ex 2: "'You're so sweet' means something very specific."

Suggested rotation (variety rule): no more than 2 of the same format per 10 reels; F1, F4, F9 as the backbone; F7 sparingly.

---

## 2. The first visual (frame 0 to 1.5 s)

What sources agree on (mostly vendor, but consistent): the still at 0:00 is the hook for the viewers watching muted; the thumb decides in ~1 s;
text on frame one is the lowest-risk option; start mid-action; cut the "settle in" seconds; do not repeat the spoken line word for word on
screen, make the text set it up; keep text clear of the UI zones (vendor: blitzcutai, captions.ai).
Meta side: Mosseri calls the first 3 s "the hook"; Instagram added Skip Rate (leave within 3 s) to Reels retention reporting (2025).

### Concrete choices for our faceless 2D B&W style
1. **A phone screen with HER message, large.** A close crop of a phone, her bubble readable: "haha", "sometime", "k.". This is the
   recognisable moment for the audience; the one-word reply IS the visual. Best for texting topics.
2. **The read receipt moment.** Phone, "Seen 9:41 PM", thumb hovering over the keyboard.
3. **Man staring at phone, shoulder/over-the-shoulder shot**, face partly hidden (obscured reveal) in a dark room lit by the screen.
4. **Her turning away / glancing at the phone face-down** (an illustrated gesture that implies the behaviour).
5. **Split frame: what she typed vs what she sent** (typing indicator, then a short text). A transformation/contrast split.
6. **The empty chat**: last message from him, large time-stamp gap ("3 days ago"). Works with the number hooks.
- Avoid: abstract silhouettes, logos, a slow fade-in from black, a wide establishing shot, and our title card being blank for the first
  seconds. Title card text (0-2 s) must carry the hook line, not a brand slogan.

### Motion in frame 1
- Something must move in the first 10 frames: typing dots animating, a bubble popping in, a slow push-in (zoom 100% to 108%),
  a thumb tap, a screen light flicker. A static image with a late caption is the biggest likely cause of our 3 s drop.
- First clip should be shorter (about 1.2-1.5 s) than the usual 2-4 words/image cadence so the second visual change lands before 2 s.
- Do not start with a settle-in. Cut the first 0.3 s of silence on the narrator track; the voice should start on frame 1-3.

### Text on screen
- 3-7 words (vendor range 3-5 when layered with a spoken hook; 4-7 when alone). Our title card should be <= 7 words and
  ideally the hook verdict or the behaviour.
- Size: big enough to read on a phone thumbnail, think roughly 6-8% of frame height for cap height (my estimate; the vendor source gave no
  exact size). This is larger than Zoltium's in-body caption size; the hook card is a special case.
- Position: upper-middle third (about 25-40% down), inside the central safe area, not under the top profile strip nor the bottom 20-25% where the
  caption/UI sit.
- Contrast: white serif on a dark/black scene is already high contrast; add a gentle dark gradient behind the text, but no glow or purple.
- Sound-off test: screenshot frame 0 and frame 1.0 s. Can a stranger tell the topic and the tension without audio? If not, redo.

### Hook sequence template (0-3 s)
| Time | Voice | Screen text | Visual |
|---|---|---|---|
| 0.0-0.3 | (silent or start word) | Hook card appears | Moving shot of phone / her message |
| 0.3-2.5 | Hook line (<= 10 words) | Same idea, shorter wording | Push-in or typing animation |
| 2.5-3.0 | Verdict half-reveal | none/new image | Hard cut to scene 2 (payoff begins) |

---

## 3. Instagram signals 2025-2026 for small accounts

What is solid:
- **Three named signals**: watch time, likes per reach, sends per reach. Mosseri, January 2025 (confirmed in multiple summaries;
  see sources). Sends are seen as the strongest for reaching NON-followers; the "3-5x a like" multiplier is unverified.
- **Mosseri on the hook**: "The first three seconds of a reel are super important. Now, we call this the hook." (quoted in Inman, March 2025).
- **Skip Rate / retention metrics**: Instagram added a Skip Rate (viewers leaving within 3 s) and retention reporting in 2025.
  Check ours in Insights per reel; it is the direct scoreboard for this work.
- **Reels are the main surface that shows content to non-followers.**
- **Trial Reels**: shown to non-followers only, not on grid/followers. Mosseri: "It's going to get less reach, almost always."
  Evaluation window is reported as 24-72 h (sources disagree). The "42% at 3 s to graduate" figure is one blog and unverified.
  Practical use for us: test 2 hook variants of the same reel as Trial Reels and keep the winner on the grid.
- **Originality**: reposts/watermarked content deprioritised (third-party reports). We use original voice + illustrations, but our
  clips come from Pinterest, so keep our branding and edit transformative. Licensing is a separate risk (see memory notes).

What is soft or conflicting:
- **Length**: no official optimum. OpusClip (Nov 2025): 7-15 s entertainment, 15-30 s educational; "over 45 s rarely keeps above 30% retention
  unless exceptionally compelling"; but total watch time matters, a 30 s reel at 50% (15 s) beats a 10 s at 80% (8 s).
  Other blogs claim reels eligible up to 3 min or 20 min; unverified. Conclusion: our 32-40 s length is fine IF retention holds. Do not go to 45-90 s
  until the 3 s hold is fixed. A longer story format (45-60 s) is a test for later, only with a mid-reel re-hook (an open loop at ~15 s and ~30 s).
- **Rewatches count**: a short reel watched twice can outrank a longer one watched once (blog claim). A loop ending ("Decode her." tying to the hook line)
  helps replay.
- **Original audio vs trending audio**: one Buffer test says trending audio beat voiceover by 24% views. Single test. We keep our own voice (brand),
  so skip this lever.
- **Hashtags/captions**: keyword-first captions and <= 5 hashtags is already our rule; no new evidence found.

Implication: optimise in this order: (1) 3 s hold, (2) mid-reel retention/rewatch, (3) one clear send prompt (sends per reach), (4) likes.

---

## 4. Hook mistakes checklist (run on every script before voicing)

Slow / empty openings
- [ ] Greeting or channel intro ("Hey guys", "Welcome back", "Today we're talking about").
- [ ] "In this video" / "Here's why" / "Let me tell you" as the first words.
- [ ] Context before the claim (backstory first, tension later). The tension must be in line 1.
- [ ] Silence or a fade-in on frames 0-10; a title card that is just a logo.
- [ ] Narrator breathing/intro pause before the first word.

Vague or weak claims
- [ ] No specific behaviour named ("Women do this weird thing"). Name the exact behaviour: the word she typed, the time, the action.
- [ ] No verdict/tension, only a topic ("Let's talk about texting").
- [ ] Hook longer than 12 words, or two ideas in one line.
- [ ] Generic psychology jargon (attachment style, dopamine) in line 1; the viewer decodes a moment, not a term.
- [ ] Hook and title-card text are identical word for word (wasted second); make one set the other up.

Clickbait without payoff
- [ ] Question hook that the body never answers in under 6 s.
- [ ] Promise ("3 signs") not delivered as exactly 3, or the payoff is "it depends".
- [ ] Verdict that contradicts the body, or a shock claim the script cannot support with a reason.
- [ ] Unusual/mismatched first visual unrelated to the topic (reads as clickbait; vendor source warns).

Niche/brand traps
- [ ] Insulting or generalising women ("girls are all..."); PUA/manipulation tone.
- [ ] Focus/self-improvement topics (outside niche).
- [ ] Spoken "follow for more" (rejected 10-15).
- [ ] Hook text overlapping the Instagram UI zones; text smaller than ~5% of frame.
- [ ] First clip held >2 s with no motion.

Sound-off and Frame-0 tests
- [ ] Frame 0 as a still: understandable? Mute test passes? Is it different from our last 3 reels' first frames?

---

## 5. 25 hook lines (strongest first)

All <= 12 words, a specific behaviour of hers plus a verdict/tension. Rank is my judgement (specificity, recognisability, loop strength);
validate with real 3 s retention. "Visual" = suggested first image (frame 0-1.5 s).

| # | Hook | First visual |
|---|---|---|
| 1 | She replies "haha" and nothing else. Here's what it means. | Phone close-up, her grey bubble "haha", typing dots flicker, slow push-in |
| 2 | She takes three hours to reply, then sends a meme. | Clock face spinning to 3 hours, cut to phone with a meme bubble popping in |
| 3 | When she says "sometime", she's already decided. | Her bubble "we should hang sometime", thumb hovering over reply, hard zoom |
| 4 | She read your text twice before saying "lol". | Phone shows "Seen", her thumb pausing above the keyboard, light flicker |
| 5 | If she asks "what are you up to", don't answer literally. | Chat screen, her bubble pops in, his hand stalls on the keyboard |
| 6 | She stopped asking questions. That's the real warning sign. | Chat with only her short answers, question-mark bubbles fading out one by one |
| 7 | "You're so sweet" from her means something very specific. | Illustrated her smiling slightly turned away, text bubble beside her |
| 8 | She leaves you on read, then likes your story. Why? | Split frame: "Seen" on the left, heart on a story on the right |
| 9 | One-word replies aren't always boredom. Check this first. | Chat full of his long paragraphs vs her "k." with a push-in on "k." |
| 10 | Her "haha" and her "hahaha" are not the same. | Two bubbles, "haha" and "hahaha", swapping positions with a hard cut |
| 11 | She says she's busy, but she's online. Here's what that is. | Phone with "Active now" green dot pulsing, his reflection in the screen |
| 12 | She double texts you once, and then goes quiet. | Two grey bubbles stacked, then a long empty gap and a time-stamp "2 days" |
| 13 | She never starts the conversation. What that really says. | Empty chat top with only his messages on the right side; scroll upward |
| 14 | She changed the subject right after you asked her out. | Chat: his invite bubble, her reply about weekend plans, slow zoom |
| 15 | When she says "we'll see", read what she does next. | Her bubble "we'll see", cursor blinking, soft push-in |
| 16 | If she takes a day to reply, never apologise for waiting. | Calendar page flipping to next day, his thumb hovering over "Sorry" typed |
| 17 | She texts you only after 10 p.m. That's not random. | Phone lighting a dark bedroom, clock "10:47 PM", her name notification |
| 18 | The one text that makes her interest drop in minutes. | His thumb about to send, big "Send" arrow, a red bubble glitch effect |
| 19 | She sent three emojis instead of an answer. Decode it. | Chat showing three emoji bubbles stacked, each popping with a beat |
| 20 | She says "I'm bad at texting". Believe her, but notice this. | Her bubble with that line, his reply frozen mid-typing |
| 21 | Is she testing you, or just being polite? | Her half-smile illustration beside a question bubble, quick push-in |
| 22 | She asked "how's your day?" but only on Sundays. | Calendar with a Sunday circled, her bubble "how's your day?" |
| 23 | She laughs at your jokes but never plans anything. | Illustrated her laughing, then cut to an empty calendar |
| 24 | Three signs she's still deciding about you. | Three bubbles pop in on the chat, the last one blurred (obscured reveal) |
| 25 | Count how fast she replies. That number tells you everything. | Stopwatch overlay over a chat, ticking numerals on the first frame |

Notes for use:
- Lines 1-4, 8, 12, 15 are the recommended first batch (strong recognisable text-message moments, easy to illustrate with a phone).
- Each hook needs its payoff within seconds 3-8 (the verdict in plain words), then the body, then "Decode her.".
- Pair every reel with a different first-visual from section 2 so the grid and feed do not look identical.
- Run a 2-variant test as Trial Reels: same body, hook A (behaviour+verdict) vs hook B (mid-scene cold open). Keep a log in `brain/`.

---

## 6. Implementation checklist (for the factory/plan)
1. Title card (0-2 s) = the hook in <= 7 words, upper-middle position, with motion in the background clip from frame 1.
2. First segment cut to ~1.2-1.5 s, voice starts at frame 1-3.
3. Hook line <= 10-12 words, behaviour + verdict, no greeting.
4. Check each reel's Insights: 3 s skip rate (target: under 40% skipped, i.e. over 60% hold; vendor benchmark, not Meta's) and watch time.
5. Use Trial Reels for hook A/B tests when available.
6. Re-hook (an open loop sentence) around 12-15 s in longer scripts.

---

## Sources (accessed 2026-10-16; most are vendor/marketing blogs, treat numbers as unverified)
- Inman, "Head of Instagram reveals secrets to social media success", 2025-03-07, https://news.inman.com/2025/03/07/head-of-instagram-reveals-secrets-to-social-media-success/ (Mosseri quote: first three seconds are the hook; sends matter)
- Engadget, Instagram "Trial Reels" launch, https://www.engadget.com/social-media/instagram-will-let-video-creators-make-trial-reels-for-non-followers-160016725.html
- Postfa.st, Trial Reels explainer, https://postfa.st/blog/instagram-trial-reels
- Storrito, Trial Reels 72 hours, https://storrito.com/resources/how-instagram-trial-reels-work-72-hours/
- Blitzcut, "Visual Hook Formats for Instagram Reels (2026)", https://blitzcutai.com/blog/visual-hooks-instagram-reels
- Blitzcut, "What Makes a Reel Hook Go Viral? (2026 Breakdown)", https://blitzcutai.com/blog/what-makes-a-reel-hook-viral
- OpusClip (Parker Miller), "The Ideal Instagram Reels Length & Format for Retention", 2025-11-11, https://www.opus.pro/blog/ideal-instagram-reels-length
- Captions.ai, how to make Instagram Reels (2026), https://captions.ai/blog/how-to-make-instagram-reels
- eClincher, "How the Instagram Algorithm Works in 2026", https://www.eclincher.com/articles/how-the-instagram-algorithm-works-in-2026
- SocialPilot, "Instagram Reels Algorithm 2026", https://www.socialpilot.co/de/blog/instagram-reels-algorithm
- Metricool, "The Complete Instagram Reels Guide 2026", https://metricool.com/instagram-reels-guide/
- PostEverywhere, "How the Instagram Algorithm Works in 2026", https://posteverywhere.ai/blog/how-the-instagram-algorithm-works
- Nestscale, "Increase Hook Rate on TikTok & Reels in 2026", https://nestscale.com/?p=47200
- Social Media Today, Instagram Reels tips, https://www.socialmediatoday.com/trendline/everything-you-need-to-know-about-instagram-reels/274/
- Gap: Meta's own creators.instagram.com guidance and Mosseri's original posts were not reachable via search; confirm there before treating any figure here as policy.
