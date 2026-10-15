# Open-weights TTS survey for dark-psychology narration (as of 2026-10-14)

Scope: replace Fish Audio cloud TTS with a self-hosted open-weights model that gets close to ElevenLabs (emphasis, rising questions, pauses/breaths, emotion, deep bass male).

## Read this first: caveats on the evidence
- Leaderboard numbers below come from third-party blog aggregators that disagree with each other (different boards, dates, scales). Treat Elo as a rough tier, not a precise rank. One source (offlinetts.com) deleted its own numeric ranking in a 2026-09-30 correction. The live boards to check yourself: https://artificialanalysis.ai/text-to-speech/leaderboard and the HF TTS Arena Space (https://huggingface.co/blog/arena-tts is only the 2024 launch post; I could not confirm current HF standings).
- Vendor-run claims (e.g. Chatterbox "65.3% preferred over ElevenLabs", https://findskill.ai/blog/best-open-source-tts-2026/) are Resemble AI's own study. Not independent.
- Speed/RTF and VRAM figures are mostly NOT in official docs; where I give them they are labelled as third-party or my estimate.
- I did not listen to any audio. Nothing here proves a model produces a good deep-bass narrator; step 1 of the plan is an A/B listening test.

## KEY FINDING for us: Fish Audio's best open model is NON-commercial
Fish Audio S2 Pro weights are under the "Fish Audio Research License": research/non-commercial free; commercial use needs a separate licence from business@fish.audio (https://huggingface.co/fishaudio/s2-pro). It has 15,000+ free-form inline tags like [whisper], [pause], [laughing] and RTF 0.195 on an H200, and scores ~1,110-1,129 Elo on third-party boards (https://www.offlinetts.com/blog/tts-arena-leaderboard-2026/ snapshot, https://local-ai-zone.github.io/blog/local-voice-models-2026.html). Great model, but for a monetised IG page it is not a free-commercial option. This matches our existing note that Fish commercial terms are unclear.

## Summary table

| Model | Quality evidence | Emotion/emphasis control | Cloning | Code / weights licence | Hardware | Verdict |
|---|---|---|---|---|---|---|
| Chatterbox (500M) / Turbo (350M) / Nano, Resemble AI | ~1,020 Elo open-weight board (local-ai-zone, Aug 2026); 1,026 on Artificial Analysis Oct 2026 per search summary; vendor blind test claim vs ElevenLabs | Original: `exaggeration` + `cfg_weight` sliders. Turbo: inline tags [cough] [laugh] [chuckle] "and more" (full list not published on card) | ~10 s clip (README example) | MIT / MIT; every output carries Perth watermark | ~3-4 GB VRAM (local-ai-zone); Turbo lighter; Nano ~3x realtime on 8 CPU cores | PICK 1 |
| Qwen3-TTS 0.6B / 1.7B (Alibaba Qwen) | Self-reported 1.24 WER Seed-TTS-en; not on the Elo table; one anecdote favours Chatterbox for consistency | Natural-language `instruct` (VoiceDesign model: describe the voice; CustomVoice: "speak in an angry tone") | 3 s clip + transcript (Base) | Apache-2.0 repo and HF cards | ~2-4 GB VRAM (local-ai-zone); flash-attn optional | PICK 2 |
| Step Audio EditX (3B, StepFun) | 1,102 Elo, highest permissive in local-ai-zone table | Post-hoc "edit" passes: emotion (happy/angry/sad/fear...), style (serious, whisper, news), paralinguistic tags; iterate 1-3 times | Clip <30 s + its text | Code Apache-2.0; weights licence not stated on README (check HF) | 12 GB optimal, 8-10 GB with AWQ 4-bit, 6-8 GB memory-efficient; NVIDIA only | Runner-up; English emotion scores lag Chinese |
| IndexTTS-2 / 2.5 (bilibili) | No independent ranking found | Separate emotion reference clip, 8-float emotion vector, or emotion-from-text; `duration_factor` speed control (2.5) | single clip | bilibili Model Use License; commercial needs email to indexspeech@bilibili.com | RTF ~0.21 on RTX 4090 (README); VRAM not stated | Skip for commercial |
| Higgs Audio v2 (3B base, ~6B params) / V3 | V3 ~1,042 Elo | Auto prosody, multi-speaker, humming | zero-shot via reference in context | HF licence "other" (custom); one source flags Higgs as non-commercial: verify the LICENSE file | ~13 GB FP16 est. (Spheron estimator), ~6 GB INT8 est. | Skip until licence verified |
| Fish S2 Pro | 1,110-1,129 Elo | 15,000+ free-form bracket tags | yes (length not stated) | Research / non-commercial weights | 4B+400M params | Not usable commercially without paid licence |
| VibeVoice (Microsoft) | 7B ~969 Elo | podcast-style multi-speaker | yes | Repo says MIT but model "research and development only", "do not recommend commercial use"; 1.5B TTS code was removed 2025-09-05, quick-try disabled (https://github.com/microsoft/VibeVoice) | 0.5B Realtime exists | Skip |
| Dia (Nari Labs, 1.6B) | not ranked in sources I found | [S1]/[S2] speaker tags, (laughs) (sighs) (coughs) | 5-10 s clip + transcript | Apache-2.0 | ~4.4 GB bf16; ~2x realtime on RTX 4090; CPU not supported | English only; voice changes every run without prompt/seed; >20 s input speeds up unnaturally; poor fit for single-narrator long reads |
| Orpheus (Canopy Labs, 3B) | not ranked in sources I found | tags <laugh> <chuckle> <sigh> <cough> <sniffle> <groan> <yawn> <gasp>; built-in voices tara, leah, jess, leo, dan, mia, zac, zoe | finetune (~50-300 examples/speaker; LoRA ok) | Apache-2.0 repo; weights licence not stated on README | vLLM; llama.cpp no-GPU path exists; ~200 ms streaming latency claimed | Possible via fine-tune for a bass voice; more work |
| Kokoro 82M | ~1,060 Elo; 1,064 on Artificial Analysis Oct 2026 per search summary | none (no emphasis/emotion tags; only phoneme override) | none, fixed voice bank (54 voices) | Apache-2.0 | CPU fine, ~2 GB RAM | Fast and clean but flat; will not fix our "robotic" complaint |
| Zonos v0.1 (Zyphra) | ~1,000 Elo | emotion/pitch conditioning | yes | Apache-2.0 | ~6 GB | Older; no reason to prefer |
| Breeze TTS 2 (3B) | 1,215 Elo (top open, vendor-adjacent blog, https://www.orcarouter.ai/blog/breeze-tts-2-tops-open-weights-speech-arena) | voice direction | weak on controlled-voice board | Research, non-commercial | 7.7-12 GB | Not commercial |
| Voxtral TTS (Mistral) | 1,082 | n/a | 3 s | CC BY-NC 4.0 | n/a | Not commercial |
| Maya1 | 1,045 | voice designed from text description | none | Apache-2.0 | n/a | Interesting for "design a deep voice"; unverified |
| F5-TTS, MaskGCT, CosyVoice 2/3, Spark-TTS, Llasa, Sesame CSM | Not covered by sources I fetched; not researched in depth | | | | | Not evaluated. Do not assume anything. |

Main sources: https://local-ai-zone.github.io/blog/local-voice-models-2026.html, https://github.com/resemble-ai/chatterbox, https://huggingface.co/ResembleAI/chatterbox-turbo, https://github.com/QwenLM/Qwen3-TTS, https://github.com/stepfun-ai/Step-Audio-EditX, https://github.com/index-tts/index-tts, https://github.com/nari-labs/dia, https://github.com/canopyai/Orpheus-TTS, https://huggingface.co/hexgrad/Kokoro-82M, https://huggingface.co/bosonai/higgs-audio-v2-generation-3B-base, https://pinggy.io/blog/best_open_source_self_hosted_text_to_speech_models/

## Per-model notes on stability / English quality
- Chatterbox: MIT, English-focused, consistent timbre from a fixed reference (anecdote: https://archy.net/from-qwen3-tts-to-chatterbox-finally-getting-voice-cloning-right/). Stability on long text: no authoritative data; the safe practice is to synthesize per sentence/phrase and join (also gives us pause control).
- Qwen3-TTS: vendor claims up to ~10 min continuous generation and 2.81% English WER (secondary write-ups, https://howaiworks.ai/blog/qwen3-tts-open-source-announcement-2026), unverified independently. The one hands-on report saw cloned timbre drift with longer reference clips and needed a pinned seed (Qwen3-TTS CustomVoice, not VoiceDesign).
- Step Audio EditX: self-reported English emotion score only 51 -> 67 after 3 edit iterations vs Chinese 81.6, so English emotional range is weaker than headline numbers.
- Dia: dialogue-oriented, see table.

## TOP 2 for us

### Pick 1: Chatterbox (original 500M for exaggeration slider; Turbo for tags and speed)
Why: only mainstream model that is MIT for code AND weights, small enough for an 8 GB card or even CPU (Nano), has an explicit drama dial, and cloning from a ~10 s clip lets us choose the bass timbre. Cost: Perth watermark in the audio (imperceptible, survives MP3, per README; check it does not matter for IG, it should not), and Turbo's `exaggeration` support is undocumented, so use the original model when you want the slider and Turbo when you want [laugh]-style tags.

Install (README says Python 3.11):
```
conda create -yn cb python=3.11 && conda activate cb
pip install chatterbox-tts
```
Usage (from README; Turbo class shown):
```python
import torchaudio as ta
from chatterbox.tts_turbo import ChatterboxTurboTTS   # check import path in repo
m = ChatterboxTurboTTS.from_pretrained(device="cuda")
wav = m.generate(text, audio_prompt_path="bass_ref_10s.wav")
ta.save("out.wav", wav, m.sr)
```
Original model: `ChatterboxTTS.from_pretrained(device="cuda"); m.generate(text, audio_prompt_path=..., exaggeration=0.7, cfg_weight=0.3)`. README guidance: defaults 0.5/0.5; for dramatic speech use exaggeration ~0.7+ and cfg_weight ~0.3; higher exaggeration speeds speech up, lower cfg_weight slows it.

Marking the script: Chatterbox has no SSML and no emphasis tag. What works (my recommendation, test it):
- Pauses/breaths: split the script into phrase-level chunks, generate each separately, and join with explicit silence you control (e.g. 250 ms comma, 600 ms dramatic beat) in ffmpeg/numpy. Natural breath: add a short breath sample (CC0) in the gap. Do not rely on "..." alone.
- Questions: end the chunk with "?" and keep the question as its own chunk; regenerate with different seeds and pick the take with rising pitch (cheap automated check: compare F0 of the last 300 ms vs the previous 300 ms).
- Emphasis: no direct control. Use short chunks around the key word (e.g. "That's not love." / "It's control.") with exaggeration 0.8 for the punchline chunk and 0.5 for setup lines; capitalisation of one word is unverified, test it.
- Emotion per line: set exaggeration per chunk (setup 0.45, reveal 0.8). Turbo tags such as [laugh], [chuckle], [cough] only (the card does not list others); for ominous tone they are rarely useful, so skip.

Deep bass narrator:
1. Reference clip (~10 s, clean, no music) of a naturally deep male reader. Licensing-safe sources: LibriVox recordings (public domain, https://librivox.org) and Mozilla Common Voice (CC0). Cloning a real person's voice from public-domain recordings is legal for audio licensing but consider the ethics; prefer a volunteer reader known for deep voice, or record someone who consents. (I did not verify specific LibriVox readers; audition several.)
2. Post-process for the bass: ffmpeg `asetrate`/`rubberband` pitch down 1-2 semitones, low-shelf +4 dB at ~120 Hz, gentle compression, high-pass 60 Hz, then a touch of room reverb. Pitch-shifting a cloned voice is the most reliable way to get "Zoltium-style" weight regardless of model. Check formant artifacts above 2 semitones.

### Pick 2: Qwen3-TTS (1.7B Base for cloning, 1.7B VoiceDesign for describing the voice)
Why: Apache-2.0 on the repo and HF cards (confirm weights licence on each card before shipping), accepts a natural-language instruction, so "deep, gravelly, slow, ominous male documentary narrator" is a prompt instead of a hunt for a reference clip. 3 s cloning also available. Cost: stability and long-form consistency are vendor-claimed only; the one anecdote had drift; independent audio quality is unproven for deep male.

Install (Python 3.12 recommended):
```
conda create -yn qw python=3.12 && conda activate qw
pip install -U qwen-tts
# optional: MAX_JOBS=4 pip install -U flash-attn --no-build-isolation
```
Usage per repo README: `generate_voice_design(text, instruct="...")` on the VoiceDesign model; Base model clone takes `ref_audio` + `ref_text` (or `x_vector_only_mode=True` with lower quality). Exact argument names: confirm in the README, I only saw them summarised.

Example voice prompt (example I suggest, untested): "A very deep, low-pitched male voice, slow measured pace, calm, intimate and ominous, like a dark documentary narrator, with deliberate pauses." Lock the voice by generating once, then reusing the clone prompt for every reel (the README describes reusing a clone prompt) and pin the seed to avoid drift.

Marking the script: emphasis/pauses via instruction and punctuation, not tags. Per-chunk `instruct` ("whisper, intimate", "rising, accusing question", "slow and heavy") is the closest thing to ElevenLabs direction. Same chunk-and-stitch approach for pauses as above. Apply the same ffmpeg bass chain.

### Runner-up if Pick 1/2 sound flat: Step Audio EditX
Highest permissive-licence Elo (1,102). Edit passes ("whisper", "serious", emotion names) on top of a cloned base give the most explicit emotion control among permissive models. Needs a 12 GB-class card (8-10 GB with AWQ), Python 3.12, PyTorch 2.9.1+. Check the weights licence on its HF card first.

## Expected per-reel generation time (ESTIMATES, not measured by me)
Assume ~120-140 words, ~45-55 s of audio, generated in ~12-15 chunks, plus 2-3 takes for question/punchline lines (~25 chunk-generations).
- (a) NVIDIA 8-12 GB: Chatterbox/Turbo and Qwen3-TTS are small models; a 5-15x realtime-ish rate is plausible but no official RTF is published (Dia is the only one with a table: ~2x realtime on a 4090, which is a larger autoregressive model; IndexTTS-2.5 RTF ~0.21 on a 4090). Estimate 1-3 minutes per reel including retakes; 10 min if you retake a lot. Step Audio EditX: several times slower because of iterative passes, estimate 5-15 min.
- (b) CPU only: Chatterbox Nano is documented ~3x realtime on 8 cores (README), so ~20-30 s of compute per 60 s of audio is plausible for Nano; the full Chatterbox/Qwen3-TTS on CPU is likely near or slower than realtime (estimate 3-15 min per reel). Kokoro is the only model well proven on CPU, but it has no emotion control. Nano quality vs full Chatterbox is untested by me.
Action: benchmark one real script on our machine (cheap) before committing.

## Where open models still fall short of ElevenLabs (honest)
- No tool in the table gives ElevenLabs-style per-word emphasis; open models infer emphasis from text/punctuation or coarse sliders, so you stitch and retake. Expect to curate takes.
- Long single-pass reads can drift in pace/timbre; chunking is mandatory, which adds work and risks pitch/loudness mismatch at joins (fix with loudness normalisation and crossfades).
- Questions rising reliably is hit-or-miss without retakes.
- Deep bass: cloned voices usually land near the reference's pitch; truly cinematic bass needs a good reference and/or DSP.
- Top-scoring open models (Fish S2 Pro, Breeze TTS 2, Higgs V3, Voxtral) are research/non-commercial, so the best naturalness is gated by licence. The permissive ones (Chatterbox, Step EditX, Kokoro, Qwen3-TTS) score lower on third-party boards than those and, per the aggregators, below ElevenLabs.
- Chatterbox output is watermarked (Perth). Dia and Orpheus and others need more setup/fine-tuning.
- Several sources are SEO blogs with conflicting figures; re-verify licences in each repo's LICENSE file before relying on them commercially.

## Suggested next step
Build a 10-line A/B script: same 3 reel scripts rendered by Chatterbox (exaggeration 0.5/0.7/0.85), Qwen3-TTS VoiceDesign, and (if GPU allows) Step Audio EditX, each through the same ffmpeg bass chain. Owner listens blind against current Fish output and an ElevenLabs sample.
