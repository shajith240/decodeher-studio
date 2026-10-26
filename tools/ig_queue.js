// Posting queue for @thedecodeher, kept on our own Cloudflare relay (relay/worker.js). The relay posts each reel at its
// slot even with this laptop off, and refreshes the Instagram token weekly.
//   node tools/ig_queue.js add <dir>          upload every *-FINAL.mp4 in <dir> (with its *-caption.txt), in filename order,
//                                             into the next free slots
//   node tools/ig_queue.js status             queue, last relay log lines, token age
//   node tools/ig_queue.js insights [days]    per-reel stats (reach, views, watch time, likes, comments, shares, saves) + followers, JSON
//   node tools/ig_queue.js pause | resume     stop / restart posting (nothing is lost while paused; >12 h late = skipped)
//   node tools/ig_queue.js ids                list every reel with its id
//   node tools/ig_queue.js remove <id>        drop a queued reel (and its hosted video)
//   node tools/ig_queue.js replace <dir>      swap re-rendered *-FINAL.mp4 into reels that are still queued (same slot)
//   node tools/ig_queue.js recaption <dir>    rewrite the captions of still-queued reels from <dir>/*-caption.txt (same slot, same video)
//   node tools/ig_queue.js cover <id> <jpg>|frame=<ms>   a still-queued reel's cover: an image (cover_url) or a frame of the reel
//   node tools/ig_queue.js captions           print every queued reel's caption
//   node tools/ig_queue.js reslot             re-pack queued reels into the earliest free slots (after a remove / slot change)
// Slots: SLOTS below (IST). Secrets: .relay.json { url, key } (or env RELAY_URL + RELAY_KEY in the cloud) and .env IG_TOKEN — never committed.
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const ROOT = path.resolve(__dirname, "..");
// .relay.json when it exists (this laptop, unchanged); otherwise RELAY_URL + RELAY_KEY from the environment (GitHub Actions secrets, 10-15)
const R = fs.existsSync(path.join(ROOT, ".relay.json")) ? JSON.parse(fs.readFileSync(path.join(ROOT, ".relay.json"), "utf8"))
  : process.env.RELAY_URL && process.env.RELAY_KEY ? { url: process.env.RELAY_URL.replace(/\/+$/, ""), key: process.env.RELAY_KEY }
  : (() => { console.error("⛔ no relay config: .relay.json or RELAY_URL + RELAY_KEY"); process.exit(1); })();
const SLOTS = ["08:30", "18:30", "22:00"];   // IST — 10-16 growth brain: 08:30 India morning / US late evening, 18:30 = US morning (9 am ET), 22:00 = US lunch + India night (brain/research/audience-location.md); was 08:30/14:00/21:00
const CSLOTS = ["04:30", "20:00"];   // IST — 10-19 owner: 2 carousels a day; 04:30 = 7 pm US Eastern, 20:00 = 10:30 am US Eastern
const IST = 330;                          // minutes ahead of UTC
const START = Date.UTC(2026, 9, 14, 3, 0);   // slots from 14 Oct 2026 08:30 IST (= 03:00 UTC); reel 1 went out 13 Oct (owner: "start today")

const api = async (method, p, body, type = "application/json") => {
  const r = await fetch(`${R.url}${p}`, { method, headers: { Authorization: `Bearer ${R.key}`, ...(body ? { "Content-Type": type } : {}) }, body });
  const t = await r.text(); if (!r.ok) throw new Error(`${method} ${p}: HTTP ${r.status} ${t.slice(0, 200)}`);
  return JSON.parse(t);
};
const fmt = (ms) => new Date(ms + IST * 60e3).toISOString().replace("T", " ").slice(0, 16) + " IST";

// every slot from START onward, in order
function* slots(list = SLOTS) {
  const d0 = new Date(START + IST * 60e3); let day = Date.UTC(d0.getUTCFullYear(), d0.getUTCMonth(), d0.getUTCDate());
  for (;; day += 86400e3) for (const s of list) { const [h, m] = s.split(":").map(Number); const t = day + (h * 60 + m - IST) * 60e3; if (t >= START) yield t; }
}

