# work-strategy — observability

**Purpose:** Lane-local **metrics** for judgment volume and hygiene — **not** Record truth.

## Artifact

- **Generated:** `artifacts/work-strategy/strategy-observability.json` via [build_strategy_observability.py](../../../scripts/build_strategy_observability.py).

## Metrics (v1)

| Field | Meaning |
|-------|---------|
| `decision_point_files` | Markdown files under `decision-points/` (excl. README) |
| `decision_points_open` | Files whose `**Status:**` line is `open` |
| `authorized_sources_yaml_entries` | Rows in `authorized-sources.yaml` |
| `promotion_policy_present` | `promotion-policy.json` exists |

**Phase-2** (not auto-computed): recommendation acceptance/rejection, cross-lane reference counts — require operator logging convention.

## Alignment

Optional alignment with [schema-registry/observability-report.v1.json](../../../schema-registry/observability-report.v1.json) for top-level dashboards is a future mapping; this file uses `schemaVersion` `1.0.0-work-strategy`.

**Authority:** Observability does **not** trigger Record merges. See [promotion-ladder.md](promotion-ladder.md).
