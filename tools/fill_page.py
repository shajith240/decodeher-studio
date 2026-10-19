"""Fill a clip reel's index.html with its own settings from reel.json (run after shot_times.py, before rendering):
the purple accent words and the white-flash reveal on the "drops" lines. Usage: python3 tools/fill_page.py <reel_dir>"""
import json, os, re, sys

R = os.path.abspath(sys.argv[1]); cfg = json.load(open(f"{R}/reel.json")); H = f"{R}/index.html"; h = open(H).read()
V3 = cfg.get("format") == "v3"   # growth plan 10-15 "v3" look (chat-bubble first frame, big title, 66 px captions, re-hook punch, 2.6 s outro); every other reel renders exactly as before
HI = cfg.get("lang") == "hi"   # Hinglish reel: captions/title card/bubble in Devanagari; every English reel renders exactly as before
HI_FAM = "'Rosarivo','Tiro Devanagari Hindi','Noto Serif Devanagari'"   # Latin loanwords stay in Rosarivo (brand), Devanagari glyphs fall through to Tiro
HI_LINK = "family=Rosarivo:ital@0;1&family=Tiro+Devanagari+Hindi:ital@0;1&family=Noto+Serif+Devanagari:wght@400"
esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
h = re.sub(r"const REEL_ACCENT = \[.*?\];", "const REEL_ACCENT = " + json.dumps([w.lower() for w in cfg.get("accent", [])]) + ";", h)
h = re.sub(r"\[T\.vo\[[\d, \]T.vo\[]*\]\]\.forEach", "[" + ", ".join(f"T.vo[{i}]" for i in cfg.get("drops", [])) + "].forEach", h)
# title card (owner 10-15, views rules): the reel's topic as a search phrase, top third, 0-2 s, and the cover frame (thumbMs 600)
TCARD_CSS = """ /*tcard*/#tcard{position:absolute;left:60px;width:960px;top:250px;text-align:center;color:#fff;font-weight:700;font-size:104px;line-height:1.02;letter-spacing:.04em;
   filter:drop-shadow(0 0 1px #0b0702) drop-shadow(0 0 1px #0b0702) drop-shadow(0 4px 4px rgba(0,0,0,.9)) drop-shadow(0 0 22px rgba(0,0,0,.75))}
 #tcard::after{content:"";display:block;width:140px;height:6px;margin:26px auto 0;background:#8B5CF6;border-radius:3px;box-shadow:0 0 18px rgba(139,92,246,.8)}
 #tcardHaze{position:absolute;left:0;top:150px;width:1080px;height:420px;background:radial-gradient(ellipse 62% 50% at 50% 50%,rgba(0,0,0,.6),rgba(0,0,0,0) 100%)}/*/tcard*/
"""
TCARD_TL = '  /*tcard*/tl.to(["#tcard", "#tcardHaze"], { opacity: 0, y: -12, duration: 0.3, ease: "power2.in" }, 2.0);/*/tcard*/\n'
h = re.sub(r" *<!--tcard-->.*?<!--/tcard-->\n?", "", h, flags=re.S)       # idempotent: drop the old card, then add the current one
h = re.sub(r" */\*tcard\*/.*?/\*/tcard\*/\n?", "", h, flags=re.S)
if cfg.get("titleCard") and not V3:   # v3 draws its own opening card (below)
    t = cfg["titleCard"].strip().upper().replace("&", "&amp;").replace("<", "&lt;")
    h = h.replace("</style>", TCARD_CSS + "</style>", 1)
    h = h.replace('<div id="caps"></div>', '<div id="caps"></div>\n  <!--tcard--><div id="tcardHaze"></div><div id="tcard">' + t + '</div><!--/tcard-->', 1)
    h = h.replace("  tl.set({}, {}, ", TCARD_TL + "  tl.set({}, {}, ", 1)
