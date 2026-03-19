# Pipeline events (`pipeline-events.jsonl`)

Append-only JSON lines: gate lifecycle, dyad hooks, maintenance. **Canonical path:** `users/<id>/pipeline-events.jsonl`.

## Common fields

| Field | Type | Description |
|-------|------|-------------|
| `ts` | string | ISO timestamp |
| `event` | string | e.g. `staged`, `approved`, `rejected`, `applied` |
| `candidate_id` | string \| null | Gate id (`CANDIDATE-*`) or `null` for non-candidate events |
| `channel_key` | string | Source route (`telegram:…`, `operator:cli`, …) |

## `event_schema`

- **`1` or absent** — legacy rows: minimal fields.
- **`2`** — richer rows (staged / approved / rejected / applied) for audits and timelines.

## `staged` (schema 2)

| Field | Description |
|-------|-------------|
| `conflicts_detected` | bool — contradiction check flagged before write |
| `mind_category`, `profile_target`, `proposal_class`, `signal_type` | From analyst YAML (truncated) |
| `summary_snippet` | Truncated candidate summary |

## `approved` / `rejected` (schema 2)

Same candidate-field picks as staged where present in the gate block, plus:

| Field | Description |
|-------|-------------|
| `conflicts_detected_at_stage` | bool — YAML indicated conflicts at staging |
| `rejection_reason` | (rejected only) |

## `applied` (schema 2)

| Field | Description |
|-------|-------------|
| `evidence_id` | `ACT-*` in self-evidence |
| `ix_entry_id` | `LEARN-*`, `CUR-*`, or `PER-*` in SELF IX |
| `surface` | `SELF_KNOWLEDGE` \| `SELF_CURIOSITY` \| `SELF_PERSONALITY` |
| `had_conflicts` | bool — staging block mentioned conflicts |
| `summary_snippet`, `mind_category`, `profile_target`, `proposal_class` | From merge context |
| `source` | e.g. `process_approved_candidates` |
| `actor` | Who approved the batch |

## Emission helpers

- In-process: `bot.core.emit_pipeline_event`
- CLI: `scripts/emit_pipeline_event.py` — use `--merge-json '<object>'` for long or structured payloads (avoids shell/argv issues).
