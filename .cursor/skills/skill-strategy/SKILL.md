---
name: skill-strategy
preferred_activation: strategy
description: >-
  Primary trigger: strategy. Work-strategy pass — cross-territory judgment with strategy-notebook as the primary write surface;
  STRATEGY.md for watches and operator log when promoting stable arcs; Islamabad / Rome frameworks, weak-signal and analogy-audit
  discipline per work-strategy README. Wires to Predictive History (work-jiang) via notebook Jiang resonance + linked lectures/analysis — not work-politics pulse.
---

# Strategy pass (`skill-strategy`)

**Preferred activation (operator):** **`strategy`**. **Aliases:** **`strategy pass`**, **`work-strategy`**.

**Purpose:** Run a **bounded strategy pass** over work-strategy: produce or extend the **strategy-notebook** first; touch [STRATEGY.md](../../../docs/skill-work/work-strategy/STRATEGY.md) only when promoting watches, analogy lines, or operator log entries that have **stabilized**.

**Persistent frontier:** The repo holds the **running edge** (latest `days.md` block, **`### Open`**, **`### Links`**, **`meta.md`** when relevant). Each **`strategy`** invocation **updates** that checkpoint from the **last committed** block—tomorrow’s pass **reads disk**, not thread recall. Informal gloss: **memoized** strategy state (see [Accumulation and evolution](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md#accumulation-and-evolution) in the architecture doc).

## When to use

- The operator wants **cross-territory** synthesis (briefs, transcripts, frameworks, Rome/Islamabad threads) captured as **dated judgment**.
- Closing or continuing a **daily** or **monthly** arc in the notebook without duplicating the full pulse or weekly-brief workflows.

## Default moves (agent)

1. Read [strategy-notebook/STATUS.md](../../../docs/skill-work/work-strategy/strategy-notebook/STATUS.md) and the tail of the active month `chapters/YYYY-MM/days.md` (and `meta.md` if the month’s theme or open questions matter).
2. Follow [STRATEGY-NOTEBOOK-ARCHITECTURE.md](../../../docs/skill-work/work-strategy/strategy-notebook/STRATEGY-NOTEBOOK-ARCHITECTURE.md) for **Daily synthesis**, **Daily length and prose** (~**2000 words** per day ceiling — compress if over), and **Accumulation and evolution** (Signal / Judgment / Links / Open / Bets). Prefer **academic prose** in the notebook block.
3. **Append or extend** today’s block in `days.md` when the operator is logging judgment; link input paths (brief file, transcript digest, framework doc) in **Links**.
4. **STRATEGY.md:** suggest or apply updates only when the operator asks to **promote** — not every notebook entry.

**Lane index:** [work-strategy README](../../../docs/skill-work/work-strategy/README.md).

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

**Disambiguation:** **Book Volume I chapter `ch20`** (Geo-Strategy in the registry) is **not** the same label as **Game Theory #20** or another series’ “20.” State **volume + series + `video_id`** when both could confuse.

**Out of scope for `skill-strategy`:** full **transcript ingest**, registry JSONL edits, or **skill-jiang** blind forward-chain — use [work-jiang-feature-checklist](../work-jiang-feature-checklist/SKILL.md) / `scripts/work_jiang/` when the operator is doing **corpus** work, not a notebook pass.

## Disambiguation

| Say this | Skill / tool |
|----------|----------------|
| **`strategy`**, **`strategy pass`**, **`work-strategy`** (this pass) | **`skill-strategy`** — notebook-primary |
| Work-politics **stale docs / queue / campaign next actions** | `python3 scripts/operator_work_politics_pulse.py -u grace-mar` (no `strategy`-only skill) |
| **`weekly brief`** | [weekly-brief-run](../weekly-brief-run/SKILL.md) |

## Boundaries

- **WORK only** — not Record, not Voice knowledge unless material goes through RECURSION-GATE per `AGENTS.md`.
- Do **not** merge profile or gate candidates from this skill; staging only if the operator runs pipeline/gate workflow elsewhere.
