# Daily brief — work-politics & work-strategy

**Date:** 2026-04-07  
**Assembled:** 2026-04-07 20:57 UTC  
**Recency window (RSS):** last **36h** (undated items may appear)  
**Config:** `docs/skill-work/work-strategy/daily-brief-config.json`

_Operator WORK product. Complete synthesis below; cite sources before any public use._

## 1. Work-politics snapshot

- **Primary:** May 19, 2026 — **days until:** 41
- **Work-politics gate:** 0 pending candidate(s)

### Upcoming (from calendar)

- ****Apr 20, 2026**** — **Voter registration deadline** (in-person and mail; mail = postmark) — Push registration in-district; remind supporters.
- ****May 5, 2026**** — Mail-in absentee ballot request portal closes — Voters who need absentee must request by this date.
- ****May 7, 2026**** — **FEC pre-primary report due** — Covers period Apr 1–Apr 29. Registration/certification & overnight mail deadline May 4.
- ****May 19, 2026**** — **Primary election day** — Polls open; final GOTV.

### Territory signals (from docs)

- **research_gap:** Opposition brief still has placeholder sections
- **freshness:** Revenue log may be stale
- **gate_rhythm:** No live work-politics candidates in RECURSION-GATE
- **brief_readiness:** Weekly brief sources are not fully ready

## 1b. Work-strategy focus

_From `docs/skill-work/work-strategy/daily-brief-focus.md` § Active focus._

- **Civilizational / geopolitics operator ledger:** [STRATEGY.md](STRATEGY.md) — long-horizon CORE + heuristics + §IV operator strategy log (WORK-only; gate only when promoting to Record or milestones).
- Campaign/companion positioning: portable Record, human-only merge, Voice boundary.
- OpenClaw ↔ repo handback and export provenance (see [work-dev workspace](../work-dev/workspace.md)).
- AI-in-schools and identity-substrate narrative vs Alpha-style bundles (see [work-alpha-school](../work-alpha-school/README.md), [work-dev offers](../work-dev/offers.md)).
- Optional: federal / state AI governance headlines when relevant to offers or civ-mem work.
- Long-form tech discourse (GTC-class, Moonshots-class): themes distilled in [external-tech-scan.md](external-tech-scan.md) — use for **strategy vocabulary** and **keyword-season** tuning in [daily-brief-config.json](daily-brief-config.json); **not** unsourced brief facts.
- **Putin — last 48h:** **Coffee menu A — Today** fills **§1d** in the daily brief per [daily-brief-putin-watch.md](daily-brief-putin-watch.md) (web scan + citations); Step 1 does not run this pass.
- **Weak signal — §1e:** Include one weak signal worth watching when a credible candidate exceeds threshold; test any historical parallel with a compact analogy audit before carrying it into synthesis ([weak-signals.md](weak-signals.md), [weak-signal-template.md](weak-signal-template.md), [analogy-audit-template.md](analogy-audit-template.md)).
- **Rome / Vatican (work-strategy-rome):** When Holy See or papal lines intersect multipolar or legitimacy stories, run the [ROME-PASS](work-strategy-rome/ROME-PASS.md) skeleton (vatican.va + wire + optional civ-mem); file notes or exemplars under [work-strategy-rome/notes/](work-strategy-rome/notes/). **Standing packet (Apr 2026):** [Leo XIV OSINT brief](../work-politics/leo-xiv-osint-prc-brief-2026-04-04.md) (Bollettino-backed China tranche) + [civ-mem context](work-strategy-rome/notes/2026-04-05-leo-xiv-civ-mem-historical-context.md) — analytic exercise; facts still tier **A** from primary URLs in the brief.

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

_Rolling ~48h window ending brief assembly (2026-04-07 20:57 UTC). Sources: Kremlin English site, TASS English._

