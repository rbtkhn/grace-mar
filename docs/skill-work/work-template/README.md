# WORK-TEMPLATE — Generic WORK territory pattern library

**Status:** Template / scaffold  
**Scope:** Reusable architecture for any WORK territory (`work-strategy`, `work-politics`, `work-dev`, future `work-*` lanes).  
**Boundary:** WORK only. No direct Record, SELF, EVIDENCE, or Voice writes. Promotion beyond WORK requires the lane’s gate and companion approval where Record or Voice are affected.

**Relation to MV checklist:** **Tier 0** onboarding steps live in [work-template.md](../work-template.md) (README + history + registry). This folder is the **deeper pattern library** (ledger, daily surface, emerging patterns, multi-frame review).

---

## Purpose

A WORK territory is an operator-facing lane used to:

- collect inputs  
- interpret signals  
- stage judgments  
- preserve local working memory  
- support decisions and downstream artifacts  

It is **not** a truth surface by itself. It is a governed workspace for analysis, synthesis, planning, experimentation, and **gated** promotion.

---

## Lane contract templates (hardening)

Copy-paste stubs for new `work-*` lanes: [lane-contract.template.md](lane-contract.template.md), [authorized-sources.template.yaml](authorized-sources.template.yaml), [lane-observability.template.json](lane-observability.template.json), [decision-ladder.template.md](decision-ladder.template.md). Roadmap: [WORK-LAYER-HARDENING-ROADMAP.md](../WORK-LAYER-HARDENING-ROADMAP.md).

## Glossary (lifecycle)

- **Promoted-to-ledger:** A pattern, heuristic, or watch is recorded in the lane’s **WORK-LEDGER** (or lane-specific equivalent such as [STRATEGY.md](../work-strategy/STRATEGY.md)). Still WORK-only.  
- **Promoted-to-Record:** Content crosses into **SELF**, **EVIDENCE**, or **prompt** only via **RECURSION-GATE** + companion approval + `process_approved_candidates.py` per [AGENTS.md](../../AGENTS.md).

Do not use **“promoted”** alone when both meanings could apply; specify ledger vs Record.

---

## Core design principles

1. **Boundary first** — WORK lanes do not directly overwrite Record, SELF, EVIDENCE, or Voice; all promotion beyond WORK is gated. See [BOUNDARY.md](BOUNDARY.md).  
2. **One daily horizon** — Compact daily surface for operator review; distinguish **fast** inputs from **slow** background context.  
3. **Emerging patterns over premature certainty** — Early, incomplete patterns that might matter; test before promotion. See [emerging-patterns.md](emerging-patterns.md).  
4. **Multiple frames before synthesis** — Important questions through more than one frame; preserve productive tensions when useful. See [multi-frame-review.md](multi-frame-review.md).  
5. **Compounding lane memory** — Local ledger for heuristics, watches, experiments, execution memory. See [WORK-LEDGER.md](WORK-LEDGER.md).  
6. **Promotion and retirement discipline** — Lifecycle states; retire weak or falsified patterns honestly.  

---

## Adoption tiers

| Tier | Name | Artifacts |
|------|------|-----------|
| **0** | **Minimum viable lane** | [work-template.md](../work-template.md): `work-<id>/README.md`, `work-<id>-history.md`, register in [skill-work README](../README.md) and [work-modules-history-principle](../work-modules-history-principle.md). |
| **1** | **Minimal architecture** | [BOUNDARY.md](BOUNDARY.md) (or excerpt in README) + [WORK-LEDGER.md](WORK-LEDGER.md) + [daily-brief-template.md](daily-brief-template.md) (semantic section titles — no fixed § numbers). |
| **2** | **Signals + frames** | Tier 1 + [emerging-patterns.md](emerging-patterns.md), [emerging-pattern-template.md](emerging-pattern-template.md), [framing-audit-template.md](framing-audit-template.md), [multi-frame-review.md](multi-frame-review.md). |
| **3** | **Full** | Tier 2 + [background-context.md](background-context.md), [lane-cadence.md](lane-cadence.md) (not `cadence.md` — avoids confusion with [work-cadence/](../work-cadence/) telemetry territory), plus optional [weekly-review.md](weekly-review.md), [experiment-log.md](experiment-log.md), [promotion-rules.md](promotion-rules.md). |

