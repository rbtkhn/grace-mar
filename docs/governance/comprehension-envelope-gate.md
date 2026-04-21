# Comprehension Envelope at the gate (vocabulary)

**Purpose:** Define **`envelope_class`** (comprehension requirement) separately from **traffic / review `risk_tier`**. Prevents confusion with [recursion-gate-three-tier.md](../recursion-gate-three-tier.md) (fast vs normal vs escalation) and [scripts/recursion_gate_review.py](../../scripts/recursion_gate_review.py) machine values.

**Status:** Governance vocabulary — WORK layer; not Record truth.

---

## Three orthogonal axes (do not merge)

| System | Field name | Where documented | Meaning |
|--------|------------|------------------|---------|
| **Traffic / merge UX** | **`risk_tier`** (machine) | [recursion-gate-three-tier.md](../recursion-gate-three-tier.md), [recursion_gate_review.py](../../scripts/recursion_gate_review.py) | `quick_merge_eligible`, `review_batch`, `manual_escalate` — how fast or heavy **review** is. |
| **Blast radius / promotion sensitivity** | **`impact_tier`** (author) | This doc; [users/…/recursion-gate.md](../../users/grace-mar/recursion-gate.md) § Candidate classification | `low`, `medium`, `high`, `boundary` — how sensitive the **content** of the merge is (canonical surfaces, governance, etc.). **Not** a rename of `risk_tier`. |
| **Comprehension proof** | **`envelope_class`** | This doc | `none`, `optional`, `required` — whether a **Comprehension Envelope** markdown block is omitted, recommended, or required. |

**Orthogonality:** Traffic `risk_tier` describes **review flow** (dashboards, quick-merge eligibility). **`impact_tier`** and **`envelope_class`** describe **what the companion must see** before approval. A candidate can be `review_batch` (traffic) and `envelope_class: required` (comprehension), or `quick_merge_eligible` with `envelope_class: none`.

**Typical pairing (rollout):** `impact_tier: low` → `envelope_class: none`; `medium` → `optional`; `high` or `boundary` → `required`. Adjust in YAML when a case is exceptional.

---

## Authority map integration

Surface keys in [`config/authority-map.json`](../../config/authority-map.json) resolve to an **authority class** (write policy). Recommended **`impact_tier`**, **`envelope_class`**, and Reflection Gate label for staging are **derived** from that class in one place: [`scripts/authority_comprehension_defaults.py`](../../scripts/authority_comprehension_defaults.py). Run `python3 scripts/check-authority.py --surface <key> --json` to see recommendations for a named surface. Full table: [docs/authority-map.md](../authority-map.md) § Relationship to Comprehension Envelope and Reflection Gates.

---

## Gate wiring (operational surface)

The first place these fields appear in day-to-day use is **`users/<id>/recursion-gate.md`** (markdown-first; YAML keys inside each `### CANDIDATE-…` fenced block).

- **`impact_tier`** and **`envelope_class`** are optional on any candidate; when present, reviewers and tooling can rely on them.
- **Do not** overload **`risk_tier`** in YAML to mean `low`/`medium`/`high` — that collides with machine traffic tiers. Use **`impact_tier`** for that ladder.
- **Rollout:** start with documentation + examples; optional **`python3 scripts/validate_gate_comprehension_envelope.py`** (presence + Reflection Gate advisory warnings). Observability-driven **Dynamic Gate** and stronger enforcement remain **follow-on**.

---

## Reflection Gates integration (v1)

**Reflection Gates** are the **process layer** that scales reviewer attention using **`impact_tier`** and **`envelope_class`** — without reusing traffic **`risk_tier`**. They apply only at the **promotion boundary** (companion review before approve).

| Label | `impact_tier` | Role in v1 |
|-------|----------------|------------|
| *(none)* | `low` or unset | No extra gate label; fast path |
| **Light Gate** | `medium` | Comprehension Envelope **recommended** (`envelope_class: optional`); advisory only |
| **Heavy Gate** | `high` or `boundary` | Envelope **required**; **Blast radius** and **Human override applied** bullets must be filled honestly; advisory-first validator warnings |

**Initial rollout:** advisory-first. **Dynamic Gate** (observability escalation) is **deferred**. Live copy: [users/grace-mar/recursion-gate.md](../../users/grace-mar/recursion-gate.md) § Reflection Gates (v1).

---

## `envelope_class` values

| Value | Meaning |
|-------|---------|
| **`none`** | No Comprehension Envelope required (trivial / local / runtime-only staging that still passes through gate policy). |
| **`optional`** | Envelope recommended for reviewer clarity; not blocking in v1 automation. |
| **`required`** | Non-empty `### Comprehension Envelope` block must be present before companion treats the candidate as ready to approve (per operator process; automation optional). |

**Naming:** Prefer **`envelope_class`** in docs and future YAML; avoid unqualified “Tier 0/1/2” for comprehension — that collides with gate traffic language.

---

## When `required` is appropriate (triggers — refine with companion)

Use **`required`** when the change is high-impact, including examples such as:

- Targets **canonical** surfaces: `self.md`, `self-archive.md`, `bot/prompt.py`, or gated profile dimensions.
- Touches **schemas** or repo validation rules (`schema-registry/`, CI validators).
- Alters **governance or boundary** behavior (authority map, abstention, gate protocol).
- **Promotes** strategy-notebook material to durable promoted arcs (e.g. [STRATEGY.md](../skill-work/work-strategy/STRATEGY.md)) — tie to explicit operator tags or paths in the candidate.
- Produces **export / handoff** artifacts intended for downstream operators or forks.

**Not** for: routine IX-A/B/C lines that already satisfy `ready_for_quick_merge` unless companion policy says otherwise.

---

## Comprehension Envelope block (canonical shape)

See [comprehension-envelope-insights-to-implementation.md](comprehension-envelope-insights-to-implementation.md) § Phase 2 for the markdown template and authoring rules.

---

## Relation to change proposals

[change-proposal.v1.json](../../schema-registry/change-proposal.v1.json) already includes `riskLevel`, `queueSummary`, `materiality`. The Comprehension Envelope is **operator proof of understanding**, not a duplicate summary. If mirrored into JSON in a later PR, fields must **complement** `queueSummary`, not replace it.

---

## See also

- [comprehension-envelope-insights-to-implementation.md](comprehension-envelope-insights-to-implementation.md) — full insight table and PR sequence
- [gate-vs-change-review.md](../gate-vs-change-review.md)
- [AGENTS.md](../../AGENTS.md)
