# WORK-LEDGER — work-dev

**Status:** WORK only — optional **judgment / compounding** layer.  
**Scaffold source:** [work-template/WORK-LEDGER.md](../work-template/WORK-LEDGER.md).  
**Canonical operator surface:** [workspace.md](workspace.md) stays first for day-to-day state and next actions.

**Rule:** Additive-first. Do not silently rewrite durable lane memory. Preserve contradictions, revisions, and retirements explicitly.

**Governance — §V vs II-A / III-A / IV:** Treat **II-A**, **III-A**, and **IV** as systems of record for those entry types. Use **§V** only as a sparse changelog (pointers, dates, why) — do not duplicate full watch rows in II-A and V.

**Not:** Record truth; not a substitute for [INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md), [openclaw-integration.md](../../openclaw-integration.md), or the companion gate. Promotion to SELF / EVIDENCE / prompt only via **RECURSION-GATE** + companion approval + merge script per [AGENTS.md](../../AGENTS.md).

---

## I. CORE

### Territory identity

- **Lane name:** work-dev  
- **Purpose:** Connect Grace-Mar (Record + Voice) with OpenClaw — identity export, session continuity, handback, **stage-only** automation — companion always gate.  
- **Primary operator use-case:** Integration health, export/handback rhythm, portability vs vendor lock-in for documented identity.  
- **Boundary summary:** OpenClaw may **stage**; it must **not merge** into the Record. Companion sovereignty is non-negotiable. See [README.md](README.md) **Invariant** and **Principles**.  
- **Promotion gate:** `users/grace-mar/recursion-gate.md` for anything crossing into Record/Voice; lane docs are git/PR workflow unless a milestone is explicitly gated (see README).

### Decision style

- **Default mode:** Spec- and contract-first ([INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md), [session-continuity-contract.md](session-continuity-contract.md)).  
- **Preferred synthesis style:** Pointer-heavy; long doctrine stays in linked files.  
- **Escalation threshold:** When integration state diverges from docs — refresh [integration-status.md](integration-status.md) / [known-gaps.md](known-gaps.md) or [workspace.md](workspace.md).  
- **Known failure modes:** Draft-as-truth, silent merge assumptions, treating OpenClaw memory as authoritative over the gated Record — see [three-compounding-loops.md](three-compounding-loops.md).

---

## II. LANE-SPECIFIC CORE

### Current focus

- See **[workspace.md](workspace.md)** — live priorities and blockers.

### Active priorities

- See **[workspace.md](workspace.md)** and **[INTEGRATION-PROGRAM.md](INTEGRATION-PROGRAM.md)** read order.

### Active capabilities

- Export / handback scripts and paths in [openclaw-integration.md](../../openclaw-integration.md) and README **Quick Reference**.

### Known blind spots

- See **[known-gaps.md](known-gaps.md)** and generated `generated/known-gaps.generated.md` when present.

### Active constraints

- Companion gate; stage-only for OpenClaw; knowledge boundary for Voice — [README.md](README.md) **Principles**.

---

## II-A. ACTIVE WATCHES

*(Emerging technical / integration patterns worth monitoring. **Do not fabricate** — add only when grounded in [integration-status.md](integration-status.md), [known-gaps.md](known-gaps.md), or [workspace.md](workspace.md).)*

**Entry format**

- **Watch:** short label  
- **First noticed:** YYYY-MM-DD  
- **Current status:** watch / escalating / promoted-to-ledger / retired  
- **Latest evidence:** short note + link  
- **Framing note:** what model or comparison is helping  
- **Primary implication:** why the lane should care  
- **Contradiction / caution:** what may invalidate the watch  

**Entries**

- *(empty until used)*

---

## III. LEARNING LEDGER

*(Durable heuristics live in README **Principles** and **three-compounding-loops** first; append here only when you want lane-specific operator shorthand.)*

### Stable heuristics

- See [README.md](README.md) § **Principles** and [three-compounding-loops.md](three-compounding-loops.md).

### Repeated lessons

- _TBD — append with dates when recurring integration lessons stabilize._

### Known anti-patterns

- _TBD — link to agent-reliability / safety-story docs when filing._

### Deprecated / retired models

- _TBD_

---

## III-A. FRAMING WATCHLIST

*(Benchmarks, architecture comparisons, positioning frames — e.g. before major integration bets.)*

**Entry format**

- **Frame:** short label  
- **Last applied:** YYYY-MM-DD + context  
- **What it explains well:** short note  
- **Where it misleads:** short note  
- **Usefulness:** low / medium / high  
- **Risk of overextension:** low / medium / high  
- **Usage mode:** illustrative / framing only / core model  

**Entries**

- *(empty until used)*

---

## IV. LOCAL MEMORY / EXECUTION LOG

*(Prefer [workspace.md](workspace.md) for day-to-day; use this section for cross-cutting ledger notes if needed.)*

### Open threads

- See [workspace.md](workspace.md).

### Recent decisions

- _TBD_

### Recent experiments

- _TBD_

### Follow-up items

- See [workspace.md](workspace.md).

---

## V. PROMOTION / RETIREMENT RECORD

*(Sparse changelog only.)*

### Promoted items

- _TBD_

### Retired items

- _TBD_

### Calibration notes

- _TBD_

---

## VI. GOVERNANCE NOTES

### Write rules

- WORK-local only. No merge into `self.md`, `self-archive.md`, or `bot/prompt.py` from this file.  
- Align with [README.md](README.md) invariant: stage-only OpenClaw; companion merges Record.

### Review cadence

- With [workspace.md](workspace.md) refresh; optional pass when [integration-status.md](integration-status.md) changes materially.

### Promotion conditions

- **To this ledger:** recurring operator judgment worth tracking — cite evidence.  
- **To Record:** RECURSION-GATE + companion approval only.

### Retirement conditions

- Watch falsified or absorbed into a stronger tracked item — log briefly in §V if useful.
