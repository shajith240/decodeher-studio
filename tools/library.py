"""Clip library: list / edit / move / delete / undo (owner 10-18: "a dashboard where I see every clip in the database, play it, and
update or delete what I don't want"). Used by the Clip Library page (tools/dashboard.js → /library); safe to run by hand.
Usage: python3 tools/library.py list                      → JSON of every clip (4 kinds, below)
       python3 tools/library.py edit <file> '<json>'      → {"description": "...", "tags": [...]} into the clip's .json
       python3 tools/library.py move <file> <kind>        → hook | visual | dark (file + .json + registry + Drive move together)
       python3 tools/library.py delete <file>             → into library/_bin/<id>/ for 7 days (Drive copy too); undo brings it back
       python3 tools/library.py undo <id>  |  bin  |  purge   (purge = empty bin entries older than 7 days)
Kinds: hook   = AI-woman openers        library/hook-pool/ai/      Drive clip-library/hooks/
       visual = other visual hooks      library/hook-pool/visual/  Drive clip-library/hooks-visual/   (10-18 test: ≤ 1 reel in 4)
       dark   = owner's dark clips      library/clips/inbox/       Drive clip-library/dark/   (+ hard link in reels/_pool/telegram-dark)
       pool   = clips the factory found on Pinterest searches, reels/_pool/<search>/ (laptop only; a curated few are on Drive)
Drive moves run in the background (rclone is slow); the page shows the laptop copy, which is what the factory uses."""
import fcntl, glob, json, os, re, shutil, subprocess, sys, time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")); os.chdir(ROOT)
DIRS = {"hook": "library/hook-pool/ai", "visual": "library/hook-pool/visual", "dark": "library/clips/inbox"}
DRIVE = {"hook": "gdrive:DecodeHer/clip-library/hooks", "visual": "gdrive:DecodeHer/clip-library/hooks-visual", "dark": "gdrive:DecodeHer/clip-library/dark"}
PREFIX = {"hook": "ai", "visual": "vis", "dark": "dark"}
BIN, REG, DRIVE_LS = "library/_bin", "library/pin-registry.json", "library/.drive-list.json"
TG = "reels/_pool/telegram-dark"
jload = lambda p, d: json.load(open(p)) if os.path.exists(p) else d
pin_of = lambda f: (re.search(r"(\d{12,})", os.path.basename(f)) or [None, None])[1]

class reg_lock:   # the same lock tools/pin_intake.py takes, so the page and the Telegram intake never write the registry at once
    def __enter__(self): self.f = open(REG + ".lock", "w"); fcntl.flock(self.f, fcntl.LOCK_EX); return jload(REG, {"items": {}})
    def __exit__(self, *a): fcntl.flock(self.f, fcntl.LOCK_UN); self.f.close()
def save_reg(r): json.dump(r, open(REG + ".part", "w")); os.replace(REG + ".part", REG)

def kind_of(f):
    for k, d in DIRS.items():
        if os.path.dirname(f) == d: return k
    return "pool" if f.startswith("reels/_pool/") and not f.startswith(TG + "/") else None

def bg(cmd):   # fire and forget (Drive), logged
    os.makedirs("logs", exist_ok=True)
    if cmd[0] == "rclone": cmd = ["flock", "library/.drive.lock"] + cmd   # Drive moves run one at a time, in order (an undo right after a delete overtook it)
    subprocess.Popen(cmd, stdout=open("logs/library-drive.log", "a"), stderr=subprocess.STDOUT, start_new_session=True)

def drive_names():   # cached listing of Drive (refreshed in the background at most every 10 min)
    c = jload(DRIVE_LS, {"at": 0, "names": []})
    if time.time() - c["at"] > 600 and not os.path.exists(DRIVE_LS + ".busy"):
        open(DRIVE_LS + ".busy", "w").close()
        bg(["sh", "-c", f'rclone lsf -R --files-only gdrive:DecodeHer/clip-library/ 2>/dev/null | python3 -c "import json,sys,time; '
                        f'n=[l.strip().split(\'/\')[-1] for l in sys.stdin if l.strip()]; json.dump({{\'at\': time.time(), \'names\': n}}, open(\'{DRIVE_LS}\', \'w\'))"; rm -f {DRIVE_LS}.busy'])
    return set(c["names"])

