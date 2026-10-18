"""Create v3 reels (growth plan 10-15, brain/growth/growth-plan-2026-10-15.md) from a v3 script file.
Usage: python3 tools/new_reels_v3.py brain/content/drafts/week3-v3-scripts.md w3 [--dry]
Each "## NN · Series · "Title"" section (+ its "## NN meta" block with <!-- meta: series=…, titleCard="…", bubble="…",
caption hook=…, caption body=…, caption prompt=…, caption tags=… -->) becomes reels/<prefix>-NN-<slug>/ with:
  assets/vo/script.json — the spoken lines; the placeholder "Follow for more." becomes the brand tagline (config reels.tagline)
  reel.json — format v3 (tools/fill_page.py + clipcut.py: chat-bubble opener, big title, bright first 3 s, re-hook punch),
    bubble, titleCard, rehookAt (the "But…" line at ~8-10 s), drops (the WHY line), short gaps, tail 0.6, cover kicker/headline
  brain/content/captions/<slug>.txt — the keyword-first caption (≤ 5 hashtags), used by tools/queue_reel.sh when it books
The v2 tool (tools/new_reels.py) is left as it was. 10-16 owner: NO 30 s cap — a reel is as long as the value needs; never rush the
narrator. Refuses only a script over 90 s; lines get real breathing pauses (0.3 s, 0.6 s after the hook and the re-hook)."""
import json, os, re, shutil, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); REF = os.path.join(ROOT, "reels/p1c-hookb")
args = [a for a in sys.argv[1:] if not a.startswith("--")]; DRY = "--dry" in sys.argv
src, prefix = args[0], args[1]
text = open(os.path.join(ROOT, src)).read()
RC = json.load(open(os.path.join(ROOT, "config.json"))).get("reels", {})
TAGLINE = RC.get("tagline", "")
WPS = 175 / 60   # our narrator's pace (Fish prosody ≈1.2 → ~175 wpm)

metas = {}
for m in re.finditer(r"^## (\d+) meta\n<!--\s*meta:(.*?)-->", text, re.S | re.M):
    body = m.group(2)
    kv = dict(re.findall(r'(series|lang|titleCard|bubble|caption hook|caption body|caption prompt|caption tags)\s*=\s*"?(.*?)"?\s*(?:,\s*\n|,\s*(?=[a-zA-Z ]+=)|$)', body, re.S))
    metas[m.group(1)] = {k: v.strip().strip('"') for k, v in kv.items()}

