# skill-think — observability

**Purpose:** Inspect **cognitive capability claims** over time — not identity, not gate queue.

## Artifact

- **Generated:** `artifacts/skill-think/think-observability.json` via [build_think_observability.py](../../scripts/build_think_observability.py).
- **Source:** [think-claims.json](../../artifacts/skill-think/think-claims.json).

## Relationship to other observability

- **Change proposals:** [build-observability-report.py](../../scripts/build-observability-report.py) outputs `observability-report.v1` — **do not** merge THINK metrics into that JSON without extending its schema.
- **Work layer:** [WORK-LAYER-HARDENING-ROADMAP.md](../WORK-LAYER-HARDENING-ROADMAP.md) — parallel pattern.

## Metrics (v1)

| Field | Meaning |
|-------|---------|
| `claim_count` | Rows in `think-claims.json` |
| `claims_by_capability_type` | Histogram |
| `claims_by_level` | Histogram |
| `claims_updated_last_30d` | Recency |
| `claims_with_multiple_evidence_refs` | Evidence depth |
| `open_promotion_candidates` | `promotion_candidate: true` |
| `top_topics` | Frequent topic strings (top 5) |
