# Seed Registry

**Companion-Self template -- Per-claim lifecycle tracking during formation**

---

## Purpose

The Seed Registry makes individual observations trackable during companion formation. Instead of treating formation as a monolithic artifact bundle, each observation becomes a first-class object with its own lifecycle: first sighting, recurrence tracking, contradiction detection, confidence scoring, and governed promotion into durable state.

This sits between the existing **seed phase** (pre-activation artifact validation) and the **RECURSION-GATE** (post-activation governed merge). The registry holds claims that are not yet durable -- observations earning their way into identity.

---

## Core concept

```
observation --> seed claim --> recurrence --> evidence clustering --> governed promotion
```

A companion should earn its identity slowly, under review, from evidence, before anything becomes durable. The Seed Registry operationalizes that principle.

---

## Storage

`users/<id>/seed-registry.jsonl` -- append-only JSONL. Each line is a seed-claim snapshot. The latest line per `seed_id` is the current state. Full history is preserved (every status change appends a new line), enabling timeline reconstruction.

---

## Schema

`schema-registry/seed-claim.v1.json` -- required fields:

| Field | Type | Description |
|-------|------|-------------|
| `seed_id` | string | Unique ID (`seed-*` pattern) |
| `user_slug` | string | Companion slug |
| `claim_text` | string | The observation in natural language |
| `category` | enum | identity, curiosity, pedagogy, expression, memory_governance, safety, preference |
| `source_events` | array | Evidence refs (session IDs, transcript lines, artifacts) |
| `first_seen` | datetime | When this claim first appeared |
| `last_seen` | datetime | Most recent observation |
| `observation_count` | integer | How many times observed |
| `recurrence_score` | 0-1 | Computed from count, time span, and source diversity |
| `contradiction_count` | integer | Number of conflicting observations |
| `confidence` | 0-1 | Recurrence minus contradiction penalty |
| `status` | enum | Lifecycle position (see below) |
| `promotion_readiness` | 0-1 | Composite score for promotion candidacy |
| `sensitivity` | enum | standard, elevated, high -- determines threshold tier |

---

## Status lifecycle

```
observed --> weak_signal --> recurring --> candidate --> cross_evidenced --> stable --> promoted
                                      \                                           \--> rejected
                                       \--> expired
```

| Status | Meaning |
|--------|---------|
| `observed` | Seen once; no pattern yet |
| `weak_signal` | Interesting but too early to pattern-match |
| `recurring` | Observed multiple times across sessions |
| `candidate` | Meets promotion thresholds; ready for review |
| `cross_evidenced` | Supported by multiple independent sources |
| `stable` | High confidence, no contradictions, time-stable |
| `promoted` | Terminal: merged into governed state via gate |
| `rejected` | Terminal: operator decided against promotion |
| `expired` | Terminal: insufficient recurrence; timed out |

---

## Scoring

**Recurrence score** = weighted combination:
- Observation count (40%): logarithmic, saturates around 8+ observations
- Time span (35%): days between first and last observation, saturates at 30 days
- Source diversity (25%): distinct source events, saturates at 5+

**Confidence** = recurrence_score - contradiction_penalty (0.15 per contradiction, max 0.5 penalty)

**Promotion readiness** = (confidence + recurrence_score) / 2, halved if contradictions exist

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/emit_seed_claim.py` | Create or update a seed claim (CLI + importable) |
| `scripts/seed_registry_summary.py` | List, filter, group claims by status/category/readiness |

---

## Cross-references

- [seed-phase.md](seed-phase.md) -- Pre-activation artifact pipeline (existing v2)
- [seed-promotion-thresholds.md](seed-promotion-thresholds.md) -- Pluggable rules for when claims can promote
- [seed-nursery.md](seed-nursery.md) -- "Why is this still a seed?" explanations
- [seed-timeline.md](seed-timeline.md) -- Formation chronology
- [seed-phase-doctrine.md](seed-phase-doctrine.md) -- Constitutional principles
- [change-review.md](change-review.md) -- Post-activation governed revision
- [AGENTS.md](../AGENTS.md) -- Knowledge boundary, gated pipeline
