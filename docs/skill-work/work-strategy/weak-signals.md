# Weak Signals + Analogy Audit

**Status:** WORK only.  
**Scope:** `work-strategy` operator discipline for early signal detection, historical pattern testing, and promotion into local strategy memory.  
**Record boundary:** No direct Record, SELF, EVIDENCE, or Voice writes. Promotion beyond WORK requires `RECURSION-GATE` + companion approval.

---

## Purpose

This file defines the lane-level discipline for handling **weak signals** inside `work-strategy`.

A weak signal is an early, incomplete, or low-confidence pattern that may become strategically important but is not yet strong enough to be treated as a lead theme, stable doctrine, or durable lane conclusion.

This discipline exists to prevent two opposite errors:

1. **Missing real change too early** because the pattern still looks fragmentary.
2. **Overclaiming from noise** by turning suggestive headlines into false strategic certainty.

To reduce both errors, every meaningful weak signal should be tested through a short **analogy audit** before it is promoted into longer-lived strategy memory.

---

## Definitions

### Weak signal

A low-to-medium-confidence pattern with potential strategic importance.

Typical examples:

- alliance drift before open realignment
- sanctions fatigue before policy reversal
- soft-power repositioning before institutional change
- elite narrative fracture before formal political break
- energy chokepoint stress before overt supply disruption
- product/governance trend before category consolidation

### Analogy audit

A short historical and structural test applied to a weak signal.

The analogy audit is not permission to force-fit the present into history. Its purpose is to:

- generate plausible strategic framing
- expose where the analogy breaks
- prevent lazy pattern projection
- clarify falsifiers and boundary conditions

### Promotion

A weak signal may be promoted into `STRATEGY.md` only when:

- it recurs across multiple briefs, or
- the evidence strengthens materially, or
- it clearly affects strategic prioritization, framing, or risk posture

### Retirement

A weak signal should be retired when:

- it fails its falsifier
- it stops recurring
- it loses explanatory power
- it is absorbed into a broader pattern already tracked elsewhere

---

## Daily rule

Each daily brief should include **one weak signal worth watching** when a credible candidate exists.

In generated briefs this appears as **§1f** (after **§1d** Putin — last 48 hours and **§1e** JD Vance — last 48 hours). Use a compact operator block, not a separate detached memo.

If no credible weak signal exists that day, the section may explicitly say:

> No credible weak signal exceeded the threshold today.

That is acceptable and preferable to filler.

---

## Required fields for each weak signal

- **Signal**
- **Domain**
- **Why it may matter**
- **Current evidence**
- **Confidence**
- **Time horizon**
- **Analogy candidate**
- **Best fit**
- **Best mismatch**
- **Falsifier**
- **Status**
- **If true, implication for strategy**

---

## Confidence standard

Use only:

- **low**
- **medium**

Do not mark a weak signal as **high** confidence.  
If confidence becomes high, it is probably no longer a weak signal and should be promoted, converted into a lead theme, or logged as a stronger watch item.

---

## Status values

Use only:

- **watch**
- **escalating**
- **decision-point** — structured options open; use [decision-point-template.md](decision-point-template.md)
- **retired**
- **promoted**

---

## Promotion rule

Promote into `STRATEGY.md` when one or more of the following are true:

- the signal appears in multiple daily briefs
- it survives multiple analogy audits without collapsing
- it changes strategic focus, framing, or operator priority
- it creates a new recurring lens, caution, or watch item for the lane

**When to open a decision point instead of promoting directly:** If the watch is escalating and there are multiple plausible responses with real tradeoffs, open a decision point (`decision-point` status) using [decision-point-template.md](decision-point-template.md) before committing to a recommendation. If the watch has a clear outcome and no branching options, promote directly.

Promotion targets:

- `## II-A. ACTIVE WATCHES`
- `## III-A. ANALOGY WATCHLIST`
- `## IV. Operator strategy log` (WORK-local dated log in this file)

---

## Failure rule

Do not preserve weak signals merely because they were interesting.

Retire them cleanly when they fail.

When retiring:

- state what failed
- state whether the analogy was misleading
- preserve the error as calibration material when useful

---

## Relationship to existing work-strategy flow

This discipline extends the current lane shape:

- Daily brief: adds one compact weak-signal block (**§1f**)
- Current-events analysis: inserts a mandatory analogy audit before triangulation when a historical parallel is proposed
- STRATEGY ledger: receives promoted watches, recurring analogies, and operator strategy log entries (**§IV**)

This is a **WORK-local strategic watch discipline**, not a replacement for `work-politics`, `work-civ-mem`, or the external `civilization_memory` repository.

---

## Operator standard

The standard is:

- notice early
- compare carefully
- preserve contradictions
- promote slowly
- retire honestly

This matches the lane’s WORK-only boundary and additive memory logic already described in the README and STRATEGY.md.
