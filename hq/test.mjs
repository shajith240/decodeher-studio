// Tests for hq/worker.js, no Cloudflare needed: node hq/test.mjs
// worker.js is loaded with its `cloudflare:workers` import swapped for a stub class; storage, the Durable Object namespace and
// every outside call (Telegram, GitHub, relay) are faked in memory. Nothing leaves this machine.
import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const src = readFileSync(fileURLToPath(new URL("./worker.js", import.meta.url)), "utf8")
  .replace(/^import \{ DurableObject \} from "cloudflare:workers";/m, "class DurableObject { constructor(ctx, env) {} }");
assert.ok(!src.includes("cloudflare:workers"), "stubbed the cloudflare import");
const mod = await import("data:text/javascript;base64," + Buffer.from(src).toString("base64"));
const worker = mod.default, HQ = mod.HQ;

// ---------- fakes ----------
const IST = 330 * 60e3;
const at = (ymd, hhmm) => Date.parse(`${ymd}T${hhmm}:00Z`) - IST;   // an IST wall-clock time → epoch ms
const realNow = Date.now;
let fakeNow = at("2026-10-16", "09:00");
Date.now = () => fakeNow;

const SECRETS = { HQ_KEY: "hqkey-SECRET-1234567890", TELEGRAM_BOT_TOKEN: "123456:TGTOKEN-SECRET-abcdef", TELEGRAM_SECRET: "tgsecret-SECRET-xyz789",
  OWNER_CHAT_ID: "4242", RELAY_URL: "https://relay.example", RELAY_KEY: "relaykey-SECRET-555555", GH_TOKEN: "github_pat_SECRET_999999", GH_REPO: "owner/decodeher" };

function storage() {
  const m = new Map(); let alarm = null;
  return {
    m,
    async get(k) { return m.has(k) ? structuredClone(m.get(k)) : undefined; },
    async put(k, v) { m.set(k, structuredClone(v)); },
    async delete(k) { return m.delete(k); },
    async getAlarm() { return alarm; },
    async setAlarm(t) { alarm = t; },
    get alarm() { return alarm; },
  };
}

// one fresh world per test: storage, DO instance, env, fetch recorder
function world({ relay, insights = 404 } = {}) {
  const st = storage(), env = { ...SECRETS }, ctx = { storage: st };
  const obj = new HQ(ctx, env);
  env.HQ = { idFromName: () => "main", get: () => obj };
  env.ASSETS = { fetch: async () => new Response("<html>dashboard</html>", { headers: { "Content-Type": "text/html" } }) };
  const w = { st, env, obj, calls: [], relay: relay ?? { paused: false, tokenAgeDays: 2, queue: [], log: [] }, relayDown: false, tgDown: false, ghDown: false, insights, msgId: 100 };
  globalThis.fetch = async (url, opts = {}) => {
    url = String(url);
    const body = opts.body ? (() => { try { return JSON.parse(opts.body); } catch { return opts.body; } })() : null;
    const c = { url, method: opts.method || "GET", headers: opts.headers || {}, body }; w.calls.push(c);
    if (url.startsWith("https://api.telegram.org/")) {
      if (w.tgDown) return new Response("bad gateway", { status: 502 });
      return Response.json({ ok: true, result: url.endsWith("/sendMessage") || url.endsWith("/sendVideo") ? { message_id: ++w.msgId } : true });
    }
    if (url.startsWith("https://api.github.com/")) {
      if (w.ghDown) throw new Error("network down");
      return new Response(null, { status: 204 });
    }
    if (url.startsWith(SECRETS.RELAY_URL)) {
      if (w.relayDown) throw new TypeError("fetch failed");
      if (c.headers.Authorization !== `Bearer ${SECRETS.RELAY_KEY}`) return new Response("decodeher relay");
      const p = url.slice(SECRETS.RELAY_URL.length);
      if (p === "/status") return Response.json(structuredClone(w.relay));
      if (p.startsWith("/insights")) return w.insights === 404 ? new Response("not found", { status: 404 }) : Response.json(w.insights);
      if (p === "/pause" || p === "/resume") { w.relay.paused = p === "/pause"; return Response.json({ ok: true, paused: w.relay.paused }); }
      return new Response("not found", { status: 404 });
    }
    throw new Error("unexpected fetch " + url);
  };
  w.tgCalls = (method) => w.calls.filter((c) => c.url.startsWith("https://api.telegram.org/") && (!method || c.url.endsWith("/" + method)));
  w.ghCalls = () => w.calls.filter((c) => c.url.startsWith("https://api.github.com/"));
  w.relayCalls = () => w.calls.filter((c) => c.url.startsWith(SECRETS.RELAY_URL));
  w.req = (path, { method = "GET", headers = {}, body } = {}) =>
    worker.fetch(new Request("https://hq.example" + path, { method, headers, body: body === undefined ? undefined : typeof body === "string" ? body : JSON.stringify(body) }), env, {});
  let uid = 1;
  w.tg = (update, secret = SECRETS.TELEGRAM_SECRET) => w.req("/tg", { method: "POST", headers: { "X-Telegram-Bot-Api-Secret-Token": secret, "Content-Type": "application/json" }, body: { update_id: uid++, ...update } });
  w.say = (text, chat = 4242) => w.tg({ message: { message_id: 1, chat: { id: chat }, from: { id: chat }, text } });
  w.auth = { Authorization: `Bearer ${SECRETS.HQ_KEY}`, "Content-Type": "application/json" };
  return w;
}
const lastText = (w) => { const s = w.tgCalls("sendMessage"); return s.length ? s[s.length - 1].body.text : ""; };
const item = (o) => ({ id: "08-w2-abcd", title: "08-W2-just-ask", key: "deadbeefcafe0000.mp4", at: at("2026-10-16", "08:30"), status: "queued", caption: "CAPTION TEXT #private", thumbMs: 600, ...o });