def listing():
    usage = jload("library/clip-usage.json", {"reels": []}); TX = jload("library/clip-text.json", {}); emb = jload("reels/_pool/emb.json", {})
    used = {}
    for u in usage["reels"]:
        for p in u["pins"]: used.setdefault(p, []).append(u["reel"])
    for rj in glob.glob("reels/*/reel.json"):   # openers: reel.json hookSrc
        src = (jload(rj, {}) or {}).get("hookSrc")
        if src: used.setdefault(os.path.basename(src), []).append(os.path.basename(os.path.dirname(rj)))
    drive = drive_names(); drive_pins = {pin_of(n) for n in drive if pin_of(n)}
    drive_pins |= {m.group(1) for n in drive if (m := re.search(r"(\d{6})(?:__\d+)?\.mp4$", n))}   # curated names end in the pin's last 6 digits
    out = []
    files = [(k, f) for k, d in DIRS.items() for f in sorted(glob.glob(f"{d}/*.mp4"))]
    files += [("pool", f) for f in sorted(glob.glob("reels/_pool/*/*.mp4")) if not f.startswith(TG + "/")]
    for k, f in files:
        b = os.path.basename(f); meta = jload(f[:-4] + ".json", {}) if k != "pool" else {}
        pin = str(meta.get("pin") or pin_of(f) or "")
        try: st = os.stat(f)
        except OSError: continue
        e = emb.get(pin_of(f) or "", {}) if k == "pool" else {}
        out.append({"file": f, "name": b, "kind": k, "pin": pin, "url": meta.get("url", f"https://pinterest.com/pin/{pin}" if pin else ""),
                    "description": meta.get("ai_description") or meta.get("title") or (os.path.basename(os.path.dirname(f)).replace("-", " ") if k == "pool" else ""),
                    "tags": meta.get("tags", []), "from": meta.get("from", "Pinterest search" if k == "pool" else ""),
                    "added": meta.get("at") or time.strftime("%F", time.localtime(st.st_mtime)), "mb": round(st.st_size / 1e6, 1),
                    "text": bool(TX.get(b, [False])[0]), "textSeen": (TX.get(b, [False, ""]) + [""])[1] if TX.get(b, [False])[0] else "",
                    "usedIn": sorted(set(used.get(pin, []) + used.get(b, []))), "drive": b in drive or (bool(pin) and (pin in drive_pins or pin[-6:] in drive_pins)),
                    "style": round(e.get("style", 0), 2) if e else None, "styleOk": e.get("ok") if e else None})
    return out

def drive_path(k, name): return f"{DRIVE[k]}/{name}" if k in DRIVE else None

def edit(f, data):
    if kind_of(f) in (None, "pool"): sys.exit("only curated clips (hooks, visual hooks, your dark clips) have a description to edit")
    js = f[:-4] + ".json"; m = jload(js, {})
    if "description" in data: m["ai_description"] = str(data["description"])[:300]
    if "tags" in data: m["tags"] = [str(t).strip()[:30] for t in data["tags"] if str(t).strip()][:12]
    m["edited"] = time.strftime("%F %T"); json.dump(m, open(js, "w"), indent=1, ensure_ascii=False); return {"ok": True}

