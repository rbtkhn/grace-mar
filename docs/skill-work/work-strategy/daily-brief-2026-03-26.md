# Daily brief — work-politics & work-strategy

**Date:** 2026-03-26  
**Assembled:** 2026-03-26 19:12 UTC  
**Recency window (RSS):** last **36h** (undated items may appear)  
**Config:** `docs/skill-work/work-strategy/daily-brief-config.json`

_Operator WORK product. Complete synthesis below; cite sources before any public use._

## 1. Work-politics snapshot

- **Primary:** May 19, 2026 — **days until:** 53
- **Work-politics gate:** 0 pending candidate(s)

### Upcoming (from calendar)

- ****Apr 20, 2026**** — **Voter registration deadline** (in-person and mail; mail = postmark) — Push registration in-district; remind supporters.
- ****May 5, 2026**** — Mail-in absentee ballot request portal closes — Voters who need absentee must request by this date.
- ****May 7, 2026**** — **FEC pre-primary report due** — Covers period Apr 1–Apr 29. Registration/certification & overnight mail deadline May 4.
- ****May 19, 2026**** — **Primary election day** — Polls open; final GOTV.

### Territory signals (from docs)

- **freshness:** Principal profile may be stale
- **research_gap:** Opposition brief still has placeholder sections
- **gate_rhythm:** No live work-politics candidates in RECURSION-GATE
- **brief_readiness:** Weekly brief sources are not fully ready

## 1b. Work-strategy focus

_From `docs/skill-work/work-strategy/daily-brief-focus.md` § Active focus._

- Campaign/companion positioning: portable Record, human-only merge, Voice boundary.
- OpenClaw ↔ repo handback and export provenance (see [work-dev workspace](../work-dev/workspace.md)).
- AI-in-schools and identity-substrate narrative vs Alpha-style bundles (see [work-alpha-school](../work-alpha-school/README.md), [work-dev offers](../work-dev/offers.md)).
- Optional: federal / state AI governance headlines when relevant to offers or civ-mem work.
- Long-form tech discourse (GTC-class, Moonshots-class): themes distilled in [external-tech-scan.md](external-tech-scan.md) — use for **strategy vocabulary** and **keyword-season** tuning in [daily-brief-config.json](daily-brief-config.json); **not** unsourced brief facts.

_Product / integration context: [work-dev/workspace.md](../work-dev/workspace.md), [work-strategy/README.md](../../work-strategy/README.md)._

## 2. Headlines (ingested RSS)

_Fetch failed for: Reuters — World._

Ranked by **W+S+G** (global keyword lists + per-`locale` maps for W/S; **G** = `geo_military_keyword_phrases`) then recency. Each feed is **recency-sorted** then **capped** (`ingest_caps`: per-feed `max_items` and/or `tier` → `max_items_by_tier`; CLI `--max-per-feed N` overrides all feeds). Optional **same-story** grouping uses `story_anchor_phrases` overlap (Jaccard + shared anchors). Tune phrases in config JSON.

_Same-story clusters use anchor overlap on titles (proper nouns / crisis terms); not neural / semantic dedupe._

#### Same-story (multilingual)

**congress · iran · israel · trump** — _8 sources_

