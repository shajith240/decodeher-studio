"""Narration editor (owner 10-26: "this is not even narration" — the friend-zone reel copied a text-screenshot format, so the voice read
bare fragments: "Yeah, we should hang out some time." Friend zone. Instead: ...). Mandatory before any voice is recorded.
95/5 keeps the source's IDEAS (same points, order, examples); the DELIVERY always follows brain/rules/spoken-script-rules.md.
One Sonnet pass rewrites only the spoken lines of every reel in a draft file:
  - every quoted text/example is FRAMED in a full sentence ("If you text her '...', she'll ...", "Instead, say '...'")
  - complete sentences (subject + verb), linked with so / because / but / that's why / now; no stacked fragments
  - keeps the [pause] / [lower voice] tags, the "Listen." beat after the hook, the closing line, and every <!-- --> / meta block
  - scores each reel on the read-aloud scorecard and keeps rewriting until it passes; writes the scores as <!-- narration: … -->
Usage: python3 tools/script_polish.py brain/content/drafts/viralN-scripts.md      (auto_planner.py runs it on every new draft)"""
import os, subprocess, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
draft = os.path.abspath(sys.argv[1]); before = open(draft).read()
prompt = f"""You are the narration editor for @thedecodeher reels (an AI narrator voices every line; viewers hear it once).
Read {os.path.join(ROOT, 'brain/rules/spoken-script-rules.md')} (how our narration must sound) and then the draft {draft}.
Rewrite ONLY the spoken lines of each reel (the lines between a "## NN · …" heading and its first <!-- comment). Keep everything else
byte for byte: headings, <!-- --> comments, "## NN meta" blocks, captions.
Hard rules:
1. Keep the content: same points, same order, same examples and quoted texts (95/5). Do not add or remove points.
2. It must sound like a friend talking, not like text on a screen. Every quoted text or example sits inside a full sentence that
   frames it: who says it, when, and what happens. E.g. NOT: "Yeah, we should hang out some time." Friend zone.
   BUT: If you text her "yeah, we should hang out some time", she'll put you in the friend zone. Instead, ask her
   "do you want to hang out later this week?"
3. Complete sentences with a subject and a verb. Link each idea to the last with so, because, but, that's why, now, instead.
   No stacked one-word or two-word sentences (one deliberate short punch per reel at most).
4. Keep the "[pause] Listen." beat right after the first (hook) sentence, keep the delivery tags ([pause], [confident],
   [lower voice]) and the closing line. One spoken line per row, like the draft.
5. Plain words a 16-year-old who speaks English as a second language gets on first listen. No texting words (lol, haha, omg).
6. Keep each reel at about the same length (do not pad).
After rewriting, read each reel aloud in your head. Score it 0/1 on: framed examples, complete sentences, connectors, first-listen
clear, same content as before. If any score is 0, rewrite again. Add a line <!-- narration: framed 1, sentences 1, connectors 1,
clear 1, content 1 --> right after each reel's spoken lines.
Write the improved draft back to {draft}. Reply DONE."""
r = subprocess.run([os.environ.get("CLAUDE_BIN", "claude"), "-p", prompt, "--model", "sonnet", "--allowedTools", "Read", "Write", "Edit",
                    "--output-format", "text"], capture_output=True, text=True, timeout=1800)
after = open(draft).read()
if after == before or "<!-- narration:" not in after: sys.exit(f"narration editor made no change: {(r.stdout or r.stderr)[-300:]}")
print(f"polished {os.path.basename(draft)} ({after.count('<!-- narration:')} reels scored)")
