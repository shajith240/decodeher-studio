# Audio (strict)

- **Voice**: Fish "horror" (`ef9c79b62ef34530bf452c0e50e3c260`), speed 1.1, every line at −18 LUFS with clean edges ([[pipeline]]). Never a clone of a real creator.
- **Speech gate**: `tools/reel_asr.py` must pass; and the final mp4's audio must contain every script word.
- **Music**: calm, warm, **no suspense**, no drones, no horror pads. CC0/CC-BY only, logged in [[assets/music]].
  Ducked under the voice (bed 0.5, under speech 0.18), one continuous take.
- **SUPERSEDED 10-14** (owner wants Zoltium-style sound design): full SFX palette and a real beat, see [[research/zoltium-sound]] and tools/reel_mix.py. The old rule was: soft pop per caption card, low thump per punch word, no whooshes.
- Mix: −14 LUFS integrated, ≤ −1 dBTP, no dropouts.

## Choosing music (owner, 10-13: "you're adding music without any idea or taste")
- Claude cannot hear. Never pick a track from a search result or a measurement and ship it as "the music".
- Shortlist CC0/CC-BY tracks that are calm, warm, with **no drums and no suspense** (soft keys, piano, ambient), then render
  the same reel once per track (`renders/music-options/`, plus a voice-only version) and **the owner picks by ear**.
- The owner's pick becomes the house track, logged in [[assets/music]]; reuse it until the owner changes it.
- Rejected so far: synthesised suspense drone (10-12), chill hip-hop beat with drums (10-13).

## Sound design v2 (owner, 10-14: "choose each sound for its psychological job, not at random")
- Research: [[research/sound-design-psychology]], [[research/zoltium-sound]].
- **Library:** library/sfx-pro (Sonniss GDC + Mixkit: commercial use, no credit; do not resell the raw files and do not use them for AI training).
- **Chosen BY EAR:** `tools/ear.py rankall` (LAION CLAP) scores every file against its job and its must-not descriptions and writes
  library/sfx-pro/ranked.json. Files that match a must-not better than their job are dropped (all "phone" and "breath" files were).
- **Sound signature, reused in every reel:**
  - scene change → soft airy whoosh
  - message → soft chat pop (library/sfx/notification-1)
  - strike → glitch
  - tag → subtle UI tick
  - punch → braam
  - drop → riser + reverse swell → 0.45 s silence → deep thud + sub drop
- **Hook layer:** a tension drone from frame 0 into the first drop; room tone under everything at -40.
- **Density:** 3–6 effects per 10 s, at most one big hit per 10 s, and voice + bed + one effect at any moment.
- **Check:** `tools/ear.py moments final.wav a-b …` should hear "deep male voice over a dark tense beat" on top.
  The "cheap soundtrack" label scores about the same on Zoltium, so it is background noise in the model.

## Outro (brand)
`DN.cta(9, { outro: "assets/brand/outro.mp4" })` plus a STATIC `<video class="clip" id="outro" …>` in the HTML before #fg.
HyperFrames finds media by reading the file, so a video injected at runtime renders as a frozen frame. The build writes its
start and duration. The source is library/brand/outro-source.mp4, cropped (watermark out), 2× speed, last frame held.
