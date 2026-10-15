# Narrator voice analysis: how real narrators in the niche talk

Written 2026-10-14. This file compares The Dark Needle (YouTube), Zoltium (2 reels) and our week-1 v3 scripts. The goal is to work out why our VO sounds "AI-written / bookish" and to write a voice bible for @thedecodeher.

## Sources and method

- **The Dark Needle (DN):** all 135 notes in the vault contain a `## Transcript` section, 349,850 words in total. The 52 transcripts from 2024 to early 2025 are YouTube auto-captions with no punctuation. The 83 from 2025-04-05 onward are punctuated, so the sentence statistics below come from those 83 videos (226,820 words, 19,137 sentences). The word-level statistics (contractions, you, I) cover all 135 videos. I read the openings (about the first 90 seconds) of 19 videos, plus story passages, analogies and endings.
- **Zoltium:** existing faster-whisper transcripts in `scratchpad/zol/v/z1.json` and `z2.json`. z1 is a 49-second psychology reel. z2 is a 36-second product ad.
- **Ours:** `reels/w1-0*-v3/assets/vo/script.json`, 7 reels, 70 lines, 644 words. Real VO durations add up to 231.5 s. I timed the `l*.wav` files.
- Scripts are in `scratchpad/voice/` (corpus.py, sent.py, conn.py).
- **Caveats.** "Fragment" means a sentence of 4 words or fewer. Whisper punctuation tends to merge clauses, so DN's real sentences are probably slightly shorter than shown. DN's words-per-minute figure (about 219) is computed against the full YouTube duration, so treat it as approximate.

---

## 1. Sentence mechanics

| Measure | Dark Needle (83 punctuated videos) | DN openings, first 90 s | Zoltium z1 (psych reel) | Zoltium z2 (ad) | **Ours (7 reels)** |
|---|---|---|---|---|---|
| Mean words per sentence | **11.9** | 13.3 | 12.2 | 6.7 | **5.3** |
| Median words per sentence | **10** | 11 | 10.5 | 7 | **5** |
| Fragments (4 words or fewer) | **16%** | 13% | 10% | 31% | **47%** |
| Contractions per 100 words | 3.9 | 3.3 | 4.1 | 3.5 | **5.3** |
| Contraction rate (contracted vs. "do not" etc.) | 78% | 75% | 83% | 100% | **100%** |
| Questions per minute | 1.25 | 1.4 | 1.1 | 4.9 | **1.0** |
| Questions as share of sentences | 6.8% | 8.7% | 10% | 23% | **3.3%** |
| you/your per 100 words | 6.8 | 6.4 | 13.9 | 3.4 | **6.8** |
| Narrator "I/me/my" per 100 words | **2.2** | **3.0** | 0 | 0 | **0** (all 5 hits are quoted lines) |
| "because" per 1,000 words | **5.3** | n/a | 8.2 (1 in 122) | 0 | **0** |
| "then" per 1,000 words | 2.5 | n/a | n/a | n/a | **10.9** |
| Words per minute | about 219 | n/a | 138 | 143 | 167 (153 to 180) |

Even DN's punchiest, most "scripted" episodes are far less clipped than ours:

| DN video | Mean | Median | Fragments | I per 100 words |
|---|---|---|---|---|
| 2025-10-16 *No Blocking. No Begging.* (his most staccato episode) | 7.6 | 6 | 30% | 1.4 |
| 2025-09-24 *Why Women Get Addicted to Men Who Act Like They're Nothing* | 9.0 | 7 | 24% | 0.7 |
| 2026-10-11 *Why She Wants Your Attention But Not You* | 10.9 | 10 | 18% | 1.2 |
| 2026-07-25 *A Simple Habit That (Sort of) Fixed My Awkwardness* | 12.9 | 12 | 13% | 4.5 |
| 2025-07-30 *She Will Only Love You… If You Dare to 'Break' Her* | 12.7 | 11 | 17% | 2.8 |

**What the numbers say:**
- Contractions and "you" density are **not** our problem. We match or beat DN on both.
- The problem is **rhythm**. Our sentences are half as long, and three times as many of them are fragments.
- We never explain with "because".
- The narrator never says "I".
- Our sentences are chained with "Then." where a person would say "and then", "so" or "but".

---

## 2. Openings: first 2–3 sentences, with hook type

