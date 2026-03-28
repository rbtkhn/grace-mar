# Daily brief — work-politics & work-strategy

**Date:** 2026-03-28  
**Assembled:** 2026-03-28 11:52 UTC  
**Recency window (RSS):** last **36h** (undated items may appear)  
**Config:** `docs/skill-work/work-strategy/daily-brief-config.json`

_Operator WORK product. Complete synthesis below; cite sources before any public use._

## 1. Work-politics snapshot

- **Primary:** May 19, 2026 — **days until:** 51
- **Work-politics gate:** 0 pending candidate(s)

### Upcoming (from calendar)

- ****Apr 20, 2026**** — **Voter registration deadline** (in-person and mail; mail = postmark) — Push registration in-district; remind supporters.
- ****May 5, 2026**** — Mail-in absentee ballot request portal closes — Voters who need absentee must request by this date.
- ****May 7, 2026**** — **FEC pre-primary report due** — Covers period Apr 1–Apr 29. Registration/certification & overnight mail deadline May 4.
- ****May 19, 2026**** — **Primary election day** — Polls open; final GOTV.

### Territory signals (from docs)

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

## 1c. Two horizons — fast vs slow

**Fast (same brief):** §**2** RSS headlines + §**1** snapshot — news cycle, principal-adjacent hooks, scored **W / S / G**.

**Slow (work-jiang):** lecture extractions, compression JSON, comparative sweeps — **structural** context; not a substitute for dated facts. Prefer [SELF-LIBRARY](../../../users/grace-mar/self-library.md) entries (e.g. reference / `lookup_priority`) when library-first lookup applies.

_From `docs/skill-work/work-strategy/daily-brief-jiang-layer.md` § Active work-jiang hooks._

- _Edit this section between brief runs. List repo-relative paths or one-line labels._
- _Example:_ `research/external/work-jiang/compressions/<slug>-YYYYMMDD.json`
- _Example:_ `research/external/work-jiang/**/*.paste-snippet.md` (paste the exact path you used)
- _Example:_ [COMPRESSION-ENGINE.md](../work-jiang/COMPRESSION-ENGINE.md) — last run: _date_
- ---

_Product / integration context: [work-dev/workspace.md](../work-dev/workspace.md), [work-strategy/README.md](README.md)._

## 2. Headlines (ingested RSS)

_Fetch failed for: Reuters — World._

Ranked by **W+S+G** (global keyword lists + per-`locale` maps for W/S; **G** = `geo_military_keyword_phrases`) then recency. Each feed is **recency-sorted** then **capped** (`ingest_caps`: per-feed `max_items` and/or `tier` → `max_items_by_tier`; CLI `--max-per-feed N` overrides all feeds). Optional **same-story** grouping uses `story_anchor_phrases` overlap (Jaccard + shared anchors). Tune phrases in config JSON.

_Same-story clusters use anchor overlap on titles (proper nouns / crisis terms); not neural / semantic dedupe._

#### Same-story (multilingual)

**iran · senate · trump** — _6 sources_

