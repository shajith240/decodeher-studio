# Sound design v2: music bed + SFX spec (10-14)

Evidence note: web evidence for this topic is thin and mostly vendor blogs. Nobody publishes numbers for dark-psychology Reels. Items marked (measured) come from our own Zoltium stem analysis ([[zoltium-sound]]). Items marked (practice) are common editor/engineer practice from the sources. Items marked (proposal) are my synthesis; test by ear on a phone. Complements [[sound-design-psychology]].

## 1. Why our current mix feels cheap

Diagnosed from `tools/reel_mix.py` and `brain/rules/audio.md`:

1. **SFX on every visual cue.** The mixer places a sound on every cue (whoosh per scene change). Clips change every ~1.5 s, so that is about 6 whooshes per 10 s plus pops/ticks. Our own density rule says 3-6 SFX per 10 s total. Sources agree: a whoosh on every cut is the top "amateur" tell (Sonilo, Beverly Boy, filmeditingpro).
2. **Same two files forever.** `pick()` alternates between the top 2 ranked files and peak-normalises each, so every whoosh has equal weight and sounds identical. No pitch or level variation, no match to the length of the move.
3. **Music is a looped file, not an arrangement.** `np.concatenate([m]*reps)` loops a short track. The "intro drone" is the same track low-passed at 380 Hz. Drops are 0.45 s hard gates in the bed. That is a mechanical effect, not a composed energy curve, and loop seams will sound "chopped".
4. **The bed is never carved for the voice.** There is no EQ on music or SFX around 100-250 Hz or 1-4 kHz. Ducking is only 3 dB (practice is 6-12 dB). Bed hits are therefore only separated by level, which causes masking.
5. **Master stage.** Everything is summed, normalised to -14 LUFS, then hard-clipped at -1 dBFS. That is sample-peak clipping, not true-peak limiting. Loud riser/impact/sub stacks then crush the voice and distort on phone speakers.
6. **Layers at inaudible or fighting levels.** Drone -26 dB and room tone -40 dB mean nothing, while whoosh -15 / pop -17 / swipe -18 / impact -14 all sit near the same level, so there is no hierarchy.
7. **Contradictory rules.** `audio.md` still says "calm, warm, no drones, no suspense, no drums" for music while the mixer builds a beat and a drone. Music choice is therefore unspecified, so the mix is random per track.
8. **Reveal stack is too big.** Riser + reverse swell + silence + impact + sub on every drop, plus a braam on punches. Sources: one big event per ~10 s; contrast needs space.

## 2. MUSIC BED SPEC

**Genres that fit (rank order):**
1. Dark ambient / cinematic tension: low drone, sparse sub pulse, no melody lead. Narration beds are typically 55-90 BPM or beatless (practice, vendor listings).
2. Slowed dark trap / half-time phonk instrumental, with the lead and cowbell removed or very quiet. Classic phonk is 130-140 BPM written half-time (feels 65-70) (Violet Recording). Zoltium z2 runs a ~120 BPM trap groove (measured).
3. Pulse-driven minimal electronic (dark synth pulse, heartbeat-like sub kick), 70-120 BPM.

**Ban:** vocals or vocal chops or choirs with words; rock/metal/guitar bands; EDM build-and-drop; happy, major-key, upbeat, "corporate inspirational"; lo-fi chill hop with a jazzy chord loop (rejected 10-13); busy piano melodies; anything with a lead melody in 1-4 kHz; trailer-epic orchestral with brass (too big, reads as a movie ad); cartoon or ironic sounds; very bright hi-hat-heavy drill (competes with consonants).

**BPM:** 60-90 (ambient/half-time feel) or 110-125 (Zoltium range). Avoid 130-160 straight-time. Accept tracks with no tempo (drone) as long as sub pulse exists.

**Key/mode:** minor (natural minor / Phrygian, ideally one or two chords or a pedal tone). Dissonance is allowed only in the pad; the bass note should be stable (F, G, A, D, E). Avoid key changes.

**Instrumentation:** sub/808 or low synth bass (30-100 Hz), dark pad or drone (150-600 Hz, low-passed), sparse percussion (kick + soft snare or rim, hats filtered), occasional reverse-cymbal or texture; no melodic lead.

**Energy curve (proposal, matching our measured Zoltium structure):**
- 0-3 s hook: drone + very low pulse only, filtered (-24 to -22 LUFS short-term), starts before the first word.
- 3-12 s setup: add sub pulse/kick at low level; keep dynamics flat.
- Turn (about 40-50 % into the reel): one riser -> 0.3-0.5 s near-silence -> impact. Here the full beat enters (+3 to +4 dB).
- Payoff: the beat stays at full level; tension stays unresolved.
- CTA: the bed thins to pad + sub; one soft impact into the outro logo. Never end on a braam (threat, not invite).
- Not more than 2 drop-outs per 40 s reel. Silence only before a reveal; dropping music at random reads as a bug.