| # | Video | Opening (verbatim) | Hook type |
|---|---|---|---|
| 1 | DN 2024-07-06 *It's actually pretty easy to get girls* | "if you search for how to make a girl like you you'll find some people say you need to have a strong body others say you need money and some say you need to learn seduction but when we look at reality most people who … attract girls don't have any of these things" … "when I was in university like any other guy I tried my best to make girls like me … however all my attempts ended in failure until a friend gave me a book" | Myth-bust, then personal origin story |
| 2 | DN 2024-07-24 *…make a girl addicted to you* | "at the end of this video you will have the addiction weapon any girl you use this weapon on will become addicted to you believe me" | Promise / payoff ("you will have") |
| 3 | DN 2024-08-02 *Ignoring Women…* | "when I started my journey to understand women … I always heard this phrase ignore her and she will chase you I tried to apply this technique but without any results and I began to think it was just empty talk" | First-person failure story |
| 4 | DN 2024-10-23 *Psychopathically Confident* | "in this video I'm going to share a secret with you a secret that will give you extraordinary power so much so that you won't even have time to respond to the girls who admire you" | Secret + exaggerated promise |
| 5 | DN 2024-11-22 *Destroying a Woman's Ego…* | "from the moment a beautiful woman steps out of her house dozens of men try to grab her attention … thanks to social media and dating apps those dozens have turned into hundreds" … "but don't worry my brother today I have the solution for you" | Scene from her side, then a brotherly reassurance |
| 6 | DN 2025-01-08 *You're Not Boring; You Just Lack Mystery* | "there is no greater sin than just being plain boring and predictable when trying to attract beautiful women" … "the problem is that everyone tells you to be mysterious but no one explains how" | Bold claim, then "nobody explains this" |
| 7 | DN 2025-02-02 *…Make ANY Woman Miss You BADLY* | "if she doesn't miss you she will never love you I want you to go back in time with me and remember that man who used to live in the cave" | Hard rule, then "come with me" analogy (caveman) |
| 8 | DN 2025-03-01 *NEVER Be the Nice Guy* | "in this life as a man you have three choices when it comes to women you can either be the nice guy … or you can be the bad boy … or you can be the half bad half nice" | Choice framing (three paths) |
| 9 | DN 2025-04-26 *You're a Smart Man, So Why Do You Struggle* | "So, you are a smart man, but you're struggling with women. It seems like no woman is attracted to you … and you don't understand why." | Call-out of the viewer's situation |
| 10 | DN 2025-05-07 *The Lazy Way to Make a Girl Obsessed* | "I still remember some time ago, I used to know this guy. He was broke, skinny, short, not good-looking, had dropped out of high school … But somehow he was successful with girls." | **Story of a guy he knew** (past tense, specific details) |
| 11 | DN 2025-07-30 *…If You Dare to 'Break' Her* | "Since the day I was born, I've always heard that the female is the gentle sex. My entire life, I have seen her as someone you must treat as if you're dealing with a very fragile being." | Confession: what I used to believe |
| 12 | DN 2025-08-13 *How She Feels When She Realizes She's Lost You* | "If you like a girl and you're afraid of losing her, then congratulations, you will lose her." | Sarcastic paradox ("congratulations") |
| 13 | DN 2025-08-27 *NEVER Text Her Again!* | "Stop scrolling. Your thumb is already hovering over her chat bubble, about to fire off that one last text you swear will fix everything." | Pattern interrupt plus mind-read of the viewer's moment |
| 14 | DN 2025-09-24 *…Men Who Act Like They're Nothing* | "Why do women chase the men who treat them like they're nothing? Strange, right? You'd think the guy who notices her … would be the one who wins." | Question, then "Strange, right?", then expectation flip |
| 15 | DN 2025-10-01 *Give me 12 Minutes…* | "Give me 12 minutes and I will make you dangerously attractive." | Time-boxed promise |
| 16 | DN 2025-10-16 *No Blocking. No Begging.* | "Most men destroy attraction the moment they try to force it. They either block or beg." | "Most men" generalisation |
| 17 | DN 2025-12-20 *Signs a Girl is Attracted to You* | "Most potential soulmates never even meet because men suck at catching signals. Yes, I'm talking to you. You really, truly, utterly suck at it." | Roast / affectionate insult |
| 18 | DN 2026-07-25 *A Simple Habit That (Sort of) Fixed My Awkwardness* | "It doesn't matter how socially awkward you are right now because I was probably more awkward than you. Imagine that I came from a village in a third world country…" | "I was worse than you" credibility story |
| 19 | DN 2026-10-11 *Why She Wants Your Attention But Not You* | "There's a girl you've probably met before, or maybe you already have one in your life who's going to waste a lot of your time without you even realizing it." | "There's a type of girl…" character intro (pays off as his own story at the end) |
| 20 | Zoltium z1 | "Your brain fools you into telling your plans to others, so you don't actually have to achieve them. Sound weird? Believe it or not, your brain doesn't care about your success." | Counterintuitive claim, then "Sound weird?" |
| 21 | Zoltium z2 (ad) | "Want to be the man every woman craves? Tired of getting ghosted, friend-zoned, and overlooked? What if you could rewire your dating life in 90 days?" | Stacked pain-point questions (infomercial) |
| — | **Ours (all 7)** | "It's 1 a.m. She's sending you memes. You're both laughing." / "She's right there. Coffee in her hand. And your mind goes blank." / "First date. An hour in. You've covered work, hometown, and her dog's name." | Present-tense second-person scene, built from fragments, with no voice behind it |

