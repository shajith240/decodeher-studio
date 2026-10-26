# comment-to-dm ("Comment GUIDE and I'll send it to your DMs")
Status: candidate (researched 2026-10-18). Do not put it on a live reel until the owner has seen the free page, the DM text and one sample reel ending.
Links: [[send-or-save-closing-line]] (running test, do not disturb), [[comment-prompt]], [[keyword-seo]], [[reply-to-comments]], [[profile-conversion]].

## The short answer
- **Path: Meta's own free "Comment to Message" automation in Meta Business Suite (desktop).** No app review, no third-party login, no cost, no limit on contacts. Fallback if it proves too limited: ManyChat Essential (about $14-17 a month, 250 contacts). Building it ourselves in the relay is blocked for now (needs Meta App Review + Business Verification, see 2).
- **What it does for us:** turns viewers into DM conversations, site visits and sales. It is a conversion tool more than a reach tool. Comments are not one of Mosseri's three main Reels signals (watch time, sends per reach, likes per reach), and one-word comments carry little information.
- **Main risk:** on reels that use it, the spoken GUIDE line replaces the SEND/SAVE line, and sends are the bigger reach signal. So it goes on 1 reel in 3, not every reel, and only after the SEND vs SAVE test ends.
- **Lead magnet already exists:** the "Never send these" section of the playbook (12 texts that make things worse, brain/content/products/decode-her-texting-playbook.md). Free page + $9 upsell on the same page.

## 1. Does comment-to-DM help or hurt reach in 2026?
| Claim | Verdict | Evidence |
|---|---|---|
| Instagram demotes "comment a specific word" posts | PARTLY TRUE, then softened | June 2024 Instagram said it won't recommend content that "explicitly asks for engagement", with "comment a specific word, number, or emoji" as the example. Days later it clarified: creators "can still use 3rd party services such as ManyChat", and "earnestly engaging with your audience in the comments and DMs" "is not considered to be engagement bait". The target is posts that try to "hack" recommendations [S7, S8]. |
| Meta's written engagement-bait rule | Facebook-only page | Transparency Center: posts that "explicitly request engagement" are demoted, EXCEPT "specific calls to action" (missing people, fundraising, petitions). It does not mention Instagram [S9]. A real resource delivered on request is closer to a specific call to action than to bait, but that is our reading, not Meta's. |
| Comment-to-DM boosts reach | UNVERIFIED | Only DM-tool vendors claim it ("signals high intent", "5x"), no primary source [S13, S14]. Official ranking inputs we trust: watch time, sends per reach, likes per reach (Mosseri; playbook A2). |
| Comments as a ranking signal | Minor, indirect | Not in Mosseri's top three. A one-word "GUIDE" comment is low-information. Treat any reach gain as a bonus, not the reason. |
How careful creators phrase it (opinion, vendor/creator practice): value first, the ask at the END (never in the hook), name the exact thing they will get ("the 12 texts"), deliver it fast, no "comment so the algorithm pushes this", no follow-gate, no fake scarcity. Do not run it on every post.
Our rule: the reel must stand alone with full value; the GUIDE line is an optional extra, never the payoff withheld.

## 2. How the automation works (technical)
Meta's flow for any tool (ours or a vendor's) [S1, S2, S3, S4]:
1. A comment arrives (webhook field `comments`, or polling `/{media-id}/comments`).
2. **Private Reply**: `POST graph.instagram.com/v25.0/{our-ig-id}/messages` with `recipient.comment_id` + `message.text`. Rules: **one message per comment**, sent **within 7 days** of the comment (Live: only during the broadcast). It lands in the person's Inbox if he follows us, otherwise in **Message requests**.
3. **Follow-ups only if he replies**, and then within **24 hours** of his reply. (A button tap in ManyChat counts as his reply; that is why ManyChat flows open with a button.)
4. Limits: private replies to post/reel comments **750 calls per hour per account**; Send API 100/s; text up to 1000 bytes; a DM can carry a PDF up to 25 MB [S4, S2].
Permissions (Instagram Login, our setup): `instagram_business_basic` + `instagram_business_manage_comments` for private replies; `instagram_business_manage_messages` for DMs/follow-ups [S1, S2]. Account: any Instagram professional account (Business or Creator); a Creator account is fine.

