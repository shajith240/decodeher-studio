#!/usr/bin/env bash
# Google Drive <-> runner sync for the cloud factory (contract: brain/cloud-architecture.md). Code lives in git; the big files
# (reels, library, deliverables, logs, approved captions) live on Drive under gdrive:decodeher/.
#
#   tools/cloud/sync.sh pull    Drive → here. Files already here are skipped. Writes a manifest of what is here afterwards.
#   tools/cloud/sync.sh push    here → Drive (rclone copy --update: only newer/changed files, never the big temp files).
#                               Files this run DELETED (in the manifest, gone now) are deleted on Drive too, so a booked reel's
#                               moved *-FINAL.mp4 or a removed queue marker never comes back on the next pull (re-booking trap).
#   Hard links: fetch_pool.py hard-links reels/_pool clips into each reel's clips/cand/ (2.7 GB on disk, 9 GB as plain files).
#   Drive has no hard links, so push uploads only the pool copy and writes reels/.hardlinks.tsv (cand path → pool path);
#   pull re-creates the links from it.
#   tools/cloud/sync.sh prune   Drive space (15 GB): delete clips/cand/ older than 14 days of reels already POSTED. Dry run unless APPLY=1.
#
# Env: RCLONE_CONF  rclone.conf CONTENT (GitHub secret) — written to a private temp file, never printed. Without it the normal
#                   rclone config is used.
#      REMOTE       default gdrive:decodeher        DRY=1  print what would happen, change nothing (pull/push)
#      SYNC_STATE   default .sync (manifest dir)    POSTED="slug slug"  prune: override the posted list (else asked from the relay)
#      SYNC_PATHS   override the synced paths (space separated, e.g. only one reel for approve.yml)
#      MAX_DELETE   push refuses to delete more than this many Drive files in one run (default 300; something went wrong)
set -euo pipefail
cd "$(dirname "$0")/../.."
MODE="${1:-}"; REMOTE="${REMOTE:-gdrive:decodeher}"; REMOTE="${REMOTE%/}"
read -r -a PATHS <<< "${SYNC_PATHS:-reels library deliverables logs brain/content/captions}"
STATE="${SYNC_STATE:-.sync}"; MANIFEST="$STATE/manifest.txt"
DRYRUN=(); NOTE=""; [ "${DRY:-}" = 1 ] && { DRYRUN=(--dry-run); NOTE="  (dry run)"; }
case "$MODE" in pull|push|prune) ;; *) echo "usage: $0 pull|push|prune   (DRY=1 for a dry run; prune is dry unless APPLY=1)" >&2; exit 2;; esac

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
if [ -n "${RCLONE_CONF:-}" ]; then
  ( umask 077; printf '%s\n' "$RCLONE_CONF" > "$TMP/rclone.conf" ); export RCLONE_CONFIG="$TMP/rclone.conf"
