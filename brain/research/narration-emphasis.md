# Narration emphasis for Chatterbox reels

Tags: [tested by others] = reported by users or issue threads; [docs] = vendor documentation or README; [opinion] = reasoned guess, not verified on our voice. Nothing here is verified on our own clone yet. Run an A/B on one 30 s script before adopting.

## 1. Human voice-over craft

- **Operative words.** Find the words that carry the meaning: nouns, adjectives, names, and the contrast word in "not X, but Y". Mark them before recording, then stress only those. [opinion, consistent across journalism VO training sources]
- **Stress levers.** Volume, pitch, rhythm, tempo. Pausing before a word stresses it without raising volume. [docs-level craft consensus]
- **Contrast.** For "she's not BUSY, she's BORED", stress the contrasting pair lightly, and pause before the second half. Heavy stress on everything sounds stilted. [opinion]
- **Pause before the reveal.** Pause just before the key line, then deliver the reveal at normal pace. Long holds sound theatrical; a short beat works. [opinion/craft]
- **Speed.** Speed through setup, slow on the operative words. [opinion]
- **Questions.** Rising intonation on the question, falling on statements. [docs: Rime guide describes "?" as rising intonation, third-party]
- **Restraint.** Documentary-style narration favours understatement over drama; a calm line can land harder than a shouted one. [opinion]

## 2. Writing text so a TTS engine emphasises

