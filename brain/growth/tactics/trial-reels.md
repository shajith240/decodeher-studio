# trial-reels
Status: idea (parked, needs the owner)
- What: Instagram Trial Reels show a reel to non-followers first; you pick afterwards whether followers see it.
- Why: lets us test hooks on cold viewers without dragging the main reel's numbers down.
- Our pipeline: the toggle is app-side. Our Cloudflare relay posts through the API; whether the API can set "trial" is unchecked. Changing the posting process needs the owner's OK.
- Evidence: [[2026-10-19-owner-tip-damini-algorithm-signals]] (official feature, low priority).