- **[W:4 S:0 G:0]** [Live updates: House tees up vote on DHS stopgap after rejecting Senate bill; Trump orders TSA paid](https://thehill.com/homenews/administration/5802558-live-updates-trump-dhs-shutdown-tsa-iran/) — _The Hill — politics_ · _2026-03-27 22:25 UTC_
- **Also** — [House Republicans pass DHS funding bill that Senate Democrats call 'dead on arrival'](https://www.nbcnews.com/politics/trump-administration/trump-johnson-dhs-house-rebels-senate-bill-ice-cbp-rcna265507) — _NBC News — politics_ · _W:4 S:0 G:0_ · _2026-03-27 17:48 UTC_
- **Also** — [Iran war splits older and younger conservatives - as pressure builds for Trump to find exit ramp](https://www.bbc.com/news/articles/cjd8e4px12ro?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _W:3 S:0 G:0_ · _2026-03-28 00:05 UTC_
- **Also** — [Rifts over Iran, but unity for Trump: Takeaways from CPAC 2026](https://www.npr.org/2026/03/28/nx-s1-5764275/cpac-2026) — _NPR — national news_ · _W:2 S:0 G:0_ · _2026-03-28 06:00 UTC_
- **Also** — [Trump sells Iran war at Saudi investment forum in Miami, warning Cuba is ‘next’](https://thehill.com/homenews/administration/5805278-trump-saudi-forum-cuba-iran/) — _The Hill — politics_ · _W:2 S:0 G:0_ · _2026-03-27 23:43 UTC_

**إسرائيل · إيران** — _2 sources_

- **[W:2 S:0 G:0]** [لماذا قصفت إسرائيل مصنع الكعكة الصفراء في محافظة يزد الإيرانية؟](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260328-%D9%84%D9%85%D8%A7%D8%B0%D8%A7-%D9%82%D8%B5%D9%81%D8%AA-%D8%A5%D8%B3%D8%B1%D8%A7%D8%A6%D9%8A%D9%84-%D9%85%D8%B5%D9%86%D8%B9-%D8%A7%D9%84%D9%83%D8%B9%D9%83%D8%A9-%D8%A7%D9%84%D8%B5%D9%81%D8%B1%D8%A7%D8%A1-%D9%81%D9%8A-%D9%85%D8%AD%D8%A7%D9%81%D8%B8%D8%A9-%D9%8A%D8%B2%D8%AF-%D8%A7%D9%84%D8%A5%D9%8A%D8%B1%D8%A7%D9%86%D9%8A%D8%A9) — _France 24 — العربية (MENA)_ · _ar_ · _2026-03-28 10:56 UTC_
- **Also** — [إسرائيل تقصف مفاعل آراك للماء الثقيل في وسط إيران](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260328-%D8%A5%D8%B3%D8%B1%D8%A7%D8%A6%D9%8A%D9%84-%D8%AA%D9%82%D8%B5%D9%81-%D9%85%D9%81%D8%A7%D8%B9%D9%84-%D8%A2%D8%B1%D8%A7%D9%83-%D9%84%D9%84%D9%85%D8%A7%D8%A1-%D8%A7%D9%84%D8%AB%D9%82%D9%8A%D9%84-%D9%81%D9%8A-%D9%88%D8%B3%D8%B7-%D8%A5%D9%8A%D8%B1%D8%A7%D9%86) — _France 24 — العربية (MENA)_ · _ar_ · _W:2 S:0 G:0_ · _2026-03-28 09:30 UTC_

#### Other headlines

- **[W:5 S:0 G:0]** [3 gráficos clave que encienden las alarmas para Trump por la guerra en Irán](https://www.bbc.com/mundo/articles/clyenx9pw31o?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-03-27 19:25 UTC_
- **[W:4 S:0 G:0]** [EN DIRECT, guerre en Ukraine : une frappe russe sur Odessa a fait au moins deux morts et douze blessés](https://www.lemonde.fr/international/live/2026/03/28/en-direct-guerre-en-ukraine-une-frappe-russe-sur-odessa-a-fait-au-moins-deux-morts-et-douze-blesses_6673450_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-03-28 12:05 UTC_
- **[W:4 S:0 G:0]** [Los hutíes lanzan misiles desde Yemen contra Israel, ampliando la guerra en Medio Oriente](https://www.bbc.com/mundo/articles/cj37nnpez4jo?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-03-28 10:45 UTC_
- **[W:4 S:0 G:0]** [House Republicans reject Senate deal, prolonging partial US government shutdown](https://www.bbc.com/news/articles/cgj052l1j2no?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-28 08:38 UTC_
- **[W:4 S:0 G:0]** [Iran-News heute: Was ein Kriegseintritt der Huthis bedeuten würde](https://www.spiegel.de/ausland/iran-news-heute-rubio-glaubt-der-krieg-sei-in-wochen-nicht-in-monaten-vorbei-a-624b1930-db95-4f39-a268-b36194b96f4f#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-03-28 09:06 UTC_
- **[W:2 S:2 G:0]** ['Memory of a generation': China mourns the sudden death of a controversial education influencer](https://www.bbc.com/news/articles/c15dz7ql59yo?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-27 23:19 UTC_
- **[W:2 S:0 G:2]** [Houthis threaten to join Iran war if these 3 red lines crossed](https://thehill.com/policy/international/5805195-houthi-threat-us-israel-iran/) — _The Hill — politics_ · _2026-03-27 22:35 UTC_
- **[W:2 S:0 G:2]** [Iran is adopting Russian drone tactics, Ukrainian troops say](https://www.defenseone.com/threats/2026/03/iran-adopting-russian-drone-tactics-ukrainian-troops-say/412434/) — _Defense One — All_ · _2026-03-27 06:27 UTC_
- **[W:3 S:0 G:0]** [House Republicans flee Congress in record numbers amid growing dysfunction](https://thehill.com/homenews/house/5805206-house-republicans-retiring-2026/) — _The Hill — politics_ · _2026-03-28 10:00 UTC_
- **[W:3 S:0 G:0]** [Gaza peace doubts deepen as attention shifts to Iran](https://www.bbc.com/news/articles/crr10v5p7lgo?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-28 06:00 UTC_
- **[W:3 S:0 G:0]** ["Mi hija está bajo los escombros": dentro de Teherán, donde las víctimas civiles aumentan por la guerra](https://www.bbc.com/mundo/articles/c705kp42507o?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-03-28 00:08 UTC_
- **[W:2 S:1 G:0]** [Democrats demand answers on sanctioned Russian lawmakers visiting Capitol](https://thehill.com/homenews/house/5805300-democrats-question-russian-lawmakers-us-capitol-visit/) — _The Hill — politics_ · _2026-03-28 00:31 UTC_
- **[W:2 S:0 G:1]** [Senate agrees to fund DHS, except ICE and CBP, in bid to end extreme airport delays](https://www.nbcnews.com/politics/congress/senate-agrees-fund-dhs-ice-border-patrol-bid-shutdown-tsa-pay-delays-rcna265108) — _NBC News — politics_ · _2026-03-27 07:16 UTC_

## 2a. Geopolitical & military (G-ranked)

_**G** = matches on `geo_military_keyword_phrases` (+ optional locale lists in config). Supports triangulation and war-powers messaging — **verify** claims against primary sources._

- **[W:2 S:0 G:2]** [Houthis threaten to join Iran war if these 3 red lines crossed](https://thehill.com/policy/international/5805195-houthi-threat-us-israel-iran/) — _The Hill — politics_ · _2026-03-27 22:35 UTC_
- **[W:2 S:0 G:2]** [Iran is adopting Russian drone tactics, Ukrainian troops say](https://www.defenseone.com/threats/2026/03/iran-adopting-russian-drone-tactics-ukrainian-troops-say/412434/) — _Defense One — All_ · _2026-03-27 06:27 UTC_
- **[W:0 S:0 G:2]** [More Columbia-class submarines?](https://www.defenseone.com/defense-systems/2026/03/more-columbia-class-submarines/412469/) — _Defense One — All_ · _2026-03-27 17:13 UTC_
- **[W:2 S:0 G:1]** [Senate agrees to fund DHS, except ICE and CBP, in bid to end extreme airport delays](https://www.nbcnews.com/politics/congress/senate-agrees-fund-dhs-ice-border-patrol-bid-shutdown-tsa-pay-delays-rcna265108) — _NBC News — politics_ · _2026-03-27 07:16 UTC_
- **[W:1 S:0 G:1]** [U.S. troops injured in attack on Saudi base as the war reaches one month](https://www.npr.org/2026/03/28/nx-s1-5764720/iran-war-one-month) — _NPR — national news_ · _2026-03-28 05:38 UTC_
- **[W:1 S:0 G:1]** [Iranian attack injures 10 Americans on base in Saudi Arabia](https://thehill.com/policy/defense/5805412-iranian-attack-saudi-base-injures-us-troops/) — _The Hill — politics_ · _2026-03-28 02:46 UTC_
- **[W:0 S:1 G:1]** [Judge blocks Pentagon's Anthropic ban, calling it illegal retaliation](https://www.defenseone.com/policy/2026/03/judge-pentagon-anthropic-ban-retaliation/412463/) — _Defense One — All_ · _2026-03-27 14:04 UTC_

## 2b. Civ-mem depth hooks (in-repo essays — not breaking news)

_Token overlap against `docs/civilization-memory/` (build: `python3 scripts/build_civmem_inrepo_index.py build`). **Historical / structural** depth only — not a substitute for dated news. See [civ-mem-draft-protocol](../work-politics/civ-mem-draft-protocol.md). Public copy still needs human approval._

- **{CMC: `minds/CIV–MIND–MEARSHEIMER.md`}** (overlap 2) — _CIV–MIND–MEARSHEIMER — v3.4 Civilizational Memory Codex · Advisory Mind John J. Mearsheimer Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture Status: ACTIVE · CANONICAL · LOCKED Class: MIND (ADVIS..._
- **{CMC: `minds/CIV–MIND–MERCOURIS.md`}** (overlap 2) — _CIV–MIND–MERCOURIS — v3.4 Civilizational Memory Codex · Primary Mind Alexander Mercouris Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture · Proportional Blend Law Status: ACTIVE · CANONICAL · LOC..._
- **{CMC: `minds/README.md`}** (overlap 1) — _**Purpose:** This folder holds the **three mind profiles** ported from upstream CMC (`research/repos/civilization_memory/docs/templates/`). They are the **specific implementation** of polyphonic cognition in civ-mem: ..._
- **{CMC: `notes/research-brief-condition-in-the-traditions.md`}** (overlap 1) — _**Purpose:** Map where Christianity, Islam, Judaism, Hinduism, and Buddhism **explicitly or implicitly** say that something must hold **before** the awaited future (return, restoration, judgment, moksha, nirvana, etc...._
- **{CMC: `minds/CIV–MIND–BARNES.md`}** (overlap 1) — _CIV–MIND–BARNES — v3.4 Civilizational Memory Codex · Liability/Mechanism Perspective Robert Barnes Cognitive–Linguistic Signature Layer Constitutional North Star · Personal Liability · Institutional Defection · Mechan..._

## 3. Lead themes (auto-stub — replace after reading)

### Work-politics / campaign angle
- 3 gráficos clave que encienden las alarmas para Trump por la guerra en Irán
- Live updates: House tees up vote on DHS stopgap after rejecting Senate bill; Trump orders TSA paid
- EN DIRECT, guerre en Ukraine : une frappe russe sur Odessa a fait au moins deux morts et douze blessés

**Replace:** 2–3 sentences for principal, district, opposition narrative.

### Work-strategy angle (product / governance / tech)

- Supreme Court mulls limiting mail-in ballots, forcing states to prepare for changes
- 'Memory of a generation': China mourns the sudden death of a controversial education influencer
- Democrats demand answers on sanctioned Russian lawmakers visiting Capitol

**Replace:** 2–3 sentences for Record/Voice positioning, OpenClaw, schools, or policy hooks.

### Slow structural layer (work-jiang)

_Not dated news — patterns from lecture extractions, `jiang-compress` JSON, comparative sweeps. Connect to **§1c** hooks when drafting campaign or opposition copy; cite sources if anything ships publicly._

**Replace:** 2–3 sentences — which slow pattern applies to today’s **W** angle, or why none does.

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
- Refresh Gallrein, Trump/MAGA, and spending lines before relying on the brief heavily.
- Confirm this is a doc-only week or stage one work-politics milestone so audit continuity stays current.
- Refresh items marked `needs_refresh` in `brief-source-registry.md` before generating the next brief.

---

_Generated by `scripts/generate_work_politics_daily_brief.py` (legacy alias: `generate_wap_daily_brief.py`); config `docs/skill-work/work-strategy/daily-brief-config.json`._
