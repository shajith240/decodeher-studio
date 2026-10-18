// Clip Library page (owner 10-18: "see every clip in the database, play it, paste a link to add one, delete what I don't want").
// Mounted by tools/dashboard.js: /library (tools/board/library.html) + /library/api/* + /library/video + /library/thumb.
// The data work is tools/library.py (list/edit/move/delete/undo) and tools/pin_intake.py add (the same intake as Telegram).
// Laptop only: every /library request must come from this machine (the board port is open on campus Wi-Fi).
const fs = require("fs"), path = require("path"), crypto = require("crypto"), { execFile, spawn } = require("child_process");
const ROOT = path.resolve(__dirname, ".."), THUMBS = path.join(ROOT, "library/_thumbs");
const MEDIA_DIRS = ["library/hook-pool", "library/clips/inbox", "reels/_pool", "library/_bin"].map((d) => path.join(ROOT, d) + path.sep);
const jobs = new Map();   // add-link jobs: id → {kind, urls, pct, step, log[], done, result}
let listCache = { t: 0, body: "" };

const py = (args, cb) => execFile("python3", [path.join(ROOT, "tools/library.py"), ...args], { cwd: ROOT, timeout: 60e3, maxBuffer: 64 << 20 },
  (err, out, errOut) => cb(err ? (String(errOut || "").trim().split("\n").pop() || err.message) : null, out));
const send = (res, code, obj) => { res.writeHead(code, { "content-type": "application/json", "cache-control": "no-store" }); res.end(JSON.stringify(obj)); };
const body = (req, cb) => { let b = ""; req.on("data", (c) => { b += c; if (b.length > 1e6) req.destroy(); }); req.on("end", () => { try { cb(JSON.parse(b || "{}")); } catch { cb(null); } }); };
const safe = (rel) => { const abs = path.resolve(ROOT, String(rel || "")); return MEDIA_DIRS.some((d) => abs.startsWith(d)) && /\.mp4$/i.test(abs) && fs.existsSync(abs) ? abs : null; };
const local = (req) => ["127.0.0.1", "::1", "::ffff:127.0.0.1"].includes(req.socket.remoteAddress);