- **2026-04-05 — Geologist’s Day greetings:** Kremlin published Putin’s message to Russian geologists, citing new field discoveries and Arctic / shelf work. Primary: [Greetings on Geologist’s Day](http://en.kremlin.ru/events/president/news/79467) (Kremlin.ru).
- **Forward schedule (not a same-day appearance):** Kremlin spokesman (TASS) flags Putin’s **SPIEF-2026** address (forum **2026-06-03–06**) as a major scheduled speech. Wire: [Putin to deliver comprehensive address at SPIEF-2026 — Kremlin](http://en.tass.ru/politics/2108677) (TASS).
- **April 6–7 visible Kremlin transcript gap:** No additional dated **president** transcripts or news items located on the English Kremlin president feed in this narrow window beyond the above; for same-day Russia–Ukraine military lines use wires (e.g. Reuters/BBC Russia–Ukraine desks), not this block.

## 1e. Weak signal worth watching

_Operator block per [weak-signal-template.md](weak-signal-template.md) and [weak-signals.md](weak-signals.md). One compact weak signal when a credible candidate exists (low/medium confidence only). If nothing clears the bar, use: **No credible weak signal exceeded the threshold today.** When a historical parallel is in play, summarize a short analogy audit ([analogy-audit-template.md](analogy-audit-template.md)) here._

## 2. Headlines (ingested RSS)

_Fetch failed for: Reuters — World._

Ranked by **W+S+G** (global keyword lists + per-`locale` maps for W/S; **G** = `geo_military_keyword_phrases`) then recency. Each feed is **recency-sorted** then **capped** (`ingest_caps`: per-feed `max_items` and/or `tier` → `max_items_by_tier`; CLI `--max-per-feed N` overrides all feeds). Optional **same-story** grouping uses `story_anchor_phrases` overlap (Jaccard + shared anchors). Tune phrases in config JSON.

_Same-story clusters use anchor overlap on titles (proper nouns / crisis terms); not neural / semantic dedupe._

#### Same-story (multilingual)

**guerre · iran · israel · moyen-orient · tehran** — _21 sources_

- **[W:8 S:0 G:0]** [EN DIRECT, guerre en Iran : Téhéran et le Moyen-Orient suspendus à la décision de Donald Trump, à quelques heures de la fin de son ultimatum ; Emmanuel Macron convoque un conseil de défense mercredi matin](https://www.lemonde.fr/international/live/2026/04/07/en-direct-guerre-en-iran-a-quelques-heures-de-l-ultimatum-teheran-et-le-moyen-orient-suspendus-a-la-decision-de-donald-trump_6676633_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-07 20:42 UTC_
- **Also** — [Iran-News 7. April: Pakistan drängt Trump zu Fristverlängerung](https://www.spiegel.de/ausland/iran-news-7-april-israelische-armee-warnt-iraner-vor-zugfahrten-a-465732b0-1adb-43a2-8d74-92537b7b115f#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _W:6 S:0 G:0_ · _2026-04-07 21:59 UTC_
- **Also** — [What the US military could do if Iran fails to meet Trump's ultimatum](https://www.bbc.com/news/articles/c98kn1zlxr1o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _W:3 S:0 G:0_ · _2026-04-07 20:55 UTC_
- **Also** — [MAGA influencers push back on Trump on Iran: 'It's time to say no'](https://www.nbcnews.com/politics/donald-trump/trump-maga-allies-push-back-iran-war-time-say-no-rcna267061) — _NBC News — politics_ · _W:3 S:0 G:0_ · _2026-04-07 17:58 UTC_
- **Also** — [Tracking recent US-Israeli strikes on Iranian infrastructure](https://www.bbc.com/news/articles/cx2w0v19gw8o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _W:3 S:0 G:0_ · _2026-04-07 17:15 UTC_

#### Other headlines

- **[W:4 S:0 G:0]** [EN DIRECT, guerre en Ukraine : suivez nos dernières informations](https://www.lemonde.fr/international/live/2026/04/07/en-direct-guerre-en-ukraine-suivez-nos-dernieres-informations_6676836_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-07 20:20 UTC_
- **[W:4 S:0 G:0]** [Trump dice que "toda una civilización morirá esta noche" si Irán no llega a un acuerdo para reabrir el estrecho de Ormuz](https://www.bbc.co.uk/mundo/live/c05d1l13zjnt?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_
- **[W:3 S:0 G:1]** [WHO suspends Gaza medical evacuations after contractor killed by Israeli troops](https://www.bbc.com/news/articles/c4g8pzpw2g2o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-07 13:55 UTC_
- **[W:2 S:0 G:2]** [The U.S. fighter jet was downed in Iran by a shoulder-fired missile](https://www.nbcnews.com/politics/white-house/us-fighter-jet-was-downed-iran-shoulder-fired-missile-rcna266907) — _NBC News — politics_ · _2026-04-07 01:15 UTC_
- **[W:3 S:0 G:0]** [« Le président des Etats-Unis est un fou » : l’escalade verbale de Donald Trump alimente les interrogations sur sa santé mentale](https://www.lemonde.fr/international/article/2026/04/07/le-president-des-etats-unis-est-un-fou-l-escalade-verbale-de-donald-trump-alimente-les-interrogations-sur-sa-sante-mentale_6677941_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-07 22:32 UTC_
- **[W:3 S:0 G:0]** [Le sénateur LR Thierry Meignen visé par une enquête après la plainte de la journaliste Nassira El Moaddem pour des menaces de mort](https://www.lemonde.fr/societe/article/2026/04/07/le-senateur-lr-thierry-meignen-vise-par-une-enquete-apres-la-plainte-de-la-journaliste-nassira-el-moaddem-pour-des-menaces-de-mort_6677935_3224.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-07 21:00 UTC_
- **[W:1 S:2 G:0]** [Voters to decide Wisconsin Supreme Court race and Georgia runoff for Marjorie Taylor Greene's seat](https://www.nbcnews.com/politics/2026-election/wisconsin-supreme-court-race-georgia-runoff-marjorie-taylor-greene-rcna266257) — _NBC News — politics_ · _2026-04-07 09:00 UTC_
- **[W:1 S:2 G:0]** [Supreme Court returns Bannon contempt of Congress case to lower court](https://rollcall.com/2026/04/06/supreme-court-returns-bannon-contempt-of-congress-case-to-lower-court/) — _Roll Call — Congress_
- **[W:2 S:0 G:0]** [Sen. Cassidy says vote to convict Trump in impeachment trial ‘might be’ a liability in primary](https://www.nbcnews.com/meet-the-press/video/sen-cassidy-says-vote-to-convict-trump-in-impeachment-trial-might-be-a-liability-in-primary-260850757963) — _NBC News — politics_ · _2026-04-07 20:42 UTC_
- **[W:2 S:0 G:0]** [Mircea Lucescu, ancien sélectionneur de l’équipe roumaine de football, est mort à 80 ans](https://www.lemonde.fr/disparitions/article/2026/04/07/mircea-lucescu-ancien-selectionneur-de-l-equipe-roumaine-de-football-est-mort-a-80-ans_6677939_3382.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-07 22:16 UTC_
- **[W:2 S:0 G:0]** [Iranians form human chains at bridges and power plants](https://www.bbc.com/news/videos/c4g5j33p6vno?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-07 19:36 UTC_
- **[W:2 S:0 G:0]** [French couple leave Iran after more than three years in jail](https://www.bbc.com/news/articles/clyxk5640wko?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-07 19:18 UTC_
- **[W:2 S:0 G:0]** [Les grands magasins du Printemps coupent à nouveau dans les effectifs, 229 postes vont être supprimés](https://www.lemonde.fr/economie/article/2026/04/07/les-grands-magasins-du-printemps-coupent-a-nouveau-dans-les-effectifs-229-postes-vont-etre-supprimes_6677936_3234.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-07 21:17 UTC_
- **[W:2 S:0 G:0]** [Können sich die USA von Donald Trump erholen?](https://www.spiegel.de/geschichte/koennen-sich-die-usa-von-donald-trump-erholen-a-334cded1-e615-4c4d-a099-a3e160660735#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-04-07 21:13 UTC_
- **[W:2 S:0 G:0]** [JD Vance in Ungarn: US-Vizepräsident unterstützt Viktor Orbán im Wahlkampf](https://www.spiegel.de/ausland/jd-vance-in-ungarn-us-vizepraesident-unterstuetzt-viktor-orban-im-wahlkampf-a-556fa3ee-0a9a-4e74-b62b-7c7f210417a8#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-04-07 20:39 UTC_

## 2a. Geopolitical & military (G-ranked)

_**G** = matches on `geo_military_keyword_phrases` (+ optional locale lists in config). Supports triangulation and war-powers messaging — **verify** claims against primary sources._

- **[W:2 S:0 G:2]** [The U.S. fighter jet was downed in Iran by a shoulder-fired missile](https://www.nbcnews.com/politics/white-house/us-fighter-jet-was-downed-iran-shoulder-fired-missile-rcna266907) — _NBC News — politics_ · _2026-04-07 01:15 UTC_
- **[W:3 S:0 G:1]** [WHO suspends Gaza medical evacuations after contractor killed by Israeli troops](https://www.bbc.com/news/articles/c4g8pzpw2g2o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-07 13:55 UTC_
- **[W:2 S:0 G:1]** [Harris: ‘American people do not support’ Trump ‘threatening to commit war crimes’](https://thehill.com/homenews/administration/5820204-harris-condemns-trump-iran-threat/) — _The Hill — politics_ · _2026-04-07 19:52 UTC_
- **[W:2 S:0 G:1]** [Top Armed Forces Democrat: Trump has ‘become as fanatical as the regime leaders in Tehran’](https://thehill.com/policy/defense/5820132-reed-criticizes-trump-iran-threat/) — _The Hill — politics_ · _2026-04-07 19:37 UTC_
- **[W:2 S:0 G:1]** [Iran rejects temporary ceasefire proposal as Trump's deadline looms](https://www.nbcnews.com/politics/national-security/trumps-deadline-looms-iran-rejects-temporary-ceasefire-proposal-rcna266905) — _NBC News — politics_ · _2026-04-06 21:30 UTC_
- **[W:1 S:0 G:1]** [Iran’s UN envoy says Tehran open to ‘genuine’ talks, rejects temporary ceasefire](https://thehill.com/policy/international/5820282-iran-envoy-un-negotiations/) — _The Hill — politics_ · _2026-04-07 20:21 UTC_
- **[W:1 S:0 G:1]** [How would the US Navy counter Iran's mines?](https://www.defenseone.com/ideas/2026/04/could-navys-lcs-counter-mines-iran/412657/) — _Defense One — All_ · _2026-04-06 16:59 UTC_
- **[W:0 S:0 G:1]** [Pentagon investigators blocked from using 'War Department' in official documents](https://www.defenseone.com/policy/2026/04/pentagon-guidance-lays-out-limits-department-war-title/412676/) — _Defense One — All_ · _2026-04-07 14:58 UTC_
- **[W:0 S:0 G:1]** [As aircraft losses mount, Pentagon wants a software fix to see through the fog of war](https://www.defenseone.com/technology/2026/04/aircraft-losses-mount-pentagon-wants-software-fix-see-through-fog-war/412667/) — _Defense One — All_ · _2026-04-07 04:40 UTC_
- **[W:0 S:0 G:1]** [General Atomics pauses drone wingman flight tests after crash](https://www.defenseone.com/defense-systems/2026/04/general-atomics-pauses-drone-wingman-flight-tests-after-crash/412664/) — _Defense One — All_ · _2026-04-06 20:58 UTC_

## 2b. Civ-mem depth hooks (in-repo essays — not breaking news)

_Token overlap against `docs/civilization-memory/` (build: `python3 scripts/build_civmem_inrepo_index.py build`). **Historical / structural** depth only — not a substitute for dated news. See [civ-mem-draft-protocol](../work-politics/civ-mem-draft-protocol.md). Public copy still needs human approval._

- **{CMC: `minds/CIV–MIND–MEARSHEIMER.md`}** (overlap 2) — _CIV–MIND–MEARSHEIMER — v3.4 Civilizational Memory Codex · Advisory Mind John J. Mearsheimer Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture Status: ACTIVE · CANONICAL · LOCKED Class: MIND (ADVIS..._
- **{CMC: `minds/CIV–MIND–MERCOURIS.md`}** (overlap 2) — _CIV–MIND–MERCOURIS — v3.4 Civilizational Memory Codex · Primary Mind Alexander Mercouris Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture · Proportional Blend Law Status: ACTIVE · CANONICAL · LOC..._
- **{CMC: `notes/research-brief-condition-in-the-traditions.md`}** (overlap 1) — _**Purpose:** Map where Christianity, Islam, Judaism, Hinduism, and Buddhism **explicitly or implicitly** say that something must hold **before** the awaited future (return, restoration, judgment, moksha, nirvana, etc...._

## 3. Lead themes (auto-stub — replace after reading)

### Work-politics / campaign angle
- EN DIRECT, guerre en Iran : Téhéran et le Moyen-Orient suspendus à la décision de Donald Trump, à quelques heures de la fin de son ultimatum ; Emmanuel Macron convoque un conseil de défense mercredi matin
- EN DIRECT, guerre en Ukraine : suivez nos dernières informations
- Trump dice que "toda una civilización morirá esta noche" si Irán no llega a un acuerdo para reabrir el estrecho de Ormuz

**Replace:** 2–3 sentences for principal, district, opposition narrative.

### Work-strategy angle (product / governance / tech)

- Voters to decide Wisconsin Supreme Court race and Georgia runoff for Marjorie Taylor Greene's seat
- Supreme Court returns Bannon contempt of Congress case to lower court
- Cybersécurité : Anthropic restreint le lancement de son dernier modèle d’IA pour prévenir les risques

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
- Review `docs/skill-work/work-politics/revenue-log.md` and confirm it still matches the live campaign context.
- Confirm this is a doc-only week or stage one work-politics milestone so audit continuity stays current.

---

_Generated by `scripts/generate_work_politics_daily_brief.py` (legacy alias: `generate_wap_daily_brief.py`); config `docs/skill-work/work-strategy/daily-brief-config.json`._