### What our setup already does
- `relay/worker.js` (Cloudflare Worker "decodeher-relay") calls `graph.instagram.com/v25.0` (Instagram API with Instagram Login) with the Instagram user token it stores in its Durable Object (`ig:token`, refreshed weekly). `GET /comments?days=N` polls each posted reel's `/{media-id}/comments`; `POST /comments/reply` posts a PUBLIC reply via `/{comment-id}/replies`. Auth = `RELAY_KEY`.
- `hq/worker.js` (Worker "decodeher-hq") runs `replyToComments` on its tick (about every 15-20 min): pulls `/comments` from the relay, writes a reply with Workers AI (`env.AI`, model `@cf/meta/llama-3.3-70b-instruct-fp8-fast`, override `COMMENT_MODEL`), posts it through the relay. Secrets by name: `RELAY_URL`, `RELAY_KEY`, `TELEGRAM_BOT_TOKEN`, `OWNER_CHAT_ID`, `HQ_KEY`, `TELEGRAM_SECRET`, `GH_TOKEN`. No webhooks, no DMs today.
- `tools/ig_queue.js` only uploads and books reels on the relay.

### Can we build it ourselves? Not yet.
- Our app runs on **Standard Access** (fine for our own account, no review [S5]). But "Standard Access apps can only access data for people who have a role on the app" [S3], so a private reply to a stranger needs **Advanced Access**, which needs **App Review** (screencast, privacy policy) and **Business Verification** [S3, S5]. Comment webhooks also need Advanced Access + Live mode + Business Verification [S6]. Polling would avoid webhooks, but not the messaging review.
- Verdict: weeks of review and business documents for a 30-follower page. Revisit after 1,000 followers or if a paid tool passes $30 a month. (Cheap proof later: one private-reply call to a real commenter; an access error confirms it.)

### Options compared
| Option | Cost | Limits | Verdict |
|---|---|---|---|
| **Meta Business Suite "Comment to Message"** (Inbox > Automations, desktop) | Free | Reported: keyword match may be exact/case-sensitive, up to ~5 keywords, possible ~15 min delay, one message (no button step) [S11, S12, secondary]. Official, no third party. | **Use first.** |
| ManyChat Free | $0 | 25 active contacts a month since March 2026 (was 1,000) [S10, secondary; official page blocked our fetch] | Too small: one decent reel uses it up. |
| ManyChat Essential / Pro | ~$14-17 / ~$29-39 a month (250 / 2,500 contacts) [S10] | Button step, follow-ups, case-insensitive, stats. Meta partner. | Fallback if native is too weak. |
| Other "free" tools (ReplyRush 1,500 DMs, LinkDM 1,000, Elev8or) | $0 | Vendor claims only; gives an unknown company access to our inbox [S14] | Avoid unless the owner trusts one. |
| Our own relay + HQ | $0 | Needs App Review + Business Verification | Later. |

