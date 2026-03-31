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

### Phase A — shipped

- **Automatic proposal classification** — `proposal_class` on gate YAML + inferred default from `mind_category`.
- **Boundary hints** — `recursion_gate_review.parse_review_candidates` attaches **`boundary_review`**: target surface, suggested surface, optional **misfiled?** string, short **why**.
- **Review panel** — Gate review app + Approval Inbox show boundary context; approve / reject / defer / minimal reclassify on pending candidates.

### Phase B1 — shipped (canonical review object)

- **JSON Schemas** — `change-proposal`, `change-decision`, and `change-review-queue` carry target surface, materiality, review type, reclassification hints, and expanded decision enums (`reclassified`, `split`, `deferred`, etc.).
- **Normalization** — `scripts/gate_review_normalize.py` maps each gate row to a unified review shape for UI and API (`items_normalized` on `/api/candidates`).
- **Gate-review app** — Pills for proposal class, surface, materiality, review type; `/action` supports **defer** and **reclassify** (maps target surface → allowed `proposal_class`).

### Phase B2 — partially shipped

- **Persisted boundary classification** — each pending candidate may have `users/<id>/review-queue/boundary-classifications/CANDIDATE-*.json` (`schema-registry/boundary-classification.v1.json`), refreshed when `parse_review_candidates` runs. Classifier logic lives in `src/grace_mar/merge/boundary_classifier.py`.
- **API** — `items_normalized` from `/api/candidates` includes `boundary_confidence`, `boundary_confidence_score`, `boundary_misfiled_warning`, `boundary_hint_reasons`, and `suggested_reclassify_proposal_class` (one-click target class).
- **Gate-review app** — cards show the same boundary hint block as the Approval Inbox (target → suggested, misfiled text, reasons) plus **Apply suggested class** when the suggested `proposal_class` differs from the current row.
- **Reclassify audit** — `gate_reclassified` pipeline events include `boundary_classification_rel_path` pointing at the on-disk artifact path.

Still **next** (seam with PR2 / later):

- Structured diff: **old location → proposed location** (when moving between surfaces).
- **Full reclassify UX** — richer forms, optional queue export bridge without manual YAML.

### Phase C

- **Audit trail (extended)** — optional additional event types (`boundary_review_hint` / `boundary_misfiled_overridden`) or richer payloads on approve-with-warning; today reclassify is covered by `gate_reclassified` + classification file. Use to tune analyst prompt and `validate_identity_library_boundary` rules.

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
