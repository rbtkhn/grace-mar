# Action receipts

Companion-Self template · Optional audit stubs for meaningful operations

---

## Purpose

**Action receipts** are small JSON records (or equivalent logs) that make a **meaningful** system action **inspectable** after the fact. They complement:

- **Observability reports** — aggregates over proposals and validators ([observability.md](observability.md))
- **Change Proposal v1** — structured post-seed change intent ([state-proposals.md](state-proposals.md))
- **Gate merge receipts / pipeline audit** — proof of **approved** merges and pipeline events ([schema-record-api.md](schema-record-api.md), [CONTRADICTION-ENGINE-SPEC.md](CONTRADICTION-ENGINE-SPEC.md))

Action receipts are **not** the Record. They are **not** a second merge path. They do **not** substitute for companion approval or instance merge scripts.

---

## Examples (when to record)

- Generated a Change Proposal v1 file
- Ran seed-phase or change-review validation with a notable outcome
- Staged evidence or prepared-context artifacts for review
- Emitted a bridge or harvest packet (ephemeral; still legible)
- Applied an **accepted** change (often **also** recorded elsewhere; receipt is redundant only if those surfaces are complete)

### Specialized evaluation receipts

**Load-Lift Receipts** are a **specialized** evaluation artifact for [known-path workflow](workflows/known-path-workflows/README.md) **runs** — they record whether a workflow **reduced operator burden** (baseline vs run vs review time) while flagging **missed signals**, **false promotion risk**, and **authority** concerns. They **do not** replace general action-receipt use cases, **do not** merge or approve the Record, and **do not** subsume a future `schema-registry/action-receipt.v1.json` (see *Shape* below). Schema: [schema-registry/load-lift-receipt.v1.json](../schema-registry/load-lift-receipt.v1.json); spec: [load-lift-receipts.md](workflows/known-path-workflows/load-lift-receipts.md).

---

## Shape (future)

When an instance or tool needs a machine schema, prefer **`schema-registry/action-receipt.v1.json`** with **camelCase** fields (`receiptId`, `createdAt`, `appliedStatus`, …), aligned with other v1 artifacts. Until then, use this doc as doctrine only.

---

## Instances

Instances may log receipts under `users/<id>/`, JSONL streams, or operator folders. The template does not require a single path until emitters exist.

---

Companion-Self template · Action receipts v1
