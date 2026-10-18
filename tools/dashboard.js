// Production board (owner 10-14: "a clean UI, no AI slop"): one row per reel, one column per stage, the posting queue, and what
// is running right now. Reads the files on disk + `ig_queue.js ids`; nothing to configure.
// Usage: node tools/dashboard.js   →   http://localhost:4317 (pixel studio, tools/board/studio.html) · /table (this table) · /state.json
//        node tools/dashboard.js --snapshot   →   print one snapshot as JSON and exit, no server (cloud: tools/cloud/report.py → HQ)
const http = require("http"), fs = require("fs"), path = require("path"), { execFile, execSync } = require("child_process");
const ROOT = path.resolve(__dirname, ".."), REELS = path.join(ROOT, "reels"), PORT = 4317;
const exists = (p) => fs.existsSync(p), ls = (p) => (exists(p) ? fs.readdirSync(p) : []);
// audit F3: a file caught mid-write parses as garbage for a moment; keep the last good value per path instead of flashing
// the default (a missing file still gives the default, so deleted reels really disappear)
const lastGood = new Map();
const json = (p, d) => {
  let raw; try { raw = fs.readFileSync(p, "utf8"); } catch { lastGood.delete(p); return d; }
  try { const v = JSON.parse(raw); lastGood.set(p, v); return v; } catch { return lastGood.has(p) ? lastGood.get(p) : d; }
};
// audit F8: one `ps` per snapshot (cached 1 s, 2 s timeout) and one read of the activity log tail, shared by every helper
let psCache = { t: 0, out: "" };
function psText() {
  if (Date.now() - psCache.t < 1000) return psCache.out;
  let out = psCache.out; try { out = execSync("ps -eo pid=,args=", { encoding: "utf8", timeout: 2000 }); } catch {}
  psCache = { t: Date.now(), out }; return out;
}
let logCache = { key: "", lines: [] };
function logLines() {   // logs/activity.log, last ~64 KB, oldest first
  const f = path.join(ROOT, "logs/activity.log"); let st; try { st = fs.statSync(f); } catch { return []; }
  const key = st.size + ":" + st.mtimeMs; if (key === logCache.key) return logCache.lines;
  const len = Math.min(st.size, 65536), buf = Buffer.alloc(len), fd = fs.openSync(f, "r");
  try { fs.readSync(fd, buf, 0, len, st.size - len); } finally { fs.closeSync(fd); }
  let lines = buf.toString("utf8").trim().split("\n"); if (len < st.size) lines = lines.slice(1);   // drop the cut first line
  logCache = { key, lines }; return lines;
}

let queue = [], queueAt = 0, queueOkAt = 0, queueStale = false;
function refreshQueue() {   // the relay queue, at most once a minute; on a failure keep the last list and say it may be stale (F16)
  if (Date.now() - queueAt < 60e3) return; queueAt = Date.now();
  execFile("node", [path.join(__dirname, "ig_queue.js"), "ids"], { timeout: 30e3 }, (e, out) => {
    const rows = e ? null : parseIds(out);
    if (rows && (rows.length || !out.trim())) { queue = rows; queueOkAt = Date.now(); queueStale = false; } else queueStale = true;
    soon();
  });
}

function parseIds(out) {   // `ig_queue.js ids` lines → [{id, status, at, title}]
  return out.trim().split("\n").map((l) => l.match(/^(\S+)\s+(\S+)\s+(\d{4}-\d\d-\d\d \d\d:\d\d IST)\s+(.*)$/)).filter(Boolean)
    .map((m) => ({ id: m[1], status: m[2], at: m[3], title: m[4] }));
}

