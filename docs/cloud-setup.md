# Running the factory in the cloud (PC off)

How the parts fit together: `brain/cloud-architecture.md`. This page covers the one-time setup. It takes about 30 minutes.

## 1. Private GitHub repository
1. On github.com, create a **private** repository, for example `decodeher-factory`.
2. Push this folder to it. `.gitignore` already leaves out the secrets (`.env`, `.relay.json`), the big folders
   (`reels/`, `library/`, `deliverables/`, `logs/`) and all video and audio files. Before the first push, run `git status` and check
   that none of those appear.
3. Free plan limits for private repos: 2,000 runner minutes a month on a 2-CPU, 7 GB machine. One full nightly run can use up to
   about 5 hours, so the monthly minutes run out within days at the full length. Either make the repo **public** (minutes are
   unlimited, and secrets and Drive files stay private) or lower `max_minutes` (Actions → factory → Run workflow).

## 2. Google Drive (rclone)
On the laptop:
1. Create the remote: `rclone config` → `n` (new) → name `gdrive` → storage `drive` → leave client id and secret empty →
   scope `1` (full access) → no advanced config → **yes** to browser auth → sign in → not a shared drive → `y`.
2. Copy the files up once: `REMOTE=gdrive:decodeher bash tools/cloud/sync.sh push`. Try it first with `DRY=1` added at the front.
   Hard-linked clips are stored as a list (`reels/.hardlinks.tsv`), so the upload is about 6 GB rather than 12 GB.
3. Print the config to paste into GitHub: `rclone config show gdrive`. Paste the whole block, including the `[gdrive]` line.
   Treat it like a password.

## 3. Repository secrets
Go to GitHub → repo → Settings → Secrets and variables → Actions → New repository secret:

| Secret | What it is |
|---|---|
| `RCLONE_CONF` | the `[gdrive]` block from step 2 |
| `FISH_API_KEY` | Fish Audio key (voice) |
| `RELAY_URL`, `RELAY_KEY` | the posting relay; the same two values as in `.relay.json` (`url`, `key`) |
| `CLAUDE_CODE_OAUTH_TOKEN` | run `claude setup-token` on the laptop and paste the token it prints |
| `HQ_URL`, `HQ_KEY` | the decodeher-hq worker URL and its write key |
| `TELEGRAM_BOT_TOKEN`, `OWNER_CHAT_ID` | the bot that sends previews and the owner's chat id |
| `PINTEREST_COOKIES` (optional) | Pinterest login as a cookies.txt export (browser extension "Get cookies.txt"). Without it, clip searches fail. |

## 4. First run
1. Actions → **factory** → Run workflow → set `max_minutes` to `20` → Run.
2. Watch the steps: Install, then Pull from Drive, Run the factory, Push to Drive, Report to HQ. The run's logs are saved as
   an artifact for 7 days.
3. Then from Telegram: `/status` should show the new snapshot. `/make` starts a run, and any other message becomes a change request
   that comes back as a preview video with Approve / Reject.

## Good to know
- Only one factory run happens at a time. A second `/make` while one is running waits. A third replaces the waiting one.
- A change request and the factory can run at the same moment. Avoid asking for changes to a reel that is mid-render.
- Drive space: `bash tools/cloud/sync.sh prune` lists old clip candidates of posted reels. `APPLY=1` deletes them.
- The laptop services keep working as before. Don't run the laptop factory and the cloud factory on the same reels at the same
  time: both would book posts.
