# Daily brief — work-politics & work-strategy

**Date:** 2026-04-03  
**Assembled:** 2026-04-03 16:33 UTC  
**Recency window (RSS):** last **36h** (undated items may appear)  
**Config:** `docs/skill-work/work-strategy/daily-brief-config.json`

_Operator WORK product. Complete synthesis below; cite sources before any public use._

## 1. Work-politics snapshot

- **Primary:** May 19, 2026 — **days until:** 45
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
- **Putin — last 48h:** **Coffee menu C — Strategy (daily brief)** fills **§1d** in the daily brief per [daily-brief-putin-watch.md](daily-brief-putin-watch.md) (web scan + citations); Step 1 does not run this pass.
- **Weak signal — §1e:** Include one weak signal worth watching when a credible candidate exceeds threshold; test any historical parallel with a compact analogy audit before carrying it into synthesis ([weak-signals.md](weak-signals.md), [weak-signal-template.md](weak-signal-template.md), [analogy-audit-template.md](analogy-audit-template.md)).
- **Rome / Vatican (work-strategy-rome):** When Holy See or papal lines intersect multipolar or legitimacy stories, run the [ROME-PASS](work-strategy-rome/ROME-PASS.md) skeleton (vatican.va + wire + optional civ-mem); file notes or exemplars under [work-strategy-rome/notes/](work-strategy-rome/notes/).

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

_Rolling window ~2026-04-01 16:33 UTC → 2026-04-03 16:33 UTC (brief assembly time). Primary: Kremlin English + TASS._

