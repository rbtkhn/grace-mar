# Review to merge

Companion-Self template · From decision to governed state update

---

## Purpose

Control the transition from a **reviewed** proposal to an update of **governed state** (Record and related durable surfaces).

---

## Requirements

- **Explicit decision** — decision record and/or proposal `status` aligned with instance rules.
- **Preserved prior state or diff** — history remains inspectable ([`schema-registry/identity-diff.v1.json`](../../schema-registry/identity-diff.v1.json) when used; `scripts/generate-identity-diff.py` for Markdown views).
- **Durable trace** — why the change happened (queue summary, notes, event log).
- **Merge path limited to authorized surfaces** — no cross-surface silent edits outside policy.

---

## Rule

**Acceptance is not silent overwrite.** A merge should preserve enough trace to explain what changed and why. Instance merge scripts and gate doctrine remain authoritative for *how* merge runs.

---

## Related

- [change-review-lifecycle.md](../change-review-lifecycle.md) — merge or preserve, log
- [governed-state-layer.md](../governed-state-layer.md) — what counts as governed
- [source-of-truth.md](../source-of-truth.md) — precedence when layers disagree
- [conflict-resolution-order.md](../conflict-resolution-order.md) — when to open a proposal instead of picking a winner

---

Companion-Self template · Pipeline stage
