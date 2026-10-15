---
name: reverse-engineer-edit
description: Take apart a reference video's edit (YouTube, Shorts, Reels) shot by shot — timing, shot grammar, devices, text, sound, hook — and turn it into a storyboard template and rules in the brain vault. Use when the owner says "reverse engineer", "steal this editing style", "copy how <creator> edits", "break down this video", or sends a reference reel.
---

# Reverse-engineer an edit

The output is **evidence, not impressions**: every claim has a timestamp you actually looked at.

## 1. Get the evidence
Use the watch skill's script (local engine). Dense frames for the hook, sparse for the rest:
```bash
W=/home/shajith/.claude/plugins/cache/claude-video/watch/0.3.2/skills/watch/scripts/watch.py
python3 $W "<url>" --start 0 --end 12 --fps 2 --out-dir <scratchpad>/re      # the hook, 2 frames per second
python3 $W "<url>" --start 12 --end 90 --detail balanced --max-frames 40 --out-dir <scratchpad>/re
```
Read every frame. Pair frames with the transcript lines at the same time (captions, or a vault note's transcript).

## 2. Log every shot
A table, one row per visual change: `start–end · what is on screen · what the voice says · how it entered/left · device`.
Measure: average shot length, longest hold, how many seconds before the first change, how many figures, what is lit vs dimmed.

## 3. Name the devices
For each recurring device (figure enters, dim-to-focus, arrow, label, speech line, single word on black, icon, prop, camera push)
write: when it is triggered relative to the words (on the noun? on the verb? before?), how long it stays, how it animates.

## 4. Hook (first 3 s)
Second by second: picture, words, text. Which hook formula (POV "this is you", contrast, bold claim, question, story)?

## 5. Sound
Music character, where it rises/drops, SFX and the exact moments they hit, silences before punchlines.

## 6. Write it into the brain
- `brain/research/<creator-or-video>.md` — the shot log, devices, hook, sound, with timestamps.
- A **storyboard template**: the beat structure as a reusable list (beat → visual device → duration).
- Proposed rule changes: list them at the end under "Proposed rules" — the main agent merges accepted ones into `brain/rules/*`.
Never copy their exact words, characters or artwork; we copy the *grammar*, with our own cast and script.
