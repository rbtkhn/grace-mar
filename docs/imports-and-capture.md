# Imports and capture

**Purpose:** Clarify the **safety boundary** between bringing material *into* the repo and promoting it *into* the durable **Record**.

> Grace-Mar is not just a memory layer; it is a **governed companion record**. Imports and bridges **feed evidence and prepared context first**; **Approval Inbox** (`recursion-gate.md`) sits before merges into SELF, SKILLS, EVIDENCE, and prompt.

---

## What is true

1. **Ingestion is normal** — bridges, hooks, operator paste, bot conversations — see [openclaw-integration.md](openclaw-integration.md), [feedback-loops.md](feedback-loops.md).
2. **Imports do not auto-write the durable Record** — material may land in **EVIDENCE**, transcripts, prepared context, or staging files without yet being “canonical identity.”
3. **Promotion is gated** — structured **candidates** in [`users/grace-mar/recursion-gate.md`](../users/grace-mar/recursion-gate.md) (**Approval Inbox**); companion approval; `process_approved_candidates.py` performs the merge ([AGENTS.md](../AGENTS.md)).

---

## Typical path

```text
External material → evidence / prepared context / staging → candidates (Approval Inbox) → approve → Record + EVIDENCE + prompt (as applicable)
```

Cross-surface or high-materiality changes may use **change-review** instead of a routine gate row ([gate-vs-change-review.md](gate-vs-change-review.md)).

---

## Related docs

- [state-model.md](state-model.md) — three layers vs four Record surfaces
- [pipeline/](pipeline/) — evidence → proposal → review → merge
- [skills-explained.md](skills-explained.md) — portable skills vs SKILLS capability
- [start-here-ob1-users.md](start-here-ob1-users.md) — OB1-oriented map
