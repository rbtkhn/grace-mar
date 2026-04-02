# Daily brief — work-politics & work-strategy

**Date:** 2026-04-01  
**Assembled:** 2026-04-01 20:42 UTC  
**Recency window (RSS):** last **36h** (undated items may appear)  
**Config:** `docs/skill-work/work-strategy/daily-brief-config.json`

_Operator WORK product. Complete synthesis below; cite sources before any public use._

## 1. Work-politics snapshot

- **Primary:** May 19, 2026 — **days until:** 47
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

- **Civilizational / geopolitics operator ledger:** [STRATEGY.md](STRATEGY.md) — long-horizon CORE + heuristics + §IV operator strategy log (WORK-only; gate only when promoting to Record or milestones).
- Campaign/companion positioning: portable Record, human-only merge, Voice boundary.
- OpenClaw ↔ repo handback and export provenance (see [work-dev workspace](../work-dev/workspace.md)).
- AI-in-schools and identity-substrate narrative vs Alpha-style bundles (see [work-alpha-school](../work-alpha-school/README.md), [work-dev offers](../work-dev/offers.md)).
- Optional: federal / state AI governance headlines when relevant to offers or civ-mem work.
- Long-form tech discourse (GTC-class, Moonshots-class): themes distilled in [external-tech-scan.md](external-tech-scan.md) — use for **strategy vocabulary** and **keyword-season** tuning in [daily-brief-config.json](daily-brief-config.json); **not** unsourced brief facts.
- **Putin — last 48h:** **Coffee menu A — Today** fills **§1d** in the daily brief per [daily-brief-putin-watch.md](daily-brief-putin-watch.md) (web scan + citations); Step 1 does not run this pass.

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

_Window ~2026-03-30 to 2026-04-02 UTC. Menu **C** refresh: added official English wire on Ukraine/ceasefire framing below._ Operator WORK, not Record._

