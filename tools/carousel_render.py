"""Render a carousel spec (brain/content/carousels/<slug>.json) to 1080x1350 PNG slides in deliverables/carousels/<slug>/.
Format (owner 10-19, copied from @manly_pinnacle's winning layout, our brand): slide 1 = photo fading to black + capitals headline
with [bracketed] words in gold; slides 2+ = plain dark text cards with our bronze-bust avatar, numbered bold points.
Usage: uv run -q --with playwright --with opencv-python-headless==4.10.0.84 python tools/carousel_render.py brain/content/carousels/<slug>.json"""
import asyncio, html, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1243/chrome-linux64/chrome")
spec = json.load(open(sys.argv[1])); OUT = f"{ROOT}/deliverables/carousels/{spec['slug']}"; os.makedirs(OUT, exist_ok=True)
F = f"file://{ROOT}/site/fonts"; LOGO = f"file://{ROOT}/site/img/logo.jpg"
def e(s):   # typographic quotes/apostrophes (straight ones look cheap on a slide)
    s = re.sub(r"(\w)'", "\\1’", s); s = re.sub(r"'(\w)", "‘\\1", s); s = re.sub(r'"(\S)', "“\\1", s); s = s.replace('"', "”")
    return html.escape(s, quote=False)
CSS = f"""
@font-face {{ font-family: ZX; src: url({F}/ZalandoSansExpanded-500.woff2) }}
@font-face {{ font-family: ZS; src: url({F}/ZalandoSans-400.woff2); font-weight: 400 }}
@font-face {{ font-family: ZS; src: url({F}/ZalandoSans-500.woff2); font-weight: 500 }}
@font-face {{ font-family: ZS; src: url({F}/ZalandoSans-600.woff2); font-weight: 600 }}
* {{ margin: 0; padding: 0; box-sizing: border-box }}
html, body {{ width: 1080px; height: 1350px; overflow: hidden; background: #0f0608 }}
.cover {{ position: relative; width: 1080px; height: 1350px }}
.cover #ph {{ position: absolute; left: 0; top: 0; width: 1080px }}
.cover .fade {{ position: absolute; left: 0; right: 0; top: 560px; height: 460px; background: linear-gradient(180deg, rgba(15,6,8,0), #0f0608 88%) }}
.cover .below {{ position: absolute; left: 0; right: 0; bottom: 0; background: #0f0608 }}
.cover .txt {{ position: absolute; left: 70px; right: 70px; bottom: 120px; text-align: center }}
.cover h1 {{ font: 500 76px/1.12 ZX, sans-serif; text-transform: uppercase; color: #f6efe3; letter-spacing: .005em; text-wrap: balance }}
.cover h1 b {{ font-weight: 500; color: #e2bd6a }}
.cover .sub {{ margin-top: 22px; font: 500 34px/1.2 ZX, sans-serif; text-transform: uppercase; color: #f6efe3 }}
.card {{ width: 1080px; height: 1350px; padding: 120px 88px 100px; display: flex; flex-direction: column; background: radial-gradient(120% 70% at 50% 0%, #241015 0%, #0f0608 65%) }}
.who {{ display: flex; align-items: center; gap: 24px; margin-bottom: 64px }}
.who img {{ width: 104px; height: 104px; border-radius: 50%; object-fit: cover; border: 2px solid rgba(201,164,92,.6) }}
.who b {{ display: block; font: 600 40px/1.2 ZS, sans-serif; color: #fff }}
.who span {{ font: 500 30px/1.2 ZS, sans-serif; color: rgba(255,255,255,.62) }}
.pt {{ margin-bottom: 60px }}
.pt h2 {{ font: 600 54px/1.22 ZS, sans-serif; color: #e8c372; margin-bottom: 18px; letter-spacing: -.005em }}
.pt p {{ font: 500 47px/1.38 ZS, sans-serif; color: #fbf7f0; letter-spacing: -.003em }}
.card.solo .pt {{ margin: auto 0 }} .card.solo .pt h2 {{ font-size: 62px; margin-bottom: 28px }} .card.solo .pt p {{ font-size: 54px; line-height: 1.4 }}
.close {{ margin-top: auto; padding-top: 34px; border-top: 2px solid rgba(201,164,92,.45); font: 600 46px/1.3 ZS, sans-serif; color: #e8c372 }}
"""
def headline(t): return re.sub(r"\[([^\]]+)\]", lambda m: "<b>" + m.group(1).replace(" ", "&nbsp;") + "</b>", e(t))   # gold phrases never break across lines
pages = []
c = spec["cover"]
# owner 10-19: highlights carry the promise — at most 2, ONE word each, never next to each other (number + key action/outcome)
_hl = re.findall(r"\[([^\]]+)\]", c["headline"])
if len(_hl) > 2 or any(" " in w.strip() for w in _hl) or re.search(r"\]\s*\[", c["headline"]):
    sys.exit(f"cover headline highlights break the rule (max 2 single words, not adjacent): {c['headline']}")
