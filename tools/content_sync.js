// The page's content memory: keeps brain/content/ (Obsidian) true to what actually happened on Instagram.
//   node tools/content_sync.js
// For every reel note in brain/content/reels/<slug>.md:
//   - status / posted / permalink from the posting relay's queue (tools/ig_queue.js)
//   - views, reach, likes, comments, saves, shares from the Instagram insights API (posted reels)
//   - part2: wanted   when ≥ 3 comments ask for more ("part 2", "next", "more", "how do I…")
// Then rewrites brain/content/00-content.md: what's posted and how it did, what's queued, the part-2 board, and the
// variety tallies (CTA type, story shape, hook style) that the next batch must balance (brain/rules/script-and-hooks.md).
// Run it before planning any batch, and whenever you want fresh numbers.
const fs = require("fs"), path = require("path");
const ROOT = path.resolve(__dirname, ".."), DIR = path.join(ROOT, "brain/content"), REELS = path.join(DIR, "reels");
const R = JSON.parse(fs.readFileSync(path.join(ROOT, ".relay.json"), "utf8"));
const TOKEN = (fs.readFileSync(path.join(ROOT, ".env"), "utf8").match(/^IG_TOKEN=(.*)$/m) || [])[1];
const GRAPH = "https://graph.instagram.com/v25.0";
const IST = (ms) => new Date(ms + 330 * 60e3).toISOString().replace("T", " ").slice(0, 16);

const parse = (s) => { const m = s.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/); const fm = {};
  for (const l of m[1].split("\n")) { const i = l.indexOf(":"); if (i > 0) fm[l.slice(0, i).trim()] = l.slice(i + 1).trim().replace(/^"(.*)"$/, "$1"); }
  return { fm, body: m[2], order: m[1].split("\n").map((l) => l.slice(0, l.indexOf(":")).trim()) }; };
const dump = ({ fm, body, order }) => `---\n${[...new Set([...order, ...Object.keys(fm)])].filter((k) => k in fm)
  .map((k) => `${k}: ${/[:#'"]|^\s|\s$/.test(String(fm[k])) && fm[k] !== "" ? JSON.stringify(String(fm[k])) : fm[k]}`).join("\n")}\n---\n${body}`;
const get = async (p, q = {}) => { const r = await (await fetch(`${GRAPH}/${p}?${new URLSearchParams({ ...q, access_token: TOKEN })}`)).json(); if (r.error) throw new Error(r.error.message); return r; };

(async () => {
  const queue = await (await fetch(`${R.url}/queue`, { headers: { Authorization: `Bearer ${R.key}` } })).json();
  const notes = fs.readdirSync(REELS).filter((f) => f.endsWith(".md")).map((f) => ({ file: path.join(REELS, f), ...parse(fs.readFileSync(path.join(REELS, f), "utf8")) }));
  for (const n of notes) {
    const q = queue.find((x) => x.slug === n.fm.slug);
    if (q) {
      n.fm.status = q.status; n.fm.scheduled = IST(q.at) + " IST";
      if (q.status === "posted") { n.fm.posted = IST(q.postedAt || q.at) + " IST"; n.fm.permalink = q.permalink || ""; n.fm.media_id = q.mediaId; }
    }
    if (n.fm.media_id && TOKEN) {
      try {
        const ins = await get(`${n.fm.media_id}/insights`, { metric: "views,reach,likes,comments,saved,shares" });
        for (const d of ins.data) n.fm[d.name === "saved" ? "saves" : d.name] = d.values?.[0]?.value ?? d.total_value?.value ?? "";
        const cm = await get(`${n.fm.media_id}/comments`, { fields: "text", limit: 100 });
        const asks = cm.data.filter((c) => /part\s*2|part two|next (one|part|move)|\bmore\b|how do i|what (do|should) i (say|do)/i.test(c.text)).length;
        n.fm.part2_asks = asks;
        if (asks >= 3 && n.fm.part2 !== "made") n.fm.part2 = "wanted";
      } catch (e) { console.log(`  ${n.fm.slug}: insights unavailable (${e.message})`); }
    }
    fs.writeFileSync(n.file, dump(n));
  }

  const link = (n) => `[[reels/${n.fm.slug}|${n.fm.title}]]`;
  const posted = notes.filter((n) => n.fm.status === "posted").sort((a, b) => a.fm.posted.localeCompare(b.fm.posted));
  const queued = notes.filter((n) => n.fm.status === "queued" || n.fm.status === "processing").sort((a, b) => (a.fm.scheduled || "").localeCompare(b.fm.scheduled || ""));
  const tally = (k) => Object.entries(notes.reduce((a, n) => ((a[n.fm[k] || "?"] = (a[n.fm[k] || "?"] || 0) + 1), a), {})).sort((a, b) => b[1] - a[1]).map(([v, c]) => `${v} ×${c}`).join(" · ");
  const p2 = notes.filter((n) => n.fm.part2 === "wanted" || n.fm.part2 === "candidate").sort((a, b) => (b.fm.part2 === "wanted") - (a.fm.part2 === "wanted"));
  const md = `# Content memory — what we made, how it did, what's next

Auto-written by \`node tools/content_sync.js\` (${IST(Date.now())} IST). Every agent planning a reel reads this first.
Rules for using it: [[../rules/script-and-hooks#Variety across a batch]].

## Posted (${posted.length})
| posted (IST) | reel | views | reach | saves | shares | comments | link |
|---|---|---|---|---|---|---|---|
${posted.map((n) => `| ${n.fm.posted} | ${link(n)} | ${n.fm.views || "–"} | ${n.fm.reach || "–"} | ${n.fm.saves || "–"} | ${n.fm.shares || "–"} | ${n.fm.comments || "–"} | ${n.fm.permalink ? `[open](${n.fm.permalink})` : ""} |`).join("\n")}

## Queued (${queued.length})
${queued.map((n) => `- ${n.fm.scheduled} — ${link(n)}`).join("\n") || "- nothing queued: make the next batch"}

## Part-2 board
\`wanted\` = viewers asked in the comments (make it next). \`candidate\` = we think it has a sequel.
${p2.map((n) => `- **${n.fm.part2}** ${link(n)} → ${n.fm.part2_idea || "(idea?)"}${n.fm.part2_asks ? ` (${n.fm.part2_asks} asks)` : ""}`).join("\n") || "- none"}

## Variety so far (balance these in the next batch)
- **CTA type:** ${tally("cta_type")}
- **Story shape:** ${tally("story_shape")}
- **Hook style:** ${tally("hook_style")}
- **Punch format:** ${tally("punch_format")}

## Topics used (don't repeat without a new angle)
${notes.map((n) => `- ${n.fm.topic} — ${link(n)}`).join("\n")}

See also: [[ideas]] (backlog).
`;
  fs.writeFileSync(path.join(DIR, "00-content.md"), md);
  console.log(`content memory synced: ${posted.length} posted, ${queued.length} queued, ${p2.length} on the part-2 board`);
})().catch((e) => { console.error(`⛔ ${e.message}`); process.exit(1); });
