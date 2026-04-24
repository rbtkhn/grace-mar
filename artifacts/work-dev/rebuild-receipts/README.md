# rebuild-receipts (work-dev)

**Purpose:** Default storage location for repo-owned **derived rebuild receipts** emitted by `scripts/regenerate_all_derived.py`.

These receipts are:

- **derived**
- **WORK-only**
- **not** the Record
- **not** EVIDENCE truth
- **not** merge or gate artifacts

They record what the repo-owned regeneration entrypoint considered changed, which rebuild targets it selected, and whether each target ran, was skipped, or failed.

Typical usage:

```bash
python3 scripts/regenerate_all_derived.py --changed --dry-run
python3 scripts/regenerate_all_derived.py --all
```

See:

- [../../../docs/skill-work/work-dev/derived-regeneration.md](../../../docs/skill-work/work-dev/derived-regeneration.md)
- [../../../docs/runtime-vs-record.md](../../../docs/runtime-vs-record.md)
