# Claims ledger (work-jiang)

Structured **philosophical and empirical claims** attributed to the Geo-Strategy corpus — not limited to [prediction-tracking](../prediction-tracking/README.md) (forecasts are one `claim_type`).

## Registry

- **File:** [`registry/claims.jsonl`](registry/claims.jsonl) — one JSON object per line (append-only discipline).

## Enums (recommended)

| Field | Values |
|-------|--------|
| `claim_type` | `descriptive`, `causal`, `normative`, `anthropological`, `theological`, `historical`, `predictive` |
| `scope` | `personal`, `civilizational`, `geopolitical`, `educational`, `religious`, `institutional` |
| `status` | `captured`, `supported`, `contested`, `pending_resolution`, `retired` |

## Optional PSY-HIST fields

When a claim is extracted from or informed by PSY-HIST lens analysis, you may add:

| Field | Type | Description |
|-------|------|-------------|
| `psycho_phase` | string | Cycle phase, e.g. `overextension`, `growth`, `crisis`, `collapse` |
| `seldon_flag` | boolean | True if the claim maps to a Seldon-crisis window (high-leverage intervention) |
| `horizon_years` | integer | Predictability window in years (e.g. 20 for a multi-decade forecast) |

No migration of existing rows; new claims may include these.

## Relationship to thesis

- [`metadata/thesis-map.yaml`](../metadata/thesis-map.yaml) lists `linked_claim_ids` per subclaim.
- [`scripts/work_jiang/link_claims_to_thesis.py`](../../scripts/work_jiang/link_claims_to_thesis.py) emits [`metadata/thesis-claim-links.yaml`](../metadata/thesis-claim-links.yaml).
- [`scripts/work_jiang/render_claims_overview.py`](../../scripts/work_jiang/render_claims_overview.py) generates [`CLAIMS-OVERVIEW.md`](../CLAIMS-OVERVIEW.md).

## Adding a row

1. Append one JSON line to `claims.jsonl` with a new `claim_id`.
2. Reference `source_id` (`geo-XX`) and `analysis_id` (same id when analysis memo exists; `null` only when [`metadata/sources.yaml`](../metadata/sources.yaml) shows analysis missing).
3. Add the `claim_id` to the appropriate `linked_claim_ids` list in `thesis-map.yaml` (or run linker in check mode).
4. Regenerate overviews and run `validate_argument_layer.py`.
