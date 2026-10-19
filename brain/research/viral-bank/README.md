# Viral bank

Proven viral shorts in our niche (1M+ views) that every @thedecodeher reel remixes (owner rule 10-19, "steal like an artist"). Each platform agent appends its own section below. Mark a source as used by setting `used_by` to the reel id so no idea is reused.

## YouTube Shorts / TikTok

Updated 2026-10-19. Data: [yt-tiktok.jsonl](yt-tiktok.jsonl), 81 shorts, all with at least 1M views. Each row has the transcript, an English translation for Hindi shorts (`transcript_en`), the on-screen text for silent text-card shorts (`onscreen_text`), hook, concept, structure, visual, why it worked, `fits_us`, `our_version`, `added` and `used_by`. The 10 sources already remixed in batches v4 and v5 are marked as used. The 360p videos and 3-frame strips are in `library/research/viral/yt/` (git-ignored).

**Refill:** `python3 tools/viral_bank_yt.py --transcribe` reads [sources-yt.txt](sources-yt.txt) (35 searches and 59 channels). Each run takes a rotating slice of the searches, both all-time and this year, reads every channel's Shorts tab, and adds only new shorts with at least 1M views (30 by default, biggest first). Other commands: `--fill` transcribes rows that were added without `--transcribe`, `--add <id>` adds one short, `--mark <id>=<reel>` records which reel used it, and `--list` previews without writing. Off-niche hits go on a `skip:` line in the sources file.

**TikTok:** anonymous access is blocked. yt-dlp fails on user pages ("Unable to extract secondary user ID") and on tag pages (the extractor is marked broken), even with browser impersonation, so this bank holds YouTube Shorts only.

### Top 25 remix candidates (not used yet, ranked by views)

