# Boundary Review Queue

**Purpose:** Make **classification and review at the Record boundary** a first-class product surface — not just storage. **Governed by:** gated pipeline, [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md), [identity-fork-protocol.md](identity-fork-protocol.md) `proposal_class`.

**Not a replacement for the gate:** **`recursion-gate.md`** remains the **default staging surface** for routine candidates (IX-A/B/C lines, analyst output). The **boundary review** story is about **where a staged line belongs** (SELF vs SELF-LIBRARY vs CIV-MEM, etc.) and **when** to escalate to **material change-review** — not about deleting or bypassing the gate. For the split between gate workflow and change-review queue, see [gate-vs-change-review.md](gate-vs-change-review.md) and IFP §4.3 (material change escalation).

---

## Problem

As the fork grows, the main risk is **right data, wrong surface** (identity vs library vs civ-mem vs skills vs work). The architecture already splits SELF, SELF-LIBRARY, SKILLS, EVIDENCE, and work territories; the scaling bottleneck is **review at the boundary**, not another memory channel.

---

## Proposal classes → surfaces

| Review bucket | Typical `proposal_class` | Canonical home |
|---------------|--------------------------|------------------|
| **SELF-KNOWLEDGE** | `SELF_KNOWLEDGE_ADD` / `REVISE` | `self.md` IX-A/B/C |
| **SELF-LIBRARY** | `SELF_LIBRARY_ADD` / `REVISE` | `self-library.md` |
| **CIV-MEM** | `CIV_MEM_ADD` / `REVISE` | LIB rows + civ-mem corpus |
| **SKILLS** | (future explicit class or evidence-linked) | `self-skills.md`, skill-think/write |
| **WORK-LAYER** | Work-politics / operator work artifacts | `work-*.md`, territories |

---

## Minimal product (phased)

### Phase A (current / shipped incrementally)

- **Automatic proposal classification** — `proposal_class` on gate YAML + inferred default from `mind_category`.
- **Boundary hints** — `recursion_gate_review.parse_review_candidates` attaches **`boundary_review`**: target surface, suggested surface, optional **misfiled?** string, short **why**.
- **Review panel** — Approval Inbox shows boundary hint; approve / reject / defer unchanged; **reclassify** = edit gate YAML (`proposal_class`) + reload (manual until Phase B).

### Phase B

- Structured diff: **old location → proposed location** (when moving between surfaces).
- **Confidence** score in API.
- **Reclassify** action writes `proposal_class` (or moves block to a sibling queue section) via authenticated API.

### Phase C

- **Audit trail** — append `boundary_review_hint` / `boundary_misfiled_overridden` to `pipeline-events.jsonl` when operator approves despite warning or changes class; use to tune analyst prompt and `validate_identity_library_boundary` rules.

---

## Evidence and trust

Every item keeps **evidence links** (`evidence_id`, `intake_evidence_id`, ACT-*) as today. Boundary queue **does not merge** — it **explains and warns** until the companion approves. Same sovereign rule: **no merge without approval**.

---

## Escalation rule

1. **Routine:** Candidate stays in **`recursion-gate.md`**; companion approves or rejects; merge via `process_approved_candidates.py` (or equivalent).
2. **Boundary ambiguity:** Use **`proposal_class`**, **boundary hints** (`recursion_gate_review`), and the Approval Inbox to **reclassify** before merge.
3. **Material change** (contradiction, cross-surface move needing audit, policy/prompt shift): **Escalate** to **`users/<id>/review-queue/`** — structured proposals, decisions, diffs — per companion-self [change-review](https://github.com/rbtkhn/companion-self/blob/main/docs/change-review.md) semantics. Optional bridge: `python3 scripts/export_gate_to_review_queue.py --user <id> --candidate-id <id>`.

Escalation **does not** auto-merge; it adds **process** before governed state changes. See [identity-fork-protocol.md](identity-fork-protocol.md) §4.3.

---

## Related

- [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md) — ontology.
- [harness-replay-spec.md](harness-replay-spec.md) — causal replay (why the system routed here); complements boundary queue (where things should go).
- [operator-weekly-review.md](operator-weekly-review.md) — rhythm.
- `scripts/recursion_gate_review.py` — `boundary_review` on each candidate row.
- `miniapp/operator-inbox.html` — displays boundary warnings.
