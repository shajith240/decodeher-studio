# Week 3 scripts, v3 format (draft for owner approval, 2026-10-15)

Format: [[growth/growth-plan-2026-10-15]] "v3 format" + VIEWS RULES in [[rules/script-and-hooks]]. Two numbered series for follow-intent:
**Decode her text #1–#5** (her exact message, what it means, what to reply) and **Signs she likes you #1–#5**. Post them alternating (01, 02, 03 …) in the evening v3 slot.
Topics are new: none repeats week 1 or week 2 (jealousy, busy, good-morning texts, compliments, mixed signals, boring, eye contact at the bar, etc.).

**Pipeline notes (read before running `tools/new_reels.py`)**
- Every script ends with `Follow for more.` ONLY because `new_reels.py` refuses a section without it (line 24). It is a **placeholder, not spoken copy**.
  It must become the tagline from `config.json` (`reels.tagline`, "Decode her… before she decodes you.") before voicing, the way `tools/remake_reel.py` swaps it.
  Simplest fix: make `new_reels.py` write `reels.tagline` as the last line. Until then, run `remake_reel.py` logic on each new reel before the voice step. Word counts below exclude it.
- Meta blocks sit under their own `## NN meta` heading so the parser's section regex stops before them (it would otherwise voice the comment). They don't match `## NN · …` so no reel is made from them.
- Numbers are spelled out, at most 2 ellipses per reel, no em dashes, no "Here's …", every quoted line is attributed ("She texts", "Just say", "Text her").
- TTS watch-outs: "haha" (01) may come out as a laugh; check the take. "café" (08) keep the accent or write "cafe" if the voice stumbles.

## Summary (computed by script, not estimated: whitespace words, 175 wpm = 2.92 words/s)
| NN | Series | Title | Words | Est. s @175 wpm | Hook line (line 1) | Send / comment prompt |
|---|---|---|---|---|---|---|
| 01 | Decode her text #1 | Haha | 72 | 24.7 | She texts, "haha." That chat is dying. | Comment her last text, and I'll decode it. (comment) |
| 02 | Signs she likes you #1 | Asking for a friend | 70 | 24.0 | "Are you seeing anyone?" That's not small talk. | Send this to your friend who overshares. (send) |
| 03 | Decode her text #2 | Believe her | 74 | 25.4 | "I'm not looking for anything serious." Believe her. | Screenshot that for the next time she says… (save) |
| 04 | Signs she likes you #2 | How's Bruno | 73 | 25.0 | She remembered your dog's name. That's a sign. | Comment the smallest thing a girl remembered about you. (comment) |
| 05 | Decode her text #3 | Three hours | 71 | 24.3 | Three hours, then "sorry, just saw this." That's fine. | Send this to the guy timing her replies right now. (send) |
| 06 | Signs she likes you #3 | Best audience | 72 | 24.7 | She laughs at your worst jokes. That's a sign. | Comment one if she laughs at everyone, two if it's only you… (comment) |
| 07 | Decode her text #4 | So sweet | 74 | 25.4 | She texts, "you're so sweet." That's not a yes. | Screenshot this for the next time she calls you sweet. (save) |
| 08 | Signs she likes you #4 | Seen by her | 72 | 24.7 | She watches every story but never texts. That's curiosity. | Send this to the friend who reads story views like stock charts. (send) |
| 09 | Decode her text #5 | Sometime | 71 | 24.3 | "We should hang out sometime." That's not a plan. | Drop her vaguest text below. I'll tell you what it means. (comment) |
| 10 | Signs she likes you #5 | Count the signs | 75 | 25.7 | She touched your arm twice. That's not nothing. | Save this for the next time she touches your arm. (save) |

