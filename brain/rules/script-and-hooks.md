# VIEWS RULES (owner approved 10-15 — these win over anything older below)
Why: reels stall at ~120-130 views = they fail Instagram's first test group. Full evidence: [[growth/views-diagnosis-2026-10-15]].
1. **Line 1 = her behaviour + a verdict, ≤ 10 words, topic clear by 1.0 s.** e.g. "If she replies in four hours, she's not busy."
   No filler line 2 ("Yeah. I did that too." / "Bro, this used to drive me crazy."): the confession, if any, moves to line 3.
2. **Searchable topic.** At least 2 of every 3 reels come from the search bank below; self-respect is the ANSWER inside the reel, not the topic.
   Search bank: signs she likes you · how to know if she's interested · signs a girl likes you but hides it · mixed signals · hot and cold ·
   why she stopped texting · she left me on read · dry texter · how to text a girl · what to text her · texting her first ·
   why she pulled away · signs she's losing interest · how to ask her out · first date tips for men · friend zone ·
   how to keep her interested · what women find attractive · body language signs she likes you · she says she's busy.
3. **Title card** (reel.json `titleCard`): 3-7 words, a search phrase in plain caps ("SIGNS SHE'S LOSING INTEREST"), on screen 0-2 s
   at the top and used as the cover (thumbMs 600). Written with the script; the plan step fills it if missing.