function reelRow(dir) {   // a rendered reel counts as judged (its judge files may be cleared later)
  const R = path.join(REELS, dir), cfg = json(path.join(R, "reel.json"), {}), script = json(path.join(R, "assets/vo/script.json"), []);
  const shots = json(path.join(R, "shots.json"), []), body = shots.filter((s) => s.q !== "OUTRO");
  const lines = ls(path.join(R, "assets/vo")).filter((f) => /^l\d\d\.wav$/.test(f)).length;
  const timed = exists(path.join(R, "assets/timing.js")) && fs.readFileSync(path.join(R, "assets/timing.js"), "utf8").includes('"words"');
  const clips = body.filter((_, n) => ls(path.join(R, "clips/cand", String(n).padStart(2, "0"))).some((f) => f.endsWith(".mp4"))).length;
  const judged = ls(path.join(R, "clips/judge")).length, sheets = ls(path.join(R, "clips/sheets")).filter((f) => f.endsWith(".jpg")).length;
  const video = path.join(ROOT, "deliverables/week-2", dir + ".mp4");
  const q = queue.find((x) => x.title.includes(dir.split("-").slice(2).join("-").slice(0, 20)) || x.title.includes(dir.slice(6, 26)));
  const stage = (done, total) => (total && done >= total ? "done" : done ? `${done}/${total}` : "");
  // where this reel IS in the line: the station it needs next (voice → scout → judge → edit → mix → render → post → posted)
  // 10-15: the 350 MB master is deleted once a reel is booked, so "has a video" = master on disk OR booked/posted (logs/queued marker)
  const posted = q && q.status === "posted", queued = q && q.status === "queued", hasVideo = exists(video) || exists(path.join(ROOT, "logs/queued", dir));
  const judgedDone = hasVideo || (sheets && judged >= sheets);
  // 10-16: a finished / booked / posted reel never goes back to Scout because the manager cleaned its raw clips off the disk
  let next = posted ? "posted" : (q || hasVideo) ? "post" : !timed ? "voice" : clips < body.length - 1 ? "scout" : !judgedDone ? "judge" : "edit";
  // the factory's own stage wins (owner 10-14: 6 reels sat on Edit's belt while they were really back with Scout for a 2nd clip search)
  const fst = (json(path.join(ROOT, "logs/factory.json"), {}).reels || {})[dir];
  // 10-15 fix: Mix was mapped to Judge and Render to Edit, so a mixing reel sat at the Judge desk; inside the render stage the clip
  // cut is Edit's job and the frame render is Render's (told apart by which program is running for this reel)
  const BY_STAGE = { voice: "voice", plan: "scout", clips: "scout", research: "scout", mix: "mix", sheets: "judge", judge: "judge", render: "render", queue: "post" };
  if (BY_STAGE[fst]) next = BY_STAGE[fst];
  if (fst === "render" && cutting(dir)) next = "edit";
  return { dir, title: cfg.title || dir, approval: cfg.approval || "",   // 10-18: "pending" = waiting for the owner's OK (the factory leaves no park reason for it)
    voice: stage(timed ? script.length : Math.min(lines, script.length - 1), script.length),
    audio: exists(path.join(R, "assets/audio/final.wav")) ? "done" : "", clips: stage(clips, body.length),
    next, queued: !!queued, judged: hasVideo ? "done" : stage(judged, sheets || body.length), video: hasVideo ? "done" : "", posted: q ? `${q.status === "posted" ? "posted" : "queued"} · ${q.at.slice(5, 16)}` : "" };
}

function cutting(dir) {   // the render stage is still picking/cutting this reel's clips (Edit), not rendering frames yet
  return psText().split("\n").some((l) => /clippick\.py|clipcut\.py/.test(l) && l.includes(dir));
}
function managerState() {   // the Manager (tools/manager.py): status ok|checking|watching|fixing, the station it is at, what it did
  const m = json(path.join(ROOT, "logs/manager.json"), {}) || {};
  return { status: m.status || "off", text: m.text || "", target: m.target || "", at: m.at || "", queueUntil: m.queue_until || "",
    history: (m.history || []).slice(0, 20), needsOwner: (m.needs_owner || []).slice(0, 3) };
}

function feed() {   // the last 14 lines of logs/activity.log, newest first
  return logLines().slice(-14).reverse();
}
// per-station status for the pixel studio: what each worker is doing (or last did), in plain words, from the activity log
const STATIONS = { voice: ["Recording voice", "Voice ready"], scout: ["Clip search"], judge: ["Contact sheet", "Judging", "Judged"],
  edit: ["Picking clips", "Cutting clips"], mix: ["Audio mixing", "Audio mixed"], render: ["Rendering", "Rendered"], post: ["Queued", "Posted"] };
