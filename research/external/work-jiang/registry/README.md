# Registry materialized DB

`work_jiang_metrics.sqlite` is **generated** from canonical JSONL:

```bash
python3 scripts/work_jiang/rebuild_registry_db.py
```

Do not edit SQLite by hand; change `prediction-tracking/registry/predictions.jsonl`, `divergence-tracking/registry/divergences.jsonl`, or `pattern-tracking/registry/patterns.jsonl` and rebuild.

**Link pass:** `link_supporting_registries.py` reads JSONL by default. Set `WORK_JIANG_REGISTRY_PREFER_SQLITE=1` to load the same rows from SQLite (after rebuild) — see [OFFLOAD-ENV.md](../OFFLOAD-ENV.md).
