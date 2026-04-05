# Source of truth

Companion-Self template · Precedence across layers and review objects

---

## Purpose

Companion-Self should not rely on ambiguous “whatever the agent said last” as truth. Operators need a **declared precedence** among evidence, prepared context, governed state, and **accepted change-review outcomes**.

This doc aligns with the three-layer model in [state-model.md](state-model.md): [Evidence Layer](evidence-layer.md), [Prepared Context Layer](prepared-context-layer.md), [Governed State Layer](governed-state-layer.md).

---

## Default precedence (high to low)

1. **Governed state** — durable Record commitments and approved governed files (instance-specific; see [governed-state-layer.md](governed-state-layer.md)).
2. **Accepted change-review objects** — proposals that reached an explicit **approved** decision and any linked decision records / diffs in `review-queue/` that the instance treats as binding for a transition. This is **audit and transition** state, not a fifth parallel truth: it exists to move governed state under policy.
3. **Prepared context** — operationally useful structured inputs for tools and agents; **not** authoritative over governed state.
4. **Evidence** — source material; may be incomplete, noisy, or mutually conflicting.

**Important:** More recent evidence does **not** automatically outrank governed state. If the gap is **material**, open a [state proposal](state-proposals.md) and route through [change review](change-review.md).

---

## Machine-readable default

Optional file: [`config/source-of-truth.json`](../config/source-of-truth.json) (schema [`schema-registry/source-of-truth.v1.json`](../schema-registry/source-of-truth.v1.json)). Starter check: `scripts/check-source-conflict.py`.

---

## Relationship to the live Record

The **Record** in an instance remains the primary durable surface for identity and knowledge the companion approved. Change-review artifacts **surround** merges; they do not replace instance merge doctrine. See [change-review.md](change-review.md) (Relationship to the live Record).

---

## Related

- [conflict-resolution-order.md](conflict-resolution-order.md) — what to do when sources disagree
- [contradiction-policy.md](contradiction-policy.md) — classification during review
- [change-review-lifecycle.md](change-review-lifecycle.md) — proposal → decision → merge

---

Companion-Self template · Source of truth v1
