#!/usr/bin/env bash
# Clip reel, stage 1 of 2 (brain/pipeline.md v1): after the voice is aligned and the clips are in clips/cand/ —
# time the shots to the voice, put the sounds on their words, fill the page, and make the contact sheets for the judges.
# Usage: tools/reel_prep.sh reels/<reel>
set -euo pipefail; R="$1"; cd "$(dirname "$0")/.."
python3 tools/shot_times.py "$R" >/dev/null
python3 tools/word_cues.py "$R" | cut -c1-40
python3 tools/fill_page.py "$R"
HF_HUB_OFFLINE=1 uv run -q --python 3.11 --with transformers --with torch --with pillow python -W ignore tools/clipsheet.py "$R" 2>&1 | grep -c "^line" | sed 's/^/sheets: /'
