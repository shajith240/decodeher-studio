# Why our reels sit at ~120–130 views, and what to do (2026-10-15)

**Read this first.** Only **2 reels are live** (10-13 "Busy is an answer", silhouette style; 10-14 "Keep yourself", clip style).
That is too few to prove anything. ~100–200 views is the size of the first test group Instagram shows a new account's reel to.
The reel only goes wider if that group watches, rewatches and sends it. So "stuck" here means the reels fail that first test.
They are not being blocked. The fix is in the first 3 seconds and in shares, not a hidden penalty.

Tags: **[V]** checked in our files or a source · **[I]** my inference.

---

## 1. Why we're stuck: top 5 causes

**1. The first 3 seconds don't name a topic a stranger cares about.** [V]
- Frame at 0.3 s of "Keep yourself": a kissing-couple cartoon, with "YOU FINALLY GOT" in thin small caps.
  The second shot shows only "HER…". Nobody can tell what the reel is about before second 2.
- Line 2 of every week-2 script is filler ("Yeah. I did that too." / "Bro, this used to drive me crazy." /
  "I used to fail this every single time.") That stalls seconds 2–4, right where Skip Rate is measured.
- 5 of the 5 scripts I read have a "Here's what…" line. Our own rules ban it (brain/rules/script-and-hooks.md).
- Instagram's Skip Rate is the share of viewers who leave in the first 3 s. Guides call over ~50 % a broken hook.

**2. Topics are "self-respect" lessons, not things men search for or send to friends.** [V/I]
- Week-2 topics: drop your plans, keep your gym, don't change your hair, she's 40 minutes late. These are good advice.
  Nobody types them into search, though, and nobody sends them to a friend.
- Search demand in the niche sits on "signs she likes you", "mixed signals" and "why she stopped texting".
  Only 2 of the 8 queued reels (just-ask = mixed signals, take-it-offline = texting) hit that.
- Mosseri named **sends per reach** as the top signal for reaching non-followers (Jan 2025).
  We close on "Follow for more" and never give a reason to send the reel.

**3. No keywords where Instagram reads them.** [V]
- Caption first lines are hooks with emojis ("You finally got her… then dropped your whole life? 🫠").
  None contains a searchable phrase like "dating advice for men" or "signs she likes you".
- On-screen text is 3-word fragments, so the screen never states the topic either.
- The **cover** is the frame at 1.5 s (`thumb_offset` 1500 in relay/worker.js). For "Keep yourself" that frame shows only "HER…".
  That is a weak grid tile and a weak search result.

**4. Hashtags break the 5-tag cap and are too broad.** [V]
- Instagram capped posts and Reels at **5 hashtags** (announced 18 Dec 2025).
- Our queued captions carry **7–8** (e.g. 02-Tue: 8 tags). Our own rule already says 3–5.
- `#psychology` and `#relationships` tell the classifier "general psychology / couples", not "dating advice for men".
- Extra tags may be stripped, or the post blocked. Either way they don't help.

**5. Originality and "same style as everyone" risk from Pinterest clips.** [I, partly V]
- The frames show mixed art styles from other people's work: a "CROWD" kinetic-type clip, a known-looking couple comic,
  a stick figure in another style.
- Instagram's rule (extended 30 Apr 2026) says voiceover and creative edits count as adding value. So we are probably **not**
  classed as an aggregator.
- But the matching system can still treat a reel built mostly of clips already on Instagram as less original [I].
- Mixed styles also weaken the "this is a brand" signal.
- Smaller factors [I]:
  - Library music (Kevin MacLeod) means we never show up on a trending-audio page.
  - The ~2 s logo outro after the spoken CTA lowers completion.
  - Post 1 (silhouette) and post 2 (clip) look like two different pages.

**Not causes (checked):**
- 2 posts a day. Mosseri says more posts means more total reach, so pick a pace you can keep.
- The AI label. The reach penalty (31 Aug 2026) is for unlabelled AI *persons/profiles*; we have no AI person, and we already send `is_ai_generated`.

**Separate risk found:** the local file `deliverables/queue/08-W2-just-ask-FINAL.mp4` is truncated (ffprobe: "moov atom not found").
Check the hosted copy before it posts on 10-17 08:30.

---

## 2. Do this next (highest impact first)

1. **New hook rule: topic and stakes on screen by 1.0 s.** *(script/hook + on-screen text)*
   - The first line names a girl's behaviour plus a verdict, in ≤ 10 words, e.g. "If she replies in 4 hours, she's not busy."
   - Delete the filler line 2 ("Bro, I…"). The confession goes in line 3, if anywhere.
   - Cut every "Here's what…". Use "But look at the timing." or similar instead.
   - **Check:** Skip Rate under 40 % and average watch time over 15 s on the next 6 reels (Insights → reel → Retention), within 48 h of each post.
