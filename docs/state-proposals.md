# State proposals

Companion-Self template · Meaningful post-seed revision as a structured object

---

## What “state proposal” means here

In this template, a **state proposal** is the **human name** for a JSON document that validates against **Change Proposal v1**:

- **Schema:** [`schema-registry/change-proposal.v1.json`](../schema-registry/change-proposal.v1.json)
- **On disk:** one file per proposal under `users/<id>/review-queue/proposals/` (see [`users/_template/review-queue/README.md`](../users/_template/review-queue/README.md))
- **Validation:** `python3 scripts/validate-change-review.py users/<id>/review-queue`

It is **not** a separate schema or a parallel format. Do not invent a second proposal JSON shape.

---

## Why proposals exist

A state proposal makes durable change:

- **visible** — operators can inspect a file, not only chat or memory
- **reviewable** — lifecycle and contradiction policy apply
- **diffable** — prior vs proposed refs and identity diffs when used
- **attributable to evidence** — `supportingEvidence` carries typed refs and summaries
- **rejectable or deferrable** — `status` records outcome without silent overwrite

---

## Field mapping (informal → machine)

| Informal idea | Machine home in Change Proposal v1 |
|---------------|-------------------------------------|
| What areas are affected | `primaryScope` + optional `secondaryScopes` ([change-types.md](change-types.md)) |
| Kind of change | `changeType` (e.g. contradiction, refinement, expansion) |
| Short narrative / “why this matters” | `queueSummary`; extra detail in `notes` if needed |
| Where governed state lives | `targetSurface`, optional `canonicalPath` |
| Decision stage | `status` (`proposed`, `under_review`, `approved`, `deferred`, `rejected`, `superseded`) |
| Evidence pointers | `supportingEvidence[]` with `type`, `ref`, `summary` |

**Record surfaces vs change scopes:** `targetSurface` names **where** in the Record (e.g. `self`, `skills`). `primaryScope` names **what kind** of commitment is changing (e.g. `pedagogy`, `identity`). Both may be required on a proposal.

---

## What proposals are for

Use a state proposal when new evidence **materially** affects durable commitments such as:

- identity, curiosity, pedagogy, expression
- memory governance, safety, preference
- template or instance collisions (`upgrade_collision`)

---

## What proposals are not

- **Not** raw evidence — evidence belongs in the [Evidence Layer](evidence-layer.md); cite it from `supportingEvidence`
- **Not** prepared context — prepared context is operational input; cite paths if they inform the proposal
- **Not** automatic approval — `approved` requires an explicit review path and usually a [decision](change-review-lifecycle.md) record
- **Not** a silent mutation path — merge authority stays with the instance gate and merge doctrine

---

## Gate vs review queue

Routine, pipeline-sized updates often use the **recursion gate** and instance merge flow. **Material** post-seed revision that needs structured audit should use the **review queue** and a Change Proposal v1 file. See [gate-vs-change-review.md](gate-vs-change-review.md).

---

## Related

- [change-review.md](change-review.md) — doctrine entrypoint
- [change-review-lifecycle.md](change-review-lifecycle.md) — proposal → decision → merge
- [change-review-validation.md](change-review-validation.md) — validator commands
- [evidence-to-context-pipeline.md](evidence-to-context-pipeline.md) — layers before governed state

---

Companion-Self template · State proposals v1
