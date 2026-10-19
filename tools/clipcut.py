"""Cut the picked clips (tools/clippick.py) into one graded vertical background film.
Usage: python3 tools/clipcut.py <reel_dir>
Each shot runs from its phrase start to the next phrase start (the outro shot is left to the composition). Every clip is
cropped to 9:16, given ONE shared grade and its own eased camera move, so footage from many sources reads as one film.
Then ONE film finish over the whole background film (owner 10-14: on the clips only, never on the captions, and natural, not an
overlay image): fresh film grain every frame (generated, slightly clumped like film stock), a vintage grade (lifted blacks,
softened whites, a warm tint), a soft highlight bloom (halation) and a gentle vignette.
Writes <reel>/assets/bg.mp4 (1080x1920, 30 fps, no audio)."""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from activity import log
R = os.path.abspath(sys.argv[1]); shots = json.load(open(f"{R}/shots.json")); pick = json.load(open(f"{R}/clips/pick.json"))
# owner 10-16: a chosen HOOK clip (reel.json "hookClip": {"file": <path under the reel>, "start": s}) always opens the reel
_hk = json.load(open(f"{R}/reel.json")).get("hookClip")
if _hk: pick["0"] = {"file": os.path.relpath(os.path.join(R, _hk["file"]), f"{R}/clips/cand"), "start": _hk.get("start", 0)}
S = f"{R}/clips/seg"; os.makedirs(S, exist_ok=True); os.makedirs(f"{R}/assets", exist_ok=True)
# 10-16: the page may start the outro LATER than the OUTRO shot (fill_page.py moves it so it ends with the reel) — the film runs on until then
_pg = open(f"{R}/index.html").read() if os.path.exists(f"{R}/index.html") else ""
_m = re.search(r"END = ([\d.]+);", _pg)
for s in shots:
    if s["q"] == "OUTRO" and _m and float(_m.group(1)) > s["t"]: s["t"] = float(_m.group(1))
end = next((s["t"] for s in shots if s["q"] == "OUTRO"), None)
# one shared grade: mute the cartoon colours a touch and cap highlights at ~80 % (Zoltium's trick, measured 10-14) so the gold
# caption is always the brightest thing on screen
GRADE = "eq=contrast=1.06:saturation=0.86:brightness=-0.02,curves=all='0/0 0.5/0.47 1/0.80'"
# owner 10-14: "the background always moves left to right, not natural" — each shot gets its own move, eased in/out (smoothstep),
# never the same move twice in a row. Worked at 2x size (2160x3840) and scaled down, so slow moves glide instead of stepping.
MOVES = {   # (zoom start, zoom end, x start, x end, y start, y end) — x/y as a share of the free space around the zoomed window
    "push": (1.00, 1.09, .5, .5, .5, .5), "pull": (1.09, 1.00, .5, .5, .5, .5), "pan_l": (1.08, 1.08, .85, .15, .5, .5),
    "pan_r": (1.08, 1.08, .15, .85, .5, .5), "tilt": (1.08, 1.08, .5, .5, .8, .25), "hold": (1.03, 1.03, .5, .5, .5, .5)}
ORDER = ["push", "pan_r", "hold", "pull", "pan_l", "tilt", "push", "pan_l", "pull", "pan_r", "tilt", "hold"]
def move_vf(n, d):
    m = ORDER[n % len(ORDER)] if d >= 1.2 else ("hold" if n % 2 else "push")   # very short shots: barely move
    zs, ze, xs, xe, ys, ye = MOVES[m]; N = max(1, round(d * 30))
    E = f"st(0,min(on/{N},1));ld(0)*ld(0)*(3-2*ld(0))"
    return (f"zoompan=z='{zs}+({ze}-{zs})*({E})':x='(iw-iw/zoom)*({xs}+({xe}-{xs})*({E}))':y='(ih-ih/zoom)*({ys}+({ye}-{ys})*({E}))'"
            f":d=1:s=1080x1920:fps=30"), m
# owner 10-14: black gaps look like a bug.
# a later line without a clip continues the shot before it, so only an empty FIRST shot stops the build
if "0" not in pick and not shots[0].get("hold"): sys.exit(f'no clip for the opening shot "{shots[0]["say"]}" — re-search it')
def _yavg(src, t):   # mean brightness (0-255) of the frame at t; looped clips wrap around
    try:
        du = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())
        y = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t % max(du, 0.1)), "-i", src, "-frames:v", "1", "-vf", "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-", "-f", "null", "-"], capture_output=True, text=True).stdout
        return float(y.split("YAVG=")[-1].split()[0])
    except (ValueError, IndexError, subprocess.CalledProcessError): return 255.0
