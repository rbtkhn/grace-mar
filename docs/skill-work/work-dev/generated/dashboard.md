<!-- GENERATED — run: python scripts/work_dev/build_dashboard.py -->

# work-dev dashboard

- **Generated:** `2026-04-13T05:22:38Z`

## Reliability

- Provenance completeness (pipeline-events proxy): **1.00**

## Autonomy (GAP-007)

- Shadow JSONL lines: **0** (`runtime/autonomy/shadow_decisions.jsonl`, gitignored)
- Tier evaluation (`low_risk_staging_suggestions`): **`no_log`**

## Boundary health

- Open gap IDs: _(none)_
- Lane violation count (observability feed): 0
- Continuity block count (observability feed): 23

## Gate throughput (pipeline events)

- `applied`: 43
- `approved`: 2
- `dyad:checkpoint_request`: 2
- `dyad:grounded_query`: 1
- `intent_constitutional_critique`: 20
- `maintenance`: 14
- `openclaw_export`: 1
- `rejected`: 4
- `sandbox_execution_post`: 1
- `sandbox_execution_pre`: 1
- `staged`: 22
- `validation_failed`: 8

## Integration status mix

- `documented_only`: 1
- `implemented`: 11
- `partial`: 2

## Notes

- Lane / continuity counts come from runtime/observability/*.jsonl when present (local or CI); empty feeds => 0.
- Regenerate after editing control-plane YAML.
- Autonomy: `runtime/autonomy/shadow_decisions.jsonl` (gitignored) + `evaluate_autonomy_tiers` vs `autonomy/tier_thresholds.yaml`; `no_log` when file missing or empty.
