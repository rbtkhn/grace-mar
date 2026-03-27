# Demo change-review queue (synthetic)

Post-seed governed-change demo for schema validation and CI. Layout:

- `change_review_queue.json`, `change_event_log.json`
- `proposals/`, `decisions/`, `diffs/` — one JSON file each in the demo

Validate:

```bash
python3 scripts/validate-change-review.py users/demo/review-queue
```

Generate a readable Markdown diff:

```bash
python3 scripts/generate-identity-diff.py users/demo/review-queue/diffs/diff-001.json --output users/demo/review-queue/identity_diff.md
```

See [docs/change-review-validation.md](../../docs/change-review-validation.md).
