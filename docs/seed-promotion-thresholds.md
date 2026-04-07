# Seed Promotion Thresholds

**Companion-Self template -- Pluggable rules for governed identity formation**

---

## Purpose

Promotion thresholds define when a seed claim has earned enough evidence to become a candidate for governed state. They prevent premature identity collapse by requiring recurrence, time stability, and contradiction resolution before any observation becomes durable.

---

## Configuration

Rules live in `config/seed-promotion-rules.json`. Operators may tighten thresholds; loosening below defaults should be documented.

---

## Default thresholds

| Rule | Default | Rationale |
|------|---------|-----------|
| `min_observations` | 2 | No promotion from a single observation |
| `min_sessions` | 2 | Must appear across multiple sessions |
| `min_time_span_days` | 7 | Time stability: not just one excited day |
| `recurrence_score_threshold` | 0.6 | Composite score must clear this bar |
| `contradiction_policy` | `block_until_resolved` | Contradicting evidence blocks promotion |

---

## Sensitivity tiers

Each seed claim carries a `sensitivity` field that selects which tier of thresholds applies.

| Tier | When to use | Additional requirements |
|------|-------------|------------------------|
| **standard** | Default for most observations | Defaults above |
| **elevated** | Identity-shaping claims, behavioral patterns | 3 observations, 3 sessions, 14 days, operator flag |
| **high** | Safety-related, deeply personal, irreversible implications | 5 observations, 4 sessions, 21 days, explicit operator approval, contradictions always block |

---

## Category overrides

Some categories automatically raise the sensitivity floor:

| Category | Sensitivity floor | Additional rules |
|----------|-------------------|------------------|
| `identity` | `elevated` | 3 observations, 14 days minimum |
| `safety` | `high` | 4 observations, 21 days minimum |

Other categories (`curiosity`, `preference`, `expression`, `pedagogy`, `memory_governance`) use the claim's declared sensitivity.

---

## Rule merging order

When evaluating a claim, rules merge in this order (later overrides earlier):

1. `defaults` -- baseline rules
2. `sensitivity_overrides[claim.sensitivity]` -- tier-specific adjustments
3. `category_overrides[claim.category]` -- category-specific adjustments (including `sensitivity_floor` upgrade)

---

## Evaluation verdicts

| Verdict | Meaning |
|---------|---------|
| **ready** | All thresholds met; claim can be promoted to governed review |
| **approaching** | Within one observation or flag of readiness |
| **blocked** | One or more hard requirements unmet |

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/evaluate_seed_promotion.py` | Evaluate all active claims against rules |
| `scripts/evaluate_seed_promotion.py --advance` | Auto-advance statuses based on evaluation |
| `scripts/seed_to_gate.py` | Convert a ready claim to RECURSION-GATE candidate (grace-mar only) |

---

## Ethics as executable rules

The threshold system makes ethical principles concrete:

- **"No promotion from a single observation"** = `min_observations >= 2`
- **"Sensitive claims require stricter thresholds"** = `sensitivity_overrides`
- **"Contradiction blocks promotion until reviewed"** = `contradiction_policy: block_until_resolved`
- **"Behavioral claims need recurrence plus context diversity"** = `recurrence_score_threshold`
- **"Identity-shaping claims require operator approval"** = `requires_operator_flag` / `requires_operator_approval`

---

## Cross-references

- [seed-registry.md](seed-registry.md) -- Claim lifecycle and scoring
- [seed-nursery.md](seed-nursery.md) -- Why claims stay in nursery
- [seed-phase-doctrine.md](seed-phase-doctrine.md) -- Constitutional principles
- [seed-phase-readiness.md](seed-phase-readiness.md) -- Existing activation gate (fork-level)