const JOB_OF = { voice: "recording a voice", scout: "searching clips", judge: "judging clips", edit: "cutting the clip film", mix: "mixing audio", render: "rendering a reel" };
function stations(run) {
  const log = logLines().slice().reverse();
  const out = {};
  for (const [k, prefixes] of Object.entries(STATIONS)) {
    const last = log.find((l) => prefixes.some((p) => l.slice(10).startsWith(p)));
    // each desk is busy only for its OWN step: the reel moves edit → mix → render, so Edit is free while Mix/Render hold it (owner 10-14)
    const busy = (k === "judge" && run.some((r) => r.startsWith("building contact sheets"))) ||
      (JOB_OF[k] && run.some((r) => r.startsWith(JOB_OF[k]))) || (k === "judge" && last && /^\S+\s+Judging(?! done)/.test(last) && !log.slice(0, log.indexOf(last)).some((l) => /Judged|Judging done/.test(l)));
    out[k] = { busy: !!busy, text: last ? last.slice(10) : "", at: last ? last.slice(0, 8) : "" };
  }
  // 10-15 fix (owner: "audio mixing is going on but every desk says on hold"): the factory's own running list is the truth —
  // the process scan above only knew old program names (Chatterbox voice) and missed the short mixing steps
  const FAC = { voice: "voice", plan: "scout", clips: "scout", research: "scout", mix: "mix", sheets: "judge", judge: "judge", render: "render", queue: "post" };
  const facNow = json(path.join(ROOT, "logs/factory.json"), {});
  for (const [dir, st] of Object.entries(facNow.running || {})) {
    const k = st === "render" && cutting(dir) ? "edit" : FAC[st]; if (!k || k === "post") continue;
    const t = (json(path.join(REELS, dir, "reel.json"), {}) || {}).title || dir;
    const say = { voice: "Recording voice", scout: "Clip search", judge: "Judging clips", edit: "Cutting clips", mix: "Audio mixing", render: "Rendering" }[k];
    out[k] = { busy: true, text: `${say} · ${t}`, at: (facNow.at || "").slice(11, 19) };
  }
  // Post is busy only while something really happens (owner 10-15): a queue job is running (factory lane "queue", or a
  // "Queuing post · X" line without its "done" yet), or a post is going live (2 min before its slot until the relay marks it posted).
  const booked = queue.filter((q) => q.status === "queued").sort((a, b) => a.at.localeCompare(b.at)), next = booked[0];
  const fac = json(path.join(ROOT, "logs/factory.json"), {}), facRun = Object.values(fac.running || {}).map(String);
  const qLine = log.find((l) => /^\S+\s+Queuing post /.test(l)), qTitle = qLine ? qLine.slice(10).replace(/^Queuing post (done )?· /, "") : "";
  const queuing = facRun.some((v) => /queue/i.test(v)) || (qLine && !/Queuing post done/.test(qLine) && (() => { const [h, m] = qLine.slice(0, 5).split(":").map(Number), d = new Date();
    const age = (d.getHours() * 60 + d.getMinutes()) - (h * 60 + m); return age >= 0 && age < 30; })());
  const slotMs = next ? new Date(next.at.replace(" IST", ":00+05:30").replace(" ", "T")).getTime() : NaN, mins = (slotMs - Date.now()) / 60e3;
  const live = queue.some((q) => /processing|container|publishing/i.test(q.status)) || (next && mins <= 2 && mins > -20);
  if (queuing) out.post = { busy: true, text: `Queuing post · ${qTitle}`, at: qLine ? qLine.slice(0, 8) : "" };
  else if (live) out.post = { busy: true, text: `Posting now · ${next ? next.title : ""}`, at: "" };
  else out.post = { busy: false, text: booked.length ? `${booked.length} booked · next ${next.at.slice(11, 16)}` : "Nothing booked", at: "" };
  return out;
}
function newest(glob1) {   // newest file among reels/*/<sub>/* or deliverables/week-2/*-frames.png, as a /media URL
  let best = null;
  for (const d of fs.readdirSync(REELS).filter((x) => /^[a-z]\d+-/.test(x))) {
    for (const f of ls(path.join(REELS, d, glob1))) if (/\.(jpg|png)$/.test(f)) {
      const p = path.join(REELS, d, glob1, f), t = fs.statSync(p).mtimeMs; if (!best || t > best.t) best = { t, p, reel: d, name: f };
    }
  }
  return best && { url: "/media/" + path.relative(ROOT, best.p), reel: best.reel, name: best.name, at: new Date(best.t).toISOString() };
}
function latestFrames() {
  const d = path.join(ROOT, "deliverables/week-2"); let best = null;
  for (const f of ls(d).filter((x) => x.endsWith("-frames.png"))) { const t = fs.statSync(path.join(d, f)).mtimeMs; if (!best || t > best.t) best = { t, f }; }
  return best && { url: "/media/deliverables/week-2/" + best.f, reel: best.f.replace("-frames.png", ""), at: new Date(best.t).toISOString() };
}
function running() {
  const jobs = [["vo_chatterbox", "recording a voice"], ["reel_vo.py", "recording a voice"], ["fetch_pool", "searching clips"], ["pinfetch", "searching clips"], ["clipsheet", "building contact sheets"],
    ["Judge every contact sheet", "judging clips"], ["You are the editor planning one Instagram Reel", "planning shots"],
    ["clipcut", "cutting the clip film"], ["hyperframes render", "rendering a reel"], ["reel_mix", "mixing audio"]];
  const ps = psText();
  // name the reel each job is working on: from its arguments, or from its working folder (renders run INSIDE the reel folder)
  const lines = ps.split("\n").map((l) => { const m = l.trim().match(/^(\d+)\s+(.*)$/); if (!m) return l;
    let cwd = ""; try { cwd = fs.readlinkSync(`/proc/${m[1]}/cwd`); } catch {}
    return m[2] + (cwd.includes("/reels/") ? " " + cwd : ""); });
  // only real job programs count: shells, greps and watch loops that merely MENTION a script name are not work (a stale wait loop showed Voice busy 10-15)
  const real = lines.filter((l) => !/(^|\/)(ba|z)?sh -c|\bu?grep\b|\bpgrep\b/.test(l));
  return jobs.flatMap(([k, label]) => { const hits = real.filter((l) => l.includes(k)); if (!hits.length) return [];
    const reels = [...new Set(hits.map((l) => (l.match(/reels\/([a-z]\d+-[\w-]+)/) || [])[1]).filter(Boolean))];
    return [label + (reels.length ? " · " + reels.map((r) => json(path.join(REELS, r, "reel.json"), {}).title || r).join(", ") : "")]; });
}

