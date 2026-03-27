# Daily brief — work-politics & work-strategy

**Date:** 2026-03-27  
**Assembled:** 2026-03-27 14:28 UTC  
**Recency window (RSS):** last **36h** (undated items may appear)  
**Config:** `docs/skill-work/work-strategy/daily-brief-config.json`

_Operator WORK product. Complete synthesis below; cite sources before any public use._

## 1. Work-politics snapshot

- **Primary:** May 19, 2026 — **days until:** 52
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

**congress · diplomacy · iran · senate · trump** — _7 sources_

- **[W:3 S:0 G:0]** [House Democrat: Trump administration not providing ‘satisfactory answers’ on Iran](https://thehill.com/homenews/house/5804063-jason-crow-trump-iran-war/) — _The Hill — politics_ · _2026-03-27 14:19 UTC_
- **Also** — [Is Trump's pause on attacking Iranian energy for diplomacy or an escalation?](https://www.bbc.com/news/articles/c2evg2m3ye2o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _W:3 S:0 G:0_ · _2026-03-27 13:17 UTC_
- **Also** — [How Trump lost the war with Iran](https://thehill.com/opinion/white-house/5802158-trump-war-fiasco-iran/) — _The Hill — politics_ · _W:3 S:0 G:0_ · _2026-03-27 13:00 UTC_
- **Also** — [Senate votes to fund most of DHS. And, Trump extends Iran's deadline to reopen strait](https://www.npr.org/2026/03/27/g-s1-115433/up-first-newsletter-dhs-funding-iran-strait-of-hormuz-cpac) — _NPR — national news_ · _W:3 S:0 G:0_ · _2026-03-27 07:33 UTC_
- **Also** — [Why Trump needs Congress on Iran in more ways than one: From the Politics Desk](https://www.nbcnews.com/politics/politics-news/trump-needs-congress-iran-ways-one-politics-desk-rcna265354) — _NBC News — politics_ · _W:3 S:0 G:0_ · _2026-03-26 21:23 UTC_

**إسرائيل · إيران** — _2 sources_

- **[W:2 S:0 G:0]** [ريبورتاج: اعتراض الصواريخ العنقودية الإيرانية.. معضلة أمام منظومة الدفاع الإسرائيلية؟](https://www.france24.com/ar/%D8%A7%D9%84%D8%B4%D8%B1%D9%82-%D8%A7%D9%84%D8%A3%D9%88%D8%B3%D8%B7/20260327-%D8%B1%D9%8A%D8%A8%D9%88%D8%B1%D8%AA%D8%A7%D8%AC-%D8%A7%D8%B9%D8%AA%D8%B1%D8%A7%D8%B6-%D8%B5%D9%88%D8%A7%D8%B1%D9%8A%D8%AE-%D8%B9%D9%86%D9%82%D9%88%D8%AF%D9%8A%D8%A9-%D8%A5%D9%8A%D8%B1%D8%A7%D9%86%D9%8A%D8%A9-%D9%85%D9%86%D8%B8%D9%88%D9%85%D8%A9-%D8%AF%D9%81%D8%A7%D8%B9-%D8%A5%D8%B3%D8%B1%D8%A7%D8%A6%D9%8A%D9%84%D9%8A%D8%A9-%D8%A3%D8%B3%D9%84%D8%AD%D8%A9-%D9%85%D8%AD%D8%B8%D9%88%D8%B1%D8%A9) — _France 24 — العربية (MENA)_ · _ar_ · _2026-03-27 13:40 UTC_
- **Also** — [رشقات صاروخية من حزب الله وإيران على إسرائيل.. ماذا عن وضع الجيش الإسرائيلي؟](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260327-%D8%B1%D8%B4%D9%82%D8%A7%D8%AA-%D8%B5%D8%A7%D8%B1%D9%88%D8%AE%D9%8A%D8%A9-%D9%85%D9%86-%D8%AD%D8%B2%D8%A8-%D8%A7%D9%84%D9%84%D9%87-%D9%88%D8%A5%D9%8A%D8%B1%D8%A7%D9%86-%D8%B9%D9%84%D9%89-%D8%A5%D8%B3%D8%B1%D8%A7%D8%A6%D9%8A%D9%84-%D9%85%D8%A7%D8%B0%D8%A7-%D8%B9%D9%86-%D9%88%D8%B6%D8%B9-%D8%A7%D9%84%D8%AC%D9%8A%D8%B4-%D8%A7%D9%84%D8%A5%D8%B3%D8%B1%D8%A7%D8%A6%D9%8A%D9%84%D9%8A) — _France 24 — العربية (MENA)_ · _ar_ · _W:2 S:0 G:0_ · _2026-03-27 13:36 UTC_

#### Other headlines

- **[W:5 S:0 G:0]** [EN DIRECT, guerre en Ukraine : Kiev poursuit ses frappes contre des ports russes de la Baltique](https://www.lemonde.fr/international/live/2026/03/27/en-direct-guerre-en-ukraine-kiev-poursuit-ses-frappes-contre-des-ports-russes-de-la-baltique_6673450_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-03-27 13:32 UTC_
- **[W:1 S:4 G:0]** [OpenAI abandonne finalement le « mode adulte » et les tchats érotiques dans ChatGPT](https://www.lemonde.fr/pixels/article/2026/03/27/openai-abandonne-finalement-le-mode-adulte-et-les-tchats-erotiques-dans-chatgpt_6674545_4408996.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-03-27 12:12 UTC_
- **[W:2 S:0 G:2]** [Iran is adopting Russian drone tactics, Ukrainian troops say](https://www.defenseone.com/threats/2026/03/iran-adopting-russian-drone-tactics-ukrainian-troops-say/412434/) — _Defense One — All_ · _2026-03-27 06:27 UTC_
- **[W:3 S:0 G:0]** [Lobbyists edge out lawmakers in charity hockey showdown](https://thehill.com/blogs/in-the-know/5803938-lobbyists-beat-lawmakers-congressional-hockey-challenge-2026/) — _The Hill — politics_ · _2026-03-27 13:50 UTC_
- **[W:3 S:0 G:0]** [Ukraine-Krieg: Wolodymyr Selenskyj schließt Flugabwehr-Abkommen mit Saudi-Arabien](https://www.spiegel.de/ausland/ukraine-krieg-wolodymyr-selenskyj-schliesst-luftabwehr-abkommen-mit-saudi-arabien-a-81101d6b-817e-4219-a2af-1fba9596850b#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-03-27 14:16 UTC_
- **[W:3 S:0 G:0]** [Rationing power and diluting petrol - how African countries are coping with effects of Iran war](https://www.bbc.com/news/articles/cq8wkq1n9epo?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-27 10:58 UTC_
- **[W:2 S:1 G:0]** [UN human rights chief calls on US to conclude probe into Iran school strike](https://www.bbc.com/news/articles/c75kzk3lgl5o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-03-27 13:25 UTC_
- **[W:2 S:0 G:1]** [Senate agrees to fund DHS, except ICE and CBP, in bid to end extreme airport delays](https://www.nbcnews.com/politics/congress/senate-agrees-fund-dhs-ice-border-patrol-bid-shutdown-tsa-pay-delays-rcna265108) — _NBC News — politics_ · _2026-03-27 07:16 UTC_
- **[W:1 S:1 G:1]** [Judge blocks Pentagon's Anthropic blacklisting for now](https://www.nbcnews.com/news/us-news/anthropic-trump-national-security-rcna265399) — _NBC News — politics_ · _2026-03-27 00:28 UTC_
- **[W:0 S:0 G:3]** [The Army wants to use bullets, mortars, and artillery to take out small drones](https://www.defenseone.com/technology/2026/03/army-wants-use-bullets-mortars-and-artillery-rounds-take-out-small-drones/412392/) — _Defense One — All_ · _2026-03-26 03:41 UTC_
- **[W:2 S:0 G:0]** [House Democrats appear ready to back Senate DHS funding deal](https://thehill.com/homenews/house/5804047-house-democrats-dhs-funding-senate-deal/) — _The Hill — politics_ · _2026-03-27 14:08 UTC_
- **[W:2 S:0 G:0]** [رد من الحرس الثوري الإيراني على تصريحات ترامب.. وتهديد للإمارات والبحرين](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260327-%D8%B1%D8%AF-%D9%85%D9%86-%D8%A7%D9%84%D8%AD%D8%B1%D8%B3-%D8%A7%D9%84%D8%AB%D9%88%D8%B1%D9%8A-%D8%A7%D9%84%D8%A5%D9%8A%D8%B1%D8%A7%D9%86%D9%8A-%D8%B9%D9%84%D9%89-%D8%AA%D8%B5%D8%B1%D9%8A%D8%AD%D8%A7%D8%AA-%D8%AA%D8%B1%D8%A7%D9%85%D8%A8-%D9%88%D8%AA%D9%87%D8%AF%D9%8A%D8%AF-%D9%84%D9%84%D8%A5%D9%85%D8%A7%D8%B1%D8%A7%D8%AA-%D9%88%D8%A7%D9%84%D8%A8%D8%AD%D8%B1%D9%8A%D9%86) — _France 24 — العربية (MENA)_ · _ar_ · _2026-03-27 13:28 UTC_
- **[W:2 S:0 G:0]** [اتهامات لروسيا بمساعدة إيران في هجماتها.. كيف؟](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260327-%D8%A7%D8%AA%D9%87%D8%A7%D9%85%D8%A7%D8%AA-%D9%84%D8%B1%D9%88%D8%B3%D9%8A%D8%A7-%D8%A8%D9%85%D8%B3%D8%A7%D8%B9%D8%AF%D8%A9-%D8%A5%D9%8A%D8%B1%D8%A7%D9%86-%D9%81%D9%8A-%D9%87%D8%AC%D9%85%D8%A7%D8%AA%D9%87%D8%A7-%D9%83%D9%8A%D9%81) — _France 24 — العربية (MENA)_ · _ar_ · _2026-03-27 13:16 UTC_

## 2a. Geopolitical & military (G-ranked)

_**G** = matches on `geo_military_keyword_phrases` (+ optional locale lists in config). Supports triangulation and war-powers messaging — **verify** claims against primary sources._

- **[W:0 S:0 G:3]** [The Army wants to use bullets, mortars, and artillery to take out small drones](https://www.defenseone.com/technology/2026/03/army-wants-use-bullets-mortars-and-artillery-rounds-take-out-small-drones/412392/) — _Defense One — All_ · _2026-03-26 03:41 UTC_
- **[W:2 S:0 G:2]** [Iran is adopting Russian drone tactics, Ukrainian troops say](https://www.defenseone.com/threats/2026/03/iran-adopting-russian-drone-tactics-ukrainian-troops-say/412434/) — _Defense One — All_ · _2026-03-27 06:27 UTC_
- **[W:2 S:0 G:1]** [Senate agrees to fund DHS, except ICE and CBP, in bid to end extreme airport delays](https://www.nbcnews.com/politics/congress/senate-agrees-fund-dhs-ice-border-patrol-bid-shutdown-tsa-pay-delays-rcna265108) — _NBC News — politics_ · _2026-03-27 07:16 UTC_
- **[W:1 S:1 G:1]** [Judge blocks Pentagon's Anthropic blacklisting for now](https://www.nbcnews.com/news/us-news/anthropic-trump-national-security-rcna265399) — _NBC News — politics_ · _2026-03-27 00:28 UTC_
- **[W:1 S:0 G:1]** [Gaetz: Ground invasion of Iran would make US ‘poorer and less safe’](https://thehill.com/policy/defense/5803893-matt-gaetz-us-military-iran-ground-invasion/) — _The Hill — politics_ · _2026-03-27 12:53 UTC_
- **[W:1 S:0 G:1]** [Senators worry about ‘historically dangerous’ strategic threats](https://rollcall.com/2026/03/26/senators-worry-about-historically-dangerous-strategic-threats/) — _Roll Call — Congress_
- **[W:0 S:0 G:1]** [Scientists watch sperm whales work as a team to assist a birth](https://www.npr.org/2026/03/27/nx-s1-5762978/sperm-whale-birth-cooperation-coordination-marine-mammals-science) — _NPR — national news_ · _2026-03-27 06:00 UTC_
- **[W:0 S:0 G:1]** [‘We’ll go 40%’: Army wants good-enough tech it can reshape for battle](https://www.defenseone.com/defense-systems/2026/03/army-good-tech-battle/412402/) — _Defense One — All_ · _2026-03-26 12:31 UTC_

## 2b. Civ-mem depth hooks (in-repo essays — not breaking news)

_Token overlap against `docs/civilization-memory/` (build: `python3 scripts/build_civmem_inrepo_index.py build`). **Historical / structural** depth only — not a substitute for dated news. See [civ-mem-draft-protocol](../work-politics/civ-mem-draft-protocol.md). Public copy still needs human approval._

- **{CMC: `minds/CIV–MIND–MEARSHEIMER.md`}** (overlap 2) — _CIV–MIND–MEARSHEIMER — v3.4 Civilizational Memory Codex · Advisory Mind John J. Mearsheimer Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture Status: ACTIVE · CANONICAL · LOCKED Class: MIND (ADVIS..._
- **{CMC: `minds/CIV–MIND–MERCOURIS.md`}** (overlap 2) — _CIV–MIND–MERCOURIS — v3.4 Civilizational Memory Codex · Primary Mind Alexander Mercouris Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture · Proportional Blend Law Status: ACTIVE · CANONICAL · LOC..._
- **{CMC: `notes/research-brief-condition-in-the-traditions.md`}** (overlap 1) — _**Purpose:** Map where Christianity, Islam, Judaism, Hinduism, and Buddhism **explicitly or implicitly** say that something must hold **before** the awaited future (return, restoration, judgment, moksha, nirvana, etc...._
- **{CMC: `essays/WRITING-THE-BOOK-AND-DEATH.md`}** (overlap 1) — _### On the Most Interesting Activity and Why We Need Not Fear the End --- This essay states a single thesis: **the most interesting activity in the human experience is writing a book** — and that therefore we need not..._

## 3. Lead themes (auto-stub — replace after reading)

### Work-politics / campaign angle
- EN DIRECT, guerre en Ukraine : Kiev poursuit ses frappes contre des ports russes de la Baltique
- House Democrat: Trump administration not providing ‘satisfactory answers’ on Iran
- Lobbyists edge out lawmakers in charity hockey showdown

**Replace:** 2–3 sentences for principal, district, opposition narrative.

### Work-strategy angle (product / governance / tech)

- OpenAI abandonne finalement le « mode adulte » et les tchats érotiques dans ChatGPT
- UN human rights chief calls on US to conclude probe into Iran school strike
- Judge blocks Pentagon's Anthropic blacklisting for now

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
