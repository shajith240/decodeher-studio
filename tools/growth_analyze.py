"""Growth brain, part 1: OUR numbers (owner 10-16: "use different tactics according to the analysis of the reels").
Usage: python3 tools/growth_analyze.py
No Claude. Reads per-reel Instagram stats (node tools/ig_queue.js insights 30) and joins each posted reel with what it WAS
(hook line, title card, topic/series, length, music, opening clip, snaps, post slot) from reels/<dir>/. Writes:
  brain/growth/data/insights-<date>.json   raw daily snapshot (kept; the history the strategist learns from)
  brain/growth/data/followers.csv          date,time,followers (one row per run)
  brain/growth/performance.md              the table + rates + what stands out, read by the daily strategist and the owner
Rates: watch % = avg watch / reel length; share/save/like/comment rates per 1,000 reached."""
import csv, datetime, glob, json, os, re, subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
G = "brain/growth"; os.makedirs(f"{G}/data", exist_ok=True)
now = datetime.datetime.now(); day = now.strftime("%F")

raw = subprocess.run(["node", "tools/ig_queue.js", "insights", "30"], capture_output=True, text=True, timeout=180).stdout
try: data = json.loads(raw)
except json.JSONDecodeError: raise SystemExit("insights not available: " + raw[:200])
json.dump(data, open(f"{G}/data/insights-{day}.json", "w"), indent=1)
acct = data.get("account", {}); followers = acct.get("followers_count")
new = not os.path.exists(f"{G}/data/followers.csv")
with open(f"{G}/data/followers.csv", "a", newline="") as f:
    w = csv.writer(f); (w.writerow(["date", "time", "followers"]) if new else None); w.writerow([day, now.strftime("%H:%M"), followers])

def reel_dir(title):   # queue title "17-W2-seen-then-story" -> reels/w7-01-seen-then-story
    slug = re.sub(r"^\d+-[A-Za-z0-9]+-", "", title).lower()
    hits = [d for d in glob.glob("reels/w*-*") if os.path.isdir(d) and d.endswith(slug)]
    return hits[0] if hits else None
def jl(p, d=None):
    try: return json.load(open(p))
    except Exception: return d
def length(d):
    t = open(f"{d}/assets/timing.js").read() if d and os.path.exists(f"{d}/assets/timing.js") else ""
    m = re.search(r'"total":\s*([\d.]+)', t); return float(m.group(1)) if m else None

IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
rows = []
for r in data.get("reels", []):
    d = reel_dir(r["title"]); cfg = jl(f"{d}/reel.json", {}) if d else {}
    script = jl(f"{d}/assets/vo/script.json", []) if d else []
    hook = re.sub(r"\[[^\]]*\]\s*", "", (script[0]["text"] if script and isinstance(script[0], dict) else (script[0] if script else ""))).strip()
    L = length(d); reach = r.get("reach") or 0; k = 1000 / reach if reach else 0
    aw = (r.get("ig_reels_avg_watch_time") or 0) / 1000
    rows.append({"title": r["title"], "link": r.get("permalink"), "posted": datetime.datetime.fromtimestamp(r["postedAt"] / 1000, IST).strftime("%m-%d %H:%M") if r.get("postedAt") else "",
                 "format": "new (10-16)" if cfg.get("frame") == "lens" else "old", "hook": hook[:90], "title_card": cfg.get("titleCard", ""),
                 "series": cfg.get("series", ""), "length_s": L, "music": cfg.get("music", ""), "hook_clip": bool(cfg.get("hookClip")),
                 "snaps": len(cfg.get("snaps", [])), "reach": reach, "views": r.get("views"), "avg_watch_s": round(aw, 1),
                 "watch_pct": round(100 * aw / L) if L and aw else None, "likes_k": round((r.get("likes") or 0) * k, 1),
                 "comments_k": round((r.get("comments") or 0) * k, 1), "shares_k": round((r.get("shares") or 0) * k, 1),
                 "saves_k": round((r.get("saved") or 0) * k, 1)})
json.dump(rows, open(f"{G}/data/joined-{day}.json", "w"), indent=1, ensure_ascii=False)

hist = list(csv.reader(open(f"{G}/data/followers.csv")))[1:]
first = next((h for h in hist if h[2] not in ("", "None")), None)
out = [f"# Performance — updated {now:%F %H:%M} IST", "",
       f"Followers: **{followers}** (first recorded {first[0] if first else '?'}: {first[2] if first else '?'}). Target: 1,000 by 2026-10-26.", "",
       "| Posted (IST) | Reel | Format | Len s | Reach | Views | Avg watch s | Watch % | Likes/1k | Comments/1k | Shares/1k | Saves/1k |",
       "|---|---|---|---|---|---|---|---|---|---|---|---|"]
for x in sorted(rows, key=lambda x: x["posted"]):
    out.append(f"| {x['posted']} | [{x['title']}]({x['link']}) | {x['format']} | {x['length_s'] or '?'} | {x['reach']} | {x['views']} | {x['avg_watch_s']} | "
               f"{x['watch_pct'] if x['watch_pct'] is not None else '?'} | {x['likes_k']} | {x['comments_k']} | {x['shares_k']} | {x['saves_k']} |")
if rows:
    best = max(rows, key=lambda x: (x["reach"], x["avg_watch_s"])); worst = min(rows, key=lambda x: (x["reach"], x["avg_watch_s"]))
    out += ["", "## What stands out", f"- Best reach: {best['title']} ({best['reach']} reach, {best['avg_watch_s']} s average watch).",
            f"- Weakest: {worst['title']} ({worst['reach']} reach, {worst['avg_watch_s']} s).",
            f"- Shares + saves across all reels: {sum(x['shares_k'] for x in rows):.1f} + {sum(x['saves_k'] for x in rows):.1f} per 1k — "
            + ("zero: nothing yet makes people send or keep a reel; the top growth lever to work on." if not any(x['shares_k'] or x['saves_k'] for x in rows) else "see table."),
            "- Hook details per reel (for the strategist):"] + [f"  - {x['title']}: hook “{x['hook']}” · card “{x['title_card']}” · music {x['music']} · AI opener {x['hook_clip']}" for x in rows if x["hook"]]
open(f"{G}/performance.md", "w").write("\n".join(out) + "\n")
print(f"followers {followers}, {len(rows)} reels -> {G}/performance.md")
