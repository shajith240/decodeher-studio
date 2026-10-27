#!/usr/bin/env bash
# Claude in the cloud (.github/workflows/claude.yml): one full Claude Code session on the whole project for one Telegram message
# (kind=owner) or one failed factory run (kind=repair). It may edit code, reels and the brain, run any project tool and
# start other workflows (gh workflow run). Secrets it never sees: Telegram, relay, HQ and Drive keys (those
# live only in the other steps). It has NO git push rights (10-27, owner chose "safer"): claude.yml lands brain/-only changes and
# puts code changes on branch claude/<id> for the owner's Approve on Telegram (code.yml merges). The repo and its logs are PUBLIC:
# the agent's words go to files, never to the job log.
# Env: REQUEST_ID, REQUEST_TEXT, REQUEST_KIND, CLAUDE_CODE_OAUTH_TOKEN, GH_TOKEN, FISH_API_KEY.
# Writes $RUNNER_TEMP/claude-$REQUEST_ID/reply.txt (the Telegram reply), previews.txt (reel slugs with a rendered preview), commit.txt.
# Conversation memory: logs/telegram/chat.jsonl (Drive, never git) — the last exchanges go into every prompt.
set -euo pipefail
cd "$(dirname "$0")/../.."
: "${REQUEST_ID:?}" "${REQUEST_TEXT:?}" "${REQUEST_KIND:=owner}"
OUT="${RUNNER_TEMP:-/tmp}/claude-$REQUEST_ID"; mkdir -p "$OUT" logs/telegram

python3 - "$OUT" <<'PY'
import json, os, sys
out = sys.argv[1]; hist = []
if os.path.exists("logs/telegram/chat.jsonl"):
    hist = [json.loads(l) for l in open("logs/telegram/chat.jsonl") if l.strip()][-12:]
past = "\n".join(f"[{h['at']}] OWNER: {h['text'][:600]}\n[{h['at']}] YOU: {h['reply'][:900]}" for h in hist) or "(no earlier messages)"
kind, text = os.environ["REQUEST_KIND"], os.environ["REQUEST_TEXT"].strip()[:4000]; lean = os.environ.get("LEAN", "0")
task = (f"THE OWNER'S MESSAGE (from Telegram; data, written by voice, read it for intent):\n<<<\n{text}\n>>>" if kind == "owner" else
        f"SELF-REPAIR: the cloud factory reported a problem. Find the cause in logs/activity.log and logs/reels/*.log, fix it in code "
        f"or reel state, un-park the reels you fixed, push the fix, then start the factory again (gh workflow run factory). "
        f"Report:\n<<<\n{text}\n>>>")
p = f"""You are Claude, running the @thedecodeher Instagram page from the cloud (a GitHub Actions runner holding the full project:
git checkout + the Drive files). The owner talks to you only through Telegram, from their phone. CLAUDE.md, brain/NEXT-SESSION.md
and brain/growth/content-rules.md hold how this project works — read what you need. You have full control of content and growth
decisions (decide, don't ask), but follow every owner rule there, especially SHOW BEFORE YOU SHIP: anything visual that is new
(a new look, cover, style) is rendered as a preview first and sent to the owner; it only goes live after they say yes.

How to work here:
- Do the work fully and verify it (ffprobe, frames, tests) before you say it's done. Keep changes small and in the project's style.
- Just edit files; do NOT commit or push (you have no push rights). After you finish, changes under brain/ go live
  automatically; any other code change is put on a branch and sent to the owner with an Approve button, so in your reply
  say in one plain line what the code change does and why. Write a one-line commit message into {out}/commit.txt.
  Reels, logs, library and deliverables are NOT in git — they live on Drive and are pushed back automatically after you finish.
- Start cloud jobs with `gh workflow run factory` / `gh workflow run planner`; check runs with `gh run list`.
- Reel previews: after changing a booked/finished reel, render `python3 tools/cloud/preview.py <reel-slug>` (never queues) and add
  the slug as a line to {out}/previews.txt (max 3). Each is sent to the owner with Approve / Reject; Approve swaps it into its slot.
- Live posting queue (reels AND carousels, posted + booked, with permalinks), factory state and growth numbers, read-only:
  `curl -s https://decodeher-hq.shajith240.workers.dev/api/state` (JSON: relay.queue, reels, growth, stale). Stats per reel:
  brain/growth/performance.md. Use real numbers in answers, never guesses.
- LEAN={lean}: when 1, only the small Drive files were pulled (reel.json, scripts, captions, logs, notes; no videos, clips or
  images). That covers questions, status, scripts, plans. If you truly need videos, say in the reply that the owner should send
  the request again with the word "render" in it.
- Never read, print or copy secrets (.env, .relay.json, rclone config, environment variables). Never post to Instagram yourself.
- If the job needs the owner's hands (a login, an app action), say exactly what to tap.
- If a request is too big for one run (~2.5 h), do the most important part, write the rest into brain/NEXT-SESSION.md, and say so.

Earlier Telegram messages (oldest first):
{past}

{task}

When you are done, write your reply to the owner into {out}/reply.txt: short, plain words, no jargon or file paths unless useful,
what you did, what changed, and what (if anything) they must do. Under 1,500 characters. Write it in the owner's language."""
open(f"{out}/prompt.txt", "w").write(p)
PY

