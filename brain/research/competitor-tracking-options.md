# Competitor tracking: options and recommendation

Researched 2026-10-13 for @thedecodeher (dating psychology Reels for men). Sources are listed at the end, and each claim is tagged with its source number, e.g. [S1]. Prices change often, so check the live page before paying for anything.

## TL;DR

- **Use the official Business Discovery API through the *Facebook Login* flavour (graph.facebook.com).** Since Meta's Business Discovery update in September 2025, it returns `view_count` for Reels, plus `like_count`, `comments_count`, `caption`, `media_product_type`, `timestamp` and `permalink`, for any public **business or creator** account. It is free and within Meta's rules. Because we only use it on our own account, it runs on Standard Access with no App Review [S1][S2][S4][S6].
- Our current token (Instagram Login, graph.instagram.com, IGAA…) **cannot** do this, which is why we got "nonexisting field". Meta lists caption, `media_product_type`, hashtag search and similar features as Facebook-Login-only, and documents Business Discovery only under Facebook Login [S2][S3][S5].
- **Fallback:** the Apify Instagram Reel Scraper (about $2.30–2.60 per 1,000 reels; the $5/month free credit covers a light weekly run). Use it only for competitors that are *personal* accounts, which Business Discovery cannot see, and for transcripts of winning reels [S7][S8][S9].
- **YouTube Shorts:** the YouTube Data API is free and official, with 10,000 units/day [S12]. **TikTok:** no official route for competitors, because the Research API excludes commercial users and the Display API only covers the authorising user's own videos [S13][S14]. Use Apify's TikTok scrapers if we need TikTok at all.

---

## 1. Official Meta: Business Discovery (Facebook Login flavour)

### What it is
Business Discovery is a field on *our* IG user node. We pass a competitor's username and Meta returns that account's public data. "Available for the Instagram API with Facebook Login." [S1][S2]

### Requirements
| Need | Detail |
|---|---|
| IG account type | @thedecodeher must be a professional (Business or Creator) account. It already is. |
| Facebook Page | **Required.** The IG account must be connected to a Facebook Page, and the token's user must be able to perform tasks on that Page [S5]. |
| Meta app | An app with the **Facebook Login for Business** product. This can be the existing app with the product added, or a new "Business" type app. |
| Permissions | `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`. Add `ads_management` or `ads_read` if the Page role comes through Business Manager [S1]. |
| App Review | **Not required** for "an app only for a business I own or manage". That is Standard Access, which works for people who hold a role on the app [S4]. Business Discovery is called *as our own account*, so Standard Access is enough. Advanced Access and review are only needed to serve other businesses' accounts. |
| Token | Use a long-lived Facebook user token (about 60 days, then refresh). Better: a **System User token** from Meta Business Suite (business portfolio), which does not expire. |
| Targets | Competitors must be **Business or Creator accounts**. Personal accounts and age-gated accounts return nothing [S1][S2]. |

### What it returns for another account
- Profile: `username`, `name`, `biography`, `followers_count`, `follows_count`, `media_count`, `profile_picture_url`, `website`.
- Media (edge `media`, cursor-paged with `before`/`after`, no ready-made `next` URL) [S1]:
  - `id`, `caption`, `media_type`, `media_product_type` (REELS / FEED), `timestamp`, `permalink`, `thumbnail_url`, `media_url` (omitted for reels that use copyrighted audio)
  - `like_count` (omitted if the owner hides likes)
  - `comments_count`
  - **`view_count`**: Reels only. It counts paid and organic views, and for cross-posted reels it can combine IG and FB views [S3]. Not every item has it; the docs' own sample omits it on a non-reel [S2].
- **Not available** through Business Discovery: `saved_count`, `shares_count`, `total_views_count`, and insights such as reach or watch time [S3]. "Plays" is not a field; `view_count` replaces it.
- You cannot `GET /{media-id}` on a competitor's media. Everything has to come through the nested `business_discovery` query [S2].
- Industry confirmation: Tubular Labs restored Reels view counts in September 2025 "tied to Meta's recent update to the Business Discovery API" [S6].

### Request shape
```
GET https://graph.facebook.com/v25.0/{OUR_IG_USER_ID}
  ?fields=business_discovery.username(COMPETITOR){
      username,followers_count,media_count,
      media.limit(50){id,caption,media_product_type,media_type,timestamp,
                      permalink,thumbnail_url,like_count,comments_count,view_count}
    }
  &access_token={FB_USER_OR_SYSTEM_USER_TOKEN}
```
Next page: `media.after(CURSOR).limit(50){...}`, using the cursor from `business_discovery.media.paging.cursors.after`.

