# Growth plan, 14 days (written 2026-10-15)

Owner: growth. This builds on [[growth/views-diagnosis-2026-10-15]] and replaces its §5 test plan.
Tags: **[D]** our own Instagram data · **[V]** checked in our files or a source · **[I]** my inference.

**In one sentence:** Instagram is showing every reel to ~120 strangers. They aren't sharing it, and they leave
by the 10th second, so it never gets a second, bigger test group. We aren't being blocked. The reels just don't win that first test yet.

---

## 1. The data (Instagram Graph API, read-only, pulled 2026-10-15 ~09:30 IST)

Account: @thedecodeher, creator account, **6 followers**, follows 0, 3 posts.
Profile name field `DecodeHer | Dating Advice for Men` and the keyword bio are already in place.

| Reel (posted, IST) | Length | Reach | Views | Likes | Comments | Shares | Saves | Skip rate (left in first 3 s) | Avg watch | Avg watch ÷ length |
|---|---|---|---|---|---|---|---|---|---|---|
| "Busy" (w1, silhouette style), 10-13 22:13 | ~43 s | 134 | 180 | 6 | 0 | 0 | 0 | **66.9 %** | 10.6 s | ~25 % |
| "Keep yourself" (w2-12), 10-14 21:05 | 36.0 s | 127 | 153 | 7 | 0 | 0 | 0 | **54.7 %** | 10.4 s | 29 % |
| "Is she testing you?" (w2-01 remake, title card, voice v2), 10-15 08:32 | 40.2 s | 115 | 126 | 2 | 0 | 0 | 0 | **43.1 %** | 8.5 s | 21 % |
| **Total** | | **376** | 459 | 15 | **0** | **0** | **0** | | | |

Account reach: 240 on 10-14 (from all content). Profile link taps: 0. The API refused per-reel `follows` and `profile_visits`
for Reels, so follows per reel have to be read in the app.
The 10-15 reel is only ~6 h old, so its numbers will still move. The other two have had 1–2 days and look settled.

**What the numbers say**
1. **Skip rate is improving with each change**: 67 → 55 → 43 %. The title card plus the "behaviour + verdict" first line is working.
   It's still above the ~35–40 % that practitioners call healthy (no official benchmark exists, see Sources). [D]
2. **The middle of the reel is the bigger leak.** About 57 % of viewers got past second 3 on the newest reel, but the average
   watch is only 8.5 s of 40 s. Even the people who stayed left around second 12–15. [D + arithmetic]
3. **Zero shares, saves and comments on 376 reach.** Mosseri names sends per reach as the main signal for reaching
   non-followers. With zero sends, the reel has nothing that earns it a second, wider test. [D]
4. Reach (115–134) is about 20× our follower count, so Instagram is already recommending us to strangers. **We are not shadow-banned.** [D]
5. Three reels is a tiny sample. Treat every conclusion below as "most likely", not proven.

---

## 2. Top 5 causes, ranked by likely impact

### 1. The reels are too long for how much happens in them (retention collapse after ~10 s)
- Evidence [D]: avg watch is 21–29 % of the length on all three reels. The same ~10 s average holds whether the reel is 36 s or 43 s,
  so the extra length only lowers the percentage.
- Evidence [V], w2-01 script: line 2 is "I used to fail this every single time." Lines 3–5 retell the confession. The "why"
  ("She was checking if I'd shake") doesn't arrive until ~14 s, after most viewers have gone.
- Instagram ranks on watch time *relative to length*, plus rewatches [V, practitioner sources]. A 22 s reel watched for 11 s
  (50 %, often looped) beats a 40 s reel watched for 10 s.

### 2. Nothing in the reel makes a man want to send it (0 sends, 0 saves, 0 comments)
- Evidence [D]: 0 / 376.
- The topics are self-improvement lessons ("keep your gym", "don't compete"). They're good advice, but nobody forwards them to a friend.
  What gets sent in this niche is a **verdict about a specific thing she did**, something men argue about in group chats
  ("she said 'I'm bad at texting'", "she viewed my story but won't reply"). [I, backed by competitors-2026-10.md:
  "signs she likes you" and "if a girl says X" are the most-viewed formats.]
- The send/comment prompt lives only in the caption, and almost nobody on the Reels tab reads it. The reel itself never asks.
- Nothing gives a reason to save it: no list, no exact text to copy, no "screenshot this".

### 3. The first 3 seconds still lose ~43 % of viewers
Evidence, frames of the posted 10-15 reel (0, 0.6, 1.2, 2.0, 3.0, 5.0 s) [V]:
- The whole frame is **very dark and low-contrast**. On a bright phone feed it reads as "nothing here".
- **At 2.0 s the frame goes almost completely black** (the phone screen in the clip switches off), right inside the
  3-second skip window.
