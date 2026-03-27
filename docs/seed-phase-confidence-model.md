# Seed Phase — Confidence model

**Companion-Self template · Confidence spec**

Confidence scores summarize **how well** each formation dimension is specified before activation. They are **not** model logits; they are **operator- or process-assigned** values in `0.0–1.0` (or derived from rubrics).

---

## Categories

| Category | Source artifact | Meaning |
|----------|-----------------|--------|
| **identity** | `seed_identity.json` | Clarity of name, role, boundaries, non-goals. |
| **curiosity** | `seed_curiosity.json` | Coverage of domains and policies. |
| **pedagogy** | `seed_pedagogy.json` | Coherence of teaching stance. |
| **expression** | `seed_expression.json` | Write/voice norms specified. |
| **memory_governance** | `seed_memory_contract.json` | Retention, deletion, protected regions. |
| **interaction_stability** | `seed_trial_report.json` | Consistency across trial scenarios. |
| **overall** | `seed_confidence_map.json` | Aggregate (may be weighted average or manual). |

---

## Bands (canonical)

Numeric scores map to bands used in prose and UI:

| Band | Range | Interpretation |
|------|-------|----------------|
| **low** | 0.00 – 0.39 | Insufficient for pass; usually blocking or requires re-stage. |
| **medium** | 0.40 – 0.74 | May proceed with **conditional_pass** if readiness policy allows. |
| **high** | 0.75 – 1.00 | Target for **pass**. |

Threshold constants are also stored in `seed_confidence_map.json` under `bands` for tooling.

---

## Per-artifact confidence fields

Each scaffold JSON may include a `confidence` object with a single primary score, e.g. `identity_confidence`. These feed into `seed_confidence_map.json` **confidence_map**; inconsistencies should be resolved before the readiness gate.

---

## Issues array

Artifacts may list `issues: string[]` for human-readable gaps. **Blocking** issues must be mirrored in `seed_readiness.json` under `blocking_issues`.

---

*Machine-readable schema: `schema-registry/seed-confidence-map.v1.json`.*
