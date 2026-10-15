"""Render a PREVIEW of one reel after an owner change request (cloud, manager-request.yml). Never queues anything.
  python3 tools/cloud/preview.py <slug>
reel.json "revoice": true → the voice is re-recorded (old timing + mix moved to <reel>/prev/), then mixed;
reel.json "remix": true   → re-mixed; otherwise the page is refilled (fill_page.py) and the reel re-rendered.
Out: deliverables/preview/<slug>.mp4 (master) and deliverables/preview/<slug>-tg.mp4 (≤ 48 MB for Telegram); prints the -tg path."""
import json, os, re, shutil, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")); os.chdir(ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))
import factory   # same stage commands as the factory (voice, mix); importing does not start it

slug = sys.argv[1] if len(sys.argv) > 1 else ""
if not re.fullmatch(r"[a-z0-9][a-z0-9-]{2,80}", slug) or not os.path.isdir(f"reels/{slug}"): sys.exit(f"no such reel: {slug!r}")
R, OUT = f"reels/{slug}", f"deliverables/preview/{slug}.mp4"; TG = OUT[:-4] + "-tg.mp4"
os.makedirs("deliverables/preview", exist_ok=True); os.makedirs("logs/reels", exist_ok=True)
logf = open(f"logs/reels/{slug}.log", "a"); logf.write(f"\n=== {time.strftime('%F %T')} preview\n"); logf.flush()

def run(cmd, **kw):
    logf.write("$ " + " ".join(cmd)[:400] + "\n"); logf.flush()
    subprocess.run(cmd, cwd=ROOT, stdout=logf, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, check=True, **kw)

cfg = json.load(open(f"{R}/reel.json")); revoice, remix = cfg.pop("revoice", False), cfg.pop("remix", False)
if revoice or remix:
    os.makedirs(f"{R}/prev", exist_ok=True)
    for f in (["assets/timing.js"] if revoice else []) + ["assets/audio/final.wav"]:
        if os.path.exists(f"{R}/{f}"): shutil.move(f"{R}/{f}", f"{R}/prev/{os.path.basename(f)}")
    json.dump(cfg, open(f"{R}/reel.json", "w"), indent=1, ensure_ascii=False)

tj = f"{R}/assets/timing.js"
if not (os.path.exists(tj) and '"words"' in open(tj).read()):
    factory.log(f"Recording voice · preview · {slug}")
    for c in factory.commands(os.path.abspath(R), "voice"): run(c)
if not os.path.exists(f"{R}/assets/audio/final.wav"):
    for c in factory.commands(os.path.abspath(R), "mix"): run(c)
else: run([sys.executable, "tools/fill_page.py", R])

factory.log(f"Rendering preview · {slug}")
run(["bash", "-c", f'exec 9>logs/render.lock; flock 9; bash tools/reel_finish.sh "{R}" "{OUT}"'])   # OUT ≠ deliverables/week-2: never queued

# Telegram bots may send at most 50 MB: a 720p copy with the bitrate set from the length (~46 MB target), checked after
dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", OUT]).strip())
for target_mb in (46, 30):
    kbps = max(800, min(5000, int(target_mb * 8 * 1024 / dur) - 160))
    run(["ffmpeg", "-loglevel", "error", "-y", "-i", OUT, "-vf", "scale=720:-2", "-c:v", "libx264", "-preset", "medium", "-b:v", f"{kbps}k",
         "-maxrate", f"{kbps}k", "-bufsize", f"{2 * kbps}k", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", TG])
    if os.path.getsize(TG) < 49 * 1024 * 1024: break
else: sys.exit(f"preview still too big for Telegram: {os.path.getsize(TG)} bytes")
print(TG)
