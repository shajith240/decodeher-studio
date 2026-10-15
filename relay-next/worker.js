import { DurableObject } from "cloudflare:workers";
// @thedecodeher posting relay (Cloudflare Worker + one SQLite Durable Object). Runs in the cloud, so posts go out with
// the laptop off. Separate from the Spot the Con relay: its own token, media and queue.
//   - holds the Instagram token and refreshes it weekly (long-lived tokens last 60 days)
//   - hosts each reel MP4 at a public, unguessable URL (Instagram downloads it from there), stored in 1.5 MB chunks
//   - a queue of reels with UTC publish times; every 10 min (Durable Object alarm) it posts what is due:
//     due → REELS container → (next tick) FINISHED → media_publish → permalink → media deleted
// Authenticated API (Bearer RELAY_KEY): PUT/DELETE /media/<key>, PUT /ig-token, GET /status, GET|PUT /queue, POST /pause|/resume
// Public: GET/HEAD /m/<key>.mp4

const GRAPH = "https://graph.instagram.com/v25.0";
const CH = 1.5 * 1024 * 1024;

export class Store extends DurableObject {
  constructor(ctx, env) { super(ctx, env); this.ctx = ctx; this.env = env; }
  // the clock: a Durable Object alarm every 10 min (the account's 5 free cron triggers are all used by the Spot the Con relay)
  async alarm() {
    try { await this.runTick(this.env.PUBLIC_URL); } finally { await this.ctx.storage.setAlarm(Date.now() + 10 * 60e3); }
  }
  async ensureAlarm() { if (!(await this.ctx.storage.getAlarm())) await this.ctx.storage.setAlarm(Date.now() + 60e3); }
  // audit 10-15 M1: one tick at a time — the 10-min alarm and the laptop's /tick nudges could overlap (awaits on fetch interleave)
  async runTick(origin) {
    if (this.ticking) return;
    this.ticking = true;
    try { await tick(this.env, origin, this); } finally { this.ticking = false; }
  }
  async putMedia(key, bytes) {
    const at = Date.now(), n = Math.ceil(bytes.byteLength / CH);
    for (let i = 0; i < n; i++) await this.ctx.storage.put(`m:${key}#${String(i).padStart(4, "0")}`, { bytes: bytes.slice(i * CH, (i + 1) * CH) });
    await this.ctx.storage.put(`m:${key}`, { chunks: n, size: bytes.byteLength, at });
  }
  async getMeta(key) { return (await this.ctx.storage.get(`m:${key}`)) || null; }
  async getChunk(key, i) { return (await this.ctx.storage.get(`m:${key}#${String(i).padStart(4, "0")}`))?.bytes || null; }
  async dropMedia(key) {
    const m = await this.getMeta(key); if (!m) return false;
    for (let i = 0; i < m.chunks; i++) await this.ctx.storage.delete(`m:${key}#${String(i).padStart(4, "0")}`);
    await this.ctx.storage.delete(`m:${key}`); return true;
  }
  async load(k) { return (await this.ctx.storage.get(k)) ?? null; }
  // audit 10-15 H1: the laptop PUTs the whole queue; it must never revert what the relay did meanwhile (posted → queued = a double
  // post; processing → queued = a second container). Items the relay has started keep the relay's posting fields.
  async putQueue(incoming) {
    const cur = (await this.load("queue")) || [], byId = new Map(cur.map((x) => [x.id, x]));
    const merged = incoming.map((x) => { const c = byId.get(x.id);
      return c && c.status !== "queued" ? { ...x, ...pick(c, SERVER_FIELDS) } : x; });
    await this.save("queue", merged); return merged.length;
  }
  async save(k, v) { await this.ctx.storage.put(k, v); }
}

const store = (env) => env.STORE.get(env.STORE.idFromName("main"));
const SERVER_FIELDS = ["status", "container", "startedAt", "mediaId", "permalink", "postedAt", "error", "tries", "firstErrAt", "lastErrAt", "noCover", "noAiFlag"];
const pick = (o, ks) => Object.fromEntries(ks.filter((k) => k in o).map((k) => [k, o[k]]));

async function ig(method, path, params, token) {
  const qs = new URLSearchParams({ ...params, access_token: token });
  const r = await fetch(method === "GET" ? `${GRAPH}/${path}?${qs}` : `${GRAPH}/${path}`, method === "GET" ? {} : { method, body: qs });
  const j = await r.json();
  if (j.error) throw new Error(`${path}: ${j.error.message}`);
  return j;
}

async function log(s, msg) {
  const l = (await s.load("log")) || [];
  l.push(`${new Date().toISOString()}  ${msg}`);
  await s.save("log", l.slice(-80));
}