- **[W:3 S:1 G:1]** [Tensions flare during Iran briefing on Capitol Hill over lack of clarity on Trump's strategy](https://www.nbcnews.com/politics/congress/tensions-flare-iran-briefing-lawmakers-trump-officials-ground-troops-rcna265231) — _NBC News — politics_ · _2026-03-26 02:16 UTC_
- **Also** — [Republicans launch new party-line bill for ICE, Iran war funding and election laws](https://www.nbcnews.com/politics/congress/republicans-launch-reconciliation-america-act-iran-war-ice-rcna265091) — _NBC News — politics_ · _W:4 S:0 G:0_ · _2026-03-25 18:08 UTC_
- **Also** — [Iran rejects U.S. peace plan. And, jury finds Meta, Google to blame in addiction trial](https://www.npr.org/2026/03/26/g-s1-115289/up-first-newsletter-iran-israel-trump-meta-google-social-media-cdc-director) — _NPR — national news_ · _W:3 S:0 G:0_ · _2026-03-26 07:16 UTC_
- **Also** — [5 takeaways from Trump’s Cabinet meeting as Iran war wages](https://thehill.com/homenews/5802654-trump-cabinet-meeting-iran-war/) — _The Hill — politics_ · _W:2 S:0 G:0_ · _2026-03-26 17:52 UTC_
- **Also** — [Trump says the 'present' from Iran was 'eight big boats of oil'](https://www.nbcnews.com/now/video/trump-says-the-present-from-iran-was-eight-big-boats-of-oil-260115013831) — _NBC News — politics_ · _W:2 S:0 G:0_ · _2026-03-26 15:59 UTC_

#### Other headlines

- **[W:6 S:0 G:0]** [EN DIRECT, guerre en Ukraine : tandis que le président ukrainien Zelensky est en Arabie saoudite, le ministre des affaires étrangères russe, Sergueï Lavrov, accordera une interview au « 20 heures » de France 2](https://www.lemonde.fr/international/live/2026/03/26/en-direct-guerre-en-ukraine-tandis-que-le-president-ukrainien-zelensky-est-en-arabie-saoudite-le-ministre-des-affaires-etrangeres-russe-serguei-lavrov-accordera-une-interview-au-20-heures-de-france-2_6673450_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-03-26 19:47 UTC_
- **[W:4 S:0 G:0]** [Iran-News heute: Berichte über US-Pläne eines »finalen Schlags« – was steckt dahinter?](https://www.spiegel.de/ausland/iran-news-heute-teheran-will-laut-abbas-araghchi-keine-verhandlungen-mit-den-usa-a-61992055-24e6-44f3-b39c-e65d3e25099e#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-03-26 18:44 UTC_
- **[W:4 S:0 G:0]** [El rechazo de Irán a dialogar con EE.UU. refleja una profunda desconfianza en Trump](https://www.bbc.com/mundo/articles/cx2eqd4vv4wo?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-03-26 12:15 UTC_
- **[W:1 S:1 G:2]** [Lessons from Ukraine are shaping US Army's drones, training, comms](https://www.defenseone.com/defense-systems/2026/03/army-needs-more-realistic-drone-training-more-versatile-drones/412389/) — _Defense One — All_ · _2026-03-25 19:33 UTC_
- **[W:3 S:0 G:0]** [Mohamed El-Erian zum Irankrieg: »Der Geist der Inflation ist aus der Flasche«](https://www.spiegel.de/wirtschaft/iran-krieg-folgen-der-geist-der-inflation-ist-aus-der-flasche-a-dfcdd9b4-f07f-4cc5-8cc0-060c29874407#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-03-26 20:06 UTC_
- **[W:3 S:0 G:0]** [Rationing power and diluting petrol - how African countries are coping with effects of Iran war](https://www.bbc.com/news/articles/cq8wkq1n9epo?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-26 17:57 UTC_
- **[W:3 S:0 G:0]** [دول تشجع واشنطن وتل أبيب على مواصلة الحرب ضد إيران.. ما موقف دول الخليج العربي؟](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260326-%D8%AF%D9%88%D9%84-%D8%AA%D8%B4%D8%AC%D8%B9-%D9%88%D8%A7%D8%B4%D9%86%D8%B7%D9%86-%D9%88%D8%AA%D9%84-%D8%A3%D8%A8%D9%8A%D8%A8-%D8%B9%D9%84%D9%89-%D9%85%D9%88%D8%A7%D8%B5%D9%84%D8%A9-%D8%A7%D9%84%D8%AD%D8%B1%D8%A8-%D8%B6%D8%AF-%D8%A5%D9%8A%D8%B1%D8%A7%D9%86-%D9%85%D8%A7-%D9%85%D9%88%D9%82%D9%81-%D8%AF%D9%88%D9%84-%D8%A7%D9%84%D8%AE%D9%84%D9%8A%D8%AC-%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A) — _France 24 — العربية (MENA)_ · _ar_ · _2026-03-26 16:07 UTC_
- **[W:3 S:0 G:0]** [Russia bans Oscar-winning film 'Mr Nobody Against Putin'](https://www.bbc.com/news/articles/cly97ddwgeko?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-26 13:18 UTC_
- **[W:3 S:0 G:0]** [Cómo China se preparó durante años para una crisis de petróleo mundial y cuál es su punto débil](https://www.bbc.com/mundo/articles/c3w3e840x8qo?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-03-26 10:39 UTC_
- **[W:2 S:1 G:0]** [US prosecutors argue Maduro 'plundered' Venezuelan wealth in court battle over legal fees](https://www.bbc.com/news/articles/c4g8wxyq7v5o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-26 18:49 UTC_
- **[W:2 S:0 G:1]** [Zelensky visits Saudi Arabia after offering Ukraine's drone expertise](https://www.bbc.com/news/articles/cx2r4wxdw3no?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-26 18:24 UTC_
- **[W:2 S:0 G:1]** [Senators request two companies preserve communications with Corey Lewandowski](https://www.nbcnews.com/politics/trump-administration/democratic-senators-want-two-companies-preserve-communications-corey-l-rcna265152) — _NBC News — politics_ · _2026-03-25 20:54 UTC_
- **[W:0 S:0 G:3]** [The Army wants to use bullets, mortars, and artillery to take out small drones](https://www.defenseone.com/technology/2026/03/army-wants-use-bullets-mortars-and-artillery-rounds-take-out-small-drones/412392/) — _Defense One — All_ · _2026-03-26 03:41 UTC_
- **[W:2 S:0 G:0]** [Watch live: Trump gives remarks at Greek Independence Day celebration](https://thehill.com/video-clips/5802716-greek-independence-white-house/) — _The Hill — politics_ · _2026-03-26 18:55 UTC_
- **[W:2 S:0 G:0]** [Trump expected to announce action to solve TSA problems amid DHS shutdown](https://thehill.com/homenews/senate/5802813-gop-trump-tsa-executive-action/) — _The Hill — politics_ · _2026-03-26 18:42 UTC_

## 2a. Geopolitical & military (G-ranked)

_**G** = matches on `geo_military_keyword_phrases` (+ optional locale lists in config). Supports triangulation and war-powers messaging — **verify** claims against primary sources._

- **[W:0 S:0 G:3]** [The Army wants to use bullets, mortars, and artillery to take out small drones](https://www.defenseone.com/technology/2026/03/army-wants-use-bullets-mortars-and-artillery-rounds-take-out-small-drones/412392/) — _Defense One — All_ · _2026-03-26 03:41 UTC_
- **[W:1 S:1 G:2]** [Lessons from Ukraine are shaping US Army's drones, training, comms](https://www.defenseone.com/defense-systems/2026/03/army-needs-more-realistic-drone-training-more-versatile-drones/412389/) — _Defense One — All_ · _2026-03-25 19:33 UTC_
- **[W:3 S:1 G:1]** [Tensions flare during Iran briefing on Capitol Hill over lack of clarity on Trump's strategy](https://www.nbcnews.com/politics/congress/tensions-flare-iran-briefing-lawmakers-trump-officials-ground-troops-rcna265231) — _NBC News — politics_ · _2026-03-26 02:16 UTC_
- **[W:2 S:0 G:1]** [Zelensky visits Saudi Arabia after offering Ukraine's drone expertise](https://www.bbc.com/news/articles/cx2r4wxdw3no?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-26 18:24 UTC_
- **[W:2 S:0 G:1]** [Senators request two companies preserve communications with Corey Lewandowski](https://www.nbcnews.com/politics/trump-administration/democratic-senators-want-two-companies-preserve-communications-corey-l-rcna265152) — _NBC News — politics_ · _2026-03-25 20:54 UTC_
- **[W:0 S:0 G:1]** [Sydney Sweeney reveals younger brother deployed overseas, thanks troops](https://thehill.com/homenews/5802533-sydney-sweeney-reveals-younger-brother-deployed-overseas-thanks-troops/) — _The Hill — politics_ · _2026-03-26 18:53 UTC_
- **[W:0 S:0 G:1]** [‘We’ll go 40%’: Army wants good-enough tech it can reshape for battle](https://www.defenseone.com/defense-systems/2026/03/army-good-tech-battle/412402/) — _Defense One — All_ · _2026-03-26 12:31 UTC_
- **[W:0 S:0 G:1]** [The real danger of military AI isn’t killer robots; it’s worse human judgement](https://www.defenseone.com/technology/2026/03/military-ai-troops-judgement/412390/) — _Defense One — All_ · _2026-03-25 21:48 UTC_
- **[W:0 S:0 G:1]** [Defense Business Brief: Pentagon equity stakes FTW?; Hill & Valley Forum takeaways; plus a bit more](https://www.defenseone.com/business/2026/03/defense-business-brief-pentagon-equity-stakes-ftw-hill-valley-forum-takeaways-plus-bit-more/412365/) — _Defense One — All_ · _2026-03-25 13:00 UTC_

## 2b. Civ-mem depth hooks (in-repo essays — not breaking news)

_Token overlap against `docs/civilization-memory/` (build: `python3 scripts/build_civmem_inrepo_index.py build`). **Historical / structural** depth only — not a substitute for dated news. See [civ-mem-draft-protocol](../work-politics/civ-mem-draft-protocol.md). Public copy still needs human approval._

- **{CMC: `minds/CIV–MIND–MEARSHEIMER.md`}** (overlap 2) — _CIV–MIND–MEARSHEIMER — v3.4 Civilizational Memory Codex · Advisory Mind John J. Mearsheimer Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture Status: ACTIVE · CANONICAL · LOCKED Class: MIND (ADVIS..._
- **{CMC: `minds/CIV–MIND–MERCOURIS.md`}** (overlap 2) — _CIV–MIND–MERCOURIS — v3.4 Civilizational Memory Codex · Primary Mind Alexander Mercouris Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture · Proportional Blend Law Status: ACTIVE · CANONICAL · LOC..._
- **{CMC: `notes/civ-mem-state-vs-scholar.md`}** (overlap 2) — _**Purpose:** Clarify the distinction between **STATE** and **SCHOLAR** in the civilization_memory (CMC) model. These are internal operating modes of the *upstream* CMC system (e.g. `research/repos/civilization_memory`..._

## 3. Lead themes (auto-stub — replace after reading)

### Work-politics / campaign angle
- EN DIRECT, guerre en Ukraine : tandis que le président ukrainien Zelensky est en Arabie saoudite, le ministre des affaires étrangères russe, Sergueï Lavrov, accordera une interview au « 20 heures » de France 2
- Iran-News heute: Berichte über US-Pläne eines »finalen Schlags« – was steckt dahinter?
- El rechazo de Irán a dialogar con EE.UU. refleja una profunda desconfianza en Trump

**Replace:** 2–3 sentences for principal, district, opposition narrative.

### Work-strategy angle (product / governance / tech)

- Tensions flare during Iran briefing on Capitol Hill over lack of clarity on Trump's strategy
- Lessons from Ukraine are shaping US Army's drones, training, comms
- US prosecutors argue Maduro 'plundered' Venezuelan wealth in court battle over legal fees

**Replace:** 2–3 sentences for Record/Voice positioning, OpenClaw, schools, or policy hooks.

## 4. Triangulation (when lead is political)

For **campaign-facing** copy, use [work-politics analytical-lenses](../work-politics/analytical-lenses/template-three-lenses.md) on a shared fact summary.

| Structural | Operational / diplomatic | Institutional |
|---|---|---|
| _TBD_ | _TBD_ | _TBD_ |

**Product / strategy thread:** _TBD (no three-lens requirement — use work-dev + INTENT as needed)._

## 5. Operator synthesis

**Work-politics:** _paragraph_

**Work-strategy:** _paragraph_

## 6. Next actions (work-politics snapshot)

- Prepare for **Voter registration deadline** (in-person and mail; mail = postmark) on **Apr 20, 2026**.
- Review `docs/skill-work/work-politics/principal-profile.md` and confirm it still matches the live campaign context.
- Refresh Gallrein, Trump/MAGA, and spending lines before relying on the brief heavily.
- Confirm this is a doc-only week or stage one work-politics milestone so audit continuity stays current.

---

_Generated by `scripts/generate_work_politics_daily_brief.py` (legacy alias: `generate_wap_daily_brief.py`); config `docs/skill-work/work-strategy/daily-brief-config.json`._
