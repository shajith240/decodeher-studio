#!/usr/bin/env bash
# Clip reel, stage 2 of 2 (brain/pipeline.md v1): after the Haiku judges wrote clips/judge/NN.json —
# pick the clips, cut the graded film (camera moves + film finish), mix the sound, render, check 4 frames, clean up.
# Usage: tools/reel_finish.sh reels/<reel> [deliverables/out.mp4]
set -euo pipefail; R="$1"; cd "$(dirname "$0")/.."; slug="$(basename "$R")"; OUT="${2:-deliverables/week-2/$slug.mp4}"; mkdir -p "$(dirname "$OUT")"
log(){ echo "$(date +%H:%M:%S)  $*" >> logs/activity.log; }; log "Picking clips · $slug"
# owner 10-17: OCR every candidate clip first; clippick refuses any clip with baked-in text (library/clip-text.json)
{ uv run -q --offline --with rapidocr_onnxruntime python -W ignore tools/clip_text.py "$R" || uv run -q --with rapidocr_onnxruntime python -W ignore tools/clip_text.py "$R"; } | head -1
python3 tools/clippick.py "$R" | grep -cE "fallback|NO CLIP" | sed 's/^/weak or missing shots: /' || true
python3 tools/clipcut.py "$R" | cut -c1-60
python3 tools/peak_points.py "$R" || true   # 10-16: snaps/laughs only at the narration peaks
{ uv run -q --offline --with numpy --with scipy --with soundfile --with pyloudnorm --with librosa python -W ignore tools/reel_mix.py "$R" || uv run -q --with numpy --with scipy --with soundfile --with pyloudnorm --with librosa python -W ignore tools/reel_mix.py "$R"; } | cut -c1-160   # 10-16: offline first (flaky internet broke a mix)
free_tmp=$(df --output=avail -k /tmp | tail -1); if [ "$free_tmp" -lt 1500000 ]; then rm -rf "/tmp/hyperframes-extract-cache-$(id -u)" 2>/dev/null || true; log "Temp space low · cleared the render cache before $slug"; fi
log "Rendering · $slug"
( cd "$R" && rm -f renders/raw.mp4 && mkdir -p renders && timeout 1500 npx -y hyperframes render --fps 30 --quality delivery --output renders/raw.mp4 >/dev/null 2>&1 )
rm -rf "/tmp/hyperframes-extract-cache-$(id -u)" 2>/dev/null || true   # 10-16: HyperFrames' frame cache grew to 3.8 GB in RAM-backed /tmp and broke a render — renders are serialised (render.lock), so clear it after each one
# audit C2/H7 (10-15): a render that exits 0 but comes out SHORT must fail (never ship a reel without its outro), and the final file
# appears only when complete (a kill mid-mux used to leave a broken master that the factory read as "ready to queue")
dv=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$R/renders/raw.mp4"); da=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$R/assets/audio/final.wav")
python3 -c "import sys; v,a=float(sys.argv[1]),float(sys.argv[2]); sys.exit(0 if v >= a-0.5 else 1)" "$dv" "$da" || { log "Render too short · $slug · video ${dv}s vs audio ${da}s"; echo "render too short: $dv vs $da" >&2; exit 1; }
ffmpeg -loglevel error -y -i "$R/renders/raw.mp4" -i "$R/assets/audio/final.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart -f mp4 "$OUT.part"
mv "$OUT.part" "$OUT"
rm -f "$R/renders/raw.mp4" "$R/assets/bg.mp4"; rm -rf ~/.cache/hyperframes/history/*   # the cut film (~600 MB) is re-cut by every render; keeping it filled the disk 10-14
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT"); S=$(mktemp -d)
for f in 0.15 0.4 0.65 0.88; do t=$(python3 -c "print(round($D*$f,2))"); ffmpeg -loglevel error -y -ss "$t" -i "$OUT" -frames:v 1 -vf scale=270:480 "$S/$f.png"; done
ffmpeg -loglevel error -y -i "$S/0.15.png" -i "$S/0.4.png" -i "$S/0.65.png" -i "$S/0.88.png" -filter_complex hstack=4 "${OUT%.mp4}-frames.png"; rm -rf "$S"
log "Rendered · $slug · ${D%.*} s"; echo "done $OUT ($D s)"