2. **A fixed title card for the first 2 s.** *(on-screen text, HyperFrames layer)*
   - One bold line of 4–7 words at the top third, held for 2 s over the clips, e.g. **SIGNS SHE'S LOSING INTEREST**.
   - Then the normal word captions.
   - Set `thumb_offset` to a frame where the title shows (~500 ms), or pass a `cover_url`.
   - **Check:** Skip Rate drops vs. the last reels; reach from "Reels tab / Explore" rises.
3. **Shift topics to search and send demand.** *(batch planning)*
   - At least 2 of every 3 reels from the keyword bank below: signs, texting, mixed signals, why she pulled away.
   - Self-respect becomes the *answer* inside those reels, not the topic.
   - **Check:** shares per 100 views ≥ 1 within 7 days.
4. **Give one reason to send it, once per reel.** *(script, last 5 s)*
   - Not a mocking "send this to the guy who…". Use a useful one: "Send this to your boy who keeps asking 'what does her text mean'."
   - Or a comment prompt: "Comment the text she sent, I'll decode it."
   - Keep "Follow for more."
   - **Check:** sends and comments per reel compared with now.
5. **Captions: keyword first line, 3–5 exact hashtags.** *(captions: week2-captions.json → queue caption.txt)*
   - Use the template in §3. Remove `#psychology` `#relationships` `#modernromance`.
   - Re-write the 7 queued captions before they post; this is a text-only change.
   - **Check:** "From search" shows up in reel views within 7 days.
6. **Fix the profile.**
   - Name field: `DecodeHer | Dating Advice for Men`.
   - Bio line 2: "Signs she likes you, texting, mixed signals: decoded."
   - Pin the 3 best reels once there are 10+.
7. **Tighten the end and the look.** *(reel_mix / outro, clip picking)*
   - Cut the outro logo to ≤ 1 s. The last spoken words should loop into the hook.
   - Pick clips from one art style per reel. Prefer our Drive library and clips we restyle (grade, crop, re-time) over raw Pinterest.
   - **Check:** average watch time ÷ length over 50 %.
8. **Use Trial Reels once they are available.** *(relay)*
   - The Content Publishing API accepts `trial_params` (graduation `SS_PERFORMANCE`). The app may only show the feature at ~200–1,000 followers.
   - Until then, A/B through the two daily slots (see §5).

---

## 3. Keywords