| NN | Her behaviour out by | Line 1 ends | Re-hook starts | WHY starts | Move starts | Prompt starts | Lines | All checks |
|---|---|---|---|---|---|---|---|---|
| 01 | 1.0 s | 2.4 s | 7.9 s | 11.0 s | 15.8 s | 20.2 s | 8 | pass |
| 02 | 1.4 s | 2.7 s | 8.6 s | 11.0 s | 15.8 s | 19.9 s | 8 | pass |
| 03 | 2.1 s | 2.7 s | 8.6 s | 11.3 s | 15.4 s | 22.6 s | 7 | pass |
| 04 | 1.7 s | 2.7 s | 8.2 s | 11.3 s | 16.5 s | 20.2 s | 8 | pass |
| 05 | 2.4 s | 3.1 s | 9.3 s | 11.7 s | 16.8 s | 20.9 s | 7 | pass |
| 06 | 2.1 s | 3.1 s | 8.6 s | 11.0 s | 16.5 s | 20.6 s | 7 | pass |
| 07 | 1.7 s | 3.1 s | 9.3 s | 12.3 s | 17.1 s | 21.9 s | 7 | pass |
| 08 | 2.4 s | 3.1 s | 8.6 s | 11.7 s | 16.1 s | 20.6 s | 7 | pass |
| 09 | 1.7 s | 3.1 s | 9.3 s | 12.0 s | 16.1 s | 20.6 s | 7 | pass |
| 10 | 1.7 s | 2.7 s | 9.3 s | 12.0 s | 17.5 s | 22.3 s | 7 | pass |

Checks run on every script (all pass): 55–75 spoken words · line 1 ≤ 10 words, her words/behaviour first, no "I used to…"/confession opener ·
re-hook line starts 7.5–10.5 s · WHY line starts ≤ 13 s · the move (a quoted line he can text/say) starts ≤ 18.5 s · exactly one spoken send/comment/save prompt ·
prompt type never the same twice in a row (comment, send, save, comment, send, comment, save, send, comment, save) · at least one "because" · a first-person line ·
no banned phrases (here's what/the/why, let that sink in, truly, genuinely, navigate, delve, did you know, stop scrolling, follow for more in spoken text) ·
no digits/em dashes · ≤ 2 ellipses · brand line not in the script · last line loops back into line 1 (or the prompt itself does: 05, 07, 08, 09, 10).

Not met (by design limits): line 1 *finishes* at 2.4–3.1 s, not 1.8 s. A ≤ 10-word line can't be spoken in 1.8 s at our pace (that's ~5 words).
Her words/behaviour are out by 1.0–2.4 s, and the title card + chat bubble carry the topic on screen from frame one.

## Variety ledger
| NN | Series | Hook style | Story shape | Prompt type | Loop |
|---|---|---|---|---|---|
| 01 | Text #1 | quoted text + verdict | chat-only | comment her text | "the next time…" → "She texts" |
| 02 | Signs #1 | quoted question + verdict | single object (one question) | send | "she only asks once…" → the question |
| 03 | Text #2 | quoted text + instruction | flash-forward (months of waiting) | screenshot | "next time she says…" → her line |
| 04 | Signs #2 | behaviour + verdict | single object (one detail) | comment (story) | "starts this small…" → "She remembered" |
| 05 | Text #3 | number + quote | his move vs her read (the clock vs the text) | send | "timing her replies" → "Three hours" |
| 06 | Signs #3 | behaviour + verdict, light roast | two-person scene | comment poll (1 or 2) | "only you…" → "She laughs" |
| 07 | Text #4 | quoted text + verdict | chat-only | screenshot | "calls you sweet" → "you're so sweet" |
| 08 | Signs #4 | behaviour + verdict | single object (viewer list) | send | "story views" → "every story" |
| 09 | Text #5 | quoted text + verdict | chat-only | comment her text | "what it means" → her line |
| 10 | Signs #5 | behaviour + count | countdown (count the signs) | save | "touches your arm" → "touched your arm" |

Promises we must keep: 01 and 09 promise to decode texts people comment. Someone has to answer those comments within a day.

---
## 01 · Decode her text #1 · "Haha"
She texts, "haha." That chat is dying.
And one more meme finishes it off.
I sent three memes once and got three hahas.
But she's not cold. Look at what you sent.
"Haha" means you gave her nothing to answer, because a joke isn't a question.
So bring back something she told you, "Wait, how did the interview go?"
Comment her last text, and I'll decode it.
Follow for more.

