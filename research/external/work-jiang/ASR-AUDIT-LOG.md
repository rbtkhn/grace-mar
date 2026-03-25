# ASR audit log — work-jiang / Predictive History

**Purpose:** Cross-session traceability for **targeted** transcript verification (not full linear proofreading). Canonical rules: [ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md). Operator research only; not companion Record.

---

## Contents

1. [Scope](#1-scope-kickoff--edit-when-you-start-a-pass)
2. [Preconditions](#2-preconditions-check-before-auditing)
3. [Targeted verification](#3-targeted-verification-what-to-actually-check)
4. [Findings log — Geo-Strategy](#4-findings-log-append-rows) — 177 rows, 20 episodes, 2026-03-24
   - [Highest-impact patterns](#highest-impact-patterns)
   - [Candidate recurring replacements](#candidate-recurring-replacements)
5. [Findings log — Secret History (Volume III)](#5-findings-log--secret-history-volume-iii) — row log SH01–04 (62 norm. subs); SH05–21 verbatim+audited; SH22–28 pending verbatim, 2026-03-24
   - [Secret History highest-impact patterns](#secret-history-highest-impact-patterns)
   - [Secret History candidate replacements](#secret-history-candidate-replacements)
   - [Secret History scope limitation](#secret-history-scope-limitation)
6. [Commands reference](#6-commands-reference)
7. [Related](#related)

---

## 1. Scope (kickoff — edit when you start a pass)

| Field | Your choice |
|-------|-------------|
| **Series** | `geo-strategy`, `secret-history` |
| **Depth** | **B** — all in-scope episodes, targeted signals only |
| **Session / date** | 2026-03-24 |

**Passes complete:**
- Geo-Strategy, depth B, 20 episodes (geo-strategy-01 through -20).
- Secret History, depth B, **21** verbatim ASR-derived `## Full transcript` episodes (secret-history-01 through -21): normalized where run, manually audited, pytest green.
- Secret History **next:** **SH22–28** still have operator-written analytical outlines under `## Full transcript` (not caption-verbatim) where not yet pasted. Raw YouTube `.txt` exists for all 28 — paste verbatim body when ready, then repeat: `normalize_lecture_transcript_asr.py <file> --write` → targeted audit → `StrReplace` → `pytest tests/test_normalize_lecture_transcript_asr.py -q`.

---

## 2. Preconditions (check before auditing)

- [x] **Raw captions:** 20/20 geo-strategy `.txt` fetched via `--input geo-strategy-urls.txt --resume` (2026-03-24).
- [x] **Coverage report:** `check_asr_audit_preconditions.py --only-glob 'geo-strategy-*'` → 20 scanned, 20 found, 0 missing.
- [x] **Tooling sanity:** `pytest tests/test_normalize_lecture_transcript_asr.py -q` → 10 passed (2026-03-24).
- [x] **Secret History raw coverage:** `check_asr_audit_preconditions.py --only-glob 'secret-history-*'` → 28 scanned, 28 raw `.txt` found, 0 missing.
- [x] **Verbatim diff layer:** `sync_verbatim_transcripts.py --write --only-glob 'geo-strategy-*'` → 20 written, 0 missing raw. Series detected as `geo-strategy` (common tier only).
- [ ] **Jiang fingerprint (optional, read-only):** [JIANG-LECTURE-FINGERPRINT.md](JIANG-LECTURE-FINGERPRINT.md) scaffold present but not populated.

---

## 3. Targeted verification (what to actually check)

Do **not** proofread entire transcripts unless depth **C** or a chapter requires it. **Do** verify when any of these apply ([ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md) § Targeted verification):

| Signal | Checked? (episode list or “all in scope”) |
|--------|-------------------------------------------|
| Proper names, non-English, book titles | All 20 geo-strategy episodes |
| Numbers, dates, counts | All 20 geo-strategy episodes |
| Direct attribution / pull-quotes | All 20 geo-strategy episodes |
| Sensitive or high-liability lines | All 20 geo-strategy episodes |

**Compare:** raw `.txt` ↔ `verbatim-transcripts/<slug>.md` (if generated) ↔ `lectures/<slug>.md` (`## Full transcript` if present) ↔ quote candidates you intend to promote to `metadata/quotes.yaml`.

**Geo-Strategy invariant:** never treat civilization-only ASR fixes as automatic for geo (e.g. “thieves” vs Thebes) — see tests and `asr_light_clean.py`.

---

## 4. Findings log (append rows)

| Date | Lecture file | Signal type | Before (short) | After / fix | Verified how |
|------|--------------|-------------|------------------|-------------|--------------|
| 2026-03-24 | geo-strategy-01 | Proper name | "Kasam salamani" | Qasem Soleimani | Raw vs known figure; ~8 occurrences across eps 01, 04 |
| 2026-03-24 | geo-strategy-01 | Domain vocab | "position strike" | precision strike | Context: "so precise that it only hit the Iranian Embassy" |
| 2026-03-24 | geo-strategy-01 | Homophone | "suicide bools" | suicide boats | Context: Millennium Challenge small-boat swarms |
| 2026-03-24 | geo-strategy-01 | Phonetic | "Star Force" | Dark Forest | Surrounding lines say "Dark Forest"; isolated garble |
| 2026-03-24 | geo-strategy-01 | Proper name | "1953 K" | 1953 coup | British/American overthrow of Mosaddegh |
| 2026-03-24 | geo-strategy-01 | Proper name | "Sha" / "shaw" | Shah | Historical title of Iranian monarch |
| 2026-03-24 | geo-strategy-01 | Garbled phrase | "overw Asha" | overthrew the Shah | Context: 1979 revolution |
| 2026-03-24 | geo-strategy-01 | Proper name | "heson Lebanon Kam M" | Hezbollah, Lebanon, Hamas | Axis of resistance enumeration |
| 2026-03-24 | geo-strategy-01 | Proper name | "hthis in Yaman" | Houthis in Yemen | Both name and place garbled |
| 2026-03-24 | geo-strategy-01 | Domain vocab | "the Torance" | deterrence | Context: disproportionality policy |
| 2026-03-24 | geo-strategy-01 | Proper name | "young K War" | Yom Kippur War | Context: wars where "entire Middle East attacked Israel" |
| 2026-03-24 | geo-strategy-01 | Homophone | "operation two promise" | Operation True Promise | Correct elsewhere in same transcript; garbled 3× later |
| 2026-03-24 | geo-strategy-01 | Domain vocab | "cout" | coup | "launched a [coup]" |
| 2026-03-24 | geo-strategy-02 | Proper name | "Austin" (intermittent) | Augustine | Correct earlier; truncation in later occurrences |
| 2026-03-24 | geo-strategy-02 | Proper name | "denters" / "descenders" | dissenters | English religious dissenters |
| 2026-03-24 | geo-strategy-02 | Proper name | "the pittin" | the Puritans | "the [dissenters], the [Puritans] killed the king" |
| 2026-03-24 | geo-strategy-02 | Proper name | "Pax Roma" | Pax Romana | Latin term truncated |
| 2026-03-24 | geo-strategy-03 | Number | "after World War III" | after World War II | Post-war factories context; clearly WWII not III |
| 2026-03-24 | geo-strategy-03 | Proper name | "the do crash" | the dot-com crash | 2001 internet/stock crash |
| 2026-03-24 | geo-strategy-03 | Domain vocab | "sub crime uh crash" | subprime crash | 2008 financial crisis |
| 2026-03-24 | geo-strategy-03 | Proper name | "Breton Woods" / "Brendon woods" / "Bron Woods" / "bread and WT" | Bretton Woods | Four garbled forms in one transcript |
| 2026-03-24 | geo-strategy-03 | Number | "133%" (Germany 1900 equities) | 13% | Alongside UK 25%, US 14.5%, France 11%; 133% impossible |
| 2026-03-24 | geo-strategy-03 | Proper name | "the regular Revolution" | the Reagan Revolution | Post-1980 neoliberal shift |
| 2026-03-24 | geo-strategy-03 | Domain vocab | "theism" | deism | Founding fathers; speaker describes deism exactly |
| 2026-03-24 | geo-strategy-04 | Proper name | "straight of humus" | Strait of Hormuz | Critical chokepoint |
| 2026-03-24 | geo-strategy-04 | Proper name | "SE Canal" / "seus canal" | Suez Canal | Multiple garbled forms |
| 2026-03-24 | geo-strategy-04 | Proper name | "jerk Kushner" | Jared Kushner | Trump son-in-law; 2 occurrences |
| 2026-03-24 | geo-strategy-04 | Proper name | "Jamal Hashi" | Jamal Khashoggi | Washington Post journalist |
| 2026-03-24 | geo-strategy-04 | Acronym | "NBS" (~8×) vs correct "MBS" (2×) | MBS (Mohammed bin Salman) | Inconsistent within same transcript |
| 2026-03-24 | geo-strategy-04 | Proper name | "alsad family" / "alide family" | al-Saud family | Saudi ruling family; two garbled forms |
| 2026-03-24 | geo-strategy-04 | Domain vocab | "applicate" | abdicate | Saudi monarchy should step down |
| 2026-03-24 | geo-strategy-04 | Proper name | "hesah" | Hezbollah | Truncated |
| 2026-03-24 | geo-strategy-05 | Proper name | "Sheldon elderson" / "sandel elderson" | Sheldon Adelson | Casino billionaire; multiple garbled forms |
| 2026-03-24 | geo-strategy-05 | Proper name | "nanyu" | Netanyahu | 3× garbled |
| 2026-03-24 | geo-strategy-05 | Proper name | "J vent" / "JD vents" / "shie Vance" | JD Vance | Multiple garbled forms |
| 2026-03-24 | geo-strategy-05 | Proper name | "rugate" | Russiagate | Media narrative about Trump/Russia |
| 2026-03-24 | geo-strategy-05 | Number | "20120" | 2020 | "also in [2020] there's something called a George Floyd protest" |
| 2026-03-24 | geo-strategy-05 | Proper name | "Camila Harris" | Kamala Harris | Correct elsewhere in same transcript |
| 2026-03-24 | geo-strategy-06 | Proper name | "Donald russfield" / "Ron field" / "RFI" | Donald Rumsfeld | Secretary of Defense; many garbled forms |
| 2026-03-24 | geo-strategy-06 | Proper name | "Paul wolitz" / "Wolford" / "wolf" | Paul Wolfowitz | Deputy Secretary of Defense |
| 2026-03-24 | geo-strategy-06 | Homophone | "ear defense" / "ear power" / "ear Supremacy" | air defense / air power / air supremacy | Persistent "air"→"ear" throughout |
| 2026-03-24 | geo-strategy-06 | Homophone | "East drop on all electronic communications" | eavesdrop | Context: surveillance |
| 2026-03-24 | geo-strategy-06 | Proper name | "Daniel ellsburg" | Daniel Ellsberg | Pentagon Papers leaker |
| 2026-03-24 | geo-strategy-06 | Proper name | "lynen Johnson" | Lyndon Johnson | US president escalating Vietnam |
| 2026-03-24 | geo-strategy-06 | Proper name | "The myly Massacre" / "viese village" | The My Lai Massacre / Vietnamese village | Vietnam War atrocity |
| 2026-03-24 | geo-strategy-06 | Domain vocab | "deification" (Iraq post-invasion) | de-Baathification | Firing old government; completely changes concept |
| 2026-03-24 | geo-strategy-06 | Domain vocab | "hamon" (sole superpower) | hegemon | Context: "the only Power" |
| 2026-03-24 | geo-strategy-06 | Homophone | "military insulations" | military installations | SOF looking for bases |
| 2026-03-24 | geo-strategy-06 | Proper name | "backd completely open" | Baghdad | Iraqi capital |
| 2026-03-24 | geo-strategy-06 | Number | "the most we can do is about 00,000" | ~500,000 (or 300,000) | Digit dropped; context: between 1M and 130k |
| 2026-03-24 | geo-strategy-07 | Proper name | "Ibraham Ry" / "Ibraham razy" / "REI" | Ebrahim Raisi | Iranian president; many garbled forms |
| 2026-03-24 | geo-strategy-07 | Proper name | "Kami" / "CI" / "camani" / "kamani" | Khamenei (Ali Khamenei) | Supreme Leader |
| 2026-03-24 | geo-strategy-07 | Proper name | "mosta Kami" / "mosab kamani" / "MOBA Kami" | Mojtaba Khamenei | Khamenei's son; multiple garbled forms |
| 2026-03-24 | geo-strategy-07 | Proper name | "salamani" / "salaman" / "solomani" | Soleimani (Qasem) | IRGC commander |
| 2026-03-24 | geo-strategy-07 | Proper name | "Azan" (dam ceremony) | Azerbaijan | Cross-border trip context |
| 2026-03-24 | geo-strategy-07 | Proper name | "masah ameni" | Mahsa Amini | 2022 protest catalyst |
| 2026-03-24 | geo-strategy-07 | Proper name | "Hussein Dagan" | Hossein Dehghan | Defense Minister 2013-17 |
| 2026-03-24 | geo-strategy-07 | Number | "from 207 to 2019" | from 2007 to 2019 | Jafari's IRGC tenure; dropped digit |
| 2026-03-24 | geo-strategy-07 | Number | "January 20120" | January 2020 | Soleimani assassination date |
| 2026-03-24 | geo-strategy-07 | Proper name | "I Iona Ki" | Ayatollah Khomeini | Brought back from exile; founder of Islamic Republic |
| 2026-03-24 | geo-strategy-07 | Homophone | "revolutionary guard corpse" | Revolutionary Guard Corps | "corpse" vs "Corps" |
| 2026-03-24 | geo-strategy-07 | Proper name | "basashi" / "Basi" / "Bazi" | Basij | Volunteer militia |
| 2026-03-24 | geo-strategy-07 | Proper name | "hufi" / "hoovies in y man" | Houthi / Houthis in Yemen | Both name and place garbled |
| 2026-03-24 | geo-strategy-07 | Proper name | "hesah" (in Lebanon) | Hezbollah | Truncated |
| 2026-03-24 | geo-strategy-07 | Proper name | "Muhammad M mbar" / "Muhammad marbar" | Mohammad Mokhber | VP predicted to win election |
| 2026-03-24 | geo-strategy-07 | Proper name | "homus" | Hormuz (Strait of) | Chokepoint |
| 2026-03-24 | geo-strategy-08 | Proper name | "APAC" (throughout) | AIPAC | Israel lobby acronym; missing "I" |
| 2026-03-24 | geo-strategy-08 | Proper name | "nanyu" / "Nan yahu" / "natany" | Netanyahu (Benjamin) | Israeli PM; multiple garbled forms |
| 2026-03-24 | geo-strategy-08 | Proper name | "Muhammad bin Salon" | Muhammad bin Salman (MBS) | Saudi leader |
| 2026-03-24 | geo-strategy-08 | Proper name | "tus Kushner" | Charles Kushner | Jared Kushner's father |
| 2026-03-24 | geo-strategy-08 | Proper name | "Nikki Hy" / "niiki heli" | Nikki Haley | VP prediction context |
| 2026-03-24 | geo-strategy-08 | Proper name | "T aiv" | Tel Aviv | US embassy moved |
| 2026-03-24 | geo-strategy-08 | Acronym | "NBS killed a journalist" | MBS | Referring to bin Salman / Khashoggi |
| 2026-03-24 | geo-strategy-08 | Proper name | "Kasam salamani" / "salamini" | Qasem Soleimani | IRGC commander |
| 2026-03-24 | geo-strategy-08 | Proper name | "Gerald art Ford" | Gerald R. Ford (USS) | Supercarrier name |
| 2026-03-24 | geo-strategy-08 | Proper name | "Tran" / "tan" / "Teran" | Tehran | Iranian capital |
| 2026-03-24 | geo-strategy-08 | Proper name | "dones" (eastern Ukraine) | Donbas | Ukraine region |
| 2026-03-24 | geo-strategy-08 | Proper name | "Crea" (southern front) | Crimea | Ukraine context |
| 2026-03-24 | geo-strategy-08 | Proper name | "K" (the capital) | Kyiv | Ukrainian capital |
| 2026-03-24 | geo-strategy-08 | Proper name | "alab alabes" / "alabed" | Alcibiades | Athenian statesman, 415 BC |
| 2026-03-24 | geo-strategy-08 | Proper name | "nus" (opponent) | Nicias | Athenian general opposing Sicily expedition |
| 2026-03-24 | geo-strategy-08 | Proper name | "faciiities the pelan war" | Thucydides; Peloponnesian War | "we studied [X] last semester" |
| 2026-03-24 | geo-strategy-08 | Proper name | "zalinski" / "zilinski" / "zinsky" | Zelenskyy | Ukrainian president |
| 2026-03-24 | geo-strategy-08 | Number | "$1 13 billion super carrier" | $13 billion | USS Gerald R. Ford cost; spurious "1" |
| 2026-03-24 | geo-strategy-09 | Proper name | "Mo mova" | Moldova | Potential Russian target |
| 2026-03-24 | geo-strategy-09 | Proper name | "federick Hegel" | Friedrich Hegel | German philosopher |
| 2026-03-24 | geo-strategy-09 | Domain vocab | "symphysis" | synthesis (Hegelian) | Thesis-antithesis-synthesis |
| 2026-03-24 | geo-strategy-09 | Proper name | "Carl Marx" / "marks" | Karl Marx | Philosopher/economist |
| 2026-03-24 | geo-strategy-09 | Proper name | "Mar thater the thater Revolution" | Margaret Thatcher | British PM |
| 2026-03-24 | geo-strategy-09 | Foreign term | "Ze guys" | Zeitgeist | German for "spirit of the times" |
| 2026-03-24 | geo-strategy-09 | Proper name | "Leo Toy Story" | Leo Tolstoy | Russian author |
| 2026-03-24 | geo-strategy-09 | Proper name | "a Korean" | Anna Karenina | Tolstoy novel |
| 2026-03-24 | geo-strategy-09 | Proper name | "J Austin" | Jane Austen | British author |
| 2026-03-24 | geo-strategy-09 | Domain vocab | "CIP to illegal immigrants" | citizenship | Military recruitment proposal |
| 2026-03-24 | geo-strategy-10 | Proper name | "Breton Woods" | Bretton Woods | 1945 monetary agreement |
| 2026-03-24 | geo-strategy-10 | Proper name | "bricks" / "breaks" | BRICS | International grouping; throughout |
| 2026-03-24 | geo-strategy-10 | Proper name | "OS bin ladin" | Osama bin Laden | al-Qaeda leader |
| 2026-03-24 | geo-strategy-10 | Proper name | "RFA" (Israel attacking) | Rafah | Gaza city |
| 2026-03-24 | geo-strategy-10 | Proper name | "northstream pipeline" | Nord Stream pipeline | Gas infrastructure |
| 2026-03-24 | geo-strategy-10 | Domain vocab | "porah state" | pariah state | Diplomatic isolation |
| 2026-03-24 | geo-strategy-10 | Proper name | "cing ping" | Xi Jinping | Chinese leader |
| 2026-03-24 | geo-strategy-10 | Proper name | "molotov rippen trop" | Molotov-Ribbentrop (Pact) | 1939 agreement |
| 2026-03-24 | geo-strategy-10 | Proper name | "Rudolph H" | Rudolf Hess | Emissary to Scotland |
| 2026-03-24 | geo-strategy-10 | Proper name | "Barbarosa" / "bar Barosa" | Barbarossa (Operation) | 1941 invasion |
| 2026-03-24 | geo-strategy-10 | Proper name | "stellin" / "Silent" / "stad" / "salon" / "Sal" / "Salin" / "silin" | Stalin | ~8 ASR garbles of one name |
| 2026-03-24 | geo-strategy-10 | Domain vocab | "land Le" / "Lenley" | Lend-Lease | WWII aid program |
| 2026-03-24 | geo-strategy-10 | Number | "45 million Soviet troops at the border" | 4-5 million | Later says "four to five million"; ASR fused digits |
| 2026-03-24 | geo-strategy-10 | Proper name | "M would not have won the war" | Mao (Zedong) | Communist China context |
| 2026-03-24 | geo-strategy-11 | Proper name | "peritan" | Puritan | "pilgrims and the peritan" — founding colonists |
| 2026-03-24 | geo-strategy-11 | Homophone | "theism" | deism | Speaker says "deism" correctly 5 lines later |
| 2026-03-24 | geo-strategy-11 | Homophone | "succeeded from the union" | seceded | Civil War secession; classic ASR homophone |
| 2026-03-24 | geo-strategy-11 | Strategy vocab | "kudas" | coups (d'état) | "arm of the military…tries to overthrow the government" |
| 2026-03-24 | geo-strategy-11 | Proper name | "SLE force" | Delta Force | "most elite…exactly 1,000 members"; dropped consonants |
| 2026-03-24 | geo-strategy-11 | Proper name | "Niki Hill hilly" / "niiki Hy" | Nikki Haley | Multiple garbled renderings |
| 2026-03-24 | geo-strategy-12 | Proper name | "turkin" (×5+) | Turchin (Peter Turchin) | Cliodynamics founder |
| 2026-03-24 | geo-strategy-12 | Proper name | "hongran" | Hong Xiuquan (洪秀全) | Leader of Taiping Rebellion |
| 2026-03-24 | geo-strategy-12 | Proper name | "typing Rebellion" | Taiping Rebellion | 19th-c. Chinese civil war |
| 2026-03-24 | geo-strategy-12 | Foreign term | "udonia" (×3) | eudaimonia | Greek concept |
| 2026-03-24 | geo-strategy-12 | Foreign term | "sity" / "cinity" / "secrity" | sociality | Social cohesion/trust; garbled differently each time |
| 2026-03-24 | geo-strategy-12 | Proper name | "Barbarosa" | Barbarossa (Operation) | 1941 invasion |
| 2026-03-24 | geo-strategy-12 | Proper name | "Octavius ptin" | Octavian / Putin | Two names merged by ASR |
| 2026-03-24 | geo-strategy-12 | Proper name | "law and EG man on" | Laocoon and Agamemnon | Homeric figures |
| 2026-03-24 | geo-strategy-12 | Proper name | "the pisan war" | the Peloponnesian War | ASR phonetic collapse |
| 2026-03-24 | geo-strategy-12 | Foreign term | "the C system" / "kuu candidates" | keju (科举) system / keju candidates | Imperial Chinese examination; ASR cannot handle Chinese term |
| 2026-03-24 | geo-strategy-13 | Editorial | Opening greeting in raw trimmed in curated | N/A — editorial choice | Raw vs curated start comparison |
| 2026-03-24 | geo-strategy-13 | Proper name | "Osam Hussein" | Saddam Hussein | "overthrows [Saddam] Hussein" |
| 2026-03-24 | geo-strategy-13 | Strategy vocab | "debuffification" / "deaf" | de-Ba'athification | Curated tags correct; transcript text garbled |
| 2026-03-24 | geo-strategy-13 | Proper name | "the trade of humus" | the Strait of Hormuz | Geo-strategic chokepoint; same error in geo-14 |
| 2026-03-24 | geo-strategy-13 | Homophone | "ferment sectarian violence" | foment | "foment" = incite |
| 2026-03-24 | geo-strategy-13 | Homophone | "the strategic death" | the strategic depth | Military concept inverted |
| 2026-03-24 | geo-strategy-13 | Foreign term | "blitz crack, shock and all" | blitzkrieg, shock and awe | Two military terms garbled |
| 2026-03-24 | geo-strategy-13 | Proper name | "the Mckender thesis" | the Mackinder thesis | Halford Mackinder's Heartland theory |
| 2026-03-24 | geo-strategy-14 | Number | "the beginning of World War II" | World War III | Video title is "WWIII Begins"; ASR "III"→"II" |
| 2026-03-24 | geo-strategy-14 | Raw→curated fix | Raw: "evading uh Iran" | Curated: "invading" Iran | Correct fix but undocumented |
| 2026-03-24 | geo-strategy-14 | Proper name | "the street of Humus" | the Strait of Hormuz | Same garble as geo-13 |
| 2026-03-24 | geo-strategy-14 | Proper name | "Sencom" | CENTCOM (Central Command) | Curated tags correct |
| 2026-03-24 | geo-strategy-14 | Strategy vocab | "exclusion dominance" | escalation dominance | Correct earlier; garbled on second mention |
| 2026-03-24 | geo-strategy-14 | Foreign term | "esquetology" | eschatology | Theology of end times |
| 2026-03-24 | geo-strategy-14 | Strategy vocab | "the Aatollah and his mas" | the Ayatollah and his mullahs | "mas" is ASR truncation |
| 2026-03-24 | geo-strategy-14 | Proper name / context | "to invade Iraq" | likely Iran | Context entirely about Iran; meaning-altering |
| 2026-03-24 | geo-strategy-14 | Number | "robbed him of power in 2022" | 2020 | Speaker self-corrects immediately after |
| 2026-03-24 | geo-strategy-15 | Proper name | "Yatollah" / "Aatollah" / "Alatia" / "Alatollah" | Ayatollah | Four ASR garbles in one lecture |
| 2026-03-24 | geo-strategy-15 | Proper name | "Nanyahu" / "Natanya" | Netanyahu | Two garbled forms |
| 2026-03-24 | geo-strategy-15 | Proper name | "Zorashinism" (×2) | Zoroastrianism | Ancient Persian religion |
| 2026-03-24 | geo-strategy-15 | Proper name | "Tomies of Egypt" | Ptolemies of Egypt | Hellenistic dynasty; dropped initial cluster |
| 2026-03-24 | geo-strategy-15 | Proper name | "Seucid Empire" | Seleucid Empire | Hellenistic successor state |
| 2026-03-24 | geo-strategy-15 | Proper name | "the Ma the ring of the Mcabes" | the reign of the Maccabees | Jewish revolt / Hasmonean period |
| 2026-03-24 | geo-strategy-15 | Proper name | "Mark Millie" | Mark Milley | Chairman of Joint Chiefs |
| 2026-03-24 | geo-strategy-15 | Proper name | "Mer Lago" | Mar-a-Lago | Trump's Florida residence |
| 2026-03-24 | geo-strategy-15 | Homophone | "climatic battle" | climactic battle | "Climatic" = weather; "climactic" = decisive |
| 2026-03-24 | geo-strategy-15 | Foreign term | "misinic" / "imaging" / "mezanite" / "meant" calling | messianic calling | Core lecture concept; garbled 4 ways |
| 2026-03-24 | geo-strategy-16 | Proper name | "Libby the Roman historian" | Livy (Titus Livius) | Known Roman historian |
| 2026-03-24 | geo-strategy-16 | Proper name | "John Maynor kings" | John Maynard Keynes | Economist; garbled |
| 2026-03-24 | geo-strategy-16 | Domain vocab | "the tendable term for Christian Zionism" | technical term | Context: "the technical term is premillennial dispensationalist" |
| 2026-03-24 | geo-strategy-16 | Proper name | "Scoffield Bible" | Scofield Bible (one f) | C. I. Scofield's reference Bible |
| 2026-03-24 | geo-strategy-16 | Foreign term | "Zorastronism" | Zoroastrianism | Garble persists |
| 2026-03-24 | geo-strategy-17 | Proper name | "Nanyahu" | Netanyahu | Dropped syllable |
| 2026-03-24 | geo-strategy-17 | Domain vocab | "maintaining American hijgemony" | hegemony | Garble persists; fixed in geo-18/19 |
| 2026-03-24 | geo-strategy-17 | Fixed phrase | "possible deniability" (×2) | plausible deniability | Standard legal/strategy phrase |
| 2026-03-24 | geo-strategy-17 | Proper name | "K. Anders Ericson" | K. Anders Ericsson (double s) | Deliberate-practice researcher |
| 2026-03-24 | geo-strategy-17 | Proper name | "Neestoran Christianity" | Nestorian Christianity | Historical Christian sect |
| 2026-03-24 | geo-strategy-17 | Domain vocab | "synretatization" | syncretization | Religious-studies term |
| 2026-03-24 | geo-strategy-17 | Domain vocab | "mezzating age" | messianic age | Context makes meaning clear |
| 2026-03-24 | geo-strategy-17 | Homophone | "lentlessness" | landlessness | Speaker listing evils: "debt, slavery, lentlessness" |
| 2026-03-24 | geo-strategy-17 | Domain vocab | "controls the armoraments" | armaments | Military term garbled |
| 2026-03-24 | geo-strategy-18 | Proper name | "Bison Empire" (4+ locations) | Byzantine Empire | Inconsistent: curated has "Byzantine" in some lines, "Bison" in others |
| 2026-03-24 | geo-strategy-18 | Proper name | "Aragon of Turkey" | Erdoğan | Correctly fixed in geo-19 but not here |
| 2026-03-24 | geo-strategy-18 | Proper name | "Haga Sophia" | Hagia Sophia | Istanbul landmark |
| 2026-03-24 | geo-strategy-18 | Proper name | "Constantinopole" / "Consipole" / "Caranopole" | Constantinople | Correct in some curated lines, garbled in others |
| 2026-03-24 | geo-strategy-18 | Proper name | "Frederick Nichi" | Friedrich Nietzsche | Fixed in geo-17 but not here |
| 2026-03-24 | geo-strategy-18 | Foreign term | "his reproachment with the Orthodox Church" | rapprochement | French diplomatic term garbled |
| 2026-03-24 | geo-strategy-18 | Domain vocab | "encircumment of Odessa" | encirclement | Military term garbled |
| 2026-03-24 | geo-strategy-18 | Proper name | "like Lenin and Trosky" (2nd instance) | Trotsky | First instance fixed; second left garbled |
| 2026-03-24 | geo-strategy-19 | — | (no findings) | Episode thoroughly curated | All major ASR issues normalized |
| 2026-03-24 | geo-strategy-20 | Proper name | "James B. Calhoun" | John B. Calhoun | Researcher; curated fixed surname but kept wrong first name |
| 2026-03-24 | geo-strategy-20 | Editorial / attribution | "they work as **cheap** labor" | "they work as **slave** labor" | Raw clearly says "slave labor"; curated diverges; meaning-altering |

### Highest-impact patterns

- **Proper names** (~70% of findings): Soleimani, Netanyahu, Khamenei, Rumsfeld, Wolfowitz, Bretton Woods, Strait of Hormuz each garbled across multiple episodes.
- **Number errors** (order-of-magnitude): "45 million" for "4–5 million" (geo-10), "133%" for "13%" (geo-03), "$1 13 billion" for "$13 billion" (geo-08), "20120" for "2020" (geo-05, -07).
- **Meaning-altering substitutions**: "deification" for "de-Baathification" (geo-06, -13), "World War II" for "III" (geo-14), "strategic death" for "depth" (geo-13), "theism" for "deism" (geo-03, -11), "succeeded" for "seceded" (geo-11).
- **Cross-episode inconsistency**: geo-17/-18 less thoroughly curated than geo-19/-20 — same terms fixed in later episodes but garbled in earlier ones.
- **Geo-19 cleanest**: zero findings — thoroughly curated.
- **Geo-07 and geo-08 densest**: Iranian and ancient Greek proper names severely corrupted.

### Candidate recurring replacements

Terms that recur across 3+ episodes and are candidates for `asr_transcript_replacements.py` (common tier):

| Term | ASR variants | Episodes |
|------|-------------|----------|
| Strait of Hormuz | "humus", "homus", "Humus" | 01, 04, 07, 08, 13, 14 |
| Qasem Soleimani | "salamani", "salaman", "solomani", "salamini" | 01, 04, 07, 08 |
| Netanyahu | "nanyu", "Nanyahu", "Nan yahu", "natany", "Natanya" | 05, 08, 15, 17 |
| Hezbollah | "hesah", "heson" | 01, 04, 07 |
| Houthis / Yemen | "hthis", "hufi", "hoovies", "Yaman", "y man" | 01, 07 |
| de-Baathification | "deification", "debuffification", "deaf" | 06, 13 |
| AIPAC | "APAC" | 08 |
| MBS | "NBS" | 04, 08 |
| BRICS | "bricks", "breaks" | 10 |
| Bretton Woods | "Breton", "Brendon", "Bron", "bread and WT" | 03, 10 |
| Ayatollah | "Yatollah", "Aatollah", "Alatia", "Alatollah" | 14, 15 |
| Khamenei | "Kami", "CI", "camani", "kamani" | 07 |
| Zelenskyy | "zalinski", "zilinski", "zinsky" | 08 |
| Zoroastrianism | "Zorashinism", "Zorastronism" | 15, 16 |
| messianic | "misinic", "mezanite", "mezzating", "meant" | 15, 17 |
| Nikki Haley | "Niki Hill", "niiki Hy", "niiki heli", "Nikki Hy" | 05, 08, 11 |

---

## 5. Findings log — Secret History (Volume III)

**Date:** 2026-03-24 | **Scope (row-level table):** secret-history-01 through -04 only | **Depth:** B | **Normalization (SH01–04):** 62 substitutions via `normalize_lecture_transcript_asr.py --write`

**SH05–SH10 (verbatim complete; row log not expanded here):** Caption-faithful `## Full transcript` sections are present; `normalize_lecture_transcript_asr.py` dry-run reports **0** pending automated substitutions in the transcript section (2026-03-24). Targeted manual pass (proper names, numbers, risky homophones) completed per [ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md). Episodes: `secret-history-05-the-birth-of-evil.md` through `secret-history-10-the-conspiracy-of-evil.md`.

**SH11 (2026-03-24):** Verbatim YouTube transcript pasted into `secret-history-11-dawn-of-the-human-imagination.md`; manual ASR pass + **12** new `COMMON_REPLACEMENTS` tuples (vine→divine phrases, von Petzinger, Van Gogh, Micronesia, Darwinism/survival-of-fittest phrases, fear→theory of evolution marker); remaining fixes applied in-file (e.g. Altamira, Graeber/Wengrow, *The Dawn of Everything*, broad-scale/Paleolithic quote, Romito 2, nomadic societies). Dry-run normalizer: **0** pending substitutions; pytest green.

**SH12 (2026-03-24):** Verbatim transcript in `secret-history-12-heaven-on-earth.md`; **11** new `COMMON_REPLACEMENTS` tuples (synesthesia, primitive/fittish, Constantinople standing, Aachen Cathedral, Manhattan project, Euler, Turnbull, Wade Davis book title, succession crisis, Graeber/Wengrow *Dawn* phrase); heavy in-file fixes for Göbekli Tepe / Çatalhöyük / Karahan Tepe / Barasana / molimo / Amazon ethnography quotes. Dry-run normalizer: **0**; pytest green.

**SH13 (2026-03-24):** Verbatim transcript in `secret-history-13-mandate-of-heaven.md` (*Mandate of Heaven*); manual ASR pass for Sumer vs “Samaria,” Göbekli Tepe / Çatalhöyük, *Enuma Elish* / Gilgamesh / Marduk cluster, university joke (Middlebury), Mesopotamia geography, Hesiod / dynastic-cycle Q&A, and debate between sheep and grain; no new `COMMON_REPLACEMENTS` tuples (fixes in-file only). Dry-run normalizer: **0**; pytest green.

**SH14 (2026-03-24):** Verbatim operator-supplied transcript in `secret-history-14-legacy-of-the-steppes.md` (*Legacy of the Steppes*); initial normalizer `--write` **1** common-tier substitution; heavy in-file pass for **steppes** (ASR “steps”), Genghis Khan, Qin/Zhou/Spring and Autumn, Confucius/Laozi, Uruk, Indus Valley, Yamnaya/Proto-Indo-European/Indo-European cluster, Marija Gimbutas, David W. Anthony / *The Horse, the Wheel, and Language*, Xiongnu, Scythians/Medes, Timur, Mosuo, Romulus/Remus, guest-host / Männerbund, caste/Dravidian, and myth line (Trito/storm god); no new `COMMON_REPLACEMENTS` tuples (too many false-positive risks on “steps”). Dry-run normalizer after audit: **0**; pytest green.

**SH15 (2026-03-24):** Verbatim transcript in `secret-history-15-capital-and-the-bronze-age-collapse.md` (*Capital and the Bronze Age Collapse*); initial normalizer `--write` **3** common-tier substitutions; manual pass for Indus/Shang/Hittite/Mycenaean/Aegean/Uruk/Çatalhöyük/BMAC/Uluburun/Eric Cline *1177 B.C.*, proto-capitalism wording, altruism/utilitarianism, David Graeber, Atlantic/brain-scan block, Troy/Sea Peoples/Mesopotamia resilience, and Greek Dark Age → polis/Homer bridge; no new `COMMON_REPLACEMENTS` tuples (fixes in-file only). Dry-run normalizer after audit: **0**; pytest green.

**SH16 (2026-03-24):** Verbatim operator-supplied transcript in `secret-history-16-the-big-bang-of-greek-civilization.md` (*The Big Bang of Greek Civilization*); initial normalizer `--write` **2** common-tier substitutions (pre–manual pass); heavy in-file pass for Mycenaean/Aegean/polis/Linear B, alphabet/syllabary/ideogram, Trojan War cast (Agamemnon, Menelaus, Patroclus, Priam, Thetis, Odysseus), Fagles quotation blocks, Julian Jaynes / Kant / Hegel / Narby / Descartes, Anna Karenina / Tolstoy / Woolf, steppe/livestock comment block; no new `COMMON_REPLACEMENTS` tuples (fixes in-file only). Dry-run normalizer after audit: **0**; pytest green.

**SH17 (2026-03-24):** Verbatim operator-supplied transcript in `secret-history-17-literary-genesis.md` (*Literary Genesis*); normalizer dry-run **0** common-tier hits pre-audit; heavy in-file pass for Bronze Age / Levant / Aegean / Mycenaean / Canaan, Philistines, nomadic pastoralists, Sigmund Freud, Esau/Laban/Leah/Rachel, serpent/Eden diction, Sodom–Gomorrah negotiation quote, **Joab** vs ASR “Job,” Abner, Hebron, Rabbah, Bathsheba/Uriah/Hittite, Nathan parable, Tanakh/Torah structure, “hill people” vs “heal,” Uriah name cluster, cherubim/sword Eden exit; no new `COMMON_REPLACEMENTS` tuples (fixes in-file only; “Job”→Joab too context-dense for blind automation). Dry-run normalizer after audit: **0**; pytest green.

**SH18 (2026-03-24):** Verbatim operator-supplied transcript in `secret-history-18-thus-spoke-zarathustra.md` (*Thus Spoke Zarathustra*); initial normalizer `--write` **9** common-tier substitutions (pre–manual pass); heavy in-file pass for Zoroastrianism / Zarathustra / Ahura Mazda / Asha–druj, Achaemenid, Kant categorical imperative, Avestan/Gathas, Rumi, Nietzsche / *Thus Spoke Zarathustra* long quotation block, Bronze Age/mines, choir/cave metaphors; transcript ends mid-sentence (“I’ll see you guys next”) as pasted; no new `COMMON_REPLACEMENTS` tuples (fixes in-file only; Ahura Mazda vs “our master” context-sensitive). Dry-run normalizer after audit: **0**; pytest green.

**SH19 (2026-03-24):** Verbatim operator-supplied transcript in `secret-history-19-dawn-of-the-jews.md` (*Dawn of the Jews*); initial normalizer `--write` **2** common-tier substitutions (pre–manual pass); heavy in-file pass for Warring States / Qin vs ASR “Qing,” Uruk / Tigris–Euphrates, Lugalzagesi / Umma / Akkad / Sargon, Akkadian vs “Canadian,” Achaemenid vs “Academic,” Zoroastrianism cluster, Cyrus / Alexander / Artaxerxes, Ezra–Nehemiah / Zerubbabel / Babylonian royal names, Balfour / Rothschild, Yehud vs “Yahoo,” Levant homophones, divide-and-rule vs “divine rule,” biblical quote fixes (word of the Lord, freewill offerings, weeping), Sun Tzu attribution, *Der Judenstaat* / Theodor Herzl; no new `COMMON_REPLACEMENTS` tuples (fixes in-file only; geopolitical thesis wording preserved). Dry-run normalizer after audit: **0**; pytest green.

**SH20 (2026-03-24):** Verbatim operator-supplied transcript in `secret-history-20-the-hellenistic-world.md` (*The Hellenistic World*); initial normalizer `--write` **11** common-tier substitutions (pre–manual pass); heavy in-file pass for Warring States / Qin / Zhao–Wei–Chu (avoid false “the way” → Wei), Uruk, Lugalzagesi, Akkad, hoplites / helots / polis, Thebes vs “thieves,” Peloponnesian War, Thermopylae / Salamis / Plataea, Themistocles, Herodotus, Mardonius / Pausanias quotes, Delian League / Parthenon, Thucydides / Pericles / Melian dialogue excerpt, Philip II / Chaeronea / phalanx, Alexander / Persepolis / Thebes / Siwa (Zeus-Ammon), Diadochi (Ptolemy / Seleucid), Plato vs Aristotle (telos, prime mover), Library of Alexandria / Mouseion / Septuagint, syncretism; careful repair where blind “the way” replacements broke sentences; no new `COMMON_REPLACEMENTS` tuples (fixes in-file only). Dry-run normalizer after audit: **0**; pytest green.

**SH21 (2026-03-24):** Verbatim operator-supplied transcript in `secret-history-21-roman-anti-civilization.md` (*Roman Anti-Civilization*); initial normalizer `--write` **4** common-tier substitutions (pre–manual pass); heavy in-file pass for Bronze Age / Etruscan / Magna Graecia, hoplites / legions / legionaries, Pyrrhus / Epirus / Italy sail, Punic Wars, Trebia / Trasimene / Cannae ASR variants (“canal,” “Kaine,” “canine”), Hannibal Barca, Polybius vs Livy (Augustus commissions Livy), optimates / populares, grain dole, Social War, Tiberius Gracchus, Marius / Sulla, Alesia / Gallic tribes, Caesar / Pompey / Pharsalus / Actium, Aeneas / Creusa, Romulus / Remus, rape of the Sabines, Lucretia / Collatinus / Tarquin / Brutus / Mucius Scaevola, *Aeneid* / Virgil block (Priam / Polites / Pyrrhus / Neoptolemus; Euripides *Trojan Women*), Q&A names; thesis wording and skepticism preserved; no new `COMMON_REPLACEMENTS` tuples (fixes in-file only). Dry-run normalizer after audit: **0**; pytest green.

**SH22–28:** `## Full transcript` is still the **analytical lecture-arc stub** where not yet pasted. **Next operator action:** replace stub with YouTube verbatim text → run normalizer `--write` → audit → extend `COMMON_REPLACEMENTS` only for safe patterns → pytest.

**Raw captions:** Available under `research/external/youtube-channels/predictive-history/transcripts/` for all 28 Secret History video IDs (verify with `check_asr_audit_preconditions.py --only-glob 'secret-history-*' -v`).

| Date | Lecture file | Signal type | Before (short) | After / fix | Verified how |
|------|--------------|-------------|------------------|-------------|--------------|
| 2026-03-24 | secret-history-01 | Proper name | "Emmanuel Kant" / "Emanuel K" | Immanuel Kant | Known philosopher; ASR garbles first name |
| 2026-03-24 | secret-history-01 | Domain vocab | "the nomina" / "the nomena" | the noumena | Kantian philosophy; ASR phonetic collapse |
| 2026-03-24 | secret-history-01 | Domain vocab | "the polyphasic system" | the polytheistic system | Context: religious systems comparison |
| 2026-03-24 | secret-history-01 | Domain vocab | "three great monophasic religions" | three great monotheistic religions | Context: Abrahamic religions |
| 2026-03-24 | secret-history-01 | Domain vocab | "montheism" / "monetism" (×4) | monotheism | Recurring across SH01-02 |
| 2026-03-24 | secret-history-01 | Proper name | "Dianesis" | Dionysus | Greek god |
| 2026-03-24 | secret-history-01 | Proper name | "Edypus" | Oedipus | Greek mythological figure |
| 2026-03-24 | secret-history-01 | Foreign term | "udeimmonia" / "Youmonia" / "ulmonia" | eudaimonia | Greek philosophical term; 3 garbled forms |
| 2026-03-24 | secret-history-01 | Domain vocab | "analyical model" (×3) | analytical model | Recurring garble |
| 2026-03-24 | secret-history-01 | Domain vocab | "fraction reserve" | fractional reserve | Banking/economics term |
| 2026-03-24 | secret-history-01 | Proper name | "Azteex" | Aztecs | Civilization name |
| 2026-03-24 | secret-history-02 | Proper name | "Thomas Pikid Pikid" / "Pikody" | Thomas Piketty | Economist |
| 2026-03-24 | secret-history-02 | Proper name | "Oswalt Spangler" / "Oswald Spangler" | Oswald Spengler | Historian; surname garbled |
| 2026-03-24 | secret-history-02 | Domain vocab | "metocratic" | meritocratic | Political term |
| 2026-03-24 | secret-history-02 | Domain vocab | "elite overp production" | elite overproduction | Turchin's concept |
| 2026-03-24 | secret-history-02 | Foreign term | "petty boujo" | petty bourgeoisie | French term garbled |
| 2026-03-24 | secret-history-02 | Proper name | "Cahoun" | Calhoun | John B. Calhoun; rat utopia |
| 2026-03-24 | secret-history-03 | Proper name | "Dian Feinstein" | Dianne Feinstein | US Senator |
| 2026-03-24 | secret-history-03 | Domain vocab | "Euphania" / "Euthan Asia" / "insunasia" / "insunia" (×5+) | euthanasia | Classic ASR error; many garbled forms |
| 2026-03-24 | secret-history-03 | Domain vocab | "moratorum" | moratorium | Policy term |
| 2026-03-24 | secret-history-03 | Domain vocab | "healthare" | healthcare | Typo-class garble |
| 2026-03-24 | secret-history-03 | Domain vocab | "rebellous" | rebellious | Adjective garble |
| 2026-03-24 | secret-history-04 | Proper name | "phoenetians" / "Infineticians" | Phoenicians | Ancient people; 2 garbled forms |
| 2026-03-24 | secret-history-04 | Proper name | "constant genians" | Carthaginians | Ancient people |
| 2026-03-24 | secret-history-04 | Proper name | "Leonitis" (×2) | Leonidas | Spartan king |
| 2026-03-24 | secret-history-04 | Proper name | "Heggo" / "Hego" | Hegel | Philosopher |
| 2026-03-24 | secret-history-04 | Proper name | "Frederick Hegel" | Friedrich Hegel | First name garbled |
| 2026-03-24 | secret-history-04 | Proper name | "Dantain" | Dante | Poet/philosopher |
| 2026-03-24 | secret-history-04 | Place name | "Thermopily" | Thermopylae | Battle site |
| 2026-03-24 | secret-history-04 | Domain vocab | "Nostism" | Gnosticism | Religious/philosophical movement |
| 2026-03-24 | secret-history-04 | Domain vocab | "synchronosity" (×3) | synchronicity | Jungian term |
| 2026-03-24 | secret-history-04 | Domain vocab | "diads" | dyads | Philosophical pairs |
| 2026-03-24 | secret-history-11 | Homophone / theology | "the vine" (×10+ in ASR) | the divine | ASR systematic; Q&A "connected to the vine" |
| 2026-03-24 | secret-history-11 | Proper name | "Genevie von Piter" | Genevieve von Petzinger | Archaeologist |
| 2026-03-24 | secret-history-11 | Proper name | "Ventang go" | Van Gogh | Painter |
| 2026-03-24 | secret-history-11 | Place | "Micronia" | Micronesia | Pacific islands |
| 2026-03-24 | secret-history-11 | Domain vocab | "Darism" / "surround the fittest" | Darwinism / survival of the fittest | Lecture register |
| 2026-03-24 | secret-history-11 | Phrase | "the fear of evolution marked" | the theory of evolution marked | Turning-point sentence |
| 2026-03-24 | secret-history-11 | Book / authors | "David Grabber and David Wangro" / "that done everything" | David Graeber and David Wengrow / *The Dawn of Everything* | Burial-care quote |
| 2026-03-24 | secret-history-11 | Quote fix | "balance appraisals" / "huntergather" / "p paleothic" | broad-scale appraisals / hunter-gatherer / Paleolithic | Aligns with published wording |
| 2026-03-24 | secret-history-11 | Archaeology | "Roma 2" / "bureau site" | Romito 2 / burial site | Ice Age dwarf burial |
| 2026-03-24 | secret-history-12 | ASR | "symphysicia" | synesthesia | Mixed senses; Beethoven |
| 2026-03-24 | secret-history-12 | ASR / sites | "K paintings" / "go tepe" / "Kak Hoyak" / "Katak" | cave paintings / Göbekli Tepe / Çatalhöyük | Site names |
| 2026-03-24 | secret-history-12 | ASR | "serial computer" (Pacific Q&A) | in a boat in the Pacific | Rebuts student; context |
| 2026-03-24 | secret-history-12 | ASR | "Kenapole" / "still instant" | Constantinople / still standing | Hagia Sophia |
| 2026-03-24 | secret-history-12 | ASR | "Minute Manhattan project" | The Manhattan project | 20th-c. nuclear program |
| 2026-03-24 | secret-history-12 | ASR | "Leonard Uler" / "Colin Turbo" | Leonhard Euler / Colin Turnbull | Names |
| 2026-03-24 | secret-history-12 | Book / quote | "thought of everything" / Grabber/Wangro | *The Dawn of Everything* / Graeber & Wengrow | Intro to ethnography block |
| 2026-03-24 | secret-history-12 | ASR | "rice rivers" (Barasana myth) | rise to rivers | Creation narrative |
| 2026-03-24 | secret-history-13 | ASR / place | "Samaria" (×many) / duplicate Sumer | Sumer | Map + trade-hub context; ASR homophone |
| 2026-03-24 | secret-history-13 | ASR | "Marist" / "Mesopotain" / "Mesopotania" / "emir lash" | Middlebury / Mesopotamia / Mesopotamia / Enuma Elish | Lecture joke + two epics |
| 2026-03-24 | secret-history-13 | Mythology | "Uranus marries Ria" | Cronus marries Rhea | Hesiod / Theogony narrative |
| 2026-03-24 | secret-history-13 | ASR | "Aadian Empire" / "found the" | Akkadian Empire / founded the | Sargon |
| 2026-03-24 | secret-history-13 | ASR | "monarch here" / "King Mard " | Marduk / King Marduk | *Enuma Elish* block |
| 2026-03-24 | secret-history-15 | ASR / place | "Indis" / "Inis Valley" / "Shan dynasty" | Indus / Indus Valley / Shang dynasty | Bronze Age map + China |
| 2026-03-24 | secret-history-15 | ASR / ancient | "Masonia" / "Msian" / "Minian" / "Elo Bun" | Mycenae / Mycenaean / Uluburun | Aegean + shipwreck |
| 2026-03-24 | secret-history-15 | ASR / book | "Eric Klein" / "17 1177" | Eric Cline / *1177 B.C.* | Collapse scholarship |
| 2026-03-24 | secret-history-15 | ASR / site | "Kak Hoyak" / "Katy Hoyek" / "Bmac" | Çatalhöyük / BMAC | Comparative archaeology |
| 2026-03-24 | secret-history-15 | ASR / period | "branch" / "branches" (metal) | bronze / Bronze Age | Homophone cluster |
| 2026-03-24 | secret-history-15 | ASR / magazine | "Atletic Monthly" / "brain scandals" | *The Atlantic* / (brain scans) | Modern analogy block |
| 2026-03-24 | secret-history-14 | ASR / geography | "steps" / "steps people" | steppes / steppe peoples | Systematic caption error |
| 2026-03-24 | secret-history-14 | ASR / history | "Genghask Khan" / "theQing" / "chunu" | Genghis Khan / Qin / Chunqiu | Names + periods |
| 2026-03-24 | secret-history-14 | ASR / PIE | "Yamaya" / "Indo-Uropean" / "Shunu" | Yamnaya / Indo-European / Xiongnu | Linguistics + frontier |
| 2026-03-24 | secret-history-14 | Book / scholar | "Will and Language" / "Harvard" / "Morabon" | *Wheel, and Language* / Anthony / Männerbund | Anthony + kinship term |
| 2026-03-24 | secret-history-14 | ASR / myth | "Ramlas" / "Third men" / storm. Got | Romulus / Trito / storm god | Roman + PIE myth |
| 2026-03-24 | secret-history-16 | ASR / Greek | "Eggman" / "Minanian" / "AGNC" / "polus" | Agamemnon / Mycenaean / Aegean / polis | High-frequency name garbles |
| 2026-03-24 | secret-history-16 | ASR / epic | "Petroles" / "Prime" / "Pry" / "Fetus" | Patroclus / Priam / Priam / Thetis | Iliad cast |
| 2026-03-24 | secret-history-16 | ASR / scholar | "Julian James" / "bicchimeal" / "Jurian Narby" | Julian Jaynes / bicameral / Jeremy Narby | Consciousness block |
| 2026-03-24 | secret-history-16 | ASR / novelists | "Anakarina" / "Toy Stoy" / "Virginia Wolf" | Anna Karenina / Tolstoy / Woolf | Modern lit coda |
| 2026-03-24 | secret-history-17 | ASR / proper | "Simon Freud" / "Leavant" / "Canine" / "Minian" | Sigmund Freud / Levant / Canaan / Mycenaean | Geography + figures |
| 2026-03-24 | secret-history-17 | ASR / biblical | "Job" (David’s general) / "Amnner" / "Bash Sheba" / "Uria" | Joab / Abner / Bathsheba / Uriah | David narrative cluster |
| 2026-03-24 | secret-history-17 | ASR / phrase | "roasted from the couch" / "reverenc the Ammonites" | rose from the couch / advanced against the Ammonites | Bathsheba scene |
| 2026-03-24 | secret-history-18 | ASR / religion | "Zorashinism" / "Persian Aid" / "montheism" | Zoroastrianism / Achaemenid / monotheism | Core terms |
| 2026-03-24 | secret-history-18 | ASR / names | "Roomie" / "Nichi" / "Zorusta" | Rumi / Nietzsche / Zarathustra | High-frequency garbles |
| 2026-03-24 | secret-history-18 | ASR / philosophy | "noose" / "monatic" / "category imperative" | nous / monad is / categorical imperative | Cosmology + Kant |
| 2026-03-24 | secret-history-19 | ASR / China | "theQing" / "waring states" / "Qin empire" | Qin / warring states / Qin | Map period; systematic ASR |
| 2026-03-24 | secret-history-19 | ASR / Mesopotamia | "Uric" / "Canadian Empire" / "Luga Luga Zagazi" | Uruk / Akkadian Empire / Lugalzagesi | Geography + empire names |
| 2026-03-24 | secret-history-19 | ASR / Persia | "Persian Academic" / "Zoroastronism" / "Syus" / "Action the Great" | Achaemenid / Zoroastrianism / Cyrus / Alexander | High-frequency |
| 2026-03-24 | secret-history-19 | ASR / Bible–politics | "Balfford" / "Rothst" / "province of Yahoo" | Balfour / Rothschild / Yehud | Modern parallel + province |
| 2026-03-24 | secret-history-19 | Phrase / grammar | "divine rule" (imperial strategy) | divide-and-rule | Homophone in lecture argument |
| 2026-03-24 | secret-history-19 | ASR / misc | "right atmosphere" / "esquetological" / "nation stones" | right hemisphere / eschatological / nation states | Q&A + method terms |
| 2026-03-24 | secret-history-20 | ASR / China | "theQing" / "waring" / "jou way chew" | Qin / warring / Zhao, Wei, Chu | Systematic; watch "the way" → Wei false positives |
| 2026-03-24 | secret-history-20 | ASR / Greece | "thieves" / "Pelpedian" / "Fezicles" | Thebes / Peloponnesian / Themistocles | High-frequency |
| 2026-03-24 | secret-history-20 | ASR / battles | "Ferupi" / "Salamus" / "Palia" | Thermopylae / Salamis / Plataea | Persian Wars cluster |
| 2026-03-24 | secret-history-20 | ASR / names | "fusidities" / "Parthonon" / "Sherania" | Thucydides / Parthenon / Chaeronea | Empire + war narrative |
| 2026-03-24 | secret-history-20 | ASR / philosophy | "tilos" / "Decart" / "empiricis" | telos / Descartes / empiricism | Plato–Aristotle block |
| 2026-03-24 | secret-history-20 | ASR / Hellenistic | "Henistic" / "Septuagent" / "Tommy" (Ptolemy) | Hellenistic / Septuagint / Ptolemy | Successor + library |
| 2026-03-24 | secret-history-21 | ASR / Rome | "Brontage" / "truskin" / "Atrusian" / "marinian" | Bronze Age / Etruscan / Etruscan / Magna Graecia | Opening geography |
| 2026-03-24 | secret-history-21 | ASR / battles | "Trivia" / "Tresamine" / "Kaine" / "canal" / "canine" | Trebia / Trasimene / Cannae / Cannae / Cannae | Hannibal campaign cluster |
| 2026-03-24 | secret-history-21 | ASR / names | "Palibius" / "Palibus" / "Libby" (historian) | Polybius / Polybius / Livy | Greek vs Roman lens; commission |
| 2026-03-24 | secret-history-21 | ASR / civil war | "Solo" / "Solah" / "Farcus" / "farceless" / "Ottomates" / "Pompei" | Sulla / Sulla / Pharsalus / Pharsalus / optimates / Pompey | Late Republic |
| 2026-03-24 | secret-history-21 | ASR / Gaul | "Alicia" / "gic tribes" | Alesia / Gallic | Caesar campaign |
| 2026-03-24 | secret-history-21 | ASR / myth | "Inas" / "Kisha" / "Lucricia" / "Kentinius" / "Buddhist" (Brutus) | Aeneas / Creusa / Lucretia / Collatinus / Brutus | Foundation myths |
| 2026-03-24 | secret-history-21 | ASR / *Aeneid* | "Prime" / "Pry" / "Iniad" | Priam / Priam / Aeneid | Virgil quotation block |

### Secret History highest-impact patterns

- **Philosophical vocabulary** (~40% of findings): noumena, eudaimonia, Gnosticism, synchronicity, monotheism, polytheistic — ASR struggles with Greek/Latin philosophical terms.
- **Proper names** (~35%): Kant, Spengler, Piketty, Hegel, Dante, Leonidas, Phoenicians, Carthaginians — similar to geo-strategy and civilization patterns.
- **Medical/policy terms** (~15%): euthanasia (5+ garbled forms in SH03 alone), moratorium, healthcare.
- **SH04 densest:** 24 substitutions — heavy philosophical and ancient Greek content.
- **SH01 second densest:** 16 substitutions — Kant, eudaimonia, monotheism cluster.

### Secret History candidate replacements

SH01–04: 62 automated substitutions via 53 entries (2026-03-24). SH11: +12 `COMMON_REPLACEMENTS` tuples (vine/divine phrases, Petzinger, Van Gogh, Micronesia, Darwin phrases). SH12: +11 tuples. SH13: in-file only (no new tuples). SH14: in-file only (no new tuples; “steps”→steppes not automated). SH15: in-file only (no new tuples). SH16: in-file only (no new tuples; Greek epic name density too high for blind automation). SH17: in-file only (no new tuples; “Job”→Joab and Uriah clusters too context-sensitive for blind automation). SH18: in-file only (no new tuples; Ahura Mazda / Zarathustra string density too high for blind automation). SH19: in-file only (no new tuples; Qin/Qing and Levant/Biblical proper-name density too high for blind automation). SH20: in-file only (no new tuples; “the way” vs Wei / Thebes vs thieves too context-sensitive for blind automation). SH21: in-file only (no new tuples; Cannae/historian-name homophones and Livy quotation density too high for blind automation). All common tier; no secret-history-specific tier.

**Not automated (too risky for string replacement):**

| Term | ASR form(s) | Why skipped |
|------|------------|-------------|
| monad | "nomad", "Mona", "Monet", "Monach" | Real English words; would cause false positives |
| Geist | "gist", "guys" | Real English words |
| nous | "news" | Real English word |
| Kant | "Kai" | Real name |
| Dante | "Donna", "Donnie" | Real names |
| divine sun | "divine son" | Both are valid phrases; context-dependent |

### Secret History scope limitation

**SH22–SH28:** Where not yet pasted, `## Full transcript` sections may still contain operator-written **lecture-arc analytical summaries** (structured outlines, bullet-point core claims) — not verbatim ASR-derived text — until pasted. When each file is replaced with pasted caption text, re-run the pipeline (normalizer → manual audit → replacements → pytest).

---

## 6. Commands reference

```bash
# Tests
pytest tests/test_normalize_lecture_transcript_asr.py -q

# Coverage (lectures with YouTube URL vs raw .txt)
python3 scripts/work_jiang/check_asr_audit_preconditions.py
python3 scripts/work_jiang/check_asr_audit_preconditions.py --only-glob 'geo-strategy-*'
python3 scripts/work_jiang/check_asr_audit_preconditions.py --only-glob 'secret-history-*'
python3 scripts/work_jiang/check_asr_audit_preconditions.py --strict   # exit 1 if gaps

# Verbatim layer (example: Geo-Strategy)
python3 scripts/work_jiang/sync_verbatim_transcripts.py --dry-run --only-glob 'geo-strategy-*'
python3 scripts/work_jiang/sync_verbatim_transcripts.py --write --only-glob 'geo-strategy-*'
```

---

## Related

- [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md) — layers and Phase B verbatim step  
- [ASR-VERIFICATION-RUBRIC.md](ASR-VERIFICATION-RUBRIC.md) — epistemic levels and when timestamps/captions are required  
