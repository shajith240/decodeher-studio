# Hindi narration: making the voice sound natural (research 2026-10-16)

Scope: Fish Audio S2 family (model header s2.1-pro-free, voice "janam" 2f46...ae74), Hindi script rules, alternative engines, and a recipe to A/B.
Legend: [OFFICIAL] = Fish/vendor docs, [3RD] = third-party/secondary, [UNVERIFIED] = inference or search-snippet only, test before trusting.
Honest limit: web search found NO creator write-ups on Fish + Hindi specifically. Most Hindi advice below is general practice, marked as such.

## 1. Fish Audio S2 / S2.1-pro: what the docs actually say

### Tag syntax (docs disagree with each other, so test)
- [OFFICIAL, HF model card fishaudio/s2-pro] Inline control is `[tag]`, free-form natural language, word-level. "15,000+ unique tags". Examples: `[pause]`, `[short pause]`, `[emphasis]`, `[inhale]`, `[exhale]`, `[sigh]`, `[laughing]`, `[chuckle]`, `[low voice]`, `[whisper]`, `[volume down]`, `[low volume]`, `[excited]`, `[sad]`, `[tsk]`, `[with strong accent]`.
- [OFFICIAL, docs.fish.audio emotions page] S2 = square brackets (`[happy]`); legacy S1 = parentheses (`(happy)`). S1 retires 2026-12-31; S1 calls then get served by s2.1-pro and parenthesis tags are NOT converted.
  Pauses there: `[break]` (short) and `[long-break]` (extended).
- [3RD, Runware guide for fishaudio:s2.1@pro] Paralanguage cues in PARENTHESES: `(break)`, `(long-break)`, `(breath)`, `(laugh)`, `(cough)`, `(sigh)`, `(lip-smacking)`. Bracket tags for mood. Says use `(break)` for timing + tags for mood.
- Net: pause syntax is contradictory across sources: `[pause]` (model card), `[break]`/`[long-break]` (Fish docs), `(break)`/`(long-break)` (Runware). Our current `[pause]` is at least documented. A/B all three on one 3-sentence snippet; keep whichever produces an audible, natural gap.
- Tag behaviour [OFFICIAL/3RD]: tag applies from its position until the next tag; tags reset, they do not blend. Sentence-level emotion tags work best at the START of a sentence; tone markers (`[emphasis]` right before a word) and sound effects can go anywhere. Stack at most 2 compatible tags (docs page says up to 3). Conflicting stacks (whisper + angry/shouting) are unstable. Give each emotion at least one full sentence. Free-form tags may take intensity words ("[very excited]").
- IMPORTANT [OFFICIAL]: the emotion-marker docs list 13 languages: en, zh, ja, de, fr, es, ko, ar, ru, nl, it, pl, pt. Hindi is NOT listed. Model card lists Hindi only under "other supported languages (hi)", outside Tier 1 (ja, en, zh) and Tier 2 (ko, es, pt, ar, ru, fr, de). So tags may be weakly followed or even partly read aloud in Hindi. Likely cause of "robotic": long stacked descriptive tags like `[casual, storytelling, like talking to a close friend]` are out-of-distribution. [UNVERIFIED inference; test by removing them.]

### Punctuation, normalize, sampling
- Punctuation guidance: NOT in official docs (only an ellipsis example). Empirical advice only (see recipe).
- `normalize` [OFFICIAL, docs best-practices]: default True; expands numbers/dates. `hi` is not in the normalization language table, so for Hindi it probably skips expansion (docs imply untabled languages skip it). Write numbers out in words yourself. [3RD, Runware]: set `normalize=false` when using paralanguage/phoneme tags because normalization "can strip or misread" them. For Hindi, normalize=false is therefore the safer test; we pre-expand numbers anyway.
- Sampling [OFFICIAL]: defaults are "well-tuned"; lower temperature = more deterministic; raise `repetition_penalty` above 1.0 to cut repeated sounds. No recommended narration temperature/top_p is published. [UNVERIFIED community habit: narration at temp ~0.6-0.7, top_p ~0.7-0.8 for steadier prosody; our 0.85/0.85 is on the expressive side and can cause rushed/odd phrasing.]
- `speed` 0.5-2.0 via `prosody`. Slowing a TTS output by prosody speed often adds the robotic, stretched feel (our observation, matches general TTS behaviour [UNVERIFIED]). Prefer making the TEXT slower (shorter sentences, breaks) over the speed knob, and keep speed 1.0.
- `language`: docs say leave unset for mixed-language text; set only for regional variants (es-MX, zh-TW). Do not set hi if the script is code-mixed.
- `latency`: use "normal" when stability matters (balanced = ~300 ms first audio, for interactive). `chunk_length` default 200, range 100-300; larger chunks for long text. [OFFICIAL] A longer chunk_length (try 300) keeps more context per chunk and may reduce seams in one long take. [UNVERIFIED effect]
- Reference audio [OFFICIAL]: cloned voices want a clean 10-30 s sample with accurate transcript. A cloned community voice inherits the reference's pacing; if "janam" was cloned from a fast, energetic clip, it will rush regardless of speed. Check the model page for sample style and compare against 1-2 other Hindi male community voices.
- Script script: Devanagari vs Romanized Hinglish: no official Fish guidance and no comparative reports found. Fish's own Hindi voice pages show Devanagari samples [3RD]. Devanagari is the safer default; test one Romanized Hinglish variant only for the English loan-heavy lines [UNVERIFIED].

