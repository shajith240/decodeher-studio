# Sound design: what each layer does to the viewer (10-14)

Why this exists: the owner said our SFX felt "random". This note says which layer to use, why it works on the viewer, how dense to go, and which libraries are legal for @thedecodeher. The files are in `library/sfx-pro/` (129 files, 17 categories, see its `index.json`). Our measured Zoltium numbers are in [[zoltium-sound]].

Honesty note: Zoltium, Dark Needle, Lemmino and Johnny Harris have not published their sound workflows, and the searches found none. What we know about Zoltium comes from our own stem analysis. The rest of this note rests on film-sound theory, music-psychology research and mixing practice.

---

## 1. The layers and the job each one does

| Layer | Psychological job | When | Typical level under the voice | Folder |
|---|---|---|---|---|
| **Room tone / ambience bed** | Makes the world feel continuous, so a silence reads as a choice and not as a dead file. "Night room" puts the viewer alone with their phone, which is relatable | Whole reel, very low | -30 to -40 dB | `room-tone/` |
| **Tension drone** | Sustained uncertainty. In Huron's ITPRA model, the *tension* response is the stress that builds before an expected event | Hook and story setup; cut it out at the reveal | -18 to -24 dB | `tension-drone/` |
| **Riser** (pitch or noise sweep up) | Anticipation: it tells the brain that something is coming. Huron says *imagination* and *tension* responses fire before the event and *prediction/reaction* fire after it. A riser deliberately triggers the before-phase | 1–4 s before a reveal | Grows to about -6 dB | `riser/` |
| **Reverse swell** ("suck-in") | The same anticipation, but short (0.5–2 s); it pulls the viewer into the cut | Into a cut or impact; the peak lands on the cut frame | -10 dB | `reverse-swell/` |
| **Silence / suck-out** (0.3–0.6 s) | A contrast spike. Murch: the audience "will crowd that silence with sounds and feelings of their own making". Zoltium z1 puts 0.5 s of silence before its drop | Between the riser and the reveal line | n/a | (no file; cut everything, and keep only room tone) |
| **Impact / boom with tail** | Release, the payoff. In Huron's terms, the *reaction* (startle) plus a *prediction* reward | On the reveal word | Peak about -6 dB, tail under the voice | `impact-cinematic/` |
| **Sub drop** | Felt weight. Low frequencies are linked to unease: in the 2003 "Soundless Music" concerts, 17 Hz infrasound raised reports of unease and chills by an average of 22% | Under the impact, or alone on the "turn" | On phone speakers it is mostly felt and seen as speaker movement, so do not rely on it alone | `sub-drop/` |
| **Braam / dark hit** | "Something is wrong". A cultural code from trailers since *Inception* (2010) for danger and scale | One per reel at most, on the red-flag or twist line | -6 dB | `braam/` |
| **Stinger / ping** | A short tonal punctuation mark: "note this" | Punchline, the number in a list, a caption slam | -10 dB | `stinger/` |
| **Whoosh, soft (air)** | Motion and continuity. It says "we moved" without being an event | Scene or caption changes inside a section | -14 to -18 dB | `whoosh-soft/` |
| **Whoosh, heavy (designed)** | A section break, an act change | Only between acts, 1–2 per reel | -8 dB | `whoosh-heavy/` |
| **Glitch** | A pattern break that signals "manipulation" or a distorted reality. It works as an interrupt near the drop-off points (about 3 s and 7 s) | On a "the trick is…" line, corrupted text, or the 7 s mark | -12 dB, very short | `glitch/` |
| **UI / text tick** | Micro-reward and order: the eye gets a sound for each new piece of information | Each caption or number pop. **Quiet**, so it never reads as a notification | -20 to -26 dB | `ui-tick/` |
| **Phone foley** (vibrate, notify, typing) | Relatability. The viewer's own life comes into the reel. It is encoded sound: Murch puts these at the "meaning" end of his spectrum, between language and music | Texting stories, "he left you on read" | -12 dB, panned slightly | `phone/` |
| **Heartbeat** | Body arousal by suggestion. In Valins (1966), men rated photos as more attractive when the heartbeat they thought was their own sped up. Later work says that *attention* to the sound explains much of the effect. Either way it fits dating content exactly | Crush, anxiety, or "your body knows before you do" lines | -14 dB | `heartbeat/` |
| **Clock tick** | Time pressure: waiting for a reply, a deadline | "3 days, no text" beats | -16 dB | `clock/` |
| **Breath** | Intimacy or fear, very close to the listener. An inhale right before a line works as a tiny riser | Before the reveal line, or for intimacy | -18 dB | `breath/` |
| **Paper / cloth foley** | Tactility. Cards and silhouettes feel physical, not like a flat graphic | Card reveals, character movement | -18 dB | `paper-cloth/` |
| **Sonic signature** | Brand memory. Ipsos (2020, via secondary sources) reports that ads with distinctive sonic brand cues were **8.5×** more likely to be high performers, yet only about 6–8% of ads use them | The **same** 2–3 sounds in every reel, in the same role | n/a | Pick once and log the choice in brain/rules |