async function tick(env, origin, s) {   // runs INSIDE the Durable Object (s = the Store instance)
  const tok = await s.load("ig:token");
  if (!tok) return;
  // weekly refresh keeps the 60-day token alive indefinitely
  if (Date.now() - tok.at > 7 * 86400e3) {
    try {
      const r = await (await fetch(`https://graph.instagram.com/refresh_access_token?grant_type=ig_refresh_token&access_token=${encodeURIComponent(tok.token)}`)).json();
      if (r.access_token) { await s.save("ig:token", { token: r.access_token, at: Date.now() }); tok.token = r.access_token; await log(s, "token refreshed"); }
      else await log(s, `token refresh failed: ${r.error?.message || "unknown"}`);
    } catch (e) { await log(s, `token refresh failed: ${e.message}`); }
  }
  if (await s.load("paused")) return;
  const q = (await s.load("queue")) || [];
  let uid;
  try { uid = (await ig("GET", "me", { fields: "user_id" }, tok.token)).user_id; }
  catch (e) {   // audit M5: an expired/revoked token used to fail silently here
    const last = (await s.load("meErrAt")) || 0;
    if (Date.now() - last > 3600e3) { await s.save("meErrAt", Date.now()); await log(s, `TOKEN/ACCOUNT ERROR: ${e.message}`); }
    return;
  }
  let started = false;
  const changed = new Map();   // id → the fields this tick set (merged into the queue as it is at save time)
  const mark = (it, f) => { Object.assign(it, f); changed.set(it.id, { ...(changed.get(it.id) || {}), ...f }); };
  const persist = async () => { const cur = (await s.load("queue")) || [];
    await s.save("queue", cur.map((x) => changed.has(x.id) ? { ...x, ...changed.get(x.id) } : x)); };
  for (const it of q) {
    if (it.status === "queued" && it.lastErrAt && Date.now() - it.lastErrAt < 5 * 60e3) continue;   // audit H3: space retries ≥ 5 min
    try {
      if (it.status === "processing") {
        const st = await ig("GET", it.container, { fields: "status_code,status" }, tok.token);
        if (st.status_code === "FINISHED") {
          const done = await ig("POST", `${uid}/media_publish`, { creation_id: it.container }, tok.token);
          mark(it, { status: "posted", mediaId: done.id, postedAt: Date.now(), tries: 0 });
          await persist();   // audit H2: save "posted" the moment it is true, before anything else can fail
          const p = await ig("GET", done.id, { fields: "permalink" }, tok.token).catch(() => ({}));
          mark(it, { permalink: p.permalink || null });
          await s.dropMedia(it.key);
          await log(s, `POSTED ${it.title} → ${p.permalink || done.id}`);
        } else if (st.status_code === "PUBLISHED") {   // audit H2: it already went live (the publish answer was lost) — never "failed"
          mark(it, { status: "posted", postedAt: Date.now(), tries: 0 });
          await s.dropMedia(it.key);
          await log(s, `POSTED ${it.title} (container already published)`);
        } else if (st.status_code === "ERROR" || st.status_code === "EXPIRED" || Date.now() - it.startedAt > 3 * 3600e3) {
          mark(it, { status: "failed", error: `${st.status_code}: ${st.status || "timed out"}` });
          await log(s, `FAILED ${it.title}: ${it.error}`);
        }
      } else if (it.status === "queued" && !started && it.at <= Date.now()) {
        if (Date.now() - it.at > 12 * 3600e3) { it.status = "skipped"; await log(s, `SKIPPED ${it.title}: more than 12 h late`); continue; }
        const c = await ig("POST", `${uid}/media`, { media_type: "REELS", video_url: `${origin}/m/${it.key}`, caption: Array.from(it.caption).slice(0, 2200).join(""),
          share_to_feed: "true", thumb_offset: String(it.thumbMs ?? 1500),
          ...(it.noAiFlag ? {} : { is_ai_generated: "true" }),   // AI-info label (API param per Meta changelog 06-2026)
          ...(it.coverUrl && !it.noCover ? { cover_url: it.coverUrl } : {}) }, tok.token);
        mark(it, { status: "processing", container: c.id, startedAt: Date.now(), tries: 0 });
        started = true;   // one new upload per tick
        await log(s, `container ${c.id} for ${it.title}`);
      }
    } catch (e) {
      // audit H3: gentle retries — ≥ 5 min apart; give up only after 6 tries AND an hour of trying (a 4-min blip used to kill a post)
      const now = Date.now(), tries = (it.tries || 0) + 1, f = { tries, lastErrAt: now, firstErrAt: it.firstErrAt || now };
      if (/is_ai_generated/i.test(e.message)) f.noAiFlag = true;                   // AI-label param rejected → post without it
      if (it.coverUrl && /cover|thumb|image/i.test(e.message)) f.noCover = true;   // cover rejected → fall back to the video frame
      if (tries >= 6 && now - f.firstErrAt > 3600e3) { f.status = "failed"; f.error = e.message; }
      mark(it, f);
      await log(s, `error on ${it.title} (try ${tries}): ${e.message}`);
    }
  }
  if (changed.size) await persist();   // audit H1: merge into the queue AS IT IS NOW (the laptop may have edited it meanwhile)
}

