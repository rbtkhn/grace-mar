<!-- GENERATED — run: python scripts/work_dev/build_dashboard.py -->

# work-dev dashboard

- **Generated:** `2026-03-25T16:14:48Z`

## Reliability

- Provenance completeness (pipeline-events proxy): **1.00**

## Boundary health

- Open gap IDs: BUILD-AI-GAP-005
- Lane violation count (observability feed): 0
- Continuity block count (observability feed): 1

## Gate throughput (pipeline events)

- `applied`: 35
- `approved`: 2
- `dyad:checkpoint_request`: 2
- `intent_constitutional_critique`: 14
- `openclaw_export`: 1
- `rejected`: 2
- `staged`: 14
- `validation_failed`: 7

## Integration status mix

- `documented_only`: 1
- `implemented`: 11
- `partial`: 2

## Notes

- Lane / continuity counts come from runtime/observability/*.jsonl when present (local or CI); empty feeds => 0.
- Regenerate after editing control-plane YAML.