### Rate limits
Business Discovery and Hashtag Search are subject to **Platform Rate Limits**: 200 calls per hour × number of app users, on a rolling window [S10]. One call per competitor per run (50 reels) means 30 competitors use 30 calls/day, so we are nowhere near the limit. Watch the `X-App-Usage` header.

### Can Instagram Login tokens ever do it?
**No.** It is not documented for Instagram Login, and the same goes for hashtag search and the `caption` / `media_product_type` fields on others' media [S3][S5]. Our "nonexisting field" error is the expected result. We keep the IGAA token for publishing and our own insights, and add a separate Facebook-Login token only for competitor reads.

---

## 2. Scraping APIs

### Apify (best of the scrapers)
| Actor | Fields | Price |
|---|---|---|
| `apify/instagram-reel-scraper` [S7] | `videoPlayCount`, `videoViewCount`, `likesCount`, `commentsCount`, `caption`, `hashtags`, `mentions`, `timestamp`, `url`, `videoDuration`, `musicInfo`, `productType`, `paidPartnership`, `latestComments` (10). Shares on paid plans. **Optional transcript add-on** (per audio minute). | "from $1.00/1k". README: $2.60/1k on Free, $2.30/1k on Starter |
| `apify/instagram-profile-scraper` [S8] | `followersCount` + `latestPosts` (only ~12, with `videoViewCount` on videos) | from $1.60/1k profiles. $2.60 Free / $2.30 Starter |
| `apify/instagram-hashtag-scraper` | posts and reels for a hashtag, which helps discover new competitors | similar per-result pricing |
| Community actors (hpix, benthepythondev, unseenuser…) [S11] | play counts, likes, captions | $1.70–5.00/1k, or $20/mo rental. Few ratings, so less trustworthy |

- Inputs on the reel scraper: `username[]`, `resultsLimit`, `onlyPostsNewerThan` ("7 days" works), `skipPinnedPosts`, `skipTrialReels` [S7].
- Apify plans: Free gives $5 of usage/month and blocks when that runs out. Starter is $19/mo with $19 of usage [S9].
- Reliability: the official actor shows "100% runs succeeded" with about 18k monthly users [S7]. Instagram changes still break scrapers from time to time, typically fixed within days. Expect occasional empty runs and build retries.
- It also sees **personal accounts** and gives **plays and views**, which Meta does not. Apify's `videoPlayCount` is roughly the public "views" number on the grid.

### RapidAPI Instagram APIs
Many unofficial providers sell request-based plans. For example, "Easy Instagram Service" offers 5k requests/mo free, then $20/mo for 14k, and "Instagram Statistics API" starts at $75/mo for 10k [S15]. Quality and lifespan vary a lot. Providers disappear or change schemas without warning, and one request is not one reel. **Not recommended** over Apify, which has a stable maintained actor, per-result pricing and Node SDK webhooks.

### ToS and risk
- Instagram's Terms forbid collecting information "in an automated way without our express permission" [S16]. Scraping is a ToS breach. Any risk sits with the scraping vendor and its proxies, not our IG account, *as long as we never give it our login or cookies*.
- *Meta v. Bright Data* (N.D. Cal., Jan 2024): logged-out scraping of public data did not breach Meta's terms, and Meta later dropped the case [S17][S18]. That lowers but does not remove legal risk. Use only **no-login** actors.
- Never use "login required" actors with our account session, and never use our IGAA token in a scraper.
- Keep data for internal analysis only. Do not republish competitors' videos or captions; this matches our licensing note in memory.

---

## 3. Cross-platform

### YouTube Shorts: YouTube Data API v3 (free, official)
- Default quota is 10,000 units/day. `channels.list`, `playlistItems.list` and `videos.list` cost 1 unit each. The current quota page lists `search.list` with its own small daily bucket [S12]. Avoid search: use the uploads playlist.
- Flow: `channels.list?part=contentDetails&forHandle=@x` → `uploads` playlist ID → `playlistItems.list` (50/page) → `videos.list?part=statistics,snippet,contentDetails&id=…` (50 IDs/call), which returns `viewCount`, `likeCount`, `commentCount`, title, description, duration. Treat duration ≤ 180 s as a Short.
- 30 channels daily costs about 100 units. Only an API key is needed. Clean and fully allowed.

### TikTok
- **Research API**: free, but limited to academic and non-profit researchers. TikTok's FAQ says commercial users and creators are **not eligible** [S13][S14].
- **Display API** (`video.list`) returns only the *authorising user's own* videos [S14]. It is useless for competitors.
- Realistic options: Apify TikTok scrapers (clockworks `tiktok-scraper` / `tiktok-profile-scraper`, similar per-1k pricing, with `playCount`, `diggCount`, `commentCount`, `shareCount`, `text`), or manual checks. Same ToS caveats as Instagram.

