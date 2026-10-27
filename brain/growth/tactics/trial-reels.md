# trial-reels
Status: idea (parked, needs the owner)
- What: Instagram Trial Reels show a reel to non-followers only; you decide afterwards whether followers see it.
- Why: lets us test hooks on cold viewers. Our followers are only 74, so our normal reels already act as a cold audition ([[audition-first-batch]]); the gain is small for now.
- Our pipeline: the toggle is app-side. Our Cloudflare relay posts through the API; whether the API can set "trial" is unchecked (CLAUDE.md open work).
- Evidence: [[2026-10-19-owner-tip-damini-algorithm-signals]], [[2026-10-27-hootsuite-instagram-features-2026]] (official feature, vendor description).