**Patterns:**
- About 9 of the 19 DN openings either bring in the narrator himself ("I", "my", "me") or address the viewer directly ("my brother", "I'm talking to you").
- Every DN opening sounds like **a person talking to you**, even when it opens on a scene.
- Ours sound like **stage directions**: noun-phrase fragments ("Coffee in her hand.", "First date. An hour in.") read like a screenplay, not like a man telling you something.
- Zoltium z1 is the closest model for a reel. It opens with one full, 18-word claim, then a two-word spoken reaction ("Sound weird?").

---

## 3. Storytelling devices

| Device | Dark Needle | Zoltium | Ours |
|---|---|---|---|
| **Named characters** | Almost never (0.01 per 100 words; once, "Charlie might be a better match for you"). He uses **types**: "this guy", "a girl", "a friend gave me a book", "I used to know this guy", "this girl I've been talking about … was a girl I knew when I was 22". | None | None, and only "she / you" |
| **First-person story** | Yes, in about half the openings: university failure, the village-to-abroad move, raising cats, the toxic friend, the girl at 22. 2.2 I/me/my per 100 words overall, 3.0 in openings. | No | **None.** The narrator is a disembodied voice. |
| **Specific details** | "calling her 69 times a day", "She gets hit on maybe 10 times a day … 100 messages from guys she doesn't even know", "Thursday, busy. Friday, can't. Weekend, maybe next week.", "dances for 2 hours", "sitting in a group of 20 people" | "in 90 days" | **This is our strength:** "1 a.m.", "her dog's name", "replies in three seconds", "Hey stranger". Keep it. |
| **Dialogue / acted skits** | Heavy. "she says" 168 times, "he says" 179, "you say" 232, "say something like" 44. Two-sided skits: "guy: hi can I get you a drink / girl: I'm good thanks / guy: speechless". Her **inner monologue**: "gosh he's really pulling out all the stops … when will this night be over", "You're thinking, 'She likes me.' She's thinking, 'This is fun.'" | No | Only reported texts ("Hey stranger", "this week is crazy, sorry") and one line for the viewer to say. **We never voice her thoughts.** |
| **Tense** | Past tense for his own stories ("He was broke, skinny, short"). Present / hypothetical for scenarios ("Imagine a girl who's about to go home with a guy. On the way, he takes her dancing instead."). | Present (general truth) | Present only, second person, every reel |
| **"Imagine / picture this" family** | "imagine" 246 times in 92 of 135 videos; "for example" 264 in 91; "let's say" 52; "imagine with me" 24; "picture this" 9 | No | **0** |
| **Asides** | "note although I'm using the word relationship this can apply to meeting a woman", "Of course, after this video, I'll explain…", "[the book name] if this video reaches 1K likes" | No | 0 |
| **Humour / attitude** | Roasts ("You really, truly, utterly suck at it"), sarcasm ("then congratulations, you will lose her"), absurd lines ("my mom warned me about Angry Birds"), "nonsense" 22 times, "stupid" 74 times ("don't be stupid") | No | 0. Tone is uniformly calm and wise. |
| **Brotherly address** | "my friend" 62, "my brother" 13, "my dear brother" 15, "please" 235, "listen to me" 111, "focus with me" 20, "trust me" 39 | "Now listen carefully" | 0 |
| **Filler / spoken connectors** | "you see", "so", "now", "and", "but", "you know what", "right?", "make sense?", "Yes, I'm talking to you" | "Believe it or not", "Sound weird?" | Almost none. "Then" used as a sentence starter. |
| **Rhetorical questions** | 6.8% of sentences, often answered immediately: "Why? Because…" ("why?" 68 times), "How did I do it? That is the subject of today's video." | "Sound weird?" | 4 in 70 lines ("So why would she need the date?") |
| **Callbacks** | Yes. 2026-10-11 opens with "There's a girl…" and ends "this girl I've been talking about … was a girl I knew when I was 22 … So, please don't be like me." Series callbacks ("as I always tell you in the series"). | No | Line 9 echoes the title. That's a slogan, not a callback. |