- The title card "Is she testing you?" is thin and smallish at the top. The word captions are small, mid-screen and sit on busy art.
- The first clip is a rough cartoon of a laughing girl on a phone. It reads as a meme or a repost, not as a branded story.
- The first spoken line takes ~3.5 s ("She mentions some guy who texted her… and watches your face."), and its stake (a test)
  only comes from the title, not the voice.

### 4. No reason to follow (6 followers, 0 profile-link taps)
- Each reel is a stand-alone lesson. There's no series, no "part 2" and no promise of what comes next. A stranger who liked one reel
  has no reason to expect the next one to be for him. [I]
- The three posts look like three different pages: silhouette, colour clips, then B&W serif. The grid doesn't say "this is a show". [V]
- The ending ("Decode her." over the logo) is a brand sign-off, not a reason to follow. That's fine as a signature, but
  something earlier in the reel has to create the follow ("part 2 tomorrow", "I decode one text every day"). [I]

### 5. The look may read as unoriginal or low effort (reused Pinterest art, mixed styles)
- Clips are other artists' illustrations, often recognisable, in mixed styles within one reel. [V, views-diagnosis §1.5]
- Instagram's originality rules (Reels since 2024, widened 30 Apr 2026) keep "mostly others' content" accounts out of
  recommendations. Our voiceover and editing probably count as adding value, and the data shows we *are* recommended. But matching
  against existing posts can still lower our ranking quietly. [I]
- This is ranked last because the account demonstrably gets recommended. It becomes urgent if the app shows "not eligible for
  recommendation" on any reel (see the checks in §3).

**Checked and NOT the cause:** a shadow-ban (reach is 20× followers); hashtags (now ≤ 5); the profile name and bio (already keyword-first);
posting through the API (no evidence API posts are ranked lower); 2 posts a day (Mosseri: more posts, more total reach).

---

## 3. The 14-day plan (10-16 → 10-29)

### Day 0–1 (10-15/16): checks (5 minutes in the app, the owner does this)
1. Settings → **Account status** → "Recommendations": it must say eligible. If not, stop everything and fix that first.
2. Open each reel → View insights. Note: **% views from non-followers**, **follows**, and the retention graph (where the drop happens).
   Look for a "not eligible for recommendation" note on each reel.
3. On the share screen of a new reel, look for the **Trial** toggle. If it's there, we use it (see Trial Reels below).

### Changes for every new reel from now on (the "v3 format")
| Area | Change | Why |
|---|---|---|
| **Length** | **20–28 s**, 55–70 spoken words, 6–8 lines. Hard cap 30 s. | Fixes cause 1. Same ~10 s of watch becomes 40–50 %. |
| **Line 1** | Her behaviour + verdict, ≤ 8 words, spoken by **1.8 s**. Ideally a quoted line she sends: *"'I'm bad at texting.' No, she isn't."* | Skip rate. |
| **Line 2** | The stake to HIM in one line ("and every fast reply makes it worse"). **No confession line, no "I used to…"** in the first 6 s. | Cause 1, cause 3. |
| **Middle** | One re-hook at 8–10 s ("But watch what she does next."). The "why" by 12 s. The move (an exact line to say) by 18 s. | Viewers leave at 10–15 s now. |
| **Ending** | The payoff calls back to the hook word, then "Decode her." Keep the outro ≤ 1.5 s. The last word should flow into line 1 so the reel loops. | Rewatches count as watch time. |
| **First frame** | Bright and readable. Use **a phone chat bubble with her exact words in large text** (an on-screen bubble we draw, not a clip) OR the brightest single-subject clip. Title card stays 0–2 s, **bigger (≈2× the current size) and lower (top third, not the edge)**. No dark or near-black frame anywhere in 0–3 s. | Cause 3. Viewers decide with the sound off. |
| **Clip grade** | Lift the B&W grade: blacks not crushed, mid-grey subjects. The darkness is atmosphere at 30 s, but at 0–3 s it reads as an empty screen. | Cause 3. |
| **Send trigger, IN the reel** | One spoken + on-screen line at ~70–80 % of the reel, rotating: "Send this to the guy who still double-texts." / "Screenshot the line, use it tonight." / "Comment the text she sent you. I'll decode it." | Cause 2. |
| **Follow reason** | Make 2 **series** with a numbered title card: **"Decode her text #N"** (we decode one real-sounding message she sent) and **"Signs she likes you #N"**. Say once in the reel: "I decode one of her texts every day." | Cause 4. A series gives a reason to follow. |
| **Topics** | 2 of every 3 reels from the search bank, phrased as *a thing she did/said*. Self-respect stays the answer inside the reel, never the topic. | Cause 2. |
| **Captions** | Keep the keyword-first format and ≤ 5 tags. Add the comment prompt as line 2. | Already done. |
| **Covers** | Title-card frame, as agreed. Once the series exist, use the same cover layout for every episode so the grid reads as a show. | Cause 4. |
| **Clips** | One art style per reel. Prefer clips that aren't instantly recognisable. Crop, re-time and grade every clip (we already do). Hold no single clip > 2 s. | Cause 5. |

