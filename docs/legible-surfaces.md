# Legible surfaces

Companion-Self template · Meaningful actions should leave a trace

---

## What “legible” means

A **legible** operation answers, without asking the agent:

- **What happened?** (action type, rough outcome)
- **Which surfaces or paths were involved?** (files, layers, review objects)
- **Was this only proposed, or actually applied?** (staged vs merged)
- **What evidence supported it?** (refs, not vibes)
- **Where does the durable result live?** (governed path, or “none” if ephemeral)

Legibility is a **governance and usability** feature, not only debugging.

---

## Relationship to other audit artifacts

- **Gate / merge receipts** (e.g. merge-receipt lines, instance pipeline logs) prove **approved merges** into the Record. See [schema-record-api.md](schema-record-api.md) and instance IFP docs.
- **Pipeline or harness events** (e.g. `pipeline-events.jsonl` where instances use them) support **operational** audit.
- **Action receipts** ([action-receipts.md](action-receipts.md)) are an **optional, lightweight** pattern for operator-visible traces of meaningful steps (validation runs, proposal generation, staging). They **do not replace** governed state or merge receipts.

---

## Rule

Not every tiny operation needs a receipt. **Meaningful** operations that affect understanding, governance, review, or durable state **should** be reconstructable from data the operator can inspect ([observability.md](observability.md)).

---

Companion-Self template · Legible surfaces v1
