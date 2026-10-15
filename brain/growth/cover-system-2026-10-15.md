> **REJECTED 2026-10-15 by the owner** ("AI slop, anybody can tell it is generated"). Do NOT generate cover images. Current method: tools/make_cover.sh (a frame of our own clip, toned, grain, one serif line). Kept only for the research notes below.

# Reel cover system (2026-10-15)

Why: our cover is the frame at 1.5 s (`thumb_offset` 1500), which often shows one word ("HER…"). It's a weak grid tile and a weak search result. See [[growth/views-diagnosis-2026-10-15]].
Full prompts: `deliverables/covers/prompts.json` (`slug, title, idea, prompt`). No images were generated; the main agent generates them.

## 1. What makes a cover get clicked (research)

| Principle | What we take | Source |
|---|---|---|
| One dominant subject | One large focal subject beats several small images. | Storyblocks; hellothematic |
| Curiosity gap, honestly | Hide the **answer**, never the **topic**. The cover asks a question the reel answers. Ethics test: does the reel pay off what the cover implies? | Descript; overseeros; Lovart |
| A symbol tells the story | Objects or contradictions make people ask "what is this?" (laptop + guitar, knight + phone). | Lovart (storytelling thumbnails) |
| Faces and eye contact | Direct gaze and readable emotion catch the eye. This is practitioner lore, not peer-reviewed, and the % figures are unsourced. | TubeFilter 2014; thumbnailtest; Lovart |
| High contrast | Bright subject on a dark or desaturated ground reads at thumbnail size. | hellothematic; routenote |
| Few words | 3–5 words: "a label, not a caption". Must read at ~120 px wide. | socialk.it; saturaai |
| Grid crop | 9:16 is cropped to the centre 3:4 on the profile (y 240–1680 of 1920). Design to the middle ~60%. | Hopper HQ; Oktopost; socialk.it |
| Consistency | Keep one template (type, position, palette); vary the image. Instagram may not let you change a cover after posting. | socialk.it; Planoly; [[research/profile-premium-2026-10]] |

**Competitors.** Our own breakdowns show Dark Needle uses glowing figures on a dark textured stage with one accent colour ([[research/darkneedle-visual-grammar]]). Zoltium changes to a literal picture of each phrase every ~1.5 s ([[research/zoltium-story-visuals]]).

**What I could not view:**
- Pinterest search pages return an empty shell to the fetcher.
- No public write-up of Zoltium's or Dark Needle's covers exists. Social Blade lists a "Dark needle" channel (118K subs) but shows no thumbnails.
- Instagram grids need a login.

Those points rest on our vault notes, not new viewing.

**Ethics.** We read "manipulative visuals" as strong curiosity: a tense moment, a symbol, a face that holds your gaze. We don't fake screenshots, invent quotes or promise things the reel doesn't deliver, and the woman is never mocked or sexualised. The vault already bans "SHE WANTS YOU IF…" or "99% of men" covers.

## 2. The system (one template, nine images)

**Canvas.**
- Generate at 1024×1536 (2:3).
- Scale it to 1080×1620, then pad 150 px of #050507 above and below to get 1080×1920. The void background makes the seam invisible.
- Upload it as `cover_url`, replacing thumb_offset.

**Zones (final 1080×1920 px).**
- **Title band, y 300–590.** It must be inside the grid crop (≥ 240) and below the Reels UI (~270). In the source this is the empty top 28%.
- **Subject, y ~640–1570,** centred horizontally, with nothing key within 85 px of the sides.
- Keep the bottom (y > 1580) empty, because the grid tile prints the view count bottom-left.
- The logo bust watermark goes small at bottom centre (y ~1500), or is left off. The grid already says whose page it is.

**Title overlay (we add it, never the model).**
- Cormorant SC 600, white, 2 lines max, centred.
- Cap height about 110–130 px; tracking +2%.
- One accent word in #C9A2FF, or #8B5CF6 when it's big.
- A soft black scrim behind the text only if needed.
- Same size and position on every cover.
- Titles are 3–5 words, plain search phrases. They also fit the 3–7-word `titleCard` rule, so the 0–2 s title card and the cover can say the same thing.

