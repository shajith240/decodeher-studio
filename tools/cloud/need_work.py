"""Cloud gate (10-16): is there anything for a factory run to do? Asks HQ only (seconds, no Drive pull), so a 3-hourly schedule
costs almost nothing when the line is idle. Work = an unfinished reel in the last snapshot, or Pinterest links in the Telegram
inbox, or the snapshot is older than 12 h (be safe: run). Prints work=true|false for $GITHUB_OUTPUT. Env: HQ_URL, HQ_KEY."""
import json, os, urllib.request
url, key = os.environ.get("HQ_URL", "").rstrip("/"), os.environ.get("HQ_KEY", "")
def get(path, auth=False):
    req = urllib.request.Request(url + path, headers={"User-Agent": "decodeher-gate/1.0", **({"Authorization": f"Bearer {key}"} if auth else {})})   # Cloudflare 403s the default Python-urllib agent
    return json.loads(urllib.request.urlopen(req, timeout=20).read())
why = []
try:
    st = get("/api/state"); stale = st.get("stale", {}) or {}
    if (stale.get("unfinished") or 0) > 0: why.append(f"{stale['unfinished']} unfinished reel(s)")
    if stale.get("factoryAgeMin") is None or stale["factoryAgeMin"] > 720: why.append("no recent snapshot")
except Exception as e: why.append(f"HQ unreadable ({type(e).__name__})")
try:
    if get("/api/inbox", auth=True).get("items"): why.append("Pinterest links waiting")
except Exception: pass
print(f"work={'true' if why else 'false'}"); print("why=" + ("; ".join(why) or "nothing to do"))
