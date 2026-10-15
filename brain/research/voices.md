# Voiceover options for dark-psychology Reels (replacing ElevenLabs)

Machine: RTX 3050 **6GB** laptop GPU (checked with nvidia-smi). This is smaller than the 8-12GB assumed in the brief, so VRAM is the main local constraint.

## Key findings

- **Fish Audio open weights are not cleared for commercial use.** The Fish Speech code and weights are under the Fish Audio Research License. It allows research, personal, and evaluation use only. Commercial Purpose, including hosted APIs and any revenue-generating product, needs a separate written license. Source: https://raw.githubusercontent.com/fishaudio/fish-speech/main/LICENSE
- **Fish Audio pricing is unclear.** The models page lists s2.1-pro (paid, with TTFA/DPA guarantees) and s2.1-pro-free ("free to use under fair-use limits", no guarantees). It gives no per-unit price, no free-tier numbers, and no commercial-use statement. Source: https://docs.fish.audio/developer-platform/models-pricing/models-overview. The fish.audio/pricing page returned 404. Secondary blogs disagree on free-tier commercial rights and quote $15 per million UTF-8 bytes for the API (unverified). Confirm terms with Fish Audio before paying or publishing.
- **No verified 2026 listening-test ranking.** Search results disagree on the TTS Arena / Artificial Analysis order. ElevenLabs Eleven v3 appears mid-pack (roughly ELO 1175-1178) in several secondary sources. Those aggregators conflict, so treat them as unverified. Check https://artificialanalysis.ai directly. Chatterbox's page links Podonos evaluations against ElevenLabs Turbo v2.5, but the results are not on that page.

## Comparison

| Option | Realism vs ElevenLabs | License (code / weights) | VRAM (6GB) | Linux install | Speed | Emotion/pacing control |
|---|---|---|---|---|---|---|
| Fish Audio hosted (s2.1-pro) | Not benchmarked here; vendor claims high quality | Hosted API: paid commercial terms (unverified) | n/a | API key | 100ms TTFA claimed (vendor) | `[bracket]` emotion tags |
| Fish Speech / OpenAudio S1/S2 (local) | Vendor-claimed near parity; unverified | Research License, **no commercial use** | Not stated | Docker or install docs | Benchmark on H200 only | Bracket tags |
| Chatterbox (resemble-ai) | Podonos tests vs ElevenLabs Turbo exist; numbers not checked | Code MIT; weights license not verified | Not stated | `pip install chatterbox-tts`, tested on Python 3.11 | Not stated | `exaggeration` (about 0.7+ for drama), `cfg_weight` for pacing. Turbo adds `[laugh]`-style tags |
| F5-TTS | Not verified | Code MIT; **pretrained weights CC-BY-NC** (Emilia data) | Not stated | conda + pip, torch cu128 (documented) | Not stated | Not documented; cloning-based |
| Dia (Nari Labs) | Not verified | Apache-2.0 | About 4.4GB bf16 on RTX 4090 (tight on 6GB) | `uv run example/simple.py` | Not stated | Audio-prompt conditioning for tone; overly long input speeds up speech |
| Orpheus (Canopy Labs) | Not verified | Apache-2.0 (card says 3B; file lists 4B) | Not stated; 3-4B will need quantization on 6GB | Not checked | Not stated | Tags such as emotion/intonation supported |
| Kokoro-82M | Lower expressiveness; no ranking claim on its page | Apache-2.0 | Under 1-3GB, runs on CPU | Easy | Very fast | Speed parameter (unverified on page); limited emotion |
| VibeVoice-TTS | Not usable | Code MIT; TTS code removed from repo, weights disabled, research-only | n/a | n/a | n/a | n/a. **Avoid.** |
| XTTS v2 / Coqui | Not verified | Coqui Public Model License: **non-commercial** | 4-6GB (secondary source) | Medium | Medium | Limited |

## Ranking

**Best hosted:** Fish Audio s2.1-pro, but only after written confirmation that a paid plan or API key covers commercial Reels. Otherwise ElevenLabs stays the safe default. Do not publish on the free tier until its terms are confirmed.

**Best local for a 6GB card:** Chatterbox. Its code is MIT, it has emotion/exaggeration control, and it has a Linux install. Check the weights' license on the Hugging Face card before commercial use. Dia is the fallback if its Apache-2.0 license and the 4.4GB footprint fit. Kokoro is the lightest option if quality is acceptable.

**Stay with Fish Audio?** Not for commercial output on the current evidence. The open weights are non-commercial. The hosted route is viable only if its terms cover commercial Reels. Get the answer from Fish Audio before switching.

**Next steps:**
1. Email Fish Audio for written commercial terms and per-unit API pricing.
2. Run a blind A/B on 3 short scripts: ElevenLabs vs Chatterbox vs Dia (and Fish s2.1-pro if licensed).
3. Verify VRAM on the 3050 for Dia and Orpheus.

## Unverified claims

- All VRAM figures except Dia's (4.4GB, RTX 4090) are unverified.
- Free-tier commercial rights and the $15/M-byte price come from secondary blogs.
- Arena ranks come from conflicting aggregators.

## Sources

- https://raw.githubusercontent.com/fishaudio/fish-speech/main/LICENSE
- https://github.com/fishaudio/fish-speech
- https://docs.fish.audio/developer-platform/models-pricing/models-overview
- https://github.com/resemble-ai/chatterbox
- https://github.com/SWivid/F5-TTS
- https://huggingface.co/canopylabs/orpheus-3b-0.1-ft
- https://huggingface.co/hexgrad/Kokoro-82M
- https://github.com/nari-labs/dia
- https://github.com/microsoft/VibeVoice
- https://huggingface.co/blog/arena-tts
- https://artificialanalysis.ai
