// Nudge the posting relay when a post is due or processing, so it lands on time (owner 10-14: the 21:00 reel came at 21:05 —
// the relay only checks every 10 min and Instagram needs two checks: upload, then publish). Run every minute by tools/factory.py;
// the relay's own 10-minute alarm still covers it when this laptop is off. Never prints the relay key.
const fs = require("fs"), path = require("path");
// .relay.json when it exists (this laptop); otherwise env RELAY_URL + RELAY_KEY (GitHub Actions, 10-15)
const F = path.join(__dirname, "../.relay.json");
const R = fs.existsSync(F) ? JSON.parse(fs.readFileSync(F, "utf8")) : { url: process.env.RELAY_URL || "", key: process.env.RELAY_KEY || "" };
if (!R.url || !R.key) { console.log("relay_tick: no relay config"); process.exit(0); }
const base = R.url.replace(/\/$/, ""), H = { Authorization: "Bearer " + R.key };
(async () => {
  const s = await (await fetch(base + "/status", { headers: H })).json();
  const due = (s.queue || []).some((q) => (q.status === "queued" && q.at <= Date.now() + 30e3) || q.status === "processing");
  if (!due || s.paused) return;
  const r = await fetch(base + "/tick", { method: "POST", headers: H }); console.log("tick", r.status);
})().catch((e) => console.log("relay_tick:", e.message));
