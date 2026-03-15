# Pre-merge / pre-release condition checklist

**Purpose:** Condition-first deployment — beneficial outcomes (sovereign gate, evidence linkage, knowledge boundary) are conditions for merge or release, not hoped-for consequences. Use this checklist before merging Record changes or before a release that touches the gate, profile, or pipeline.

**Governance:** [Identity Fork Protocol](identity-fork-protocol.md); [AGENTS.md](../AGENTS.md). Aligned with [AI Ethics from the Condition](civilization-memory/essays/AI-ETHICS-FROM-THE-CONDITION.md) (condition-first deployment, no sacred footnote).

---

## Pre-merge (Record / profile / prompt)

Before merging any change into `users/[id]/self.md`, `users/[id]/self-evidence.md`, `users/[id]/self-archive.md`, `bot/prompt.py`, or PRP exports:

- [ ] **All Record changes came from RECURSION-GATE** — No direct merge to SELF, EVIDENCE, or prompt without staged candidates.
- [ ] **Companion (or delegated human) approved** — Merge authority is human-only; no autonomous merge.
- [ ] **Knowledge boundary respected** — No facts, references, or knowledge from LLM training or external sources merged without companion-provided content and approval.
- [ ] **Evidence linkage** — New SELF entries reference evidence (e.g. `evidence_id: ACT-XXXX`, `provenance: human_approved`).
- [ ] **File Update Protocol followed** — All affected files updated together (self.md, self-evidence.md, recursion-gate, session-log, prompt, pipeline-events, PRP if changed).

---

## Pre-release (gate, pipeline, or policy)

Before a release that changes pipeline behavior, gate logic, or policy surfaces:

- [ ] **Gate remains human-only** — No new path that merges without companion (or delegated human) approval.
- [ ] **Checklist above** — Any Record-affecting change in the release satisfies the pre-merge conditions.
- [ ] **Audit trail** — Pipeline events, merge receipts, or equivalent remain append-only and traceable.

---

*When in doubt: stage, don't merge. The agent may stage; it may not merge.*
