"""Royal reel cover (owner 10-15, version "B"): the reel's own clip, faint, under the brand's royal crimson gradient, with a
two-level hook in gold Rosarivo — a small letter-spaced KICKER that names the situation, a thin gold rule, then the HEADLINE.
Laid out for all three places a 9:16 cover is seen:
  - profile grid: Instagram shows only the centre 3:4 (y 240-1680) → every element sits inside it
  - feed: caption + buttons cover the bottom ~25 % and the icons the right edge → the hook sits above the optical centre, 800 px wide
  - small size: headline 112 px, max 2 balanced lines, no widow words
No generated images (owner: AI covers looked fake).
Usage: python3 tools/make_royal_cover.py reels/<reel> "KICKER" "Headline. (| = line break)" [shot nn] [0-1 position]  →  deliverables/covers-royal/<reel>.jpg"""
import glob, html, os, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
R, kicker, head = sys.argv[1].rstrip("/"), sys.argv[2], sys.argv[3]
shot = sys.argv[4] if len(sys.argv) > 4 else "00"; pos = float(sys.argv[5]) if len(sys.argv) > 5 else 0.4
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
out = f"deliverables/covers-royal/{os.path.basename(R)}.jpg"; os.makedirs(os.path.dirname(out), exist_ok=True)

with tempfile.TemporaryDirectory() as T:
    seg = f"{R}/clips/seg/{shot}.mp4"
    if not os.path.exists(seg): seg = (sorted(glob.glob(f"{R}/clips/cand/{shot}/*.mp4")) or sorted(glob.glob(f"{R}/clips/cand/*/*.mp4")))[0]   # not cut yet: a raw clip of that shot
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", seg]))
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{d * pos:.2f}", "-i", seg, "-frames:v", "1", "-vf",
                    "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,hue=s=0", f"{T}/f.png"], check=True)
    open(f"{T}/c.html", "w").write(f"""<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Rosarivo:ital@0;1&display=block" rel="stylesheet">
<style>html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0c0204}}
.bg{{position:absolute;inset:0;background:radial-gradient(ellipse 70% 46% at 50% 45%,#6a121f 0%,#3a0a12 45%,#0c0204 100%)}}
.f{{position:absolute;inset:0;background:url(f.png) center/cover;opacity:.34;mix-blend-mode:luminosity}}
.tint{{position:absolute;inset:0;background:radial-gradient(ellipse 75% 50% at 50% 45%,rgba(106,18,31,.5),rgba(12,2,4,.93));mix-blend-mode:multiply}}
.blk{{position:absolute;left:140px;width:800px;top:860px;transform:translateY(-50%);text-align:center;font-family:Rosarivo,serif}}
.k{{font-size:36px;letter-spacing:.24em;line-height:1.6;color:#c9a45c;text-wrap:balance;text-transform:uppercase}}
.r{{width:110px;height:1.5px;margin:42px auto 40px;background:linear-gradient(90deg,transparent,#c9a45c,transparent)}}
.h{{font-size:112px;line-height:1.34;color:#ecd6a3;text-wrap:balance;text-shadow:0 2px 26px rgba(0,0,0,.5)}}
.m{{position:absolute;left:0;right:0;top:1350px;text-align:center;font-family:Rosarivo,serif;font-size:24px;letter-spacing:.44em;color:#c9a45c;opacity:.85}}
</style><div class="bg"></div><div class="f"></div><div class="tint"></div>
<div class="blk"><div class="k">{html.escape(kicker)}</div><div class="r"></div><div class="h">{"<br>".join(html.escape(x.strip()) for x in head.split("|"))}</div></div>
<div class="m">THE&nbsp;DECODE&nbsp;HER</div>""")
    subprocess.run([CHROME, "--headless=new", "--virtual-time-budget=9000", "--hide-scrollbars", "--window-size=1080,1920",
                    f"--screenshot={T}/c.png", f"file://{T}/c.html"], check=True, capture_output=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f"{T}/c.png", "-q:v", "2", out], check=True)
print(out)
