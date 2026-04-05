# Evidence to proposal

Companion-Self template · Staged step from inputs to a proposal file

---

## Purpose

Convert raw or staged **evidence** (and optionally **prepared context**) into a **visible proposal object** without silently mutating governed state.

This is a **reference** sequence. The dependable part is **data + schema + validation**, not any single agent skill or chat turn.

---

## Stages

1. **Identify relevant evidence** — paths, session ids, artifacts, or validation output that motivate a material change.
2. **Normalize or stage** — keep provenance; use [Prepared Context Layer](../prepared-context-layer.md) when structuring for operators or tools.
3. **Classify affected scopes** — map to `primaryScope` / `secondaryScopes` ([change-types.md](../change-types.md)).
4. **Draft a Change Proposal v1** — JSON under `users/<id>/review-queue/proposals/` ([state-proposals.md](../state-proposals.md)).
5. **Validate** — `python3 scripts/validate-change-review.py users/<id>/review-queue`.
6. **Route into review** — queue index, event log, lifecycle ([change-review-lifecycle.md](../change-review-lifecycle.md)).

---

## Rule

No materially important governed change should skip the **proposal** stage. Tools may assist drafting; **validate-change-review.py** is the mechanical check.

---

## Related

- [evidence-to-context-pipeline.md](../evidence-to-context-pipeline.md) — full layer flow (collect → … → route material changes)
- [change-review-lifecycle.md](../change-review-lifecycle.md) — detect → propose → classify → …
- [proposal-to-review.md](proposal-to-review.md) — next step
- `scripts/generate-change-proposal.py` — starter JSON (replace placeholder refs before merge)

---

Companion-Self template · Pipeline stage