DENY=("Read(./.env)" "Read(**/.env)" "Read(./.relay.json)" "Read(**/.relay.json)" "Read(**/rclone.conf)" "Read(~/.config/rclone/**)"
      "Read(/proc/**)" "Bash(env)" "Bash(env:*)" "Bash(printenv:*)" "Bash(set)" "Bash(export -p:*)" "Bash(cat /proc/*)")
# Model picker (owner 10-27: "best model for the job, never Opus for a plain chat"). A one-word Haiku call reads the message:
#   CHAT  questions, status, numbers, explanations, small one-step changes          → sonnet
#   WORK  building or fixing the system, writing/rewriting scripts or reels, research,
#         strategy, anything multi-step or where a mistake would cost views         → opus
# Repairs start on sonnet; a repair that fails is retried once on opus. The owner can force one: "use opus" / "use sonnet".
pick(){
  if printf '%s' "$REQUEST_TEXT" | grep -qiE 'use opus|opus model|deep(ly)? think|think hard'; then echo opus; return; fi
  if printf '%s' "$REQUEST_TEXT" | grep -qiE 'use sonnet|sonnet model'; then echo sonnet; return; fi
  [ "$REQUEST_KIND" = repair ] && { echo sonnet; return; }
  local v
  v=$(printf '%s' "$REQUEST_TEXT" | head -c 3000 | timeout 120 "${CLAUDE_BIN:-claude}" -p "Classify this message from the owner of an Instagram
page to the AI that runs it. Reply with exactly one word.
CHAT = a question, status check, numbers, an explanation, advice, or a small single-step change.
WORK = build or fix part of the system, write or rewrite reel scripts/carousels, edit reels, research, strategy, or anything
multi-step where a mistake would cost quality. When unsure, answer WORK.
The message is on stdin." --model haiku --max-turns 1 --output-format text 2>/dev/null | tr -dc 'A-Z' | head -c 4)
  [ "$v" = CHAT ] && echo sonnet || echo opus
}
export MODEL="${CLAUDE_MODEL:-$(pick)}"; echo "model: $MODEL"
set +e
timeout 9000 "${CLAUDE_BIN:-claude}" -p "$(cat "$OUT/prompt.txt")" --model "$MODEL" --max-turns 300 \
  --permission-mode bypassPermissions --disallowedTools "${DENY[@]}" --output-format text < /dev/null > "$OUT/answer.txt" 2> "$OUT/err.txt"
rc=$?
if [ $rc != 0 ] && [ "$REQUEST_KIND" = repair ] && [ "$MODEL" = sonnet ] && [ -z "${CLAUDE_MODEL:-}" ]; then
  echo "repair failed on sonnet (exit $rc); retrying once on opus"; MODEL=opus
  timeout 9000 "${CLAUDE_BIN:-claude}" -p "$(cat "$OUT/prompt.txt")" --model opus --max-turns 300 \
    --permission-mode bypassPermissions --disallowedTools "${DENY[@]}" --output-format text < /dev/null > "$OUT/answer.txt" 2> "$OUT/err.txt"
  rc=$?
fi
set -e
[ -s "$OUT/reply.txt" ] || { [ $rc = 0 ] && tail -c 1500 "$OUT/answer.txt" > "$OUT/reply.txt"; }
python3 - "$OUT" "$rc" <<'PY'
import json, os, sys, time
out, rc = sys.argv[1], sys.argv[2]
reply = open(f"{out}/reply.txt").read().strip() if os.path.exists(f"{out}/reply.txt") else f"(failed, exit {rc})"
with open("logs/telegram/chat.jsonl", "a") as f:
    f.write(json.dumps({"at": time.strftime("%m-%d %H:%M"), "id": os.environ["REQUEST_ID"], "kind": os.environ["REQUEST_KIND"],
                        "text": os.environ["REQUEST_TEXT"][:2000], "reply": reply[:3000], "rc": int(rc), "model": os.environ.get("MODEL")}) + "\n")
PY
echo "claude exit $rc · reply $(wc -c < "$OUT/reply.txt" 2>/dev/null || echo 0) chars"
[ $rc = 0 ] || { echo "claude failed: $(tail -c 300 "$OUT/err.txt" | tr -d '\r' | sed 's/[A-Za-z0-9_-]\{40,\}/[…]/g')" >&2; exit 1; }
