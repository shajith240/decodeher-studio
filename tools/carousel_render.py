"""Render a carousel spec (brain/content/carousels/<slug>.json) to 1080x1350 PNG slides in deliverables/carousels/<slug>/.
Format (owner 10-19, copied from @manly_pinnacle's winning layout, our brand): slide 1 = photo fading to black + capitals headline
with [bracketed] words in gold; slides 2+ = plain dark text cards with our bronze-bust avatar, numbered bold points.
Usage: uv run -q --with playwright python tools/carousel_render.py brain/content/carousels/<slug>.json"""
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
.cover .ph {{ position: absolute; inset: 0 0 auto 0; height: 1000px; background-size: cover }}
.cover .fade {{ position: absolute; left: 0; right: 0; top: 560px; height: 460px; background: linear-gradient(180deg, rgba(15,6,8,0), #0f0608 92%) }}
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
.close {{ margin-top: auto; padding-top: 34px; border-top: 2px solid rgba(201,164,92,.45); font: 600 46px/1.3 ZS, sans-serif; color: #e8c372 }}
"""
def headline(t): return re.sub(r"\[([^\]]+)\]", lambda m: "<b>" + m.group(1).replace(" ", "&nbsp;") + "</b>", e(t))   # gold phrases never break across lines
pages = []
c = spec["cover"]
pages.append(f'<div class="cover"><div class="ph" style="background-image:url(file://{ROOT}/{c["image"]});background-position:{c.get("focus","50% 30%")}"></div>'
             f'<div class="fade"></div><div class="txt"><h1>{headline(c["headline"])}</h1>' + (f'<div class="sub">{e(c["sub"])}</div>' if c.get("sub") else "") + "</div></div>")
for i, pts in enumerate(spec["slides"]):
    last = i == len(spec["slides"]) - 1
    body = "".join(f'<div class="pt"><h2>{e(h)}</h2><p>{e(p)}</p></div>' for h, p in pts)
    pages.append(f'<div class="card"><div class="who"><img src="{LOGO}"><div><b>DecodeHer</b><span>@thedecodeher</span></div></div>{body}'
                 + (f'<div class="close">{e(spec["closing"])}</div>' if last and spec.get("closing") else "") + "</div>")
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=CHROME); pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i, body in enumerate(pages, 1):
            hf = f"{OUT}/.slide.html"; open(hf, "w").write(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
            await pg.goto(f"file://{hf}"); await pg.wait_for_load_state("load")
            await pg.evaluate("document.fonts.ready"); await pg.wait_for_timeout(250)
            over = await pg.evaluate("document.body.scrollHeight > 1350 || [...document.querySelectorAll('.card')].some(c => c.scrollHeight > 1350)")
            await pg.screenshot(path=f"{OUT}/{i:02d}.png"); print(f"{i:02d}.png{'  OVERFLOW' if over else ''}")
        await b.close()
    open(f"{OUT}/caption.txt", "w").write(spec.get("caption", "")); os.path.exists(f"{OUT}/.slide.html") and os.remove(f"{OUT}/.slide.html")
asyncio.run(main())