## 01 meta
<!-- meta: series=Decode her text #1, titleCard="When she texts 'haha'", bubble="haha",
caption hook="When she texts 'haha', the chat is dying. It's fixable.",
caption body="You sent a meme, she sent 'haha', and now you're staring at the screen. 'Haha' means you gave her nothing to answer.",
caption prompt="Comment her last text and I'll decode it.",
caption tags="#datingadviceformen #datingtips #textingtips #howtotextagirl" -->

## 02 · Signs she likes you #1 · "Asking for a friend"
"Are you seeing anyone?" That's not small talk.
Most guys answer way too seriously.
I told one girl my whole dating history. She got bored.
But it was never about your past.
She's checking if you're free, because nobody wants to fall for a taken guy.
So keep it light. Just say, "No. Why, asking for a friend?"
Send this to your friend who overshares.
Follow for more.

## 02 meta
<!-- meta: series=Signs she likes you #1, titleCard="She asks if you're single", bubble="wait are you seeing anyone rn?",
caption hook="She asks if you're seeing anyone? That's a sign she likes you, not small talk.",
caption body="She's checking if you're free before she lets herself like you more. Keep the answer short and flip it back.",
caption prompt="Send this to the guy who answered with his life story.",
caption tags="#datingadviceformen #datingtips #signsshelikesyou #femalepsychology" -->

## 03 · Decode her text #2 · "Believe her"
"I'm not looking for anything serious." Believe her.
Most guys hear "not yet" and wait.
I did that for five whole months with one girl.
But she didn't trick you. She warned you.
She said it early because she didn't want to lead you on.
If you want the same, cool. If not, say it once, "Respect that. I want something real, so I'll step back."
Screenshot that for the next time she says…
Follow for more.

## 03 meta
<!-- meta: series=Decode her text #2, titleCard="Not looking for anything serious", bubble="I'm not looking for anything serious rn",
caption hook="When she says 'I'm not looking for anything serious', believe her.",
caption body="She told you early so she wouldn't lead you on. If you want the same, great. If you want something real, say it once and step back.",
caption prompt="Screenshot the line for when you need it.",
caption tags="#datingadviceformen #datingtips #mixedsignals #femalepsychology" -->

## 04 · Signs she likes you #2 · "How's Bruno"
She remembered your dog's name. That's a sign.
Most guys miss it. I did.
You mentioned him once. Weeks later she texts, "How's Bruno?"
But out of everything you told her, why that?
She kept it because you were on her mind. Not proof, but a real sign.
Just say, "You remembered Bruno? He wants to meet you. Sunday?"
Comment the smallest thing a girl remembered about you.
It always starts this small…
Follow for more.

## 04 meta
<!-- meta: series=Signs she likes you #2, titleCard="She remembers small details", bubble="omg how's Bruno doing??",
caption hook="She remembers small details about you? That's one of the quiet signs she likes you.",
caption body="You mentioned it once, weeks ago, and she brought it back. Notice it out loud and turn it into a plan.",
caption prompt="Comment the smallest thing a girl ever remembered about you.",
caption tags="#datingadviceformen #datingtips #signsshelikesyou #femalepsychology" -->

## 05 · Decode her text #3 · "Three hours"
Three hours, then "sorry, just saw this." That's fine.
Making her wait back is what kills it.
I played that game once. It died in a week.
So forget the clock. Read her text.
If she asked you something, she wants more, because interested people leave a door open.
Reply like the wait never happened, "No stress. So, did you go?"
Send this to the guy timing her replies right now.
Follow for more.

## 05 meta
<!-- meta: series=Decode her text #3, titleCard="She replies after three hours", bubble="sorry just saw this",
caption hook="She replies after 3 hours? The delay matters less than what she wrote.",
caption body="A late reply with a question in it means she wants to keep talking. Don't punish the wait, just answer like normal.",
caption prompt="Send this to the guy who's timing her replies right now.",
caption tags="#datingadviceformen #datingtips #textingtips #mixedsignals" -->

## 06 · Signs she likes you #3 · "Best audience"
She laughs at your worst jokes. That's a sign.
And you think you're just funny tonight.
I've had a girl crying over my worst joke.
But watch what she does right after.
If she leans in after, she's enjoying you, because people laugh more around someone they like.
Don't explain the joke. Just say, "Okay, you're officially my best audience."
Comment one if she laughs at everyone, two if it's only you…
Follow for more.

