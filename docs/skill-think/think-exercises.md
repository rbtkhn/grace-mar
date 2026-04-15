# THINK — exercises and tests

**Purpose:** Add a lightweight exercise layer to THINK so capability claims are not only recorded, but also tested.

**Fits current doctrine:** THINK remains a Record-bound capability surface for intake, learning, and evidenced cognitive growth. These exercises do **not** replace EVIDENCE, IX, or WORK. They strengthen evidence for existing [maturity levels](think-levels.md) and improve judgment about whether a claim is merely exposed, or actually emerging / consistent / transferable / independent.

## Principles

- Prefer small, repeatable tests over large ceremonies.
- Tests should strengthen evidence for existing THINK levels.
- Tests should improve judgment about whether a claim is merely exposed, or actually emerging / consistent / transferable / independent.
- WRITE and STRATEGY may consume THINK outputs, but do not own THINK truth.

---

## Standard test types

### 1. `compression`

Turn 3-5 `READ-*` / `ACT-*` items into 1 capability claim.

**Goal:** Distinguish summary from capability.

**Prompt:**

> Using these evidence items, write one THINK claim that states a reusable capability rather than a summary of what was read.

**Return:**
- claim
- level
- evidence_ids
- why this is capability and not summary

### 2. `recall`

Explain a concept from memory after delay.

**Goal:** Distinguish temporary exposure from retained understanding.

**Prompt:**

> Explain this concept from memory in 4-6 sentences without checking notes.

**Then assess:**
- accurate / partly accurate / inaccurate
- what was missing
- whether this supports `exposed`, `emerging`, or `consistent`

### 3. `transfer`

Apply a concept in a different domain.

**Goal:** Justify `transferable` claims.

**Prompt:**

> Apply this concept from domain A to domain B and explain what changes and what remains the same.

**Return:**
- what transfers cleanly
- what does not transfer
- one useful judgment produced by the transfer
- whether this supports `transferable`

### 4. `contrast`

Differentiate a concept from nearby concepts.

**Goal:** Improve precision.

**Prompt:**

> Distinguish X from Y and Z, then give one example of each.

**Return:**
- one-sentence definition of each
- one example of each
- the most common confusion pattern

### 5. `failure_mode`

Identify how a capability usually breaks.

**Goal:** Support `consistent` level judgments.

**Prompt:**

> How does this capability usually fail, and what correction restores it?

**Return:**
- common failure mode
- what causes it
- what correction restores performance
- whether this supports `consistent`

### 6. `independent_use`

Perform the task with minimal or no operator structure.

**Goal:** Justify `independent` claims.

**Prompt:**

> Perform the same reasoning task with no template and no hints.

**Then assess:**
- quality of result
- whether operator structure was still implicitly needed
- whether this supports `independent`

---

## Scaffolding levels

| Level | Meaning |
|-------|---------|
| `full_template` | Full structure and hints provided |
| `hints_only` | Partial guidance; no template |
| `none` | No scaffolding; independent performance |

## Test result values

| Result | Meaning |
|--------|---------|
| `pass` | Meets the test goal cleanly |
| `partial` | Some success, some gaps |
| `fail` | Does not meet the test goal |

---

## Recording results

Add the following optional fields to the claim in [`think-claims.json`](../../artifacts/skill-think/think-claims.json):

| Field | Type | Purpose |
|-------|------|---------|
| `test_type` | string (enum) | Which test was run |
| `test_date` | date string | When |
| `test_result` | `pass` / `partial` / `fail` | Outcome |
| `scaffolding_level` | `full_template` / `hints_only` / `none` | How much support |
| `transfer_domain` | string (optional) | Target domain for transfer tests |
| `failure_mode_notes` | string (optional) | What breaks and how to fix it |
| `next_test` | string (optional) | Next intended test type |

See [`think_claims.schema.json`](../../schemas/skill_think/think_claims.schema.json) for the full schema.

---

## Promotion guidance

A claim is a stronger IX candidate when it has:
- repeated evidence across time
- at least one successful test beyond `compression`
- stable performance at reduced scaffolding
- no unresolved failure-mode concern

See [think-to-ix-promotion-rules.md](think-to-ix-promotion-rules.md) for the full promotion criteria.

---

## Weekly test loop

See [think-update-ritual.md](think-update-ritual.md) for the full update ritual. The weekly test loop adds:

1. Select 1-2 existing THINK claims.
2. Run 1 small test (`recall`, `transfer`, `contrast`, `failure_mode`, or `independent_use`).
3. Record the result in `think-claims.json`.
4. Update prose only if the test changed the real judgment.
5. Optionally append a receipt.

This doc is additive and compatible with the repo's existing THINK structure and update ritual.