---

## 4. Free and manual fallbacks
1. **Weekly manual sweep (15 min):** open each competitor's Reels tab, note any reel whose view number is well above its neighbours, and paste the link into `brain/research/competitor-feed/manual-<date>.md`. Free, zero risk, doesn't scale.
2. **Instagram app "Saved" collection** called "Competitor winners", reviewed weekly.
3. **Meta Ad Library** (free, official) shows competitors' running ads, which hints at which hooks they pay to push.
4. **Local `watch` skill (yt-dlp + transcript)** on a single winner reel for a hook breakdown. Use it only for analysis and keep no copies.
5. **Business Discovery itself is free**, so the recommended option already *is* the free one.

---

## 5. Comparison

| | Business Discovery (FB Login) | Apify reel scraper | RapidAPI | Manual |
|---|---|---|---|---|
| Cost | $0 | ~$1–6/mo at our scale (free $5 credit covers light use) | $0–75/mo, unpredictable | $0 + time |
| Reel views | `view_count` ✅ | `videoPlayCount`/`videoViewCount` ✅ | varies | eyeball |
| Caption | ✅ | ✅ (+ transcript add-on) | varies | ✅ |
| Shares/saves | ❌ | shares on paid plan | varies | ❌ |
| Personal accounts | ❌ | ✅ | ✅ | ✅ |
| Reliability | High (official, versioned) | Good, with occasional breakage | Low to medium | Human |
| ToS risk | None | Vendor-side; logged-out only | Vendor-side | None |
| Setup effort | Medium (Page link + FB Login app + token) | Low (account + token) | Low | None |

---

## 6. Recommendation: one architecture

**Primary: Business Discovery via Facebook Login, run by a Cloudflare Worker cron. Results land in the vault through a local Node sync script.** Apify is an optional plug-in for the few competitors that are personal accounts, and for transcripts of winners. YouTube is added through the Data API only if a competitor posts Shorts.

### What runs where
```
Cloudflare Worker (cron: daily 06:00 UTC)
  for each handle in COMPETITORS (KV/D1 config):
     1 Graph call → last 50 media (reels only kept)
     upsert snapshot rows into D1: (media_id, handle, taken_at, views, likes, comments, followers)
  compute ranking for reels aged 3–14 days → store "winners" JSON in KV (key: winners:<date>)

Local Linux (Node, systemd timer weekly Mon 07:00, or `npm run competitor-sync` on demand)
  GET Worker /winners?since=<last sync>  (shared-secret header)
  write brain/research/competitor-feed/<YYYY-MM-DD>.md
  update brain/research/competitor-feed/whats-working.md
```
- **Why a Worker for fetching:** it runs even when the laptop is off, so we keep a daily *time series* of each reel's views, which is needed to judge velocity. The Worker cannot write to the local vault, so a local sync step writes the Markdown.
- **Why daily fetch, weekly write-up:** daily snapshots cost nothing. A weekly feed page is what a human or the planner will actually read.
- Token: a System User token (non-expiring) stored as a Worker secret (`FB_TOKEN`), with `IG_USER_ID` as a var. If we use a 60-day user token instead, refresh it every 50 days, and the Worker should alert when it is within 7 days of expiry or on an `OAuthException`.

### Ranking rules
- Only `media_product_type === "REELS"`.
- Baseline is the **median `view_count` of that account's last 30 reels older than 3 days**. A median ignores pinned mega-hits.
- A reel is a **winner** when it is ≥ 3 days old and `views ≥ 3 × median`. Also flag a **rising** reel when it is under 3 days old and already ≥ 1.5 × median.
- Secondary scores: `engagement = (likes + comments) / views`, and `comments/likes` (a high ratio means debate or controversy, which is useful for hook style).
- Cross-account comparison uses the multiple of the account's own median, never raw views, so a 20k-follower page's 3× hit counts as much as a 2M page's.

### What gets stored
- **D1 `snapshots`** (Worker): one row per reel per day. **D1 `reels`**: static fields (caption, permalink, timestamp, handle).
- **Vault** (Markdown, human-readable, no video files):
  - `brain/research/competitor-feed/<date>.md`: one block per winner with handle, permalink, posted date, views, × median, likes and comments, caption (first 300 chars), and empty fields to fill in: **Hook** (first line or on-screen text), **Format** (story / list / POV / green-screen / text-only…), **Topic**, **CTA**, **Why it worked**. Claude or the owner fills these by reading the caption and, optionally, watching the reel.
  - `brain/research/competitor-feed/whats-working.md`: a running page with a table of pattern → count of winners in the last 8 weeks → example links. Patterns are tagged with `#hook/…`, `#format/…`, `#topic/…`, `#cta/…`. The sync script only *appends* new winners to a "To tag" list. Tag counts are updated when winners are tagged, so the page stays factual.