const page = (rows, jobs) => `<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="10">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>DecodeHer · production</title>
<style>
:root{--bg:#0b0b0c;--fg:#e8e6e3;--mute:#8a8a8f;--line:#232326;--acc:#b98cff}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 -apple-system,"Segoe UI",Inter,system-ui,sans-serif}
main{max-width:1060px;margin:0 auto;padding:40px 24px}
h1{font-size:20px;font-weight:600;margin:0 0 4px}h2{font-size:13px;font-weight:500;color:var(--mute);margin:30px 0 10px;text-transform:uppercase;letter-spacing:.06em}
.log{list-style:none;margin:0;padding:0;border-top:1px solid var(--line)}.log li{padding:7px 0;border-bottom:1px solid var(--line);font-size:14px}.log li:first-child{color:var(--fg)}.log li:not(:first-child){color:var(--mute)}.log time{display:inline-block;width:78px;color:var(--mute);font-variant-numeric:tabular-nums}p{margin:0;color:var(--mute)}
.now{margin:22px 0 0;font-size:14px}.now b{color:var(--acc);font-weight:500}
table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums}
th{font-size:12px;font-weight:500;color:var(--mute);text-align:left;padding:0 10px 10px;border-bottom:1px solid var(--line)}
td{padding:11px 10px;border-bottom:1px solid var(--line);font-size:14px;white-space:nowrap}
td.t{white-space:normal}td.t small{display:block;color:var(--mute);font-size:12px}
.done{color:var(--fg)}.done::before{content:"✓";color:var(--acc);margin-right:6px}.part{color:var(--mute)}.none{color:#3a3a3e}
@media(max-width:700px){main{padding:24px 16px}th:nth-child(3),td:nth-child(3),th:nth-child(5),td:nth-child(5){display:none}}
</style></head><body><main>
<h1>DecodeHer · week 2</h1><p>${rows.filter((r) => r.video === "done").length} of ${rows.length} reels rendered · ${rows.filter((r) => r.posted).length} in the posting queue</p>
<div class="now">${jobs.length ? "Running now: <b>" + jobs.join(" · ") + "</b>" : "Nothing running"}</div>
<h2>Activity</h2><ol class="log">${feed().map((l) => `<li><time>${l.slice(0, 8)}</time>${l.slice(10).replace(/&/g, "&amp;").replace(/</g, "&lt;")}</li>`).join("") || "<li>Nothing yet</li>"}</ol>
<h2>Reels</h2><table><tr><th>Reel</th><th>Voice</th><th>Audio</th><th>Clips</th><th>Judged</th><th>Video</th><th>Post</th></tr>
${rows.map((r) => `<tr><td class="t">${r.title}<small>${r.dir}</small></td>${["voice", "audio", "clips", "judged", "video", "posted"].map((k) => {
  const v = r[k]; return `<td class="${v === "done" ? "done" : v ? "part" : "none"}">${v === "done" ? "done" : v || "—"}</td>`; }).join("")}</tr>`).join("")}
</table></main></body></html>`;

