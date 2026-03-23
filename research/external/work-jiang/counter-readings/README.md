# Counter-readings registry

Rival frameworks and objections that sit alongside Jiang’s lecture-backed claims (for comparison chapters, not Voice knowledge).

## Registry

- **File:** [registry/counter-readings.jsonl](registry/counter-readings.jsonl) — one JSON object per line.

## Fields

| Field | Meaning |
|-------|---------|
| `counter_id` | Stable id (`cr-0001`, …). |
| `target_type` | `chapter` \| `thesis_subclaim` \| `claim` \| `concept`. |
| `target_id` | `ch03`, `t01`, `clm-0007`, `civ-formation`, … |
| `framework` | Short label for the rival school (e.g. “realist IR”, “secularization thesis”). |
| `claim` | One-sentence counter or tension. |
| `source_basis` | Where this reading is usually argued (text, tradition, or “common IR”). |
| `strength` | `low` \| `medium` \| `high` (how strong the rival is in debate, not truth). |
| `status` | `draft` \| `reviewed`. |
| `notes` | Operator notes, citations to add. |

## Relation to divergence

[Divergence tracking](../divergence-tracking/README.md) records **where Jiang differs from mainstream**. Counter-readings here are **structured rival lenses** used for thesis and chapter comparison — overlap is possible, but the schemas differ.

## Renders

- `COUNTER-READINGS.md` — human-readable (run `python3 scripts/work_jiang/render_counter_readings.py`).
- `metadata/counter-reading-links.yaml` — machine links for chapters/thesis/claims/concepts (run `python3 scripts/work_jiang/link_counter_readings.py`).
