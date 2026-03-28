# Pattern tracking (cross-lecture mechanisms)

**Purpose:** Index **recurring mechanisms / civilizational scripts** Jiang uses across lectures — separate from **forecast-like rows** in [`prediction-tracking`](../prediction-tracking/README.md). Operator research only; not Record until merged through the gate.

**Relation to predictions:** Predictions stay in `predictions.jsonl` (`jiang-GS..-NNN`). Patterns may list **`linked_prediction_ids`** that those forecasts instantiate or stress-test. Do **not** fold pattern rhetoric into the prediction registry without a real evaluable claim.

**Relation to divergence:** Divergence rows ([`divergence-tracking`](../divergence-tracking/README.md)) compare claims to named mainstream frames. A pattern can underwrite many divergences; link in prose or add optional `related_divergence_ids` when you need machine joins.

---

## ID policy (aligned with repo)

- **`pattern_id`** — `pat-` + zero-padded digits, globally unique (e.g. `pat-0001`, `pat-0012`). **Do not** use `pred:` / `pat:` URI-style prefixes; keep the same plain-slug style as `jiang-GS01-001` and `div-GS02-001`.
- **Evidence hooks** use existing join keys: **`video_id`**, **`lecture_ref`** (path under `lectures/`), optional **`source_id`** when already known from [`metadata/sources.yaml`](../metadata/sources.yaml).
- **Links to predictions:** `linked_prediction_ids` must be existing **`prediction_id`** values from `predictions.jsonl`.

---

## Recurrence semantics (single source of truth)

**`performance`** holds the overall assessment frame:

| Field | Meaning |
|--------|--------|
| `signatures_matched` | Cases (lecture + analog + mixed) where the pattern’s **observable signatures** were judged to match |
| `total_cases` | Comparable cases **examined** for this pattern (denominator for human summary) |
| `narrative` | Prose: where it recurs, where it breaks, caveats |
| `utility_score` | Optional: `high` / `medium` / `low` (operator judgment) |

**`performance.recurrence`** (optional) breaks out **where** matches came from — **without duplicating** a second mystery `total_cases`:

| Field | Meaning |
|--------|--------|
| `lecture_occurrences` | Count of matches anchored in **curated lecture / transcript** evidence |
| `analog_occurrences` | Count of matches from **historical or external analog** cases (not the same as lecture count) |
| `frequency_qualifier` | `high` / `medium` / `low` / `rare` / `context-dependent` |
| `scope` | Short qualifier (e.g. region, era, “strong analogs only”) |
| `note` | Caveats; avoids false precision |

**Invariant (validator-enforced):**  
`lecture_occurrences + analog_occurrences <= total_cases`  
**Recommended:** `lecture_occurrences + analog_occurrences <= signatures_matched` (if you treat the sum as “explained matches”; if not, document in `note`).

Optional display **`rate`** for sorting: `signatures_matched / total_cases` — derive at render time; do not require stored floats that drift from integers.

---

## Registry format

**Append-only JSONL:** [registry/patterns.jsonl](registry/patterns.jsonl)

Required per row:

- `pattern_id`, `name`, `definition` (min substance per validator)
- `observable_signatures` — non-empty list of short strings
- `performance` — `signatures_matched`, `total_cases` (≥1), `narrative`

Optional:

- `evidence_hooks` — list of `{ "video_id"?, "lecture_ref"?, "source_id"?, "excerpt"? }`
- `linked_prediction_ids`, `dependencies` (other `pattern_id`s), `concept_refs`
- `performance.utility_score`, `performance.recurrence`, `performance.historiographic_note`
- `notes` — operator-only caveats

---

## Tooling

- Validate: `python3 scripts/work_jiang/validate_patterns_registry.py`
- Also runs as part of `validate_book_consistency.py --all` / `--chapter` / `--volume`
- Link pass: `link_supporting_registries.py` writes `metadata/pattern-links.yaml`
- SQLite: `rebuild_registry_db.py` materializes `patterns` table from JSONL (canonical remains JSONL)

---

## Rhythm

- **After** adding a substantive pattern row: run `validate_patterns_registry.py` and `rebuild_registry_db.py` if you query SQLite.
- **Dedup:** Similar `name` + overlapping hooks → merge or cross-link `dependencies` before inflating `pat-*` IDs.
