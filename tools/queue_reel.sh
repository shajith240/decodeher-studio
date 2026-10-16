#!/usr/bin/env bash
# Turn a finished clip reel into a queued Instagram post (owner 10-14: "I want the content to post throughout the week"):
# a posting copy under 30 MB (the relay's limit; Instagram recompresses to ~3-5 Mbps anyway), the caption from
# brain/content/drafts/week2-captions.json + the track's CC-BY credit, then `ig_queue.js add` into the next free slot.
# Usage: tools/queue_reel.sh reels/<reel>
set -euo pipefail; R="$1"; cd "$(dirname "$0")/.."; slug="$(basename "$R")"; Q=deliverables/queue; mkdir -p "$Q"
# never twice: if this reel already has a caption in the queue folder, it is queued — stop
if [ -f "logs/queued/$slug" ]; then echo "already queued: $slug"; exit 0; fi   # marker written only after the relay confirmed
# audit 10-15 H1: never write the queue while a post is going live — wait out 3 min before to 12 min after each slot (08:30, 18:30, 22:00 IST — slots changed 10-16, keep in sync with tools/ig_queue.js SLOTS)
while python3 -c "
import datetime as d; n=d.datetime.now(d.timezone(d.timedelta(hours=5,minutes=30))); m=n.hour*60+n.minute
raise SystemExit(0 if any(s-3<=m<=s+12 for s in (8*60+30, 18*60+30, 22*60)) else 1)"; do sleep 30; done
# audit M4 (10-15): read the relay ONCE; if it can't be read, stop — an empty answer used to look like "not booked" → duplicate post
# 10-15: Cloudflare refuses any single upload over 32 MiB (a 46 s reel came out at 34.4 MB and failed twice). The posting copy's
# bitrate cap is set from the reel's length so the file lands under ~28 MB; the size is checked again after encoding.
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "deliverables/week-2/$slug.mp4" 2>/dev/null || echo 40)
VMAX=$(python3 -c "import sys; d=float(sys.argv[1]); print(min(6000, int(28*8*1024*1024/d/1000 - 200)))" "$DUR")k
IDS=$(node tools/ig_queue.js ids) || { echo "relay unreachable, not booking $slug" >&2; exit 1; }
[ -n "$IDS" ] || { echo "relay returned nothing, not booking $slug" >&2; exit 1; }
last=$( { ls "$Q"/*-FINAL.mp4 "$Q"/booked/*-FINAL.mp4 2>/dev/null | sed 's|.*/||'; echo "$IDS" | awk '{print $NF}'; } | grep -o '^[0-9]*' | sort -n | tail -1 || true)   # 10-15: an EMPTY queue folder made this fail silently (pipefail)   # highest number so far (a removed
n=$(printf "%02d" $(( 10#${last:-1} + 1 )))                                                           # duplicate made a count-based one repeat)
title="$n-W2-$(echo "$slug" | cut -d- -f3- | cut -c1-28)"
# the relay is the truth: if it already holds this reel (a run died after the upload, before the marker), just write the marker
part="-W2-$(echo "$slug" | cut -d- -f3- | cut -c1-28)"
# the title card (0-2 s) is the cover when the reel has one
export THUMB_MS=$(python3 -c "import json,sys; print(600 if json.load(open(sys.argv[1])).get('titleCard') else 1500)" "$R/reel.json")
onrelay=$(echo "$IDS" | awk '$2=="queued"{print $NF}' | grep -- "^[0-9]*$part\$" | head -1 || true)
if [ -n "$onrelay" ] && python3 -c "import json,sys; sys.exit(0 if json.load(open(sys.argv[1])).get('requeue') else 1)" "$R/reel.json"; then
  # a RE-MADE reel (reel.json "requeue": owner 10-15 re-voice + new ending): swap the new video into its existing slot, same caption
  tmp=$(mktemp -d); trap 'rm -rf "$tmp"' EXIT
  ffmpeg -loglevel error -y -i "deliverables/week-2/$slug.mp4" -c:v libx264 -preset slow -crf 22 -tune grain -maxrate "$VMAX" -bufsize "$VMAX" -pix_fmt yuv420p \
    -profile:v high -c:a aac -b:a 160k -movflags +faststart "$tmp/$onrelay-FINAL.mp4"
  ffprobe -v error -show_entries format=duration -of csv=p=0 "$tmp/$onrelay-FINAL.mp4" | grep -q . || { echo "re-encode broken: $slug" >&2; exit 1; }
  node tools/ig_queue.js replace "$tmp" | tee /dev/stderr | grep -q "video replaced" || { echo "replace failed: $slug" >&2; exit 1; }
  mkdir -p "$Q/booked"; cp "$tmp/$onrelay-FINAL.mp4" "$Q/booked/$onrelay-FINAL.mp4"   # audit M8: never in the folder `add` uploads
  if [ "$THUMB_MS" = 600 ] && [ ! -f "deliverables/covers-royal/$slug.jpg" ]; then   # audit M3: a swap keeps the approved royal cover; frame only when there is none
    id=$(node tools/ig_queue.js ids 2>/dev/null | awk -v t="$onrelay" '$2=="queued" && $NF==t {print $1}' | head -1)
    [ -n "$id" ] && node tools/ig_queue.js cover "$id" frame=600 || true; fi
  python3 -c "import json,sys; p=sys.argv[1]; c=json.load(open(p)); c.pop('requeue',None); json.dump(c,open(p,'w'),indent=1,ensure_ascii=False)" "$R/reel.json"
  mkdir -p logs/queued; date "+%F %T" > "logs/queued/$slug"; echo "$(date +%H:%M:%S)  Re-made video swapped in · $onrelay" >> logs/activity.log; exit 0
fi
if echo "$IDS" | awk '{print $NF}' | grep -q -- "^[0-9]*$part\$"; then
  mkdir -p logs/queued; date "+%F %T" > "logs/queued/$slug"; echo "already on the relay: $slug"; exit 0; fi
python3 - "$slug" "$R" "$Q/$n-W2-$slug-caption.txt" <<'PY'
# owner 10-15 (brain/rules/script-and-hooks.md, VIEWS RULES): search-phrase first line · his situation · send/comment prompt ·
# "Follow … for more dating advice for men." · #datingadviceformen #datingtips + topic tags, NEVER more than 5 (Instagram cap)
import json, os, re, sys
slug, R, out = sys.argv[1:]; caps = json.load(open("brain/content/drafts/week2-captions.json")) if os.path.exists("brain/content/drafts/week2-captions.json") else {}
approved = f"brain/content/captions/{slug}.txt"   # owner-approved keyword-first caption (10-15 rewrite) wins over everything
if os.path.exists(approved):
    txt = open(approved).read().strip() + "\n"; assert len(re.findall(r"#\w+", txt)) <= 5
    cr = f"{R}/assets/audio/credit.txt"   # audit L3: the CC-BY music credit is required — add it if the approved caption lacks it
    if os.path.exists(cr) and "Music:" not in txt and open(cr).read().strip(): txt += f"\nMusic: {open(cr).read().strip()}\n"
    open(out, "w").write(txt); sys.exit(0)
c = json.load(open(f"{R}/reel.json")).get("caption") or {}
if c: hook, body, prompt, tags = c.get("hook", ""), c.get("body", ""), c.get("prompt", ""), c.get("tags", "")
else: hook, body, tags = caps[slug]; prompt = ""
base = ["#datingadviceformen", "#datingtips"]; weak = {"#psychology", "#relationships", "#modernromance", "#relationshipadvice", "#mensadvice", "#communication"}
extra = [t for t in dict.fromkeys(re.findall(r"#\w+", tags.lower())) if t not in base and t not in weak]
tags = " ".join(base + extra[:3])
credit = open(f"{R}/assets/audio/credit.txt").read().strip() if os.path.exists(f"{R}/assets/audio/credit.txt") else ""
lines = [hook.strip(), body.strip()] + ([""] + [prompt.strip()] if prompt.strip() else [""])
open(out, "w").write("\n".join(lines) + "\nFollow @thedecodeher for more dating advice for men.\n\n" + tags + "\n" + (f"\nMusic: {credit}\n" if credit else ""))
assert len(re.findall(r"#\w+", open(out).read())) <= 5
PY
# a run that dies half way (killed, disk full) must leave NOTHING behind: `ig_queue add` uploads every *-FINAL.mp4 in the folder,
# so a leftover file got booked as a second post on 10-14. Clean up on any exit until the relay has confirmed.
trap '[ -f "logs/queued/$slug" ] || rm -f "$Q/$title-FINAL.mp4" "$Q/$title.part.mp4" "$Q/$n-W2-$slug-caption.txt"' EXIT
ffmpeg -loglevel error -y -i "deliverables/week-2/$slug.mp4" -c:v libx264 -preset slow -crf 22 -tune grain -maxrate "$VMAX" -bufsize "$VMAX" -pix_fmt yuv420p \
  -profile:v high -c:a aac -b:a 160k -movflags +faststart -f mp4 "$Q/$title.part.mp4"
[ "$(stat -c %s "$Q/$title.part.mp4")" -lt 32000000 ] || { echo "posting copy too big for the relay: $(stat -c %s "$Q/$title.part.mp4") bytes" >&2; exit 1; }
mv "$Q/$title.part.mp4" "$Q/$title-FINAL.mp4"   # only a complete file ever carries the -FINAL name
out=$(node tools/ig_queue.js add "$Q" 2>&1); echo "$out" | grep -E "^\+|saved|⛔"
if echo "$out" | grep -q "^+ .*$title" && echo "$out" | grep -q "queue saved"; then
  mkdir -p logs/queued; date "+%F %T" > "logs/queued/$slug"; echo "$out" | grep "^+ .*$title" | sed "s/^+ /$(date +%H:%M:%S)  Queued · /" >> logs/activity.log
  cov="deliverables/covers-royal/$slug.jpg"   # owner 10-15: the approved royal cover (tools/make_royal_cover.py) on every post
  if [ ! -f "$cov" ]; then   # v3 reels: make it from reel.json coverKicker / coverHeadline (series + title)
    ck=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('coverKicker',''))" "$R/reel.json")
    ch=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('coverHeadline',''))" "$R/reel.json")
    [ -n "$ch" ] && python3 tools/make_royal_cover.py "$R" "$ck" "$ch" >/dev/null 2>&1 || true
  fi
  if [ -f "$cov" ]; then id=$(node tools/ig_queue.js ids 2>/dev/null | awk -v t="$title" '$2=="queued" && $NF==t {print $1}' | head -1)
    [ -n "$id" ] && node tools/ig_queue.js cover "$id" "$cov" >/dev/null && echo "$(date +%H:%M:%S)  Cover set · $title" >> logs/activity.log || echo "$(date +%H:%M:%S)  Cover NOT set · $title" >> logs/activity.log; fi
  # owner 10-15 ("clean them, I trust you"): once the relay holds the post, the 350 MB master goes; the 30 MB posting copy in $Q stays
  [ -s "$Q/$title-FINAL.mp4" ] && rm -f "deliverables/week-2/$slug.mp4"
  # audit M8 (10-15): a booked reel's files leave the folder `ig_queue add` uploads from, so a later add can never re-book it
  mkdir -p "$Q/booked"; mv -f "$Q/$title-FINAL.mp4" "$Q/$n-W2-$slug-caption.txt" "$Q/booked/" 2>/dev/null || true
else
  rm -f "$Q/$title-FINAL.mp4" "$Q/$n-W2-$slug-caption.txt"; echo "queue add failed for $slug" >&2; exit 1   # never leave a half-queued reel
fi
