# Spoken script rules (owner 10-15: "can't understand it, robotic, not natural")
Method (templates, hooks, scorecard, honesty): brain/rules/script-writing-system.md (10-17). This file = how the words sound.

## 10-17 owner, HARD RULE: only words a person really SAYS out loud
Texting words that are written but never spoken (haha, hahaha, hehe, lol, lmao, rofl, omg, idk, tbh, smh, brb, ikr, k, kk, xD)
are banned from the voice, even when quoting her text: the AI reads them literally and it sounds weird and awkward. No reel may be
built around one (the "Haha" reel was pulled from the queue 10-17). Describe it instead ("she sends a laughing reply and nothing else").
tools/reel_vo.py and tools/hindi_vo.py refuse a script that contains one.

## 10-16 owner, FINAL: value over length, effort into the hook
- No 30 s cap. A reel is as long as the explanation needs (usually 35–60 s). Never speed up the voice or squeeze pauses to fit.
- The body explains calmly, so the viewer leaves with something real. The tension and pattern-interrupt live only in the opening.
- The hook decides everything: the spoken line, the on-screen text, and the FIRST VISUAL (instantly relatable, a moment every man
  has lived). See brain/research/hooks-2026.md.

Test: a 16-year-old Indian guy who speaks English as a second language gets every line on FIRST listen. It sounds like a friend telling you something real. Applies to every script, before the voice step. Run `anthropic-skills:unslop` on the draft too.
Sources: Biber (speech vs writing), Dicks "Dinner Test", Parker/Stone "so/but", brain/research/reel-storytelling-craft.md, narrator-voice-analysis.md (real narrators average 12 words per sentence, 10% fragments, ours was 5 and 47%).

1. One reel, one idea, one situation. Name her exact text and say what it means in the first 2 sentences.
2. Order of beats: her text + what it means -> one concrete moment (told as "you" or an obvious hypothetical; never a made-up "my friend" story presented as true, 10-17) -> the real reason -> exactly what to text instead -> one comment/send line.
3. Every sentence is COMPLETE: subject + verb, 6 to 16 words. No fragments ("Just that."), no stacked one-liners. A fragment is allowed at most once, and only for her quoted text.
4. Connect every idea to the last one with "so", "because", "but", "and that's why", "now". Never jump. If you can't say which connector fits, the idea does not belong.
5. Grade-5 words. Say "doesn't know what to say", not "has no conversational hook". Ban: metaphors, abstract nouns (energy, dynamic, frame, value, investment), "look at what you sent", "here's", "that's the thing".
6. Write how you talk: contractions, "you", "she", "my friend". No "one", no "individuals", no "thus". Max one "like," or "so" opener per line.
7. Concrete beats abstract: a real object, a real text in quotes ("Wait, how did your interview go?"). The suggested text is word for word.
8. Exactly 60 to 80 spoken words (25 to 30 s). Count them. Numbers spelled out. No em dashes, no colons, max one ellipsis.
9. Explain the reason once, in one plain sentence, then move on. No lists of three. No "studies show".
10. End on one natural prompt ("Comment her last text, and I'll tell you what it means."). No "follow", no begging. The pipeline adds "Decode her."
11. Say it aloud before shipping. Any line you would not say to a friend gets rewritten.

## Reference-style writing (owner video, 10-15)
12. Before drafting, paste 2 to 3 of the transcripts in brain/research/reference-transcripts.md (Zoltium R1 plus R3, and R4 if room) into the writer prompt. Say: "Match their rhythm, word choice and sentence length. Do not copy their lines or their claims."
13. Structure: pattern-interrupt hook (a "don't" or a "stop", with her exact text) -> the relatable moment -> TEASE at each turn ("I'll show you what to text in a second") -> the plain reason -> exact text to send -> payoff and prompt.
14. Teases are complete sentences, one or two per reel, never "wait for it".

## Review pass (mandatory, after drafting, before any voice call)
Score the draft 0 or 1 on each, fix and re-score until 11 of 11:
a first-listen clear for a 16-year-old ESL reader; b no fragment (except her quoted text); c every line has a connector or a tease; d concrete (a real text, a real moment); e one reason, one fix; f 60 to 80 words (count); g contractions and "you"; h no banned words (rule 5); i hook names her exact text and the meaning within 2 sentences; j one tease; k natural comment prompt.
Then run unslop, read it aloud once, and list the scores in the draft's meta block.