## 2. How Hindi VO / YouTube narration is written for natural delivery
(Mostly general craft knowledge; search found no authoritative Hindi-VO style guide. Mark everything here [UNVERIFIED] unless noted.)
- Short sentences, one idea each; spoken Hindi averages shorter clauses than written. Plain news-writing guidance agrees: short sentences, everyday words, split complex ideas [3RD, news-script guide]. Target 6-12 words per sentence, hard max ~18.
- Write the way it is SPOKEN. Devanagari carries inherent "a" sounds spoken Hindi drops (कमल = "kamal") [3RD]. TTS reads spelling, so choose spellings that sound right, and avoid rare conjuncts.
- Register: "tum/tu-level" conversational (तुम, यार, देखो, सुनो, पता है?), not "आप" lecture and not शुद्ध/Sanskritised words. Swap: परन्तु->लेकिन/पर, अतः->इसलिए, प्रतीत होता है->लगता है, व्यवहार->बर्ताव, आकर्षण->अट्रैक्शन or खिंचाव, संदेश->मैसेज.
- Conversational markers that cue a human prosody: "देखो,", "सुनो", "अब सोचो", "है ना?", "असल में", "मतलब", "और पता है सबसे अजीब क्या है?". Use sparingly, one per few sentences.
- Rhetorical rhythm: statement -> short beat -> twist. Questions lift intonation; TTS handles "?" better than tags.
- Breathing points: after each sentence, and mid-sentence at a comma before a "लेकिन/पर/और फिर". Mark with "," and "।" plus a pause cue; use "…" sparingly (a long run of "…" can make TTS drawl or sound hesitant [UNVERIFIED]).
- Loanwords (dubbing practice): modern Hindi VO keeps everyday English nouns in English (text, reply, relationship, red flag) pronounced Indian-English style; translating them into Hindi sounds bookish. Written in Devanagari the TTS pronounces them Hindi-accented, which matches natives. Spell them as people say: रिलेशनशिप, इग्नोर, ब्लॉक, मैसेज. Do not mix scripts within a sentence (Latin words mid-Devanagari can switch the model into an English voice/accent). [UNVERIFIED but consistent with Sarvam's note that code-mixing is handled at model level.]
- Numbers: spell out (तीन, 80 प्रतिशत -> अस्सी परसेंट) because normalization for hi is not documented.
- Avoid: stacks of 3+ clauses with "जो/जिसके/कि", passive/formal constructions, English abbreviations, dashes and parentheses (read oddly).

## 3. Alternatives (2025-2026)
### Sarvam AI Bulbul (Indian specialist)
- [OFFICIAL API docs] Models: `bulbul:v3` (stable, default), `bulbul:v2`, `bulbul:v4-flash` (docs recommend v4-flash for new integrations). v3 params: `pace` 0.5-2.0 (default 1.0), `temperature` 0.01-1.0 (default 0.6), `speaker` lowercase (default shubh), sample rate 8k-24k (REST also up to 48k), up to 2500 chars/request, wav/mp3/aac/flac/linear16 (no opus). `pitch` and `loudness` are v2 only.
- Male v3 speakers (names, gender inferred from names, so audition): shubh, aditya, rahul, rohan, amit, dev, ratan, varun, manan, sumit, kabir, aayan, ashutosh, advait, anand, tarun, sunny, mani, gokul, vijay, mohit, rehan, soham. Sarvam's sample page shows Dev as a Hinglish edtech voice.
- [OFFICIAL blog] 35+ voices across 11 Indian languages from professional voice artists; handles Hinglish/mid-sentence switching in-model; 48 kHz output. Self-reported Josh Talks blind test (20k+ votes): ElevenLabs v3 alpha leads on full-band audio quality, Bulbul V3 beats Cartesia Sonic-3 and others, lowest character error rate for code-mixed/Romanized/numerics. Vendor-run benchmark, treat as marketing-adjacent.
- Pricing [OFFICIAL pricing page 2026-10]: pay-as-you-go v3 Rs 30 per 10K chars, v4-flash Rs 20 per 10K chars. Free credits on signup (amount not stated; one source says Rs 100, another 1,000 credits; credits = Rs 1 each, no expiry). A 60 s reel is ~600-900 chars, so ~Rs 2-3 per reel. Commercial-use terms for output: NOT stated on pricing page, check Sarvam ToS before relying on it.
- Weakness: no emotion/audio tags; control is only pace + temperature + punctuation. Fixed professional voices (no cloning without enterprise contact).

### ElevenLabs (v3 / Multilingual v2)
- [3RD] Eleven v3 supports 70+ languages including Hindi and audio tags like `[whispers]`, `[laughs]`; reviewers call Hindi naturalness best-in-class but accent can be slightly non-native for some voices. No Hindi-specific tag evaluation found.
- [OFFICIAL pricing page, 2026-10-16] Commercial license is a Starter-plan feature ("Everything in Free plus Commercial License"), so Free is NOT commercial. Starter $1 first month then ~$6 (promo until Oct 18), 30,000 credits/month. v3 availability by plan unconfirmed. One Indian pricing blog claims commercial rights on Free; contradicts the pricing page, ignore.
- Best fit if we want tags + expressiveness; need a library voice that is a native-sounding Hindi male (audition; check "Hindi" filter in Voice Library).

### Google Chirp 3: HD
- [OFFICIAL pricing via search] $30 per 1M chars, free monthly allowance up to ~1M chars. [UNVERIFIED] Hindi (hi-IN) HD voices exist with named voices (Charon, Puck, etc.), pace control via SSML-lite, supports code-mixed text, no cloning on the standard path. I could not verify Hindi voice list, pace API or Hinglish quality here; audition in the Cloud TTS console before deciding.
- Artificial Analysis has a Chirp 3 HD quality Elo page (English-centric).

### AI4Bharat Indic Parler-TTS (open source)
- [3RD] 11 Indian languages including Hindi; speaker + style via a text DESCRIPTION prompt; license listed as Apache 2.0 but the HF model is gated, confirm terms. No independent benchmark vs commercial engines found; runs on GPU (heavy on our 15 GB RAM laptop, CPU slow). Named Hindi male speakers exist in the model card [UNVERIFIED, check]. Good free fallback, not the first choice for reel-grade polish.

### Verdict on "most natural male Hindi narrator for reels"
No neutral head-to-head exists. Evidence: Sarvam's own blind test puts ElevenLabs v3 alpha first on full-band audio quality and Bulbul V3 first on Indian-specific robustness; reviewers praise ElevenLabs breathing/inflection. Practical ranking to AUDITION (not proven): 1) ElevenLabs v3 with a Hindi male voice, 2) Sarvam Bulbul v3/v4-flash (speakers dev, kabir, rohan, aditya, shubh), 3) Fish with a better-chosen/fixed-config voice, 4) Chirp 3 HD, 5) Indic Parler. Sarvam is the cheapest credible route and built for Hinglish; ElevenLabs is the most expressive.

## 4. Recipe for us

### Text-prep rules (apply to every script, all variants)
1. Sentences 6-12 words, hard cap 18. One idea per sentence. End every sentence with "।", "?" or "!" (not "...").
2. Conversational register (तुम/यार/देखो), zero शुद्ध words (see section 2 swap list).
3. English loanwords stay in Devanagari, spelled as spoken; never mix Latin script in the line.
4. Numbers and symbols written out in Hindi words. No dashes, parentheses, emoji, hashtags.
5. At most ONE short mood tag at the start of the script (and rare `[emphasis]`), short tags only: `[calm]`, `[warm]`, `[low voice]`. Drop long descriptive tags.
6. Pause strategy: do NOT rely on tags for rhythm. Put one sentence per line, and rather than tags, insert the silence in post (below). Keep at most one inline pause cue per 3-4 sentences, for punches.
7. Add a line break between paragraphs (beats); keep a comma before "लेकिन/पर/और फिर".

### Post-processing (our edge; works with any engine)
- Whisper word timestamps -> split at sentence ends -> insert silence: 350-450 ms after normal sentences, 600-800 ms after the hook and before the twist/lesson, 250 ms after commas only if a sentence is >12 words. Use a 10-20 ms crossfade at each join to avoid clicks. Random +/-60 ms jitter on gaps avoids a metronome feel.
- Optional: global tempo trim with atempo 0.97 (not Fish speed) only if still fast; keep it above 0.95 to avoid artefacts. Keep the voice take as one Fish call so timbre stays consistent.

### Fish request variants to A/B (same 4-sentence snippet, 3 runs each, judge blind)
- A "steady" : speed 1.0, temperature 0.6, top_p 0.7, normalize=false, latency=normal, chunk_length 300, no language param, repetition_penalty 1.1, text with NO tags except one leading `[calm]`; pauses by post-processing only.
- B "documented pauses": same as A but add `[pause]` (then repeat once with `[break]`, once with `(break)`) at sentence ends of key beats; temperature 0.65, top_p 0.75.
- C "defaults + shorter text": drop temperature/top_p overrides (use Fish defaults), speed 1.0, normalize=false, text rewritten to the 6-12 word rule with loanword spelling checks, no tags at all.
Expectation [UNVERIFIED]: C or A wins; B tells us which pause syntax Fish honours in Hindi. Also test A with a second Hindi male community voice to separate "voice problem" from "settings problem".

### When to switch engines
- If after variants A/B/C the owner still says "robotic" on 2 of 3 blind samples, or if any listener says it reads "like a foreigner" or hears tags spoken aloud, switch.
- First switch: Sarvam Bulbul (cheap, Hinglish-native). Test v3 and v4-flash, speakers dev/kabir/rohan/shubh, pace 0.95-1.0, temperature 0.6-0.7, same snippets; split script into <2500-char calls (reels fit one call). Confirm output commercial-use terms in Sarvam ToS first.
- If Sarvam sounds flat (no emotion levers): ElevenLabs Starter ($1-6/mo, commercial licence) with v3 and tags like `[softly]`, `[chuckles]`.
- Keep Fish only if we want a cloned/owned voice identity; cloning a very natural Hindi reference (30 s, clean, calm pace) of our own would likely beat a random community voice.

## Sources (accessed 2026-10-16)
- Fish Audio S2 Pro model card: https://huggingface.co/fishaudio/s2-pro  [OFFICIAL]
- Fish Audio emotions/tags guide: https://docs.fish.audio/developer-guide/core-features/emotions  [OFFICIAL]
- Fish Audio TTS best practices: https://docs.fish.audio/features/text-to-speech  [OFFICIAL]
- Runware guide for Fish s2.1 pro emotion and expression: https://runware.ai/docs/models/fish-audio-s2-1-pro/guides/emotion-and-expression  [3RD]
- HackerNoon overview of S2 Pro: https://hackernoon.com/fish-audios-s2-pro-brings-emotion-tags-to-text-to-speech  [3RD]
- Fish Hindi voice pages (marketplace, e.g.): https://fish.audio/m/073044c2b93a4ef0b589c24cf4945396  [3RD]
- Sarvam Bulbul v3 blog: https://sarvam.ai/blogs/bulbul-v3  [OFFICIAL/vendor]
- Sarvam TTS API reference: https://docs.sarvam.ai/api-reference-docs/text-to-speech/convert  [OFFICIAL]
- Sarvam pricing: https://www.sarvam.ai/api-pricing  [OFFICIAL]
- Sarvam TTS product page: https://www.sarvam.ai/text-to-speech  [OFFICIAL]
- ElevenLabs pricing: https://elevenlabs.io/pricing  [OFFICIAL]
- ElevenLabs India pricing guide (conflicting claim): https://www.zoutons.com/news/elevenlabs-pricing-india-may-2026  [3RD]
- ElevenLabs v3 overview: https://tech-now.io/en/blogs/elevenlabs-v3-next-gen-ai-voices-features-use-cases-pricing-2025  [3RD]
- Google Cloud TTS pricing: https://cloud.google.com/text-to-speech/pricing  [OFFICIAL, via search snippet]
- Artificial Analysis Chirp 3 HD: https://artificialanalysis.ai/text-to-speech/models/chirp3-hd  [3RD]
- Indic Parler-TTS overview: https://dev.co/ai/llms/indic-parler-tts  [3RD]; model card to check: https://huggingface.co/ai4bharat/indic-parler-tts
- Hindi script-writing general guidance (weak): https://blog.openl.io/hindi/ and a news-script guide surfaced via search  [3RD]
