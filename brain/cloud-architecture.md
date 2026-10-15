# DecodeHer in the cloud — PC-off architecture (10-15, owner: "completely free, works with my PC off")

Oracle (card declined) and Hugging Face Docker Spaces (now paid) are out. Free, no card:

```
                 ┌──────────────── Cloudflare (free, 24/7) ─────────────────┐
 Telegram ◄────► │ decodeher-hq  (Worker + Durable Object "HQ")             │
  (owner)        │  - Telegram bot (webhook) = the Manager you talk to      │
                 │  - dashboard (static assets) + GET /api/state            │
                 │  - DO alarm every 10 min: watch relay, notify, digest    │
                 │  - starts factory runs on GitHub (repository_dispatch)   │
 browser ──────► │                                                          │
                 │ decodeher-relay (EXISTING, posts 08:30/21:00, untouched  │
                 │  except the reviewed audit update + read-only /insights) │
                 └───────────────▲──────────────────────────▲───────────────┘
                                 │ state/events (HQ_KEY)     │ queue (RELAY_KEY)
                 ┌───────────────┴── GitHub Actions (free) ──┴───────────────┐
                 │ workflow "factory": nightly + on dispatch                │
                 │  rclone pull Drive → python3 tools/factory.py --once     │
                 │  (voice→…→render→queue) → push Drive → report to HQ      │
                 │ workflow "manager-request": claude -p on owner's request │
                 └───────────────────────────▲──────────────────────────────┘
                                             │ rclone (RCLONE_CONF secret)
                                    Google Drive (15 GB free): decodeher/
```

## Contracts (all parts must match these)

### HQ Worker `decodeher-hq` (dir `hq/`)
- Secrets: `HQ_KEY` (Bearer for writes), `TELEGRAM_BOT_TOKEN`, `TELEGRAM_SECRET` (webhook header
  `X-Telegram-Bot-Api-Secret-Token`), `OWNER_CHAT_ID` (only this chat may command), `RELAY_URL`, `RELAY_KEY`,
  `GH_TOKEN` (fine-grained, actions+contents on the one repo), `GH_REPO` ("owner/name").
- Routes:
  - `GET /` and static assets → dashboard (`hq/public/index.html`, responsive).
  - `GET /api/state` (public, read-only, no secrets) → latest snapshot JSON (shape below) + `relay` (queue/log from relay
    `/status`, captions stripped) + `manager` (recent manager messages) + `stale` flags.
  - `POST /api/state` (Bearer HQ_KEY) → factory pushes a snapshot.
  - `POST /api/event` (Bearer HQ_KEY) → `{type, text, reel?, preview_url?, slot?}`; types: `activity`, `preview`
    (asks the owner to approve), `error`, `done`.
  - `POST /tg` → Telegram webhook (verify secret header; ignore any chat ≠ OWNER_CHAT_ID).
- Durable Object `HQ` storage keys: `snapshot`, `snapshotAt`, `msgs` (last 200 manager lines), `pending`
  (approvals by id), `requests` (owner requests and their state), `lastRelay` (for change detection), `stats` (daily).
- Alarm every 10 min: fetch relay `/status`; on a new POSTED/FAILED/SKIPPED/TOKEN ERROR → Telegram message; if the
  factory snapshot is older than 26 h while reels are unfinished → warn; 10:00 IST daily digest (yesterday's posts +
  insights via relay `/insights`).
- Telegram commands: `/status`, `/queue`, `/stats`, `/pause`, `/resume` (→ relay), `/make` (dispatch `factory`),
  `/help`; inline buttons on previews: Approve / Reject; any other text = a change request → stored → dispatch
  `manager-request` with `{request_id, text}` → reply "On it, I'll send a preview".
- GitHub dispatch: `POST https://api.github.com/repos/{GH_REPO}/dispatches` body `{event_type, client_payload}`.

### Factory snapshot (POST /api/state) — same as today's board data
`{ now, reels:[{dir,title,next,video,queued,posted,...}], running:[...], activity:[...], stations:{...},
   factory:{running:{dir:stage}, reels:{dir:stage}, parked:{...}}, ver }` (build it with dashboard.js's snapshot logic).

### GitHub Actions (dir `.github/workflows/`, helpers `tools/cloud/`)
- Secrets: `FISH_API_KEY`, `RELAY_URL`, `RELAY_KEY`, `HQ_URL`, `HQ_KEY`, `CLAUDE_CODE_OAUTH_TOKEN`, `RCLONE_CONF`,
  `TELEGRAM_BOT_TOKEN`, `OWNER_CHAT_ID` (previews are sent straight to Telegram as video, ≤ 50 MB).
- `factory.yml`: on `schedule` (nightly, 19:30 UTC) + `repository_dispatch: [factory]` + `workflow_dispatch`.
  Steps: install deps (ffmpeg, rubberband-cli, chromium deps, node, uv, claude CLI) with caching → `tools/cloud/sync.sh pull`
  → `python3 tools/factory.py --once --max-minutes 300` → `tools/cloud/sync.sh push` → `tools/cloud/report.py` (snapshot to HQ).
  concurrency group "factory" (never two at once).
- `manager-request.yml`: `repository_dispatch: [manager-request]` → pull → `claude -p` with `tools/manager_request_prompt.txt`
  and the request text, restricted tools → result: a re-rendered preview sent to Telegram + `pending` approval event to HQ →
  push. Approval later → `repository_dispatch: [approve]` → swap into the reel's slot (`queue_reel.sh` requeue path).
- Drive layout `decodeher/`: `reels/`, `library/`, `deliverables/`, `logs/`, `brain/` (big binaries; code stays in git).

### Relay additions (reviewed update, owner deploys)
- `GET /insights?days=N` (Bearer) → per posted reel: reach, views, likes, comments, shares, saved,
  ig_reels_avg_watch_time; account followers_count. Read-only Graph calls with the relay's own token.
