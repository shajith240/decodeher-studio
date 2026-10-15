#!/usr/bin/env bash
# Install everything the factory needs on a fresh GitHub Actions runner (ubuntu-24.04, x86_64). Safe to run twice: each step
# skips what is already there. Contract: brain/cloud-architecture.md. Usage: bash tools/cloud/setup.sh
#   ffmpeg + rubberband-cli (voice/mix/render), fonts + Chrome's shared libraries (HyperFrames renders in headless Chrome),
#   node 22, uv (+ Python 3.11 for the tools run with `uv run --python 3.11`), the claude CLI (plan + judge steps),
#   HyperFrames warmed up (its own Chrome downloaded once), rclone (tools/cloud/sync.sh). Prints every version at the end.
set -euo pipefail
cd "$(dirname "$0")/../.."
SUDO=""; [ "$(id -u)" = 0 ] || SUDO="sudo"
have(){ command -v "$1" >/dev/null 2>&1; }
say(){ echo "== $*"; }

# 1. system packages (one apt run, only when something is missing)
PKGS=(ffmpeg rubberband-cli fonts-liberation fonts-dejavu-core fonts-noto-core fonts-noto-color-emoji fontconfig
      libnss3 libatk1.0-0t64 libatk-bridge2.0-0t64 libcups2t64 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3
      libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2t64 libxshmfence1 libgtk-3-0t64 sqlite3 jq unzip curl ca-certificates)
missing=(); for p in "${PKGS[@]}"; do dpkg -s "$p" >/dev/null 2>&1 || missing+=("$p"); done
if [ ${#missing[@]} -gt 0 ]; then
  say "apt: ${missing[*]}"
  $SUDO apt-get update -qq
  DEBIAN_FRONTEND=noninteractive $SUDO apt-get install -y -qq --no-install-recommends "${missing[@]}" >/dev/null
else say "apt: all present"; fi

# 2. node 22 (the runner image ships one; actions/setup-node in the workflow pins it — this is the fallback)
if ! have node || [ "$(node -p 'process.versions.node.split(".")[0]')" -lt 22 ]; then
  say "node 22"
  curl -fsSL https://deb.nodesource.com/setup_22.x | $SUDO -E bash - >/dev/null
  $SUDO apt-get install -y -qq nodejs >/dev/null
fi

# 3. uv + Python 3.11
if ! have uv; then say "uv"; curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null; export PATH="$HOME/.local/bin:$PATH"; fi
[ -n "${GITHUB_PATH:-}" ] && echo "$HOME/.local/bin" >> "$GITHUB_PATH"
uv python install 3.11 >/dev/null 2>&1 || true

# 4. rclone (Drive sync)
if ! have rclone; then say "rclone"; curl -fsSL https://rclone.org/install.sh | $SUDO bash >/dev/null; fi

# 5. claude CLI (auth comes from env CLAUDE_CODE_OAUTH_TOKEN at run time)
if ! have claude; then
  say "claude CLI"
  if [ -w "$(npm prefix -g)/lib" ] 2>/dev/null; then npm install -g --silent @anthropic-ai/claude-code; else $SUDO npm install -g --silent @anthropic-ai/claude-code; fi
fi

# 6. project node deps (puppeteer) and HyperFrames, warmed up: npx cache + its own headless Chrome (cached in ~/.cache/hyperframes)
if [ -f package.json ] && [ ! -d node_modules/puppeteer ]; then say "npm install"; npm install --silent --no-audit --no-fund; fi
say "hyperframes warm-up"
npx -y hyperframes --version >/dev/null
npx -y hyperframes browser ensure >/dev/null 2>&1 || npx -y hyperframes browser ensure

# 7. Python deps the `uv run --with …` steps pull: fetch once now so the first job is not slow (cached by actions/cache ~/.cache/uv)
uv run -q --python 3.11 --with faster-whisper --with numpy --with scipy --with soundfile --with pyloudnorm --with librosa \
  --with gallery-dl --with yt-dlp --with secretstorage python -c "pass" >/dev/null 2>&1 || echo "warn: uv warm-up failed (steps will retry)"

say "versions"
ffmpeg -version | head -1
rubberband --version 2>&1 | head -1 || true
echo "node $(node --version) · npm $(npm --version)"
uv --version
uv run -q --python 3.11 python --version
python3 --version
rclone version | head -1
claude --version 2>/dev/null || echo "claude: not on PATH"
echo "hyperframes $(npx -y hyperframes --version 2>/dev/null | tail -1)"
echo "chrome: $(npx -y hyperframes browser path 2>/dev/null | tail -1)"
df -h . | tail -1 | awk '{print "disk free: " $4}'
