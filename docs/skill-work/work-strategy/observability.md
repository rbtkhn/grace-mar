# work-strategy — observability

**Purpose:** Lane-local **metrics** for judgment volume, quality, and hygiene — **not** Record truth.

## Artifact

- **Generated:** `artifacts/work-strategy/strategy-observability.json` via [build_strategy_observability.py](../../../scripts/build_strategy_observability.py).

## Metrics — structure (v1, unchanged)

| Field | Meaning |
|-------|---------|
| `structure.decision_point_files` | Markdown files under `decision-points/` (excl. README) |
| `structure.decision_points_open` | Files whose `**Status:**` line is `open` |
| `structure.authorized_sources_yaml_entries` | Rows in `authorized-sources.yaml` |
| `structure.promotion_policy_present` | `promotion-policy.json` exists |

## Metrics — judgment quality (v2)

| Field | Meaning | Healthy range |
|-------|---------|---------------|
| `judgment_quality.notebook_entries_total` | Total `## YYYY-MM-DD` blocks across all months | Growing; 0 early is fine |
| `judgment_quality.inbox_pending_lines` | Non-blank lines below the append marker in `daily-strategy-inbox.md` | 0–30 normal; >50 = overdue weave or prune |
| `judgment_quality.promotion_date_mentions` | Date strings found in `STRATEGY.md` (proxy for promotion activity) | 0 fine early; sustained 0 over months = notebook may not feed STRATEGY |
| `months.<YYYY-MM>.dated_entries` | Entries that month | Variable |
| `months.<YYYY-MM>.avg_sections_per_entry` | Average of Chronicle/Reflection/References/Open present per entry | 4.0 = all four; <3.0 = sections skipped regularly |
| `months.<YYYY-MM>.avg_links_per_entry` | Average link/path references per `### References` section | >2 healthy; <1 = under-cited judgment |
| `months.<YYYY-MM>.open_carry_forward` | Open sections with unresolved items (verify, deferred, questions) | Active threads normal; very high relative to entries = debt |

**Not yet auto-computed:** recommendation acceptance/rejection, cross-lane reference counts — require operator logging convention.

**Notebook markers (`[watch]`, `[decision]`, `[promote]`):** not counted in this JSON; definitions live in [NOTEBOOK-PREFERENCES.md](strategy-notebook/NOTEBOOK-PREFERENCES.md#escalation-marker-preference). Extend [build_strategy_observability.py](../../../scripts/build_strategy_observability.py) before documenting marker counts in this file.

## Alignment

Optional alignment with [schema-registry/observability-report.v1.json](../../../schema-registry/observability-report.v1.json) for top-level dashboards is a future mapping; this file uses `schemaVersion` `2.0.0-work-strategy`.

**Authority:** Observability does **not** trigger Record merges. See [promotion-ladder.md](promotion-ladder.md).
