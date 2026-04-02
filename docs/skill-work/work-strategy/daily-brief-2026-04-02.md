# Daily brief — work-politics & work-strategy

**Date:** 2026-04-02  
**Assembled:** 2026-04-02 12:42 UTC  
**Recency window (RSS):** last **36h** (undated items may appear)  
**Config:** `docs/skill-work/work-strategy/daily-brief-config.json`

_Operator WORK product. Complete synthesis below; cite sources before any public use._

## 1. Work-politics snapshot

- **Primary:** May 19, 2026 — **days until:** 46
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

- **Civilizational / geopolitics operator ledger:** [STRATEGY.md](STRATEGY.md) — long-horizon CORE + heuristics + `WS–MEM` entries (WORK-only; gate only when promoting to Record or milestones).
- Campaign/companion positioning: portable Record, human-only merge, Voice boundary.
- OpenClaw ↔ repo handback and export provenance (see [work-dev workspace](../work-dev/workspace.md)).
- AI-in-schools and identity-substrate narrative vs Alpha-style bundles (see [work-alpha-school](../work-alpha-school/README.md), [work-dev offers](../work-dev/offers.md)).
- Optional: federal / state AI governance headlines when relevant to offers or civ-mem work.
- Long-form tech discourse (GTC-class, Moonshots-class): themes distilled in [external-tech-scan.md](external-tech-scan.md) — use for **strategy vocabulary** and **keyword-season** tuning in [daily-brief-config.json](daily-brief-config.json); **not** unsourced brief facts.
- **Putin — last 48h:** Hey **menu C** fills **§1d** in the daily brief per [daily-brief-putin-watch.md](daily-brief-putin-watch.md) (web scan + citations); Step 1 does not run this pass.

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

## 1d. Putin — last 48 hours

_Rolling window ~**2026-03-31 12:42** → **2026-04-02 12:42 UTC** (brief assembly time). **Bullets + URLs** per [daily-brief-putin-watch.md](daily-brief-putin-watch.md). RIA = Russian state wire._

- **[2026-04-01 — RIA Novosti]** Putin said **parliamentary parties help bring people “proven in battle”** into positions of power and state structures (party–personnel framing). https://ria.ru/20260401/putin-2084650883.html
- **[2026-04-01 — RIA Novosti]** Putin **said he hopes the energy situation will straighten out** (*nadeyetsya, chto situatsiya … vypravitsya* — wire paraphrase/quote per article). https://ria.ru/20260401/putin-2084331184.html
- **[Secondary — verify vs Kremlin transcript]** *The Moscow Times* (Russian edition, **2026-04-01**), citing **unnamed sources / Bloomberg-style Kremlin reporting**, claimed **orders to prepare a new Ukraine offensive** and a **multi-year war horizon** if talks fail — **not** matched here to a published Kremlin **transcript**; use for narrative risk only until primary text exists. https://ru.themoscowtimes.com/2026/04/01/putin-sobralsya-prodolzhat-voinu-esche-dva-goda-i-poruchil-gotovit-novoe-nastuplenie-v-ukraine-a191424
- **Primary bookmark (same window):** Kremlin president events / transcripts — http://kremlin.ru/events/president

_Spokesman-only Ukraine lines (e.g. Peskov on ceasefire proposals) are out of scope for this § unless tied to a joint appearance; see wires if needed._

## 2. Headlines (ingested RSS)

_Fetch failed for: Reuters — World._

Ranked by **W+S+G** (global keyword lists + per-`locale` maps for W/S; **G** = `geo_military_keyword_phrases`) then recency. Each feed is **recency-sorted** then **capped** (`ingest_caps`: per-feed `max_items` and/or `tier` → `max_items_by_tier`; CLI `--max-per-feed N` overrides all feeds). Optional **same-story** grouping uses `story_anchor_phrases` overlap (Jaccard + shared anchors). Tune phrases in config JSON.

_Same-story clusters use anchor overlap on titles (proper nouns / crisis terms); not neural / semantic dedupe._

#### Same-story (multilingual)

