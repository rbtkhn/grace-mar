# Lecture analysis JSON schema (work-jiang)

Operator research only — not Voice knowledge until merged through the gate. See [research/external/work-jiang/README.md](../../research/external/work-jiang/README.md) § Boundaries.

## File location

Sidecar next to the Markdown memo, same stem:

- `analysis/<video_id>-<slug>-analysis.md` → `analysis/<video_id>-<slug>-analysis.json`

Optional front-matter key: `analysis_json_path` if the JSON lives elsewhere.

## Version fields

| Field | Where |
|-------|--------|
| `schema_version` | Root of JSON (e.g. `1.0`) |
| `memo_format_version` | YAML front matter on `.md` (e.g. `1`) |
| `analysis_json_version` | Optional; if set, must match `schema_version` (validator enforces) |

**Lazy upgrade:** `python3 scripts/work_jiang/validate_lecture_analysis_json.py --write-bump-major path.json` bumps `1.x` → `2.0` after a clean validate. Batch: `migrate_analysis_memo.py --from 1 --to 2`.

## Root object (required keys)

| Key | Type | Description |
|-----|------|-------------|
| `schema_version` | string | Schema version for migrations |
| `summary` | string | Short synthesis of the lecture |
| `key_claims` | array | See below |
| `predictions` | array | Forecast-like rows (map to prediction registry) |
| `divergences_from_prior` | array | Contrasts vs earlier lectures or named mainstream |
| `open_questions` | array of string | Unresolved questions |
| `cross_links` | array | Links to other sources / memos |

Optional:

| Key | Type | Description |
|-----|------|-------------|
| `source` | object | `video_id`, `source_id`, `model_id` |

## `key_claims[]` objects

| Key | Type | Required |
|-----|------|----------|
| `claim_text` | string | yes |
| `claim_type` | string | yes — e.g. `observation`, `interpretation`, `forecast`, `normative` |
| `confidence` | string | no — e.g. `low`, `medium`, `high` |
| `evidence_quote_ref` | string | no — pointer into transcript or timestamp |

## `predictions[]` objects (align with JSONL)

| Key | Type | Required |
|-----|------|----------|
| `claim_summary` | string | yes |
| `claim_type` | string | yes |
| `excerpt` | string | no |
| `evaluation_window` | object or null | `{ "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" }` |
| `resolution_status` | string | default `pending` for new extractions |

## `divergences_from_prior[]` objects

| Key | Type | Required |
|-----|------|----------|
| `jiang_claim` | string | yes |
| `mainstream_anchor` | string | no |
| `mainstream_summary` | string | no |
| `divergence_type` | string | no — `empirical`, `interpretive`, … |
| `strength` | string | no |

## `cross_links[]` objects

| Key | Type | Required |
|-----|------|----------|
| `target` | string | yes — slug, `video_id`, or URL |
| `relation` | string | no — e.g. `supports`, `contradicts`, `extends` |
| `note` | string | no |

## Example (minimal)

```json
{
  "schema_version": "1.0",
  "summary": "Lecture argues X; predicts Y under conditions Z.",
  "key_claims": [
    {
      "claim_text": "Alliance seams open under electoral cycles.",
      "claim_type": "interpretation",
      "confidence": "medium",
      "evidence_quote_ref": "~12:00"
    }
  ],
  "predictions": [
    {
      "claim_summary": "Event E within two years.",
      "claim_type": "time_bounded",
      "excerpt": "verbatim hint",
      "evaluation_window": { "start": "2026-01-01", "end": "2028-12-31" },
      "resolution_status": "pending"
    }
  ],
  "divergences_from_prior": [],
  "open_questions": ["What metric for 'popular'?"],
  "cross_links": [
    { "target": "geo-strategy-01-iran-strategy-matrix-2024-04-24.md", "relation": "extends", "note": "Iran matrix" }
  ],
  "source": { "video_id": "xEEpOxqdU5E", "source_id": "geo-01" }
}
```

Validation: `python3 scripts/work_jiang/validate_lecture_analysis_json.py path/to/file.json`