## Beats (for the voice)
Write the script as 3 to 5 BEATS, a blank line between beats, each beat 1 to 3 sentences about one thought. The voice step reads one beat per call (see brain/pipeline.md, per-beat voicing), so a beat must make sense alone and must end on a full stop.
Format in the draft file: one beat per paragraph.

## Before / after
BEFORE (rejected): She texts, haha. That chat is dying. / And one more meme finishes it off. / But she's not cold. Look at what you sent. / Haha means you gave her nothing to answer, because a joke isn't a question.
Why it failed: fragments, a jump after every line, "look at what you sent" says nothing, the reason is rushed.
AFTER: When a girl texts you just "haha", she isn't laughing. She doesn't know what to say back. / My friend sent a girl a meme, and she said "haha". So he sent another. Then she stopped replying. / A meme doesn't ask her anything, so she has nothing to answer. / So bring up something she told you. Like, "Wait, how did your interview go?" Now she has something to talk about.

BEFORE: "Three hours later: 'sorry, just saw this.' Fine. Her time, her rules. Stop counting. Match her energy."
AFTER: "She waited three hours and then wrote, 'sorry, just saw this.' That doesn't mean she's playing games. It means she was busy and she felt a bit bad. So don't punish her with a cold reply. Just write back like normal, and ask her how her day was."

## Owner rule (10-15): never READ text-speak aloud
Never voice "haha", "lol", "hmm", "k", "lmao", emojis or slang spellings. The narrator DESCRIBES them like a person would
("she just sends a laugh back", "she replies with one letter", "she leaves you on seen"). Her exact text appears on screen in the
chat bubble — the voice never reads it.

## Owner rule (10-15): no fixed slogan — a natural closing line per script
End every script with ONE short closing line that sums up THAT reel's point in plain words, like the last thing a friend says
("Give her something to answer, and she will."). ≤ 12 words, memorable, no catchphrase repeated across reels. Order: …the move →
the comment/send/save prompt → [confident] closing line. Never end on "Decode her." or "Follow for more."

## Value test — every script must pass all (owner 10-15: "be strict: every reel must create something valuable")
Why: scripts were thin (a hook, a friend story, one line to text). A viewer must leave knowing something he did not know. Research: [[research/value-density]]. This test OVERRIDES the 60-80 word rule (8): scripts run 85 to 115 spoken words (~35-45 s), longer only because of real value.
Score 1 or 0 on each. Ship only at 7 of 7.
a. **Real reason**: says WHY she does it, with the mechanism in one plain "because" sentence. "She likes you" or "she is busy" alone fails.
b. **Why his instinct backfires**: names what guys do and the exact way it makes things worse.
c. **Two moves minimum**, each with exact words in quotes or an exact action (when, where, what to say).
d. **A repeatable insight**: one sentence he could say to a friend and sound smart. It must stand alone.
e. **Zero filler**: no invented friend stories (owner 10-15); at most a one-sentence "you" scenario. Every sentence adds a new fact, mistake or move. Delete any line that only repeats.
f. **Save test**: would a guy screenshot or save it for the next time this happens? If he would only nod, it fails.
g. **Accurate and respectful**: no overclaiming (use "usually", "often", "most"), no invented stats, no manipulation or PUA tactics, nothing that hides intent.
Hook: her behaviour and why it matters in the first two sentences (unchanged). Order: hook -> "Here's why" mechanism -> the mistake -> two or three moves -> the repeatable line -> prompt -> [confident] closing line. Keep "Here's why" as the start of the mechanism line and one "because" in it (the pipeline finds the re-hook and the why-drop from them).

## Engagement test — every script must pass all (owner 10-15: storytelling = draw the viewer in, NOT a made-up story)
Do not invent anecdotes ("my friend did..."). Narrative pull comes from tension, an open loop and escalation. Score 1 or 0, ship at 7 of 7, alongside the value test.
A. **Hook tension**: line 1 is her exact behaviour and line 1-2 leaves him unsure what it means.
B. **Open loop**: an early line promises a payoff he doesn't yet have ("most guys get the next part wrong", "what you do next kills the chat").
C. **Escalation**: each line raises the cost or curiosity (the mistake, then what it does to her). Lines 2 to 4 are in an order that cannot be swapped.
D. **Reveal**: one "Here's why" turn that changes how he sees her behaviour.
E. **Payoff**: the loop closes with the moves, in his words, right after the reveal.
F. **Emotional close**: the last line lands as a feeling or a rule he'll remember, unique to this reel.
G. **No dead lines**: every line makes him want the next one; a line that only repeats or explains gets cut.
