# Working-identity candidates

A working-identity candidate is a structured proposal representing portable working-intelligence extracted from an external AI system, observed at runtime, or noted manually by the operator. Candidates are **non-canonical review material** — they represent what an external source believes about the companion, not what the Record has confirmed.

---

## What candidates are

Each candidate captures a single observation or claim about how the companion works, what they know, how they behave, or what they've built. Candidates are classified by layer (domain, workflow, behavioral, artifact), confidence, durability, sensitivity, and portability.

Candidates are the **input** to the review pipeline. They are not facts until reviewed and approved.

---

## What candidates are not

- Not canonical Record content. A candidate in `pending` state has no authority over SELF, SELF-LIBRARY, SKILLS, or EVIDENCE.
- Not a second memory system. Candidates enter the existing gated pipeline — `recursion-gate.md` staging, companion approval, `process_approved_candidates.py` merge.
- Not auto-merged. No candidate becomes Record truth without explicit human review.

---

## Schema

The formal schema is at [`schema-registry/working-identity-candidate.v1.json`](../../schema-registry/working-identity-candidate.v1.json).

### Required fields

| Field | Type | Description |
|---|---|---|
| `candidate_id` | string | Unique identifier (convention: `WI-NNNN`) |
| `source_type` | enum | `external_ai_extract`, `internal_runtime_observation`, `manual_operator_note` |
| `layer_type` | enum | `domain_encoding`, `workflow_calibration`, `behavioral_calibration`, `artifact_rationale` |
| `claim` | string | One-sentence description of the observation |
| `confidence` | enum | `high`, `medium`, `low` |
| `durability_class` | enum | `ephemeral`, `recurring`, `stable` |
| `sensitivity_class` | enum | `safe`, `review_required`, `non_portable` |
| `portability_class` | enum | `cross_tool`, `role_specific`, `employer_bound`, `non_exportable` |
| `proposed_target_surface` | enum | `SELF`, `SELF-LIBRARY`, `SKILLS`, `EVIDENCE` |

### Recommended fields

| Field | Type | Description |
|---|---|---|
| `source_tool` | string | Name of the AI system that produced this candidate |
| `source_window` | string | Time period the source observed this pattern |
| `supporting_examples` | array of strings | Concrete evidence supporting the claim |
| `review_status` | enum | `pending`, `approved`, `rejected`, `modified` |
| `review_notes` | string | Reviewer notes |

---

## Review process

1. **Extract** — Use the [extraction prompt pack](extraction-prompt-pack.md) or manual observation to produce candidates
2. **Normalize** — Structure each item as a working-identity candidate per the schema
3. **Stage** — Add candidates to `users/<id>/recursion-gate.md` with `candidate_type: identity_update` (or the appropriate type) and `territory: portable-working-identity`
4. **Review** — Companion reviews each candidate, approves, rejects, or modifies
5. **Merge** — Approved candidates are merged via `scripts/process_approved_candidates.py` into the appropriate Record surface

Candidates with `sensitivity_class: non_portable` or `portability_class: non_exportable` should be reviewed with extra care and typically rejected from the portable Record.

---

## Related

- [extraction-prompt-pack.md](extraction-prompt-pack.md) — how to extract candidates from external AI systems
- [current-capability-map.md](current-capability-map.md) — portability capability inventory
- [../portable-working-identity.md](../portable-working-identity.md) — portability doctrine and four-layer mapping
- [`schema-registry/working-identity-candidate.v1.json`](../../schema-registry/working-identity-candidate.v1.json) — formal JSON Schema
- [promotion-rules.md](promotion-rules.md) — where approved candidates land in the Record
- [import-external-working-identity.md](import-external-working-identity.md) — how to import extracted candidates
