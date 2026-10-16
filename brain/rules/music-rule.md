# Background music rule (owner 10-16, FINAL)

Only smooth HORROR-FILM ambience or PIANO / strings scores. Never beats, drums, pulses, trap, uplifting or "breaking" / choppy tracks.
The music never competes with the narrator.

Measured gate (librosa, first 120 s) — a track joins library/music/approved only if ALL hold:
- percussive energy share (HPSS) <= 0.03
- onsets per second <= 3
- 99th-percentile loudness jump between frames <= 4 dB
- and it is horror ambience or piano/strings by ear

Mix (tools/reel_mix.py): bed at -26 LUFS un-ducked, ducked 9 dB under speech, plus a hard rule that the bed stays >= 12 dB
under the voice wherever he talks.

Removed 10-16 (failed the gate or the owner rejected it): portal-mysterious, portal-2-mysterious, thriller-suspense,
gritty-gated-vapor-trap-beat, sleeper-beats, drums-of-the-deep, dark-pulse, intense-ambient-rhythmic-pulse, dark-fog,
ghostpocalypse-4-temptress, giant-wyrm, ossuary-6-air, promising-relationship, stay-the-course (files in library/music/removed/).
