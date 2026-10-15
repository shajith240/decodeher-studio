# Caption readability for vertical Reels (1080x1920)

Scope: burned-in captions, 2-4 words at a time, centred near y=1100-1300, over grainy 2D illustration. Confidence is marked: [src] = stated in a source found; [est] = my estimate, not verified. The search found no controlled studies. Most numbers come from vendor blogs.

## 1. Numeric rules

1. **Size.** Body captions at 60-75 px on a 1080-wide frame. Floor about 48 px [src: Clipspeed]. Other sources say 45 px or 55 px minimum. Above about 100 px, captions cover the footage [src: a vendor guide]. For a serif, measure cap height, not font size: aim for cap height of at least 40 px [est].
2. **Safe zones.** Meta publishes these as percentages. Vendor conversions for 1080x1920 are: top ~270 px and bottom ~670 px reserved, centre ~950x980 [src: Hopper HQ]. Another source says keep text 450-480 px above the bottom edge [src: Clipspeed]. Sources disagree on the top margin (150 vs 270 px). Keep captions in the centre band, y 1100-1300, which clears both.
3. **Contrast.** WCAG AA: 4.5:1 for normal text, 3:1 for large text (18 pt / 24 px regular, or 14 pt bold) [src: W3C]. Apply this to the worst-case pixel under the text, not the average.
4. **Backing.** Ranking: opaque or semi-opaque dark box first, outline second, drop shadow third [src: BlitzCut; BBC comment to W3C]. Shadows make the screen busier and fail on light footage [src: BBC comment]. Use a dark box or a local scrim, and an outline on top.
5. **Outline.** About 2 px black stroke around the fill [src: one vendor guide]. Stay at 1-3 px. A heavier stroke clogs thin serifs.
6. **Words and lines.** 2-4 words per caption [owner rule]. Max 2 lines. Keep line length at or below 68% of frame width, about 730 px [src: one summary of BBC rules]. On-screen text blocks at 10 words or fewer [src: a vendor guide].
7. **Duration.** I found no sourced minimum on-screen time. Hold each caption at least as long as it takes to read it aloud at a comfortable pace [est]. Make the caption change on the beat, not sooner.
8. **Weight.** Use bold or semi-bold for captions [src: vendor guides]. Avoid Light (300). Hairlines vanish at small sizes.

## 2. Thin serifs on video

- Cormorant SC: no tested legibility data was found. Cormorant Garamond's designer says its larger counters give more reading comfort. Other guides call it a display face that should stay at 18 pt and up, and say its hairlines disappear at small sizes [src: various guides]. Treat it as display-only unless backed.
- Keep the serif out of all-caps unless the weight is 600 or heavier [est].
- Letter-spacing for all caps: no source found. Start at +0.05 to +0.10 em and test on a phone [est].
- Background: a dark scrim (a 60-80% black band behind the caption block) beats a gradient inside the letters [est]. Avoid busy gradients inside thin strokes.
- Solid fill is more legible than texture. Keep metallic effects to a highlight on the fill edge.

## 3. Metallic gold and purple

- Metallic gold #D4AF37 on white is about 2.1:1, a fail. Black on gold is about 9.99:1 [src: Linearity]. Gold needs a dark ground.
- Pure bright gold (#FFD700) is fine as an accent and fails on light backgrounds [src: Linearity].
- Keep the gradient low contrast, with stops within about 15% lightness of each other. Put one soft highlight on the top edge only [est].
- No source tested a thin dark stroke around gold. The 1-2 px dark outline in rule 5 is the best available fix [est].
- Purple key words: use a lighter purple (around L 55-65) with the same dark box behind it [est]. Purple on near-black is low contrast.

## 4. Font comparison (Google Fonts)

Sources gave few numbers. Cinzel, Marcellus, Italiana, Prata and Gilda Display have no x-height or stroke data from the search. Check them with fontTools (OS/2 sxHeight, sCapHeight) before committing.

| Font | Weight for captions | Readability notes | Fit |
|---|---|---|---|
| Cormorant SC | 700 | Small-caps lowercase; no tested data; hairlines thin | Display only |
| Cormorant Garamond | 700 | Larger counters than Cormorant; weights 300-700; 300 too thin | Good, keeps look |
| Bodoni Moda | 600-700 | Optical-size axis keeps hairlines at small sizes [src: fontalternatives]; weights 100-900 | Good, more robust |
| Cinzel | 600 | Capitals only; ornamental; one source says better for titles [src] | All-caps fallback |
| Playfair Display | 700 | Large x-height [src]; less slim | Readable, less royal |
| Marcellus | 400-600 | Flared serif, clear on screen [src] | Unverified |

## 5. Top recommendations

1. **Cormorant Garamond 700** in place of Cormorant SC. Same royal feel with a sturdier stroke. Use SC only for titles.
2. **Bodoni Moda 600** with the optical size set low for captions. It keeps hairlines at small sizes and is slim and royal.

Keep the dark scrim and 2 px outline either way. Test both on a phone at real size over the grainiest frame before the owner signs off.

## Sources

- https://www.hopperhq.com/blog/instagram-reel-size/
- https://www.clipspeed.ai/blog/instagram-reels-captions.html
- https://www.trymypost.com/blog/instagram-reels-safe-zones-text-placement-2026
- https://www.opus.pro/blog/instagram-reels-caption-subtitle-best-practices
- https://blitzcutai.com/blog/best-caption-size-instagram-reels-2026
- https://blitzcutai.com/blog/caption-background-vs-outline-vs-shadow
- https://blitzcutai.com/blog/best-caption-fonts-reels-2026
- https://lists.w3.org/Archives/Public/public-pfwg-comments/2014OctDec/0003.html
- https://w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
- https://fontalternatives.com/alternatives/bodoni/for/display/
- https://fontalternatives.com/compare/bodoni-moda-vs-playfair-display/
- https://www.linearity.io/academy/colors/metallic-gold/
- https://www.media.io/colors/gold-color.html
- https://madegooddesigns.com/cormorant-alternatives/
- https://fontalternatives.com/fonts/cormorant-garamond/