Recommended signature (keep it the same every reel, do not rotate):
- **Reveal** = `reverse-swell-03-async-tonal-deep` → 0.4 s silence → `impact-cinematic-04-boom-091` + `sub-drop-03-sfx-sub-sonic-bass-09`
- **Caption tick** = `ui-tick-01-…glassticks-25`
- **Red flag** = `braam-04-braam-035-g`

## 2. Layering plan per moment type

**Hook (0–3 s).** Room tone + a tension drone that starts *before* the first word. Optionally add one glitch or stinger on the hook word. No heavy whoosh: the reel has no "before" to transition from.

**Relatable setup (story, texting).** Room tone, drone or beat low, then phone foley (vibrate, notify, typing) on the matching words. Use soft whooshes on scene changes and UI ticks on captions. 2–4 SFX per 10 s.

**Turn / "but here's the thing".** Glitch or reverse swell into the cut, then a sub drop on the turn word. Drop the drone level or change it, so the turn is heard as well as said.

**Reveal / payoff (the psychology fact).** Riser (1–3 s), then **suck-out of 0.3–0.6 s** (kill music and drone; keep room tone), then **impact + sub** on the key word, letting the tail ring under the next line. Do this once per reel, at most twice. That matches Zoltium's riser → 0.5 s silence → drop.

**List items / numbers.** A stinger or ping per item, *or* a tick per item. Never both.

**Red flag / dark twist.** Braam (once per reel), with heartbeat or clock under the following line.

**CTA ("follow for more").** Bring back the signature reveal sound, smaller: a soft whoosh plus a quiet stinger. The music resolves. Don't end on a braam, because it feels like a threat, not an invite.

## 3. Rules of thumb

1. **Density.** Count only *discrete* SFX (not the beat). Aim for **3–6 per 10 s**, including ticks, and **at most 1 big event** (impact, braam or heavy whoosh) per 10 s. Zoltium's 14–24 "bed hits per 10 s" ([[zoltium-sound]]) are mostly drums in the music, not SFX.
2. **Murch's "law of two-and-a-half".** The ear tracks about 2.5 layers *of the same kind*. Spread across the spectrum, about 5 layers is the tolerable maximum. So at any instant you can have at most: voice + bed + one SFX event (+ sub + tail). Two whooshes on top of each other read as mush.
3. **Every SFX has a reason** you can name: a cut, a word, a caption, or an emotion. If you can't name it, delete it. "Random" means sounds without a role.
4. **Build big moments in three layers:** *transient* (click or crack, 0–30 ms, so it reads on phone speakers) + *body* (boom or tonal hit, 100 Hz–1 kHz) + *tail* (reverb or sub, 1–4 s). Line up the transients on the same frame.
5. **Phone-speaker reality.** Sub drops alone vanish on phones. Always pair them with a mid-range transient. Check every mix on a phone.
6. **Sit SFX around the voice.** Speech intelligibility lives at about 2.5–5 kHz. Cut that band 2–4 dB on the SFX/music bus while the voice talks, and duck by automation or sidechain (ProSoundWeb). Put long tails and reverbs *between* phrases, or duck the reverb itself (Production Expert).
7. **Contrast beats loudness.** The impact is big because of the silence before it. Never put two impacts within 5 s of each other.
8. **Pick one family per reel.** Pick one whoosh family, one impact family and one tick, and reuse them. Mixing sci-fi, cartoon and trailer sounds is what makes a reel sound cheap.
9. **Avoid the cheap tells:** a whoosh on *every* cut, loud UI pops, cartoon "boing" or record scratch, the same sample repeated at the same pitch (vary pitch ±1–2 semitones), and SFX louder than the voice.
10. **Duration fit.** A whoosh must match the length of the move it covers, and a riser must end exactly on the cut.

## 4. Libraries: what is legal for an Instagram brand page

