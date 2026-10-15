#!/usr/bin/env bash
# Reel cover in the competitor style the owner showed (10-15, Zoltium's grid): one frame of OUR OWN illustrated clip, toned to a
# single colour, paper grain + vignette, one bold italic serif line in the middle. No generated images (owner: "AI slop").
# Usage: tools/make_cover.sh reels/<reel> <shot nn> <0-1 position in the shot> "<Title line>" <tint hex>   →   deliverables/covers/<reel>.jpg
set -euo pipefail; cd "$(dirname "$0")/.."; R="$1"; n="$2"; pos="$3"; title="$4"; tint="${5:-#3b1d6e}"; slug=$(basename "$R")
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT; mkdir -p deliverables/covers
seg="$R/clips/seg/$n.mp4"; d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$seg")
ffmpeg -loglevel error -y -ss "$(python3 -c "print($d*$pos)")" -i "$seg" -frames:v 1 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" "$T/f.png"
cp "$R/assets/brand/paper_grain.png" "$T/grain.png"
t=$(python3 -c "import html,sys; print(html.escape(sys.argv[1]))" "$title")
cat > "$T/c.html" <<H
<!doctype html><meta charset="utf-8"><link href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Text:ital,wght@1,400&family=Playfair+Display:ital,wght@1,700&display=block" rel="stylesheet">
<style>html,body{margin:0;width:1080px;height:1920px;background:#000;overflow:hidden}
.f{position:absolute;inset:0;background:url(f.png) center/cover;filter:grayscale(1) contrast(1.18) brightness(.9)}
.tone{position:absolute;inset:0;background:$tint;mix-blend-mode:color}
.deep{position:absolute;inset:0;background:$tint;mix-blend-mode:multiply;opacity:.35}
.grain{position:absolute;inset:0;background:url(grain.png) center/cover;mix-blend-mode:overlay;opacity:.55}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse 75% 62% at 50% 45%,rgba(0,0,0,0) 35%,rgba(0,0,0,.82) 100%)}
.band{position:absolute;left:0;right:0;top:640px;height:420px;background:radial-gradient(ellipse 70% 50% at 50% 50%,rgba(0,0,0,.45),rgba(0,0,0,0))}
h1{position:absolute;left:80px;right:80px;top:700px;margin:0;text-align:center;color:#fff;font:italic 700 84px/1.02 'Playfair Display',serif;letter-spacing:-.01em;
 text-shadow:0 3px 0 rgba(0,0,0,.55),0 0 22px rgba(0,0,0,.85),0 0 4px #000}</style>
<div class="f"></div><div class="tone"></div><div class="deep"></div><div class="grain"></div><div class="vig"></div><div class="band"></div><h1>$t</h1>
H
timeout 40 ~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome --headless=new --no-sandbox --allow-file-access-from-files --hide-scrollbars \
  --virtual-time-budget=9000 --window-size=1080,1920 --screenshot="$T/out.png" "file://$T/c.html" >/dev/null 2>&1
ffmpeg -loglevel error -y -i "$T/out.png" -q:v 2 "deliverables/covers/$slug.jpg" && echo "deliverables/covers/$slug.jpg"
