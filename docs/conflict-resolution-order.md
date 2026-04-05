# Conflict resolution order

Companion-Self template · When sources disagree

---

## Purpose

When **evidence**, **prepared context**, and **governed state** (or two proposals) disagree, Companion-Self should not silently pick a winner. This document gives a **deterministic order of operations** for humans and tools.

Use it together with [source-of-truth.md](source-of-truth.md) and [contradiction-policy.md](contradiction-policy.md).

---

## Order

1. **Governed touch?** Determine whether the disagreement affects **governed state** (durable Record or equivalent) or only operational context.
2. **Materiality** — Is the disagreement **material** (would change behavior, safety, or identity-facing commitments) or incidental (wording, low-impact prefs)?
3. **If material** — create or update a **Change Proposal v1** ([state-proposals.md](state-proposals.md)) and route through [change review](change-review.md); do not overwrite governed files without that path.
4. **Contradiction type** — classify per [contradiction-policy.md](contradiction-policy.md) (direct contradiction, scope tension, etc.).
5. **Review** — explicit decision; then merge or preserve per [change-review-lifecycle.md](change-review-lifecycle.md).

---

## Contradiction classes (reminder)

Align detailed taxonomy with contradiction policy. At a high level:

- soft vs hard contradiction
- scope conflict
- source conflict
- timing conflict

Naming and blocking rules live in [contradiction-policy.md](contradiction-policy.md).

---

## Rules

- **Silence is not resolution.**
- **Unexplained overwrite is not resolution.**
- **Agent self-report is not resolution** — fix the data (proposal, evidence refs, validation) before relying on outcomes.

---

## Related

- [pipeline/review-to-merge.md](pipeline/review-to-merge.md) — merge discipline
- `scripts/check-source-conflict.py` — trivial precedence helper for layer tokens

---

Companion-Self template · Conflict resolution order v1
