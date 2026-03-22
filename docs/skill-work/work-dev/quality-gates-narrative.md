# Quality gates for identity — operator + partner narrative

**Purpose:** Treat **evals and CI checks** as a **product surface**, not a hidden engineering chore. Same checks that protect the fork are the **story** you tell operators and partners: *green means within boundary*.

---

## One-sentence pitch

**Identity and integration stay inside agreed boundaries when these gates pass** — not because the model “feels right,” but because **automated checks + human gate** encode stewardship.

---

## The “green = within boundary” map

Use this table to align **scripts/tests** with **what they defend**. Nothing here replaces **RECURSION-GATE approval**; these gates defend **engineering truth** (prompt boundary, repo shape, continuity contract).

| Gate | What it defends | Typical command / signal |
|------|-----------------|---------------------------|
| **Counterfactual harness** | Voice stays inside documented knowledge; stress probes | `python scripts/run_counterfactual_harness.py` |
| **Voice linguistic authenticity** | Lexile / voice fingerprint expectations | `python scripts/test_voice_linguistic_authenticity.py` |
| **Integrity** | Canonical layout, derived exports not stale | `python scripts/validate-integrity.py --user grace-mar` |
| **Governance** | Repo policy / structure | `python scripts/governance_checker.py` |
| **Continuity CI** | `continuity_read_log.py` dry-run + grace-mar paths exist | `pytest tests/test_continuity_read_log.py` — **product meaning:** the continuity *contract* stays executable; see [session-continuity-contract.md](session-continuity-contract.md). |
| **Gate health** (manual / derived) | Stale pending, time-in-gate — see [economic-benchmarks.md](economic-benchmarks.md) | `operator_blocker_report`, `recursion_gate_review`, session brief |

**Partner-facing line (short):** *We treat evals as guardrails you can see — not vibes — so the fork doesn’t drift from the companion’s knowledge boundary.*

---

## Operator dashboard (conceptual)

**Future product shape:** one surface that aggregates **pass/fail** for harness + integrity + (optional) gate staleness metrics — **green** when boundary checks pass; **yellow/red** when something needs review or a script failed. Pair with **visible pipeline state** (pending vs approved, receipts, staged vs merged) as the **safety story** — see [safety-story-ux.md](safety-story-ux.md).

This repo does **not** yet ship that UI; the **narrative** above is the contract: when you build or sell a dashboard, it should answer: **“Is the fork still within boundary?”** not only **“Did the model run?”**

---

## Relation to other docs

- **[agent-reliability-playbook.md](agent-reliability-playbook.md)** — failure modes and mitigation layers.
- **[economic-benchmarks.md](economic-benchmarks.md)** — instrumented vs manual; gate metrics.
- **[variation-types.md](variation-types.md)** — factorial stressors for eval design.
- **AGENTS.md** — success metrics (harness, voice benchmark) as repo invariants.

---

## Guardrail

Do not claim **full** “green” if **compute-ledger** cost rows or **aggregation** scripts are still **planned** — see [economic-benchmarks.md](economic-benchmarks.md). Honesty is part of the product story.
