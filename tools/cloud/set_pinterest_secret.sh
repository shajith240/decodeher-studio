#!/usr/bin/env bash
# OWNER RUNS THIS (10-16): copies ONLY the Pinterest login cookies from Brave into the GitHub secret PINTEREST_COOKIES, so the
# cloud factory can search Pinterest. Nothing is printed; the temp file is deleted. Re-run if Pinterest logs you out.
set -euo pipefail
cd "$(dirname "$0")/../.."
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
uv run -q --with yt-dlp --with secretstorage yt-dlp --cookies-from-browser brave+gnomekeyring --cookies "$T/all.txt" --skip-download --no-warnings "https://www.pinterest.com/" >/dev/null 2>&1 || true
{ echo "# Netscape HTTP Cookie File"; grep -E "^\S*pinterest\.com\s" "$T/all.txt" || true; } > "$T/pin.txt"
n=$(grep -vc "^#" "$T/pin.txt" || true)
[ "$n" -ge 3 ] || { echo "Could not find your Pinterest login in Brave ($n cookies). Log in to pinterest.com in Brave and run this again."; exit 1; }
gh secret set PINTEREST_COOKIES < "$T/pin.txt"
echo "Done: the cloud factory now has your Pinterest login ($n cookies, Pinterest only)."