| Library | Commercial on IG? | Attribution? | Key catch | Licence link |
|---|---|---|---|---|
| **Sonniss #GameAudioGDC bundle** (free) | **Yes** | **No** | Can't sell or redistribute the SFX *as SFX*; AI/ML training banned; "videos" are listed as allowed project types | <https://sonniss.com/gdc-bundle-license/> |
| **Mixkit SFX** (free) | **Yes** (its own page lists "social media marketing") | **No** | Don't resell or redistribute the raw files | <https://mixkit.co/license/#sfxFree>, summary <https://mixkit.co/llm-info/> |
| **Pixabay sound effects** (free) | **Yes** | **No** | No standalone redistribution; no trademarked content in commercial use | <https://pixabay.com/service/license-summary/> |
| **Freesound** | **CC0: yes** / CC-BY: yes, *with credit* / CC-BY-NC: **no** | CC0: no; BY: yes | Check each sound's licence; only CC0 needs nothing | <https://freesound.org/help/faq/> |
| **Zapsplat** | Yes | **Free plan: yes**; Gold plan: no | Credit line needed on the free tier | <https://www.zapsplat.com/license-type/standard-license/> |
| **BBC Sound Effects** (RemArc) | **No.** Personal, educational and research use only; commercial use needs a paid licence from the site | Yes | Do not use on a monetised or brand page without buying | <https://sound-effects.bbcrewind.co.uk/licensing> |
| **Epidemic Sound** (paid) | Yes, for safelisted channels | No | Content published while subscribed stays cleared; no *new* posts after the subscription ends | <https://www.epidemicsound.com/how-it-works/license-music-legally/> |
| **Artlist SFX** (paid) | Yes (social plan for own channels; Pro for client or ads) | No | Post-2020 accounts: published projects stay covered, but no new use after you cancel | <https://artlist.io/license> |
| **Envato Elements** (paid) | Yes | No | End products completed while subscribed stay licensed; no "as-is" redistribution | <https://help.elements.envato.com/hc/en-us/articles/360000628966> |
| **Soundly** (free tier + Pro) | Yes. Its EULA names "social media platforms" | No | Can't create *new* productions after the subscription ends; past posts stay licensed | <https://getsoundly.com/assets/Soundly-EULA.pdf> |
| **BOOM Library** (paid packs) | Yes, perpetual | No | No AI training; no use as a real-time audio tool | <https://www.boomlibrary.com/> (EULA) |

**Our choice:** Sonniss GDC (free, royalty-free, commercial, no attribution) for 124 files, plus Mixkit for 5 heartbeats. If the page later pays for one service, Epidemic or Artlist both cover Instagram. Soundly Pro is the sound-designer's choice (it includes Pro Sound Effects and Freesound integration).

## Sources
- Walter Murch, "Dense Clarity – Clear Density" (encoded vs embodied sound, law of two-and-a-half, silence): <https://transom.org/2005/walter-murch/>
- Randy Thom, "Designing a Movie for Sound" (sound as a story and point-of-view tool): <https://filmsound.org/articles/designing_for_sound.htm>; "Screenwriting for Sound": <https://www.asoundeffect.com/randy-thom-screenwriting-for-sound/>
- David Huron, *Sweet Anticipation* (ITPRA: tension and imagination before an event, prediction and reaction after): <https://researchgate.net/profile/David-Huron-2/publication/209436188_Sweet_Anticipation_Music_and_the_Psychology_of_Expectation/links/0c96052e02be139f9f000000/Sweet-Anticipation-Music-and-the-Psychology-of-Expectation.pdf>
- Valins effect (false heartbeat feedback raises attractiveness ratings; attention critique): <https://en.wikipedia.org/wiki/Valins_effect>, <https://www.psy.ox.ac.uk/publications/1124812>
- Infrasound "Soundless Music" concerts, 2003 (17 Hz, +22% unease reports): <https://www.nbcnews.com/id/3077192/ns/technology_and_science-science/t/infrasound-linked-spooky-effects>, <https://www.sarahangliss.com/?p=27293>
- Braam history (Inception, Zimmer and Zarin): <https://en.wikipedia.org/wiki/BRAAAM>, <https://www.smithsonianmag.com/smart-news/how-that-annoying-drone-from-inception-took-over-movie-trailers-12874196/>
- Shepard tone tension (Dunkirk): <https://kottke.org/18/05/hans-zimmers-clever-use-of-the-shepard-scale-in-dunkirk>
- TikTok × Kantar (88% say sound is essential; 73% stop for ads with audio): <https://ads.tiktok.com/business/tr/blog/kantar-report-how-brands-are-making-noise-and-driving-impact-with-sound-on-tiktok>
- Ipsos sonic brand cues (8.5× more likely to be high performing; secondary): <https://www.sixiemeson.com/news/ipsos-brand-audio-cues/>, <https://yougov.com/articles/40973-invest-sonic-branding-boost-consumer-recall-and-re>
- Riser, impact and whoosh grammar: <https://sounddesign.irpr.agency/glossary/riser/>, <https://www.ableton.com/en/blog/learn-how-to-make-high-impact-sounds-for-movies-and-trailers/>
- Voice and SFX mixing (2.5–5 kHz carve, ducking): <https://www.prosoundweb.com/in-the-studio-balancing-dialog-in-post-production/>, <https://www.production-expert.com/production-expert-1/using-ducking-to-improve-the-clarity-of-reverberated-dialogue>
- Short-form SFX restraint and retention interrupts (blog-level evidence): <https://socialk.it/en/blog/best-video-editing-apps-for-creators>, <https://www.socialrevver.com/blog/short-form-video-editing>
- Licences: links in the table above.
