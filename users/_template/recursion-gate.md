# recursion-gate — At the Gate (Template)

**Template only. No real data.** Copy this structure when creating a new user directory in an instance repo. The pipeline stages candidates **at the gate**; only the companion (or delegated human) may merge approved items into self, self-evidence, and the dimension files.

Governed by Identity Fork Protocol: agent may stage, may not merge. The gate is where the **recursive** loop turns—proposed changes wait here until the companion approves; then they enter the Record and the system improves. Hence *recursion-gate*.

**Operator routing:** [docs/recursion-gate-three-tier.md](../../docs/recursion-gate-three-tier.md) — fast vs normal vs escalated review, change-review export, work-politics batch scope vs tier depth.

**Comprehension Envelope:** [docs/governance/comprehension-envelope-gate.md](../../docs/governance/comprehension-envelope-gate.md) — optional **`impact_tier`** and **`envelope_class`** on each candidate; orthogonal to traffic **`risk_tier`**. Optional check: `python3 scripts/validate_gate_comprehension_envelope.py -u <user_id>`.

---

## Candidate classification (optional YAML keys)

On each `### CANDIDATE-…` block, you may add:

| Field | Values |
|-------|--------|
| **`impact_tier`** | `low` \| `medium` \| `high` \| `boundary` |
| **`envelope_class`** | `none` \| `optional` \| `required` |

**Pairing:** `low` → `none`; `medium` → `optional`; `high` or `boundary` → `required`. Do **not** put blast-radius labels on **`risk_tier`** — that name is reserved for traffic tiers (`quick_merge_eligible` / `review_batch` / `manual_escalate`).

**Authority map (advisory):** If the change maps to a [surface key](../../docs/authority-map.md), run `python3 scripts/check-authority.py --surface <key> --json` for recommended `impact_tier` / `envelope_class` from write policy (companion may override).

### Comprehension Envelope (when not `none`)

Place **below** the YAML fence, same candidate section:

```markdown
### Comprehension Envelope
- What this is:
- Why this path:
- Why not the next-best option:
- Blast radius:
- Assumptions / fragile points:
- Human override applied:
```

---

## Reflection Gates (v1)

Process labels at **promotion** time only (orthogonal to traffic **`risk_tier`** — see [recursion-gate-three-tier.md](../../docs/recursion-gate-three-tier.md)).

- **`impact_tier: low`** or unset — no Reflection Gate; fast path.
- **`impact_tier: medium`** — **Light Gate**: envelope recommended (`envelope_class: optional`); advisory only in v1.
- **`impact_tier: high`** or **`boundary`** — **Heavy Gate**: `envelope_class: required`; fill **Blast radius** and **Human override applied** in the Comprehension Envelope; optional `reflection_ack: heavy` after explicit read.

**Dynamic Gate** deferred. Validator: `python3 scripts/validate_gate_comprehension_envelope.py -u <user_id>`.

---

## Candidates

(Each pending candidate lives **above** `## Processed`. Bot and scripts insert new blocks immediately before `## Processed`.)

---

## Processed

*(Approved / merged / rejected history — per instance.)*

---

*Copy to `users/<new_id>/recursion-gate.md` in an instance. Do not use this template file as a live staging area.*
