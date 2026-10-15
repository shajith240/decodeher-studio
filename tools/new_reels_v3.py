"""Create v3 reels (growth plan 10-15, brain/growth/growth-plan-2026-10-15.md) from a v3 script file.
Usage: python3 tools/new_reels_v3.py brain/content/drafts/week3-v3-scripts.md w3 [--dry]
Each "## NN · Series · "Title"" section (+ its "## NN meta" block with <!-- meta: series=…, titleCard="…", bubble="…",
caption hook=…, caption body=…, caption prompt=…, caption tags=… -->) becomes reels/<prefix>-NN-<slug>/ with:
  assets/vo/script.json — the spoken lines; the placeholder "Follow for more." becomes the brand tagline (config reels.tagline)
  reel.json — format v3 (tools/fill_page.py + clipcut.py: chat-bubble opener, big title, bright first 3 s, re-hook punch),
    bubble, titleCard, rehookAt (the "But…" line at ~8-10 s), drops (the WHY line), short gaps, tail 0.6, cover kicker/headline
  brain/content/captions/<slug>.txt — the keyword-first caption (≤ 5 hashtags), used by tools/queue_reel.sh when it books
The v2 tool (tools/new_reels.py) is left as it was. Refuses a script that would run over 30 s (hard cap of the v3 format)."""
import json, os, re, shutil, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); REF = os.path.join(ROOT, "reels/p1c-hookb")
args = [a for a in sys.argv[1:] if not a.startswith("--")]; DRY = "--dry" in sys.argv
src, prefix = args[0], args[1]
text = open(os.path.join(ROOT, src)).read()
RC = json.load(open(os.path.join(ROOT, "config.json"))).get("reels", {})
TAGLINE = RC.get("tagline", "Decode her… before she decodes you.")
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
    if lines and lines[-1] in ("Follow for more.", "Follow for more", "फॉलो करो।"): lines = lines[:-1]
    lines.append(TAGLINE)
    meta = metas.get(num, {})
    words = sum(len(l.split()) for l in lines)
    est = words / WPS + 0.15 * (len(lines) - 1) + 0.6
    if est > 30: sys.exit(f"{num}: ~{est:.1f} s > 30 s cap — shorten the script")
    n = len(lines)
    rehook = next((i for i, l in enumerate(lines) if i >= 2 and re.match(r"^(but|and|so here|wait|पर|लेकिन|मगर|और)(?![\u0900-\u097F\w])", l, re.I)), 3)
    why = next((i for i, l in enumerate(lines) if i > rehook and re.search(r"\bbecause\b|क्योंकि", l, re.I)), min(rehook + 1, n - 3))
    prompt = next((i for i, l in enumerate(lines) if re.match(r"^(comment|send|save|screenshot|drop|कमेंट|भेज|सेव|स्क्रीनशॉट)(?![\u0900-\u097F\w])", l, re.I)), n - 2)
    script = [{"text": l, "ex": 0.62, "cfg": 0.42} if i == 0 else l for i, l in enumerate(lines)]
    gaps = [0.12] * n
    gaps[rehook - 1] = 0.3; gaps[prompt - 1] = max(gaps[prompt - 1], 0.25); gaps[n - 2] = 0.45; gaps[n - 1] = 0
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:24]
    R = os.path.join(ROOT, "reels", f"{prefix}-{num}-{slug}")
    cfg = {"format": "v3", "series": meta.get("series", series), "title": title, "topic": series,
           "titleCard": meta.get("titleCard", title), "bubble": meta.get("bubble", ""), "rehookAt": rehook,
           "gaps": gaps, "tail": 0.6, "lead": 0.08, "music": "auto", "drops": [why], "ctaLine": n - 1, "speed": 1.07,
           "accent": [], "voice_chain": 2,
           "coverKicker": meta.get("series", series), "coverHeadline": meta.get("titleCard", title)}
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