(async () => {
  const [cmd, arg] = process.argv.slice(2);
  if (cmd === "insights") {   // 10-16 growth brain: per-reel stats + followers as JSON (tools/growth_analyze.py reads this)
    const days = Math.min(30, Number(process.argv[3] || 30));
    return console.log(JSON.stringify(await api("GET", `/insights?days=${days}`)));
  }
  if (cmd === "status") {
    const s = await api("GET", "/status");
    console.log(`paused: ${s.paused}   token age: ${s.tokenAgeDays} days`);
    for (const q of s.queue) console.log(`  ${fmt(q.at)}  ${q.status.padEnd(10)} ${q.title}${q.permalink ? "  " + q.permalink : ""}${q.error ? "  ✗ " + q.error : ""}`);
    if (s.log.length) console.log("\nrelay log:\n  " + s.log.join("\n  "));
    return;
  }
  if (cmd === "pause" || cmd === "resume") return console.log(await api("POST", `/${cmd}`));
  if (cmd === "postnow") {   // 10-26 owner: post a queued item right now (its slot moves to now; the relay posts it on this tick)
    const fresh = await fullQueue(), it = fresh.find((q) => q.id === arg && q.status === "queued");
    if (!it) throw new Error(`no queued item "${arg}"`);
    it.at = Date.now() - 1000; fresh.sort((a, b) => a.at - b.at); await api("PUT", "/queue", JSON.stringify(fresh));
    await api("POST", "/tick"); return console.log(`posting now: ${it.title}`);
  }
  if (cmd === "carousel") {   // 10-19: book a rendered carousel (<dir>/NN.jpg + caption.txt) into the next free carousel slot (CSLOTS)
    const dir = path.resolve(arg), imgs = fs.readdirSync(dir).filter((f) => /^\d+\.jpe?g$/i.test(f)).sort();
    if (imgs.length < 2 || imgs.length > 10) throw new Error(`a carousel needs 2-10 slides as NN.jpg, found ${imgs.length}`);
    const title = "C-" + path.basename(dir), queue = await fullQueue();
    if (queue.some((q) => q.title === title && !["failed", "skipped"].includes(q.status))) return console.log(`= ${title} already queued`);
    const caption = fs.readFileSync(path.join(dir, "caption.txt"), "utf8").trim();
    const taken = new Set(queue.filter((q) => q.type === "carousel" && !["failed", "skipped"].includes(q.status)).map((q) => q.at));
    const free = slots(CSLOTS), now = Date.now(); let at; do at = free.next().value; while (taken.has(at) || at < now + 15 * 60e3);
    const keys = [];
    for (const f of imgs) {
      const key = `${crypto.randomBytes(12).toString("hex")}.jpg`, bytes = fs.readFileSync(path.join(dir, f));
      await api("PUT", `/media/${key}`, bytes, "image/jpeg");
      const head = await fetch(`${R.url}/m/${key}`, { method: "HEAD" });
      if (!head.ok || Number(head.headers.get("content-length")) !== bytes.length) throw new Error(`hosted slide ${f} is not reachable`);
      keys.push(key);
    }
    const fresh = await fullQueue();
    fresh.push({ id: `c-${path.basename(dir).slice(0, 10)}-${keys[0].slice(0, 4)}`, type: "carousel", title, keys, key: keys[0], at, caption, status: "queued" });
    fresh.sort((a, b) => a.at - b.at); await api("PUT", "/queue", JSON.stringify(fresh));
    return console.log(`+ ${fmt(at)}  ${title}  (${keys.length} slides)`);
  }
  if (cmd === "ids") {   // id, status, slot and title of every reel (for remove)
    for (const q of await fullQueue()) console.log(`${q.id.padEnd(16)} ${q.status.padEnd(9)} ${fmt(q.at)}  ${q.title}`);
    return;
  }
  if (cmd === "remove") {
    const s = await api("GET", "/status"), it = s.queue.find((q) => q.id === arg);
    if (!it || it.status !== "queued") throw new Error(`no queued reel "${arg}"`);
    for (const k of (it.keys || [it.key])) await api("DELETE", `/media/${k}`);   // a carousel hosts one image per slide
    const full = await fullQueue(); await api("PUT", "/queue", JSON.stringify(full.filter((q) => q.id !== arg)));
    return console.log(`removed ${it.title}`);
  }
  if (cmd === "reslot") {   // re-pack the still-queued reels, in order, into the earliest free slots
    const queue = await fullQueue(), fixed = new Set(queue.filter((q) => q.status !== "queued" && q.type !== "carousel").map((q) => q.at)), free = slots(), now = Date.now();
    for (const q of queue.filter((q) => q.status === "queued" && q.type !== "carousel").sort((a, b) => a.at - b.at)) {   /* carousels keep their own slots */ let at; do at = free.next().value; while (fixed.has(at) || at < now + 15 * 60e3); q.at = at; }
    queue.sort((a, b) => a.at - b.at); await api("PUT", "/queue", JSON.stringify(queue));
    return console.log("re-slotted");
  }
  if (cmd === "recaption") {   // owner 10-15: rewrite captions of reels still queued (same slot, same video) from <dir>/*-caption.txt
    const dir = path.resolve(arg), queue = await fullQueue(); let n = 0;
    for (const it of queue.filter((q) => q.status === "queued")) {
      const cap = captionFor(dir, it.title); if (!cap) { console.log(`= ${it.title}: no caption file, kept`); continue; }
      const text = fs.readFileSync(path.join(dir, cap), "utf8").trim();
      if (text === it.caption) { console.log(`= ${it.title}: unchanged`); continue; }
      it.caption = text; n++; console.log(`~ ${fmt(it.at)}  ${it.title}  (caption: ${text.split("\n")[0].slice(0, 70)})`);
    }
    const fresh = await fullQueue();   // never touch a reel that started posting while we worked
    for (const q of fresh) { const mine = queue.find((x) => x.id === q.id); if (q.status === "queued" && mine) q.caption = mine.caption; }
    if (n) await api("PUT", "/queue", JSON.stringify(fresh));
    return console.log(n ? `captions updated on the relay: ${n}` : "nothing to change");
  }
  if (cmd === "cover") {   // owner 10-15: a designed cover (deliverables/covers/<slug>.jpg) instead of a video frame — usage: cover <id> <file.jpg>
    const [id, file] = [arg, process.argv[4]], queue = await fullQueue(), it = queue.find((q) => q.id === id && q.status === "queued");
    if (it && /^frame=\d+$/.test(file || "")) {   // owner 10-15: no generated covers — use a frame of the reel itself (600 ms = the title card)
      const fresh = await fullQueue(), cur = fresh.find((q) => q.id === id && q.status === "queued");
      if (!cur) return console.log(`! ${id} is not queued`);
      if (cur.coverKey) await api("DELETE", `/media/${cur.coverKey}`);
      delete cur.coverUrl; delete cur.coverKey; cur.thumbMs = Number(file.split("=")[1]); await api("PUT", "/queue", JSON.stringify(fresh));
      return console.log(`~ ${fmt(cur.at)}  ${cur.title}  (cover = video frame at ${cur.thumbMs} ms)`);
    }
    if (!it || !file || !/\.jpe?g$/i.test(file)) throw new Error("usage: cover <queued id> <cover.jpg>");
    const key = `${crypto.randomBytes(12).toString("hex")}.jpg`, bytes = fs.readFileSync(file);
    await api("PUT", `/media/${key}`, bytes, "image/jpeg");
    const head = await fetch(`${R.url}/m/${key}`, { method: "HEAD" });
    if (!head.ok || Number(head.headers.get("content-length")) !== bytes.length) throw new Error("cover upload check failed");
    const fresh = await fullQueue(), cur = fresh.find((q) => q.id === id);
    if (!cur || cur.status !== "queued") { await api("DELETE", `/media/${key}`); return console.log(`! ${id} started posting meanwhile, cover not set`); }
    cur.coverUrl = `${R.url}/m/${key}`; cur.coverKey = key; await api("PUT", "/queue", JSON.stringify(fresh));
    return console.log(`~ ${fmt(cur.at)}  ${cur.title}  (cover set)`);
  }
  if (cmd === "captions") {   // print every queued reel's caption (to check)
    for (const it of (await fullQueue()).filter((q) => q.status === "queued")) console.log(`\n### ${fmt(it.at)}  ${it.title}\n${it.caption}`);
    return;
  }
  if (cmd === "replace") {   // swap in re-rendered videos (same title) for reels still queued; slots and captions stay
    const dir = path.resolve(arg), queue = await fullQueue();
    for (const v of fs.readdirSync(dir).filter((f) => f.endsWith("-FINAL.mp4")).sort()) {
      const it = queue.find((q) => q.title === v.replace(/-FINAL\.mp4$/, "") && q.status === "queued");
      if (!it) { console.log(`= ${v}: not queued, skipped`); continue; }
      const key = `${crypto.randomBytes(12).toString("hex")}.mp4`, bytes = fs.readFileSync(path.join(dir, v));
      await api("PUT", `/media/${key}`, bytes, "video/mp4");
      const head = await fetch(`${R.url}/m/${key}`, { method: "HEAD" });
      if (Number(head.headers.get("content-length")) !== bytes.length) throw new Error(`upload check failed for ${v}`);
      const old = it.key; it.key = key;
      const fresh = await fullQueue(), cur = fresh.find((q) => q.id === it.id);
      if (!cur || cur.status !== "queued") { await api("DELETE", `/media/${key}`); console.log(`! ${it.title} started posting meanwhile, kept the old video`); continue; }
      cur.key = key; await api("PUT", "/queue", JSON.stringify(fresh)); await api("DELETE", `/media/${old}`);
      console.log(`~ ${fmt(it.at)}  ${it.title}  (video replaced)`);
    }
    return;
  }
  if (cmd === "add") {
    const dir = path.resolve(arg), vids = fs.readdirSync(dir).filter((f) => f.endsWith("-FINAL.mp4")).sort();
    const queue = await fullQueue(), taken = new Set(queue.filter((q) => q.status !== "failed" && q.status !== "skipped").map((q) => q.at));
    const free = slots(), now = Date.now(), added = [];
    for (const v of vids) {
      const title = v.replace(/-FINAL\.mp4$/, "");
      if (queue.some((q) => q.title === title && q.status !== "failed")) { console.log(`= ${title} already queued`); continue; }
      const cap = captionFor(dir, title);
      if (!cap) throw new Error(`no caption file for ${v}`);
      let at; do at = free.next().value; while (taken.has(at) || at < now + 15 * 60e3);
      taken.add(at);
      const key = `${crypto.randomBytes(12).toString("hex")}.mp4`;
      await api("PUT", `/media/${key}`, fs.readFileSync(path.join(dir, v)), "video/mp4");
      const head = await fetch(`${R.url}/m/${key}`, { method: "HEAD" });
      if (!head.ok || Number(head.headers.get("content-length")) !== fs.statSync(path.join(dir, v)).size) throw new Error(`hosted video for ${title} is not reachable`);
      added.push({ id: title.split("-").slice(0, 2).join("-").toLowerCase() + "-" + key.slice(0, 4), title, key, at,
        slug: (cap.match(/w\d+-\d+-[a-z0-9-]+?(?=-caption)/) || [""])[0],   // links the post to brain/content/reels/<slug>.md
        caption: fs.readFileSync(path.join(dir, cap), "utf8").trim(), status: "queued", thumbMs: Number(process.env.THUMB_MS) || 1500 });   // 600 = the title card frame (queue_reel.sh)
      console.log(`+ ${fmt(at)}  ${title}`);
    }
    // audit 10-15 H1: the uploads above take minutes; a post can go live meanwhile. Never PUT the stale copy back (it would flip a
    // just-posted reel to "queued" again = double post): re-read the queue NOW and only append the new items to the fresh copy.
    if (!added.length) return console.log("nothing new to add");
    const fresh = await fullQueue(), freshTaken = new Set(fresh.filter((q) => q.status !== "failed" && q.status !== "skipped").map((q) => q.at));
    for (const a of added) {
      if (fresh.some((q) => q.title === a.title && q.status !== "failed")) { console.log(`= ${a.title} already queued (meanwhile)`); continue; }
      if (freshTaken.has(a.at)) throw new Error(`slot ${fmt(a.at)} was taken meanwhile; run add again`);
      fresh.push(a); freshTaken.add(a.at);
    }
    fresh.sort((a, b) => a.at - b.at);
    await api("PUT", "/queue", JSON.stringify(fresh));
    return console.log("queue saved on the relay");
  }
  console.log("usage: node tools/ig_queue.js add <dir> | status | pause | resume | remove <id>");
})().catch((e) => { console.error(`⛔ ${e.message}`); process.exit(1); });

// the caption file of a reel title: "08-W2-just-ask" ↔ "08-W2-w2-16-just-ask-caption.txt" — match the NAME, not just the number
// (10-15: two reels numbered 08 could take each other's caption when matched on "08-W2" alone)
function captionFor(dir, title) {
  const num = title.split("-").slice(0, 2).join("-"), name = title.split("-").slice(2).join("-");
  const all = fs.readdirSync(dir).filter((f) => f.startsWith(num + "-") && f.endsWith("-caption.txt"));
  return all.find((f) => f.slice(0, -"-caption.txt".length).endsWith("-" + name) || f.includes("-" + name + "-")) || (all.length === 1 ? all[0] : null);
}

// the full queue (with captions) as the relay holds it
function fullQueue() { return api("GET", "/queue"); }