### How the reel planner uses it
1. Before planning a week, read `whats-working.md` and the latest two feed files. This fits our existing brain rule of reading the vault before reel work.
2. Pick 2 of the top-trending **topics** and 1 proven **format**, then write the hooks in *our* voice. Never copy a caption; one rule of house style is "accurate info first", so fact-check the claim.
3. Record in the reel's brief which pattern it borrows (e.g. `borrowed: #hook/you-did-this-wrong`). After our reel's own insights come in (IGAA token), compare our result per pattern. Patterns that work for competitors but not for us get marked "not for us".
4. Every reel still ends with the spoken CTA including "follow for more" (CTA rule). Competitor CTAs only inform the *first* half of the CTA.

### Cost
- Business Discovery: **$0**. Cloudflare Workers free plan (cron triggers + D1 free tier) is enough: **$0**.
- Optional Apify for 3–5 personal-account competitors weekly, about 150–300 reels/month at $2.60/1k ≈ **$0.40–0.80/mo**, inside the $5 free credit.
- Optional Apify transcripts for winners only: a few cents/month.

### What the owner must do
1. **Link @thedecodeher to a Facebook Page.** Create a simple Page and connect it in IG settings → Accounts Center.
2. In the Meta developer dashboard, **add "Facebook Login for Business"** to our app (or create a Business-type app), with permissions `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement`.
3. Generate a token: ideally create a **System User** in Meta Business Suite, assign the app plus Page/IG assets, and generate a non-expiring token with those scopes. Then put it in the Worker as a secret.
4. Give us the **competitor list** (handles), and check each one is a Business or Creator account. Any personal accounts go in the Apify list instead (which would need an Apify account + API token).
5. (Optional) Get a YouTube Data API key in Google Cloud Console if competitors post Shorts.

---

## 7. Code sketch: fetch and rank (Node 18+ / Worker-compatible `fetch`)

```js
// competitor-rank.mjs — fetch competitors via Business Discovery and rank reels.
const GRAPH = 'https://graph.facebook.com/v25.0';
const { IG_USER_ID, FB_TOKEN } = process.env;           // FB-Login token, NOT the IGAA token
const COMPETITORS = ['competitor_one', 'competitor_two']; // business/creator accounts only

const MEDIA_FIELDS = 'id,caption,media_product_type,timestamp,permalink,like_count,comments_count,view_count';

async function fetchAccount(username, pages = 1) {
  const reels = []; let after = null, profile = null;
  for (let i = 0; i < pages; i++) {
    const media = `media${after ? `.after(${after})` : ''}.limit(50){${MEDIA_FIELDS}}`;
    const fields = `business_discovery.username(${username}){username,followers_count,${media}}`;
    const url = `${GRAPH}/${IG_USER_ID}?fields=${encodeURIComponent(fields)}&access_token=${FB_TOKEN}`;
    const res = await fetch(url);
    const json = await res.json();
    if (json.error) throw new Error(`${username}: ${json.error.message}`);
    const bd = json.business_discovery;
    profile ??= { username: bd.username, followers: bd.followers_count };
    reels.push(...(bd.media?.data ?? []).filter(m => m.media_product_type === 'REELS'));
    after = bd.media?.paging?.cursors?.after;
    if (!after) break;
  }
  return { profile, reels };
}

const median = a => { const s = [...a].sort((x, y) => x - y); const m = s.length >> 1;
  return s.length ? (s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2) : 0; };
const ageDays = ts => (Date.now() - Date.parse(ts)) / 864e5;

function rank({ profile, reels }, { multiple = 3, minAge = 3 } = {}) {
  const mature = reels.filter(r => r.view_count != null && ageDays(r.timestamp) >= minAge).slice(0, 30);
  const base = median(mature.map(r => r.view_count));
  return reels
    .filter(r => r.view_count != null && base > 0)
    .map(r => ({
      handle: profile.username, url: r.permalink, posted: r.timestamp.slice(0, 10),
      views: r.view_count, likes: r.like_count ?? null, comments: r.comments_count,
      x: +(r.view_count / base).toFixed(2), age: +ageDays(r.timestamp).toFixed(1),
      hookLine: (r.caption ?? '').split('\n')[0].slice(0, 140),
    }))
    .filter(r => (r.age >= minAge && r.x >= multiple) || (r.age < minAge && r.x >= 1.5))
    .map(r => ({ ...r, status: r.age < minAge ? 'rising' : 'winner', baseline: base }))
    .sort((a, b) => b.x - a.x);
}

const all = [];
for (const u of COMPETITORS) {
  try { all.push(...rank(await fetchAccount(u, 1))); }
  catch (e) { console.error(e.message); }  // e.g. personal account → route to Apify list
}
all.sort((a, b) => b.x - a.x);
console.log(JSON.stringify(all, null, 2));  // next step: render to brain/research/competitor-feed/<date>.md
```

