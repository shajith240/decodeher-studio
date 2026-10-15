# Reel pipeline: PRODUCTION v1 (logged 2026-10-14)

Reference build: `reels/p1c-hookb` → `deliverables/REEL-01-FINAL-v1.mp4` (43.6 s, -11.4 LUFS). Post this look for one week, then
change things only from audience feedback. The old silhouette pipeline is archived in ~/dark-psycology-archive/2026-10-14-v1/.

## Look (owner-approved, each rule was earned by a rejection)
- 2D illustrated clips from Pinterest, one per phrase (~1.5–2.5 s), each with its own eased camera move (push / pull / pan / tilt / hold).
  NEVER a black gap: a line without a clip continues the previous shot (owner: black screens look like a bug).
- Film finish ON THE CLIPS ONLY: fresh grain every frame, vintage grade (faded blacks, warm), soft bloom, vignette.
- Captions crisp on top: Cormorant SC 700, 90 px, solid WHITE, key words in our signature purple #C9A2FF (no gold, no metal — owner),
  thin dark edge, soft haze, CENTRED (top 905 px — owner: "a bit downward"),
  ≤ 3 words, appear 0.12 s BEFORE the word (no lag), key words bloom a purple glow. No shimmer.
- Bust watermark bottom-centre; logo outro on "Follow for more" with the signature outro hit.

## Script (owner: "plain talk, like a guy to his friend")
Hook names his exact situation in ≤ 12 words → first-person story ("Bro, I was that guy…") → "but" turn at ~12 s → one plain
picture of WHY → one copyable move → motivational close ("You wasted so much time, boy. Now focus on yourself.") → "Follow for more."
as its own line. 40–45 s. Grade with brain/research/hooks-retention-v2.md; owner approves the script before voicing.

## Steps (tools/)
1. `assets/vo/script.json` (+ optional per-line {"text","ex","cfg"}), `reel.json` (gaps, drops, ctaLine, speed 1.07, accent, music)
2. `python3 tools/reel_vo.py R` (Chatterbox natural, -1.5 st Rubber Band, whisper-checked) → `reel_timing.py` → `align_words.py`
3. `shots.json` (say, q) → `shot_times.py` → `pinfetch.py` (LINES=…) → `clipsheet.py` → Haiku judges (clips/judge/NN.json,
   "force" for editor picks) → `clippick.py` (meaning-first, no repeats, fallback flagged) → `clipcut.py` (moves + film finish)
4. `sfx.json` (every_cut whoosh + word cues) → `word_cues.py` → `reel_mix.py` (music from library/music/approved, -11 LUFS,
   bed -22 un-ducked / 6 dB duck, effects +5 dB, signature outro hit; CC-BY credit → assets/audio/credit.txt)
5. `npx hyperframes render --quality delivery` → mux final.wav → deliverables/. Check 4 frames before handing over.
6. `cliplib.py add R` (judged clips → Drive), then delete unused candidates and bg.mp4 (disk is tight).

Research behind each rule: research/sound-design-v2.md, hooks-retention-v2.md, narration-emphasis.md, captions-readability.md,
zoltium-sound.md, zoltium-story-visuals.md.
