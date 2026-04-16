# Strategy notebook — operator preferences

**Status:** ACTIVE  
**Set:** 2026-04 (from multiple-choice questionnaire)  
**Governed by:** [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) — this file **narrows** daily practice; it does not replace architecture for repo-wide defaults (e.g. architecture still describes a **~1000w** consolidated **`days.md`** daily target where no override applies, and a **300–1000w** target per **`strategy-notebook-knot-*.md`** file on weave).  
**Skill contract:** Together with the architecture doc and [daily-strategy-inbox.md](daily-strategy-inbox.md), this file is **part of** [`skill-strategy`](../../../../.cursor/skills/skill-strategy/SKILL.md) — operator defaults the skill **must** apply on a **`strategy`** pass; not optional flavor beside the skill.

---

## Summary

| Area | Preference |
|------|------------|
| **Daily length** | **Variable by day** — no fixed default word budget. |
| **Minimum `days.md` sections** | **`### Signal` · `### Judgment` · `### Links`** only. |
| **Weave-time prose register** | **Popular-academic** by default — reader-facing **Signal / Judgment** in `days.md` after **weave**; avoid **internal repo nicknames**, **operator-only path tokens**, and **backend shorthand** in the **notebook spine** (spell out ideas or use public equivalents). Operator docs and inbox may keep technical labels. Aligns with [skill-strategy Session hygiene](../../../../.cursor/skills/skill-strategy/SKILL.md) § *Session hygiene*. |
| **Inbox vs notebook** | **Raw paste and URL dumps** → [daily-strategy-inbox.md](daily-strategy-inbox.md). **Notebook** (knots) = **synthesis + key links**, not mirrors of the inbox. |
| **Expert corpus (`thread`)** | Inbox lines with **`thread:<expert_id>`** → operator **`thread`** rebuilds **`strategy-expert-<expert_id>.md`** only — **`python3 scripts/strategy_thread.py`** — **not** a **`weave`** (no `days.md` / knots). Architecture § *Thread (terminology)*. |
| **Weave → page structure** | **Promotion choice** — what lands under **Signal** vs **Judgment** vs **Links** vs **Open** follows **what you choose to weave** and at **which** weave, not inbox length or equal padding per section. Intra-day weaves **iterate one** `## YYYY-MM-DD` block (merge, don’t duplicate). See [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave choice and section weighting*. |
| **Weave knot-shape menu** | On **`weave`**, assistants present **4–6** labeled options (**knot thesis / shape / content emphasis**) **before** writing to disk—see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Weave command — knot-shape menu*. Each option should be **scoped** so a resulting **knot file** (when in scope) can be written within **300–1000 words** (e.g. “thin knot + `days.md` carry,” “full in-knot synthesis,” “Links-heavy / Judgment-tight”). Operator picks a letter, says **`no menu`**, or names the shape explicitly. |
| **Weave skeleton (primary expert)** | **S1–S5** — when **`weave`** names one **primary** `strategy-expert` (or MC pick), default **Signal / Judgment / Links / Open weighting** follows § *Weave skeletons (S1–S5)*; multi-expert analysis stays in the **knot body**; primary = **filing / spine**, not sole epistemic authority. |
| **Knot length (weave output)** | **`strategy-notebook-knot-*.md`:** target **300–1000 words** (`wc -w`). Router / deferral knots may sit **below 300** only when prose is **explicitly** routed to **`days.md`** per architecture. |
| **Batch-analysis / visual snapshot** | Inbox **`batch-analysis | …`** lines stay **markdown SSOT**; a future **derived** JSON snapshot for a **visual UI** should emit **`batch_analysis_refs[]`** with **`expert_ids`**, per-row **`confidence`** (`high` \| `medium` \| `low` \| `none`), and **`sources`** (`crosses` / `thread_in_line` / `upstream_verify` / `label_alias`) — **architecture** § *Batch-analysis — machine parse & visual snapshot*. Thematic batches with **no** indexed **`thread:`** may legitimately show **empty** `expert_ids`. |
| **Judgment priority** | **Structural first** — power, incentives, constraints; narrative second. |
| **Islamabad / US–Iran / pause** | When the day touches this thread, **always capture scope fights**: what is in/out of the **pause**, **Lebanon**, **Hormuz** definition. |
| **Leo XIV / Holy See / Rome (primary thread)** | **Voice** = papal / Holy See moral–diplomatic lines (**Leo XIV**, `@Pontifex`, audiences). **Hub** = [work-strategy-rome](../work-strategy-rome/README.md) + [ROME-PASS](../work-strategy-rome/ROME-PASS.md). When the day touches this thread, **keep planes separate** from Beltway mechanics: **IHL / legitimacy vocabulary** is not a forecast of **kinetic** facts; weave **Judgment** with **dated** vatican.va or press-office URLs when claiming official text (see ROME-PASS source order). If **Lebanon** (or other crises) appears in **both** expert-commentary and papal lines, prefer **two bullets** or **Thesis A / B** — do not merge registers without verify. |
| **JD Vance / VP channel (primary thread)** | **Voice** = **Vice President** public lines, travel, and **White House** readouts (not Senate archive unless window-relevant). **Hub** = [daily-brief-jd-vance-watch.md](../daily-brief-jd-vance-watch.md) (**§1e** in daily briefs — coffee **C** pass). When the day touches **U.S.–Iran**, **Islamabad**, **war powers**, or **coalition** framing, **tag whether Vance is acting as channel** (delegation lead, “final offer” voice, restraint narrative) vs **atmospheric** quote — separate **official** URL from **cable analysis**. If **Vance** and **Pentagon / State** lines **diverge** on scope (**Lebanon**, **Hormuz**, pause), **two bullets** or **Thesis A / B**; do not collapse into one “White House says.” |
| **Vladimir Putin / Kremlin (primary thread)** | **Voice** = **Russian President** public lines, **Kremlin** schedule (events, calls, transcripts). **Hub** = [daily-brief-putin-watch.md](../daily-brief-putin-watch.md) (**§1d** — coffee **C** pass, rolling **48h**). When the day touches **Ukraine**, **Iran** (Russia as actor), **NATO**, or **multilateral** ceasefire framing, separate **Kremlin-primary** quotes from **Western wire paraphrase**; add **Russian-language or Kremlin-primary** triangulation per [daily-brief-native-international-pass.md](../daily-brief-native-international-pass.md) when Russia is load-bearing. If **Putin** lines and **U.S. / allied** readouts **diverge** on **facts or scope**, **two bullets** or **Thesis A / B** — do not merge **personality** headlines with **operational** claims without URLs. |
| **PRC / Beijing (primary thread)** | **Voice** = **People’s Republic of China** **party–state** lines (**MFA**, **summits**, major **state** readouts). **Hub** = [daily-brief-prc-watch.md](../daily-brief-prc-watch.md) (**§1g** — coffee **C** pass, rolling **48h**). When the day touches **U.S.–China**, **cross-strait**, **Indo-Pacific**, **trade / sanctions**, or **PRC** as **named** party beside **Russia** / **Iran** / **U.S.** stories, separate **MFA / state-primary** wording from **Western** “China” **analysis**; add **Mandarin-primary** triangulation per [daily-brief-native-international-pass.md](../daily-brief-native-international-pass.md) when the PRC thread is load-bearing. If **Beijing** and **Washington** lines **diverge** on **terms or scope**, **two bullets** or **Thesis A / B**. |
| **Islamic Republic of Iran (primary thread)** | **Voice** = **Iranian state** lines (**MFA**, **presidency**, **IRNA** / major **state-adjacent** wires). **Hub** = [daily-brief-iran-watch.md](../daily-brief-iran-watch.md) (**§1h** — coffee **C** pass, rolling **48h**). **Not** a substitute for the **Islamabad** bargaining **framework** ([islamabad-operator-index.md](../islamabad-operator-index.md), gap matrices)—use **both**: framework for **trade space**, IRI watch for **what Tehran says** on **pause**, **Hormuz**, **Lebanon**, **nuclear** terms. Separate **Persian-primary** or **MFA** quotes from **Western** “Iran” **digest**; add **Persian** triangulation per [daily-brief-native-international-pass.md](../daily-brief-native-international-pass.md) when the Iran thread is load-bearing. If **Tehran** and **Washington** lines **diverge** on **facts or scope**, **two bullets** or **Thesis A / B**. |
| **Predictive History (work-jiang)** | **Episodic** — cite when you **actually** engaged lecture/corpus that day; no standing PH obligation in the notebook. |
| **Lenses (B / M / Merc)** | After **substantive** notebook-relevant work, assistant **offers three one-liners** — operator **picks or skips** (see [strategy-minds-granular.mdc](../../../../.cursor/rules/strategy-minds-granular.mdc)). |
| **Where lens depth lives** | **Daily brief mind shells** and **`minds/outputs/`** as needed; **strategy-notebook day block stays thin**. |
| **Inbox → `days.md`** | **Weave** at **`dream`** (day-end), on **`weave`** / **explicit** operator direction (intra-day), or equivalent — assistants do **not** append `days.md` on ingest alone (see [daily-strategy-inbox.md](daily-strategy-inbox.md)). |
| **Promotion to `STRATEGY.md`** | **Weekly** when the **week** had a **clear thesis** (not only rare milestones). |
| **STATUS.md** | **Minimal** — last entry / pointer; no rich dashboard unless asked. |
| **Uncertainty** | Emphasize **narrative and framing risk** over formal numeric confidence tags. |
| **Analogue-app patterns (Metaculus / Kialo / etc.)** | **Do not** add **numeric or ordinal confidence** tags, **forecast scoreboards**, or **argument-tree “impact” / branch-vote** metadata to default notebook or `skill-strategy` output — they **conflict** with the **Uncertainty** row unless this file is **revised** to allow them. Prefer **Thesis A / B** and falsifiers in `meta.md` / expert index. |
| **Conflicting experts** | **Two Judgment bullets** — **Thesis A** / **Thesis B** — preserve tension; no forced merge. |
| **External model briefs (LLM digests)** | **Grok-class** or other **closed-world** strategic narratives pasted for triage: **never** substitute for **§1d–§1h** watch passes or **tier-A** URLs. **Default:** one labeled **weak-signal / overlay** block in **`daily-brief-YYYY-MM-DD.md` §1f** (see [weak-signal-template.md](../weak-signal-template.md)) — **hypothesis + falsifiers**; line-by-line **fact-check** triage before any **weave** into **`days.md` Judgment**. **Do not** import **unsourced** counts, meeting quotes, or same-day **macro tables** from the digest into **Signal/Judgment** as facts. |

---

<a id="weave-skeletons-s1-s5"></a>

## Weave skeletons (S1–S5)

**Purpose:** Renames and extends the earlier **three-skeleton** idea (mechanics / legitimacy / domestic) into **five** default **spines** for a knot or day block when **`weave`** picks a **primary** `strategy-expert`. The skeleton sets **section weighting** and **Open** pressure; **all other experts** appear as **synthesis, seams, and falsifiers** in the knot **body** (and in `days.md` when woven there). **Primary** = navigation and default structure, not a claim that one voice owns the truth.

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
| `scott-ritter` | **S1** | |
| `daniel-davis` | **S1** | Ultimatum / resumption / policy–military interface. |
| `seyed-marandi` | **S1** | Red-line / regional **hard edge**; often paired with **S2** in body. |
| `steve-jermy` | **S1** | Naval / maritime. |
| `brian-berletic` | **S1** | OSINT / open military-technical. |
| `jacques-baud` | **S1** | Operational / mil-intel mechanism claims. |
| `larry-johnson` | **S1** | OOB / feasibility / operational skepticism. |
| `douglas-macgregor` | **S1** | Campaign-scale force mechanics — override to **S2** if weave is **grand strategic map** with little ORBAT. |
| `john-mearsheimer` | **S2** | Alliance geometry and structural incentives. |
| `alexander-mercouris` | **S3** | |
| `trita-parsi` | **S3** | War-powers / accountability frames land in body vs **S4** when Congress machinery owns the title. |
| `charles-freeman` | **S3** | |
| `alastair-crooke` | **S3** | |
| `glenn-diesen` | **S3** | Euro–Russian strategic narrative room. |
| `jeffrey-sachs` | **S3** | Multilateral / development table — override toward **S5** if macro/debt/sanctions **lead**. |
| `jiang-xueqin` | **S3** | Civilizational / education-bridge speech layer. |
| `aaron-mate` | **S3** | Media / narrative contestation — override toward **S5** if **commodity / price** leads. |
| `max-blumenthal` | **S3** | Investigative / counter-narrative legitimacy — same override as Mate. |
| `robert-barnes` | **S4** | |
| `robert-pape` | **S4** | Escalation trap / domestic lock-in — body may glue **S5** when calendar is load-bearing. |
| `martin-armstrong` | **S5** | Market / cycle machinery. |

**Overrides:** Use when inbox density or knot title makes another spine honest (e.g. **Mate** + lead = **commodity arithmetic** → weight **S5** in body while keeping **S3** primary only if narrative room still owns the file title).

---

<a id="escalation-marker-preference"></a>

## Escalation marker preference

**SSOT** for optional inline cues inside **`days.md`** / notebook prose (WORK-only; not Record updates):

- **`[watch]`** — a reusable signal that may need follow-up or watch-support work later.
- **`[decision]`** — a live issue that may warrant a **decision point** when real options exist.
- **`[promote]`** — material that looks stable enough to **consider** promotion (see [promotion-ladder.md](../promotion-ladder.md)); does not itself change promotion stage.

Use **sparingly**. They cue later handling in this lane; they are **not** formal status fields and **not** substitutes for the promotion ladder’s required artifacts when you promote.

---

<a id="external-digest-stub"></a>

## External model briefs (LLM digests — operator stub)

**Grok-class** (and similar) outputs are useful as **adversarial coherence tests**: they surface **what would have to be true** for one arc to close. They are **dangerous** as **implicit evidence** because they **mix channels** (G7, Hungary, Ukraine, CPI, Taiwan, Russia) and **fake precision** (telemetry, “verified” OSINT) without **plane tags** or **primaries**. **`skill-strategy`** treats them per the **Information logic** rule: **channels, not one story** ([`skill-strategy` SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md)). **Operational default:** land the paste under **`daily-brief` §1f** with an explicit **NOT verified** header and a **short triage** (what checked vs what failed); pull **confirmable** lines into **§1d–§1h** or **`### Web verification`** only after **`strategy + verify`** or [`.cursor/skills/fact-check/SKILL.md`](../../../../.cursor/skills/fact-check/SKILL.md). **Trim §1f** after verify so the notebook does not carry **double truth**.

---

## Short paste block (meta / handoff)

Operator notebook prefs: variable daily length; minimum Signal / Judgment / Links; weave-time prose popular-academic (no internal nicknames in spine). **Knot files (`strategy-notebook-knot-*.md`):** target **300–1000 words** on weave (`wc -w`). Inbox = raw; notebook = synthesis + key links. **Expert corpus:** **`thread`** → `strategy_thread.py` → `strategy-expert-*.md` only (not weave). **Weave skeletons S1–S5:** optional primary-expert spine + failure modes — § *Weave skeletons (S1–S5)*. Weave choice weights sections (Signal/Judgment/Links/Open), not inbox order. Judgment leads structure. Islamabad / US–Iran: scope (pause, Lebanon, Hormuz). Leo XIV / Rome: moral–diplomatic plane vs mechanics; ROME-PASS source order. JD Vance: VP channel vs cable; §1e watch doc. Putin / Kremlin: §1d watch; Kremlin vs wire. PRC / Beijing: §1g watch; MFA vs Western analysis. IRI / Tehran: §1h watch; MFA/IRNA vs Western digest (framework = Islamabad index). **External LLM strategic digests:** §1f labeled overlay + fact-check triage before weave — not §1d–§1h. PH when engaged that day. Offer B/M/M one-liners after substantive passes; lens depth in daily brief minds, notebook thin. Weave inbox at dream or explicit **weave**; not on ingest alone. Promote to STRATEGY weekly on clear thesis. STATUS minimal. Framing risk over numeric confidence; analogue-app confidence scores / branch-vote metadata out of band until this file revises that. Split disagreements as Thesis A / Thesis B.

---

## Relation to assistants

- **Calibration / branch patterns from external analogue apps** (e.g. Metaculus-style scores, Kialo-style branch weights): gated by the **Analogue-app patterns** summary row — assistants **do not** introduce them into default captures or weaves until **Uncertainty** / that row is explicitly changed here.
- **Default on-disk capture** for strategy ingests remains **[daily-strategy-inbox.md](daily-strategy-inbox.md)** per [skill-strategy SKILL.md](../../../../.cursor/skills/skill-strategy/SKILL.md).
- **Expert rolling corpus:** When the operator runs **`thread`** (or **`python3 scripts/strategy_thread.py`**), rebuild **`strategy-expert-<expert_id>.md`** from inbox **`thread:<expert_id>`** lines only — **not** a **`weave`** into `days.md` (architecture § *Thread (terminology)*).
- **Rome / Leo XIV:** When the month’s **`meta.md`** includes **Leo XIV / Rome helix** or ingests touch the Holy See, follow [ROME-PASS](../work-strategy-rome/ROME-PASS.md) source order for **Judgment** claims; optional **`ROME` / `LeoXIV`** tags in inbox cold lines per [daily-strategy-inbox.md](daily-strategy-inbox.md).
- **JD Vance:** When **`meta.md`** includes **JD Vance thread** or the day covers **Islamabad / VP travel / war powers**, align notebook **Links** with [daily-brief-jd-vance-watch.md](../daily-brief-jd-vance-watch.md) guardrails (URLs, 48h window); optional **`JDVance` / `VANCE`** tags in inbox cold lines.
- **Putin / Kremlin:** When **`meta.md`** includes **Putin thread** or the day covers **Ukraine**, **Russia** as negotiation actor, or **NATO**–Russia framing, align **Links** with [daily-brief-putin-watch.md](../daily-brief-putin-watch.md) (Kremlin + wire + native triangulation); optional **`PUTIN` / `KREMLIN`** tags in inbox cold lines.
- **PRC / Beijing:** When **`meta.md`** includes **PRC thread** or the day covers **U.S.–China**, **cross-strait**, **Indo-Pacific**, or **PRC**–adjacent **trade** / **sanctions**, align **Links** with [daily-brief-prc-watch.md](../daily-brief-prc-watch.md) (MFA + wire + Mandarin triangulation); optional **`PRC` / `CN` / `CHINA`** tags in inbox cold lines.
- **IRI / Tehran:** When **`meta.md`** includes **IRI thread** or the day covers **Islamabad**, **pause / Hormuz / Lebanon**, **nuclear** talks, or **Iranian** **state** messaging, align **Links** with [daily-brief-iran-watch.md](../daily-brief-iran-watch.md) (MFA + IRNA + Persian triangulation) alongside **Islamabad** framework artifacts when relevant; optional **`IRAN` / `IRI` / `TEHRAN`** tags in inbox cold lines.
- **Do not** extend `chapters/YYYY-MM/days.md` unless **`dream`** weave, **`weave`** / **explicit** operator instruction, or equivalent — unchanged. Section weighting per weave: architecture § *Weave choice and section weighting*.
- **Batch-analysis snapshot (future emitter):** Derived **`batch_analysis_refs[]`** for a visual UI uses **`confidence`** + **`sources`** per architecture § *Batch-analysis — machine parse & visual snapshot*; inbox markdown remains SSOT.

---

## Changelog

| Date | Change |
|------|--------|
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
| 2026-04-17 | **Knot length on weave:** **`strategy-notebook-knot-*.md`** target **300–1000 words**; knot-shape menu stubs scoped to that band; architecture § *Weave command* + *Weave choice*; template + skill-strategy checklist. |
