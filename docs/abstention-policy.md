# Abstention and fabricated-history policy (runtime and pre-gate)

This document is **normative** for Grace-Mar’s **uncertainty envelope** ([`schema-registry/uncertainty-envelope.v1.json`](../schema-registry/uncertainty-envelope.v1.json)) and the scripts under [`scripts/runtime/`](../scripts/runtime/) that derive it. It **does not** change companion merge authority over the Record ([`AGENTS.md`](../AGENTS.md)).

## Principles

1. **Runtime memory is assistance, not truth.** Observations in the runtime ledger, prepared context, and memory briefs are **operator scaffolding**. They are **not** SELF, SELF-LIBRARY, SKILLS, or EVIDENCE until merged through the gated pipeline with companion approval.

2. **Weakly supported claims** should be labeled **partial**, **insufficient**, or **hold** at promotion time—not polished as if they were proven.

3. **Contradicted material** must not be promoted to the Record **without explicit review**, even when phrasing sounds confident.

4. **Candidate staging** may be **downgraded or blocked** when the envelope says so; any **block** from tooling is **advisory** unless the operator enables a strict hook. **Companion approval** remains the only path to merge into `self.md` / EVIDENCE / `bot/prompt.py`.

5. **Fabricated-history risk** is **screening language**, not an accusation of malice. It flags patterns where text looks like **durable biographical or historical narrative** without evidence references—especially when combined with **record mutation** intent.

## Relation to existing doctrine

- **[`AGENTS.md`](../AGENTS.md) — Knowledge boundary:** The envelope makes **epistemic status** visible; it does not replace abstention in the Voice or LLM layer.
- **[`docs/prepared-context-doctrine.md`](prepared-context-doctrine.md):** Prepared context is optimized for reasoning and **must not** be mistaken for the Record. The uncertainty section makes that **explicit per bundle**.
- **[`docs/runtime/read-hints.md`](runtime/read-hints.md)** and runtime tooling docs: Higher-level tools remain **scaffolding**; the ledger does not auto-stage into `users/<id>/recursion-gate.md`.

## Distinction from seed-phase confidence

- **[`schema-registry/seed-confidence-map.v1.json`](../schema-registry/seed-confidence-map.v1.json)** applies to **seed-phase** / survey-style maps. **Do not** conflate those numeric bands with **runtime `evidence_state`** or **`fabricated_history_risk`**.

## Envelope fields (summary)

| Field | Meaning |
|--------|---------|
| `evidence_state` | `sufficient` \| `partial` \| `insufficient` \| `conflicted` |
| `fabricated_history_risk` | `low` \| `medium` \| `high` (orthogonal to evidence_state) |
| `promotion_recommendation` | `allow` \| `allow_with_review` \| `hold` \| `block` |

**Derivation:** Values are computed **only** from [`schema-registry/runtime-observation.v1.json`](../schema-registry/runtime-observation.v1.json) fields on selected observations (and optional synthetic precheck text)—see [`scripts/runtime/uncertainty_envelope.py`](../scripts/runtime/uncertainty_envelope.py). There is **one pipeline**; scores are not hand-edited in parallel.

## First-pass promotion rules

| Condition | Recommendation |
|-----------|----------------|
| `sufficient` + `fabricated_history_risk: low` | `allow` |
| `partial` + `low` or `medium` | `allow_with_review` |
| `insufficient` | `hold` |
| `conflicted` **or** `fabricated_history_risk: high` | `block` (advisory; operator may override with documented rationale) |

## Gate staging precheck

- [`scripts/runtime/precheck_gate_staging.py`](../scripts/runtime/precheck_gate_staging.py) prints the envelope and **stderr** guidance when `block` is recommended.
- **Default:** exit **0** (advisory). **`--strict`** exits **1** on `block` for CI or local gates; **`--force-override`** exits **0** when the operator acknowledges override.
- [`integrations/openclaw_stage.py`](../integrations/openclaw_stage.py) may append an **ABSTENTION_PRECHECK** line when `--precheck` is set; staging **still proceeds** unless the operator configures otherwise.

## What this policy does *not* do

- Full probabilistic truth scoring or a giant safety framework.
- Blocking all low-confidence **work-layer** exploration.
- Turning runtime notes into **rigid compliance objects** without human judgment.

## See also

- [`scripts/runtime/score_evidence_sufficiency.py`](../scripts/runtime/score_evidence_sufficiency.py)
- [`scripts/runtime/flag_fabricated_history_risk.py`](../scripts/runtime/flag_fabricated_history_risk.py)
- [`scripts/runtime/memory_brief.py`](../scripts/runtime/memory_brief.py) (optional envelope footer)
- [`scripts/prepared_context/build_context_from_observations.py`](../scripts/prepared_context/build_context_from_observations.py) (uncertainty section)