export default {
  async fetch(req, env, ctx) {
    try { return await handle(req, env, ctx); } catch (e) { return new Response(`error: ${e.stack || e.message}`, { status: 500 }); }
  },
};

async function handle(req, env, ctx) {
  {
    const url = new URL(req.url), s = store(env);
    if (url.pathname.startsWith("/m/") && (req.method === "GET" || req.method === "HEAD")) {
      const key = url.pathname.slice(3), meta = await s.getMeta(key);
      if (!meta) return new Response("not found", { status: 404 });
      const type = /\.jpe?g$/i.test(key) ? "image/jpeg" : /\.png$/i.test(key) ? "image/png" : "video/mp4";   // audit M2
      const headers = { "Content-Type": type, "Content-Length": String(meta.size), "Cache-Control": "public, max-age=3600", "Accept-Ranges": "none" };
      if (req.method === "HEAD") return new Response(null, { headers });
      const { readable, writable } = new FixedLengthStream(meta.size);
      ctx.waitUntil((async () => { const w = writable.getWriter(); for (let i = 0; i < meta.chunks; i++) await w.write(new Uint8Array(await s.getChunk(key, i))); await w.close(); })());
      return new Response(readable, { headers });
    }
    if (req.headers.get("Authorization") !== `Bearer ${env.RELAY_KEY}`) return new Response("decodeher relay");
    await s.ensureAlarm();
    if (url.pathname.startsWith("/media/")) {
      const key = url.pathname.slice(7);
      if (req.method === "PUT") { await s.putMedia(key, await req.arrayBuffer()); return Response.json({ ok: true, url: `${url.origin}/m/${key}` }); }
      if (req.method === "DELETE") return Response.json({ ok: true, deleted: await s.dropMedia(key) });
    }
    if (url.pathname === "/ig-token" && req.method === "PUT") { const t = await req.json(); await s.save("ig:token", { token: t.token, at: t.at || Date.now() }); return Response.json({ ok: true }); }
    if (url.pathname === "/queue" && req.method === "GET") return Response.json((await s.load("queue")) || []);
    if (url.pathname === "/queue" && req.method === "PUT") { const n = await s.putQueue(await req.json()); return Response.json({ ok: true, items: n }); }
    if (url.pathname === "/pause") { await s.save("paused", true); return Response.json({ ok: true, paused: true }); }
    if (url.pathname === "/resume") { await s.save("paused", false); return Response.json({ ok: true, paused: false }); }
    if (url.pathname === "/tick") { await s.runTick(url.origin); return Response.json({ ok: true }); }
    if (url.pathname === "/insights" && req.method === "GET") {   // 10-15 growth: READ-ONLY stats for the manager's digest
      const t = await s.load("ig:token"); if (!t) return Response.json({ error: "no token" }, { status: 503 });
      const days = Math.min(30, Number(url.searchParams.get("days") || 7)), since = Date.now() - days * 86400e3;
      const g = async (path, params) => { try { return await ig("GET", path, params, t.token); } catch (e) { return { error: e.message }; } };
      const me = await g("me", { fields: "username,followers_count,media_count" });
      const posted = ((await s.load("queue")) || []).filter((x) => x.status === "posted" && x.mediaId && (x.postedAt || 0) >= since);
      const reels = [];
      for (const x of posted) {
        let m = await g(`${x.mediaId}/insights`, { metric: "reach,views,likes,comments,shares,saved,ig_reels_avg_watch_time,ig_reels_video_view_total_time" });
        if (m.error) m = await g(`${x.mediaId}/insights`, { metric: "reach,likes,comments,shares,saved" });
        const v = Object.fromEntries((m.data || []).map((d) => [d.name, d.values?.[0]?.value ?? d.total_value?.value ?? null]));
        reels.push({ title: x.title, permalink: x.permalink || null, postedAt: x.postedAt, ...v, ...(m.error ? { error: m.error } : {}) });
      }
      return Response.json({ account: me.error ? { error: me.error } : me, reels });
    }
    if (url.pathname === "/status") {
      const t = await s.load("ig:token");
      return Response.json({ paused: !!(await s.load("paused")), tokenAgeDays: t ? Math.floor((Date.now() - t.at) / 86400e3) : null,
        queue: ((await s.load("queue")) || []).map(({ caption, ...r }) => r), log: ((await s.load("log")) || []).slice(-15) });
    }
    return new Response("not found", { status: 404 });
  }
}