**iran · israel · krieg · netanyahu · trump** — _16 sources_

- **[W:7 S:0 G:0]** [Donald Trump: Der US-Präsident beschleunigt den Niedergang Amerikas durch den Iran-Krieg](https://www.spiegel.de/ausland/donald-trump-der-us-praesident-beschleunigt-den-niedergang-amerikas-durch-den-iran-krieg-a-15261d31-1da0-48a5-b867-cc807f3e4a12#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-04-02 14:26 UTC_
- **Also** — [Trump’s push to end Iran war bucks Israel’s desire for regime change](https://thehill.com/policy/international/5812018-trump-netanyahu-iran-priorities/) — _The Hill — politics_ · _W:4 S:0 G:0_ · _2026-04-02 10:00 UTC_
- **Also** — [Iran responds to Trump address with missile attacks on Israel, Gulf states](https://thehill.com/policy/international/5812466-iran-trump-address-response-israel-gulf-state-strikes/) — _The Hill — politics_ · _W:3 S:0 G:1_ · _2026-04-02 12:22 UTC_
- **Also** — [Trump’s half-baked attacks against Iran won’t work](https://thehill.com/opinion/white-house/5811772-trump-iran-strategy-failures/) — _The Hill — politics_ · _W:3 S:0 G:0_ · _2026-04-02 12:30 UTC_
- **Also** — [Trump leaves key questions unanswered as he seeks to calm nerves over Iran war](https://www.bbc.com/news/articles/cnv81ven263o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _W:3 S:0 G:0_ · _2026-04-02 03:22 UTC_

**guerra · trump** — _2 sources_

- **[W:5 S:0 G:0]** [Trump deja preguntas cruciales sin respuesta al intentar calmar los nervios en EE.UU. y el resto del mundo por la guerra con Irán](https://www.bbc.com/mundo/articles/cre1n7x78pro?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-04-02 10:05 UTC_
- **Also** — [Trump dice que los objetivos de la guerra con Irán están "cerca de completarse" en un mensaje a la nación](https://www.bbc.com/mundo/articles/c8x7g028ww5o?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _W:5 S:0 G:0_ · _2026-04-02 02:46 UTC_

**إيران · ترامب · حرب** — _2 sources_

- **[W:3 S:0 G:0]** [خطاب ترامب بشأن استمرار الحرب على إيران يعيد الأسواق المالية إلى دائرة القلق](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260402-%D8%AE%D8%B7%D8%A7%D8%A8-%D8%AA%D8%B1%D8%A7%D9%85%D8%A8-%D8%A8%D8%B4%D8%A3%D9%86-%D8%A7%D8%B3%D8%AA%D9%85%D8%B1%D8%A7%D8%B1-%D8%A7%D9%84%D8%AD%D8%B1%D8%A8-%D8%B9%D9%84%D9%89-%D8%A5%D9%8A%D8%B1%D8%A7%D9%86-%D9%8A%D8%B9%D9%8A%D8%AF-%D8%A7%D9%84%D8%A3%D8%B3%D9%88%D8%A7%D9%82-%D8%A7%D9%84%D9%85%D8%A7%D9%84%D9%8A%D8%A9-%D8%A5%D9%84%D9%89-%D8%AF%D8%A7%D8%A6%D8%B1%D8%A9-%D8%A7%D9%84%D9%82%D9%84%D9%82) — _France 24 — العربية (MENA)_ · _ar_ · _2026-04-02 11:13 UTC_
- **Also** — [ما الردود الإيرانية على خطاب ترامب؟](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260402-%D9%85%D8%A7-%D8%A7%D9%84%D8%B1%D8%AF%D9%88%D8%AF-%D8%A7%D9%84%D8%A5%D9%8A%D8%B1%D8%A7%D9%86%D9%8A%D8%A9-%D8%B9%D9%84%D9%89-%D8%AE%D8%B7%D8%A7%D8%A8-%D8%AA%D8%B1%D8%A7%D9%85%D8%A8) — _France 24 — العربية (MENA)_ · _ar_ · _W:2 S:0 G:0_ · _2026-04-02 10:07 UTC_

#### Other headlines

- **[W:8 S:0 G:1]** [EN DIRECT, guerre en Ukraine : Emmanuel Macron accuse Donald Trump de vider l’OTAN de sa substance en créant « le doute sur son engagement »](https://www.lemonde.fr/international/live/2026/04/02/en-direct-guerre-en-ukraine-un-gazoduc-russe-pris-pour-cible-par-des-drones-ukrainiens-affirme-gazprom_6675208_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-02 11:41 UTC_
- **[W:4 S:0 G:0]** [Barr leads wide-open Kentucky GOP Senate primary: Survey](https://thehill.com/homenews/campaign/5811888-andy-barr-kentucky-senate-race-poll/) — _The Hill — politics_ · _2026-04-02 10:00 UTC_
- **[W:3 S:0 G:0]** [Guerre au Moyen-Orient : les profits exceptionnels des tradeurs de TotalEnergies](https://www.lemonde.fr/economie/article/2026/04/02/guerre-au-moyen-orient-les-profits-exceptionnels-des-tradeurs-de-totalenergies_6676110_3234.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-02 12:00 UTC_
- **[W:3 S:0 G:0]** [EE.UU. levanta las sanciones contra la presidenta interina de Venezuela, Delcy Rodríguez](https://www.bbc.com/mundo/articles/c36r5l25429o?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-04-01 21:52 UTC_
- **[W:1 S:2 G:0]** [Supreme Court Casts Doubt on Trump Birthright Citizenship Order](https://www.today.com/video/justices-appear-doubtful-of-trump-s-birthright-citizenship-order-260574789928) — _NBC News — politics_ · _2026-04-02 12:25 UTC_
- **[W:1 S:2 G:0]** [Inside the Supreme Court as Trump faced the justices he's criticized](https://www.nbcnews.com/politics/supreme-court/supreme-court-trump-faced-justices-criticized-rcna266067) — _NBC News — politics_ · _2026-04-01 20:52 UTC_
- **[W:1 S:1 G:1]** [Strikes on Iranian universities raise war crime questions, fears of retaliation](https://thehill.com/homenews/education/5811380-iran-war-university-strikes-war-crimes/) — _The Hill — politics_ · _2026-04-02 10:00 UTC_
- **[W:2 S:0 G:0]** [Europe is in Trump’s crosshairs](https://thehill.com/opinion/national-security/5811347-europe-is-in-trumps-crosshairs/) — _The Hill — politics_ · _2026-04-02 11:00 UTC_
- **[W:2 S:0 G:0]** [Trump ramps up war on mail-in voting ahead of midterms](https://thehill.com/homenews/campaign/5811266-trump-mail-in-voting-midterms/) — _The Hill — politics_ · _2026-04-02 10:00 UTC_
- **[W:2 S:0 G:0]** [Trump’s surgeon general nominee caught in GOP crossfire over MAHA](https://thehill.com/policy/healthcare/5811902-trump-surgeon-general-nominee-stuck-senate/) — _The Hill — politics_ · _2026-04-02 10:00 UTC_
- **[W:2 S:0 G:0]** [Trump goes on a revenge tour in Indiana after failed redistricting vote](https://www.nbcnews.com/politics/2026-election/trump-goes-revenge-tour-indiana-failed-redistricting-vote-rcna265994) — _NBC News — politics_ · _2026-04-02 09:00 UTC_

## 2a. Geopolitical & military (G-ranked)

_**G** = matches on `geo_military_keyword_phrases` (+ optional locale lists in config). Supports triangulation and war-powers messaging — **verify** claims against primary sources._

- **[W:8 S:0 G:1]** [EN DIRECT, guerre en Ukraine : Emmanuel Macron accuse Donald Trump de vider l’OTAN de sa substance en créant « le doute sur son engagement »](https://www.lemonde.fr/international/live/2026/04/02/en-direct-guerre-en-ukraine-un-gazoduc-russe-pris-pour-cible-par-des-drones-ukrainiens-affirme-gazprom_6675208_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-02 11:41 UTC_
- **[W:3 S:0 G:1]** [Iran responds to Trump address with missile attacks on Israel, Gulf states](https://thehill.com/policy/international/5812466-iran-trump-address-response-israel-gulf-state-strikes/) — _The Hill — politics_ · _2026-04-02 12:22 UTC_
- **[W:1 S:1 G:1]** [Strikes on Iranian universities raise war crime questions, fears of retaliation](https://thehill.com/homenews/education/5811380-iran-war-university-strikes-war-crimes/) — _The Hill — politics_ · _2026-04-02 10:00 UTC_
- **[W:1 S:0 G:1]** [Donalds dominates Florida GOP gubernatorial race: Poll](https://thehill.com/homenews/5811842-donalds-jolly-hypothetical-matchup/) — _The Hill — politics_ · _2026-04-02 10:00 UTC_
- **[W:1 S:0 G:1]** [U.S. lifts sanctions on Venezuela's acting President Delcy Rodríguez](https://www.npr.org/2026/04/02/g-s1-116142/u-s-lift-sanctions-venezuela-president-delcy-rodriguez) — _NPR — national news_ · _2026-04-02 02:44 UTC_
- **[W:0 S:0 G:1]** [Defense Business Brief: The Navy’s MUSV pivot; NGA taps Vantor for $2.3M spy satellite contract; and a bit more](https://www.defenseone.com/business/2026/04/defense-business-brief-navys-musv-pivot-nga-taps-vantor-23m-spy-satellite-contract-and-bit-more/412546/) — _Defense One — All_ · _2026-04-01 12:00 UTC_

## 2b. Civ-mem depth hooks (in-repo essays — not breaking news)

_Token overlap against `docs/civilization-memory/` (build: `python3 scripts/build_civmem_inrepo_index.py build`). **Historical / structural** depth only — not a substitute for dated news. See [civ-mem-draft-protocol](../work-politics/civ-mem-draft-protocol.md). Public copy still needs human approval._

- **{CMC: `minds/CIV–MIND–MEARSHEIMER.md`}** (overlap 2) — _CIV–MIND–MEARSHEIMER — v3.4 Civilizational Memory Codex · Advisory Mind John J. Mearsheimer Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture Status: ACTIVE · CANONICAL · LOCKED Class: MIND (ADVIS..._
- **{CMC: `minds/CIV–MIND–MERCOURIS.md`}** (overlap 2) — _CIV–MIND–MERCOURIS — v3.4 Civilizational Memory Codex · Primary Mind Alexander Mercouris Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture · Proportional Blend Law Status: ACTIVE · CANONICAL · LOC..._
- **{CMC: `notes/civ-mem-state-vs-scholar.md`}** (overlap 1) — _**Purpose:** Clarify the distinction between **STATE** and **SCHOLAR** in the civilization_memory (CMC) model. These are internal operating modes of the *upstream* CMC system (e.g. `research/repos/civilization_memory`..._
- **{CMC: `essays/WRITING-THE-BOOK-AND-DEATH.md`}** (overlap 2) — _### On the Most Interesting Activity and Why We Need Not Fear the End --- This essay states a single thesis: **the most interesting activity in the human experience is writing a book** — and that therefore we need not..._

## 3. Lead themes (auto-stub — replace after reading)

### Work-politics / campaign angle
- EN DIRECT, guerre en Ukraine : Emmanuel Macron accuse Donald Trump de vider l’OTAN de sa substance en créant « le doute sur son engagement »
- Donald Trump: Der US-Präsident beschleunigt den Niedergang Amerikas durch den Iran-Krieg
- Trump deja preguntas cruciales sin respuesta al intentar calmar los nervios en EE.UU. y el resto del mundo por la guerra con Irán

**Replace:** 2–3 sentences for principal, district, opposition narrative.

### Work-strategy angle (product / governance / tech)

- Supreme Court Casts Doubt on Trump Birthright Citizenship Order
- Inside the Supreme Court as Trump faced the justices he's criticized
- Lemonade by AMD: a fast and open source local LLM server using GPU and NPU

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
