# Policy modes (governance envelopes)

A **policy mode** is a **named envelope** that answers, at a glance:

- How far retrieval should reach (posture, not a hard code path in every script yet).
- How candidate staging to the gate is constrained (`blocked`, `allowed`, `hold_by_default`, etc.).
- How strong abstention and promotion thresholds should be **before** companion review.
- Whether receipts stay visible for operator legibility.

Modes **tune** behavior **before** canonical review. They **do not** replace [source-of-truth order](source-of-truth.md), [authority mapping](authority-map.md), [runtime vs Record](runtime-vs-record.md), or the **approve → merge** pipeline in `AGENTS.md`. They are **not** a new truth surface.

## Why modes exist

The same repository may be used in different contexts (internal operator work, identity-sensitive edits, reference-only synthesis, youth-facing tutoring, high-stakes promotion decisions). **Declaring** the active mode makes assumptions **visible** on prepared context, review packets, checkpoints, and staging attempts — so behavior does not silently drift across contexts.

## Default and discovery

- **Default mode:** `operator_only` (normal internal operator use).
- **Environment:** `GRACE_MAR_POLICY_MODE` may be set to one of the keys in [`config/policy_modes/defaults.json`](../config/policy_modes/defaults.json).
- **CLI:** Scripts that support policy accept `--policy-mode NAME`; CLI overrides env for that invocation.

## First-wave modes (summary)

| Mode | Intent |
|------|--------|
| `operator_only` | Baseline: full lane retrieval posture, standard abstention, gate staging allowed. |
| `identity_bound` | SELF-facing and identity claims need stricter guardrails; staging allowed with **strict self** discipline (use `--policy-ack` when overriding warnings). |
| `reference_only` | Analysis / library-heavy work; **no** staging into SELF/SKILLS (automation **blocks** `stage_candidate_from_observations.py`). |
| `youth_facing` | Tutoring / pedagogical surfaces; staging **blocked** by automation; stricter abstention posture. |
| `high_risk_abstention` | Wrong memory or promotion is especially costly; envelope favors **hold** and surfaces uncertainty; staging requires `--policy-ack` when the mode would otherwise warn. |

Exact string values per mode live in `defaults.json` (`retrieval_scope`, `candidate_staging`, `self_promotion_threshold`, `abstention_level`, `show_receipts`).

## Relation to frontier PRs

- **PR 1 (abstention / uncertainty):** Modes scale how aggressively to pair envelope output with promotion posture — especially `high_risk_abstention`. See [abstention-policy.md](abstention-policy.md).
- **PR 2 (review orchestrator):** Review packets can show the active mode next to promotion advice — [review-orchestrator.md](orchestration/review-orchestrator.md).
- **PR 3 (checkpoints / handoffs):** Checkpoints and handoffs may record `Policy mode:` for resumption — [long-horizon-work.md](runtime/long-horizon-work.md).
- **PR 4 (budgeted context):** Budgeted prepared context lists policy mode at the top — [context-budgeting.md](runtime/context-budgeting.md).

## What modes do not do

- They do **not** bypass companion gate review or merge authority.
- They do **not** replace evidence, provenance, or [conflict resolution order](conflict-resolution-order.md).
- They are **not** a compliance theater layer — they operationalize **governance-first** boundaries already in this repo.

## See also

- [`config/policy_modes/defaults.json`](../config/policy_modes/defaults.json)
- [`scripts/runtime/policy_mode_config.py`](../scripts/runtime/policy_mode_config.py)
