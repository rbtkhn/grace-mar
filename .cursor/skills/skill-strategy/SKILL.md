---
name: skill-strategy
preferred_activation: strategy
description: >-
  Primary trigger: strategy. Work-strategy pass — cross-territory judgment with strategy-notebook as the primary write surface;
  STRATEGY.md only when promoting stable arcs. Modes: default notebook pass; strategy + verify (web or fact-check tier, dated citations in Links);
  optional promote to STRATEGY.md. Islamabad / Rome frameworks, JD Vance VP channel (brief §1e), Putin / Kremlin (brief §1d), PRC / Beijing (brief §1g), gap matrices, weak-signal and analogy-audit discipline. PH (work-jiang) via Jiang resonance —
  not work-politics pulse or weekly brief generator.
---

# Strategy pass (`skill-strategy`)

**Preferred activation (operator):** **`strategy`**. **Aliases:** **`strategy pass`**, **`work-strategy`**.

**Purpose:** Run a **bounded strategy pass** over work-strategy: produce or extend the **strategy-notebook** first; touch [STRATEGY.md](../../../docs/skill-work/work-strategy/STRATEGY.md) only when promoting watches, analogy lines, or operator log entries that have **stabilized**.

**Operator preferences (structure, Judgment rules, fold rhythm, promotion):** [NOTEBOOK-PREFERENCES.md](../../../docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md) — **narrows** defaults in [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md).