def _dark(src, t, d):   # 10-17: True if ANY frame in [t, t+d] is near-black (4 checks/s; a 3-point check missed a 1 s fade-out)
    try:
        du = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())
        if t + d > du: return any(_yavg(src, t + k * d / 8) < 22 for k in range(9))   # looped window: spot checks
        y = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-t", str(d), "-i", src, "-vf", "fps=4,signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-", "-f", "null", "-"], capture_output=True, text=True).stdout
        return any(float(v) < 22 for v in re.findall(r"YAVG=([0-9.]+)", y))
    except (ValueError, subprocess.CalledProcessError): return False
segs, moves = [], []; prev, prev_d = None, 0
# 10-16 owner: the AI-woman hook is NOT chopped after one caption group — it plays as one continuous shot for the whole hook
# line (until the "Listen…" snap), limited only by how much clip there is after its start point
HOOK_SKIP, HOOK_END = set(), None
_he = json.load(open(f"{R}/reel.json")).get("hookEnd")   # chosen by fill_page.py: 2.5-4 s, at a sentence end
if _hk and _he:
    _k = min(range(1, len(shots)), key=lambda i: abs(shots[i]["t"] - _he))
    if _k > 1 and abs(shots[_k]["t"] - _he) < 0.05: HOOK_SKIP = set(range(1, _k)); HOOK_END = shots[_k]["t"]
for n, s in enumerate(shots):
    if s["q"] == "OUTRO": break
    if n in HOOK_SKIP: continue
    t0 = 0.0 if n == 0 else s["t"]; t1 = HOOK_END if (n == 0 and HOOK_END) else shots[n + 1]["t"]; d = round(t1 - t0, 3)
    p = pick.get(str(n))
    out = f"{S}/{n:02d}.mp4"
    if not p and prev and _hk and prev.get("file") == pick["0"]["file"]:   # 10-19 owner: the AI-woman hook NEVER continues under captions —
        _nx = next((pick[str(m)] for m in range(n + 1, len(shots)) if pick.get(str(m)) and shots[m]["q"] != "OUTRO"), None)   # borrow the next line's clip
        if _nx: p = dict(_nx)
    if not p and prev:   # no clip for this line (owner 10-14: black gaps look like a bug) — the previous shot simply CONTINUES
        p = dict(prev); p["start"] = round(prev["start"] + prev_d, 2)
        # 10-16: a continued clip can run into its own fade-to-black ending (2 s of black under the closing words) — if the
        # continuation is dark anywhere in this shot, replay the clip from where it first started instead
        _src = f"{R}/clips/cand/{p['file']}"
        if os.path.exists(_src) and _dark(_src, p["start"], d): p["start"] = p.get("orig", prev["start"])
    if not p:   # nothing before it either (very first shot): a black hold, the caption carries it
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=1080x1920:r=30:d={d}", "-c:v", "libx264", "-pix_fmt", "yuv420p", out], check=True)
    if p and not os.path.exists(f"{R}/clips/cand/{p['file']}") and os.path.exists(out):
        # 10-17 remake (e.g. only a new hook clip): the downloads were cleaned up after the first render, so keep the piece
        # already cut from it (same shot timings: the voice is unchanged)
        segs.append(out); prev, prev_d = (p if "orig" in p else {**p, "orig": p["start"]}), d; continue
    if p:
        src = f"{R}/clips/cand/{p['file']}"
        for _ in range(8):   # 10-16: a clip that opens on black frames (fade-in) showed as a black shot — step past them
            y = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(p["start"]), "-i", src, "-frames:v", "1", "-vf", "signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-", "-f", "null", "-"], capture_output=True, text=True).stdout
            try: yavg = float(y.split("YAVG=")[-1].split()[0])
            except (ValueError, IndexError): break
            if yavg >= 22: break
            p = dict(p); p["start"] = round(p["start"] + 0.5, 2)
        # 10-17 test reel: the start frame was fine but the clip faded to black MID-shot (a 1.5 s black stretch). Check the
        # middle and end of the window too; if dark, slide the window to the first spot that stays lit all the way through
        if _dark(src, p["start"], d):
            try: _du = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())
            except (ValueError, subprocess.CalledProcessError): _du = 0
            for s0 in [x * 0.5 for x in range(int(max(_du - 0.2, 0) / 0.5) + 1)]:
                if not _dark(src, s0, d): p = dict(p); p["start"] = s0; break
        mv, name = move_vf(n, d); moves.append(name)
        vf = f"fps=30,scale=2160:3840:force_original_aspect_ratio=increase:flags=lanczos,crop=2160:3840,{mv},{GRADE},format=yuv420p"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(p["start"]), "-stream_loop", "-1", "-i", src,
                        "-t", str(d), "-vf", vf, "-an", "-c:v", "libx264", "-crf", "18", "-preset", "veryfast", out], check=True)
    segs.append(out); prev, prev_d = (p if (not p or "orig" in p) else {**p, "orig": p["start"]}), d; log(f"Cutting clips · {os.path.basename(R)} · shot {n + 1} of {len(shots) - 1}")