## 06 meta
<!-- meta: series=Signs she likes you #3, titleCard="She laughs at your jokes", bubble="stop that was SO bad lmao",
caption hook="She laughs at your worst jokes? Watch what she does right after. That's the real sign.",
caption body="A laugh plus leaning in means she's enjoying you, not the joke. Don't explain it, just enjoy it back.",
caption prompt="Comment 1 if she laughs at everyone, 2 if it's only you.",
caption tags="#datingadviceformen #datingtips #signsshelikesyou #femalepsychology" -->

## 07 · Decode her text #4 · "So sweet"
She texts, "you're so sweet." That's not a yes.
Get sweeter and you're heading for the friend zone.
I got that after pouring my heart out once.
So is she into you? Look at what's missing.
There's no question and no plan, because she's being kind, not inviting you closer.
So skip the sweet stuff. Text her, "Glad it made you smile. Coffee Saturday?"
Screenshot this for the next time she calls you sweet.
Follow for more.

## 07 meta
<!-- meta: series=Decode her text #4, titleCard="She says you're so sweet", bubble="aww you're so sweet",
caption hook="When she texts 'you're so sweet', it's kind. It isn't a yes yet.",
caption body="No question, no plan. Getting sweeter walks you into the friend zone. Give her a plan instead.",
caption prompt="Screenshot this for the next time she calls you sweet.",
caption tags="#datingadviceformen #datingtips #friendzone #textingtips" -->

## 08 · Signs she likes you #4 · "Seen by her"
She watches every story but never texts. That's curiosity.
And curiosity isn't a crush yet.
I've checked my viewers at two a.m. for one name.
But you can turn that view into a chat.
Watching costs her nothing, because a view is one tap and zero risk.
So reply to her story, "Wait, where's that café? I need to go."
Send this to the friend who reads story views like stock charts.
Follow for more.

## 08 meta
<!-- meta: series=Signs she likes you #4, titleCard="She watches all your stories", bubble="Seen by Maya",
caption hook="She watches all your stories but doesn't text? That's curiosity, not a crush yet.",
caption body="A view costs her one tap. Turn it into a real chat by replying to HER story with something specific.",
caption prompt="Send this to the friend who checks his story viewers every night.",
caption tags="#datingadviceformen #datingtips #signsshelikesyou #mixedsignals" -->

## 09 · Decode her text #5 · "Sometime"
"We should hang out sometime." That's not a plan.
Reply "yeah for sure," and it never becomes one.
I let that text sit for a month once.
But she just handed you an easy yes.
You pick the day, because "sometime" only turns real when someone does.
So pick it. Text her, "I'm in. Thursday after work, that taco place?"
Drop her vaguest text below. I'll tell you what it means.
Follow for more.

## 09 meta
<!-- meta: series=Decode her text #5, titleCard="She says let's hang out sometime", bubble="we should hang out sometime!",
caption hook="When she says 'we should hang out sometime', it's an open door. Pick the day.",
caption body="'Sometime' only becomes real when someone names a day. Reply with a day and a place, once.",
caption prompt="Drop her vaguest text in the comments and I'll tell you what it means.",
caption tags="#datingadviceformen #datingtips #howtotextagirl #textingtips" -->

## 10 · Signs she likes you #5 · "Count the signs"
She touched your arm twice. That's not nothing.
But if you freeze up, she'll probably stop.
I froze like a statue once. She never did it again.
One touch can just be friendly, so count.
Touch plus standing close means she's comfortable, because people keep distance from guys they don't like.
Before you leave, say, "I like talking to you. Can I take you out?"
Save this for the next time she touches your arm.
Follow for more.

## 10 meta
<!-- meta: series=Signs she likes you #5, titleCard="She touches your arm", bubble="stoppp you're so funny",
caption hook="She touches your arm when she talks to you? One touch can be friendly. Count the other signs.",
caption body="Touch, standing close and eye contact together mean she's comfortable with you. Stay relaxed and ask her out before you leave.",
caption prompt="Save this for the next time she touches your arm.",
caption tags="#datingadviceformen #datingtips #signsshelikesyou #femalepsychology" -->