---

## 4. How DN explains a psychological point without sounding like a textbook

1. **"Why? Because…" in the same breath.** "Most famous women who are considered attractive are beautiful. Why? Because simply a woman's beauty lies in her looks while a man's beauty lies in other things." He asks the question a viewer would ask and answers it out loud. Ours state the conclusion with no "because" (0 in 644 words).
2. **"You vs. her" perspective swap.** "You, as a man, when a girl gives you attention, it's a big event. A girl smiled at you today, you'll remember it for the whole week. But for an attractive girl, it's the opposite. She gets hit on maybe 10 times a day."
3. **Everyday analogy in plain words.**
   - "It's like talking to a receptionist at a hotel. She'll laugh at your jokes, nod at your stories … but you don't feel anything behind it."
   - "It's like taking a painkiller. Not to heal the wound, but just to stop the hurt."
   - The chicken / tomato soup restaurant story.
   - "Think about magnets. Push too hard and they repel."
4. **A mini-scenario with a twist.** "Imagine a girl who's about to go home with a guy. On the way, he takes her dancing instead. She dances for 2 hours … After that, she doesn't feel the need to go home with him anymore."
5. **Voice her head.** "she'll think to herself isn't this guy strong and calm why is he dancing who is this person really". The psychology is shown as her thoughts, not named as a mechanism.
6. **"Here's what's actually happening" signposts.** "And this is the part most guys don't understand." "And now listen to this because this is the most important thing in the whole video." "Here's the twist." "That's the loop." He flags the insight and then says it in plain words.
7. **Pre-empting the objection.** "And now you will tell me but I'm not needy. Yes my friend you almost certainly are." "Now you're going to ask me, okay, if she's tired of attention, why does she still talk to me? Because she likes it."
8. **Plain-language science, said casually.** "we still have the same brain as the caveman"; Zoltium: "your brain releases the same chemicals as when you have already achieved them. Your brain can't tell the difference…"

Ours does the opposite. We compress the mechanism into an abstract maxim: "When she knows exactly how you feel, there's nothing left to wonder about. And wondering is what keeps you on her mind." "Closeness comes from questions that go one level deeper." "A line sounds rehearsed. And rehearsed feels like a performance." These are written sentences. Nobody says "closeness comes from" out loud to a friend.

---

## 5. How they end

- **DN signature sign-off** (98 of 135 videos): "This was the Dark Needle. I love you and I'll see you in the next video." "I love you" appears in 69 videos, often as "if you're still watching up to this point, I just want to say I love you."
- **Callback / confession punchline:** "this girl … was a girl I knew when I was 22 years old. and I lost a year of my life because of her. So, please don't be like me." (2026-10-11)
- **Parallel-line crescendo** (in his more scripted episodes): "The man who doesn't chase becomes the one she chases … And the man who acts like nothing becomes everything she can't stop thinking about." (2025-09-24)
- **Personal challenge:** "Try it once … Then come back and tell me. I want to hear how it feels in your skin." (2025-10-16)
- **Engagement ask:** "if you have any questions … let me know in the comments" ("comment" appears 129 times in 71 videos). Plus an ebook / free course plug.
- **Zoltium z1:** "Now listen carefully, you may not see us again. Join Zoltium and learn to become powerful." This is a mild threat / scarcity CTA. z2: "Get the power code now. Link in bio."
- **Ours:** a 2–3-word maxim ("Busy is an answer.", "Be missable.", "Depth beats charm.", "Simple wins.", "Hold her gaze.") followed by "Send this to the guy who… And follow for more." All 7 reels end identically.