**Search phrases (use in the caption's first line, the title card, and the spoken first sentence):**
signs she likes you · how to know if she's interested · signs a girl likes you but hides it · mixed signals ·
hot and cold · why she stopped texting · she left me on read · dry texter · how to text a girl ·
what to text her · texting her first · why she pulled away · signs she's losing interest · how to ask her out ·
first date tips for men · friend zone · how to keep her interested · what women find attractive ·
female psychology · body language signs she likes you · she says she's busy · dating advice for men

**Bio keywords:** dating advice for men · texting · signs she likes you · female psychology.

**Hashtags: max 5 (Instagram's hard cap since Dec 2025, caption and comments counted together).**
Formula: 2 niche + 2 topic + 0–1 broad.
- Always: `#datingadviceformen` `#datingtips`
- Topic (pick 2): `#mixedsignals` `#textingtips` `#signsshelikesyou` `#femalepsychology` `#friendzone` `#firstdate`
- Optional broad: `#datingadvice`

**Caption template**
```
[Search phrase as a plain sentence]: [the reel's verdict in one line].
[One line naming his exact situation.]
[Send/comment prompt.]
Follow @thedecodeher for more dating advice for men.
#datingadviceformen #datingtips #[topic1] #[topic2]
[music credit if CC-BY]
```

**Example A: w2-16 "Just ask" (mixed signals)**
- Hook (spoken + title card): **"Flirty Friday, one-word replies Sunday? That's not a game."**
- Caption:
  > Mixed signals from her? Most of them aren't a game, they're things nobody said out loud.
  > Warm one day, dry texter the next, and you're rereading the chat at 2 a.m.
  > Send this to the friend who keeps asking "what does her text mean."
  > Follow @thedecodeher for more dating advice for men.
  > #datingadviceformen #datingtips #mixedsignals #textingtips

**Example B: w2-10 "Take it offline" (texting)**
- Hook: **"If your chat with her dies after 'what are you up to', this is why."** Title card: **WHY HER TEXTS GO DRY**.
- Caption:
  > Why she stopped texting back: your questions feel like work.
  > "What are you up to?" "Nothing." Say something about HER instead, then ask her out.
  > Comment the last text you sent her and I'll fix it.
  > Follow @thedecodeher for more dating advice for men.
  > #datingadviceformen #datingtips #textingtips #howtotextagirl

---

## 4. News (Instagram changes that matter to us)

| Date | Change | What it means for us |
|---|---|---|
| Jan 2025 | Mosseri: top ranking signals are watch time, likes per reach, **sends per reach** (sends matter most for non-followers) | Build a send reason into every reel |
| 10 Jul 2025 | Public professional accounts indexable by Google/Bing | Captions and bio double as web SEO |
| Aug 2025 | **Skip Rate** and a retention chart added to Reels Insights (the first 3 s) | Our main hook metric |
| Dec 2025 | Skip Rate and new metrics reported in the insights API | We can pull it automatically later |
| 10 Dec 2025 | "Your Algorithm": viewers see and edit the topics that drive their Reels | Clear, repeated niche keywords help classification |
| 18 Dec 2025 | **5-hashtag cap** on posts and Reels | Our 7–8 tags must drop to ≤5 |
| 30 Apr 2026 | Reposters/aggregators lose all recommendations (Reels rule extended to photos/carousels); watermark or speed change ≠ original; voiceover + creative edits = OK | Keep voice and edits substantial; don't drift to raw clips |
| 31 Aug 2026 | Unlabelled AI-*person* profiles get limited reach; AI tools for editing don't need the label | Not us (no AI persona), but keep `is_ai_generated` |
| 2025–26 | Trial Reels in the publishing API (`trial_params`) | Test hooks on non-followers once eligible |

---

## 5. Test plan, next 7 days (14 posts)

- **Test 1, hook style (days 1–4).** AM slot: verdict hook ("If she does X, it means Y").
  PM slot: question hook ("Why does she go cold right after a great date?"). Same title-card rule for both.
- **Test 2, title card on vs. off (days 5–7).** Same hook style both slots, only the 2-s title card changes.
- **Read it at 48 h per reel**, in the app (Reel → View insights). Log these numbers:
  - Skip Rate
  - Average watch time
  - Views
  - Shares
  - Saves
  - Follows
  - "Views from non-followers %"
- **The winner** has lower Skip Rate and higher shares per 100 views across at least 3 reels. One reel proves nothing.
- **Success by 2026-10-22:** at least 1 reel over 500 views, median Skip Rate under 40 %, shares on every reel.
- **If all reels still sit under 200 views with Skip Rate over 50 %:** the hook and first frame are still the problem.
  Make the title card bigger, use a phone-chat screenshot as the first frame, and cut the hook to ≤ 7 words.
- **Gap:** `tools/content_sync.js` pulls views/reach/saves/shares but rewrites brain files, and it lacks Skip Rate and watch time.
  A read-only stats printer (adding `ig_reels_avg_watch_time` and skip rate) would make this test automatic.

---
Sources:
- [TechCrunch, 30 Apr 2026](https://techcrunch.com/2026/04/30/instagram-restricts-reach-of-content-aggregators-in-new-crackdown/)
- [Tubefilter](https://tubefilter.com/2026/04/30/instagram-removes-algorithm-recommendations-repost-content-aggregator)
- [Later, hashtags 2026](https://later.com/blog/instagram-hashtags/amp)
- [Lilach Bullock, hashtag limit](https://www.lilachbullock.com/instagram-hashtag-limit/)
- [Social Samosa, Skip Rate](https://www.socialsamosa.com/news-2/instagram-retention-chart-skip-rate-new-performance-metrics-reels-9730992)
- [Metricool](https://metricool.com/instagram-reel-analytics/)
- [Meta media insights](https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/insights/)
- [Meta changelog](https://developers.facebook.com/docs/instagram-platform/changelog)
- [Bundle.social, trial reels API](https://info.bundle.social/api-reference/platforms/instagram)
- [TechCrunch, Your Algorithm](https://techcrunch.com/2025/12/10/instagrams-new-your-algorithm-tool-gives-you-more-control-over-the-reels-you-see)
- [MediaPost, AI profile label](https://mediapost.com/publications/article/417580/instagram-limits-reach-for-creator-profiles-withou.html)
- [eClincher, ranking signals](https://www.eclincher.com/articles/how-the-instagram-algorithm-works-in-2026)
- [RouteNote, Mosseri on frequency](https://routenote.com/blog/how-often-you-should-post-on-instagram/)
- [PPC Land, Google indexing](https://ppc.land/instagram-content-becomes-searchable-on-google-starting-july-10/)