pages.append(f'<div class="cover"><img id="ph" src="file://{ROOT}/{c["image"]}">'
             f'<div class="fade" id="fade"></div><div class="below" id="below"></div><div class="txt"><h1>{headline(c["headline"])}</h1>' + (f'<div class="sub">{e(c["sub"])}</div>' if c.get("sub") else "") + "</div></div>")
for i, pts in enumerate(spec["slides"]):
    last = i == len(spec["slides"]) - 1
    body = "".join(f'<div class="pt"><h2>{e(h)}</h2><p>{e(p)}</p></div>' for h, p in pts)
    pages.append(f'<div class="card{" solo" if len(pts) == 1 else ""}"><div class="who"><img src="{LOGO}"><div><b>DecodeHer</b><span>@thedecodeher</span></div></div>{body}'
                 + (f'<div class="close">{e(spec["closing"])}</div>' if last and spec.get("closing") else "") + "</div>")
def face_box(img):
    """10-19 owner: the headline must never cover the girl's face — find the face (largest frontal face, OpenCV) in source pixels."""
    try:
        import cv2
        g = cv2.cvtColor(cv2.imread(img), cv2.COLOR_BGR2GRAY)
        f = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml").detectMultiScale(g, 1.1, 5, minSize=(60, 60))
        if len(f): x, y, w, h = max(f, key=lambda r: r[2] * r[3]); return [int(x), int(y), int(w), int(h)]
    except Exception as ex: print("face detection unavailable:", ex)
    return None

# place the photo so the face (incl. chin) sits above the headline with a gap; shrink the headline if the photo can't move enough
PLACE = """async (face) => {
  // 10-19 owner: the face is centred in the photo area above the headline, the whole head (with hair) stays in frame,
  // the chin never reaches the text. The photo zooms a little (max 1.5x) when that is the only way to centre the face.
  const img = document.getElementById('ph'); if (!img) return null; await img.decode().catch(() => {});
  const h1 = document.querySelector('.cover h1'), t = document.querySelector('.cover .txt').getBoundingClientRect().top;
  const area = t - 40, W0 = img.naturalWidth, H0 = img.naturalHeight;
  let z = 1, s, top, left;
  for (; z <= 1.25; z += 0.05) {
    s = 1080 / W0 * z; const W = W0 * s, H = H0 * s;
    if (!face) { left = (1080 - W) / 2; top = Math.min(0, Math.max(area - H, -0.12 * H)); break; }
    const [fx, fy, fw, fh] = face.map((v) => v * s), headTop = fy - 0.45 * fh, chin = fy + 1.25 * fh, cx = fx + fw / 2;
    top = area * 0.48 - (headTop + chin) / 2;                       // head centred a touch above the middle of the photo area
    top = Math.min(top, 40 - headTop);                              // hair stays in frame
    top = Math.max(top, -(chin - (area - 20)));                     // ...but the chin stays above the text
    top = Math.min(0, Math.max(top, area + 80 - H));                // the photo covers the area
    left = Math.min(0, Math.max(540 - cx, 1080 - W));               // face centred left-right as far as the photo allows
    if (top + headTop >= 20 && top + chin <= area - 10) break;   // whole head in frame + chin clear: no more zoom (centring left-right is a bonus)
  }
  if (z > 1.25 && face) {   // nothing fully fits (hair already cut in the source): fall back to no zoom, best vertical placement
    z = 1; s = 1080 / W0; const H = H0 * s, [fx, fy, fw, fh] = face.map((v) => v * s), headTop = fy - 0.45 * fh, chin = fy + 1.25 * fh;
    top = Math.min(0, Math.max(Math.min(area * 0.48 - (headTop + chin) / 2, 40 - headTop), -(chin - (area - 20)), area + 80 - H)); left = 0;
  }
  img.style.width = (W0 * s) + 'px'; img.style.top = top + 'px'; img.style.left = left + 'px';
  const fade = document.getElementById('fade'); fade.style.top = Math.max(0, t - 380) + 'px'; fade.style.height = '420px';
  document.getElementById('below').style.top = (t + 40) + 'px';
  const lines = Math.round(h1.getBoundingClientRect().height / parseFloat(getComputedStyle(h1).lineHeight));
  return { zoom: +z.toFixed(2), top: Math.round(top), left: Math.round(left), lines, ...(lines > 4 ? { warn: 'title over 4 lines: write it shorter' } : {}) };
}"""

async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i, body in enumerate(pages, 1):
            hf = f"{OUT}/.slide.html"; open(hf, "w").write(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
            await pg.goto(f"file://{hf}"); await pg.wait_for_load_state("load")
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            if i == 1: print("cover placement:", await pg.evaluate(PLACE, face_box(os.path.join(ROOT, spec["cover"]["image"]))))
            over = await pg.evaluate("[...document.querySelectorAll('.card')].some(c => c.scrollHeight > 1350)")
            await pg.screenshot(path=f"{OUT}/{i:02d}.png"); print(f"{i:02d}.png{'  OVERFLOW' if over else ''}")
        await b.close()
    open(f"{OUT}/caption.txt", "w").write(spec.get("caption", "")); os.path.exists(f"{OUT}/.slide.html") and os.remove(f"{OUT}/.slide.html")
asyncio.run(main())