**Level under voice (proposal + practice):** bed sits 12-16 dB under voice in short-term LUFS while talking (voice -17 LUFS, bed about -30 to -33 LUFS during speech), 6-8 dB under it during pauses. Sources give: music -20 LUFS or quieter vs voice -12 LUFS (voxbooster), duck 6-12 dB (CapCut), 7-14 dB (Vegas forum). Zoltium (measured): voice only +3.3 / -4.4 dB over bed, but their bed is mostly carved; do not copy that ratio without the carve in section 5. Start with ~10 dB and listen.

**Cutting the track to the reel:**
- Choose a section that already starts with a drone/no kick; start at a bar boundary (`music_offset`), never loop. Need track length >= reel length + 5 s, else crossfade at a bar line (2 s equal-power) at a quiet point.
- The riser/impact is placed on a beat or bar boundary where possible (quantise the drop to the nearest beat <= 0.15 s from the line start).
- End: 1.2 s fade is too short; use 2.5 s tail that lands on the logo outro hit, with reverb tail ringing 1-2 s under the logo.

## 3. Track selection checklist (automatable)

| Check | Pass | Tool |
|---|---|---|
| Tempo | 60-90 or 110-125 BPM, or no stable pulse (drone) | librosa beat_track |
| Vocals | vocal-stem energy < -35 dB re mix (Demucs) and no lyric detected (Whisper returns no words) | Demucs + whisper |
| Mode | minor (key detect: Krumhansl profile or chroma vs minor template) | librosa chroma |
| Low-mid space | after a +0 dB scale, energy 1-4 kHz is 10+ dB below energy 40-250 Hz; energy 200-500 Hz not above 40-150 Hz | STFT band ratio |
| Spectral centroid | < 1.5 kHz (median) | librosa |
| Dynamic range | LRA 2-6 LU, crest factor not > 14 dB, no sudden +6 dB jumps in 1 s frames | pyloudnorm |
| Intro | first 3 s has no kick transient above -20 dB re the track peak | onset strength |
| Duration | >= reel length + 5 s | ffprobe |
| Loop safety | no clipping (true peak <= -1) | pyloudnorm / ffmpeg ebur128 |
| Hi-hat density | onsets in 5-12 kHz < 8 per s | librosa |
| Licence | CC0/royalty-free logged in assets/music | manual |

Automatic score only shortlists. Rule in `audio.md` stands: the owner picks the final bed by ear on a phone.

## 4. SFX SPEC

**Types and jobs (one family per reel):**
- Soft whoosh (air, 0.3-0.8 s): section/scene-group changes. NOT every cut.
- Heavy designed whoosh: act changes, max 1-2 per reel.
- Reverse swell (0.5-2 s) into a cut or impact.
- Riser (1-3 s) before the reveal only.
- Impact + sub drop (+ transient click for phones): the reveal word, once per reel or twice at most.
- Glitch (short): corrupted text / "the trick is" / manipulation line.
- UI tick / paper foley: quiet, for card reveals or numbers.
- Phone foley, heartbeat, clock: only when the line is about it.
- Braam: once per reel at most.

**Density (practice + our rule):** 3-6 discrete SFX per 10 s, max 1 big event per 10 s. With clips changing every 1.5 s, put a sound on about 1 of 3 cuts: the ones that change meaning (new scene, new character, reveal). Quiet ticks can go on caption pops but at most every other one. Never two impacts within 5 s. "If an SFX doesn't change what the audience understands or feels, skip it" (editor guide).

**Where:**
1. Cuts that start a new idea, aligned so the transient or peak of the whoosh hits the first frame of the new clip (tens of ms matter). Whoosh length matches the on-screen motion.
2. Keywords: on the stressed word of the line (impact/sub/stinger lands on the word start, not mid-sentence). Never over the voice's vowels with a loud sound.
3. Reveals: riser ends 0.3-0.5 s before the word, silence, impact on the word, tail under the next pause.
4. Pauses: long tails/reverbs go into the gaps between phrases.

**Levels vs voice (peak, voice -17 LUFS):** soft whoosh -16 to -20 dB; heavy whoosh -8 to -10; glitch -12; tick -22 to -26; stinger -10 to -12; impact/braam -6 to -8 (peak, tail ducked); sub -9 (mono, < 100 Hz); riser grows to -8; heartbeat -14; room tone -38 to -35 (audible in silence, else drop it); drone -20 under the hook, then faded. Re-level SFX by LUFS or RMS, not by peak (a peak-normalised whoosh is loudest on its noise).

**Layering:** transient (click or crack, 0-30 ms, mids) + body (150 Hz-1 kHz) + tail (reverb/sub, 1-4 s), aligned on the same sample; the sub is mono and high-passed at 30 Hz; the whoosh gets a high-pass at 200-300 Hz so it doesn't fight the voice body. Whoosh + subtle sub for heavy ones (sub, mid punch, high whoosh layering is recommended by Sonilo/Artlist).