- **Commas and full stops.** Short sentences and full stops give clean stress and breath. "Not. One. Date." is a valid pattern but each fragment is short (see section 4 on short-input failure). [docs: ElevenLabs "standard punctuation provides natural speech rhythm"]
- **Ellipses "...".** Add weight and a trailing pause, but can add hesitation. Use max once per paragraph. [docs: ElevenLabs]
- **Em dash / dashes.** Short pauses, less consistent than break tags. [docs: ElevenLabs]
- **Question marks.** Rising intonation. Keep the "?" when the line is a question. [docs, third-party]
- **ALL CAPS on one word.** ElevenLabs states "capitalization increases emphasis". Not documented for Chatterbox. Risk: a caps word may be spelled out letter by letter, especially acronym-like words of 3-4 letters. Use caps only on ordinary words, never on acronyms. [docs for ElevenLabs; Chatterbox untested]
- **Italics / asterisks.** No source found for Chatterbox. Strip them before sending; do not rely on them. [opinion]
- **Line breaks.** Splitting a sentence into separate lines or separate generations is the most reported fix for flat delivery. [tested by others, vendor blogs]
- **Phonetic respelling.** ElevenLabs suggests stress through spelling, e.g. "trapezIi". Chatterbox has no phoneme input (feature request #550 is open). Respelling is the only route. [docs + issue]
- **Repeating words.** No source. [opinion] Avoid unless a line needs weight.
- **SSML.** Chatterbox does not document SSML or break tags. ElevenLabs v3/v4 also dropped SSML breaks. [docs]

## 3. Chatterbox specifically

- **Defaults.** exaggeration 0.5, cfg_weight 0.5 "work well for most prompts across all languages". [docs: README]
- **Expressive/dramatic.** Lower cfg_weight (about 0.3) and raise exaggeration to about 0.7 or higher. [docs: README]
- **Pacing trade-off.** Higher exaggeration tends to speed speech up; lower cfg_weight counters that and slows delivery. [docs: README]
- **Fast reference speaker.** Lowering cfg_weight to about 0.3 improves pacing. [docs: README]
- **Emotion control.** Exaggeration is the only real lever; users praise it for the English model. Issue #61 asks for finer emotion control, unresolved. [tested by others]
- **Multilingual caveat.** Exaggeration has little effect in the multilingual models (issue #355). We use the English model, so the effect should hold. [tested by others]
- **Paralinguistic tags.** [laugh], [cough] are documented for Turbo only. Issue #557 reports most tags parse but have no audible effect. Not useful for us. [docs + tested by others]
- **Length limit.** Generations over about 1000 tokens or 40 s are cut off (issue #181). Keep each generation to one to three sentences. [tested by others]
- **Short inputs.** Very short texts ("Yes.", "Why?") often produce gibberish or hallucinated audio (issue #97). Merge fragments under about 20 characters into the neighbouring sentence. [tested by others]
- **Chunk joins.** Users report pace changes and noise at chunk joins when long text is split. Split at sentence ends, never mid-phrase. [tested by others]
- **Punctuation/caps handling.** Not documented in the README and not covered in any issue. Test before relying on it. [untested]

## 4. Per-line recipe (starting values, all [opinion] until A/B tested)

| Line type | Markup | exaggeration | cfg_weight | Notes |
|---|---|---|---|---|
| Hook question | End with "?", one sentence | 0.6 | 0.4 | Rising end. Keep it its own generation. |
| Punchy short fact | Full stop, short | 0.5 | 0.5 | Default. Do not go below 20 characters; merge. |
| Story setup | Plain, commas | 0.4 | 0.5 | Calm, slightly slower. |
| The twist/reveal | Split into own generation; "..." before it in the previous line | 0.7 | 0.3 | Stress the operative word via a short line; add 300-500 ms silence before it in the edit. |
| Advice line | Plain, one caps word max | 0.5 | 0.5 | Speak it plainly. |
| Motivational close: "You wasted so much time, boy. Now focus on yourself." | Two generations; caps on "BOY" not needed; full stop after "boy." | 0.6 then 0.4 | 0.4 then 0.5 | Silence 400-600 ms between; end falling. |

Per-line settings require separate generations. Stitch in the editor, not in one long generation.

## Markup rules we can apply automatically

1. Split text on sentence endings and keep each generation to one to three sentences under about 200 characters.
2. Merge any fragment under 20 characters into its neighbour before generation.
3. Strip *, _, and markdown before sending.
4. Keep "?" on questions; never end a statement with "?".
5. Allow at most one "..." per paragraph; replace a second with a full stop.
6. Add silence in the edit for pauses before reveals (300-600 ms), not punctuation hacks.
7. Apply the per-line settings table by a line-type tag set by the script, one generation per tagged line.
8. Reject any caps word of 2-4 letters that is an acronym; keep caps for ordinary words only.

## Sources

- https://github.com/resemble-ai/chatterbox (README; exaggeration/cfg guidance fetched)
- https://github.com/resemble-ai/chatterbox/issues/61 (emotion control)
- https://github.com/resemble-ai/chatterbox/issues/355 (multilingual exaggeration)
- https://github.com/resemble-ai/chatterbox/issues/97 (short-input hallucination)
- https://github.com/resemble-ai/chatterbox/issues/181 (length limit and chunking)
- https://github.com/resemble-ai/chatterbox/issues/550 (phoneme input request)
- https://github.com/resemble-ai/chatterbox/issues/557 (Turbo paralinguistic tags)
- https://elevenlabs.io/docs/best-practices/prompting/eleven-v3 (punctuation, caps, pacing; fetched)
- https://elevenlabs.io/docs/best-practices/prompting/normalization (caps, phonetic respelling; fetched)
- https://elevenlabs.io/docs/product/prompting/pauses (break tags, dashes, ellipses; fetched)
- https://docs.rime.ai/docs/punctuation.md (question mark rising intonation; search snippet only)
- https://em.sej.org/sites/default/files/VoicingYourScript101912.pdf (operative words; search snippet only)
- https://www.npr.org/sections/npr-training/2025/09/29/g-s1-90460/how-marking-scripts-can-help-you-sound-more-natural (script marking; search snippet only)
- https://deapi.ai/blog/kokoro-tts-guide-how-to-control-41-voices-with-nothing-but-punctuation (Kokoro ignores caps and tags; search snippet only, third-party)
- Not reachable: runware.ai directing-with-audio-tags (404), capcut.com voiceover guide (451).