- **2026-04-01 — Talks with Armenian PM Pashinyan (Moscow).** Kremlin-scheduled meeting on strategic partnership, Eurasian integration, South Caucasus / economic and transport-logistics ties; extended to working breakfast. Wire: [TASS — Putin to hold talks with Armenian PM in Moscow on April 1](http://en.tass.ru/politics/2109563).
- **2026-04-01 — Address to International Transport and Logistics Forum (video message).** Official English page summarizes themes: global logistics under geopolitical stress, **Iran / energy markets / Strait of Hormuz**, Russia’s role in “new architecture” of trade, **digital tech and AI** in transport, biennial forum cadence. Primary: [Kremlin — Address to forum participants](http://en.kremlin.ru/events/president/news/79449).
- **2026-03-31 — Phone call with Egypt’s President El-Sisi.** Reporting: Middle East de-escalation, Ukraine, bilateral projects (incl. nuclear); not a substitute for Kremlin readout if you need exact quotes. [Ahram Online — El-Sisi tells Putin Russia can help end war…](https://english.ahram.org.eg/NewsContent/1/1234/564996/Egypt/Foreign-Affairs/ElSisi-tells-Putin-Russia-can-help-end-war-in-call.aspx).
- **2026-03-31 — Peskov / Ukraine (briefing).** Kremlin stresses **lasting peace** over a short truce; says Kyiv’s ceasefire framing lacked a clearly formulated initiative (official English wire). [TASS — Russia needs lasting peace in Ukraine instead of ceasefire](https://en.tass.ru/politics/2109539). Western summary of the “Easter” angle: [The Moscow Times — Kremlin rebuffs Zelensky’s Easter ceasefire proposal](https://www.themoscowtimes.com/2026/03/31/kremlin-rebuffs-zelenskys-easter-ceasefire-proposal-a92387).

## 2. Headlines (ingested RSS)

_Fetch failed for: Reuters — World._

Ranked by **W+S+G** (global keyword lists + per-`locale` maps for W/S; **G** = `geo_military_keyword_phrases`) then recency. Each feed is **recency-sorted** then **capped** (`ingest_caps`: per-feed `max_items` and/or `tier` → `max_items_by_tier`; CLI `--max-per-feed N` overrides all feeds). Optional **same-story** grouping uses `story_anchor_phrases` overlap (Jaccard + shared anchors). Tune phrases in config JSON.

_Same-story clusters use anchor overlap on titles (proper nouns / crisis terms); not neural / semantic dedupe._

#### Same-story (multilingual)

**guerre · iran · israel · moyen-orient · trump** — _7 sources_

- **[W:10 S:0 G:0]** [EN DIRECT, guerre au Moyen-Orient : avant le discours de Donald Trump, l’Iran annonce une vague d’attaques menée contre Israël et des bases américaines dans le Golfe](https://www.lemonde.fr/international/live/2026/04/01/en-direct-guerre-au-moyen-orient-avant-le-discours-attendu-de-donald-trump-l-iran-annonce-une-vague-d-attaques-menee-contre-israel-et-des-bases-americaines-dans-le-golfe_6674837_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-01 20:45 UTC_
- **Also** — [Guerre au Moyen-Orient : comment le plastique et la chimie, ingrédients-clés de l’économie, alimentent l’inflation](https://www.lemonde.fr/economie/article/2026/04/01/guerre-au-moyen-orient-comment-le-plastique-et-la-chimie-ingredients-cles-de-l-economie-alimentent-l-inflation_6675943_3234.html) — _Le Monde — français (France / monde)_ · _fr_ · _W:3 S:0 G:0_ · _2026-04-01 20:00 UTC_
- **Also** — [Polls show consistent majorities opposing military action in Iran after a month of war](https://www.nbcnews.com/politics/trump-administration/polls-show-consistent-majorities-opposing-military-action-iran-month-w-rcna266229) — _NBC News — politics_ · _W:2 S:0 G:0_ · _2026-04-01 18:53 UTC_
- **Also** — [Trump to address nation at critical moment in his war with Iran](https://www.npr.org/2026/04/01/nx-s1-5770093/trump-address-iran-war) — _NPR — national news_ · _W:2 S:0 G:0_ · _2026-04-01 13:48 UTC_
- **Also** — [Trump to address the nation with 'important' update on the Iran war](https://www.nbcnews.com/politics/donald-trump/president-address-nation-important-iran-war-update-karoline-leavitt-rcna266131) — _NBC News — politics_ · _W:2 S:0 G:0_ · _2026-04-01 01:30 UTC_

**nato · trump** — _3 sources_

- **[W:3 S:0 G:1]** [What do Trump's latest comments on leaving Nato mean for the alliance?](https://www.bbc.com/news/articles/c79je4vldq5o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-01 16:31 UTC_
- **Also** — [NATO ambassador says Trump ‘reevaluating’ US involvement in alliance](https://thehill.com/homenews/administration/5811605-trump-considering-nato-exit/) — _The Hill — politics_ · _W:2 S:0 G:1_ · _2026-04-01 19:07 UTC_
- **Also** — [Rubio NATO tweet from 2023 goes viral after Trump threats](https://thehill.com/homenews/administration/5811552-rubio-trump-nato-reconsider/) — _The Hill — politics_ · _W:2 S:0 G:1_ · _2026-04-01 18:54 UTC_

**hezbollah · israel · lebanon** — _2 sources_

- **[W:2 S:0 G:1]** [Israel intensifies Lebanon attacks and hits areas not in Hezbollah's control](https://www.bbc.com/news/articles/cvg07j6yeweo?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-01 10:33 UTC_
- **Also** — [After Israel's invasion, many in southern Lebanon worry they'll never go home](https://www.npr.org/2026/04/01/g-s1-115929/israel-south-lebanon-evacuation) — _NPR — national news_ · _W:1 S:0 G:1_ · _2026-04-01 11:15 UTC_

#### Other headlines

- **[W:5 S:0 G:0]** ["Trump logró un cambio de régimen, pero del régimen marítimo": Irán se burla del presidente de EE.UU. y cobrará peaje en el estrecho de Ormuz](https://www.bbc.com/mundo/articles/c75k3er07q0o?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-04-01 12:53 UTC_
- **[W:4 S:0 G:0]** [EN DIRECT, guerre en Ukraine : Volodymyr Zelensky dit avoir eu une discussion « positive » avec les émissaires américains concernant un cessez-le-feu pour les fêtes de Pâques](https://www.lemonde.fr/international/live/2026/04/01/en-direct-guerre-en-ukraine-volodymyr-zelensky-dit-avoir-eu-une-discussion-positive-avec-les-emissaires-americains-pour-un-cessez-le-feu-pour-les-fetes-de-paques_6675208_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-01 20:34 UTC_
- **[W:4 S:0 G:0]** [Au Brésil, l’élection d’une députée transgenre à la tête d’une commission parlementaire visant à défendre les droits des femmes suscite la polémique](https://www.lemonde.fr/international/article/2026/04/01/au-bresil-l-election-d-une-deputee-transgenre-a-la-tete-d-une-commission-parlementaire-visant-a-defendre-les-droits-des-femmes-suscite-la-polemique_6675935_3210.html) — _Le Monde — français (France / monde)_ · _fr_ · _2026-04-01 19:30 UTC_
- **[W:3 S:0 G:0]** [La conmovedora historia de la madre palestina que se reencontró con su hija evacuada de Gaza después de 2 años](https://www.bbc.com/mundo/articles/c1krvj0zrrzo?at_medium=RSS&at_campaign=rss) — _BBC Mundo — español (Américas / global)_ · _es_ · _2026-04-01 09:31 UTC_
- **[W:3 S:0 G:0]** [China is trying to play peacemaker in the Iran war - will it work?](https://www.bbc.com/news/articles/cze0kz7gr84o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-01 07:16 UTC_
- **[W:2 S:0 G:1]** [Former Trump advisor joins board of Ukraine-focused drone tech company Powerus](https://www.defenseone.com/business/2026/03/former-trump-advisor-joins-board-ukraine-focused-drone-tech-company/412510/) — _Defense One — All_ · _2026-03-31 09:30 UTC_
- **[W:1 S:2 G:0]** [Here are the very rare exceptions to birthright citizenship in the US](https://thehill.com/regulation/court-battles/5811184-birthright-citizenship-exceptions-supreme-court-trump/) — _The Hill — politics_ · _2026-04-01 18:27 UTC_
- **[W:1 S:2 G:0]** [Supreme Court appears skeptical of Trump's effort to limit birthright citizenship](https://www.nbcnews.com/now/video/supreme-court-appears-skeptical-of-trump-s-effort-to-limit-birthright-citizenship-260525125663) — _NBC News — politics_ · _2026-04-01 17:32 UTC_
- **[W:1 S:2 G:0]** [Supreme Court majority seems inclined to rule against Trump on birthright citizenship](https://www.npr.org/2026/04/01/nx-s1-5754762/trump-supreme-court-birthright-citizenship) — _NPR — national news_ · _2026-04-01 13:02 UTC_
- **[W:1 S:2 G:0]** [Trump to Attend Supreme Court Birthright Citizenship Hearing](https://www.today.com/video/supreme-court-weighs-trump-s-bid-to-ban-birthright-citizenship-260503109662) — _NBC News — politics_ · _2026-04-01 12:33 UTC_

## 2a. Geopolitical & military (G-ranked)

_**G** = matches on `geo_military_keyword_phrases` (+ optional locale lists in config). Supports triangulation and war-powers messaging — **verify** claims against primary sources._

- **[W:1 S:0 G:2]** [Last 24 hours saw ‘lowest number’ of Iranian missile and drone attacks, Hegseth says](https://www.defenseone.com/policy/2026/03/last-24-hours-saw-lowest-number-iranian-missile-and-drone-attacks-hegseth-says/412521/) — _Defense One — All_ · _2026-03-31 13:57 UTC_
- **[W:3 S:0 G:1]** [What do Trump's latest comments on leaving Nato mean for the alliance?](https://www.bbc.com/news/articles/c79je4vldq5o?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-01 16:31 UTC_
- **[W:2 S:0 G:1]** [NATO ambassador says Trump ‘reevaluating’ US involvement in alliance](https://thehill.com/homenews/administration/5811605-trump-considering-nato-exit/) — _The Hill — politics_ · _2026-04-01 19:07 UTC_
- **[W:2 S:0 G:1]** [Rubio NATO tweet from 2023 goes viral after Trump threats](https://thehill.com/homenews/administration/5811552-rubio-trump-nato-reconsider/) — _The Hill — politics_ · _2026-04-01 18:54 UTC_
- **[W:2 S:0 G:1]** [Israel intensifies Lebanon attacks and hits areas not in Hezbollah's control](https://www.bbc.com/news/articles/cvg07j6yeweo?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-01 10:33 UTC_
- **[W:2 S:0 G:1]** [Former Trump advisor joins board of Ukraine-focused drone tech company Powerus](https://www.defenseone.com/business/2026/03/former-trump-advisor-joins-board-ukraine-focused-drone-tech-company/412510/) — _Defense One — All_ · _2026-03-31 09:30 UTC_
- **[W:1 S:0 G:1]** [Trump endorses funding ICE and Border Patrol in GOP-only bill](https://thehill.com/homenews/administration/5811446-trump-ice-border-patrol-funding-bill/) — _The Hill — politics_ · _2026-04-01 18:13 UTC_
- **[W:1 S:0 G:1]** [After Israel's invasion, many in southern Lebanon worry they'll never go home](https://www.npr.org/2026/04/01/g-s1-115929/israel-south-lebanon-evacuation) — _NPR — national news_ · _2026-04-01 11:15 UTC_
- **[W:1 S:0 G:1]** [South African army arrive in crime hotspots to help tackle gangs](https://www.bbc.com/news/articles/cx2e78yk09no?at_medium=RSS&at_campaign=rss) — _BBC News — World_ · _2026-04-01 14:35 UTC_
- **[W:1 S:0 G:1]** [Despite month of bombing, Iran retains some missile capability](https://rollcall.com/2026/03/31/despite-month-of-bombing-iran-retains-some-missile-capability/) — _Roll Call — Congress_
- **[W:0 S:0 G:1]** [A Turkish border town known for its cats - in times of peace](https://www.npr.org/2026/04/01/nx-s1-5766197/a-turkish-border-town-known-for-its-cats-in-times-of-peace) — _NPR — national news_ · _2026-04-01 15:54 UTC_
- **[W:0 S:0 G:1]** [Is the U.S. Navy ready to clear sea mines in the Persian Gulf?](https://www.npr.org/2026/04/01/nx-s1-5766222/mines-persian-gulf-strait-navy-lcs) — _NPR — national news_ · _2026-04-01 15:54 UTC_
- **[W:0 S:0 G:1]** [Ukrainian drone holds position for 6 weeks](https://defenceleaders.com/news/ukrainian-combat-robot-holds-frontline-position-for-six-weeks-in-sign-of-growing-ugv-maturity/) — _Hacker News — front page_ · _2026-04-01 17:57 UTC_
- **[W:0 S:0 G:1]** [Defense Business Brief: The Navy’s MUSV pivot; NGA taps Vantor for $2.3M spy satellite contract; and a bit more](https://www.defenseone.com/business/2026/04/defense-business-brief-navys-musv-pivot-nga-taps-vantor-23m-spy-satellite-contract-and-bit-more/412546/) — _Defense One — All_ · _2026-04-01 12:00 UTC_

## 2b. Civ-mem depth hooks (in-repo essays — not breaking news)

_Token overlap against `docs/civilization-memory/` (build: `python3 scripts/build_civmem_inrepo_index.py build`). **Historical / structural** depth only — not a substitute for dated news. See [civ-mem-draft-protocol](../work-politics/civ-mem-draft-protocol.md). Public copy still needs human approval._

- **{CMC: `minds/CIV–MIND–MEARSHEIMER.md`}** (overlap 2) — _CIV–MIND–MEARSHEIMER — v3.4 Civilizational Memory Codex · Advisory Mind John J. Mearsheimer Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture Status: ACTIVE · CANONICAL · LOCKED Class: MIND (ADVIS..._
- **{CMC: `minds/CIV–MIND–MERCOURIS.md`}** (overlap 2) — _CIV–MIND–MERCOURIS — v3.4 Civilizational Memory Codex · Primary Mind Alexander Mercouris Cognitive–Linguistic Signature Layer Simplified Polyphony Architecture · Proportional Blend Law Status: ACTIVE · CANONICAL · LOC..._
- **{CMC: `essays/ONE-SUBJECT-MANY-TONGUES.md`}** (overlap 2) — _### Islam and Christianity and the Shared Reference --- The world's traditions speak in different languages. They disagree about God, revelation, and the path to salvation. That difference has often been taken to mean..._

## 3. Lead themes (auto-stub — replace after reading)

### Work-politics / campaign angle
- EN DIRECT, guerre au Moyen-Orient : avant le discours de Donald Trump, l’Iran annonce une vague d’attaques menée contre Israël et des bases américaines dans le Golfe
- "Trump logró un cambio de régimen, pero del régimen marítimo": Irán se burla del presidente de EE.UU. y cobrará peaje en el estrecho de Ormuz
- EN DIRECT, guerre en Ukraine : Volodymyr Zelensky dit avoir eu une discussion « positive » avec les émissaires américains concernant un cessez-le-feu pour les fêtes de Pâques

**Replace:** 2–3 sentences for principal, district, opposition narrative.

### Work-strategy angle (product / governance / tech)

- Here are the very rare exceptions to birthright citizenship in the US
- Supreme Court appears skeptical of Trump's effort to limit birthright citizenship
- Supreme Court majority seems inclined to rule against Trump on birthright citizenship

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
