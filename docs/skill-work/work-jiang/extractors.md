# Work-jiang lecture extractors

Pluggable **series** handlers live under [`scripts/work_jiang/extractors/`](../../scripts/work_jiang/extractors/).

## Add a new domain

1. Subclass [`LectureExtractor`](../../scripts/work_jiang/extractors/base.py): set `series_id`, implement `prompt_system_path()`, `schema_version()`, optional `postprocess()`, `json_schema_variant()`, `map_prediction_to_staging` / `map_divergence_to_staging`.
2. Register in [`registry.py`](../../scripts/work_jiang/extractors/registry.py) (`_EXTRACTORS` dict) and/or add `source_id` prefix rules in `get_extractor_class()`.
3. If prompts differ materially, add `scripts/work_jiang/prompts/<series>_lecture_analysis_system.md` and point `prompt_system_path()` at it.

**Bundled plugins:** `GeoStrategyExtractor` (`geo-*`), `CivilizationExtractor` (`civ-*`), `PredictiveHistoryExtractor` (default / umbrella).

**Override for tests:** `WORK_JIANG_EXTRACTOR_SERIES=geo-strategy` forces a registered series.

## Smoke test

```bash
PYTHONPATH=scripts/work_jiang python3 scripts/work_jiang/run_lecture_analysis_dispatch.py --source-id civ-01
PYTHONPATH=scripts/work_jiang python3 scripts/work_jiang/run_lecture_analysis_dispatch.py --list-series
```

## Offload / env

See [OFFLOAD-ENV.md](../../../research/external/work-jiang/OFFLOAD-ENV.md) for GPU profile, registry SQLite read shim, and future LLM backend switches.
