# Strategy notebook — operator preferences

**Status:** ACTIVE  
**Set:** 2026-04 (from multiple-choice questionnaire)  
**Governed by:** [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) — this file **narrows** daily practice; it does not replace architecture for repo-wide defaults (e.g. architecture still describes a **~1000w** consolidated **`days.md`** daily target where no override applies, and a **500–1000w** target per **`strategy-page`** prose body on **EOD compose**). **`weave` (operator token) is deprecated** — use **end-of-day strategy session** / **EOD notebook compose**; see architecture § *End-of-day strategy session*.  
**Skill contract:** Together with the architecture doc and [daily-strategy-inbox.md](daily-strategy-inbox.md), this file is **part of** [`skill-strategy`](../../../../.cursor/skills/skill-strategy/SKILL.md) — operator defaults the skill **must** apply on a **`strategy`** pass; not optional flavor beside the skill.

---

## Summary

| Area | Preference |
|------|------------|
| **Daily length** | **Variable by day** — no fixed default word budget. |
| **Minimum `days.md` sections** | **`### Signal` · `### Judgment` · `### Links`** only. |
| **EOD compose prose register** | **Popular-academic** by default — reader-facing **Signal / Judgment** in `days.md` after the **EOD strategy session**; avoid **internal repo nicknames**, **operator-only path tokens**, and **backend shorthand** in the **notebook spine** (spell out ideas or use public equivalents). Operator docs and inbox may keep technical labels. Aligns with [skill-strategy Session hygiene](../../../../.cursor/skills/skill-strategy/SKILL.md) § *Session hygiene*. |
| **Inbox vs notebook** | **Raw paste and URL dumps** → [daily-strategy-inbox.md](daily-strategy-inbox.md); **full verbatim** → [`raw-input/`](raw-input/README.md). **Notebook** (`days.md` + **`strategy-page`** blocks in expert **`thread.md`**) = **synthesis + key links**, not mirrors of the inbox or **`raw-input/`**. |
| **Expert corpus (`thread`)** | Inbox lines with **`thread:<expert_id>`** → operator **`thread`** rebuilds per-expert **`experts/<expert_id>/thread.md`** machine layer (and transcripts) — **`python3 scripts/strategy_thread.py`** — **not** **EOD compose** (no `days.md` / page composition). Architecture § *Thread (terminology)*. |
| **Compiled views (derived)** | **Refresh-only** multi-expert snapshots under [`compiled-views/`](compiled-views/README.md) — **`python3 scripts/compile_strategy_view.py`**; **not** SSOT (threads + `strategy-page` blocks are). Polyphony + operator-as-conductor discipline: [SYNTHESIS-OPERATING-MODEL.md](SYNTHESIS-OPERATING-MODEL.md) §§ 7–8; architecture § *Compiled views (derived)*. |
| **Expert thread journal (verbatim-forward)** | **`transcript.md`** holds **verbatim SSOT**; **`thread.md`** machine layer **echoes** expert speech each **`thread`** run; **journal layer** = **light gloss** (stubs, pins, short cross-check scope), **quote-led** months allowed — **not** long assistant paraphrase of the expert. Operator **[`docs/skill-write/`](../../../../docs/skill-write/write-operator-preferences.md)** applies to **Locals / X / PH**, not to on-disk thread composition. Architecture § *Thread (terminology)*. |
| **EOD compose → page structure** | **Promotion choice** — what lands under **Signal** vs **Judgment** vs **Links** vs **Open** follows **what you choose in the EOD session**, not inbox length or equal padding per section. **Same-day iteration** within one session **merges into one** `## YYYY-MM-DD` block (merge, don’t duplicate). See [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Compose choice and section weighting*. |
| **`days.md` heading dates (anti-split)** | **`## YYYY-MM-DD`** names the **compose / continuity day**, not “operator uploaded files on this calendar day” and **not** a mandatory mirror of **`Accumulator for:`** or inbox **`### … YYYY-MM-DD`** subsection titles. **Do not** open extra bottom **`##`** blocks **only** because the local accumulator rolled forward or a **wire byline** differs — **consolidate**; put external dates in **Signal / Links**; add a short **compose date note** (legacy: **weave date note**) when **operator boundary** and **publication dates** diverge. [STRATEGY-NOTEBOOK-ARCHITECTURE.md § `days.md` date keys](STRATEGY-NOTEBOOK-ARCHITECTURE.md#days-md-date-semantics); [.cursor/rules/strategy-notebook-days-date-semantics.mdc](../../../../.cursor/rules/strategy-notebook-days-date-semantics.mdc). |
| **EOD page-shape menu** | In the **EOD strategy session**, assistants present **4–6** labeled options (**page thesis / shape / content emphasis**) **before** writing to disk—see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *EOD compose — page-shape menu* and § *Page design and notebook-use jobs*. Each stub should **name the implied notebook-use job(s)** (same seven vocations as expert tags — `orient`, `negotiate`, `validate`, `authorize`, `stress-test`, `narrate`, `historicize`) in a **thesis-first** line, not as a tag-only menu. Each option should be **scoped** so a resulting **`strategy-page`** (when in scope) can be written within **500–1000 words** in Signal/Judgment/Open (e.g. “thin page + `days.md` carry,” “full in-thread synthesis,” “Links-heavy / Judgment-tight”). Operator picks a letter, says **`no menu`**, or names the shape explicitly. **Optional — full MCQ stack:** When the operator wants **session type → lanes → promotion → shape → (page action) → `days.md` mode** before any prose, follow [EOD-MCQ-PROTOCOL.md](EOD-MCQ-PROTOCOL.md) (architecture § *EOD MCQ protocol (v1)*). |
| **Compose skeleton (primary expert)** | **S1–S5** — when the **EOD session** names one **primary** `strategy-expert` (or MC pick), default **Signal / Judgment / Links / Open weighting** follows § *Weave skeletons (S1–S5)* (heading unchanged for grep); multi-expert analysis stays in the **`strategy-page`** body (and compressed `days.md` when composed there); primary = **filing / spine**, not sole epistemic authority. |
| **Page length (EOD output)** | **`strategy-page`:** target **500–1000 words** in prose sections (`wc -w` on body above **Technical appendix**). Router / deferral pages may sit **below 500** only when prose is **explicitly** routed to **`days.md`** per architecture. |
| **Batch-analysis / visual snapshot** | Inbox **`batch-analysis | …`** lines stay **markdown SSOT**; a future **derived** JSON snapshot for a **visual UI** should emit **`batch_analysis_refs[]`** with **`expert_ids`**, per-row **`confidence`** (`high` \| `medium` \| `low` \| `none`), and **`sources`** (`crosses` / `thread_in_line` / `upstream_verify` / `label_alias`) — **architecture** § *Batch-analysis — machine parse & visual snapshot*. Thematic batches with **no** indexed **`thread:`** may legitimately show **empty** `expert_ids`. |
| **Judgment priority** | **Structural first** — power, incentives, constraints; narrative second. |
| **Islamabad / US–Iran / pause** | When the day touches this thread, **always capture scope fights**: what is in/out of the **pause**, **Lebanon**, **Hormuz** definition. |
| **US–Iran kinetic likelihood (cross-expert)** | Standing **hypothesis object**: near-term **large-scale U.S. kinetic** pressure on **Iran** (major new strike wave / sustained campaign framing) vs **diplomatic off-ramp** — **tracked** when experts speak to it; **`N/A`** for off-topic lanes. SSOT stub: [US-IRAN-KINETIC-TRACKER.md](US-IRAN-KINETIC-TRACKER.md); full rules § *US–Iran kinetic likelihood (cross-expert track)* below. |
| **Leo XIV / Holy See / Rome (primary thread)** | **Voice** = papal / Holy See moral–diplomatic lines (**Leo XIV**, `@Pontifex`, audiences). **Hub** = [work-strategy-rome](../work-strategy-rome/README.md) + [ROME-PASS](../work-strategy-rome/ROME-PASS.md). When the day touches this thread, **keep planes separate** from Beltway mechanics: **IHL / legitimacy vocabulary** is not a forecast of **kinetic** facts; land **Judgment** with **dated** vatican.va or press-office URLs when claiming official text (see ROME-PASS source order). If **Lebanon** (or other crises) appears in **both** expert-commentary and papal lines, prefer **two bullets** or **Thesis A / B** — do not merge registers without verify. |
| **JD Vance / VP channel (primary thread)** | **Voice** = **Vice President** public lines, travel, and **White House** readouts (not Senate archive unless window-relevant). **Hub** = [daily-brief-jd-vance-watch.md](../daily-brief-jd-vance-watch.md) (**§1e** in daily briefs — coffee **C** pass). When the day touches **U.S.–Iran**, **Islamabad**, **war powers**, or **coalition** framing, **tag whether Vance is acting as channel** (delegation lead, “final offer” voice, restraint narrative) vs **atmospheric** quote — separate **official** URL from **cable analysis**. If **Vance** and **Pentagon / State** lines **diverge** on scope (**Lebanon**, **Hormuz**, pause), **two bullets** or **Thesis A / B**; do not collapse into one “White House says.” |
| **Vladimir Putin / Kremlin (primary thread)** | **Voice** = **Russian President** public lines, **Kremlin** schedule (events, calls, transcripts). **Hub** = [daily-brief-putin-watch.md](../daily-brief-putin-watch.md) (**§1d** — coffee **C** pass, rolling **48h**). When the day touches **Ukraine**, **Iran** (Russia as actor), **NATO**, or **multilateral** ceasefire framing, separate **Kremlin-primary** quotes from **Western wire paraphrase**; add **Russian-language or Kremlin-primary** triangulation per [daily-brief-native-international-pass.md](../daily-brief-native-international-pass.md) when Russia is load-bearing. If **Putin** lines and **U.S. / allied** readouts **diverge** on **facts or scope**, **two bullets** or **Thesis A / B** — do not merge **personality** headlines with **operational** claims without URLs. |
| **PRC / Beijing (primary thread)** | **Voice** = **People’s Republic of China** **party–state** lines (**MFA**, **summits**, major **state** readouts). **Hub** = [daily-brief-prc-watch.md](../daily-brief-prc-watch.md) (**§1g** — coffee **C** pass, rolling **48h**). When the day touches **U.S.–China**, **cross-strait**, **Indo-Pacific**, **trade / sanctions**, or **PRC** as **named** party beside **Russia** / **Iran** / **U.S.** stories, separate **MFA / state-primary** wording from **Western** “China” **analysis**; add **Mandarin-primary** triangulation per [daily-brief-native-international-pass.md](../daily-brief-native-international-pass.md) when the PRC thread is load-bearing. If **Beijing** and **Washington** lines **diverge** on **terms or scope**, **two bullets** or **Thesis A / B**. |
| **Islamic Republic of Iran (primary thread)** | **Voice** = **Iranian state** lines (**MFA**, **presidency**, **IRNA** / major **state-adjacent** wires). **Hub** = [daily-brief-iran-watch.md](../daily-brief-iran-watch.md) (**§1h** — coffee **C** pass, rolling **48h**). **Not** a substitute for the **Islamabad** bargaining **framework** ([islamabad-operator-index.md](../islamabad-operator-index.md), gap matrices)—use **both**: framework for **trade space**, IRI watch for **what Tehran says** on **pause**, **Hormuz**, **Lebanon**, **nuclear** terms. Separate **Persian-primary** or **MFA** quotes from **Western** “Iran” **digest**; add **Persian** triangulation per [daily-brief-native-international-pass.md](../daily-brief-native-international-pass.md) when the Iran thread is load-bearing. If **Tehran** and **Washington** lines **diverge** on **facts or scope**, **two bullets** or **Thesis A / B**. |
| **Predictive History (work-jiang)** | **Episodic** — cite when you **actually** engaged lecture/corpus that day; no standing PH obligation in the notebook. |
| **Lenses (B / M / Merc)** | After **substantive** notebook-relevant work, assistant **offers three one-liners** — operator **picks or skips** (see [strategy-minds-granular.mdc](../../../../.cursor/rules/strategy-minds-granular.mdc)). |
| **Where lens depth lives** | **Daily brief mind shells** and **`minds/outputs/`** as needed; **strategy-notebook day block stays thin**. |
| **Inbox → `days.md`** | **EOD strategy session** (default **once per local day**), optionally beside **`dream`**, or **breaking-glass** explicit override — assistants do **not** append `days.md` on ingest alone (see [daily-strategy-inbox.md](daily-strategy-inbox.md)). |
| **Promotion to `STRATEGY.md`** | **Weekly** when the **week** had a **clear thesis** (not only rare milestones). |
| **STATUS.md** | **Minimal** — last entry / pointer; no rich dashboard unless asked. |
| **Uncertainty** | Emphasize **narrative and framing risk** over formal numeric confidence tags. |
| **Analogue-app patterns (Metaculus / Kialo / etc.)** | **Do not** add **numeric or ordinal confidence** tags, **forecast scoreboards**, or **argument-tree “impact” / branch-vote** metadata to default notebook or `skill-strategy` output — they **conflict** with the **Uncertainty** row unless this file is **revised** to allow them. Prefer **Thesis A / B** and falsifiers in `meta.md` / expert index. |
| **Conflicting experts** | **Two Judgment bullets** — **Thesis A** / **Thesis B** — preserve tension; no forced merge. |
| **Daily brief — LLM or paste supplements** | **Same artifact and discipline** as **`generate_work_politics_daily_brief.py` output:** pasted or LLM-produced “daily strategic” text lives in **`docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md`** (usually **§1f** per [weak-signal-template.md](../weak-signal-template.md)) — **not** a separate “overlay” product. **Never** substitute for **§1d–§1h** watch passes or **tier-A** URLs until verified; **same** **hypothesis + falsifiers** and **`strategy + verify`** / fact-check triage before **`days.md` Judgment** at **EOD compose**. **Do not** import **unsourced** counts, meeting quotes, or same-day **macro tables** into **Signal/Judgment** as facts. |
| **Expert-thread backfill / arc refine** | **Optional tooling** on **`strategy-expert-*-thread.md`:** `scripts/backfill_expert_thread.py` inserts a labeled reconstructed arc **above** the machine block; `scripts/refine_backfilled_thread_arc.py` adds **derivative** month-level scan lines only when the backfill already has **`### YYYY-MM`** sections with dated bullets — **skip** refine for empty windows or sparse backfills (the refine script **no-ops** when there are no month headings). **`scripts/score_backfilled_thread_sources.py`** (optional) tags each dated bullet with conservative **high / medium / low** strength from the existing `_Source:_` line — **no-op** when there are no month sections. |

---

<a id="weave-skeletons-s1-s5"></a>

## Weave skeletons (S1–S5)

**Purpose:** Renames and extends the earlier **three-skeleton** idea (mechanics / legitimacy / domestic) into **five** default **spines** for a **`strategy-page`** or day block when **`weave`** picks a **primary** `strategy-expert`. The skeleton sets **section weighting** and **Open** pressure; **all other experts** appear as **synthesis, seams, and falsifiers** in the page **body** (and in `days.md` when woven there). **Primary** = navigation and default structure, not a claim that one voice owns the truth.

### Definitions + failure modes (one line each)

| ID | Name | What leads | **Failure mode** |
|----|------|------------|-------------------|
| **S1** | **Operations & mechanics** | Hulls, ORBAT, closure, naval facts, OSINT material claims; Judgment stresses **tier / falsify**. | **Grand-bargain, legitimacy stack, or MFA speech** smuggled in as **hull facts** without naming the **register shift**. |
| **S2** | **Power, alliances & incentives** | Structural map — who can afford what, alliance geometry, balances; **not** ORBAT-first, not speech-act diplomacy first. | **Incentive story** displaces **receipt-tier** discipline on **observables** that would falsify the map. |
| **S3** | **Legitimacy, institutions & room** | Diplomatic / multilateral / civilizational **register**: credibility in the room, precedents, choreography (MFA, Kremlin, UN table, long arc). | **Diplomatic credibility** substitutes for **power-structure or kinetic** checks where **seams** are load-bearing. |
| **S4** | **Domestic political & legal machinery** | Votes, courts, war powers, escalation-trap as **binding** machinery; jurisdiction and enforceability. | **Domestic machinery** **colonizes** foreign operational claims (**pseudo–CENTCOM** from roll calls or headlines). |
| **S5** | **Markets, macro & system constraints** | Prices, cycles, inventories, sanctions pass-through, **commodity calendar** when **arithmetic / market** leads the spine. | **Price or cycle narrative** substitutes for **tiered** commodity, hull, or wire evidence without **hypothesis-grade** labeling. |

### Default primary → skeleton (`strategy-expert-*`)

| Primary (`thread:`) | Default | Notes |
|---------------------|---------|--------|
| `ritter` | **S1** | |
| `davis` | **S1** | Ultimatum / resumption / policy–military interface. |
| `marandi` | **S1** | Red-line / regional **hard edge**; often paired with **S2** in body. |
| `jermy` | **S1** | Naval / maritime. |
| `berletic` | **S1** | OSINT / open military-technical. |
| `baud` | **S1** | Operational / mil-intel mechanism claims. |
| `johnson` | **S1** | OOB / feasibility / operational skepticism. |
| `macgregor` | **S1** | Campaign-scale force mechanics — override to **S2** if weave is **grand strategic map** with little ORBAT. |
| `mearsheimer` | **S2** | Alliance geometry and structural incentives. |
| `mercouris` | **S3** | |
| `parsi` | **S3** | War-powers / accountability frames land in body vs **S4** when Congress machinery owns the title. |
| `freeman` | **S3** | |
| `crooke` | **S3** | |
| `diesen` | **S3** | Euro–Russian strategic narrative room. |
| `sachs` | **S3** | Multilateral / development table — override toward **S5** if macro/debt/sanctions **lead**. |
| `jiang` | **S3** | Civilizational / education-bridge speech layer. |
| `mate` | **S3** | Media / narrative contestation — override toward **S5** if **commodity / price** leads. |
| `blumenthal` | **S3** | Investigative / counter-narrative legitimacy — same override as Mate. |
| `barnes` | **S4** | |
| `pape` | **S4** | Escalation trap / domestic lock-in — body may glue **S5** when calendar is load-bearing. |
| `armstrong` | **S5** | Market / cycle machinery. |

**Overrides:** Use when inbox density or page title makes another spine honest (e.g. **Mate** + lead = **commodity arithmetic** → weight **S5** in body while keeping **S3** primary only if narrative room still owns the file title).

---

<a id="escalation-marker-preference"></a>

## Escalation marker preference

**SSOT** for optional inline cues inside **`days.md`** / notebook prose (WORK-only; not Record updates):

- **`[watch]`** — a reusable signal that may need follow-up or watch-support work later.
- **`[decision]`** — a live issue that may warrant a **decision point** when real options exist.
- **`[promote]`** — material that looks stable enough to **consider** promotion (see [promotion-ladder.md](../promotion-ladder.md)); does not itself change promotion stage.

Use **sparingly**. They cue later handling in this lane; they are **not** formal status fields and **not** substitutes for the promotion ladder’s required artifacts when you promote.

---

<a id="us-iran-kinetic-track"></a>

## US–Iran kinetic likelihood (cross-expert track)

**Purpose:** One **shared**, **falsifiable** **prediction object** across **`thread:`** experts when material touches **U.S.–Iran** **war** **risk**: *on **expert-stated** grounds, how **plausible** is a **near-term** **large-scale** **U.S.** **attack** **on** **Iran** **or** **core** **Iranian** **infrastructure** (not routine patrol rhetoric, not Lebanon-only detours unless the expert ties them to a **new** **Iran** **kinetic** **arc*)?*

**WORK-only;** not Record. Default **hypothesis-grade** until **wires**, **Pentagon-primary**, or **named** **order-of-battle** **receipts** land.

**Core roster (illustrative):** Experts who **often** **speak** **this** **thread** — e.g. `ritter`, `johnson`, `davis`, `marandi`, `parsi`, `mercouris`, `jermy`, `mearsheimer`, `baud`, `berletic`, `macgregor`, `sachs`, `diesen`. **Log a row** in [US-IRAN-KINETIC-TRACKER.md](US-IRAN-KINETIC-TRACKER.md) **only** when **that** **ingest** **states** **a** **directional** **view** (↑ higher near-term kinetic risk, ↓ lower, — flat/unclear, **N/A** abstain or no Iran-kinetic content).

**Peripheral / off-topic weeks:** Experts whose **only** **material** **is** **Europe**, **Rome**, **KY-4**, **PH** **lecture**, **etc.** → **omit** **row** **or** **explicit** **`N/A`** — **silence** **≠** **neutral** **forecast**.

**Optional inbox tail** on a **`thread:`** line: add **`us-iran-kinetic:↑|↓|—|N/A`** inside **`verify:`** (after other tags) when the operator wants grep without opening the tracker.

**Batch-analysis template:** canonical one-liner in [US-IRAN-KINETIC-TRACKER.md](US-IRAN-KINETIC-TRACKER.md) § *Batch-analysis template*.

**Relation to daily brief:** When **§1h** / **Islamabad** / **Hormuz** **loads** **the** **day**, **consider** **one** **Judgment** **or** **Open** **bullet** **that** **names** **whether** **expert** **lanes** **diverge** **on** **this** **object** **(Thesis** **A** **/** **B** **per** **Conflicting** **experts** **row** **above)**.

---

<a id="external-digest-stub"></a>
<a id="daily-brief-supplements"></a>

## Daily brief supplements — LLM or paste (parity with generator)

**Policy:** Treat pasted or LLM-assisted “daily strategic” blocks **the same** as other **`daily-brief-YYYY-MM-DD.md`** content from **`generate_work_politics_daily_brief.py`**: same file, same **§1f** weak-signal home when used as a dense digest, **same** obligation to **fill §1d–§1h** from watch docs and **not** collapse voice planes. Dense multi-theater narratives are still **useful coherence tests** (what would have to be true) and still carry **precision risk** (mixed channels, unsourced numbers) until **`strategy + verify`** or [`.cursor/skills/fact-check/SKILL.md`](../../../../.cursor/skills/fact-check/SKILL.md) — **no special “overlay” tier**. **`skill-strategy`** applies **Information logic**: **channels, not one story** ([`skill-strategy` SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md)). **Trim §1f** after verify so the brief does not carry **double truth**.

---

## Short paste block (meta / handoff)

Operator notebook prefs: variable daily length; minimum Signal / Judgment / Links; EOD-session prose popular-academic (no internal nicknames in spine). **`days.md` `##` dates:** compose / continuity anchors — not inbox clock / upload receipts; anti-split per architecture § `days.md` date keys. **`strategy-page` blocks:** target **500–1000 words** prose on **EOD compose** (`wc -w` above Technical appendix). Inbox + **`raw-input/`** = capture; notebook = synthesis + key links. **Expert corpus:** **`thread`** → `strategy_thread.py` → `experts/<id>/thread.md` only (not EOD compose). **Weave skeletons S1–S5:** optional primary-expert spine + failure modes — § *Weave skeletons (S1–S5)* (heading unchanged for grep). Compose choice weights sections (Signal/Judgment/Links/Open), not inbox order. Judgment leads structure. Islamabad / US–Iran: scope (pause, Lebanon, Hormuz). **US–Iran kinetic cross-expert track:** [US-IRAN-KINETIC-TRACKER.md](US-IRAN-KINETIC-TRACKER.md) + prefs § *US–Iran kinetic likelihood*. Leo XIV / Rome: moral–diplomatic plane vs mechanics; ROME-PASS source order. JD Vance: VP channel vs cable; §1e watch doc. Putin / Kremlin: §1d watch; Kremlin vs wire. PRC / Beijing: §1g watch; MFA vs Western analysis. IRI / Tehran: §1h watch; MFA/IRNA vs Western digest (framework = Islamabad index). **LLM or paste strategic digest:** same §1f + verify discipline as generator output — not §1d–§1h until watch-backed. PH when engaged that day. Offer B/M/M one-liners after substantive passes; lens depth in daily brief minds, notebook thin. **EOD strategy session** at day-end or explicit instruction (**breaking glass**); not on ingest alone. Promote to STRATEGY weekly on clear thesis. STATUS minimal. Framing risk over numeric confidence; analogue-app confidence scores / branch-vote metadata out of band until this file revises that. Split disagreements as Thesis A / Thesis B.

---

## Relation to assistants

- **Calibration / branch patterns from external analogue apps** (e.g. Metaculus-style scores, Kialo-style branch weights): gated by the **Analogue-app patterns** summary row — assistants **do not** introduce them into default captures or **EOD compose** until **Uncertainty** / that row is explicitly changed here.
- **Default on-disk capture** for strategy ingests remains **[daily-strategy-inbox.md](daily-strategy-inbox.md)** per [skill-strategy SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md).
- **Expert rolling corpus:** When the operator runs **`thread`** (or **`python3 scripts/strategy_thread.py`**), rebuild **`strategy-expert-<expert_id>.md`** from inbox **`thread:<expert_id>`** lines only — **not** **EOD compose** into `days.md` (architecture § *Thread (terminology)*).
- **Rome / Leo XIV:** When the month’s **`meta.md`** includes **Leo XIV / Rome helix** or ingests touch the Holy See, follow [ROME-PASS](../work-strategy-rome/ROME-PASS.md) source order for **Judgment** claims; optional **`ROME` / `LeoXIV`** tags in inbox cold lines per [daily-strategy-inbox.md](daily-strategy-inbox.md).
- **JD Vance:** When **`meta.md`** includes **JD Vance thread** or the day covers **Islamabad / VP travel / war powers**, align notebook **Links** with [daily-brief-jd-vance-watch.md](../daily-brief-jd-vance-watch.md) guardrails (URLs, 48h window); optional **`JDVance` / `VANCE`** tags in inbox cold lines.
- **Putin / Kremlin:** When **`meta.md`** includes **Putin thread** or the day covers **Ukraine**, **Russia** as negotiation actor, or **NATO**–Russia framing, align **Links** with [daily-brief-putin-watch.md](../daily-brief-putin-watch.md) (Kremlin + wire + native triangulation); optional **`PUTIN` / `KREMLIN`** tags in inbox cold lines.
- **PRC / Beijing:** When **`meta.md`** includes **PRC thread** or the day covers **U.S.–China**, **cross-strait**, **Indo-Pacific**, or **PRC**–adjacent **trade** / **sanctions**, align **Links** with [daily-brief-prc-watch.md](../daily-brief-prc-watch.md) (MFA + wire + Mandarin triangulation); optional **`PRC` / `CN` / `CHINA`** tags in inbox cold lines.
- **IRI / Tehran:** When **`meta.md`** includes **IRI thread** or the day covers **Islamabad**, **pause / Hormuz / Lebanon**, **nuclear** talks, or **Iranian** **state** messaging, align **Links** with [daily-brief-iran-watch.md](../daily-brief-iran-watch.md) (MFA + IRNA + Persian triangulation) alongside **Islamabad** framework artifacts when relevant; optional **`IRAN` / `IRI` / `TEHRAN`** tags in inbox cold lines.
- **Do not** extend `chapters/YYYY-MM/days.md` unless **EOD strategy session**, **`dream`**-thread explicit compose, **breaking glass**, or equivalent. Section weighting: architecture § *Compose choice and section weighting*.
- **`days.md` calendar headings:** Follow architecture § [`days.md` date keys](STRATEGY-NOTEBOOK-ARCHITECTURE.md#days-md-date-semantics) — **consolidate** EOD passes; **do not** mint new **`## YYYY-MM-DD`** from **`Accumulator for:`** / inbox batch labels alone; keep **[STATUS.md](STATUS.md)** links aligned with real anchors.
- **Batch-analysis snapshot (future emitter):** Derived **`batch_analysis_refs[]`** for a visual UI uses **`confidence`** + **`sources`** per architecture § *Batch-analysis — machine parse & visual snapshot*; inbox markdown remains SSOT.

---

## Changelog

| Date | Change |
|------|--------|
| 2026-04-18 | **EOD strategy session:** Deprecate operator **`weave`** token for notebook composition; default **once-per-day** **`days.md` + `strategy-page`** from inbox + **`raw-input/`**; **`weave` → EOD compose** across summary, architecture pointer, `skill-strategy`, `dream`, DEFAULT-PATH, rules. |
| 2026-04-18 | **Pages replace knots:** Summary table — **EOD page-shape menu**, **Page length**, inbox vs notebook, expert corpus, compose skeleton, short paste block; word band **500–1000** for **`strategy-page`**; architecture § *Page design and notebook-use jobs* (was knot-shape / knot design). |
| 2026-04-14 | **`days.md` date semantics (anti-split):** Summary table row **`days.md` heading dates**; **Relation to assistants** bullet + **Short paste block** line; pointers to [STRATEGY-NOTEBOOK-ARCHITECTURE.md § `days.md` date keys](STRATEGY-NOTEBOOK-ARCHITECTURE.md#days-md-date-semantics) and [.cursor/rules/strategy-notebook-days-date-semantics.mdc](../../../../.cursor/rules/strategy-notebook-days-date-semantics.mdc). |
| 2026-04-14 | **Knot design and notebook-use jobs:** Summary table **Weave knot-shape menu** row — each stub names implied **notebook-use** job(s); architecture § *Knot design and notebook-use jobs* + revised § *Notebook-use tags (weave-adjacent)*; `skill-strategy` weave obligation + pre-write checklist. |
| 2026-04-17 | **Weave skeletons (S1–S5):** Renumber from three conceptual skeletons to **five** (operations, power/structure, legitimacy/room, domestic machinery, markets/macro) with **one-line failure modes** per skeleton; default **primary expert → skeleton** table; summary table + short paste + anchor `weave-skeletons-s1-s5`; architecture § *Weave skeletons* pointer. |
| 2026-04-17 | **Batch-analysis / visual snapshot:** summary table row — derived JSON may expose **`batch_analysis_refs[]`** with **`confidence`** + **`sources`** for expert navigation; pointer to architecture § *Batch-analysis — machine parse & visual snapshot*. |
| 2026-04-16 | **Operator command `thread`:** expert rolling corpus rebuild (`strategy_thread.py` → `strategy-expert-*.md`); distinct from **`weave`** — architecture § *Thread (terminology)*; summary table + short paste + Relation to assistants. |
| 2026-04-15 | **Escalation marker preference:** SSOT for optional `[watch]` / `[decision]` / `[promote]` inline cues; cross-links from architecture SSOT and promotion ladder. |
| 2026-04-12 | Initial preferences from operator questionnaire (1D, 2A, 3A, 4A, 5A, 6D, 7C, 8C, 9A, 10B, 11A, 12C, 13C). |
| 2026-04-12 | **Leo XIV / Rome primary thread:** naming — **Leo XIV / Holy See** = voice; **ROME-PASS** / **work-strategy-rome** = hub. Implementation: architecture paragraph + `meta.md` helix + inbox grep tags + `skill-strategy` + [daily-brief-focus.md](../daily-brief-focus.md). |
| 2026-04-12 | **JD Vance primary thread:** **VP channel** = voice; [daily-brief-jd-vance-watch.md](../daily-brief-jd-vance-watch.md) = hub — mirrored in architecture, `meta.md`, inbox tags, `skill-strategy`, [daily-brief-focus.md](../daily-brief-focus.md). |
| 2026-04-12 | **Vladimir Putin / Kremlin primary thread:** [daily-brief-putin-watch.md](../daily-brief-putin-watch.md) = hub — same mirror pattern as JD Vance / Rome. |
| 2026-04-12 | **PRC / Beijing primary thread:** [daily-brief-prc-watch.md](../daily-brief-prc-watch.md) = hub (**§1g**); generator + `meta` + prefs + `skill-strategy`. |
| 2026-04-12 | **Islamic Republic of Iran primary thread:** [daily-brief-iran-watch.md](../daily-brief-iran-watch.md) = hub (**§1h**); complements Islamabad index; generator + `meta` + prefs + `skill-strategy`. |
| 2026-04-11 | **Weave → page structure:** [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave choice and section weighting*; inbox weave rhythm cross-link; prefs table + Relation to assistants + short paste block (explicit intra-day **weave**). |
| 2026-04-14 | **Operator command `weave`:** Canonical name for inbox → `days.md` merge; legacy `fold` retired; **`weave`** is the canonical command ([STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave (terminology)*; [skill-strategy SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md) **Weave** mode). |
| 2026-04-15 | **External model briefs (LLM digests):** Summary table row + § stub — **§1f** overlay + **`strategy + verify`** falsifiable-table gate before weave; mirrored in [`skill-strategy` SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md) (description + pre-write checklist + Session hygiene). |
| 2026-04-17 | **Daily brief LLM parity:** Retired separate “Grok overlay” / “external model overlay” wording — LLM or paste supplements = same `daily-brief-YYYY-MM-DD.md` artifact as generator output; prefs § *Daily brief supplements*, `skill-strategy`, sample April briefs §1f, `grok-daily-brief.md`, `DEFAULT-PATH.md`. |
| 2026-04-17 | **Knot length on weave:** **`strategy-notebook-knot-*.md`** target **300–1000 words**; knot-shape menu stubs scoped to that band; architecture § *Weave command* + *Weave choice*; template + skill-strategy checklist. |
| 2026-04-17 | **US–Iran kinetic (cross-expert track):** summary table row + § *US–Iran kinetic likelihood* + [US-IRAN-KINETIC-TRACKER.md](US-IRAN-KINETIC-TRACKER.md) stub; short paste block pointer; `chapters/YYYY-MM/meta.md` cross-link when the month touches U.S.–Iran escalation. |
