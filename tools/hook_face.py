"""Where is the face in a reel's AI-woman hook clip, in page pixels (1080x1920)? Prints JSON {"top": y0, "bottom": y1} or {}.
Used by tools/fill_page.py for reels with reel.json "hookText": the text hook sits above or below the face, never on it (owner 10-26)."""
import json, os, subprocess, sys
import cv2
R = sys.argv[1]; cfg = json.load(open(f"{R}/reel.json")); hk = cfg.get("hookClip") or {}
src = os.path.join(R, hk.get("file", "")); boxes = []
cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
for dt in (0.2, 0.8, 1.4, 2.0):
    f = f"/tmp/hook_face_{os.getpid()}.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(float(hk.get("start", 0)) + dt), "-i", src, "-frames:v", "1", "-pix_fmt", "yuvj420p", f], capture_output=True)
    im = cv2.imread(f)
    if im is None: continue
    h, w = im.shape[:2]; fs = cas.detectMultiScale(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), 1.1, 6, minSize=(60, 60))
    if not len(fs): continue
    x, y, fw, fh = max(fs, key=lambda r: r[2] * r[3]); s = max(1080 / w, 1920 / h); oy = (h * s - 1920) / 2
    boxes.append(((y - 0.45 * fh) * s - oy, (y + 1.3 * fh) * s - oy))   # hair to chin
print(json.dumps({"top": round(min(b[0] for b in boxes)), "bottom": round(max(b[1] for b in boxes))} if boxes else {}))