### What happens to the 10 booked reels (10-15 → 10-19)
They're the old format (36–43 s, lesson topics). Don't scrap them. **Keep the morning slot (08:30) running the booked reels as the
control group**, and from **10-17** put a v3 reel into the evening slot (21:00) each day as soon as one is ready. That way each day
compares old vs new on the same day. Each evening reel pushed out by this moves to the end of the queue, not into the bin.

### A/B tests (one change per test, 3+ reels per arm before deciding)
| Days | Test | Arm A | Arm B | Decide on |
|---|---|---|---|---|
| 10-17 → 10-20 | **Format** | booked reel, 36–43 s (AM) | v3, 20–28 s (PM) | avg watch % and skip rate |
| 10-21 → 10-24 | **First frame** | chat-bubble text frame | best illustration frame + big title | skip rate |
| 10-25 → 10-29 | **Send trigger** | "send this to the guy who…" | "comment her text, I'll decode it" | sends + comments per 100 reach |

Keep the hook formula, voice and caption style the same within a test. **Note for steps 1–2 of THE PLAN (new captions + new voice):**
ship them together in the v3 format from 10-17. Don't change them mid-test, or we won't know what worked.

**Trial Reels:** most sources say the app shows them from ~1,000 followers (some say 200; it's a staged rollout). If the toggle
appears, post every **test arm** as a Trial (shown to non-followers only, so a weak test doesn't touch followers). Until then,
the two daily slots are our A/B. Do not try Trial through the API before the app shows the toggle.

### Metrics to watch (read each reel at 24 h and 72 h, in Insights or via a read-only API script)
| Metric | Now | Target by 10-22 | Target by 10-29 |
|---|---|---|---|
| Skip rate | 43–67 % | < 40 % | **< 35 %** |
| Avg watch ÷ length | 21–29 % | > 40 % | **> 50 %** |
| Views ÷ reach (loops) | 1.1–1.3 | > 1.3 | > 1.5 |
| Sends per 100 reach | 0 | ≥ 0.5 | **≥ 1** |
| Saves + comments per 100 reach | 0 | ≥ 1 | ≥ 2 |
| Reach of the best reel | 134 | > 500 | > 2,000 |
| Followers | 6 | 25 | **100** |

### Decision rules
- **A reel that gets > 400 reach in 48 h**: make 2 more on the same topic within 3 days (same hook shape, a different situation),
  and pin it.
- **If v3 beats the old format on avg watch % across 3 reels**: stop posting the old format and move every remaining booked
  reel to 08:30 only, or re-cut it to ≤ 30 s.
- **Skip rate > 50 % on a reel**: the first frame or line 1 failed. Next reel: chat-bubble first frame + a quoted line hook.
- **Skip rate < 35 % but avg watch < 35 %**: the hook works, the middle doesn't. Cut lines, re-hook at 8 s, aim for 20 s.
- **Retention fine but 0 sends after 5 v3 reels**: the topic is the problem, not the edit. Switch to "decode her text" reels only.
- **By 10-29, if no reel has passed 500 reach** even with skip < 40 % and watch > 45 %: suspect originality/look (cause 5).
  Make 3 reels with no Pinterest art (our own drawn chat bubbles + simple text animation) and compare.
- **Never judge a reel before 24 h.** Judge a format only on 3+ reels.

---

## 4. STOP doing
1. **Stop making 36–43 s reels.** Hard cap 30 s until a reel holds > 50 %.
2. **Stop the confession line 2** ("I used to fail this every single time.", "Yeah. I did that too."). A story is fine in line 3–4, after the stake.
3. **Stop dark or black frames in the first 3 s** (the 10-15 reel goes almost black at 2.0 s).
4. **Stop lesson topics** ("keep your gym", "your plans matter") as the headline. They're answers, not hooks.
5. **Stop putting the only call to action in the caption.** The reel itself has to ask for the send, save or comment.
6. **Stop changing five things at once** (voice, caption font, covers, outro, topic) between posts without logging it.
   Log what changed per reel in the queue, or the data means nothing.
7. **Stop judging by views at 2 hours** and stop reacting to one reel. Read at 24 h and 72 h, decide on three.
8. **Stop putting growth time into the studio board** (THE PLAN step 5) until a reel passes 500 reach. It doesn't move views.

---

## 5. Risks
| Risk | How likely | What to do |
|---|---|---|
| **Unoriginal content / Pinterest art.** Reused illustrations from other creators are matched against existing posts; accounts that "mostly share others' content" lose recommendations (rule widened 30 Apr 2026). Pinterest art is also not licensed for reposting (see the voice-and-assets-licensing memory). | Medium now, high if we scale | Check Account status weekly. Keep the voiceover and edits heavy. Move step by step to our own visual layer: chat bubbles, text cards, our bust and silhouettes. Never post a clip with another creator's watermark. |
| **Copyright takedown** by an artist whose drawing we used. | Low–medium | Keep a source list per reel (we have shots.json). Remove a reel at once if asked. Prefer the Drive library. |
| **AI label / AI voice.** The relay sends `is_ai_generated`. The August 2026 reach limit targets unlabelled AI *personas*, not us. A robotic voice still hurts retention. | Low for reach, medium for retention | Keep the label. Pick the new voice on retention (THE PLAN step 2), not only on taste. |
| **Brand drift into rage bait.** "Women are…" hooks get comments fast and poison the page (PsycheDepth pattern). | Medium (tempting) | Verdicts about a *behaviour*, never about women as a group. |
| **Too few posts per arm.** 2/day × 14 days = 28 reels, ~9 per test. Enough for big effects only. | Certain | Only act on big gaps (e.g. skip 35 % vs 50 %). |
| **The factory posts a reel that hasn't been checked** (black frame, broken file). | Medium | Add a check: no frame darker than X in 0–3 s, length ≤ 30 s for v3. |

---

## Gaps
- The API doesn't give follows, profile visits or "% non-followers" per reel. Read them in the app.
- The 10-15 reel was ~6 h old when pulled. Re-pull on 10-16.
- A read-only stats script (`me` + `me/media` + per-reel insights incl. `reels_skip_rate`, `ig_reels_avg_watch_time`) worked on 10-15.
  It's worth turning it into `tools/ig_stats.py` and printing it daily into `brain/growth/stats.md`.

## Sources
- Mosseri signals (watch time, likes per reach, sends per reach), via [eClincher 2026](https://www.eclincher.com/articles/how-the-instagram-algorithm-works-in-2026) and [Dataslayer](https://dataslayer.ai/blog/instagram-algorithm-2025-complete-guide-for-marketers) (secondhand; no primary 2026 restatement found)
- Skip rate definition and practitioner thresholds: [Metricool](https://metricool.com/instagram-reel-analytics/), [Inro](https://www.inro.social/blog/instagram-reels-insights), [TrueFutureMedia](https://www.truefuturemedia.com/articles/lower-instagram-reels-skip-rate). No official benchmark; Instagram shows "typical skip rate" from your own history.
- Trial Reels: [TechCrunch Dec 2024](https://techcrunch.com/2024/12/10/instagram-rolls-out-trial-reels-that-arent-shown-to-a-creators-followers), [Publer guide](https://publer.com/blog/instagram-trial-reels-guide/), [Outfy](https://outfy.com/blog/instagram-trial-reels) (thresholds conflict: none / 200 / 1,000)
- Originality: [3rd and Lamar, May 2026](https://3rdandlamar.com/news/how-instagrams-new-policy-impacts-video-clipping/), [Sociallyin](https://sociallyin.com/blog/instagram-algorithm-update-repost/), [Lindsey Gamble 2024](https://lindseygamble.com/blog/instagram-is-tweaking-its-algorithm-to-prioritize-original-content-creators)
- Recommendation eligibility: [Instagram creators blog](https://creators.instagram.com/blog/instagram-recommendations-eligibility-tips-creators), [Instagram Help](https://help.instagram.com/653964212890722)
- Posting frequency: [SocialPilot](https://www.socialpilot.co/instagram-marketing/how-often-to-post-on-instagram)
- First-frame and on-screen text practice: [Opus](https://www.opus.pro/blog/instagram-reels-caption-subtitle-best-practices), [TrueFutureMedia hooks](https://www.truefuturemedia.com/articles/instagram-reels-hooks-two-step-test) (vendor blogs, directional only)
- Our own: [[research/competitors-2026-10]], [[research/hooks-retention-v2]], [[research/zoltium-story-visuals]], [[research/profile-premium-2026-10]]