**Image style.**
- 2D graphic-novel illustration: clean ink line and flat cel shading with soft gradients. Not photoreal, not 3D. It matches the cartoon clip style.
- Black void, faint violet haze, film grain.
- **One purple rim/key light** (#8B5CF6) with lavender highlights (#C9A2FF). Everything else is black, charcoal and ivory.
- One focal subject. No text, logos or UI writing; phone screens show blank bubble shapes only.

**Cast.**
- **"Him":** one recurring man (late 20s, short dark hair, stubble, charcoal shirt, calm). He is the page's face without being a real face.
- **"Her"** appears only partly or as a portrait, never mocked or sexualised.

**Grid rhythm.**
- Alternate **figure** covers (him, often with eye contact) and **symbol** covers (one object: keys, phone, scissors).
- Never put two of the same type side by side in a row of three. Never use the same title opener twice in a row.
- The same light, palette and title position make the 3×3 grid look like one set. The subjects keep it from looking copy-pasted.

**Shared prompt base.** It is appended to every scene in prompts.json:
> 2D graphic-novel illustration, clean ink linework, flat cel shading with soft gradients, cinematic noir, not photoreal/3D · pure black void #050507, faint violet haze, film grain · one electric purple #8B5CF6 rim light, lavender #C9A2FF highlights, else black/charcoal/ivory · ONE focal subject centred, 30–88 % of height; top 28 % empty void for a title; edges and bottom 10 % clear · no text, letters, numbers, logos, watermarks or readable UI; screens show blank bubbles · adults, fully clothed, nothing sexualised.

## 3. The nine covers (posting order)

The **bold** word in each title is the purple accent. F = figure cover, S = symbol cover.

1. **w2-01-doesn-t-move-me · THE OTHER GUY **TEST** · F**
   - He stays calm with direct eye contact. A faceless "other guy" made of purple smoke looms behind his shoulder, and he doesn't turn.
   - Honest to the reel: she's checking whether you shake. The answer is calm.
2. **w2-03-your-plans-matter · STOP DROPPING YOUR **PLANS** · S**
   - His hand freezes over his car keys. Beside them a phone lights up purple; his friends' glasses are blurred behind.
   - The open loop: does he go?
3. **w2-04-not-a-free-service · WHY SHE **FRIEND-ZONED** YOU · F**
   - He stands inside a glowing glass display case: safe, on show, shut in. This is the reel's "safe box".
4. **w2-10-take-it-offline · SHE STOPPED TEXTING **BACK** · S**
   - Chat bubbles rise on a phone and crumble into purple ash. The cover shows the topic and keeps the reason for the reel.
5. **w2-16-just-ask · SHE'S HOT AND **COLD** · F**
   - Her face is split by light: a warm lavender smile on one half, cold shadowed stillness on the other. The mood is uncertainty, not villainy.
6. **w2-05-you-almost-had-me · SHE CALLED YOU **BORING** · F**
   - Across a candlelit table he leans back with an easy smirk and eye contact. Her hand and wine glass are blurred in the foreground, so the viewer sits in her seat.
7. **w2-17-stay-you · DON'T **CHANGE** FOR HER · S**
   - Open barber scissors are frozen mid-air, with one lock of dark hair falling: the cut that hasn't happened yet.
8. **w2-08-be-someone · WHY SHE'S **BORED** OF YOU · F**
   - He is a hollow purple outline with void inside, repeated outward in fading echoes. It is the reel's "just an echo".
9. **w2-07-not-every-second · STOP TEXTING GOOD **MORNING** · S**
   - A phone sits on a nightstand at dawn: a tall stack of his blank sent bubbles on the right and nothing on the left.

Grid check:
- Rows read F-S-F / S-F-F / S-F-S. Row 2 has two F covers, but one is her portrait and one is him at a table.
- No two neighbours share a subject.
- Title openers rotate between WHY / SHE / STOP / DON'T.

## 4. QA before upload

- Shrink the cover to 120 px wide and check the title is still readable.
- Check the 3:4 centre crop.
- Make sure the model added no letters (it often sneaks text onto phone screens). Regenerate if it did.
- Check that his face and the palette match the earlier covers.
- Check the title says what the reel actually answers.

## Sources

- https://www.storyblocks.com/resources/blog/how-to-make-a-killer-video-thumbnail-for-youtube
- https://hellothematic.com/youtube-thumbnails-playbook/
- https://licensing.routenote.com/blog/?p=8676
- https://saturaai.com/blog/what-makes-a-good-youtube-thumbnail
- https://descript.com/blog/article/the-youtubers-guide-to-the-curiosity-gap-how-to-keep-your-audiences-interest
- https://www.overseeros.com/blog/curiosity-gap-youtube-titles
- https://www.lovart.ai/blog/storytelling-thumbnails-intrigue-not-just-subject
- https://www.tubefilter.com/2014/06/19/youtube-thumbnails-definitive-guide/amp/
- https://thumbnailtest.com/guides/face-in-youtube-thumbnail/
- https://socialk.it/en/blog/instagram-reel-covers-guide
- https://www.hopperhq.com/blog/instagram-reel-size/
- https://www.oktopost.com/blog/instagram-grid-size-guide/
- https://webflow.planoly.com/blog/designing-reel-covers
- https://masterbundles.com/tabitha-emma/instagram-dark-reels-cover-templates/
- https://socialblade.com/youtube/handle/darkneedle-z1h/videos
- https://flowshorts.app/faceless-reels/psychology