**Persistent frontier:** The repo holds the **running edge** (latest `days.md` block, **`### Open`**, **`### Links`**, **`meta.md`** when relevant). Each **`strategy`** invocation **updates** that checkpoint from the **last committed** block—tomorrow’s pass **reads disk**, not thread recall. Informal gloss: **memoized** strategy state (see [Accumulation and evolution](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#accumulation-and-evolution) in the architecture doc).

## When to use

- The operator wants **cross-territory** synthesis (briefs, transcripts, frameworks, Rome/Islamabad/Putin/Vance/PRC threads) captured as **dated judgment**.
- Closing or continuing a **daily** or **monthly** arc in the notebook without duplicating the full pulse or weekly-brief workflows.

**Relation to `dream`:** Daytime **`strategy`** passes **produce** notebook judgment. **`dream`** (end of day) **initiates production closeout** for that calendar day’s page — stub, condense, defer, or gap note per [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md); see [.cursor/skills/dream/SKILL.md](../dream/SKILL.md) § *Strategy notebook*. Dream does not replace analysis; it **accounts** for the daily artifact before sleep.

**Seal with `self-skill-write`:** When a daily block becomes the **finished page** for that date, **`strategy`** (structure) and **`self-skill-write`** (linguistic layer — [skills-modularity](../../../docs/skills-modularity.md)) **converge** on the same markdown. That seal may occur in a daytime pass or in **`dream`**; the skills still meet at the moment the entry is **committed** as the day’s artifact.

## Transcript demo / calibration (optional)

Runnable **multi-phase** calibration (preflight, notebook, verify, tri-frame, boundaries): [`docs/skill-work/work-strategy/strategy-notebook/DEMO-SKILL-STRATEGY-TRANSCRIPTS.md`](../../../docs/skill-work/work-strategy/strategy-notebook/DEMO-SKILL-STRATEGY-TRANSCRIPTS.md). **Preflight:** `bash scripts/demo_skill_strategy_transcripts_check.sh` from repo root. **Audit rubric (optional):** `docs/skill-work/work-strategy/strategy-notebook/demo-runs/skill-strategy-results-YYYY-MM-DD.md`. **Executive summary:** [`DEMO-SKILL-STRATEGY-EXECUTIVE-REPORT.md`](../../../docs/skill-work/work-strategy/strategy-notebook/DEMO-SKILL-STRATEGY-EXECUTIVE-REPORT.md). WORK only — not Record.

## Modes (operator / agent)

| Mode | Trigger | Agent behavior |
|------|---------|----------------|
| **Default** | `strategy`, `strategy pass`, `work-strategy` | Read notebook frontier (tail of `days.md`) + inbox. **Default on-disk capture** = [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) (paste-ready lines). **Do not** append or merge into `days.md` until **`dream`** folds inbox or the operator **explicitly** directs a notebook update. |
| **+ verify** | Same + **search the web**, **verify claims**, **fact-check**, **wires** | Run a **short web pass** or [fact-check](../fact-check/SKILL.md) on load-bearing numbers/names; write under **`### Web verification (YYYY-MM-DD)`** (or equivalent) with **dated** claims and **URLs** in **Links**. Do not treat chat or operator paste as verified. |
| **Promote** | Operator asks to **promote** / **stitch to STRATEGY** / stable arc | Then suggest or edit [STRATEGY.md](../../../docs/skill-work/work-strategy/STRATEGY.md) watches, §IV log, analogy list — **not** every daily entry. |

**Oil, prices, ship counts, casualties** — time-stamp sensitive; prefer **dated market/maritime read** or omit the number.

## Default moves (agent)

1. Read [strategy-notebook/STATUS.md](../../../docs/skill-work/work-strategy/strategy-notebook/STATUS.md), [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) (if using the day’s accumulator), and the tail of the active month `chapters/YYYY-MM/days.md` (and `meta.md` if the month’s theme or open questions matter). **Rome / Leo XIV watch:** When `meta.md` names **Leo XIV / Rome helix** or the day’s captures include **Holy See** / `@Pontifex` / Vatican lines, skim [ROME-PASS.md](../../../docs/skill-work/work-strategy/work-strategy-rome/ROME-PASS.md) (source order + boundaries) and the **latest relevant** dated note under [work-strategy-rome/notes/](../../../docs/skill-work/work-strategy/work-strategy-rome/notes/) before folding **Judgment** — do not treat social syndication as primary for official claims. **JD Vance / VP watch:** When `meta.md` names **JD Vance thread** or the day touches **Islamabad**, **pause / Hormuz / Lebanon** U.S. role, or **war powers**, skim [daily-brief-jd-vance-watch.md](../../../docs/skill-work/work-strategy/daily-brief-jd-vance-watch.md) (48h window, URL guardrails) and align **Judgment** with **official** readouts where load-bearing — optional **`JDVance` / `VANCE`** grep tags in inbox cold lines. **Putin / Kremlin watch:** When `meta.md` names **Putin thread** or the day touches **Ukraine**, **Russia** as actor in **Iran** / **NATO** / **ceasefire** stories, skim [daily-brief-putin-watch.md](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md) (Kremlin + native triangulation guardrails) before folding **Judgment** — optional **`PUTIN` / `KREMLIN`** grep tags in inbox cold lines. **PRC / Beijing watch:** When `meta.md` names **PRC thread** or the day touches **U.S.–China**, **cross-strait**, **Indo-Pacific**, or **PRC**-adjacent **trade** / **sanctions**, skim [daily-brief-prc-watch.md](../../../docs/skill-work/work-strategy/daily-brief-prc-watch.md) (MFA + Mandarin triangulation guardrails) before folding **Judgment** — optional **`PRC` / `CN` / `CHINA`** grep tags in inbox cold lines. **Chat `strategy ingest` output** defaults to **new paste-ready lines** appended **below the append line** in `daily-strategy-inbox.md` (canonical shape: inbox § *Paste-ready one-liner* — SSOT; optional **`ROME` / `LeoXIV`** / **`JDVance` / `VANCE`** / **`PUTIN` / `KREMLIN`** / **`PRC` / `CN` / `CHINA`** grep tags in cold lines). **Optional:** **two-tier gist** (`cold: … // hook: …`) when the capture is **Judgment-sensitive** or **multi-chain** — see [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) § *Optional two-tier gist (cold claim // operator hook)*. Use `session-transcript.md` / `log_operator_choice.py` only when the operator asks for a **session receipt** ([work-menu-conventions § Auditing picks](../../../docs/skill-work/work-menu-conventions.md#6-auditing-picks-choice-journal)).
2. Pick **session type** (A–D) and use the **section router** in [SYNTHESIS-OPERATING-MODEL.md](../../../docs/skill-work/work-strategy/strategy-notebook/SYNTHESIS-OPERATING-MODEL.md) when the operator wants a systematic synthesis path; then follow [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) for **Daily synthesis**, **Daily length and prose** (architecture **~1000 words** band where applicable; **variable length** per [NOTEBOOK-PREFERENCES.md](../../../docs/skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md)), **Condense-to-target**: **Fast** path = tiers **A → D** only; **Full** path = **Summarize-and-condense** (tag → route ARTIFACT → **K** + K-tests → skeleton → DUPLICATE → tiers → stop rule) when the draft mixes notebook + lens/DEMO/web bulk; use the **Condense checklist** there, and **Accumulation and evolution** — **minimum** notebook sections per NOTEBOOK-PREFERENCES (**Signal / Judgment / Links**); optional **Open** / **Bets** / **Jiang** / **History** only when the operator or architecture calls for them. Prefer **academic prose** in the notebook block.
3. **Notebook write surface:** **Assistants** default to appending [daily-strategy-inbox.md](../../../docs/skill-work/work-strategy/strategy-notebook/daily-strategy-inbox.md) for **`strategy ingest`** and rough capture; **fold** into `chapters/YYYY-MM/days.md` at **`dream`** or when the operator **explicitly** asks to extend the **`## YYYY-MM-DD`** block. When the operator **does** direct a same-session page update, **append or extend** the daily page per architecture; **Links** to inputs (brief file, transcript digest, framework doc). The rolling inbox **does not** auto-reset each dream — **prune** when scratch exceeds **~20k** chars, in **~5k** blocks from the top (see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) § *Daily strategy inbox*). **`batch-analysis`:** default to **proposing** the joint line **in chat** (tension-first; standalone line, no `paired-with`); **append** to the inbox when the operator asks (**EXECUTE** / explicit paste) — same architecture § *Batch-analysis* and inbox § *Multi-item ingest*. **Chat echo:** In the **same assistant reply**, repeat what was appended—**paste-ready one-liners**, **batch-analysis** lines, and **new notebook bullets / paragraphs** in full (or the minimum excerpt that remains copy-paste useful if the write is very long). Default: **no file-only drops** for ingest lines and day-block edits; the operator should not need to open the file to get the text.
4. **STRATEGY.md:** suggest or apply updates only when the operator asks to **promote** — not every notebook entry.

5. **Companion artifacts (link in `### Links` when touched):** [islamabad-operator-index.md](../../../docs/skill-work/work-strategy/islamabad-operator-index.md), [us-iran-bargaining-gaps-matrix.md](../../../docs/skill-work/work-strategy/us-iran-bargaining-gaps-matrix.md), [us-iran-top-three-flashpoints-formal.md](../../../docs/skill-work/work-strategy/us-iran-top-three-flashpoints-formal.md) (dated formal flashpoint summary), [us-iran-divergence-and-proposed-compromises.md](../../../docs/skill-work/work-strategy/us-iran-divergence-and-proposed-compromises.md) (divergence + illustrative compromises), framework files (`islamabad-framework*.md`). **Rome / Leo XIV:** [work-strategy-rome/README.md](../../../docs/skill-work/work-strategy/work-strategy-rome/README.md), [ROME-PASS.md](../../../docs/skill-work/work-strategy/work-strategy-rome/ROME-PASS.md), and the month’s **Leo XIV / Rome helix** subsection in [chapters/YYYY-MM/meta.md](../../../docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/meta.md) when Vatican lines matter. **JD Vance / VP:** [daily-brief-jd-vance-watch.md](../../../docs/skill-work/work-strategy/daily-brief-jd-vance-watch.md) and the month’s **JD Vance thread** subsection in the same `meta.md` when Islamabad / executive channel lines matter. **Putin / Kremlin:** [daily-brief-putin-watch.md](../../../docs/skill-work/work-strategy/daily-brief-putin-watch.md) and the month’s **Vladimir Putin / Kremlin thread** subsection in the same `meta.md` when Ukraine / Russia / NATO lines matter — so analysis does not sit orphan to the notebook. **PRC / Beijing:** [daily-brief-prc-watch.md](../../../docs/skill-work/work-strategy/daily-brief-prc-watch.md) and the month’s **PRC / Beijing thread** subsection in the same `meta.md` when U.S.–China / Indo-Pacific / MFA lines matter.

6. **Flashpoint / gap-rank passes** — optional subsection in the day block (see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#skill-strategy-modes-and-verification-passes)): **claim → wire check → correction (if any) → operative move**; point at the **gap matrix** row when the pass ranks **Iran / U.S.** tensions.

**Lane index:** [work-strategy README](../../../docs/skill-work/work-strategy/README.md).

## Three minds (optional — granular)

Do **not** default to tri-frame on every pass — [strategy-minds-granular.mdc](../../../.cursor/rules/strategy-minds-granular.mdc). **Load mind files from:** [strategy-notebook/minds/](../../../docs/skill-work/work-strategy/strategy-notebook/minds/) (**Grace-Mar canonical** `CIV-MIND-*.md` — full profiles in-repo; **no civ-mem required**). Entry stubs: [minds/README.md](../../../docs/skill-work/work-strategy/minds/README.md). **Advisory patterns** (single/two-lens, links-only lensing, verify ownership, recipes): [MINDS-SKILL-STRATEGY-PATTERNS.md](../../../docs/skill-work/work-strategy/minds/MINDS-SKILL-STRATEGY-PATTERNS.md). Full **LEARN MODE** + tri-frame ordering: [LEARN_MODE_RULES.md](../../../docs/skill-work/work-strategy/LEARN_MODE_RULES.md). **Structured tri-mind pass** (A/B/C menu: solo, two-letter duet, or **`abc`** roundtable): [tri-mind SKILL.md](../tri-mind/SKILL.md) — invoke with **`tri-mind`** / **`tri-frame`** / **`tutti`**, not as the default wrapper on every `strategy` pass.

**Ensemble shorthand (solo / duet / tutti):** **Tacet** = no lens (plain Judgment). **Solo** = one mind. **Duet** = two-part tension pass. **Tutti** = explicit tri-frame / LEARN day. Gloss (score, parts, conductor, dissonance): [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Ensemble metaphor](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#ensemble-metaphor-chamber-group-gloss). **Post-entry menu** order **B → M → M** is **program order** for the optional three one-liners in chat — **not** the same ordering as **LEARN MODE** tri-frame (follow `LEARN_MODE_RULES.md` when that mode applies).

### Post-entry lens offer

After any **substantive** notebook entry (Signal / Judgment / Links written or extended — whether from coffee A daily brief, a standalone `strategy` pass, or a transcript digest; **History resonance** optional when mechanism ids apply), include a **three-option lens block** in the WORK menu:

```
Lens pass (optional — pick one, combine, or skip):
- Barnes: <one line in Barnes linguistic fingerprint>
- Mearsheimer: <one line in Mearsheimer linguistic fingerprint>
- Mercouris: <one line in Mercouris linguistic fingerprint>
```

**Linguistic fingerprint (required for each line):** Each option is **one line** (may wrap in chat) written **in-voice** for that mind — cadence, markers, and **moves** taken from the **LINGUISTIC FINGERPRINT** section of the trimmed stubs (read before writing):

- **Barnes:** [CIV-MIND-BARNES.md](../../../docs/skill-work/work-strategy/strategy-notebook/minds/CIV-MIND-BARNES.md) — e.g. constraint architecture / jurisdiction, liability and mechanism, rhetorical questions, declarative closes (“That’s the reality of it.” / “Period.”) where apt; **sardonic, sequential, minimal hedging** per table in stub.
- **Mearsheimer:** [CIV-MIND-MEARSHEIMER.md](../../../docs/skill-work/work-strategy/strategy-notebook/minds/CIV-MIND-MEARSHEIMER.md) — e.g. structural framing (“The fact is…”, “The question you have to ask yourself is…”), is/isn’t distinctions, power and incentives; **academic, blunt** register.
- **Mercouris:** [CIV-MIND-MERCOURIS.md](../../../docs/skill-work/work-strategy/strategy-notebook/minds/CIV-MIND-MERCOURIS.md) — e.g. nested qualification, reset pivots (“Now, it’s important to stress…”), legitimacy and institutional continuity; **long-form** density **compressed** to one line.

**Do not** emit generic analytical placeholders (e.g. “one line — power distribution”) without fingerprint. **Do not** parody or cartoon the voices; stay within WORK/strategy tone. If a fingerprint is uncertain, skim the stub’s fingerprint bullets then write.

**Rules:** Always **B → M → M** order (Barnes, then Mearsheimer, then Mercouris). Always optional (operator may skip or pick any combination). Appears alongside other WORK menu options (promote, pivot, verify), not as a separate menu. **Present, don't pre-develop:** these are **orienting** one-liners in-voice; do **not** generate the full lens analysis until the operator picks one. If the operator picks a lens, deliver analysis in chat and/or **inbox**; **append the lens block to the same day's `days.md` entry** only when the operator **directs** a notebook write or at **`dream`** fold — Recipes A/B/C in [MINDS-SKILL-STRATEGY-PATTERNS.md](../../../docs/skill-work/work-strategy/minds/MINDS-SKILL-STRATEGY-PATTERNS.md). If two lenses are run, include a **tension section** (see Recipe B). Trivial entries (minor link fix, one-line Open update) do not trigger the offer.

## Predictive History (`work-jiang`) — how it wires in

**Roles:** **Predictive History** is the **slow corpus** (lectures, book spine, registries). **`skill-strategy`** is **fast judgment** in the strategy-notebook. PH **feeds** strategy; it is **not** merged into SELF or Voice without the gate.

**When to pull PH in during a strategy pass**

- The operator’s question overlaps a **named crisis, region, or thesis** also treated in an ingested **lecture** or **analysis memo**.
- You are tightening **Islamabad / Gulf / Iran** outreach copy and need the **Jiang** line next to **analyst** or **Rome** lines already in the notebook.
- **`meta.md`** or **`Open`** points at **Part II Geo**, **Game Theory**, or another **volume** thread.

**Where to look (read-only unless the operator asks for corpus edits)**

| Need | Path |
|------|------|
| Book / volume map | [research/external/work-jiang/BOOK-ARCHITECTURE.md](../../../research/external/work-jiang/BOOK-ARCHITECTURE.md) and volume-specific `book/VOLUME-*.md` |
| Queue / status | [research/external/work-jiang/STATUS.md](../../../research/external/work-jiang/STATUS.md) |
| Lecture + digest | [research/external/work-jiang/lectures/](../../../research/external/work-jiang/lectures/) |
| Episode analysis stubs | [research/external/work-jiang/analysis/](../../../research/external/work-jiang/analysis/) |
| Channel pulls / ingest wiring | [research/external/youtube-channels/predictive-history/README.md](../../../research/external/youtube-channels/predictive-history/README.md); [common-inputs § PH](../../../docs/skill-work/work-strategy/common-inputs.md) |
| Islamabad × Jiang | [research/external/work-jiang/intake/](../../../research/external/work-jiang/intake/) (e.g. five-point + commentary) |

**Write surface — `### Jiang resonance (optional)`** in the day’s `days.md` block: one tight line with **series + episode** (e.g. Game Theory #20, `ue8y5e3HnHE`) or **lecture filename stem**, plus **Links** to the curated lecture and any **analysis** file. That is the **explicit wire** from PH into the notebook (see [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) § Parallel to Predictive History).

If the pass is **Islamabad / Gulf / Iran** but **no** lecture applies, use **one line**: e.g. `Jiang resonance: deferred — no new lecture id this pass` — avoid empty boilerplate. **Web-verified** headlines are **not** a substitute for an **ingested** thesis; do not imply PH alignment without a lecture or analysis link.

**Disambiguation:** **Book Volume I chapter `ch20`** (Geo-Strategy in the registry) is **not** the same label as **Game Theory #20** or another series’ “20.” State **volume + series + `video_id`** when both could confuse.

## History notebook (LIB-0156) — how it wires in

**Roles:** [History notebook](../../../docs/skill-work/work-strategy/history-notebook/README.md) is the operator’s **slow mechanism library** (compressed chapters, arcs, PH cross-map). **`skill-strategy`** remains **fast judgment** in the strategy-notebook. HN **informs** warrants and analogies; it is **not** merged into SELF or Voice without the gate.

**When to pull HN in during a strategy pass**

- Judgment uses **civilizational pattern language** (frontier, legitimacy, siege, naval hinge, tolerance → compression, …) that already has a **chapter id** or **arc** in [`book-architecture.yaml`](../../../docs/skill-work/work-strategy/history-notebook/book-architecture.yaml).
- You are stress-testing an **analogy** for Islamabad / outreach / Rome copy — cite the **HN chapter** + [analogy-audit](../../../docs/skill-work/work-strategy/analogy-audit-template.md) when the parallel ships publicly.
- **`meta.md`** or **`Open`** points at a **civilization arc** spanning volumes.

**Where to look (read-only unless the operator asks for HN edits)**

| Need | Path |
|------|------|
| Book / chapter SSOT | [`book-architecture.yaml`](../../../docs/skill-work/work-strategy/history-notebook/book-architecture.yaml) |
| PH ↔ HN coverage | [`cross-book-map.yaml`](../../../docs/skill-work/work-strategy/history-notebook/cross-book-map.yaml) · `python3 scripts/validate_cross_book.py` |
| Chapter prose + STYLE-GUIDE | [`history-notebook/`](../../../docs/skill-work/work-strategy/history-notebook/) |
| Polyphonic drafting | [`POLYPHONY-WORKFLOW.md`](../../../docs/skill-work/work-strategy/history-notebook/POLYPHONY-WORKFLOW.md) |

**Write surface — `### History resonance (optional)`** in the day’s `days.md` block: **chapter id(s)** (e.g. `hn-i-v1-04`) + **one mechanism line** + **Links** to the chapter file or anchor. Do **not** paste full HN chapters into the daily page. If no chapter applies: **none** or **deferred** — same honesty standard as **`### Jiang resonance`**.

**Out of scope for `skill-strategy`:** full **transcript ingest**, registry JSONL edits, or **skill-jiang** blind forward-chain — use [work-jiang-feature-checklist](../work-jiang-feature-checklist/SKILL.md) / `scripts/work_jiang/` when the operator is doing **corpus** work, not a notebook pass.

## Disambiguation

| Say this | Skill / tool |
|----------|----------------|
| **`strategy`**, **`strategy pass`**, **`work-strategy`** (this pass) | **`skill-strategy`** — notebook-primary |
| **`tri-mind`**, **`tri-frame`**, **`tutti`**, **`abc`** (after menu), **`ab`** / **`ac`** / **`bc`** (duet codes) | **`tri-mind`** — [tri-mind SKILL.md](../tri-mind/SKILL.md) (A=Mercouris, B=Mearsheimer, C=Barnes); not a substitute for the whole notebook pass unless the operator also says **`strategy`** |
| **`strategy` + web / verify / fact-check** | **`skill-strategy`** + [fact-check](../fact-check/SKILL.md) or explicit web search; citations go to notebook **Links** |
| Work-politics **stale docs / queue / campaign next actions** | `python3 scripts/operator_work_politics_pulse.py -u grace-mar` (no `strategy`-only skill) |
| **`weekly brief`** | [weekly-brief-run](../weekly-brief-run/SKILL.md) |
| **Generate today’s daily brief file** | `generate_work_politics_daily_brief.py` — see [work-strategy README](../../../docs/skill-work/work-strategy/README.md); **coffee** menu **A — Daily Brief** — not `strategy` Step 1 |
| **Rome / Vatican analytic pass** | [ROME-PASS.md](../../../docs/skill-work/work-strategy/work-strategy-rome/ROME-PASS.md) — can stack **after** or **beside** notebook judgment; not identical to a generic `strategy` day block |

## Anti-patterns

- **Thread-only or unlinked numbers** as notebook truth — especially for public-facing or campaign copy; use **+ verify** or **fact-check**.
- **Editing STRATEGY.md** from one volatile news day without operator **promote** intent.
- **Duplicating** full **pulse** output, **weekly brief** body, or **ROME-PASS** inside `days.md` — **link** and synthesize.
- **Triple narrative:** full brief + full transcript + notebook each a full recap — compress; notebook holds **warrants and links**.
- **Plane merge without tags:** same failure mode as Rome **mind–soul vs administrative** collapse — mixing **negotiation scope (A)**, **material/Hormuz facts (B)**, and **strategic narrative (C)** in one sentence without a seam. Use [template-three-lenses](../../../docs/skill-work/work-politics/analytical-lenses/template-three-lenses.md) **plane tags** / **(W)(A)(R)** or split sentences; see [transcript digest](../../../docs/skill-work/work-strategy/transcript-analysis-haiphong-ritter-johnson-iran-2026-04.md) and [STRATEGY-NOTEBOOK-ARCHITECTURE — Cross-artifact alignment](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#cross-artifact-alignment-planes-and-layers).

## Boundaries

- **WORK only** — not Record, not Voice knowledge unless material goes through RECURSION-GATE per `AGENTS.md`.
- Do **not** merge profile or gate candidates from this skill; staging only if the operator runs pipeline/gate workflow elsewhere.