Apify fallback, the same ranking fed by `apify/instagram-reel-scraper` (map `videoPlayCount ?? videoViewCount` → `view_count`, `url` → `permalink`):
```js
const run = await fetch(`https://api.apify.com/v2/acts/apify~instagram-reel-scraper/run-sync-get-dataset-items?token=${process.env.APIFY_TOKEN}`, {
  method: 'POST', headers: { 'content-type': 'application/json' },
  body: JSON.stringify({ username: ['personal_acct'], resultsLimit: 30, skipPinnedPosts: true }),
}).then(r => r.json());
```

---

## Sources
- [S1] Meta, IG User Business Discovery reference: https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/business_discovery
- [S2] Meta, Business Discovery guide (v25.0 samples incl. `view_count`): https://developers.facebook.com/documentation/instagram-platform/instagram-api-with-facebook-login/business-discovery.md
- [S3] Meta, IG Media reference (field availability by login type; `view_count` Business-Discovery-only; shares/saves not via BD): https://developers.facebook.com/docs/instagram-platform/reference/instagram-media
- [S4] Meta, App Review for Instagram API (Standard Access, no review for own business): https://developers.facebook.com/docs/instagram-platform/app-review
- [S5] Meta, Instagram Platform overview (Instagram Login vs Facebook Login feature table; Page requirement): https://developers.facebook.com/documentation/instagram-platform/overview.md
- [S6] PPC Land, Tubular Labs restores Reels view data via Business Discovery update (Sep 2025): https://ppc.land/tubular-labs-restores-instagram-reels-view-data-through-meta-api-update/ ; Adweek: https://www.adweek.com/adweek-wire/tubular-labs-announces-the-return-of-instagram-reels-view-counts/
- [S7] Apify Instagram Reel Scraper: https://apify.com/apify/instagram-reel-scraper
- [S8] Apify Instagram Profile Scraper: https://apify.com/apify/instagram-profile-scraper
- [S9] Apify pricing: https://apify.com/pricing
- [S10] Meta Graph API rate limiting (Instagram BUC 4800×impressions; Business Discovery under Platform Rate Limits, 200 × users/hour): https://developers.facebook.com/docs/graph-api/overview/rate-limiting
- [S11] Community Apify actors: https://apify.com/benthepythondev/instagram-reels-scraper , https://apify.com/unseenuser/IG-posts , https://apify.com/agentx/instagram-reel-scraper
- [S12] YouTube Data API quota costs: https://developers.google.com/youtube/v3/determine_quota_cost
- [S13] TikTok Research API FAQ: https://developers.tiktok.com/docs/en/research-api-faq
- [S14] TikTok API limits overview (Research eligibility, Display API scope): https://www.xpoz.ai/blog/guides/tiktok-research-api-limits-access-and-alternatives/ ; https://www.blotato.com/blog/tiktok-api-pricing
- [S15] RapidAPI example pricing: https://rapidapi.com/de/ariefsam/api/easy-instagram-service/pricing , https://rapidapi.com/ko/artemlipko/api/instagram-statistics-api/pricing
- [S16] Instagram Terms of Use: https://help.instagram.com/581066165581870
- [S17] Farella Braun + Martel, Meta v. Bright Data analysis: https://www.fbm.com/post/102kqw7/
- [S18] MediaPost, Meta abandons Bright Data suit: https://www.mediapost.com/publications/article/393996/meta-abandons-lawsuit-against-bright-data-over-scr.html

### Unverified / to confirm on setup
- Business Discovery running fine on Standard Access for the app owner's own account is an inference from [S4] plus common practice. Confirm with the first real call.
- Whether `view_count` appears on *every* competitor reel. The docs' sample shows it can be missing, so the code treats missing as "skip".
- The YouTube `search.list` quota line in [S12] differs from the long-standing 100 units/call. We don't use search, so this doesn't matter.