4. **One reason to send or comment, every reel** (last 5 s, before "follow for more"), rotating: a useful send ("Send this to your boy who
   keeps asking what her text means.") or a comment prompt ("Comment the text she sent, I'll decode it."). Never mocking.
5. **Caption** (queue_reel.sh builds it from reel.json `caption`): line 1 = a search phrase as a plain sentence + the verdict ·
   line 2 = his exact situation · the send/comment prompt · "Follow @thedecodeher for more dating advice for men." ·
   hashtags: `#datingadviceformen #datingtips` + exactly 2 topic tags (#mixedsignals #textingtips #signsshelikesyou #femalepsychology
   #friendzone #firstdate #howtotextagirl #datingadvice). **Never more than 5 hashtags** (Instagram cap since 2025-12-18).
6. Still banned: "Here's what…", "Here's the thing", "Here's why" (every week-2 script had one).

# Script & hooks (strict) — relatable stories, not a facts channel

Owner, 10-13: "these reels should be relatable, not like some facts channel… 'according to this study' is not needed…
every reel should explain a real-life relatable scenario… they should watch the full reel, like, save and follow."
Evidence: [[research/relatable-storytelling]], [[research/darkneedle-visual-grammar]].

## The rules
1. **One real moment per reel** the viewer has lived (the 2 a.m. "haha", the "I'm busy this week", the girl who looks twice).
2. **Hook in the first 1–2 s**: drop him into that moment in second person, with a concrete detail (time, app, words on the
   screen). No intro, no name, no "did you know". The picture shows the same moment at the same time.
3. **Open a loop by second 3–5** ("…and that's exactly where you lose her.") and close it in the last fifth.
4. **Name his inner excuse / feeling** ("you tell yourself she's just busy").
5. **Dialogue**: at least two short lines of real-sounding text/speech (notifs or speech text) — that's what makes it real.
   The narrator never speaks a character's line as his own: attribute it ("She says, …", "She texts you, …", "Just say, …").
6. **Show the turn** (the moment it goes wrong) with the cast; narrate only what it means.
7. **The mechanism in plain words**, like a friend who's been there — **never** "studies show / researchers found / in 1986…".
   Stay honest: if it comes from research, say it as plain truth, narrowly ("people want what they might lose"), never absolute.
8. **One move he can copy** (a line to say, a thing to stop doing) — that's what earns the save.
9. **Payoff line** that calls back to the hook (punch words at the end), and could loop into the first line.
10. **Every reel ENDS ON A SPOKEN CTA** (owner, 10-13 — non-negotiable): the last voice line names a person or a moment
    and asks to follow, e.g. "Send this to the guy who … And follow for more." / "Save this for … And follow for more."
    It is the last line of script.json (reel.json `ctaLine`), built on screen like any line, after the punch clears.
    (We noted one vendor study linking follow prompts to lower reach; the owner chose the explicit CTA.)
11. 30–40 s, 9–11 lines, short sentences, no word a 17-year-old wouldn't say.
12. The viewer's blind spot is the subject — never mock the girl, never lecture from above.

## Template
HOOK (0–3 s) → SCENE (two details) → TENSION (excuse + one line of dialogue) → TURN (what goes wrong) →
WHAT'S REALLY HAPPENING (one plain claim) → THE MOVE (one line/action) → PAYOFF (callback, punch words) → SPOKEN CTA line ("Send this to … And follow for more.").

## Captions (Instagram post text)
Caption shape: a keyword-rich first line (search reads captions; Mosseri: hashtags don't add reach) · 1–2 lines that name the
situation · the CTA sentence · 3–5 hashtags (Instagram caps posts at 5 from 2026). No "voice is AI-generated" line in the caption:
the relay sends `is_ai_generated=true` on every post. That flag can't be read back, so check the app's "AI info" label after posting.

## Variety across a batch (owner, 10-13: "every reel looks like a template, it looks automated")
- Before writing scripts, fill a variety ledger for the whole batch. Give every reel its own row:
  CTA type | hook style | story shape | signature visual | punch format
- No two consecutive reels share a CTA type, story shape or signature visual.
- CTA types to rotate (the spoken CTA still always includes "follow for more", see [[cta-rule]]):
  - save ("save this for your next date")
  - comment-keyword ("comment PART 2")
  - poll ("which one are you, 1 or 2?")
  - series ("part 2 tomorrow", only when it exists)
  - share ("send this to…"): at most once per week
- Never promise a guide, DM or freebie we don't actually have.
- Story shapes to rotate:
  - chat-only (a phone screen tells it)
  - two-person scene
  - before/after split
  - countdown list
  - "his move vs her read" side by side
  - single object (one text, one moment)
  - flash-forward to the consequence
- Punch formats to rotate: a single word, a short line, a number, a question back to the viewer.

## SPOKEN VOICE v2 (owner, 10-14: "the English feels bookish and AI-generated, not a guy telling a story")
Research: [[research/reel-storytelling-craft]] and [[research/narrator-voice-analysis]] (measured on 135 Dark Needle transcripts and Zoltium).
- **Dinner test:** every line is something a guy would say to his friend about one specific girl on one specific night.
- **Rhythm:**
  - Median 9–11 words per sentence, joined with and / but / so / because.
  - Under 20 % fragments. A fragment is a deliberate punch ("Crazy."), never a list of three.
  - The old scripts averaged 5.3 words, with 47 % fragments. That is what sounded robotic.
- **A narrator, not a voice from nowhere:** at least one first-person line per reel ("I've been that guy", "a guy I knew…").
- **Reason out loud:** at least one "because" per reel, plus one everyday analogy or her side said aloud ("she's thinking…").
- **The subject is a person doing something,** never an abstract noun (no "closeness comes from…", "attraction is…").
- **Specifics:** one exact time, one object, one quoted text per reel.
- **Attitude:** one moment of it (a light roast or sarcasm), and get ahead of the viewer's objection once ("now you're gonna say…").
- **Banned:**
  - slogan endings ("Busy is an answer", "X beats Y") and "It's not X, it's Y"
  - fragment triplets ("The laughs. The attention. The talks.")
  - "Here's the thing" / "Here's what nobody tells you" / "Did you know" / "Let me tell you" / "Stop scrolling"
  - em dashes, and the words truly, genuinely, navigate, delve
- **Ending:** a call-back to the hook or a personal line, then the CTA with "follow for more". Never a moral.
- **Hooks (rotate, never the same type twice in a row):** mid-scene ("It's one a.m. and she…"), confession ("I told a girl…"),
  call-out ("If your mind goes blank when…"), diagnosis ("You're missing girls who… because…"), specific numbers ("Thirty days."),
  POV, contrarian ("Everyone says… But get this…"), concrete rule.
- **For the TTS:**
  - Spell out numbers and times.
  - At most 2 ellipses per reel, and no all-caps.
  - At most 2 casual words ("look", "man", "honestly") per reel, never in the first 2 s.