---

## 6. Side by side: exactly why ours sound bookish

1. **Too clipped.** Mean 5.3 / median 5 words per sentence, against DN's 11.9 / 10 and Zoltium z1's 12.2 / 10.5. **47% of our sentences are fragments**, against DN's 16%. Even DN's most staccato episode is 30%. A wall of fragments reads as ad copy or a poem, not speech.
2. **Every reel uses the same template.** Present-tense scene, then the misread, then "But / Here's what nobody tells you", then a principle, then an instruction, then a slogan, then "Send this to the guy who… And follow for more." Seven out of seven. Identical scaffolding is an AI tell.
3. **Every reel has a slogan line.** Line 9 is always an aphorism: "Busy is an answer." "Let her wonder." "Simple wins." "She already did her part." "Be missable." "Depth beats charm." "Hold her gaze." DN almost never does this. His closers are personal ("please don't be like me").
4. **Abstract-noun maxims instead of explanation.** "Closeness comes from questions that go one level deeper." "Eye contact says something words can't." "Rehearsed feels like a performance." "Wondering is what keeps you on her mind." "Depth beats charm." "Simple wins." Abstract nouns become sentence subjects. That's essay grammar.
5. **Zero "because"** in 644 words (DN: about 5 per 1,000), so the reasoning is asserted, never talked through. There's no "Why? Because…" move either.
6. **Fragment triplets** (the rule-of-three tic): "The laughs. The attention. The late-night talks." "The gym. Your friends. Your plans." "A real day. A real place." "Count to two. Smile. Then look away slowly." "Good morning. Good night." There's one per reel, which is a classic LLM cadence.
7. **No narrator.** 0 first-person lines from the narrator. Every "I" is inside quotes ("What did I say wrong?", "I'd regret it if I didn't say hi", "I see you"). DN uses I/me/my about once every 45 words and tells his own failures.
8. **No characters beyond "you" and "she".** There's no "this guy I knew", "my friend", or "a girl I dated". DN doesn't use names much either. He uses **types** plus a personal link.
9. **No two-sided dialogue and no inner monologue.** We report texts, but we never act out a short exchange and never voice what she's thinking. DN does both constantly.
10. **No attitude.** There's no sarcasm, no roast, no "nonsense", no "my brother", no "listen". Everything is delivered in the same calm, wise register, and calm-wise-everywhere is the AI default.
11. **"Then." as a sentence opener** (10.9 per 1,000, against DN's 2.5): "Then she went quiet." "Then the follow up." "Then look away slowly." Real speech glues these together: "and then she just… went quiet."
12. **Signposts lifted from AI copy:** "Here's what nobody tells you." (DN's real versions are clunkier and more personal: "And this is the part most guys don't understand", "Now listen to this because…")
13. **What we already do right:** contractions (100%), "you" density (6.8, same as DN), concrete detail ("1 a.m.", "her dog's name", "Hey stranger", "replies in three seconds"), and a short spoken CTA. Keep all of these.

---

## 7. Voice bible for the @thedecodeher narrator

### 15 do's and don'ts

1. **DO** let the narrator be a person: at least one "I / me / my" line per reel ("I did this for two years", "a guy I used to work with", "I learned this the hard way"). DN: 2.2 per 100 words.
2. **DO** aim for a median of about 9–11 words per sentence, with fragments under 20% of sentences. Long sentence, long sentence, short punch. Not five punches in a row.
3. **DO** explain with "because" and "Why? Because…" at least once per reel.
4. **DO** introduce people as types tied to the narrator: "this guy I knew", "my buddy", "a girl I was talking to back in college". Avoid fake names like "Jake" (DN almost never uses names). A type plus a personal link sounds real.
5. **DO** act out a two-line exchange, or **voice her thoughts**: "You're thinking, she likes me. She's thinking, this is fun."
6. **DO** use one everyday analogy per reel (receptionist, painkiller, soup, magnets). Make it concrete and casual, never "a metaphor for".
7. **DO** pre-empt the viewer's objection: "Now you're gonna say, but I'm not needy. Yeah… you are."
8. **DO** allow one moment of attitude per reel: sarcasm ("congratulations, you'll lose her"), a light roast ("you really suck at this"), or "that's nonsense".
9. **DO** glue clauses with "and", "but", "so", "and then", "because" instead of full stops.
10. **DO** keep concrete details (times, exact texts, numbers). It's our one real strength.
11. **DON'T** end on a 2–3-word slogan ("Simple wins.", "Be missable."). End on a personal line, a callback to the opening, or a plain instruction, then the CTA.
12. **DON'T** use the same structure two reels in a row. Rotate openings: confession, call-out, "there's a girl who…", myth-bust, sarcastic paradox, scene.
13. **DON'T** make abstract nouns the subject of a sentence ("Closeness comes from…", "Depth beats…", "Eye contact says…"). Put a person in the subject slot: "She'll feel closer when you…"
14. **DON'T** use fragment triplets ("The X. The Y. The Z."). At most one list per reel, and say it as a list: "the gym, your boys, your own plans".
15. **DON'T** open with a stage-direction fragment ("First date. An hour in."). If you open on a scene, say it like a guy telling it: "So you're on a first date, right, an hour in, and you've already covered work, where she grew up, her dog's name…"

### 30 phrases and sentence starters a real guy uses
(From DN and Zoltium transcripts, lightly normalised.)

1. "I still remember…"
2. "I used to know this guy…"
3. "When I was in college…"
4. "I learned this the hard way."
5. "I was probably worse than you."
6. "There's a girl you've probably met before…"
7. "So you like this girl, right?"
8. "Yes, I'm talking to you."
9. "Listen to me carefully."
10. "Now listen to this, because this is the important part."
11. "And this is the part most guys don't get."
12. "Here's the twist."
13. "Why? Because…"
14. "Strange, right?"
15. "Sound weird?"
16. "Believe it or not…"
17. "You'd think … but no."
18. "Now you're gonna ask me…"
19. "Let me give you an example."
20. "Imagine a girl who…"
21. "Picture this."
22. "Let's say she texts you…"
23. "It's like…"
24. "You're thinking … She's thinking…"
25. "She'll say something like…"
26. "Trust me."
27. "That's nonsense."
28. "Then congratulations, you'll…"
29. "Try it once. Then come back and tell me."
30. "So please, don't be like me."

### 20 phrases to ban

1. "Here's what nobody tells you."
2. "Simple wins." / "Depth beats charm." (any "[noun] beats [noun]" or "[adj] wins" slogan)
3. "Be [adjective]-able." ("Be missable.")
4. "X is an answer." / "X is a signal." (abstract-equation maxims)
5. "Closeness comes from…" / "Attraction comes from…"
6. "[Abstract noun] says something words can't."
7. "The laughs. The attention. The late-night talks." (fragment triplets)
8. "A real day. A real place." (paired echo fragments)
9. "That's her opening the door." (stock metaphor stated as fact)
10. "It never comes." (dramatic fragment closer)
11. "And that changes everything."
12. "Let that sink in."
13. "Here's the truth:" / "The truth is simple."
14. "Not X. Y." used as a standalone reveal ("Not what do you do. What are you excited about?")
15. "In a world where…"
16. "Unlock / unleash / elevate / navigate / journey."
17. "It's not about X, it's about Y." (allowed at most once a month)
18. "The secret?" / "The answer?" (one-word question setups)
19. "Science says…" / "Studies show…" without saying what was found
20. "Then." as a sentence opener (use "and then" inside a sentence)

---

## 8. Caution: DN is not a pure model

From mid-2025 some DN episodes (2025-08-27, 2025-09-24, 2025-10-16) switch to a polished, staccato style: "Attention is cheap. Indifference is rare." "Here's the twist." "That's the paradox." These are his own AI-flavoured scripts, and they show the same tells we have, only milder.

His native voice is in 2024–mid-2025 and 2026: long, run-on, brotherly, first person, sarcastic, slightly non-native ("Focus with me", "my dear brother"). Copy that register, not his slogan episodes.

Zoltium z2 is an ad. Copy z1's rhythm instead: a full claim, then "Sound weird?", then a plain-words mechanism, then a scarcity CTA.
