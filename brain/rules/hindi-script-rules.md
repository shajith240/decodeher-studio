# Hindi page — script & voice rules (owner 10-16)

## WHO we talk to (owner 10-16, important)
A WIDE audience: anyone in India whose mother tongue is Hindi — students, office workers, people who speak English daily.
Goal: EVERYBODY understands instantly, including people more comfortable in English than in Hindi.
- Simple, everyday Hindi words only; no difficult or शुद्ध Hindi vocabulary (if a word needs thinking, swap it).
- Use the common English words Indians already say: text, reply, chat, attention, ignore, psychology, mood, loop, pattern.
- Short, clear sentences; one idea each. Real psychology terms are fine, always followed by a plain explanation ("यानी …").
- Friendly and respectful, like a smart friend talking — never a caricature, never preachy.

Same template as English (hook → turn → named psychology → three moves → why → natural closing line), but a Hindi-native
approach. Voice: Fish **janam** `2f4654989a3147b0a775db4f9a13ae74` (native Hindi storyteller), speed 1.05 (owner 10-16: slower speeds sound robotic — keep 1.05, slow it with PAUSES instead), temperature 0.85,
top_p 0.85, one whole take. Write in **Devanagari**; English words Indians really say stay English, written in Devanagari
(टेक्स्ट, रिप्लाई, साइकोलॉजी, लूप, फॉलो). Never bookish/शुद्ध Hindi.

Hooks that work in Hindi (Rebelvids creator's scripts, brain/research/rebelvids-dark-psych-course-transcript.txt + his ChatGPT chat):
- Direct question to the viewer: "क्या वो … और फिर …?" / "क्या तुम्हें कोई …?"
- Scenario: "सोचो, तुम …"
- Secret/curiosity: "एक साइकोलॉजिकल ट्रिक जो …" , "यहाँ है असली सीक्रेट…"
- Turn line: "तो सुनो …" / "अब सुनो, …" (instead of "Listen carefully").
- Spoken connectors make it human: ना, यार, सच बताऊँ तो, देखो, यानी, बस. Prefer flowing sentences with commas and "…",
  not short choppy sentences with full stops (that sounds robotic).
- Moves: "पहली बात… दूसरी बात… तीसरी बात…" (not "नंबर वन").
- Closing: a reason to follow/send (part 2 promise), in plain Hindi. The Hindi page gets its own outro (TBD).

## Localize every example (owner 10-16: "Hindi people don't even know a slot machine")
Every analogy, example and reference must be something an ordinary Indian viewer lives with. Never translate a Western
reference word for word; swap it for the Indian equivalent that carries the same idea:
- slot machine / casino / gambling → तीन पत्ती, लॉटरी ("बस एक बार और, शायद इस बार")
- dollars, miles, Fahrenheit → रुपये, किलोमीटर, डिग्री (or drop the number)
- prom, Thanksgiving, high-school football, Tinder-only culture → कॉलेज फेस्ट, दिवाली, क्रिकेट, इंस्टाग्राम/व्हाट्सऐप
- "grab coffee" → चाय पर मिलना; "his buddy" → उसका दोस्त/यार; "mom" → मम्मी
- Brand names only when every Indian knows them generically (WhatsApp, Instagram); never a betting-app brand.
Check before voicing: would a 20-year-old in Lucknow or Indore picture this instantly? If not, change it.

## Pace (owner 10-16, tested: speed 0.94 + "calm, unhurried" sounded ROBOTIC; speed 1.05 + casual sounded natural)
Keep speed 1.05 and the cue "[casual, storytelling, like talking to a close friend]". Make it breathe with a [pause] after the
hook turn and between the three moves, and "…" where a speaker would breathe. Never slow the speed setting itself.

## LOCKED RECIPE (owner approved 10-16: "the research recipe one sounds good and natural")
Reference: deliverables/voice-tests/hindi-v7-research-recipe-LOUD.mp3; research: brain/research/hindi-voice.md.
- Script: one thought per sentence (6-12 words, cap 18), each ends in "।" / "?" / "!", "…" for breaths, casual register
  (देखो, ना, यार, सच बताऊँ तो), loanwords in Devanagari, Indian examples only. Saved per line: brain/content/drafts/*-lines.txt.
- Voice: Fish janam 2f4654989a3147b0a775db4f9a13ae74, ONE whole take, NO tags at all (Fish tags aren't built for Hindi),
  speed 1.0, temperature 0.6, top_p 0.7, normalize false, chunk_length 300.
- Rhythm in post (never via speed or tags): split at sentence ends (tools/vo_split.py, lang hi, cuts snapped to the quietest
  point), then LIGHT pauses: 0.55 x the per-line pause plan (≈0.15-0.45 s) with ±50 ms jitter, 15 ms fades.
- Loudness: about -11.5 LUFS (same as the English reels), true peak <= -1 dBTP. Chain: acompressor threshold -20 dB ratio 3
  attack 8 release 120 makeup 4 -> +1.5 dB -> oversampled alimiter 0.89 (a limiter alone stalls at -12: voice peaks). In a full
  reel the mixer (tools/reel_mix.py) masters the voice + music to -11 anyway.
- Not used: per-part takes (owner chose the whole take), slowing the speed (robotic), long English style tags (robotic).

## 10-16 fix: no dead air (owner: "it says तीसरी बात, pauses saying nothing, then continues — robotic")
- NEVER "…" inside a Hindi line: Fish turns it into long dead air mid-sentence. Use commas; a question that spans two lines
  ends the first line with "," (not "।").
- Sentence pauses added in post: ~0.2 s inside a section, ~0.45 s at section breaks (after the hook turn, after the verdict
  line, after each move, after the payoff), ±40 ms jitter, none inside the opening question.
- Final pass caps EVERY silence at 0.6 s (the longest natural beat in conversation), then mastering (chain above).
Reference: deliverables/voice-tests/hindi-FINAL-hot-and-cold.mp3.