// 10-15: every batch the factory works on (config.json factory.batches), not just week 2 — the w3 reels were invisible on the board
const batchDirs = () => { const cfg = json(path.join(ROOT, "config.json"), {}), bs = [...new Set([...((cfg.factory && cfg.factory.batches) || []), ...ls(REELS).filter((f) => f.endsWith("-batch.json")).map((f) => "reels/" + f)])];   // 10-17: every reels/*-batch.json, exactly like the factory (a new s2 batch was invisible)
  return [...new Set(bs.flatMap((b) => json(path.join(ROOT, b), [])).map((p) => path.basename(p)))].filter((d) => exists(path.join(REELS, d))); };
const snapshot = () => { const run = running(); return { reels: batchDirs().map(reelRow), running: run, activity: feed(), queue, stations: stations(run), manager: managerState(), media: { sheet: newest("clips/sheets"), frames: latestFrames() }, ver: pageVer(),
  queueStale, queueAt: queueOkAt ? new Date(queueOkAt).toISOString() : "" }; };
function pageVer() { try { return String(fs.statSync(path.join(__dirname, "board/studio.html")).mtimeMs); } catch { return ""; } }   // the board reloads itself when this changes

// --snapshot (cloud, 10-15): the same snapshot the board pushes, plus the factory's own view (logs/factory.json), printed once as JSON.
// Nothing below this block runs in this mode: no server, no watchers, no timers.
if (process.argv.includes("--snapshot")) {
  try { const out = require("child_process").execFileSync("node", [path.join(__dirname, "ig_queue.js"), "ids"], { encoding: "utf8", timeout: 30e3, stdio: ["ignore", "pipe", "ignore"] });
    queue = parseIds(out); queueOkAt = Date.now(); } catch { queueStale = true; }   // relay unreachable: empty queue, flagged stale
  let snap; try { snap = snapshot(); } catch (e) { snap = { reels: [], running: [], activity: feed(), queue, error: String(e && e.message || e) }; }
  const fac = json(path.join(ROOT, "logs/factory.json"), {}) || {};
  process.stdout.write(JSON.stringify({ now: new Date().toISOString(), ...snap, queueStale,
    factory: { at: fac.at || "", running: fac.running || {}, reels: fac.reels || {}, parked: fac.parked || {} } }) + "\n");
  return;   // CommonJS: ends this module here
}

// /events: live push (owner 10-15: "no latency"). The board gets a full state the moment logs/ changes (activity line, factory or
// manager status) instead of polling every 2 s; a 2 s sweep catches reel-file changes. Sent only when something differs.
const subs = new Set(); let lastSent = "", pushTimer = null;
function push() {
  pushTimer = null; if (!subs.size) return;
  let body; try { refreshQueue(); body = JSON.stringify(snapshot()); } catch (e) { console.error("board: snapshot failed", e && e.message); return; }   // F6: skip one push, never die
  if (body === lastSent) return; lastSent = body;
  const msg = `data: ${JSON.stringify({ now: new Date().toISOString(), ...JSON.parse(body) })}\n\n`;
  for (const r of subs) { try { r.write(msg); } catch {} }
}
function soon() { if (!pushTimer) pushTimer = setTimeout(push, 300); }   // F8: coalesce bursts of writes into one push (300 ms)
try { fs.watch(path.join(ROOT, "logs"), soon); } catch {}
// F4: a real heartbeat event every 10 s, so the board can tell a live stream from a frozen one
setInterval(soon, 2000); setInterval(() => { const hb = `event: hb\ndata: ${JSON.stringify({ now: new Date().toISOString() })}\n\n`; for (const r of subs) { try { r.write(hb); } catch {} } }, 10e3);