made = []
for m in re.finditer(r"^## (\d+) · ([^·\n]+?) · \"([^\"]+)\"\n(.*?)(?=^## |\Z)", text, re.S | re.M):
    num, series, title, body = m.group(1), m.group(2).strip(), m.group(3), m.group(4)
    lines = [l.strip() for l in body.strip().splitlines() if l.strip() and not l.startswith(("---", "<!--", "|"))]
    TAG = re.compile(r"\[[^\]]*\]\s*")   # inline delivery directions ([pause], [lower voice]…) — voice directions, never words
    clean = lambda l: TAG.sub("", l).strip()
    while lines and clean(lines[-1]).rstrip(".…। ").lower() in ("follow for more", "फॉलो करो", "decode her", clean(TAGLINE).rstrip(".… ").lower()):
        lines = lines[:-1]   # the brand line is added once, below (a script ending in it was spoken twice)
    if TAGLINE: lines.append(TAGLINE)   # 10-15: no fixed slogan — each script ends on its own natural closing line
    meta = metas.get(num, {})
    words = sum(len(clean(l).split()) for l in lines)
    est = words / WPS + 0.35 * (len(lines) - 1) + 0.6
    if est > 90: sys.exit(f"{num}: ~{est:.1f} s > 90 s — split it into two reels")
    n = len(lines)
    rehook = next((i for i, l in enumerate(lines) if i >= 2 and re.match(r"^(but|and|so here|here'?s why|wait|पर|लेकिन|मगर|और)(?![\u0900-\u097F\w])", clean(l), re.I)), 3)
    why = next((i for i, l in enumerate(lines) if i > rehook and re.search(r"\bbecause\b|क्योंकि", l, re.I)), min(rehook + 1, n - 3))
    prompt = next((i for i, l in enumerate(lines) if re.search(r"(^|[.?!]\s)(comment|send this|save this|screenshot|drop|कमेंट|भेज|सेव|स्क्रीनशॉट)(?![\u0900-\u097F\w])", clean(l), re.I)), n - 2)
    script = [{"text": l, "ex": 0.62, "cfg": 0.42} if i == 0 else l for i, l in enumerate(lines)]
    gaps = [0.3] * n   # 10-16 owner: the narrator explains — let each line land, no rushing
    gaps[0] = 0.6; gaps[rehook - 1] = 0.6; gaps[prompt - 1] = max(gaps[prompt - 1], 0.25); gaps[n - 2] = 0.45; gaps[n - 1] = 0
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:24]
    R = os.path.join(ROOT, "reels", f"{prefix}-{num}-{slug}")
    cfg = {"format": "v3", "series": meta.get("series", series), "title": title, "topic": series,
           "titleCard": meta.get("titleCard", title), "bubble": meta.get("bubble", ""), "rehookAt": rehook,
           "gaps": gaps, "tail": 0.6, "lead": 0.08, "music": "auto", "drops": [why], "ctaLine": n - 1, "speed": 1.0,
           "accent": [], "voice_chain": 2,
           "coverKicker": re.sub(r"\s*#\d+\s*$", "", meta.get("series", series)), "coverHeadline": meta.get("titleCard", title)}
    if RC.get("frame") == "lens":   # 10-16 owner-approved format (sample w6-01): colour + soft lens edges + paper texture, no re-hook flash,
        # the hook-end riser/impact on line 1 and on the "Here's how…" turn; snaps are chosen later by tools/peak_points.py
        how = next((i for i, l in enumerate(lines) if re.match(r"^(here'?s how|so here'?s what|here'?s what)", clean(l), re.I)), min(5, n - 3))
        cfg.update({"frame": "lens", "colour": True, "rehookAt": None, "drops": sorted({1, how})})
    if meta.get("lang", "en").lower() == "hi": cfg["lang"] = "hi"   # Hinglish reel: Devanagari script + English loanwords; tagline stays English
    tags = " ".join(re.findall(r"#\w+", meta.get("caption tags", "#datingadviceformen #datingtips"))[:5])
    caption = "\n".join(x for x in [meta.get("caption hook", ""), meta.get("caption body", ""), "", meta.get("caption prompt", ""),
                                      "Follow @thedecodeher for more dating advice for men.", "", tags] if x is not None).strip() + "\n"
    print(f"{prefix}-{num}-{slug}: {n} lines, {words} words ≈ {est:.1f} s, rehook line {rehook + 1}, why line {why + 1}, prompt line {prompt + 1}"
          f" | bubble {cfg['bubble']!r} | title {cfg['titleCard']!r}")
    if DRY: continue
    os.makedirs(f"{R}/assets/vo", exist_ok=True); os.makedirs(f"{R}/assets/audio", exist_ok=True)
    json.dump(script, open(f"{R}/assets/vo/script.json", "w"), indent=1, ensure_ascii=False)
    json.dump(cfg, open(f"{R}/reel.json", "w"), indent=1, ensure_ascii=False)
    shutil.copy(f"{REF}/index.html", f"{R}/index.html")
    if not os.path.exists(f"{R}/assets/brand"): shutil.copytree(f"{REF}/assets/brand", f"{R}/assets/brand")
    os.makedirs(os.path.join(ROOT, "brain/content/captions"), exist_ok=True)
    open(os.path.join(ROOT, f"brain/content/captions/{prefix}-{num}-{slug}.txt"), "w").write(caption)
    made.append(os.path.relpath(R, ROOT))
if not DRY: json.dump(made, open(os.path.join(ROOT, f"reels/{prefix}-batch.json"), "w"), indent=1); print(f"{len(made)} reels → reels/{prefix}-batch.json")
# 10-19 owner: every reel opens on its AI-woman hook clip. The factory never picks one, so do it here, before the batch can render
if not DRY and RC.get("frame") == "lens":
    import subprocess
    for r in made: subprocess.run([sys.executable, os.path.join(ROOT, "tools/pick_hook.py"), r], cwd=ROOT, timeout=300)
