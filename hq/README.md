# DecodeHer HQ (`decodeher-hq`)

The always-on "HQ" for @thedecodeher. It runs free on Cloudflare, so it keeps working with the laptop off.

- **Telegram bot**: you talk to it. Commands: `/status` `/queue` `/stats` `/pause` `/resume` `/make` `/help`.
  Anything else you type is a change request: the bot starts the work on GitHub and later sends you a preview with
  **Approve / Reject** buttons.
- **Dashboard**: the web page at the HQ address (files in `public/`). Live data comes from `/api/state`, which shows no
  secrets and no captions.
- **Watcher**: every 10 minutes it checks the posting relay and messages you when a reel is posted (with its link), fails,
  is skipped, or Instagram's login has a problem. Each event is reported once. If the factory hasn't checked in for 26 hours
  while reels are unfinished, it warns you (once a day). At **10:00 IST** you get a short morning digest of yesterday's posts.

How it works: `brain/cloud-architecture.md`. Code: `worker.js`. Tests: `node test.mjs` (they run offline and contact nothing).

---

## One-time setup (about 15 minutes)

Run every command inside this folder: `cd ~/Projects/dark-psycology/hq`

### 1. Create the Telegram bot
1. In Telegram, open **@BotFather** and send `/newbot`.
2. Give it a name (for example "DecodeHer HQ") and a username that ends in `bot`.
3. BotFather replies with a **token** that looks like `123456789:AA...`. Keep it private.
4. Open your new bot and send it any message, for example "hi". You need this for step 4.

### 2. Make two random passwords
```
openssl rand -hex 24      # run it twice: the first result is HQ_KEY, the second is TELEGRAM_SECRET
```
Save both somewhere private, such as a password manager. The factory on GitHub needs the same `HQ_KEY`.

### 3. Put the HQ online
```
npx wrangler login        # only if you aren't logged in already (same Cloudflare account as the relay)
npx wrangler deploy
```
It prints the address, for example `https://decodeher-hq.<your-name>.workers.dev`. That's your **HQ URL**.

### 4. Find your OWNER_CHAT_ID
Open this in a browser, with your bot token in place of `<TOKEN>`:
```
https://api.telegram.org/bot<TOKEN>/getUpdates
```
Look for `"chat":{"id":123456789` and copy that number. If the page shows `"result":[]`, send the bot another message and
reload. This page only works **before** step 6, because once the webhook is set it stays empty.

### 5. Add the secrets
Run each line. Wrangler asks for the value; paste it and press Enter.
```
npx wrangler secret put HQ_KEY               # password 1 from step 2
npx wrangler secret put TELEGRAM_SECRET      # password 2 from step 2
npx wrangler secret put TELEGRAM_BOT_TOKEN   # the BotFather token
npx wrangler secret put OWNER_CHAT_ID        # the number from step 4
npx wrangler secret put RELAY_URL            # https://decodeher-relay.shajith240.workers.dev
npx wrangler secret put RELAY_KEY            # the "key" value in ../.relay.json (open the file yourself; don't paste it into chats)
npx wrangler secret put GH_TOKEN             # GitHub token, see below
npx wrangler secret put GH_REPO              # e.g. yourname/dark-psycology
```
**GitHub token:** on GitHub go to Settings → Developer settings → Fine-grained tokens → Generate new token.
Under Repository access choose **Only select repositories** and pick the one repo. Under Permissions set
**Contents: Read and write** and **Actions: Read and write**, then generate it and paste it as `GH_TOKEN`.

### 6. Connect Telegram to the HQ (webhook)
Fill in your bot token, HQ URL and TELEGRAM_SECRET, then run:
```
curl -s "https://api.telegram.org/bot<TOKEN>/setWebhook" \
  -d "url=<HQ URL>/tg" \
  -d "secret_token=<TELEGRAM_SECRET>" \
  -d 'allowed_updates=["message","callback_query"]' \
  -d "drop_pending_updates=true"
```
It should answer `{"ok":true,...,"description":"Webhook was set"}`. To check it later, run:
`curl -s "https://api.telegram.org/bot<TOKEN>/getWebhookInfo"`. It should show no `last_error_message`.

Optional, to give the bot its menu of commands:
```
curl -s "https://api.telegram.org/bot<TOKEN>/setMyCommands" -H "Content-Type: application/json" -d '{"commands":[
 {"command":"status","description":"How everything is doing"},{"command":"queue","description":"Booked posts"},
 {"command":"stats","description":"How the reels perform"},{"command":"pause","description":"Stop posting"},
 {"command":"resume","description":"Start posting again"},{"command":"make","description":"Start the factory now"},
 {"command":"help","description":"What I can do"}]}'
```

### 7. Try it
- Send `/help`, then `/status` to the bot. It should answer within a few seconds.
- Open the HQ URL in a browser to see the dashboard.
- The 10-minute watcher starts on its own with the first message or page visit.

---

## Day to day
- **Update the code:** `node test.mjs && npx wrangler deploy`. Secrets and stored data are kept.
- **The bot doesn't answer:** run `getWebhookInfo` (step 6). If the secret or URL is wrong, run `setWebhook` again.
  Messages from any other chat are ignored on purpose.
- **Live logs:** `npx wrangler tail decodeher-hq`.
- **Change a secret:** run `npx wrangler secret put <NAME>` again.

## For the factory and agents (API)
| Route | Who | What |
|---|---|---|
| `GET /api/state` | anyone (CORS open) | latest factory snapshot + `relay` (queue without captions or media keys, log) + `manager` (last 50 lines) + `pending` previews + `stale` flags |
| `POST /api/state` | `Authorization: Bearer HQ_KEY` | factory snapshot (the board's state.json shape), max 1 MB |
| `POST /api/event` | `Authorization: Bearer HQ_KEY` | `{type: activity\|preview\|error\|done, text, reel?, preview_url?, slot?, request_id?, id?}` |
| `POST /tg` | Telegram only (secret header) | bot webhook |

- `preview` messages you with Approve/Reject buttons. If `preview_url` (https) is given, Telegram fetches the video from that URL.
  A tap sends GitHub `repository_dispatch` `approve` or `reject` with `client_payload {id, request_id, reel, slot}`.
- `error` messages you with ⚠️. `done` messages you with ✅ and marks `request_id` as done. `activity` only goes into the feed.
- Your free-text requests are sent to GitHub as `manager-request` with `{request_id, text}`. `/make` sends `factory`.