// audit 10-15 F1/F6: one bad URL ("%E0%A4%A") or a file deleted mid-read threw inside the handler and killed the whole board.
// Every request and every push is now guarded; an unexpected error is logged and answered with 400, the server stays up.
process.on("uncaughtException", (e) => console.error("board: uncaught", e && e.stack || e));
http.createServer((req, res) => {
  try { handle(req, res); } catch (e) {
    console.error("board: request failed", req.url, e && e.message);
    try { if (!res.headersSent) res.writeHead(400, { "content-type": "text/plain" }); res.end("bad request"); } catch {}
  }
}).listen(PORT, () => console.log(`production board: http://localhost:${PORT}`));
const library = require("./library_routes");   // 10-18 Clip Library page (/library)
function handle(req, res) {
  if (library.handle(req, res)) return;
  refreshQueue();
  const batch = batchDirs();
  if (req.url.startsWith("/events")) {
    res.writeHead(200, { "content-type": "text/event-stream", "cache-control": "no-store", connection: "keep-alive", "x-accel-buffering": "no" });
    res.write(`retry: 1000\ndata: ${JSON.stringify({ now: new Date().toISOString(), ...snapshot() })}\n\n`);
    subs.add(res); req.on("close", () => subs.delete(res)); return;
  }
  // /board/<file>: the studio's art (tools/board/art/*.png|webp) and scripts
  if (req.url.startsWith("/board/")) {
    const abs = path.resolve(__dirname, "board", decodeURIComponent(req.url.slice(7).split("?")[0]));
    const types = { ".png": "image/png", ".webp": "image/webp", ".jpg": "image/jpeg", ".js": "text/javascript", ".css": "text/css", ".json": "application/json" };
    if (!abs.startsWith(path.join(__dirname, "board") + path.sep) || !types[path.extname(abs)] || !exists(abs)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": types[path.extname(abs)], "cache-control": "public, max-age=300" }); return res.end(fs.readFileSync(abs));
  }
  // /state.json: everything the pixel studio (tools/board/studio.html) animates — reels per stage, running jobs, activity, queue
  if (req.url.startsWith("/factory.json")) {   // the automated conductor's own view (tools/factory.py)
    res.writeHead(200, { "content-type": "application/json", "cache-control": "no-store" });
    return res.end(exists(path.join(ROOT, "logs/factory.json")) ? fs.readFileSync(path.join(ROOT, "logs/factory.json")) : "{}");
  }
  if (req.url.startsWith("/state.json")) {
    res.writeHead(200, { "content-type": "application/json", "cache-control": "no-store" });
    return res.end(JSON.stringify({ now: new Date().toISOString(), ...snapshot() }));
  }
  // /media/<path>: real images for the studio (latest contact sheet, latest rendered frames) — images only, reels/ + deliverables/ only
  if (req.url.startsWith("/media/")) {
    const rel = decodeURIComponent(req.url.slice(7).split("?")[0]), abs = path.resolve(ROOT, rel);
    const okDir = [path.join(ROOT, "reels") + path.sep, path.join(ROOT, "deliverables") + path.sep].some((d) => abs.startsWith(d));
    if (!okDir || !/\.(jpg|jpeg|png)$/i.test(abs) || !exists(abs)) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": abs.endsWith(".png") ? "image/png" : "image/jpeg", "cache-control": "no-store" }); return res.end(fs.readFileSync(abs));
  }
  if (req.url.split("?")[0] === "/v2") {   // the isometric still-plate version (owner 10-15: "no motion" — kept to compare)
    res.writeHead(200, { "content-type": "text/html; charset=utf-8" }); return res.end(fs.readFileSync(path.join(__dirname, "board/studio.html")));
  }
  if (req.url.split("?")[0] === "/" || req.url.startsWith("/studio")) {
    const f = path.join(__dirname, "board/studio.html");
    if (exists(f)) { res.writeHead(200, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" }); return res.end(fs.readFileSync(f)); }   // 10-15: a browser kept an old board after a fix
  }
  res.writeHead(200, { "content-type": "text/html; charset=utf-8" }); res.end(page(batch.map(reelRow), running()));
}
