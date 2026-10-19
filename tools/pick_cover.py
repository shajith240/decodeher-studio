"""Pick a carousel cover whose LOOK fits the carousel's message (owner 10-19: "girls to avoid" gets a baddie / attitude look, not a
sweet girl; "marry her" gets a warm, wholesome one). Never a dark-psychology clip.
Candidates: the owner's covers (library/carousel-covers/*.jpg, sent on Telegram — preferred) + the AI-woman hook pool
(library/hook-pool/ai/*.mp4). One cheap Haiku call reads the title + points and the candidates' descriptions and picks one;
covers used in the last 10 carousels are skipped. For a clip, the frame with the biggest clear face (OpenCV) is used.
Usage: uv run -q --with "opencv-python-headless==4.10.0.84" python tools/pick_cover.py brain/content/carousels/<slug>.json
Writes brain/content/carousels/<slug>-cover.jpg and sets the spec's cover.image."""
import glob, json, os, re, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
SPEC = sys.argv[1]; spec = json.load(open(SPEC)); USED = "brain/content/carousels/cover-usage.json"
used = json.load(open(USED)) if os.path.exists(USED) else []
recent = {u["src"] for u in used[-10:] if u.get("slug") != spec["slug"]}

cands = []
for j in sorted(glob.glob("library/carousel-covers/*.json")):
    d = json.load(open(j)); img = j[:-5] + ".jpg"
    if os.path.exists(img) and img not in recent: cands.append({"name": os.path.basename(img), "src": img, "kind": "owner", "look": d.get("description", ""), "tags": d.get("tags", [])})
for j in sorted(glob.glob("library/hook-pool/ai/*.json")):
    d = json.load(open(j)); mp4 = j[:-5] + ".mp4"
    if os.path.exists(mp4) and mp4 not in recent: cands.append({"name": os.path.basename(mp4), "src": mp4, "kind": "ai", "look": d.get("ai_description") or d.get("description", ""), "tags": d.get("tags", [])})
if not cands: sys.exit("no cover candidates")

title = re.sub(r"[\[\]]", "", spec["cover"]["headline"]); pts = "; ".join(h for sl in spec["slides"] for h, _ in sl)
rows = "\n".join(f'{c["name"]} | {"OWNER PICK" if c["kind"] == "owner" else "pool"} | {c["look"][:160]} | {", ".join(c["tags"][:6])}' for c in cands)
prompt = ("Choose the cover photo for an Instagram carousel for men about dating. The woman's LOOK must match the carousel's message: "
          "warnings / red flags / girls to avoid → bold, edgy, attitude, 'baddie', provocative energy; marriage / green flags / a good "
          "woman → warm, wholesome, soft, traditional; attraction / signs she likes you → flirty, playful, inviting eye contact. Prefer an "
          "OWNER PICK when it fits as well as a pool one. Reply with JSON only: {\"pick\": \"<exact name>\", \"why\": \"<short>\"}.\n\n"
          f"Title: {title}\nPoints: {pts}\n\nCandidates (name | source | look | tags):\n{rows}")
import cv2
_cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
def has_face(src):   # 10-19 owner: covers show the girl's FACE (like the hook) — a back / silhouette clip is never a cover
    for t in (0.5, 1.5, 2.5, 3.5):
        f = f"/tmp/pick_face_{os.getpid()}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", src, "-frames:v", "1", "-pix_fmt", "yuvj420p", "-q:v", "3", f], capture_output=True)
        im = cv2.imread(f)
        if im is not None and len(_cas.detectMultiScale(cv2.cvtColor(im, cv2.COLOR_BGR2GRAY), 1.1, 6, minSize=(80, 80))): return True
    return False
for _try in range(4):
    out = subprocess.run([os.environ.get("CLAUDE_BIN", "claude"), "-p", prompt, "--model", "haiku", "--output-format", "text"], capture_output=True, text=True, timeout=300).stdout
    try: j = json.loads(re.search(r"\{.*\}", out, re.S).group(0)); c = next(x for x in cands if x["name"] == j["pick"])
    except Exception: sys.exit(f"no valid pick: {out[:300]}")
    if c["kind"] == "owner" or has_face(c["src"]): break
    print(f"no clear face in {c['name']}, asking again"); cands = [x for x in cands if x is not c]
    rows = "\n".join(f'{x["name"]} | {"OWNER PICK" if x["kind"] == "owner" else "pool"} | {x["look"][:160]} | {", ".join(x["tags"][:6])}' for x in cands)
    prompt = prompt.split("Candidates (name")[0] + f"Candidates (name | source | look | tags):\n{rows}"

dst = f"brain/content/carousels/{spec['slug']}-cover.jpg"
if c["kind"] == "owner":
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", c["src"], "-q:v", "2", dst], check=True)
else:   # 10-19: frames with a clear, whole face → numbered sheet → the AI picks the EXPRESSION that fits the message
    import cv2
    cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml"); keep = []
    tmpd = f"/tmp/pick_cover_{os.getpid()}"; os.makedirs(tmpd, exist_ok=True)
    for t in [x * 0.4 for x in range(1, 26)]:
        f = f"{tmpd}/{len(keep):02d}.jpg"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", c["src"], "-frames:v", "1", "-pix_fmt", "yuvj420p", "-q:v", "2", f], capture_output=True)
        im = cv2.imread(f)
        if im is None: continue
        H = im.shape[0]; g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY); fs = cas.detectMultiScale(g, 1.1, 6, minSize=(80, 80))
        if not len(fs): continue
        x, y, w, h = max(fs, key=lambda r: r[2] * r[3])
        if y < 0.06 * H or h > 0.42 * H or cv2.Laplacian(g, cv2.CV_64F).var() < 60: continue   # head cut at the top, too close, or blurry
        keep.append((t, f))
        if len(keep) >= 12: break
    if not keep: sys.exit("no clear face frame in that clip")
    sheet = f"{tmpd}/sheet.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{tmpd}/%02d.jpg", "-frames:v", "1", "-vf",
                    "scale=240:-1,drawtext=text='%{eif\\:n\\:d}':x=8:y=8:fontsize=36:fontcolor=yellow:box=1:boxcolor=black@0.6,tile=6x2", sheet], capture_output=True)
    ask = (f"Read the image {sheet}: numbered frames (0, 1, 2…) of one woman. Pick the frame whose EXPRESSION best fits the cover of a "
           f"carousel titled \"{title}\" ({j.get('why', '')}). Eyes open, whole head in frame, not mid-blink or mid-word. "
           'Reply with JSON only: {"frame": <number>}')
    o2 = subprocess.run([os.environ.get("CLAUDE_BIN", "claude"), "-p", ask, "--model", "haiku", "--allowedTools", "Read", "--output-format", "text"],
                        capture_output=True, text=True, timeout=300).stdout
    try: n = int(json.loads(re.search(r"\{.*\}", o2, re.S).group(0))["frame"]); t = keep[n][0]
    except Exception: t = keep[0][0]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", c["src"], "-frames:v", "1", "-pix_fmt", "yuvj420p", "-q:v", "2", dst], check=True)
spec["cover"]["image"] = dst; spec["cover"]["picked"] = {"src": c["src"], "why": j.get("why", "")}
json.dump(spec, open(SPEC, "w"), indent=1, ensure_ascii=False)
used = [u for u in used if u.get("slug") != spec["slug"]] + [{"slug": spec["slug"], "src": c["src"]}]
json.dump(used, open(USED, "w"), indent=1)
print(f"{spec['slug']}: {c['name']} — {j.get('why', '')}")