- **2026-04-02 — Telephone conversation with Crown Prince and Prime Minister of Saudi Arabia Mohammed bin Salman:** Kremlin readout: both sides stressed the need for a rapid cessation of hostilities in the Middle East and intensified political and diplomatic efforts toward a lasting settlement; also discussed oil market stability and OPEC+ coordination. — [President of Russia — event 79458](http://en.kremlin.ru/events/president/news/79458)
- **2026-04-02 — Peskov on Iran / US (briefing to press):** Moscow is not sure what Washington will do next on Iran; heard Trump’s statements about stopping hostilities but “we don’t know what will happen in reality”; Middle East should be “shepherded to the peace track” as soon as possible. — [TASS — IN BRIEF](https://tass.com/world/2110909)
- **2026-04-03 — Peskov (wire summary):** Putin “continues to work on” the escalating Middle East situation; an international telephone conversation was expected later in the day. Treat as **secondary** until mirrored on Kremlin English; use for orientation only. — [Caliber.az English](https://caliber.az/en/post/putin-continues-work-on-middle-east-situation-kremlin-says)

_Automated fetch of Kremlin “by date” English listings failed (timeout); add any same-day rows from [Kremlin — president / events](http://en.kremlin.ru/events/president) if needed before ship._

## 1e. Weak signal worth watching

_Operator block per [weak-signal-template.md](weak-signal-template.md) and [weak-signals.md](weak-signals.md). One compact weak signal when a credible candidate exists (low/medium confidence only). If nothing clears the bar, use: **No credible weak signal exceeded the threshold today.** When a historical parallel is in play, summarize a short analogy audit ([analogy-audit-template.md](analogy-audit-template.md)) here._

**No credible weak signal exceeded the threshold today.** Salient lines were already high-confidence crisis coverage in §2 (Iran/U.S./Israel, NATO); no separate low-probability tail worth isolating here without a dedicated analogy audit.

## 2. Headlines (ingested RSS)

_Fetch failed for: Reuters — World._

Ranked by **W+S+G** (global keyword lists + per-`locale` maps for W/S; **G** = `geo_military_keyword_phrases`) then recency. Each feed is **recency-sorted** then **capped** (`ingest_caps`: per-feed `max_items` and/or `tier` → `max_items_by_tier`; CLI `--max-per-feed N` overrides all feeds). Optional **same-story** grouping uses `story_anchor_phrases` overlap (Jaccard + shared anchors). Tune phrases in config JSON.

_Same-story clusters use anchor overlap on titles (proper nouns / crisis terms); not neural / semantic dedupe._

#### Same-story (multilingual)

**iran · pentagon · trump** — _3 sources_

- **[W:3 S:0 G:1]** [Live updates: Iran shoots down US F-15; White House’s 2027 budget seeks $1.5T for Pentagon](https://thehill.com/homenews/administration/5813088-live-updates-trump-iran-doj-2027-budget/) — _The Hill — politics_ · _2026-04-03 15:15 UTC_
- **Also** — [Iran downs a U.S. F-15 jet and hits Gulf refineries as the war rounds its 5th week](https://www.npr.org/2026/04/03/g-s1-116314/iran-hits-gulf-refineries-as-trump-warns-u-s-will-attack-iranian-bridges-power-plants) — _NPR — national news_ · _W:2 S:0 G:0_ · _2026-04-03 06:29 UTC_
- **Also** — [Takeaways from Trump's tough week, as war and gas prices take a toll](https://www.npr.org/2026/04/03/nx-s1-5771684/trump-iran-war-gas-prices-bondi) — _NPR — national news_ · _W:2 S:0 G:0_ · _2026-04-03 05:00 UTC_

#### Other headlines

- **[W:4 S:0 G:0]** [EN DIRECT, guerre en Ukraine : Volodymyr Zelensky estime qu’il n’y a aucun signal que les Etats-Unis suspendent leurs livraisons d’armes à l’Ukraine](https://www.lemonde.fr/international/live/2026/04/03/en-direct-guerre-en-ukraine-volodymyr-zelensky-estime-qu-il-n-y-a-aucun-signal-que-les-etats-unis-suspendent-leurs-livraisons-d-armes-a-l-ukraine_6675208_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-03 16:50 UTC_
- **[W:4 S:0 G:0]** ["Sé serio... no hables todos los días": Macron critica la postura de Trump respecto a Irán y dice que sus comentarios sobre su esposa fueron "poco elegantes"](https://www.bbc.com/mundo/articles/c3r39vlw85xo?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-04-02 22:05 UTC_
- **[W:3 S:0 G:1]** [As Trump rails against NATO, secretary general heads to Washington](https://www.nbcnews.com/politics/white-house/trump-rails-nato-secretary-general-heads-dc-rcna266423) — _NBC News — politics_ · _2026-04-02 21:37 UTC_
- **[W:3 S:0 G:0]** [Iran-Krieg: US-Kampfjet abgeschossen – Suche nach Besatzung](https://www.spiegel.de/ausland/iran-us-kampfjet-abgeschossen-suche-nach-besatzung-a-38c5d01b-625b-4240-873e-66d56b32026d#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-04-03 16:44 UTC_
- **[W:3 S:0 G:0]** [El Pentágono obliga a dimitir al jefe del Estado Mayor del Ejército de EE.UU. en medio de las dudas por la guerra contra Irán](https://www.bbc.com/mundo/articles/cg735p9jnkpo?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-04-03 08:13 UTC_
- **[W:3 S:0 G:0]** ["Ya no te considero mi hermana": las peleas por la guerra que están dividiendo familias en Irán](https://www.bbc.com/mundo/articles/cgk0d8drle4o?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-04-03 03:13 UTC_
- **[W:2 S:0 G:1]** [Van Hollen: Iran ‘nowhere near’ any ICBM that can reach US](https://thehill.com/homenews/senate/5814762-chris-van-hollen-iran-icbm-missiles-middle-east-conflict/) — _The Hill — politics_ · _2026-04-03 15:05 UTC_
- **[W:2 S:0 G:0]** [Couric: Trump mail-in voting order, national voting list part of effort to ‘scare election workers’](https://thehill.com/blogs/in-the-know/5814876-couric-trump-mail-in-voting-order-national-voting-list-part-of-effort-to-scare-election-workers/) — _The Hill — politics_ · _2026-04-03 16:08 UTC_
- **[W:2 S:0 G:0]** [تصريحات إسرائيلية: تجريد حزب الله من سلاحه ليس من أهداف الحرب في الوقت الراهن](https://www.france24.com/ar/%D9%81%D9%8A%D8%AF%D9%8A%D9%88/20260403-%D8%AA%D8%B5%D8%B1%D9%8A%D8%AD%D8%A7%D8%AA-%D8%A5%D8%B3%D8%B1%D8%A7%D8%A6%D9%8A%D9%84%D9%8A%D8%A9-%D8%AA%D8%AC%D8%B1%D9%8A%D8%AF-%D8%AD%D8%B2%D8%A8-%D8%A7%D9%84%D9%84%D9%87-%D9%85%D9%86-%D8%B3%D9%84%D8%A7%D8%AD%D9%87-%D9%84%D9%8A%D8%B3-%D9%85%D9%86-%D8%A3%D9%87%D8%AF%D8%A7%D9%81-%D8%A7%D9%84%D8%AD%D8%B1%D8%A8-%D9%81%D9%8A-%D8%A7%D9%84%D9%88%D9%82%D8%AA-%D8%A7%D9%84%D8%B1%D8%A7%D9%87%D9%86) — _France 24 — العربية (MENA)_ · _ar_ · _2026-04-03 16:02 UTC_
- **[W:2 S:0 G:0]** [« Véronique », sur France 3 : Véronique Sanson, une « drôle de vie » en chansons](https://www.lemonde.fr/culture/article/2026/04/03/veronique-sur-france-3-veronique-sanson-une-drole-de-vie-en-chansons_6676396_3246.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-03 18:00 UTC_
- **[W:2 S:0 G:0]** [Trump seeks massive $1.5tn for defence alongside cuts in domestic spending](https://www.bbc.com/news/articles/crr1q4kjvn2o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-03 15:45 UTC_
- **[W:2 S:0 G:0]** [Trumps Rausschmisse: Wer ist nach Pam Bondi und Kristi Noem dran?](https://www.spiegel.de/ausland/trumps-rausschmisse-wer-ist-nach-pam-bondi-und-kristi-noem-dran-a-f45d1fd5-ce0e-4f41-89b8-a4dbeb0e7ae9#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-04-03 17:06 UTC_
- **[W:2 S:0 G:0]** [Iran verfügt offenbar noch immer über erhebliches Raketenarsenal und Tausende Drohnen](https://www.spiegel.de/ausland/iran-verfuegt-offenbar-noch-immer-ueber-erhebliches-raketenarsenal-und-tausende-drohnen-a-c05816b7-48ee-4a73-be42-030b6b2d6fa6#ref=rss) — _Der Spiegel — Deutsch (Schlagzeilen)_ · _de_ · _2026-04-03 16:16 UTC_
- **[W:2 S:0 G:0]** [US jobs surge unexpectedly in March despite Iran war](https://www.bbc.com/news/articles/crk165g4vv3o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-03 13:35 UTC_
- **[W:2 S:0 G:0]** [Experts dispute US account of deadly Iran sports hall strike in Lamerd](https://www.bbc.com/news/articles/c4gx8e1x5j3o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-03 13:16 UTC_
- **[W:2 S:0 G:0]** [International law experts allege violations in Iran war](https://www.bbc.com/news/articles/cy91x2n29nlo?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-03 11:53 UTC_
- **[W:2 S:0 G:0]** [Trump removes US Attorney General Pam Bondi](https://www.bbc.com/news/articles/ce843ge47z4o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-03 11:42 UTC_

## 2a. Geopolitical & military (G-ranked)

_**G** = matches on `geo_military_keyword_phrases` (+ optional locale lists in config). Supports triangulation and war-powers messaging — **verify** claims against primary sources._

- **[W:3 S:0 G:1]** [Live updates: Iran shoots down US F-15; White House’s 2027 budget seeks $1.5T for Pentagon](https://thehill.com/homenews/administration/5813088-live-updates-trump-iran-doj-2027-budget/) — _The Hill — politics_ · _2026-04-03 15:15 UTC_
- **[W:3 S:0 G:1]** [As Trump rails against NATO, secretary general heads to Washington](https://www.nbcnews.com/politics/white-house/trump-rails-nato-secretary-general-heads-dc-rcna266423) — _NBC News — politics_ · _2026-04-02 21:37 UTC_
- **[W:2 S:0 G:1]** [Van Hollen: Iran ‘nowhere near’ any ICBM that can reach US](https://thehill.com/homenews/senate/5814762-chris-van-hollen-iran-icbm-missiles-middle-east-conflict/) — _The Hill — politics_ · _2026-04-03 15:05 UTC_
- **[W:1 S:0 G:1]** [International law experts: US strikes on Iran may have amounted to war crimes](https://thehill.com/policy/defense/5815014-war-crimes-international-law-letter-us-iran/) — _The Hill — politics_ · _2026-04-03 16:07 UTC_
- **[W:1 S:0 G:1]** [I prefer OG style websites – what are yours?](https://news.ycombinator.com/item?id=47627255) — _Hacker News — front page_ · _2026-04-03 14:45 UTC_
- **[W:1 S:0 G:1]** [Pete Hegseth asks US Army's top general to step down](https://www.bbc.com/news/articles/cn8d63v058zo?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-03 13:03 UTC_
- **[W:1 S:0 G:1]** [Who is Christopher LaNeve, set to lead the US Army?](https://www.bbc.com/news/articles/clye2e85dwjo?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-03 11:52 UTC_
- **[W:1 S:0 G:1]** [‘It’s drones fighting drones’: Ukrainian officer offers inside look at roboticized war](https://www.defenseone.com/threats/2026/04/drones-ukraine-officer-robot-war/412597/) — _Defense One — All_ · _2026-04-03 00:01 UTC_
- **[W:0 S:0 G:1]** [GOP rep on Hegseth firing Army chief of staff: ‘I will look into it immediately’](https://thehill.com/policy/defense/5814904-rich-mccmormick-pete-hegseth-army-chief-of-staff-firing/) — _The Hill — politics_ · _2026-04-03 15:23 UTC_
- **[W:0 S:0 G:1]** [US Military Destroys Bridge Near Tehran in New Airstrike](https://www.today.com/video/us-military-destroys-bridge-near-tehran-in-new-airstrike-260651589549) — _NBC News — politics_ · _2026-04-03 11:22 UTC_
- **[W:0 S:0 G:1]** [Hegseth forces out Army’s top general](https://www.nbcnews.com/nightly-news/video/hegseth-forces-out-army-s-top-general-260616261974) — _NBC News — politics_ · _2026-04-02 23:01 UTC_
- **[W:0 S:0 G:1]** [Hegseth forces out Army’s top general in ‘widely anticipated’ move](https://www.defenseone.com/policy/2026/04/hegseth-forces-out-armys-top-general-widely-anticipated-move/412603/) — _Defense One — All_ · _2026-04-02 18:29 UTC_
- **[W:0 S:0 G:1]** [Pete Hegseth fires Army's top officer and two other generals](https://www.nbcnews.com/politics/national-security/pete-hegseth-forces-army-chief-staff-randy-george-rcna266491) — _NBC News — politics_ · _2026-04-02 21:48 UTC_

## 2b. Civ-mem depth hooks (in-repo essays — not breaking news)

_Token overlap against `docs/civilization-memory/` (build: `python3 scripts/build_civmem_inrepo_index.py build`). **Historical / structural** depth only — not a substitute for dated news. See [civ-mem-draft-protocol](../work-politics/civ-mem-draft-protocol.md). Public copy still needs human approval._

- **{CMC: `minds/CIV–MIND–MEARSHEIMER.md`}** (overlap 2) — _CIV–MIND–MEARSHEIMER — v3.4 Civilizational Memory Codex · Advisory Mind John J. Mearsheimer Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture Status: ACTIVE · CANONICAL · LOCKED Class: MIND (ADVIS..._
- **{CMC: `minds/CIV–MIND–MERCOURIS.md`}** (overlap 2) — _CIV–MIND–MERCOURIS — v3.4 Civilizational Memory Codex · Primary Mind Alexander Mercouris Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture · Proportional Blend Law Status: ACTIVE · CANONICAL · LOC..._
- **{CMC: `essays/UNIVERSAL-LOVE-AND-MASTERY.md`}** (overlap 2) — _### Only Through Universal Love Can We Master the Universe --- This essay states a single thesis and draws out its consequences. The thesis is: **only through universal love can we master the universe.** It is a theol..._

## 3. Lead themes (auto-stub — replace after reading)

### Work-politics / campaign angle
- EN DIRECT, guerre en Ukraine : Volodymyr Zelensky estime qu’il n’y a aucun signal que les Etats-Unis suspendent leurs livraisons d’armes à l’Ukraine
- "Sé serio... no hables todos los días": Macron critica la postura de Trump respecto a Irán y dice que sus comentarios sobre su esposa fueron "poco elegantes"
- Live updates: Iran shoots down US F-15; White House’s 2027 budget seeks $1.5T for Pentagon

**Replace:** 2–3 sentences for principal, district, opposition narrative.

### Work-strategy angle (product / governance / tech)

- France's Muslim gathering ban overturned by courts
- Courts likely to block Trump’s effort to curtail mail-in voting
- Beware Dr. Chatbot: Privacy laws don’t protect health care data from AI

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
