"""Report the factory to HQ (Cloudflare Worker decodeher-hq; contract: brain/cloud-architecture.md).

  python3 tools/cloud/report.py                         snapshot (node tools/dashboard.js --snapshot) → POST $HQ_URL/api/state
  python3 tools/cloud/report.py event <type> <text> [--reel R] [--preview-url U] [--slot S] [--request-id ID]
                                                        → POST $HQ_URL/api/event  {type, text, reel?, preview_url?, slot?, request_id?}
                                                          types: activity · preview · error · done
Env: HQ_URL, HQ_KEY (Bearer; never printed). Without them it prints what it would send and exits 0, so a run without HQ
still finishes. A failed POST is retried 3 times, then exits 1 (the workflow step decides whether that matters)."""
import argparse, json, os, subprocess, sys, time, urllib.error, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TYPES = ("activity", "preview", "error", "done")


def post(path, payload):
    url, key = os.environ.get("HQ_URL", "").rstrip("/"), os.environ.get("HQ_KEY", "")
    body = json.dumps(payload, ensure_ascii=False).encode()
    if not url or not key:
        print(f"HQ_URL/HQ_KEY not set: would POST {path} ({len(body)} bytes)"); return 0
    for attempt in range(4):
        try:
            req = urllib.request.Request(url + path, data=body, method="POST",
                                         headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "User-Agent": "decodeher-factory"})
            with urllib.request.urlopen(req, timeout=30) as r:
                print(f"POST {path}: HTTP {r.status} ({len(body)} bytes)"); return 0
        except urllib.error.HTTPError as e:
            msg = f"HTTP {e.code}"
            if 400 <= e.code < 500 and e.code != 429: print(f"POST {path} refused: {msg}", file=sys.stderr); return 1   # auth/shape: retrying won't help
        except Exception as e:
            msg = type(e).__name__
        if attempt < 3: time.sleep(3 * (attempt + 1))
    print(f"POST {path} failed: {msg}", file=sys.stderr); return 1


def snapshot():
    out = subprocess.run(["node", os.path.join(ROOT, "tools", "dashboard.js"), "--snapshot"], cwd=ROOT, capture_output=True, text=True, timeout=120)
    if out.returncode != 0: sys.exit(f"dashboard --snapshot failed: {out.stderr.strip()[-300:]}")
    snap = json.loads(out.stdout)
    snap["source"] = "github-actions" if os.environ.get("GITHUB_ACTIONS") else "local"
    if os.environ.get("GITHUB_RUN_ID"):
        snap["run"] = {"id": os.environ["GITHUB_RUN_ID"], "workflow": os.environ.get("GITHUB_WORKFLOW", ""),
                       "url": f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{os.environ.get('GITHUB_REPOSITORY', '')}/actions/runs/{os.environ['GITHUB_RUN_ID']}"}
    return snap


def main(argv):
    if argv[:1] == ["event"]:
        ap = argparse.ArgumentParser(prog="report.py event")
        ap.add_argument("type", choices=TYPES); ap.add_argument("text")
        ap.add_argument("--reel"); ap.add_argument("--preview-url"); ap.add_argument("--slot"); ap.add_argument("--request-id")
        a = ap.parse_args(argv[1:])
        ev = {"type": a.type, "text": a.text}
        if a.reel: ev["reel"] = a.reel
        if a.preview_url: ev["preview_url"] = a.preview_url
        if a.slot: ev["slot"] = a.slot
        if a.request_id: ev["request_id"] = a.request_id
        return post("/api/event", ev)
    if argv: sys.exit(__doc__)
    return post("/api/state", snapshot())


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
