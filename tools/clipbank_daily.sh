#!/bin/bash
# Daily clip-bank harvest: 40 Pinterest queries (~10 clips each tried), gentle (20-40 s between queries); stops for the day on 429/login errors.
# Wiring (owner does this): the factory/manager can run `bash tools/clipbank_daily.sh` once a day (e.g. manager checks logs/clipbank.log mtime > 20 h,
# and runs it detached when the disk has > 6 GB free). Safe to run twice: harvest-state.json resumes, and stopped_day blocks a second run after an error.
# GitHub Actions: needs PINTEREST_COOKIES_FILE (cookies.txt from the secret) + rclone config; run the same command on a daily cron.
cd "$(dirname "$0")/.." || exit 1
FREE=$(df --output=avail -BG . | tail -1 | tr -dc 0-9); [ "${FREE:-0}" -lt 3 ] && { echo "disk < 3 GB free, skipping" >> logs/clipbank.log; exit 0; }
exec uv run --with torch --with transformers --with pillow --with numpy --with gallery-dl --with yt-dlp --with secretstorage \
  python tools/clipbank.py harvest --queries "${QUERIES:-40}" --per "${PER:-10}"
