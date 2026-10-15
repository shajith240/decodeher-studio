# Profile audit: @thedecodeher (premium look + early reach), Oct 2026

Researched 2026-10-13. Scope: bio, name field, highlights, grid and covers, pinned posts, avatar, algorithm signals, and account setup for a new faceless Reels page.

**How to read this:** **[Fact]** means a sourced claim (link given). **[Opinion]** means our recommendation or judgment. Many "Instagram growth" blogs repeat numbers they can't back up, so they are flagged where they appear. Instagram's own statements (Mosseri, about.instagram.com, creators.instagram.com, the Meta developer changelog) carry more weight than vendor blogs.

---

## 0. TL;DR (the 10 changes that matter most)

1. **The API posting flow must send `is_ai_generated=true`.** The brain rule says "the owner switches on Instagram's AI label when posting", but we post through the API, so that in-app toggle is never seen. The Content Publishing API has supported the flag since 22 June 2026, and it can only be set when the container is created. [Fact, [Meta changelog](https://developers.facebook.com/docs/instagram-platform/changelog)]
2. **Hashtags: cap them at 3–5.** Instagram is rolling out a hard limit of 5 hashtags per post/Reel ([Social Media Today, Dec 2025](https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/)). Our caption rule says "4–6", so change it to "3–5". Put the search value in plain keyword sentences instead.
3. **Name field:** `DecodeHer | Dating Advice for Men` (see §1).
4. **Bio:** drop the slashes and "guys". Use three lines: a hook, a keyword line, and a cadence line plus a CTA (5 options in §1).
5. **Highlights: not yet.** Add them only after there are real Stories to fill them (see §2).
6. **Covers:** design every Reel cover for the 3:4 grid crop (centre 1080×1440 of the 1080×1920 frame). Use one fixed cover template: a short 2–4 word title in Montserrat Black Italic, one purple accent word, the same position every time.
7. **Pin 3 posts** once you have 6+ reels: your best "relatable story" reel, a "start here / what this page is" reel, and your most-sent reel (see §3).
8. **Avatar:** the cream "dh" is high-contrast but doesn't say anything about the niche and leaves out the brand purple. Add a thin #B26BFF rim ring (direction A), or switch to a silhouette symbol (direction B). See §4.
9. **What to optimise for:** sends per reach (non-follower reach), watch time and likes per reach (Mosseri, Jan 2025), plus a low skip rate in the first 3 s. Every reel's spoken CTA should favour "send this to…" over "like".
10. **Don't look automated:** vary posting times by ±20–40 min around one or two fixed slots, reply to comments by hand in the first hour, keep every reel structurally different (the existing variety ledger), and never use follow/DM automation.

---

## 1. Bio and name field

### What top faceless and education pages do

- **The name field is the main search lever on the profile.** Several SEO guides agree that the bold name (not the @handle) is weighted in Instagram search and should carry a keyword, in a "Brand | What you do" format. [Fact as practitioner consensus; Instagram doesn't publish the ranking: [Later](https://later.com/blog/instagram-seo/), [Inro](https://www.inro.social/blog/instagram-seo), [Vista Social](https://vistasocial.com/insights/instagram-seo/)]
- **Write the bio in the words a searcher would type.** Say who it's for and what they get, plainly, with no keyword stuffing. [Same sources]
- **Profiles and posts now reach Google too.** Since 10 July 2025, public professional (creator/business) accounts of adult users are indexable by Google and Bing by default. Captions and bios therefore also work as web SEO. [Fact: [PPC Land](https://ppc.land/instagram-content-becomes-searchable-on-google-starting-july-10/), [afaqs](https://www.afaqs.com/news/digital/search-engines-can-now-index-public-content-from-instagram-9483796)]
- **Links:** up to 5 links are allowed, and the first one shows with "and N other". [Fact: [Search Engine Land](https://searchengineland.com/instagram-now-allows-up-to-5-links-in-bio-395742)] We have nothing to link to yet. [Opinion] Leave the link empty rather than use an empty Linktree. An empty or placeholder link looks cheaper than no link. Add one when there is a real lead magnet (for example a free "texting playbook" PDF or a newsletter).
- **Structure used by the cleanest niche pages** [Opinion, from observation; no study exists]:
  - Line 1: a promise or hook in the reader's own language.
  - Line 2: a keyword line (topic + audience).
  - Line 3: proof or cadence ("New reel daily") plus a CTA.
  - 0–1 emoji. A single arrow (↓ or →) reads as premium. Rows of emojis read as "theme page from 2019".
- **Faceless pages need a "who's talking" signal more than face pages do** [Opinion]. Without a face, the bio and the name field are the only identity cues. One plain, confident sentence beats hype.

### Audit of the current bio

> Understand her. Become the man she notices. / Female psychology, dating & confidence for guys / New reel daily. / Follow to decode her ↓

- Good: the hook is strong ("Become the man she notices"), the keywords are present, the cadence is stated, and the CTA is there. 136/150 chars.
- Weak [Opinion]:
  - The " / " separators look like a pasted one-liner. Use real line breaks.
  - "for guys" is casual next to a premium visual brand. "for men" matches searches better ("dating advice for men" is the common query phrase).
  - It is four lines, which pushes the profile buttons down.
  - "Follow to decode her ↓" plays on the name, but the ↓ points at nothing when there's no link or highlights.
  - "Daily" is a promise. Only keep it if the pipeline really ships every day, because a broken promise in the bio looks abandoned.

### Five bio options (all under 150 chars, line breaks intended)

| # | Bio | Chars | Angle |
|---|---|---|---|
| 1 | Why she pulls away, and what to do about it.<br>Female psychology & dating for men<br>New reel daily ↓ | 96 | Pain-point hook. Our strongest pick for a story-led page |
| 2 | Decoding the texts, signals and silences.<br>Dating psychology for men<br>New reel daily. Follow ↓ | 92 | Mirrors the WhatsApp-bubble format |
| 3 | She's not confusing. You just weren't taught.<br>Female psychology for men<br>1 reel a day ↓ | 86 | Reframe hook, warm rather than "alpha". Fits rule 12 (never mock her, never lecture) |
| 4 | Dating psychology for men<br>What her texts, signals & silence really mean<br>New reel daily | 86 | Keyword first, the most search-friendly |
| 5 | Become the man she notices.<br>Dating & female psychology, explained<br>New reel every day ↓ | 86 | Keeps the current hook, cleaner |

[Opinion] Pick **#1 or #3**. Both open on a feeling the viewer recognises, which matches the relatable-story format. #4 is best if search is the priority.

### Recommended name field

**`DecodeHer | Dating Advice for Men`** (33 chars)

- "Dating advice" is a much more common search phrase than "Dating & Psychology". "for men" sets the audience, and the brand stays first.
- Alternative: `DecodeHer | Dating Psychology for Men` (37), if you want to stay closer to the psychology angle.
- [Fact, observed in-app] Instagram allows only about 2 name changes per 14 days, so test deliberately.

---

## 2. Highlights

- [Fact, practitioner sources] Highlights are still used as profile navigation and conversion aids, with simple brand-coloured covers because they show very small. There is no sign Instagram deprioritised them. [[alejandrorioja.com](https://alejandrorioja.com/instagram-story-highlight-how-to-use-it-for-brand-account/), [Vista Social](https://vistasocial.com/insights/instagram-highlights/)]
- Highlights can only contain Stories, and we don't post Stories yet.

**Recommendation: no for now; yes from about week 3–4.** [Opinion] Empty or thin highlights (one story each, or just a cover slide) look more amateur than having none. Start a light Stories habit first: re-share each new reel to Stories, plus one poll or quiz a day on "what would you reply?". Then launch 3 highlights. Never use more than 4–5.

**Names** (short, lowercase or Title Case, one word where possible):

1. **Start Here**: what the page is, plus the 3 best reels.
2. **Texts**: chat-bubble reels and "what would you reply" polls.
3. **First Dates**: date-situation reels.
4. **Signals**: "what her behaviour means" reels.
5. (later) **Free Guide**: once a lead magnet exists.

**Cover style** (fits the Dark Needle look):

- A near-black (#0B0B0F) circle with a thin #B26BFF ring, about 3% of the diameter, inset slightly.
- One cream line icon in the centre at about 40% of the diameter, with consistent stroke weight across the set. Icons: arrow for Start Here, chat bubble for Texts, wine glass for First Dates, eye for Signals.
- No text on the cover (the name sits under it), no gradients, no stock emoji.
- All covers come from the same template, so the row looks like one set. [Opinion]

---

## 3. Premium look

### 3a. Grid, covers and the 3:4 crop

- [Fact] The profile grid now shows tall 3:4 thumbnails. A 9:16 Reel cover (1080×1920) is cropped to the centre 1080×1440, which loses about 240 px at the top and 240 px at the bottom. [[Hopper HQ](https://www.hopperhq.com/blog/instagram-reel-size/), [Planoly](https://planoly.com/blog/guide-to-instagrams-new-vertical-grid)] Our brain/rules/layout.md already uses a safest band of y≈420–1500. Keep it, because the margin also absorbs app-version differences.
- [Fact] Grid reordering went live worldwide in June 2026: long-press → "Reorder grid". Pinned posts (max 3) stay on top. [[MacRumors](https://www.macrumors.com/2026/06/09/instagram-now-lets-users-reorder-posts/), [MobileSyrup](https://mobilesyrup.com/2026/06/09/instagram-reorder-posts-grid/)] This means a bad-looking early post can be moved down later rather than deleted. Deleting hurts nothing, but don't mass-delete, because that looks like a bot cleanup.
- [Fact, conflicting] Sources disagree on whether a Reel cover can be changed after posting ("Adjust preview" vs. not possible). Treat the cover as fixed at publish time. Through the API that means setting the cover image or frame on the create-container call.

**Cover template** [Opinion]:

- **Background:** the hero frame of the reel (the glowing silhouette), darkened about 30% so the text pops. Keep the silhouette head inside the safe band.
- **Title:** 2–4 words, Montserrat Black Italic, cream/white, large (about 120–150 px cap height on 1080 wide), centred in the y 700–1200 zone.
- **Accent:** exactly one word in #B26BFF (for example "She **left** you on read"). The same rule as the in-video captions, so the cover and the video feel like one system.
- **Same position, size and treatment on every cover.** Consistency comes from the template, not from identical images. Vary the silhouette pose and scene so the grid doesn't look copy-pasted.
- **No** emoji, no "PART 1" stickers, no arrows on covers, no "Watch till the end", and no tiny text. It must be readable at about 120 px wide (the grid tile on a phone).

### 3b. Pinned posts (once there are 6+ reels)

1. **The best relatable story reel** (highest watch time). It sells the format in one view.
2. **A "Start here" reel**: 20–30 s, the narrator says what the page decodes and for whom ("Every day, one situation you've lived through, explained"). It works as a trailer and answers "should I follow?".
3. **The most-sent reel** (highest sends per reach). It's social proof, and it's the content that brings non-followers. Rotate this slot as better reels appear.

[Opinion] Until then, pin nothing. Pinning 1 of 1 reel adds nothing.

### 3c. Visual consistency and brand colour

- **Purple stays an accent: under 10% of any frame.** Use it on rim light, one caption word, the avatar ring and the highlight rings. Purple backgrounds or purple gradient text look cheap fast. [Opinion]
- **Fix the palette:** void black #0B0B0F, cream #F2EBDD (match the avatar's cream), white #FFFFFF for captions, purple #B26BFF. Nothing else, so no extra accent colours for "variety".
- **One typeface family:** Montserrat Black Italic for hooks and titles, Montserrat Medium for any secondary text.

### 3d. Premium versus cheap or spammy

| Reads premium | Reads cheap or spammy |
|---|---|
| Restraint: one accent colour, one font, lots of black | Rainbow emojis, 3+ fonts, glow on everything |
| Cover titles are a phrase from the story ("She said 'I'm fine'") | Clickbait covers ("SHE WANTS YOU IF…", "99% of men don't know") |
| A bio with a point of view | A bio full of keywords and hashtags |
| No link, or one real useful link | Linktree with "DM me", "coaching", "affiliate" on day 1 |
| Captions written like a person (hook line, 1–2 lines of context) | A hashtag wall, or 30 hashtags in the first comment (now capped at 5 anyway) |
| Replies to comments in the first hour | Zero replies, or bot-like "🔥🔥 thanks bro" |
| A calm, warm-confident tone (rule 12) | Pick-up-artist or "alpha" vocabulary. It also risks sexually suggestive flags (see §5) |

**What makes a page look automated** [Opinion, plus the owner's own 10-13 feedback]:

- Every reel has an identical structure, cover layout and CTA wording.
- Posts go up at the exact same minute every day.
- The same voice pacing and music bed in every reel.
- Captions follow one template.
- No Stories, no replies, no community presence.

Mitigations: keep the variety ledger (CTA type, hook style, story shape and signature visual rotate), add ±20–40 min jitter to publish times, and add a human layer (comment replies, a Story poll).

---

## 4. Logo and profile picture

**Specs** [Fact]: shown as a circle at about 110×110 px on mobile and 180×180 on desktop. Upload 320×320 minimum; 1080×1080 is safer for high-density screens. Keep the corners empty because of the circular crop. [[FirstPier](https://www.firstpier.com/resources/instagram-profile-picture-size), [postfa.st](https://postfa.st/sizes/instagram/profile)] It also appears at about 32–40 px next to comments and in DMs, and that's where most non-followers see it.

**Small-avatar best practice** [Opinion; common brand-design practice]:

- One shape, filling 60–70% of the circle.
- Very high contrast.
- No thin details or gaps under about 3% of the diameter, because they vanish or look like compression artifacts at 40 px.
- At most one or two colours.
- It should be recognisable as a blurred blob. Test by downscaling to 110 px and 40 px and blurring slightly.

**Verdict on the current cream "dh" on near-black** [Opinion]:

- **Legibility:** cream on near-black gives excellent contrast, and two lowercase letters are a good count. Risk: the stencil cuts. At 40 px those gaps either disappear or turn into noise, and "dh" can read as "oh", "ah" or "d h". Widen the cuts or remove them for the small version.
- **Niche signal:** weak. "dh" means nothing to a stranger until they've read the name. Monograms work for brands people already know. A new faceless page benefits from a symbol that hints at the topic.
- **Brand fit:** the dark background fits, but there's **no purple**. The single brand colour is missing from the one asset that appears everywhere (comments, DMs, Story ring). The cream also isn't used anywhere in the videos. Either bring cream into the cover and caption system, or move the logo to white plus purple.

**Three improvement directions:**

- **A. Keep the monogram, add the rim** (lowest effort, recommended first):
  - Same "dh" without stencil cuts, or with wider cuts.
  - Add a thin #B26BFF ring at about 88% diameter with a subtle outer glow. That echoes the purple rim light on the silhouettes.
  - The ring is what people recognise at 40 px.
- **B. Silhouette symbol** (strongest niche signal):
  - A woman's head in side profile as a glowing white silhouette with a thin purple rim, cropped to the circle. This is literally the video's visual language.
  - Optionally, a small "dh" cut-out or a code-bracket/keyhole shape where the ear would be, for "decode".
  - Reads as "female psychology" instantly.
  - Risk: it can look generic if the silhouette is a stock vector. Draw it from our own silhouette assets.
- **C. A single glyph:**
  - Either a stylised "D" whose counter (inner space) forms a keyhole or an eye, cream on black with a purple inner glow.
  - Or a chat bubble with an eye inside, which ties to the WhatsApp-bubble format.
  - Simpler than B and more meaningful than "dh".

[Opinion] Do **A now** (10-minute change), and test **B** as the long-term mark. Whichever is chosen, reuse the same ring on highlight covers.

---

## 5. Algorithm signals (Reels), as of late 2026

**What Instagram itself has said:**

- **Top three signals: watch time, likes, sends.** Mosseri, January 2025 video series: "The top three signals that matter most for ranking are watch time, likes and sends." Likes weigh slightly more with followers (connected reach), and sends (DM shares) weigh more with non-followers (unconnected reach). Look at average watch time, likes per reach and sends per reach in Insights. [[Social Samosa, 23 Jan 2025](https://www.socialsamosa.com/news-2/instagram-reveals-key-factors-for-boosting-reach-8646916)]
- **Sends per reach.** Mosseri: "One of the most important signals we use in ranking is sends per reach… out of all the people who saw your video or photo, how many of them sent it to a friend in a DM?" [[Mosseri Reel](https://www.instagram.com/reel/C86WDnEuBjB/), via [Search Engine Journal](https://searchenginejournal.com/instagram-algorithm-shift-why-sends-matter-more-than-ever/521389)]
  - → For us: the "Send this to the friend who…" CTA is the single most important line in the reel. Rotate it with save CTAs, but lean on sends.
  - The "3–5× more than likes" figure in blogs is **not** from Instagram. Ignore it.
- **What Reels ranking predicts.** It predicts the likelihood that a viewer reshares, watches through, likes, or opens the audio page. Reels get less distribution if they are "low-resolution or watermarked", muted, have borders, are mostly text, or were already posted on Instagram. [[Instagram Ranking Explained](https://about.instagram.com/blog/announcements/instagram-ranking-explained)]
- **Recommendation eligibility.** Content that is watermarked, blurry or low quality, reposted or aggregated, or longer than 3 minutes is not recommended to non-followers. Sexually explicit or suggestive content is also excluded, and repeated violations make the **whole account** ineligible for a period. Check **Account Status** for this. [[creators.instagram.com](https://creators.instagram.com/blog/instagram-recommendations-eligibility-tips-creators), [Instagram Help: recommendations](https://help.instagram.com/313829416281232)] Engagement bait is also listed as ineligible.
  - → For us: the dating niche sits close to the "suggestive" line. Keep silhouettes non-sexual (clothed, no body focus), keep captions free of sexual phrasing, and avoid "comment YES if…" engagement-bait CTAs. Check Account Status weekly in the first month.
- **Originality.** Instagram favours original creators. Accounts that repost others' content (reported as 10+ times in 30 days) are removed from recommendations, and in 2026 this was extended beyond Reels to photos and carousels. [[TechCrunch, Apr 2024](https://techcrunch.com/2024/04/30/instagram-is-updating-its-ranking-systems-to-surface-more-content-from-smaller-original-creators), [PetaPixel, Apr 2026](https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/)] Our content is original, so this helps us. Never post a clip with another app's watermark (CapCut, Fish, etc.).
- **First 3 seconds and skip rate.** In 2025 Instagram replaced the old view rate metric with **skip rate** in Insights: the share of viewers who scroll away within the first 3 s, shown next to a retention chart. [[Social Samosa](https://www.socialsamosa.com/news-2/instagram-retention-chart-skip-rate-new-performance-metrics-reels-9730992), [Metricool](https://metricool.com/instagram-reel-analytics/)] There is no official "good" benchmark (vendor figures like "under 40%" are unsourced). Use it relatively: compare our reels with each other.
  - → The hook needs to be both on screen and spoken by about 0.5 s. No logo sting or slow fade-in.
- **Original audio.** Instagram counts the audio page opens as a predicted action (source above). Since June 2026 the API reports `media_audio_type` (MUSIC vs ORIGINAL_SOUND) and can attach licensed or original audio at creation. [[Meta changelog](https://developers.facebook.com/docs/instagram-platform/changelog)]
  - [Opinion] Our narrator track is original sound, so name it (for example "DecodeHer – original audio") so the audio page is branded.
  - Keep the music bed quiet under the voice. Avoid uncleared commercial tracks via the API, since muted reels lose distribution.
- **Hashtags versus keywords.** Mosseri says hashtags "don't increase your reach" but help categorise a post. Instagram is rolling out a **5-hashtag maximum** (announced December 2025). [[Social Media Today](https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/)]
  - → Use 3–5 specific hashtags (#datingadvice #datingtipsformen #femalepsychology #relationshipadvice + 1 rotating). Put the real search weight in the caption's first line as a natural keyword sentence ("Dating advice for men: why she goes quiet after the first date").
  - Instagram also says to keep captions even when you have on-screen text. [[Social Media Today on Instagram's Reels guide](https://www.socialmediatoday.com/news/instagram-shares-reels-creation-tips-in-new-guide/831551/)]
- **Posting frequency.** Mosseri says there is no single rule: posting more generally gets more total reach, so pick a pace you can sustain without burnout. [[RouteNote on Mosseri's Reel](https://routenote.com/blog/how-often-you-should-post-on-instagram/)] The common "3–5/week" figure comes from vendors (SocialPilot), not Instagram.
  - [Opinion] For a new account, daily is fine **only if quality and variety hold**. Five strong reels a week beat seven samey ones, because samey reels drag down average watch time and make the page look automated.
- **Trial Reels.** These go only to non-followers first. Results show after about 24 h, and the reel can auto-publish to followers if it hits thresholds within 72 h. [[Lindsey Gamble](https://www.lindseygamble.com/blog/instagram-launches-trial-reels-giving-creators-the-ability-to-share-reels-with-non-followers-before-sharing-with-everyone), [Planoly](https://api.planoly.com/blog/instagram-trial-reels)]
  - Supported in the **Content Publishing API** since 3 December 2025 via the optional `trial_params` on the create-media call. [[Meta changelog](https://developers.facebook.com/docs/instagram-platform/changelog)] Third-party docs list the graduation strategies `MANUAL` and `SS_PERFORMANCE` (auto-graduate on performance). [[Ayrshare docs](https://www.ayrshare.com/apis/post/social-networks/instagram)]
  - **Eligibility:** reported as public professional accounts with about 1,000+ followers, with some reports of access from about 200. Instagram hasn't published an official threshold. **So at 0 followers we almost certainly can't use it yet.**
  - [Opinion] At 0 followers every reel is effectively a trial anyway: nearly all reach is non-follower. Revisit Trial Reels around 1k followers and use them for format experiments, so off-brand tests don't land on the grid.
- **AI content label.**
  - **The requirement:** Meta requires a label on content with "photorealistic video or realistic-sounding audio that has been digitally generated or altered", and may apply penalties if it's missing. AI images don't require a label. [[Instagram Help](https://help.instagram.com/761121959519495)]
  - **Why it applies to us:** our narrator is a synthetic, realistic-sounding voice, so we should label.
  - **Reach:** no reach penalty for a correctly applied label has been established. [[gradually.ai](https://www.gradually.ai/en/instagram-ai-label/), secondary]
  - **Via the API:** pass **`is_ai_generated: true`** when creating the media container (available since 22 June 2026). Per third-party docs it can't be added afterwards through the API. [[Meta changelog](https://developers.facebook.com/docs/instagram-platform/changelog), [Inro glossary](https://www.inro.social/glossary/ai-content-disclosure)] **Update brain/rules/script-and-hooks.md**, which assumes an in-app toggle that never happens when posting through the API.
  - **Context:** Mosseri's year-end memo (31 Dec 2025) says that as AI content floods feeds, "authenticity is becoming infinitely reproducible" and imperfection becomes a signal of what's real. [[Om Malik](https://om.co/2026/01/01/what-is-instagrams-adam-mosseri-really-saying-in-his-year-end-memo/), [afaqs](https://www.afaqs.com/news/mktg/instagram-ceo-warns-the-ai-content-boom-is-eroding-authenticity-10971125)] [Opinion] For us this argues for real human-feeling writing (specific, lived situations) rather than more polish.
- **Scheduling or API posting and reach.** Instagram has said scheduled or third-party-published posts aren't penalised, and the ranking system doesn't look at how a post was published. [[Planoly quoting Mosseri](https://planoly.com/blog/does-scheduling-your-posts-affect-your-post-reach), [Kontentino](https://www.kontentino.com/q-and-a/does-scheduling-instagram-posts-affect-reach/)] The caveat is that these sources sell schedulers, though there's no evidence to the contrary. The real risk with API posting is not reach. It's looking robotic (identical timing and format) and skipping in-app-only features.
- **Small creators.** Instagram adjusted ranking in 2024 to give smaller original creators more distribution, and said it would keep doing so in 2025. [[TechCrunch](https://techcrunch.com/2024/04/30/instagram-is-updating-its-ranking-systems-to-surface-more-content-from-smaller-original-creators), [Social Media Today](https://www.socialmediatoday.com/news/instagram-shares-key-focus-in-2025-ai-messaging/737196/)] 0 followers is not a reach handicap for Reels in itself.

---

## 6. Account setup checklist (new creator account)

**Profile and account type**

- [ ] **Account type: Creator** (not Business). Creator accounts get creator-oriented tools and analytics, and either type qualifies for Google indexing. [Opinion: Creator suits a personality-led media page]
- [ ] **Category: "Digital creator"** or "Education". [Opinion] "Digital creator" is the safe, neutral choice. Avoid "Dating service", which signals an app or service and may draw policy scrutiny.
- [ ] **Display category on profile: off** (it adds clutter). Turn it on only if you pick "Education" and want the authority cue. [Opinion]
- [ ] **Contact options:** add an email (a dedicated brand inbox, not personal) for brand deals, and hide it from the profile until there's demand (a "Contact" button on a 0-follower page looks presumptuous). No phone number. [Opinion]
- [ ] **Name field, bio and avatar** per §1 and §4.
- [ ] **Public account**, and leave search-engine indexing **on** (Settings → Account privacy). [[PPC Land](https://ppc.land/instagram-content-becomes-searchable-on-google-starting-july-10/)]
- [ ] **Account Status** (Settings → Account Status): check weekly for "can be recommended". [[creators.instagram.com](https://creators.instagram.com/blog/instagram-recommendations-eligibility-tips-creators)]
- [ ] **Two-factor authentication on.** API tokens plus a password-only login is the classic way pages get stolen. [Opinion / standard security]
- [ ] **Professional dashboard:** check Insights per reel for skip rate, average watch time, sends and saves. Log them in a sheet weekly so we learn which hook styles work.

**Publishing**

- [ ] Captions for every reel: on-screen text plus a written caption with a natural keyword sentence and 3–5 hashtags.
- [ ] AI label sent through the API (`is_ai_generated=true`) on every reel.
- [ ] Cover set at publish (§3a template).
- [ ] No watermarks from any tool. Export at 1080×1920 with a high bitrate, since low resolution is downranked.
- [ ] Reels under 3 minutes (ours are far under), so they remain recommendable.
- [ ] **Publish-time rhythm:** pick one or two windows when the audience is active (check Insights → "Most active times" after ~100 followers). Until then, use the target audience's evening (19:00–22:00 in their timezone). Add ±20–40 min random jitter. [Opinion]

**Behaviour that prevents limits and "automated" signals** (no official thresholds exist; limits are dynamic and stricter on new accounts [[ChatPlace blog](https://blog.chatplace.io/en/instagram-limits/), secondary])

- [ ] No follow/unfollow, auto-like, auto-comment or auto-DM tools, ever.
- [ ] No engagement pods or bought followers. They poison likes and sends per reach, which are the very ratios that rank us.
- [ ] Log in from the phone app regularly and do normal human things: reply to comments, browse the niche, leave thoughtful comments on bigger dating and psychology creators' posts (5–10 a day, written by hand). Comments on big pages are also the main free way for a faceless page to be discovered. [Opinion]
- [ ] Avoid many accounts on one device or IP, and VPN hopping, especially while the account is new. [Secondary sources, as above]
- [ ] Don't mass-edit captions or mass-delete posts right after posting.
- [ ] Re-share each reel to Stories by hand (the API can't do it, and it's a human signal). This also builds Story material for the future highlights.

**Content and brain-rule updates this research implies**

1. `brain/rules/script-and-hooks.md`, captions:
   - "4–6 hashtags" → "3–5 hashtags (Instagram cap is 5)".
   - "owner switches on the AI label when posting" → "the publish script sends `is_ai_generated=true`".
2. The publish script should set: `is_ai_generated`, cover, caption, and a named original audio track where supported. Add `trial_params` later, once the account is eligible.
3. Keep the variety ledger. It is the main defence against "looks automated".

---

### Source list

- Instagram ranking explained: https://about.instagram.com/blog/announcements/instagram-ranking-explained
- Recommendations eligibility (creators.instagram.com): https://creators.instagram.com/blog/instagram-recommendations-eligibility-tips-creators
- Instagram Help, recommendations: https://help.instagram.com/313829416281232
- Instagram Help, AI labels: https://help.instagram.com/761121959519495
- Meta Instagram Platform changelog (trial_params, is_ai_generated, Audio API): https://developers.facebook.com/docs/instagram-platform/changelog
- Mosseri, sends per reach Reel: https://www.instagram.com/reel/C86WDnEuBjB/ and https://searchenginejournal.com/instagram-algorithm-shift-why-sends-matter-more-than-ever/521389
- Mosseri, top 3 signals (Jan 2025): https://www.socialsamosa.com/news-2/instagram-reveals-key-factors-for-boosting-reach-8646916
- Hashtag cap: https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/
- Skip rate and retention: https://www.socialsamosa.com/news-2/instagram-retention-chart-skip-rate-new-performance-metrics-reels-9730992, https://metricool.com/instagram-reel-analytics/
- Original content and aggregators: https://techcrunch.com/2024/04/30/instagram-is-updating-its-ranking-systems-to-surface-more-content-from-smaller-original-creators, https://petapixel.com/2026/04/30/new-instagram-policies-target-reposted-content/
- Trial Reels: https://www.lindseygamble.com/blog/instagram-launches-trial-reels-giving-creators-the-ability-to-share-reels-with-non-followers-before-sharing-with-everyone, https://www.ayrshare.com/apis/post/social-networks/instagram
- Year-end memo: https://om.co/2026/01/01/what-is-instagrams-adam-mosseri-really-saying-in-his-year-end-memo/
- Grid 3:4 and reordering: https://www.hopperhq.com/blog/instagram-reel-size/, https://planoly.com/blog/guide-to-instagrams-new-vertical-grid, https://www.macrumors.com/2026/06/09/instagram-now-lets-users-reorder-posts/
- Google indexing: https://ppc.land/instagram-content-becomes-searchable-on-google-starting-july-10/
- Bio links: https://searchengineland.com/instagram-now-allows-up-to-5-links-in-bio-395742
- Instagram SEO (name field): https://later.com/blog/instagram-seo/, https://www.inro.social/blog/instagram-seo
- Avatar specs: https://www.firstpier.com/resources/instagram-profile-picture-size
- Posting frequency (Mosseri): https://routenote.com/blog/how-often-you-should-post-on-instagram/
- Scheduling and reach: https://planoly.com/blog/does-scheduling-your-posts-affect-your-post-reach
