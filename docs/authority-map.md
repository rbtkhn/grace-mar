# Authority map

Companion-Self template · Who may change what

---

## Why this exists

Not every surface should be writable by the same runtime. The template distinguishes **read-only**, **draftable**, **review-required**, **human-only**, and **ephemeral-only** behavior so operators and agents do not silently widen write authority “because it was faster.”

Machine-readable defaults: [`config/authority-map.json`](../config/authority-map.json) (schema [`schema-registry/authority-map.v1.json`](../schema-registry/authority-map.v1.json)). Lookup helper: `scripts/check-authority.py --surface <key>` (authority class only). Structured recommendations: `python3 scripts/check-authority.py --surface <key> --json` (includes Comprehension Envelope + Reflection Gate hints; see below).

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

## Relationship to Comprehension Envelope and Reflection Gates

Write **authority class** (per surface key) is the **policy** layer: who may change what. **Comprehension Envelope** and **Reflection Gates** (see [governance/comprehension-envelope-gate.md](governance/comprehension-envelope-gate.md) and [users/grace-mar/recursion-gate.md](users/grace-mar/recursion-gate.md)) are the **staging** layer: how much deliberate review and proof accompany a candidate before promotion.

**Single derivation (SSOT in code):** [`scripts/authority_comprehension_defaults.py`](../scripts/authority_comprehension_defaults.py) maps each **authority class** to recommended **`impact_tier`**, **`envelope_class`**, and **`recommended_reflection_gate`** (aligned with `none` \| `optional` \| `required` and Light/Heavy gate labels). **Companion may override** these in candidate YAML when context demands it.

| Authority class | Typical recommended `impact_tier` | `envelope_class` | Reflection Gate label |
|-----------------|-----------------------------------|------------------|-------------------------|
| **human_only** | `boundary` | `required` | Heavy |
| **review_required** | `medium` | `optional` | Light |
| **draftable** | `low` | `none` | *(none)* |
| **read_only** | `low` | `none` | *(none)* |
| **ephemeral_only** | `low` | `none` | *(none)* |

**Lookup:** `python3 scripts/check-authority.py --surface <key> --json` prints `authority_class` plus the recommended fields and a short rationale. This does **not** change merge authority or automate merges; it advises staging only.

---

## Related

- [template-instance-contract.md](template-instance-contract.md) — instance may extend tooling but should not silently widen agent writes
- [source-of-truth.md](source-of-truth.md) — precedence when layers disagree

---

Companion-Self template · Authority map v1
