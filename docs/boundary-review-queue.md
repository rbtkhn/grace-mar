# Boundary Review Queue

**Purpose:** Make **classification and review at the Record boundary** a first-class product surface — not just storage. **Governed by:** gated pipeline, [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md), [identity-fork-protocol.md](identity-fork-protocol.md) `proposal_class`.

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
| **SKILLS** | (future explicit class or evidence-linked) | `skills.md`, skill-think/write |
| **WORK-LAYER** | WAP / operator work artifacts | `work-*.md`, territories |

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

## Related

- [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md) — ontology.
- [harness-replay-spec.md](harness-replay-spec.md) — causal replay (why the system routed here); complements boundary queue (where things should go).
- [operator-weekly-review.md](operator-weekly-review.md) — rhythm.
- `scripts/recursion_gate_review.py` — `boundary_review` on each candidate row.
- `miniapp/operator-inbox.html` — displays boundary warnings.
