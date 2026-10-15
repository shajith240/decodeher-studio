# Assets (strict)

- Reuse first. Every reel has `shots.json`; run `node tools/assets.js need reels/<reel>/shots.json`. It reuses indexed stills and
  generates only the missing ones (same characters via the reference still), then indexes them.
- Ids: `him/<name>`, `her/<name>`, `fx/<name>`. Names describe the situation (`table_wait`, `bed_texting`), not the pose geometry.
- After generating, run `node tools/vault_sync.js` and look at [[assets/cast]] / [[assets/fx]] — reject anything wrong (delete the png + index entry).
- Never use downloaded third-party footage, clip-art, or Pinterest images.