1. **46.5M** · OutOfPocket · [Is she DELUSIONAL? What do you think? #shorts #streetintervi](https://www.youtube.com/shorts/x9hjPNTr3L0)  
   Our version: Her checklist says 6 ft and 200K. Here is what actually makes her choose a man.
2. **32.8M** · Coach Kyle · [How Girls Drop Hints LOL🤣](https://www.youtube.com/shorts/IWfbNCccMqc)  
   Our version: The 5 hints she drops that you keep missing (and what each one means).
3. **25.8M** · Steph Speaks · [cold approach in a grocery store 😬 #shorts #stephspeaks #att](https://www.youtube.com/shorts/svwHvdwtFFA)  
   Our version: Why shooting your shot and hearing 'I have a man' is still a win (rejection psychology).
4. **25.4M** · 1 Minute Talk Show · [What Girls Mean When They Text](https://www.youtube.com/shorts/gnWCOU0JUnw)  
   Our version: What her texts really mean: 'I'm so busy', 'haha', 'we'll see', 'you're sweet', 'k' — decoded.
5. **24.2M** · Ngamshishi · [is this a red flag or nah? #shorts #explorepage #movies #cel](https://www.youtube.com/shorts/LUuiQcLHDeU)  
   Our version: Is looking at another girl in front of her cheating? What her brain reads in that glance.
6. **18.6M** · Kuldeep Singhania Shorts · [How Women Manipulate Men in Kalyug 😲💀 | Kuldeep Singhaniaa #](https://www.youtube.com/shorts/1IxBTuN5-t0)  
   Our version: She asks for 45K, then settles for 5K: the door-in-the-face trick, decoded.
7. **13.9M** · Jumana Abdu Rahman · [When your crush looks at you ☺️](https://www.youtube.com/shorts/TWQkzNbX6_M)  
   Our version: The 3 things her face does in the second her crush looks at her.
8. **13.0M** · WHATS CHATS · [She friendzoned herself! 💀😂 #shorts #funny #texting #friendz](https://www.youtube.com/shorts/LVpGtG7mVSg)  
   Our version: She replied 'nice, send it' — the texting mistake that friend-zones you.
9. **13.0M** · Isaiah Miranda · [When she plays hard to get 😂 #shorts](https://www.youtube.com/shorts/_mQ4yTX6pqg)  
   Our version: Why she plays hard to get, and the one move that ends the game.
10. **10.2M** · Kiran Kumar · [Biggest Red Flags In A Girl!](https://www.youtube.com/shorts/5wKfvQz_hBA)  
   Our version: Biggest red flags in a girl, in 30 seconds (number 3 is about how she talks about her ex).
11. **8.1M** · SochShift · [3 Psychology Tricks #Shorts](https://www.youtube.com/shorts/SHIm14LwPtI)  
   Our version: 3 things that make her notice you without saying a word.
12. **8.0M** · How to Beast Talks · [why she friend zoned you 🙅‍♀️](https://www.youtube.com/shorts/bjEEswGXFrk)  
   Our version: 3 texts that put you in the friend zone — and what to send instead.
13. **7.2M** · Alana Lintao · [girls flirting when they aren't interested vs when they are😭](https://www.youtube.com/shorts/RFBVRn7KYBk)  
   Our version: If she gets awkward around you, read this: why nervous = interested.
14. **6.6M** · RSH MindTree · [Psychology Facts About Girls. #shorts #psychologyfacts](https://www.youtube.com/shorts/QApLF4YCz_8)  
   Our version: A woman is more attracted to you when she isn't sure how much you like her: the uncertainty effect, decoded.
15. **6.4M** · QuickMindFacts · [When Girls Have These 5 Qualities, Boys Get Weak... #shorts](https://www.youtube.com/shorts/2vc5f2ihBhc)  
   Our version: When a man has these 5 traits, she gets weak (honest attraction version).
16. **5.2M** · Cayden Morack · [texts that give girls butterflies…](https://www.youtube.com/shorts/V5vzlTChcks)  
   Our version: 5 texts that give her butterflies, and why each one works.
17. **4.8M** · Jimmy on Relationships · [Anxious Avoidant First Date](https://www.youtube.com/shorts/70gMSO1VF_w)  
   Our version: Anxious vs avoidant: why the one who pulls away feels so attractive.
18. **4.8M** · Content Machine · [How girls friendzone guys #shorts](https://www.youtube.com/shorts/NrftJvqx5aw)  
   Our version: 4 signs she's keeping you around, not falling for you.
19. **4.7M** · Victoria Pfeifer · [How to know if a girl likes you 👩🏻‍❤️‍👨🏻](https://www.youtube.com/shorts/jCGJrFVQi6I)  
   Our version: 5 body-language signs she likes you (one most guys read wrong).
20. **4.4M** · Mind Over Shadows · [The Hidden Psychology of Dark Attraction  #psycholgyfacts #d](https://www.youtube.com/shorts/dqIUyqmnBT0)  
   Our version: Dark attraction psychology: 4 effects that make her like you more (Ben Franklin effect…).
21. **4.3M** · Limitless Real Factzz · [Psychology Facts#shorts](https://www.youtube.com/shorts/HWRAoT6q1Ek)  
   Our version: If she stays on your mind for months without talking: the psychology (Zeigarnik effect).
22. **3.8M** · Monika Mancini · [Signs she likes you | How to know if a girl likes you](https://www.youtube.com/shorts/Q_Mm_wgijuI)  
   Our version: A girl's own list: 4 signs she likes you (number 4 is in your phone).
23. **3.7M** · HamzaUniverse · [How To Make A Girl CHASE YOU](https://www.youtube.com/shorts/3IRx6JlOUk4)  
   Our version: Why chasing her pushes her away (the attraction flip).
24. **3.6M** · Daily Facts Worth · [5 Ways On How To Know If A Girl Likes You But Is Hiding It..](https://www.youtube.com/shorts/zfOnYXxE7SA)  
   Our version: 5 signs she likes you but is hiding it (number 3 is her friends).
25. **3.5M** · Iron Man Lifestyle · [Top 5 Signs A Girl Likes You #shorts](https://www.youtube.com/shorts/BTDS0yj9q3Q)  
   Our version: She laughs at your worst joke: 5 signs she likes you.

### Hook patterns that repeat across the winners

1. **Translator or decoder.** "What girls mean when they text…" followed by one line of text and one line of meaning, repeated (25M). Every line is its own small payoff.
2. **Cliff-hanger fact card.** "Girl Fact: A woman is more attracted to a man when……" stays on screen for 6–8 s, then the answer appears (2–6M each, RSH MindTree, SilentFlix, QuickMindFacts). The viewer has to wait for the answer, so the short loops.
3. **Numbered signs with a promise.** "5 signs she likes you but is hiding it…", "4 things girls do when they like you" (2–5M). The "hiding it" or "secretly" angle beats a plain list.
4. **Labelled at the audience.** A tag such as "FOR BOYS", "Boys fact" or "Fellas, here are…" opens the short, telling men it is for them.
5. **A woman tells men the secret.** "Boys, I'm spilling the lady's secrets", or a female coach saying "Things I wish men knew" (2–4.5M). A woman's voice works as insider proof.
6. **The mistake hook.** "If you say this, she's gonna put you in the friend zone", or "NEVER do this around a girl you like." Fear of doing it wrong, then the fix.
7. **A blunt hard truth.** "Women don't ignore men they like" (2.8M in 10 s). One sentence that stings and gets sent to a friend.
8. **A named effect or archetype.** Ben Franklin effect, the uncertainty principle, anxious vs avoidant, "Thomas Shelby's 3 rules", or pupils widening as a sign. A name makes the advice feel like science.
9. **An open loop on the last point.** "Especially the last one" or "the third is my favourite" (Hindi faceless winners, 3–8M) keeps viewers to the end.
10. **Relatable texting artefacts.** A chat screenshot ("She said 'Nice, send it'", 13M) or text bubbles on screen. People read them in 5 s and rewatch.

Formats that win and fit our faceless narration: text-card facts over moody stock video, faceless Hindi voiceover over dark film clips (Peaky Blinders and "aura" edits), and numbered lists. Acted skits and street interviews take the biggest raw numbers, but we can only remix their idea, not their footage.

## Instagram

Updated 2026-10-19. Data: [ig.jsonl](ig.jsonl), 202 outlier posts (149 reels, 53 carousels) out of 1,910 posts scanned. 110 reels have Instagram's own play count of at least 1M, and 9 more pass 1M on an estimate. The top 40 niche reels and top 20 carousels are fully analysed (`analysed: true`): hook, transcript (`transcript_en` = English translation of the Hindi ones), `screen_text` (OCR of the on-screen list for silent text-card reels), concept, structure, visual, why it worked, `fits_us` {ok, reason} and `our_version`. Every row has `added` and `used_by: null`. Videos, 3-frame contact sheets (`<code>_sheet.jpg`) and carousel slides 1–3 (`<code>_s1..3.jpg`) are in `library/research/viral/ig/` (git-ignored).

**How it was built (anonymous only, no login, no cookies, never @thedecodeher).** Instagram shows logged-out visitors three useful things: (1) `instagram.com/popular/<topic>/` pages list each topic's top reels with the real play count; 90 topic pages were crawled and 25 niche ones kept as sources. (2) A profile's public reels tab shows the 12 newest plus pinned reels with play counts, and the profile-timeline web query lists 50–100 posts with likes. (3) A post's public `/embed/` page gives its caption, likes and video. For older reels without a play count, `views_est` = likes × that account's own plays-per-like ratio (`views_estimated: true`). Requests were 5–14 s apart; no rate limit was hit.

**Accounts (21):** femalephilosophy, psychounfold, bookswithswapnil_, bookwises, the1stwealth, moneymindedman, revolverise, psychologyupgrade, earnvalue_, masculinityforge_, brainhex_, successtheory.co, psycheofattraction, jeremy_sarter1x, mindvarta, datingwithgracie, datingbyblaine, lethimchase, manly_pinnacle, thealphamakerx, zoltium, plus the winners from the topic pages (thatgurlera, memestime.in, psychologydepth, anzana_official and others). Instagram hides **zoltium** and **psychounfold** from logged-out visitors, so their profiles return nothing. psychounfold's 35M reel came in through a repost (memestime.in). Many other big pages are hidden the same way, including masculineprint (301K), chadoutlaws, hoe_math, psych2go and sadiapsychology.

**Refill:** `uv run -q --with curl_cffi python tools/viral_bank_ig.py --transcribe` reads [accounts-ig.txt](accounts-ig.txt) (handles plus `topic:` lines). It adds only URLs it has not seen before (30 by default, `--max-new N`) and refreshes counts on rows up to 30 days old. With `--transcribe` it also downloads, transcribes and makes a contact sheet for new reels with at least 1M views. On a rate limit it saves its progress and exits; the next run resumes. `--media-only <codes>` fetches media for chosen rows. A Claude session still has to write the analysis fields for new rows (`analysed: false`).

**Key finding:** the 35M "how to attract any girl" reel (psychounfold, reposted by memestime.in) uses **our exact look**: 2D illustrated clips inside a round lens vignette, one caption word-group at a time, and a male narrator. It is in Hindi, and our format has the same skeleton. The other big pattern is the **5–8 s text-card list** (27M, 26M, 12M, 11M): one numbered list on a texture, no voice, and the caption repeats it ("read caption"). These loop many times, which inflates plays.

### Top 25 remix candidates (not used yet, ranked by views)

1. **35.5M** · @thatgurlera · [6 Eye Contact Techniques you should master to make anyone obsessed wit](https://www.instagram.com/reel/DGGAuUpIh2X/)  
   Our version: 6 eye-contact moves that make her remember you, voiced over our lens clips.
2. **35.3M** · @memestime.in · [If you want to make a strong connection with a girl, ask her these thr](https://www.instagram.com/reel/DIOe3sVPwoB/)  
   Our version: 3 questions that make her feel truly seen (and what to say back).
3. **27.6M** · @psychologydepth · [FEMALE DARK PSYCHOLOGY](https://www.instagram.com/reel/DHHWQi4o8UB/)  
   Our version: What her texts really mean: 5 phrases decoded (narrated, one per scene).
4. **12.7M** · @the1stwealth · [How to make girl regret loosing you](https://www.instagram.com/reel/DOII0Zp2CG8/)  
   Our version: How to make her regret losing you (without saying a word).
5. **12.6M** · @anzana_official · [4 signs you are still a girl, not a woman](https://www.instagram.com/reel/DAzzYRdyCLF/)  
   Our version: 4 signs she's a woman, not a girl (what to look for before you commit).
6. **11.8M** · @olgasafari · [Do not teach a man how to be your man.](https://www.instagram.com/reel/C1KnPSNvslt/)  
   Our version: If she wanted to, she would: the signs she's already choosing you.
7. **11.2M** · @psychologyupgrade · [DARK SIDE OF FEMALE PSYCHOLOGY](https://www.instagram.com/reel/DNlL9atp496/)  
   Our version: Dark side of female psychology: 6 things she'll never say out loud.
8. **10.5M** · @femalephilosophy · [You can find out in three ways that someone likes you.](https://www.instagram.com/reel/DGNnlolAxqe/)  
   Our version: 3 signs she likes you (and why she still might say no).
9. **9.4M** · @stefano.fracchiolla · [Body Language NEVER Lies, Part 26](https://www.instagram.com/reel/DI63MysCzFn/)  
   Our version: Her body language never lies: 5 gestures and what they mean.
10. **9.1M** · @olgasafari · [This is the most spot-on thing I've ever read.](https://www.instagram.com/reel/C0cPnmXvia8/)  
   Our version: Men settle where there's peace: why she stays with one man and leaves another.
11. **8.6M** · @psycheofattraction · [How one professor proved you can make yourself fall out of love in 15 ](https://www.instagram.com/reel/DQx-jafjGvH/)  
   Our version: The 15-minute study that makes people fall in love (36 questions).
12. **8.5M** · @earnvalue_ · [5 Signs She Thinks That You're Handsome.](https://www.instagram.com/reel/C7Vyf8SMVdP/)  
   Our version: 5 signs she thinks you're handsome.
13. **7.8M** · @jasexplains · [Here are the secrets that girls like most](https://www.instagram.com/reel/C56IyBqyaxs/)  
   Our version: What she notices about you that you don't (girl facts).
14. **7.7M** · @drmaxbutterfield · [I can always tell when two people are soulmates.](https://www.instagram.com/reel/DItlufLpWvO/)  
   Our version: 'Soulmate' myths vs the 3 things that actually predict she stays.
15. **5.5M** · @the1stwealth · [Why beautiful girls chase bad boys](https://www.instagram.com/reel/DOXlmX0DNux/)  
   Our version: Why she chases the bad boy (and how to keep the good parts without the bad).
16. **5.4M** · @successtheory.co · [Dark Attraction Psychology (Part 1)](https://www.instagram.com/reel/DLcSqIItV3J/)  
   Our version: Dark attraction psychology: 5 tricks with their real names.
17. **5.3M** · @datingwithgracie · [When a woman looks at you, don't do this.](https://www.instagram.com/reel/C54WQvmM6VO/)  
   Our version: When she looks at you, don't do this.
18. **5.1M (est.)** · @datingbyblaine · [Woman rejects man for his first-date picnic idea in the park](https://www.instagram.com/reel/DaEVN6lP4_5/)  
   Our version: She rejected his picnic date: what it tells you about her.
19. **4.9M** · @datingwithgracie · [Here are six compliments that will make a woman obsess over you.](https://www.instagram.com/reel/C_WuSTFsJYq/)  
   Our version: 6 compliments she'll repeat to her friends.
20. **4.9M** · @factoon.daily_ · [She uses you vs she loves you](https://www.instagram.com/reel/DZlzf-ETxBk/)  
   Our version: She uses you vs she loves you: 6 differences.
21. **4.9M** · @thesabrinazoharshow · [Run if someone says one of these three things in dating.](https://www.instagram.com/reel/DDuQXdEJz9s/)  
   Our version: Run if she says one of these 3 things.
22. **4.7M** · @revolverise · [Weird little habits I stole from attractive people (and never returned](https://www.instagram.com/reel/DRND0NYjFnV/)  
   Our version: Habits I stole from attractive men (her version).
23. **4.6M (est.)** · @datingwithgracie · [There are four things women find unattractive.](https://www.instagram.com/reel/C5zIr0PRtxs/)  
   Our version: 4 things that quietly kill her attraction.
24. **4.6M** · @bookswithswapnil_ · [Girls Psychology](https://www.instagram.com/reel/DVzp7V-DGoj/)  
   Our version: If she does this, it means this: 7 girl-psychology decodes.
25. **4.2M** · @datingwithgracie · [Three non-sexual ways men touch women that send shivers up her spine.](https://www.instagram.com/reel/DeM0RSJAv-c/)  
   Our version: 3 small touches that make her feel safe with you.

Left out on purpose: manly_pinnacle's biggest carousels (50K likes: "12 types of women to avoid", "marrying a woman 30+ is a trap", "h*e era") are degrading rage-bait, and its "sex every day" carousel is sexual (`fits_us.ok: false`). The usable carousel ideas are listed under `type: carousel` with `fits_us.ok: true`: the rescuer trap, signs to walk away, first-date moves, the no-contact rule, playing dumb, and the 24-hour rule.

### Hook patterns that repeat across the winners

1. **"She says X, she means Y" decoding.** "Female dark psychology: when she laughs while apologising…, 'with my friend' vs 'with a friend'…" (27.6M and 26.7M, the same list on two pages). Each line pays off on its own.
2. **A forbidden-knowledge label.** "Dark side of female psychology", "Dark attraction psychology (Part 1)", "Dark signs you're more attractive" (11M, 5M, 3M). The word "dark" sits on harmless, honest tips.
3. **Exact lines to say.** "Ask her these 3 questions… when she answers, say…" (35M), "6 compliments that make her melt" (4.9M), "text like a high value man: instead of X, say Y" (2.8M). The viewer leaves with a script.
4. **A promise of control.** "Make anyone obsessed with you" (35M), "make her regret losing you" (12.7M), "send shivers up her spine" (4.2M).
5. **A negative or warning hook.** "When she looks at you… don't do this" (5.3M), "RUN if she says one of these 3 things" (4.9M), "5 signs a girl is playing you" (4.1M).
6. **Signs lists.** "5 signs she thinks you're handsome" (8.5M), "10 signs your crush secretly likes you" (3M), "4 signs she's flirting and you missed it" (3M). Adding "secretly" or "you missed it" beats a plain list.
7. **A named study or scientist.** Arthur Aron's 36 questions (8.6M and 4.2M), the Ben Franklin effect. A name makes it feel like proof.
8. **A binary contrast.** "She uses you vs she loves you" (4.9M), "girl vs woman" (12.6M), "girls when they like a guy vs not" (3.2M).
9. **A series plus a follow line.** "Part 1 / Part 2" (35M and 7.9M, both by psychounfold), and closing lines such as "we may never meet again, so follow" or "if you're not following, you'll probably never see us again". These are used by most of the faceless winners.
10. **A woman tells men the secret.** datingwithgracie and datingbyblaine (24 outlier reels between them) are female coaches speaking to men. The insider voice works as proof.