def move(f, to):
    k = kind_of(f)
    if k not in DIRS or to not in DIRS or k == to: sys.exit(f"can't move a {k} clip to {to}")
    b = os.path.basename(f); nb = re.sub(r"^(ai|vis|dark)-", PREFIX[to] + "-", b); nf = f"{DIRS[to]}/{nb}"
    os.makedirs(DIRS[to], exist_ok=True); shutil.move(f, nf)
    if os.path.exists(f[:-4] + ".json"): shutil.move(f[:-4] + ".json", nf[:-4] + ".json")
    if k == "dark" and os.path.exists(f"{TG}/{b}"): os.remove(f"{TG}/{b}")
    if to == "dark":
        os.makedirs(TG, exist_ok=True)
        try: os.link(nf, f"{TG}/{nb}")
        except OSError: shutil.copy(nf, f"{TG}/{nb}")
    with reg_lock() as r:
        for v in r["items"].values():
            if v.get("file") == f: v["file"], v["kind"] = nf, ("hook" if to != "dark" else "dark")
        save_reg(r)
    bg(["rclone", "moveto", drive_path(k, b), drive_path(to, nb)])
    return {"ok": True, "file": nf}

def delete(f):
    k = kind_of(f)
    if not k or not os.path.exists(f): sys.exit("not a library clip")
    bid = time.strftime("%Y%m%d-%H%M%S-") + re.sub(r"[^a-z0-9]+", "-", os.path.basename(f)[:-4].lower())[:40]
    d = f"{BIN}/{bid}"; os.makedirs(d)
    moved = [(f, f"{d}/{os.path.basename(f)}")] + ([(f[:-4] + ".json", f"{d}/{os.path.basename(f)[:-4]}.json")] if os.path.exists(f[:-4] + ".json") else [])
    for a, b in moved: shutil.move(a, b)
    tg = f"{TG}/{os.path.basename(f)}"
    if k == "dark" and os.path.exists(tg): os.remove(tg)
    regs = {}
    with reg_lock() as r:   # out of the registry, so you could add the same link again later; undo puts it back
        for key in [key for key, v in r["items"].items() if v.get("file") == f]: regs[key] = r["items"].pop(key)
        save_reg(r)
    dp = drive_path(k, os.path.basename(f)); bin_drive = f"gdrive:DecodeHer/clip-library/_bin/{bid}/{os.path.basename(f)}"
    if dp: bg(["rclone", "moveto", dp, bin_drive])
    json.dump({"id": bid, "kind": k, "at": time.time(), "files": moved, "reg": regs, "drive": [dp, bin_drive] if dp else None,
               "name": os.path.basename(f)}, open(f"{d}/manifest.json", "w"), indent=1)
    return {"ok": True, "id": bid}

def undo(bid):
    d = f"{BIN}/{os.path.basename(bid)}"; m = jload(f"{d}/manifest.json", None)
    if not m: sys.exit("nothing to undo")
    for a, b in m["files"]: os.makedirs(os.path.dirname(a), exist_ok=True); shutil.move(b, a)
    f = m["files"][0][0]
    if m["kind"] == "dark":
        os.makedirs(TG, exist_ok=True)
        try: os.link(f, f"{TG}/{os.path.basename(f)}")
        except OSError: pass
    with reg_lock() as r: r["items"].update(m["reg"]); save_reg(r)
    if m.get("drive"): bg(["rclone", "moveto", m["drive"][1], m["drive"][0]])
    shutil.rmtree(d); return {"ok": True, "file": f}

def bin_list(): return sorted((jload(f, {}) for f in glob.glob(f"{BIN}/*/manifest.json")), key=lambda m: -m.get("at", 0))
def purge(days=7):
    n = 0
    for m in bin_list():
        if time.time() - m.get("at", 0) > days * 86400:
            shutil.rmtree(f"{BIN}/{m['id']}", ignore_errors=True); n += 1
            if m.get("drive"): bg(["rclone", "purge", os.path.dirname(m["drive"][1])])
    return {"ok": True, "purged": n}

if __name__ == "__main__":
    a = sys.argv[1:]; cmd = a[0] if a else "list"
    r = (listing() if cmd == "list" else edit(a[1], json.loads(a[2])) if cmd == "edit" else move(a[1], a[2]) if cmd == "move"
         else delete(a[1]) if cmd == "delete" else undo(a[1]) if cmd == "undo" else bin_list() if cmd == "bin" else purge() if cmd == "purge" else None)
    if r is None: sys.exit(__doc__)
    print(json.dumps(r, ensure_ascii=False))