Lanes may stop at any tier. Do not copy nine files into a thin lane “because the template said required.”

---

## Canonical operating loop

1. **Ingest** — Headlines, repos, notes, events, tickets, memos, conversations, task outputs (lane-specific).  
2. **Lane snapshot** — Compact operator view of the lane today.  
3. **Background context** — Slower-moving context that interprets current inputs ([background-context.md](background-context.md)).  
4. **Emerging pattern check** — One or more early patterns worth monitoring when credible.  
5. **Framing audit** — Test important frames, analogies, or models before relying on them ([framing-audit-template.md](framing-audit-template.md)).  
6. **Multi-frame review** — Multiple perspectives on the same problem before synthesis (frames defined per lane — see [MAPPING.md](MAPPING.md)).  
7. **Synthesis** — What matters, what is uncertain, what to do next, what to watch.  
8. **Promotion / retirement** — Durable items into the ledger; retire falsified or exhausted items.  

---

## Required template primitives (by concept)

| Primitive | Description |
|-----------|-------------|
| **A. Boundary contract** | What the lane is for; what it may write; what it may not; how promotion works; which gate applies. |
| **B. Daily horizon** | Lane snapshot, focus, fast vs slow, optional emerging-pattern block, synthesis, next actions. |
| **C. Emerging-pattern lifecycle** | watch → escalating → **promoted-to-ledger** or **retired** (align status labels with lane habits). |
| **D. Framing audit** | Test whether a proposed framing is useful before it hardens into doctrine. |
| **E. Multi-frame review** | At least 2–3 recurrent frames; **definitions** live in a lane manifest or table, not duplicated in the procedure doc. |
| **F. Lane ledger** | Compounding WORK-local memory. |

---

## How to specialize (examples)

| Lane | Emerging patterns | Framing audit | Multi-frame review | Background context |
|------|-------------------|---------------|--------------------|--------------------|
| **work-strategy** | Weak geopolitical / civilizational signals ([weak-signals.md](../work-strategy/weak-signals.md)) | Analogy / historical parallel ([analogy-audit-template.md](../work-strategy/analogy-audit-template.md)) | Strategic lenses + triangulation ([current-events-analysis.md](../work-strategy/current-events-analysis.md)) | Civilizational / historical slow layer (e.g. work-jiang, CIV-MEM) |
| **work-dev** | Architecture / product / tooling shifts | Benchmark or architecture comparison audit | Product / architecture / operations | Debt, constraints, roadmap, platform state ([workspace.md](../work-dev/workspace.md)) |
| **work-politics** | Coalition / narrative / campaign shifts | Electoral or institutional precedent audit | Persuasion / coalition / institutional ([analytical-lenses/manifest.md](../work-politics/analytical-lenses/manifest.md)) | District, donors, legal timing, coalition structure |

**Lane → file mapping:** [MAPPING.md](MAPPING.md).

---

## Repo machinery (light touch)

- **Gate / Record:** [AGENTS.md](../../AGENTS.md) — merge only via script after companion approval.  
- **Operator menus:** [work-menu-conventions.md](../work-menu-conventions.md).  
- **Lane prefixes:** [operator-agent-lanes.md](../../operator-agent-lanes.md).  
- **Coffee / daily brief habit:** [.cursor/skills/coffee/SKILL.md](../../../.cursor/skills/coffee/SKILL.md), [work-coffee/README.md](../work-coffee/README.md) — e.g. work-strategy combined brief is **coffee menu C — Strategy (daily brief)** (generator does not run in coffee Step 1).  
- **PR labels:** Many lanes use [LANE-CI.md](../work-strategy/LANE-CI.md)-style labeling; mirror per lane.  

