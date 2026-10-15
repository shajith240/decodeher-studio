# Zoltium sound design: measured (10-14)

Source: two @zoltium reels (54.5 s and 37.2 s) the owner sent, compared with our w1-01. Method: Demucs stem split (vocals /
drums / bass / other), then pyloudnorm, librosa onsets/pitch/pyin, spectrograms. Files are in the session scratchpad (zol/).

| | z1 | z2 | ours (w1-01) |
|---|---|---|---|
| voice LUFS | -18.5 | -22.5 | -16.6 |
| music+sfx LUFS | -24.7 | -20.8 | **-34.0** |
| voice over bed while talking | +3.3 dB | **-4.4 dB** | **+20.9 dB** |
| drums / bass LUFS | -30.8 / -26.3 | -26.8 / -22.3 | -46.5 / **-58.4** (none) |
| tempo | ~118 BPM | ~120 BPM | n/a (pad) |
| bed hits per 10 s | 13.9 | 23.9 | 11.7 |
| talk ratio | 0.85 | 0.86 | 0.65 |
| pause median / max | 0.20 / 0.97 s | 0.30 / 0.65 s | 0.50 / 0.91 s |
| voice pitch median (p10–p90) | 80 Hz (66–135) | 97 Hz (72–148) | 75 Hz (52–90): flat |
| voice body (<300 Hz share) | 0.31 | 0.23 | 0.18: thin |
| room tail after phrases | 0.14 s | 0.22 s | 0.11 s: dry |

**Structure (spectrograms):**
- z1 opens on a bass drone with high air.
- At 6.8 s: a rising sweep, then **0.5 s of silence**, then the beat DROPS (full spectrum, heavy sub).
- Mid-reel: whoosh and reverse sweep → silence → a big impact with a long tail → a new, louder section.
- z2: a trap groove (808 every beat, dense hats) with whooshes on cuts.

**What we apply (tools/reel_mix.py):**
- the bed only ~4 dB under the voice
- a real beat
- drops on the story's turn and on the payoff: riser → 0.45 s silence → impact + sub
- the intro filtered like a drone
- whooshes on scene changes
- a warmer voice with a short room tail
- pauses tight (0.25–0.3 s), except the 0.6 s before a drop

Picture rhythm: [[zoltium-story-visuals]]. The whole frame changes about every 1.5 s; see DN.rhythm.
