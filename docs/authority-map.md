# Authority map

Companion-Self template · Who may change what

---

## Why this exists

Not every surface should be writable by the same runtime. The template distinguishes **read-only**, **draftable**, **review-required**, **human-only**, and **ephemeral-only** behavior so operators and agents do not silently widen write authority “because it was faster.”

Machine-readable defaults: [`config/authority-map.json`](../config/authority-map.json) (schema [`schema-registry/authority-map.v1.json`](../schema-registry/authority-map.v1.json)). Lookup helper: `scripts/check-authority.py --surface <key>`.

---

## Authority classes (normative)

| Class | Meaning |
|--------|---------|
| **read_only** | Inspect only; no writes, no merge. |
| **draftable** | May create drafts, summaries, prepared context, staging artifacts, or non-governed tooling output. |
| **review_required** | May prepare materially important change objects (e.g. Change Proposal v1); **not** apply to governed state without explicit review and instance merge path. |
| **human_only** | Final judgment and authoritative writes belong to the human operator (or instance policy they delegate). |
| **ephemeral_only** | Operational outputs only; must not be treated as durable companion state. |

---

## Surface keys in `config/authority-map.json`

The config file uses a **single flat map** for simplicity. Keys mix **different dimensions** on purpose; interpret each key with the dimension below.

### State layers (evidence → governed)

- **`evidence`** — Evidence layer inputs (see [evidence-layer.md](evidence-layer.md)).
- **`prepared_context`** — Prepared context layer (see [prepared-context-layer.md](prepared-context-layer.md)).
- **`governed_state`** — Durable Record and governed files (see [governed-state-layer.md](governed-state-layer.md)).

### Formation and review artifacts

- **`seed_phase_artifacts`** — Pre-activation JSON under `users/<id>/seed-phase/`; changes affect activation readiness.

### Change scopes (align with [change-types.md](change-types.md) / `primaryScope`)

- **`identity`**, **`curiosity`**, **`pedagogy`**, **`expression`**, **`memory_governance`**, **`safety`** — durable commitment areas; high-trust zones may be `human_only` or `review_required` per config.

### Operator cadence packets (non-Record)

- **`bridge_packets`**, **`harvest_packets`** — Session handoff / harvest artifacts under skill-work cadence docs; **ephemeral_only** in the default map (see [work-cadence README](skill-work/work-cadence/README.md)).

**Rule:** Automation should not treat every key as the same kind of “surface.” Use this section when wiring tools.

---

## Relationship to change review

Transition into governed state must respect the authority map and the gated pipeline ([change-review.md](change-review.md), [change-review-lifecycle.md](change-review-lifecycle.md)). Proposal generation and review routing should be **authority-aware**: draftable and review_required are not merge authority.

---

## Related

- [template-instance-contract.md](template-instance-contract.md) — instance may extend tooling but should not silently widen agent writes
- [source-of-truth.md](source-of-truth.md) — precedence when layers disagree

---

Companion-Self template · Authority map v1
