STATUS: TODO
# NEXT SESSION — written 2026-10-19 04:45 IST (owner's Claude limit ran out; auto-resume at 07:35 IST)

Read CLAUDE.md first. Never read/print .env, .relay.json, .secrets/*. Decide yourself; be economical. When ALL tasks below are
done, change the first line to `STATUS: DONE`.

## What changed on 10-19 (owner orders, all decided)
- NEW CONTENT RULE "steal like an artist" + 95/5: every reel remixes a proven viral Short/Reel (1M+ views). Keep 95% of the
  source (same hook, same points in the same order, same examples, similar length); ours = the "Listen" beat after the hook +
  our closing line ("Save this…"/"Send this to…") + our voice/opener/clips/look. Reword sentence by sentence, never word for word.
  Mainstream niche tactics (space, push-pull, "make her miss you") are allowed. Each script names its source URL + views.
- All 21 old queued reels (w2 remakes, w9–w11) were REMOVED from the relay (owner: abandon them). Their folders stay; their
  logs/queued markers stay so they never re-book. deliverables/queue/booked was emptied.
- v1/v2/v3 batches RETIRED (parked: they changed the sources too much). Replacements:
  - reels/v4-batch.json = TODAY's 3 (brain/content/drafts/viral4-scripts.md): Habits women find attractive (4.4M),
    Six words (1.2M), Biggest turn-off (1.3M) → slots today 08:30 / 18:30 / 22:00 (the factory books the next free slot).
  - reels/v5-batch.json = 7 for Tue–Wed (brain/content/drafts/viral5-scripts.md).
- Every reel must open on its AI-woman hook clip with NO text on her (no title, no captions until the hook ends).
  tools/new_reels_v3.py now runs tools/pick_hook.py itself; fill_page.py hides the title when reel.json has hookClip.
  If a reel was built before its hookClip existed: `python3 tools/fill_page.py reels/<r>` and re-render.

## Tasks, in order
1. Check v5 exists: `ls reels/v5-batch.json`. If missing, run
   `python3 tools/new_reels_v3.py brain/content/drafts/viral5-scripts.md v5` (it also picks the hook clips).
   Every v4/v5 reel.json must have hookSrc/hookClip; if one says "first available", re-run `python3 tools/pick_hook.py reels/<r> --force`.
2. VERIFY each v4 reel as it books (`node tools/ig_queue.js ids`; the posting copy is deliverables/queue/booked/*-FINAL.mp4):
   - first 4 s: `ffmpeg -ss 0 -t 4 -i F -vf "fps=2,scale=200:-1,tile=8x1" -frames:v 1 open.jpg` → the AI woman, ZERO text on her.
   - whole reel grid (fps=1/3), captions present after the hook, bronze bust outro at the end, no black frames.
   - loudness: ebur128 integrated about -11 to -14 LUFS, no clipping.
   If one fails: `node tools/ig_queue.js remove <id>`, move logs/queued/<slug> + its booked files aside, fix the cause, let the
   factory re-render. Make sure 08:30 today gets a correct reel; if it can't be ready, leave the slot empty (never post a wrong one).
3. Same checks for v5 reels as they book (Tue 08:30 onward).
4. Viral bank (two agents were building it when the session ended; they may have been cut off):
   brain/research/viral-bank/ (ig.jsonl, yt-tiktok.jsonl, README.md), tools/viral_bank_ig.py, tools/viral_bank_yt.py,
   library/research/viral/. If the scripts exist, run them once; if not, build tools/viral_bank_yt.py (yt-dlp, channel /shorts
   tabs, keep ≥1M views, incremental, "used_by": null, "added") — method that worked 10-19: list niche channels via
   `yt-dlp --flat-playlist -J "ytsearch30:<query>"` → channel_url → `yt-dlp --flat-playlist -J --playlist-end 120 <channel>/shorts`.
   Download with `-f "136+ba/398+ba/bv*+ba" --merge-output-format mp4`; transcribe via faster-whisper (scratchpad tx.py pattern:
   ffmpeg → 16 kHz PCM → WhisperModel("small.en", int8)).
   Mark the 10 sources already used (viral4/viral5 drafts) as used_by.
5. Write the next batch (v6, 6 reels for Thu 10-22 → Fri 10-23) with the 95/5 rule from the bank's best unused ≥1M entries,
   create it with tools/new_reels_v3.py. Same for v7 (Sat–Sun) if the bank has enough.
6. 24/7 plan (owner asked; do after content is safe): systemd user timers with Persistent=true for the bank refresh (daily) and an
   auto-planner (daily: if < 7 days booked, write the next 95/5 batch from the bank); Telegram alert when < 3 days booked;
   cloud factory failover later (GitHub factory/planner workflows exist but are disabled — never run both at once).

## Owner to-do (only they can)
- Paste the lid-close command (keeps the laptop working with the lid shut while plugged in):
  `sudo mkdir -p /etc/systemd/logind.conf.d && printf '[Login]\nHandleLidSwitchExternalPower=ignore\nHandleLidSwitchDocked=ignore\n' | sudo tee /etc/systemd/logind.conf.d/decodeher-lid.conf && sudo systemctl kill -s HUP systemd-logind`
- Polar: replace the playbook PDF in the "Decode Her Texting Playbook (PDF)" benefit with deliverables/products/Decode-Her-Texting-Playbook.pdf; test-buy the pack with a 100% code.
- Make the relaxed ethics rule permanent in CLAUDE.md (the edit was blocked for Claude).

## Also done 10-19 (no action needed)
Site live https://decodeher.pages.dev (two tiers $9/$19 launch, throne-king image, native scroll, short copy); bonuses in
deliverables/products/bonuses/; carousel research brain/research/carousels/manly-pinnacle-analysis.md (carousel sample not made yet);
memories: steal-like-an-artist (95/5), simple-hands-off, private-audience.
