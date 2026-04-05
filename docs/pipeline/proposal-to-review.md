# Proposal to review

Companion-Self template · From valid proposal JSON to explicit review

---

## Purpose

Move a **schema-valid** Change Proposal v1 into an explicit **review** state: classification, checks, and operator-visible narrative before any merge.

---

## Review checks

Use instance policy; at minimum consider:

- **Evidence sufficiency** — do `supportingEvidence` entries justify `materiality` and `changeType`?
- **Contradiction classification** — align with [contradiction-policy.md](../contradiction-policy.md).
- **Surface targeting** — do `targetSurface` / `canonicalPath` match the scopes (`primaryScope`, `secondaryScopes`)?
- **Confidence** — optional `confidenceDelta` when numeric bands are in use.
- **Scope** — routine vs boundary vs policy ([change-review.md](../change-review.md)).
- **Authority fit** — gate vs queue ([gate-vs-change-review.md](../gate-vs-change-review.md)).

---

## Outcomes

- Accepted path → decision record and merge per instance doctrine (`approved`)
- Rejected (`rejected`)
- Deferred (`deferred`)
- Revised → new or updated proposal (`superseded` on prior item when applicable)

Statuses are defined on Change Proposal v1; see [state-proposals.md](../state-proposals.md).

---

## Related

- [change-review-lifecycle.md](../change-review-lifecycle.md) — classify, render diff, review, decide
- [evidence-to-context-pipeline.md](../evidence-to-context-pipeline.md) — layer context
- [review-to-merge.md](review-to-merge.md) — next step
- `scripts/render-change-proposal-summary.py` — human-readable summary (not a full identity diff)

---

Companion-Self template · Pipeline stage