---

## Contents (this folder)

| File | Tier | Role |
|------|------|------|
| [README.md](README.md) | — | This index |
| [BOUNDARY.md](BOUNDARY.md) | 1+ | Copy-paste boundary checklist |
| [MAPPING.md](MAPPING.md) | — | Existing lanes ↔ template concepts |
| [WORK-LEDGER.md](WORK-LEDGER.md) | 1+ | Generic ledger scaffold |
| [daily-brief-template.md](daily-brief-template.md) | 1+ | Semantic daily surface (example mapping for work-strategy) |
| [emerging-patterns.md](emerging-patterns.md) | 2+ | Generic emerging-pattern discipline |
| [emerging-pattern-template.md](emerging-pattern-template.md) | 2+ | Block template |
| [framing-audit-template.md](framing-audit-template.md) | 2+ | Generic framing audit (+ link to strategy analogy form) |
| [multi-frame-review.md](multi-frame-review.md) | 2+ | Procedure; points to per-lane frame registry |
| [background-context.md](background-context.md) | 3 | Slow-layer stub |
| [lane-cadence.md](lane-cadence.md) | 3 | Lane rhythm stub (distinct from work-cadence territory) |
| [weekly-review.md](weekly-review.md) | 3 (opt) | Weekly rhythm + skill pointers |
| [experiment-log.md](experiment-log.md) | 3 (opt) | Stub |
| [promotion-rules.md](promotion-rules.md) | 3 (opt) | Stub; points back to README tiers |

---

## Promotion rule (ledger)

Promote into the lane ledger when the pattern recurs, evidence strengthens, framing survives audit, or synthesis changes priorities. **Promoted-to-Record** is a separate, gated step.

## Retirement rule

Retire when falsifier hits, recurrence stops, explanatory power drops, or a stronger pattern subsumes the item. Retired items may remain as **calibration** notes in the ledger.

## Standard

Observe early → frame carefully → compare honestly → synthesize slowly → promote selectively → retire cleanly.

---

## Risk-mitigation checklist (Tier 1+)

Any WORK territory that creates **ongoing obligations** (active artifacts, external dependencies, recurring operator tasks) should address these four patterns. Copy the relevant sections into the lane's README or WORK-LEDGER and fill in. Thin lanes with no ongoing obligations may skip.

### 1. Quantitative success criteria

Define how you know the lane or artifact is working. At least 2–3 measurable targets before shipping. Examples: retrieval precision, review time budget, propagation reach, signal-to-noise ratio. Without numbers, "success" is unfalsifiable.

**Template:**

| Metric | Target | How to measure |
|--------|--------|----------------|
| _metric_ | _threshold_ | _method_ |

### 2. Sustainment table

List recurring maintenance tasks that prevent silent degradation. Each task needs a cadence and a check. If the lane has no maintenance tasks, it probably has no ongoing obligations and doesn't need this section.

**Template:**

| Task | Cadence | What to check |
|------|---------|---------------|
| _task_ | _weekly / monthly / quarterly / on-event_ | _what to verify_ |

### 3. Deprecation / retirement path

Document what happens when the lane, artifact, or dependency is abandoned. The answer should be "cleanup, not migration" — if retiring a lane requires a complex data migration, the architecture has a coupling problem.

**Template:**

1. Stop [active process].
2. Clear pending items normally.
3. Archive docs to `[lane]-archived/` with a README note.
4. Remove scripts / automation. No data is lost.

### 4. Scope creep guardrail

Name the boundary that prevents incremental expansion beyond the lane's original purpose. If a proposed feature crosses this boundary, it requires a new plan or ADR, not an incremental PR.

**Template:**

> Any feature that introduces [specific expansion pattern] requires a [new plan / ADR / operator decision]. This lane's charter does not authorize [specific out-of-scope pattern].

---

**Reference implementation:** [work-strategy/](../work-strategy/README.md).