// ---------- Telegram webhook ----------
test("webhook with a wrong or missing secret header is rejected", async () => {
  const w = world();
  assert.equal((await w.tg({ message: { chat: { id: 4242 }, text: "/status" } }, "wrong")).status, 403);
  assert.equal((await w.req("/tg", { method: "POST", body: { message: { chat: { id: 4242 }, text: "/status" } } })).status, 403);
  assert.equal(w.calls.length, 0, "nothing was sent anywhere");
});

test("a chat that isn't the owner's is ignored", async () => {
  const w = world();
  const r = await w.say("/status", 999);
  assert.equal(r.status, 200);
  assert.equal(w.tgCalls().length, 0); assert.equal(w.ghCalls().length, 0);
  await w.tg({ callback_query: { id: "cb1", data: "approve:x", from: { id: 999 }, message: { message_id: 5, chat: { id: 999 } } } });
  assert.equal(w.tgCalls().length + w.ghCalls().length, 0);
});

test("/status replies to the owner", async () => {
  const w = world({ relay: { paused: false, tokenAgeDays: 1, queue: [item({})], log: [] } });
  await w.req("/api/state", { method: "POST", headers: w.auth, body: { reels: [{ dir: "w2-20-x", title: "X", next: "render" }], factory: { running: { "w2-20-x": "render" } } } });
  await w.say("/status");
  const msgs = w.tgCalls("sendMessage"); assert.equal(msgs.length, 1);
  assert.equal(msgs[0].body.chat_id, "4242"); assert.equal(msgs[0].body.parse_mode, "HTML");
  assert.match(msgs[0].body.text, /DecodeHer status/); assert.match(msgs[0].body.text, /1 booked/); assert.match(msgs[0].body.text, /1 reel still in the works/);
});

