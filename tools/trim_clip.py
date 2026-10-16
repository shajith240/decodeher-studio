"""Keep only the useful head of a downloaded clip (owner 10-16: "we use a small portion; 1-minute clips waste Drive space").
Usage: python3 tools/trim_clip.py <seconds> <file.mp4> [...]   — files longer than <seconds>+2 are cut to the first <seconds>
in place, losslessly (stream copy: instant, no quality change). Shorter files are left alone. Hard links are respected:
the file is rewritten in place, so every link sees the trimmed clip. Also importable: trim(path, seconds)."""
import os, subprocess, sys, tempfile

def dur(f):
    try: return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).decode())
    except Exception: return 0.0
def trim(f, secs):
    d = dur(f)
    if d <= secs + 2: return False
    fd, tmp = tempfile.mkstemp(suffix=".mp4", dir=os.path.dirname(os.path.abspath(f))); os.close(fd)
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-t", str(secs), "-c", "copy", "-map", "0", "-movflags", "+faststart", tmp])
    if r.returncode != 0 or dur(tmp) < min(secs, d) - 1.5: os.remove(tmp); return False
    with open(tmp, "rb") as src, open(f, "r+b") as dst: dst.write(src.read()); dst.truncate()   # in place: hard links stay valid
    os.remove(tmp); return True
if __name__ == "__main__":
    secs = float(sys.argv[1]); n = sum(trim(f, secs) for f in sys.argv[2:]); print(f"trimmed {n} of {len(sys.argv) - 2} clips to {secs:g} s")
