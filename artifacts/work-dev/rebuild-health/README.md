# rebuild-health (work-dev)

**Purpose:** Derived observability for the repo-owned regeneration lane.

This folder holds summaries built from:

- `artifacts/work-dev/rebuild-receipts/`
- `artifacts/work-dev/derived-regeneration-manifest.json`

These outputs are:

- **derived**
- **rebuildable**
- **not** Record truth
- **not** gate authority

Typical command:

```bash
python3 scripts/report_rebuild_health.py
```

See:

- [../../../docs/skill-work/work-dev/derived-regeneration.md](../../../docs/skill-work/work-dev/derived-regeneration.md)
- [../../../docs/runtime-vs-record.md](../../../docs/runtime-vs-record.md)