## 3. What to send in the DM
- **Free value first, sales link second, both honest.** A stranger who asked for "the guide" and gets a $9 checkout feels tricked; that is how DM funnels get reported as spam. So the DM gives a real free thing, and the free page carries a calm upsell to the full playbook.
- Free thing: a phone-friendly web page `decodeher.pages.dev/free` (no download, no email wall): "12 texts that quietly kill it, and what to send instead", from the playbook's "Never send these" section, with a "what to send instead" line under each (the playbook already has these moves). Bottom: one box, "The full playbook: 25 situations, exact texts, $9", linking to the existing buy button. Track with `?src=dm`.
- Rules: one DM per comment (Meta's rule anyway); no follow-gate; no "limited time"; say the price plainly; never message anyone who did not comment the keyword; no follow-up chase. Possible minors in the audience: the content is general dating advice, no adult material; never ask for age or personal details.
- If he replies with his situation: we cannot auto-answer DMs (no review). The DM points him back to the comments ("comment her text under any reel and I'll decode it"), where the HQ already answers.

## 4. Reel integration
- **Keyword: GUIDE.** Viewers already know the "comment GUIDE" mechanic (owner's pick, matches the trend), one syllable, the TTS says it cleanly, nobody comments it by accident. Not TEXT: our reels and HQ already invite people to comment her actual text, so TEXT would mix two flows. DECODE is on-brand but two syllables and less self-explaining. Accept variants in the tool: GUIDE, Guide, guide (and "guide pls" if the tool allows "contains").
- **Where it sits:** the closing line, after the last move and the "why". Two short sentences: the specific free thing, then the ask. It replaces the SEND/SAVE line on that reel (never stack two asks). The outro bust still rises during the closing words.
- **On screen:** the normal small white serif caption, with the word GUIDE in caps (the one emphasised word). Keep it on screen at least 2 s before the bust covers the frame. New visual element = owner sees a sample first.
- **The clip under it:** the factory picks a clip per spoken line, and "comment guide" would match random clips. Give the CTA beat its own small shelf: a man's hand on a phone in the dark, a phone lighting a face, a thumb hovering over a reply. Colour, no baked-in text (clippick rule), same grade.
- **Caption:** line 1 stays the SEO phrase ([[keyword-seo]]). Replace the send/save line with the GUIDE line. Keep hashtags as now.
- **Pinned comment:** posted by us, pinned by the owner in the app (the API cannot pin). It also tells non-followers to check Message requests.
- **How often:** 1 reel in 3 (one a day, rotating slots so the slot does not decide the result). The other two keep the SEND/SAVE winner. Start only after the SEND vs SAVE test reads (~10-23; the queue is booked with send/save closings to 10-25, do not recaption those).
- **Zero-risk pilot right away:** a pinned GUIDE comment on the two best past reels (~1,100 reach each, already measured) once the automation and free page are live. That tests delivery without touching the experiment.
- **Measure (per GUIDE reel vs the send/save reels, after 6 GUIDE reels):** keyword comments, DMs sent (Business Suite shows them), `/free?src=dm` visits, Polar sales, follows, shares/1k, watch %. Keep it if it adds sales or follows without dropping shares/1k much; n is small, read it as direction only.

## 5. Drafts (owner approves before use)
Spoken closing lines (complete sentences, calm, [lower voice] like the current closings):
1. "Most guys have already sent one of these twelve texts. Comment guide, and I'll send you the full list for free."
2. "There are eleven more texts like this that quietly kill it. Comment guide, and I'll send them to you."
3. "I put the texts you should never send her in one free guide. Comment guide, and it's yours."

Caption line (replaces the send/save line):
`Want the 12 texts you should never send her? Comment GUIDE and I'll DM you the free list.`

Pinned comment:
`Comment GUIDE and I'll DM you the free list: 12 texts that quietly kill it, and what to send instead. Not following yet? Check your message requests.`

DM, native Business Suite path (one message, so value + link together):
`Here's your free guide: the 12 texts that quietly kill it with her, and what to send instead.
decodeher.pages.dev/free?src=dm
If you want every situation covered (slow replies, "we'll see", hot and cold, 25 in all), the full Texting Playbook is $9 on the same page. The free list works on its own either way.`

DM, ManyChat path (two steps):
- First message (private reply): `Hey, thanks for the comment. Your free guide is ready: 12 texts never to send her. Tap below and I'll send the link.` [button: Send it]
- Link message (after the tap): `Here you go: decodeher.pages.dev/free?src=dm
Read number 4 before your next text. The full playbook (25 situations, exact words) is $9 on the same page if you want it.`

Public reply to a GUIDE comment (HQ, fixed rotating lines, no AI): `Sent. If it's not in your DMs, check message requests.` / `Check your DMs, it's there.` (only once the automation is confirmed working).

## Implementation checklist
### Owner does (needs his hands, about 20 min)
1. Confirm @thedecodeher is a Professional account (Creator is fine) and public.
2. On a laptop, open business.facebook.com (Meta Business Suite) and connect @thedecodeher if it is not there. If it asks for a Facebook Page, make a plain one named "DecodeHer".
3. Inbox > Automations > Create automation > "Comment to message" (or "Custom keywords" on comments), channel Instagram. Keywords: GUIDE, Guide, guide. Paste the DM text Claude gives him. Apply to all reels if offered, else to the chosen reels.
4. In the Instagram app: Settings > Messages and story replies > Message controls > Connected tools > "Allow access to messages" ON (needed by any tool; ManyChat fails silently without it).
5. Test from a second account (comments from our own account never trigger): comment GUIDE, check the DM arrives (look in Requests too), note how long it took.
6. Pin the GUIDE comment on the two best past reels, then on each GUIDE reel (Claude posts the comment; pinning is app-only).
7. Approve: the free page, the DM text, one sample reel ending with the GUIDE card and clip.
8. Only if native fails (no Instagram option, delay too long, exact match misses most comments): sign up for ManyChat Essential and connect Instagram; Claude writes the flow text.

### Claude builds (no live change before owner OK)
1. Free page `decodeher.pages.dev/free`: the 12 texts + "send this instead" lines, same site style, upsell box to the existing buy button, `?src=dm` tracking. Show owner the phone screenshot.
2. HQ `replyToComments`: detect GUIDE comments, skip the AI reply, post one fixed rotating public reply (only after delivery is confirmed); count GUIDE comments per reel in the growth stats.
3. Relay: `POST /comments/new` to post our own top-level comment (`/{media-id}/comments`) so the pinned comment is ready for the owner to pin. (Needs a relay deploy; wait until no queue job runs.)
4. Factory: a `cta: "guide"` field in the batch/reel.json; the plan step gives the CTA beat a clip from a new `library/cta-pool/` shelf (phone-in-hand, colour, no text); captions put GUIDE in caps. Render one sample for the owner.
5. Script writer: `next-batch-plan.md` marks 2 of 6 reels as GUIDE after the send/save verdict; closing lines from section 5, rotated.
6. growth_analyze: compare GUIDE reels vs send/save reels (comments, shares/1k, follows, `/free` visits, Polar sales). Log as experiment `2026-10-2x-comment-guide`.
7. Later (after 1,000 followers or if paid tooling costs > $30/month): our own private replies via the relay; needs App Review + Business Verification for `instagram_business_manage_messages` / `instagram_business_manage_comments` Advanced Access.

## Sources (fetched 2026-10-18)
- [S1] Meta, Instagram Platform: Private Replies (Instagram Login + Facebook Login tables, 7 days, one message, 24 h follow-ups): https://developers.facebook.com/docs/instagram-platform/private-replies
- [S2] Meta, Messaging API (Instagram Login): permissions, 24 h window, message types/sizes, Standard vs Advanced: https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/messaging-api
- [S3] Meta, Instagram Messaging: Private Replies ("Standard Access apps can only access data for people who have a role on the app"; Inbox vs Requests; Advanced Access required): https://developers.facebook.com/documentation/business-messaging/instagram-messaging/features/private-replies
- [S4] Meta, Rate limiting (private replies 750/hour per account; Send API 100/s): https://developers.facebook.com/docs/graph-api/overview/rate-limiting
- [S5] Meta, Instagram App Review (own business = Standard Access, no review): https://developers.facebook.com/docs/instagram-platform/app-review
- [S6] Meta, Instagram webhooks (Live mode, Advanced Access for comments, Business Verification, public account): https://developers.facebook.com/docs/instagram-platform/webhooks
- [S7] Social Media Today, Instagram on CTAs that hurt reach (June 2024): https://www.socialmediatoday.com/news/instagram-says-using-certain-ctas-can-impact-post-reach/717732/
- [S8] Social Media Today, Instagram clarifies single-word CTAs, ManyChat still fine (2024-06-05): https://www.socialmediatoday.com/news/instagram-clarifies-advice-on-single-word-ctas-and-longer-reels/718151/
- [S9] Meta Transparency Center, Engagement bait (Facebook): https://transparency.meta.com/features/approach-to-ranking/content-distribution-guidelines/engagement-bait/
- [S10] ManyChat pricing (third-party, 2026; official page blocked automated fetch, owner should glance at manychat.com/pricing): https://www.featurebase.app/blog/manychat-pricing , https://www.elev8or.io/blog/engage/manychat-pricing
- [S11] CreatorFlow, Instagram built-in automation (2026-07-27, quotes Meta help pages; secondary): https://creatorflow.so/blog/instagram-built-in-automation/
- [S12] ManyChat community, triggers not firing / "Allow access to messages" / own-account comments don't trigger: https://community.manychat.com/general-q-a-43/keyword-automation-not-triggering-at-all-instagram-comments-dm-0-runs-even-on-a-fresh-flow-10781
- [S13] InstantDM blog, comment-to-DM and reach claims (vendor, unverified): https://instantdm.com/blog/why-the-instagram-algorithm-loves-automated-replies-in-2026
- [S14] Elev8or / ReplyRush free DM tool comparisons (vendor): https://www.elev8or.io/engage/best-free-instagram-dm-tools , https://www.replyrush.com/post/free-instagram-dm-automation-tools
- Not found: an official Instagram 2025-2026 statement on keyword-comment CTAs after the 2024 clarification; Meta's own help page for Business Suite "Comment to Message" (only quoted second-hand). Verify the native tool in the app (owner step 3).