fi
# never moved: the re-cut film and raw render (~600 MB each, rebuilt by every render), half-written files, secrets, locks
cat > "$TMP/exclude.txt" <<'EOF'
**/renders/raw.mp4
**/assets/bg.mp4
*.part
*.part.mp4
**/.env
**/.relay.json
*.lock
**/__pycache__/**
**/node_modules/**
EOF
skip(){ case "$1" in */renders/raw.mp4|*/assets/bg.mp4|*.part|*.part.mp4|*/.env|*/.relay.json|*.lock|*/__pycache__/*|*/node_modules/*) return 0;; esac; return 1; }
FLAGS=(--exclude-from "$TMP/exclude.txt" --transfers 8 --checkers 16 --drive-chunk-size 64M --stats 2m --stats-one-line --stats-log-level NOTICE)
FLAGS+=("${DRYRUN[@]}")
run(){ echo "+ rclone $1 $2 → $3$NOTE"; rclone "$@" "${FLAGS[@]}"; }

if [ "$MODE" = pull ]; then
  for p in "${PATHS[@]}"; do
    mkdir -p "$p"
    # exit 3 = the folder is not on Drive yet (first run): fine
    set +e; run copy "$REMOTE/$p" "$p" --ignore-existing; rc=$?; set -e
    [ $rc = 0 ] || [ $rc = 3 ] || { echo "pull failed for $p (rclone exit $rc)" >&2; exit $rc; }
  done
  # re-create the pool hard links (see top); a link whose pool clip is missing is skipped (the clip stage re-fetches it)
  if [ -f reels/.hardlinks.tsv ]; then
    n=0; miss=0
    while IFS=$'\t' read -r c p; do
      [ -e "$c" ] && continue
      if [ ! -f "$p" ]; then miss=$((miss + 1)); continue; fi
      if [ "${DRY:-}" = 1 ]; then n=$((n + 1)); continue; fi
      mkdir -p "$(dirname "$c")"; ln "$p" "$c"; n=$((n + 1))
    done < reels/.hardlinks.tsv
    echo "hard links re-created: $n${NOTE}$([ $miss = 0 ] || echo " · $miss skipped (pool clip missing)")"
  fi
  if [ "${DRY:-}" != 1 ]; then
    mkdir -p "$STATE"; find "${PATHS[@]}" -type f 2>/dev/null | LC_ALL=C sort > "$MANIFEST"
    echo "manifest: $(wc -l < "$MANIFEST") files"
  fi
  exit 0
fi

if [ "$MODE" = push ]; then
  for p in "${PATHS[@]}"; do
    [ -d "$p" ] || continue
    if [ "$p" = reels ] && [ -d reels/_pool ]; then
      # cand files sharing an inode with a pool clip → reels/.hardlinks.tsv (not uploaded); the others are uploaded as files
      find reels/_pool -type f -printf '%i\t%p\n' > "$TMP/pool.tsv"
      find reels -path 'reels/*/clips/cand/*' -type f -printf '%i\t%p\n' > "$TMP/cand.tsv"
      awk -F'\t' -v solo="$TMP/solo.txt" 'NR==FNR { pool[$1] = $2; next } ($1 in pool) { print $2 "\t" pool[$1]; next } { sub(/^reels\//, "", $2); print $2 > solo }' \
        "$TMP/pool.tsv" "$TMP/cand.tsv" > "$TMP/hardlinks.tsv"
      touch "$TMP/solo.txt"
      if [ "${DRY:-}" != 1 ] && ! cmp -s "$TMP/hardlinks.tsv" reels/.hardlinks.tsv 2>/dev/null; then cp "$TMP/hardlinks.tsv" reels/.hardlinks.tsv; fi
      echo "  hard links kept as a list: $(wc -l < "$TMP/hardlinks.tsv") · cand files uploaded as files: $(wc -l < "$TMP/solo.txt")"
      run copy reels "$REMOTE/reels" --update --exclude "/*/clips/cand/**"
      if [ -s "$TMP/solo.txt" ]; then rclone copy reels "$REMOTE/reels" --update --files-from-raw "$TMP/solo.txt" --transfers 8 --checkers 16 "${DRYRUN[@]}"; fi
    else run copy "$p" "$REMOTE/$p" --update; fi
  done
  # deletions made by this run (only files the pull brought or found here; nothing outside the manifest is ever deleted)
  if [ -f "$MANIFEST" ]; then
    : > "$TMP/gone.txt"
    while IFS= read -r f; do [ -e "$f" ] || skip "$f" || printf '%s\n' "$f" >> "$TMP/gone.txt"; done < "$MANIFEST"
    n=$(wc -l < "$TMP/gone.txt")
    if [ "$n" -gt "${MAX_DELETE:-300}" ]; then
      echo "NOT deleting $n files on Drive (over MAX_DELETE=${MAX_DELETE:-300}) — check what removed them" >&2; head -20 "$TMP/gone.txt" >&2
    elif [ "$n" -gt 0 ]; then
      echo "+ delete on Drive: $n file(s) this run removed$NOTE"; sed 's/^/    - /' "$TMP/gone.txt" | head -50
      rclone delete "$REMOTE" --files-from-raw "$TMP/gone.txt" "${DRYRUN[@]}"
    fi
    # the next push in this job compares against what is here now
    [ "${DRY:-}" = 1 ] || find "${PATHS[@]}" -type f 2>/dev/null | LC_ALL=C sort > "$MANIFEST"
  else echo "no manifest (no pull in this job): Drive deletions skipped"; fi
  exit 0
fi

# prune: posted reels only, clips/cand/ only, files older than 14 days only
if [ -n "${POSTED:-}" ]; then posted="$POSTED"
else
  ids=$(node tools/ig_queue.js ids) || { echo "relay unreachable: nothing pruned" >&2; exit 1; }
  # relay titles look like "03-W2-your-plans-matter" (queue_reel.sh: slug minus "w2-NN-", first 28 chars)
  titles=$(echo "$ids" | awk '$2=="posted"{print $NF}' | sed -E 's/^[0-9]+-W[0-9]+-//')
  posted=""
  for d in $(rclone lsf --dirs-only "$REMOTE/reels" 2>/dev/null | sed 's|/$||'); do
    part=$(echo "$d" | cut -d- -f3- | cut -c1-28)
    if [ -n "$part" ] && echo "$titles" | grep -qxF -- "$part"; then posted="$posted $d"; fi
  done
fi
[ -n "${posted// /}" ] || { echo "no posted reels: nothing to prune"; exit 0; }
for d in $posted; do
  echo "+ prune $REMOTE/reels/$d/clips/cand (older than 14 days)$([ "${APPLY:-}" = 1 ] && echo "  APPLY")"
  if [ "${APPLY:-}" = 1 ]; then rclone delete "$REMOTE/reels/$d/clips/cand" --min-age 14d && rclone rmdirs "$REMOTE/reels/$d/clips/cand" --leave-root || true
  else rclone delete "$REMOTE/reels/$d/clips/cand" --min-age 14d --dry-run 2>&1 | grep -c "Skipped delete" | sed 's/^/    would delete files: /' || true; fi
done
[ "${APPLY:-}" = 1 ] || echo "(dry run — APPLY=1 to delete)"