# owner 10-15 look "bw" (config.json reels.look): the reel body black and white (the outro stays in colour, owner 10-15) with Zoltium's captions — a small plain white serif,
# dead centre, sentence case, punctuation kept, hard swaps; no purple, no glow, no haze (brain/research/zoltium-story-visuals.md)
RC = (json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json"))).get("reels", {}))
od = None; h = re.sub(r"<!--look-->.*?<!--/look-->\n?", "", h, flags=re.S); h = re.sub(r" ?/\*look\*/.*?/\*/look\*/\n?", "", h, flags=re.S)
if RC.get("look") == "bw":
    # owner 10-15 brand: the bronze outro (owner's Flow clip, normal speed, mark cropped, own fade to black) + bronze watermark in EVERY reel
    import shutil, subprocess
    LB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "library/brand"); os.makedirs(f"{R}/assets/brand", exist_ok=True)
    for a, b in (("outro-bronze.mp4", "outro.mp4"), ("watermark.png", "watermark.png")): shutil.copyfile(f"{LB}/{a}", f"{R}/assets/brand/{b}")
    od = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/assets/brand/outro.mp4"]))
    h = re.sub(r'(id="outro"[^>]*data-duration=")[\d.]+', rf"\g<1>{od - 0.01:.2f}", h)
    F = RC.get("captionFont", "Rosarivo"); FS = RC.get("captionSizeV3", 66) if V3 else RC.get("captionSize", 60)   # v3: 66 px for phone readability
    h = h.replace("<style>", '<!--look--><link href="https://fonts.googleapis.com/css2?family=' + (HI_LINK if HI else F.replace(" ", "+") + ":ital@0;1")
                  + '&display=block" rel="stylesheet"><!--/look-->\n<style>', 1)
    FQ = HI_FAM if HI else "'" + F + "'"
    h = h.replace("</style>", " /*look*/.cap{font-family:" + FQ + ",serif;font-weight:400;font-size:" + str(FS) + "px;line-height:1.18;letter-spacing:0;top:"
                  + str(960 - FS * 0.6) + "px}\n .cap .w,.cap .a{color:#fff;filter:none;padding:0;text-shadow:0 0 3px rgba(0,0,0,.95),0 2px 10px rgba(0,0,0,.85),0 0 34px rgba(0,0,0,.7)}\n #haze{display:none}\n #wm{filter:grayscale(1);left:509px;top:1596px;height:78px}\n"
                  " #tcard{font-family:" + FQ + ",serif;font-weight:400;font-size:84px;line-height:1.15;letter-spacing:0;filter:none;text-shadow:0 2px 18px rgba(0,0,0,.55)}\n"
                  " #tcard::after{display:none}/*/look*/\n</style>", 1)
    # hard swap at the word (Zoltium), no blur-in, no purple bloom; keep the punctuation on the card
    h = re.sub(r"tl\.fromTo\(`#c\$\{k\}`, \{ opacity: 0, letterSpacing.*?\);", "tl.set(`#c${k}`, { opacity: 1 }, Math.max(0, t0 - 0.05));", h)
    h = re.sub(r"\n *if \(html\.includes\('class=\"w a\"'\)\) tl\.fromTo\(`#c\$\{k\} \.a`.*?\);", "", h)
    h = h.replace(r'.replace(/[,;:]$/, "").replace(/\.$/, "")', "")
    # owner 10-15 bug ("the a.m. caption is stuck" in w2-13): "a.m." became its own 0.08 s caption, its hide time (next start - 0.13)
    # fell BEFORE its show time, so it was hidden, then shown, and never hidden again. Now: a caption shorter than 0.35 s joins the
    # one before it, and every caption hides exactly when the next one shows — never before it was shown itself.
    h = h.replace("chunks.push(cur); cur = []; } });\n", "chunks.push(cur); cur = []; } });\n"
                  "  for (let k = chunks.length - 1; k > 0; k--) if (chunks[k].at(-1)[2] - chunks[k][0][1] < 0.35) chunks.splice(k - 1, 2, chunks[k - 1].concat(chunks[k]));   /*capfix*/\n", 1) if "/*capfix*/" not in h else h
    h = h.replace("const t0 = c[0][1], t1 = chunks[k + 1] ? chunks[k + 1][0][1] - 0.13 : c.at(-1)[2] + 0.4;",
                  "const t0 = c[0][1], t1 = chunks[k + 1] ? Math.max(chunks[k + 1][0][1] - 0.05, t0 + 0.1) : c.at(-1)[2] + 0.4;   /*capfix*/")
    # owner 10-15: "I can still see the image when it goes away" — no cross-fade into the outro: the reel dips fully to black,
    # THEN the bronze outro (full 9:16, its own 0.9 s fade to black at the end; owner: fades must be slow and smooth, never a cut) rises out of the dark
    h = h.replace("#outro{top:330px;height:1260px;opacity:0}", "#outro{top:0;height:1920px;opacity:0}")
    h = re.sub(r'tl\.fromTo\("#outro".*?\);', 'tl.fromTo("#outro", { opacity: 0, scale: 1.05 }, { opacity: 1, scale: 1, duration: 0.9, ease: "sine.out", immediateRender: false }, END + 0.05);', h)
    h = re.sub(r'tl\.to\("#bg", \{ opacity: 0, duration: [\d.]+(?:, ease: "[\w.]+")? \}, END - [\d.]+\);', 'tl.to("#bg", { opacity: 0, duration: 0.6, ease: "sine.inOut" }, END - 0.6);', h)
    h = re.sub(r'tl\.to\("#wm", \{ opacity: 0, duration: [\d.]+(?:, ease: "[\w.]+")? \}, END - [\d.]+\);', 'tl.to("#wm", { opacity: 0, duration: 0.6, ease: "sine.inOut" }, END - 0.6);', h)
    if cfg.get("titleCard"):   # the card in sentence case, like the captions
        tc = cfg["titleCard"].strip(); tc = tc[0].upper() + tc[1:].lower()
        h = re.sub(r'<div id="tcard">.*?</div>', '<div id="tcard">' + tc.replace("&", "&amp;").replace("<", "&lt;") + '</div>', h, count=1)