lst = f"{S}/list.txt"; open(lst, "w").write("".join(f"file '{x}'\n" for x in segs))
FILM = ("[0:v]format=yuv420p,split[img][hi];[hi]curves=all='0/0 0.62/0 1/1',gblur=sigma=14[bloom];[img][bloom]blend=all_mode=screen:all_opacity=0.16,"
        "curves=all='0/0.045 0.5/0.49 1/0.93',colorbalance=rs=.025:bs=-.03:rh=.015:bh=-.02,eq=saturation=0.93,vignette=angle=PI/5,format=yuv420p[pic];"
        "color=c=gray:s=720x1280:r=30,noise=alls=48:allf=t+u,scale=1080:1920:flags=bilinear,format=yuv420p[grain];"
        "[pic][grain]blend=all_mode=overlay:all_opacity=0.5:shortest=1,format=yuv420p[o]")
# owner 10-15: "make everything black and white, then white captions on it — that's our brand" (config.json reels.look = "bw"):
# no colour at all, a touch more contrast, pushed a little darker with a deeper vignette and whites capped at ~68 % (Zoltium's trick) so the white serif caption is always the brightest thing on screen
RJ = json.load(open(f"{R}/reel.json"))
if (json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "config.json"))).get("reels", {}).get("look") == "bw") and not RJ.get("colour"):
    FILM = FILM.replace("colorbalance=rs=.025:bs=-.03:rh=.015:bh=-.02,eq=saturation=0.93,vignette=angle=PI/5",
                        "hue=s=0,eq=contrast=1.12:brightness=-0.04,curves=all='0/0 0.5/0.42 1/0.68',vignette=angle=PI/4.2")
# growth plan 10-15, v3 reels only (reel.json "format": "v3"): the first 3 s must never read as an empty dark screen — the same
# grade and vignette, but a lifted curve (blacks not crushed, mid-grey subjects, whites to ~90 %) that eases back into the normal
# grade between 2.6 s and 3.4 s. Every other reel's film is untouched.
if json.load(open(f"{R}/reel.json")).get("format") == "v3":
    FILM = FILM.replace(",format=yuv420p[pic];", ",format=yuv420p[pic0];[pic0]split[dk][lt];"
                        "[lt]curves=all='0/0.08 0.25/0.36 0.5/0.62 0.75/0.82 1/0.92'[lift];"
                        "[dk][lift]blend=all_expr='A+(B-A)*clip((3.4-T)/0.8,0,1)',format=yuv420p[pic];", 1)
# owner 10-16 (Rebelvids course format, reel.json "frame": "lens"): the clip sits in a lens-shaped window (straight sides, curved
# top and bottom: a 860x1500 frame cut by a circle) centred on the pack's black paper texture
EXTRA = []
if RJ.get("frame") == "lens":   # owner 10-16 (2nd try): FULL-SCREEN clip as before; only the top/bottom EDGES curve (a 1000 px circle
    # cuts the corners, ~120 px at the sides, nothing at the centre); the pack's black paper sits OVER the clip as a soft texture
    PK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "library/rebel-pack")
    EXTRA = ["-loop", "1", "-i", f"{PK}/paper-overlay-1080.png", "-loop", "1", "-i", f"{PK}/edge-mask-soft.png"]   # 10-16 owner: soft vignette fade, not a sharp curve
    FILM = FILM.replace("format=yuv420p[o]", "format=yuv420p[full];[1:v]format=yuv420p[pp];[full][pp]blend=all_mode=softlight:all_opacity=0.35,format=yuva420p[tx];"
                        "[2:v]format=gray[mk];[tx][mk]alphamerge[wa];color=c=black:s=1080x1920:r=30[bk];[bk][wa]overlay=0:0:shortest=1,format=yuv420p[o]")
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, *EXTRA, "-filter_complex", FILM, "-map", "[o]",
                "-t", str(round(sum(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", x]).decode()) for x in segs) + 0.1, 2)),   # hard cap: never longer than the shots
                "-c:v", "libx264", "-crf", "15", "-tune", "grain", "-preset", "veryfast", "-g", "15", "-movflags", "+faststart", f"{R}/assets/bg.mp4"], check=True)   # -tune grain: the encoder keeps the grain instead of smoothing it away
d = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"{R}/assets/bg.mp4"]).decode().strip()
print(f"bg.mp4: {len(segs)} shots, {d} s (outro starts at {end}); moves: {' '.join(moves)}")