test("/queue, /help, /make and /pause work", async () => {
  const w = world({ relay: { paused: false, tokenAgeDays: 1, queue: [item({})], log: [] } });
  await w.say("/queue"); assert.match(lastText(w), /08-W2-just-ask/);
  await w.say("/help"); assert.match(lastText(w), /\/resume/);
  await w.say("/make"); assert.equal(w.ghCalls().at(-1).body.event_type, "factory"); assert.match(lastText(w), /Started the factory/);
  await w.say("/pause"); assert.ok(w.relayCalls().some((c) => c.url.endsWith("/pause") && c.method === "POST")); assert.equal(w.relay.paused, true);
  await w.say("/stats"); assert.match(lastText(w), /How it's going/);
});

test("free text becomes a change request → GitHub manager-request with the text", async () => {
  const w = world();
  await w.say("make the captions <bigger> & white");
  const gh = w.ghCalls(); assert.equal(gh.length, 1);
  assert.equal(gh[0].url, "https://api.github.com/repos/owner/decodeher/dispatches");
  assert.equal(gh[0].headers.Authorization, `Bearer ${SECRETS.GH_TOKEN}`); assert.ok(gh[0].headers["User-Agent"]);
  assert.equal(gh[0].body.event_type, "manager-request");
  assert.equal(gh[0].body.client_payload.text, "make the captions <bigger> & white"); assert.ok(gh[0].body.client_payload.request_id);
  assert.match(lastText(w), /On it, I'll send a preview/);
  const reqs = await w.st.get("requests"); assert.equal(reqs.length, 1); assert.equal(reqs[0].state, "working");
});

test("a retried Telegram update (same update_id) is handled once", async () => {
  const w = world();
  const u = { update_id: 77, message: { chat: { id: 4242 }, text: "new outro please" } };
  for (let i = 0; i < 2; i++) await w.req("/tg", { method: "POST", headers: { "X-Telegram-Bot-Api-Secret-Token": SECRETS.TELEGRAM_SECRET }, body: u });
  assert.equal(w.ghCalls().length, 1);
});

test("GitHub down: the request is kept and the owner is told, no crash", async () => {
  const w = world(); w.ghDown = true;
  const r = await w.say("swap the voice");
  assert.equal(r.status, 200); assert.match(lastText(w), /couldn't start the work/);
  assert.equal((await w.st.get("requests"))[0].state, "not-started");
});

// ---------- previews and approvals ----------
test("preview event → message with Approve / Reject buttons", async () => {
  const w = world();
  const r = await w.req("/api/event", { method: "POST", headers: w.auth, body: { type: "preview", text: "New <captions>", reel: "w2-07", request_id: "r1", slot: "10-17 08:30" } });
  assert.equal(r.status, 200); const j = await r.json(); assert.ok(j.id);
  const m = w.tgCalls("sendMessage"); assert.equal(m.length, 1);
  assert.match(m[0].body.text, /New &lt;captions&gt;/, "outside text is HTML-escaped");
  const kb = m[0].body.reply_markup.inline_keyboard.flat();
  assert.deepEqual(kb.map((b) => b.callback_data), [`approve:${j.id}`, `reject:${j.id}`]);
  assert.match(kb[0].text, /Approve/); assert.match(kb[1].text, /Reject/);
});

test("preview with a video URL is sent as a video (by URL) with the buttons", async () => {
  const w = world();
  await w.req("/api/event", { method: "POST", headers: w.auth, body: { type: "preview", text: "look", preview_url: "https://example.com/p.mp4" } });
  const v = w.tgCalls("sendVideo"); assert.equal(v.length, 1); assert.equal(v[0].body.video, "https://example.com/p.mp4");
  assert.equal(v[0].body.reply_markup.inline_keyboard[0].length, 2);
});

test("tapping Approve → GitHub approve with the pending id + answerCallbackQuery; a 2nd tap does nothing", async () => {
  const w = world();
  const { id } = await (await w.req("/api/event", { method: "POST", headers: w.auth, body: { type: "preview", text: "x", reel: "w2-07", request_id: "r1", slot: "s" } })).json();
  const cq = { callback_query: { id: "cbq-1", data: `approve:${id}`, from: { id: 4242 }, message: { message_id: 101, chat: { id: 4242 } } } };
  await w.tg(cq);
  const gh = w.ghCalls(); assert.equal(gh.length, 1);
  assert.equal(gh[0].body.event_type, "approve"); assert.equal(gh[0].body.client_payload.id, id); assert.equal(gh[0].body.client_payload.request_id, "r1");
  const ans = w.tgCalls("answerCallbackQuery"); assert.equal(ans.length, 1); assert.equal(ans[0].body.callback_query_id, "cbq-1");
  const ed = w.tgCalls("editMessageReplyMarkup"); assert.equal(ed.length, 1); assert.deepEqual(ed[0].body.reply_markup.inline_keyboard, []);
  assert.equal((await w.st.get("pending"))[id].state, "approved");
  await w.tg({ callback_query: { ...cq.callback_query, id: "cbq-2" } });
  assert.equal(w.ghCalls().length, 1, "no second dispatch");
  assert.match(w.tgCalls("answerCallbackQuery").at(-1).body.text, /Already approved/);
});

test("tapping Reject → GitHub reject", async () => {
  const w = world();
  const { id } = await (await w.req("/api/event", { method: "POST", headers: w.auth, body: { type: "preview", text: "x" } })).json();
  await w.tg({ callback_query: { id: "c", data: `reject:${id}`, from: { id: 4242 }, message: { message_id: 1, chat: { id: 4242 } } } });
  assert.equal(w.ghCalls()[0].body.event_type, "reject");
});

test("Telegram down: events still succeed, nothing crashes", async () => {
  const w = world(); w.tgDown = true;
  for (const type of ["preview", "error", "done", "activity"]) assert.equal((await w.req("/api/event", { method: "POST", headers: w.auth, body: { type, text: "t" } })).status, 200);
  assert.equal((await w.say("/status")).status, 200);
});

// ---------- the API ----------
test("POST /api/state and /api/event need the Bearer key", async () => {
  const w = world();
  for (const p of ["/api/state", "/api/event"]) {
    assert.equal((await w.req(p, { method: "POST", body: { type: "activity" } })).status, 401);
    assert.equal((await w.req(p, { method: "POST", headers: { Authorization: "Bearer nope" }, body: { type: "activity" } })).status, 401);
    assert.equal((await w.req(p, { method: "POST", headers: { Authorization: SECRETS.HQ_KEY }, body: { type: "activity" } })).status, 401);
  }
  assert.equal(await w.st.get("snapshot"), undefined);
  assert.equal((await w.req("/api/state", { method: "POST", headers: w.auth, body: { reels: [] } })).status, 200);
  assert.ok(await w.st.get("snapshotAt"));
  assert.equal((await w.req("/api/state", { method: "POST", headers: w.auth, body: "not json" })).status, 400);
  assert.equal((await w.req("/api/event", { method: "POST", headers: w.auth, body: { type: "weird" } })).status, 400);
});

test("GET /api/state merges snapshot + relay + manager, has CORS and no secrets/captions/media keys", async () => {
  const w = world({ relay: { paused: false, tokenAgeDays: 3, queue: [item({ coverKey: "c0ffee.jpg", coverUrl: "https://relay.example/m/c0ffee.jpg" })], log: ["2026-10-16T00:00:00Z  container 1 for x"] } });
  // a snapshot that (wrongly) contains a secret must still not leak it
  await w.req("/api/state", { method: "POST", headers: w.auth, body: { reels: [{ dir: "w2-1", next: "voice" }], note: "oops " + SECRETS.RELAY_KEY } });
  await w.req("/api/event", { method: "POST", headers: w.auth, body: { type: "activity", text: "Rendering w2-1" } });
  const r = await w.req("/api/state"); assert.equal(r.status, 200);
  assert.equal(r.headers.get("Access-Control-Allow-Origin"), "*");
  const text = await r.text(), j = JSON.parse(text);
  for (const v of Object.values(SECRETS).filter((v) => v.includes("SECRET"))) assert.ok(!text.includes(v), "leaked " + v);
  assert.ok(!text.includes("CAPTION TEXT"), "caption stripped"); assert.ok(!text.includes("deadbeefcafe"), "media key stripped"); assert.ok(!text.includes("c0ffee"), "cover key stripped");
  assert.equal(j.reels.length, 1); assert.equal(j.relay.queue[0].title, "08-W2-just-ask"); assert.equal(j.relay.ok, true);
  assert.equal(j.manager.at(-1).text, "Rendering w2-1"); assert.equal(j.stale.factory, false); assert.equal(j.stale.unfinished, 1);
  const pre = await w.req("/api/state", { method: "OPTIONS" }); assert.equal(pre.status, 204);
});

test("other paths go to the static dashboard", async () => {
  const w = world();
  assert.match(await (await w.req("/")).text(), /dashboard/);
  assert.equal((await w.req("/api/nope")).status, 404);
});

// ---------- the alarm ----------
test("alarm announces a NEW post once (not twice), with its link", async () => {
  fakeNow = at("2026-10-16", "09:00");
  const w = world({ relay: { paused: false, tokenAgeDays: 1, queue: [item({}), item({ id: "old", title: "07-W2-old", status: "posted", permalink: "https://ig/old" })], log: [] } });
  await w.obj.alarm();
  assert.equal(w.tgCalls("sendMessage").length, 0, "first look only remembers (old posts are not re-announced)");
  assert.ok(w.st.alarm > fakeNow, "next alarm set");
  w.relay.queue[0] = item({ status: "posted", permalink: "https://www.instagram.com/reel/ABC/", postedAt: fakeNow });
  await w.obj.alarm();
  const m = w.tgCalls("sendMessage"); assert.equal(m.length, 1);
  assert.match(m[0].body.text, /Posted/); assert.match(m[0].body.text, /08-W2-just-ask/); assert.match(m[0].body.text, /instagram\.com\/reel\/ABC/);
  await w.obj.alarm();
  assert.equal(w.tgCalls("sendMessage").length, 1, "not announced twice");
});

test("alarm announces failed / skipped / token errors once", async () => {
  fakeNow = at("2026-10-16", "09:00");
  const w = world({ relay: { paused: false, tokenAgeDays: 1, queue: [item({}), item({ id: "b", title: "09-W2-b" })], log: ["2026-10-15T10:00:00Z  token refreshed"] } });
  await w.obj.alarm();
  w.relay.queue[0].status = "failed"; w.relay.queue[0].error = "ERROR: bad video";
  w.relay.queue[1].status = "skipped";
  w.relay.log.push("2026-10-16T03:20:00Z  TOKEN/ACCOUNT ERROR: Error validating access token");
  await w.obj.alarm(); await w.obj.alarm();
  const t = w.tgCalls("sendMessage").map((c) => c.body.text).join("\n---\n");
  assert.equal(w.tgCalls("sendMessage").length, 3, t);
  assert.match(t, /failed/); assert.match(t, /skipped/); assert.match(t, /Instagram login problem/);
});

test("10:00 IST digest: yesterday's posts + insights, once a day", async () => {
  fakeNow = at("2026-10-16", "09:55");
  const y = at("2026-10-15", "21:00");
  const w = world({ relay: { paused: false, tokenAgeDays: 1, queue: [item({ status: "posted", postedAt: y, at: y, permalink: "https://ig/p1", title: "05-W2-test" }), item({ id: "n", title: "06-W2-next", at: at("2026-10-16", "21:00") })], log: [] },
    insights: { account: { followers_count: 321 }, reels: [{ title: "05-W2-test", permalink: "https://ig/p1", views: 1234, likes: 56, shares: 7, saved: 8, ig_reels_avg_watch_time: 4500 }] } });
  await w.obj.alarm();
  assert.equal(w.tgCalls("sendMessage").length, 0, "no digest before 10:00");
  fakeNow = at("2026-10-16", "10:05");
  await w.obj.alarm();
  const m = w.tgCalls("sendMessage"); assert.equal(m.length, 1);
  assert.match(m[0].body.text, /Good morning/); assert.match(m[0].body.text, /05-W2-test/); assert.match(m[0].body.text, /1234 views/);
  assert.match(m[0].body.text, /avg watch 4\.5 s/); assert.match(m[0].body.text, /Followers: 321/); assert.match(m[0].body.text, /21:00/);
  fakeNow = at("2026-10-16", "10:15"); await w.obj.alarm();
  assert.equal(w.tgCalls("sendMessage").length, 1, "once a day");
  fakeNow = at("2026-10-17", "10:01"); await w.obj.alarm();
  assert.equal(w.tgCalls("sendMessage").length, 2, "again the next day");
});

test("digest still goes out when the relay has no /insights (404)", async () => {
  fakeNow = at("2026-10-16", "10:30");
  const w = world({ relay: { paused: false, tokenAgeDays: 1, queue: [], log: [] }, insights: 404 });
  await w.obj.alarm();
  const m = w.tgCalls("sendMessage"); assert.equal(m.length, 1); assert.match(m[0].body.text, /No reels went out yesterday/);
});

test("stale factory warning: once a day, only while reels are unfinished", async () => {
  fakeNow = at("2026-10-16", "09:00");
  const w = world();
  await w.req("/api/state", { method: "POST", headers: w.auth, body: { reels: [{ dir: "w2-30", next: "voice", queued: false, posted: "" }, { dir: "w2-31", next: "posted", queued: false, posted: "posted · 10-15 21:00" }] } });
  fakeNow += 24 * 3600e3;   // 24 h later (09:00 IST, before the digest hour)
  await w.obj.alarm(); assert.equal(w.tgCalls("sendMessage").length, 0, "not stale yet");
  fakeNow = (await w.st.get("snapshotAt")) + 27 * 3600e3;
  const before = w.tgCalls("sendMessage").length;
  await w.obj.alarm(); await w.obj.alarm();
  const warns = w.tgCalls("sendMessage").slice(before).filter((c) => /hasn't checked in/.test(c.body.text));
  assert.equal(warns.length, 1); assert.match(warns[0].body.text, /1 reel is still unfinished/);
  fakeNow += 24 * 3600e3; await w.obj.alarm();
  assert.equal(w.tgCalls("sendMessage").filter((c) => /hasn't checked in/.test(c.body.text)).length, 2, "again the next day");
});

test("no stale warning when every reel is finished", async () => {
  fakeNow = at("2026-10-16", "09:00");
  const w = world();
  await w.req("/api/state", { method: "POST", headers: w.auth, body: { reels: [{ dir: "w2-31", next: "post", queued: true }] } });
  fakeNow += 40 * 3600e3; await w.obj.alarm();
  assert.equal(w.tgCalls("sendMessage").filter((c) => /hasn't checked in/.test(c.body.text)).length, 0);
});

test("relay down: alarm, /status, /queue and GET /api/state don't crash", async () => {
  fakeNow = at("2026-10-16", "09:00");
  const w = world(); w.relayDown = true;
  await w.obj.alarm(); assert.ok(w.st.alarm > fakeNow, "alarm rescheduled");
  assert.equal((await w.say("/status")).status, 200); assert.match(lastText(w), /couldn't reach the posting service/);
  assert.equal((await w.say("/queue")).status, 200); assert.match(lastText(w), /couldn't reach/);
  assert.equal((await w.say("/pause")).status, 200); assert.match(lastText(w), /nothing changed/);
  const r = await w.req("/api/state"); assert.equal(r.status, 200); assert.equal((await r.json()).stale.relay, true);
  // after ~1 h of failures the owner hears about it once
  for (let i = 0; i < 8; i++) { fakeNow += 10 * 60e3; await w.obj.alarm(); }
  assert.equal(w.tgCalls("sendMessage").filter((c) => /haven't been able to reach the posting service/.test(c.body.text)).length, 1);
  w.relayDown = false; fakeNow += 10 * 60e3; await w.obj.alarm();
  assert.ok(w.tgCalls("sendMessage").some((c) => /reachable again/.test(c.body.text)));
});

test("relay answering garbage (HTML / 500) doesn't crash the alarm", async () => {
  fakeNow = at("2026-10-16", "09:00");
  const w = world();
  w.relay = "<html>oops</html>";
  await w.obj.alarm(); assert.ok(w.st.alarm > fakeNow);
});

test.after(() => { Date.now = realNow; });