# ── v3 look (growth plan 10-15, brain/growth/growth-plan-2026-10-15.md "First frame"), only for reel.json "format": "v3" ──
# reel.json keys: "bubble" (her exact message, drawn as a phone chat bubble), "titleCard" (sentence case, under the bubble at ~2x size),
# "bubbleTime" (optional stamp, default 11:47 PM),
# "rehookAt" (line index, 0-based like "drops": a subtle zoom punch + faint flash when that line starts).
# The brighter first 3 s of the film is done in tools/clipcut.py (same flag). Markers <!--v3--> /*v3*/ keep this idempotent.
h = re.sub(r" *<!--v3-->.*?<!--/v3-->\n?", "", h, flags=re.S); h = re.sub(r" */\*v3\*/.*?/\*/v3\*/\n?", "", h, flags=re.S)
if V3:
    F = RC.get("captionFont", "Rosarivo"); title = (cfg.get("titleCard") or "").strip(); bubble = (cfg.get("bubble") or "").strip().strip('"“”')
    if title: title = title[0].upper() + title[1:].lower() if title.isupper() else title[0].upper() + title[1:]
    ts = 124 if len(title) <= 26 else 108 if len(title) <= 38 else 94           # max 2 balanced lines at ~2x the old 60 px title
    bs = 76 if len(bubble) <= 22 else 68 if len(bubble) <= 44 else 64          # her message, never under 64 px
    HOOKV = bool(cfg.get("hookClip"))   # 10-16 owner: no text on the woman during the hook — title in the top band, captions wait
    HOOK_END = None
    if HOOKV:   # 10-16 owner: the hook shot is 2.5-4 s (not chopped, not 7-10 s), ending where a sentence ends; clipcut.py uses the same point
        try:
            sh = json.load(open(f"{R}/shots.json"))
            import subprocess as _sp
            _cl = float(_sp.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", os.path.join(R, cfg["hookClip"]["file"])]).decode())
            _max = min(4.0, _cl - float(cfg["hookClip"].get("start", 0)) - 0.1)
            cands = [i for i in range(1, len(sh)) if sh[i]["q"] != "OUTRO" and 2.5 <= sh[i]["t"] <= _max]
            if not cands:   # 10-19: no shot starts in 2.5-4 s (first sentence ended early) — cut at the first one after 1.5 s, never leave it unset
                cands = [i for i in range(1, len(sh)) if sh[i]["q"] != "OUTRO" and 1.5 <= sh[i]["t"] <= _max]
            ends = [i for i in cands if re.search(r"[.?!…]['\"”]?\s*$", sh[i - 1].get("say", ""))]
            k = (ends or cands or [None])[-1]
            if k: HOOK_END = round(sh[k]["t"], 3)
            elif len(sh) > 1: HOOK_END = round(sh[1]["t"], 3)   # 10-19: no cut point — the hook runs the whole first shot, so captions wait for it
        except Exception as e: print("hook end: kept the default", e)
        if HOOK_END: cfg["hookEnd"] = HOOK_END
        else: cfg.pop("hookEnd", None)
        json.dump(cfg, open(f"{R}/reel.json", "w"), indent=1, ensure_ascii=False)
    css = (" /*v3*/" + ("#v3card{display:none !important} " if HOOKV else "") + "#v3card{position:absolute;left:70px;width:940px;top:" + ("150" if HOOKV else "560" if bubble else "700") + "px;display:flex;flex-direction:column;align-items:center;transform-origin:50% 40%}\n"
           " #v3meta{margin:0 0 14px 20px;font:500 30px/1 'Inter',sans-serif;letter-spacing:.01em;color:#d9d9de;text-shadow:0 1px 6px rgba(0,0,0,.85)}\n"
           " #v3meta b{font-weight:600;color:#fff}\n"
           " #v3msg{display:flex;flex-direction:column;align-items:flex-start;max-width:900px}\n"
           " #v3bub{max-width:900px;box-sizing:border-box;padding:28px 46px 32px;border-radius:54px 54px 54px 14px;background:#ededf1;color:#0d0d10;"
           "font:500 " + str(bs) + "px/1.16 'Inter',sans-serif;letter-spacing:-.012em;text-align:left;box-shadow:0 18px 50px rgba(0,0,0,.5),0 2px 6px rgba(0,0,0,.3)}\n"
           " #v3title{margin-top:" + ("56" if bubble else "0") + "px;width:940px;padding:22px 0 30px;background:none;text-align:center;text-wrap:balance;color:#fff;font:400 " + str(ts) + "px/1.08 " + (HI_FAM if HI else "'" + F + "'") + ",serif;"
           "text-shadow:0 0 3px rgba(0,0,0,.9),0 3px 14px rgba(0,0,0,.75),0 0 40px rgba(0,0,0,.55)}/*/v3*/\n")
    h = h.replace("<style>", '<!--v3--><link href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600&display=block" rel="stylesheet"><!--/v3-->\n<style>', 1)
    if HI: h = h.replace("<style>", '<!--v3--><link href="https://fonts.googleapis.com/css2?' + HI_LINK + '&display=block" rel="stylesheet"><!--/v3-->\n<style>', 1)
    h = h.replace("</style>", css + "</style>", 1)
    card = ('<div id="v3msg"><div id="v3meta"><b>Her</b> · ' + esc(cfg.get("bubbleTime", "11:47 PM")) + '</div><div id="v3bub">' + esc(bubble) + "</div></div>" if bubble else "") + ('<div id="v3title">' + esc(title) + "</div>" if title else "")
    if card: h = h.replace('<div id="caps"></div>', '<div id="caps"></div>\n  <!--v3--><div id="v3card">' + card + "</div><!--/v3-->", 1)
    tl3 = ""
    if card:   # readable from frame 0 (only a 0.15 s scale pop, no fade-in); the word captions wait until the card has gone
        tl3 += ('  /*v3*/tl.fromTo("#v3card", { scale: 0.96 }, { scale: 1, duration: 0.15, ease: "power2.out" }, 0);'
                ' tl.to("#v3card", { opacity: 0, duration: 0.2, ease: "power2.in" }, 2.0);'
                ' tl.set("#caps", { opacity: 0 }, 0); tl.set("#caps", { opacity: 1 }, ' + (str(round(HOOK_END + 0.15, 3)) if HOOK_END else "2.2") + ');/*/v3*/\n')
    if isinstance(cfg.get("rehookAt"), int):   # the re-hook line: a quick 0.15 s push-in on the film that relaxes back, and a faint flash
        i = cfg["rehookAt"]
        tl3 += (f'  /*v3*/tl.fromTo("#bg", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.15, ease: "power2.out", immediateRender: false }}, T.vo[{i}]);'
                f' tl.to("#bg", {{ scale: 1, duration: 0.9, ease: "sine.inOut" }}, T.vo[{i}] + 0.15);'
                f' tl.fromTo("#flash", {{ opacity: 0.32 }}, {{ opacity: 0, duration: 0.25, ease: "power2.out", immediateRender: false }}, T.vo[{i}]);/*/v3*/\n')
    if od:   # the bronze outro is capped at 2.6 s and fades itself out (the clip's own fade sits at ~3.1 s); if the spoken tagline needs
        #   longer than that (total - END > 2.6), the outro stays up for the tagline instead — never black under the voice
        END = float(re.search(r"END = ([\d.]+);", h).group(1)); TOT = float(re.search(r'id="root"[^>]*data-duration="([\d.]+)"', h).group(1))
        cap = round(min(od - 0.01, max(2.6, TOT - END)), 2)
        if TOT - END > cap + 0.05:   # owner 10-16: the outro ran out before the closing words did (black gap under "Follow…") —
            new = round(TOT - cap, 2)   # start it later so it rises during the last words and ends WITH the reel
            h = re.sub(r"END = [\d.]+;", f"END = {new};", h, count=1)
            h = re.sub(r'(id="outro"[^>]*data-start=")[\d.]+', rf"\g<1>{new:.2f}", h); END = new
        h = re.sub(r'(id="outro"[^>]*data-duration=")[\d.]+', rf"\g<1>{cap:.2f}", h)
        bgd = re.search(r'id="bg"[^>]*data-duration="([\d.]+)"', h)
        if bgd and float(bgd.group(1)) < END:   # 10-16: the clip film plays on until the outro rises (it stopped at the old outro time: 2 s of black)
            h = re.sub(r'(id="bg"[^>]*data-duration=")[\d.]+', rf"\g<1>{END:.2f}", h)
        tl3 += f'  /*v3*/tl.to("#outro", {{ opacity: 0, duration: 0.5, ease: "sine.in" }}, END + {cap - 0.5:.2f});/*/v3*/\n'
        if TOT - END > 2.65: print(f"v3 note: the outro runs {TOT - END:.2f} s (target 2.6) — shorten the tagline or lower reel.json tail by {TOT - END - 2.6:.2f} s")
    h = h.replace("  tl.set({}, {}, ", tl3 + "  tl.set({}, {}, ", 1)
# Hindi reels: Devanagari needs more line height (matras above/below), the chunker must also break at the danda and treat Hindi
# postpositions as "weak" words (never end a card on का/की/के/में/पर...). English reels never enter this block.
h = re.sub(r" */\*hi\*/.*?/\*/hi\*/\n?", "", h, flags=re.S)
if HI:
    h = h.replace("</style>", " /*hi*/.cap{line-height:1.34} #v3title{line-height:1.22} #tcard{line-height:1.3} #v3bub{font-family:'Inter','Noto Sans Devanagari',sans-serif}/*/hi*/\n</style>", 1)
    if "।" not in h:
        h = h.replace('/[.,!?…]["”’\']?$/.test(w[0])', '/[.,!?…।]["”’\']?$/.test(w[0])')
        h = h.replace("/^(the|a|an|to|of|and|her|at|for|with|who's)$/i", "/^(the|a|an|to|of|and|her|at|for|with|who's|का|की|के|को|से|में|पर|और|ने|तो|भी|ही|है|हो|या|कि|जो|वो|ये)$/i")
h = h.replace('<div id="title"><b>FOLLOW</b> FOR MORE</div>', '<div id="title"></div>')   # owner 10-15: no "follow for more" — the brand ending
open(H, "w").write(h)
print(f"{os.path.basename(R)}: title card {cfg.get('titleCard') or 'none'}, accent {len(cfg.get('accent', []))} words, reveal on lines {[i + 1 for i in cfg.get('drops', [])]}")