function handle(req, res) {
  const u = new URL(req.url, "http://x"), p = u.pathname;
  if (p !== "/library" && !p.startsWith("/library/")) return false;
  if (!local(req)) { res.writeHead(403); res.end("laptop only"); return true; }
  if (p === "/library" || p === "/library/") {
    res.writeHead(200, { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" });
    res.end(fs.readFileSync(path.join(__dirname, "board/library.html"))); return true;
  }
  if (p === "/library/api/list") {
    if (Date.now() - listCache.t < 3000) { res.writeHead(200, { "content-type": "application/json" }); res.end(listCache.body); return true; }
    py(["list"], (e, out) => { if (e) return send(res, 500, { error: e }); listCache = { t: Date.now(), body: out }; res.writeHead(200, { "content-type": "application/json", "cache-control": "no-store" }); res.end(out); });
    return true;
  }
  if (p === "/library/api/bin") { py(["bin"], (e, out) => (e ? send(res, 500, { error: e }) : (res.writeHead(200, { "content-type": "application/json" }), res.end(out)))); return true; }
  if (req.method === "POST" && /^\/library\/api\/(edit|move|delete|undo)$/.test(p)) {
    const op = p.split("/").pop();
    body(req, (b) => {
      if (!b) return send(res, 400, { error: "bad request" });
      const args = op === "edit" ? [b.file, JSON.stringify({ description: b.description, tags: b.tags })] : op === "move" ? [b.file, b.to] : op === "undo" ? [b.id] : [b.file];
      if (op !== "undo" && !safe(b.file)) return send(res, 404, { error: "no such clip" });
      py([op, ...args], (e, out) => { listCache.t = 0; e ? send(res, 400, { error: e }) : send(res, 200, JSON.parse(out)); });
    });
    return true;
  }
  if (req.method === "POST" && p === "/library/api/add") {
    body(req, (b) => {
      const urls = String((b && b.urls) || "").match(/https?:\/\/\S+/g) || [], kind = b && b.kind;
      if (!urls.length || !["hook", "visual", "dark"].includes(kind)) return send(res, 400, { error: "paste at least one link and pick a type" });
      const id = crypto.randomBytes(6).toString("hex"), job = { id, kind, urls, pct: 0, step: "starting…", done: false, result: null, at: Date.now() };
      jobs.set(id, job);
      const ch = spawn("python3", [path.join(ROOT, "tools/pin_intake.py"), "add", kind, ...urls], { cwd: ROOT });
      let buf = "";
      ch.stdout.on("data", (c) => {
        buf += c; let i;
        while ((i = buf.indexOf("\n")) >= 0) {
          const line = buf.slice(0, i); buf = buf.slice(i + 1);
          try { const m = JSON.parse(line); if (m.pct != null) job.pct = m.pct; if (m.step) job.step = m.step; if (m.done) { job.result = m; } } catch {}
        }
      });
      ch.on("close", (code) => { job.done = true; listCache.t = 0; if (!job.result) job.result = { error: `intake stopped (code ${code})` }; });
      send(res, 200, { id });
    });
    return true;
  }
  if (p === "/library/api/jobs") {
    for (const [k, j] of jobs) if (j.done && Date.now() - j.at > 3600e3) jobs.delete(k);
    send(res, 200, [...jobs.values()].sort((a, b) => b.at - a.at)); return true;
  }
  if (p === "/library/video") {   // Range requests, so the player can scrub
    const abs = safe(u.searchParams.get("f")); if (!abs) { res.writeHead(404); res.end(); return true; }
    const size = fs.statSync(abs).size, m = /bytes=(\d*)-(\d*)/.exec(req.headers.range || "");
    if (m) {
      const a = m[1] ? +m[1] : size - +m[2], z = m[1] && m[2] ? Math.min(+m[2], size - 1) : size - 1;
      if (a >= size || a < 0) { res.writeHead(416, { "content-range": `bytes */${size}` }); res.end(); return true; }
      res.writeHead(206, { "content-type": "video/mp4", "accept-ranges": "bytes", "content-range": `bytes ${a}-${z}/${size}`, "content-length": z - a + 1 });
      fs.createReadStream(abs, { start: a, end: z }).pipe(res);
    } else { res.writeHead(200, { "content-type": "video/mp4", "accept-ranges": "bytes", "content-length": size }); fs.createReadStream(abs).pipe(res); }
    return true;
  }
  if (p === "/library/thumb") {   // one frame per clip, made once (library/_thumbs)
    const abs = safe(u.searchParams.get("f")); if (!abs) { res.writeHead(404); res.end(); return true; }
    const st = fs.statSync(abs), out = path.join(THUMBS, crypto.createHash("sha1").update(abs + st.size).digest("hex") + ".jpg");
    const serve = () => { if (!fs.existsSync(out)) { res.writeHead(404); return res.end(); } res.writeHead(200, { "content-type": "image/jpeg", "cache-control": "public, max-age=86400" }); res.end(fs.readFileSync(out)); };
    if (fs.existsSync(out)) return serve(), true;
    fs.mkdirSync(THUMBS, { recursive: true });
    execFile("ffmpeg", ["-v", "error", "-y", "-ss", "1", "-i", abs, "-frames:v", "1", "-vf", "scale=320:-2", "-q:v", "5", out], { timeout: 20e3 }, (e) => {
      if (e || !fs.existsSync(out)) return execFile("ffmpeg", ["-v", "error", "-y", "-i", abs, "-frames:v", "1", "-vf", "scale=320:-2", "-q:v", "5", out], { timeout: 20e3 }, serve);
      serve();
    });
    return true;
  }
  res.writeHead(404); res.end(); return true;
}
// the bin empties itself after 7 days
setInterval(() => py(["purge"], () => {}), 3600e3);
module.exports = { handle };
