"""Write the Haiku judge's instructions for one clip reel (owner 10-14: meaning first, our style, good quality, no kid art).
Usage: python3 tools/judge_prompt.py reels/<reel>   → prints the prompt (narration + every shot with its sheet letters)"""
import json, os, sys
R = os.path.abspath(sys.argv[1]); S = json.load(open(f"{R}/shots.json")); idx = json.load(open(f"{R}/clips/sheets/index.json"))
text = " ".join(l["text"] if isinstance(l, dict) else l for l in json.load(open(f"{R}/assets/vo/script.json")))
rows = "\n".join(f"{k} | {S[int(k)]['say']} | {S[int(k)]['q']} | letters {''.join(idx[k]['clips'])}" for k in sorted(idx) if idx[k]["clips"])
print(f"""You are a strict, premium-minded video editor picking B-roll for an Instagram Reel (dating psychology for men) narrated over 2D animated clips. Judge every contact sheet below and write JSON verdicts. Do NOT modify anything else.

Narration: "{text}"

Sheets: {R}/clips/sheets/NN.jpg (view each with the Read tool). Clips are labelled with yellow letters; each clip = a strip of 3 frames (start, middle, end).

Shots (NN | words spoken while the clip shows | intended picture | letters on the sheet):
{rows}

For EVERY lettered clip score:
- "shows": 4-10 words, literally what happens.
- "meaning" 0-10: does it SHOW these words (literally or an instantly readable metaphor)? Gender matters: you/I/me = the man, she/her = the woman.
- "style" 0-10: target = 2D hand-drawn / flat illustration animation for ADULTS (paper texture, simple grown-up characters, flat motion graphics). 0-2 for live action, 3D/Pixar renders, AI-photoreal images, CHILDREN / kid-style cartoons, anime screenshots, emoji/clip-art.
- "quality" 0-10: premium and finished? 0-2 for green screen, flat key-colour backgrounds, blurry, clip-art, cheap templates.
- "text": true if ANY visible words, logos, watermarks or artist signatures (look at the corners).
Write one file per sheet: {R}/clips/judge/NN.json exactly like
{{"clips": {{"A": {{"shows": "...", "meaning": 7, "style": 8, "quality": 7, "text": false}}, ...}}, "better_query": ""}}
Every letter on each sheet. Be harsh. Reply with one line per NN: best letter + meaning.""")