**Avoid:** same whoosh repeated at the same pitch (vary ±1-2 semitones and pick from 6+ files, never always the top 2); whoosh on slow fades (use swell); mixed families (sci-fi + cartoon + trailer); SFX louder than voice; sounds with no nameable reason; record scratch, boings; whoosh and impact in the same 1 s; stacking 3 big sounds on the same drop.

## 5. Mix chain

**Voice (our mixer already does a warm shelf + short room):**
1. HPF 70-80 Hz. Our voice is flat (pitch p10-p90 52-90 Hz, body 0.18 vs Zoltium 0.31); add a 2-3 dB bell at 100-150 Hz and 1-2 dB air shelf at 8-10 kHz.
2. De-mud: -2 dB at 250-350 Hz if boomy. Presence +1-2 dB at 3 kHz (speech clarity zone 2.5-5 kHz).
3. Compressor 3:1, 3-6 dB gain reduction, attack 10-20 ms, release 80-150 ms; then a de-esser at 6-8 kHz.
4. Short reverb 0.5-0.8 s, 10-14 % wet, pre-delay 10-20 ms, ducked.
5. Voice target -17 to -16 LUFS short-term at the mix bus before the master.

**Music/SFX bus carve (the missing step):** on the music bus: HPF 30 Hz; dip 2-3 dB at 200-300 Hz; dip 3-4 dB at 2.5-5 kHz (a dynamic EQ keyed from the voice is best); low-pass pads at 8-10 kHz. ProSoundWeb recommends the 2-4 dB cut at 2.5-5 kHz.

**Ducking (sidechain keyed by voice):** music -8 to -10 dB (not the current 3 dB); threshold set so only speech triggers it; attack 15-60 ms, hold 100 ms, release 250-500 ms (CapCut: 30-80 ms attack, 250-700 ms release). SFX tails and reverb duck 3-4 dB. Bed rises back +3 dB across pauses > 0.4 s. Never duck the sub drop or impact transient.

**Master:** integrated -14 LUFS, true peak <= -1 dBTP (practice; Instagram publishes no official spec, sources agree on -14/-1, some say -10 to -12 for TikTok/IG, low confidence). Use a lookahead true-peak limiter (ffmpeg `alimiter` or `loudnorm=I=-14:TP=-1.5:LRA=7` two-pass) and not a hard clip. Check LRA 4-8 LU. Verify on a phone speaker and on earbuds.

**Fix the mixer first (priority):** (1) drop SFX on every cue; add a per-cue importance flag and a density cap; (2) carve + deeper duck; (3) bar-aligned music_offset, no loop; (4) limiter instead of clip; (5) rotate >=6 files per role with pitch jitter; (6) update `audio.md` (it contradicts the mixer).

## 6. Sources
- https://murf.ai/faq/amp/how-to-adjust-music-and-voice-over-volumeloudness/
- https://www.capcut.com/create/audio-ducking-for-clear-dialogue-in-video (duck 6-12 dB, attack 30-80 ms, release 250-700 ms)
- https://voxbooster.com/blog/mix-background-music-with-voice-streamer-podcaster-guide (music -20 LUFS or quieter; URL as returned by search: https://voxbooster.com/blog/mix-voice-with-background-music)
- https://tryuncle.com/learn/davinci-resolve/how-to-duck-background-music-under-dialogue-in-davinci-resolve
- https://www.vegascreativesoftware.info/us/forum/mixing-voice-overs-with-music--31674 (7-14 dB, attack ~15 ms)
- https://sonicstate.com/news/2022/11/23/automatic-voice-over-mixing/
- https://vloggingpro.com/tools/audio-loudness/ (IG -14 LUFS / -1 dBTP; not official)
- https://openclip.app/learn/audio-normalization
- https://opus.pro/blog/best-loudness-normalizers
- https://sonilo.com/ai-music/whoosh-sound-effect-guide
- https://beverlyboy.com/blog/transition-sound-design-that-strengthens-commercial-video-editing
- https://www.filmeditingpro.com/a-video-editors-guide-to-sound-design/
- https://artlist.io/blog/tips-that-will-take-your-sound-design-to-the-next-level/
- https://violetrecording.com/sound-design-for-trailers/
- https://sounddesign.irpr.agency/guides/guide-to-trailer-sound-design/
- https://sounddesign.irpr.agency/glossary/riser/
- https://violetrecording.com/what-is-phonk/ (phonk BPM 130-140 half-time)
- https://shortsfast.com/blog/mix-background-music-under-narration-without-masking-speech/
- https://easyviral.ai/blog/we-analyzed-500-viral-faceless-shorts (vendor stats, low trust)
- https://darksideofsynth.gumroad.com/l/dark-tension-drone (listing; 55-90 BPM narration beds, vendor)
- Prior notes: [[sound-design-psychology]] (Murch, ProSoundWeb 2.5-5 kHz carve, Production Expert reverb ducking), [[zoltium-sound]] (measured).
