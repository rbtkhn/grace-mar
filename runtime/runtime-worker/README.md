# Runtime worker (Grace-Mar)

**Non-canonical.** Disposable worker outputs: **proposals** (markdown) and **trace** lines (JSONL). **Not** SELF, EVIDENCE, SKILLS, or gate truth.

| Path | Role |
|------|------|
| `proposals/` | Operator-facing markdown snapshots (gitignored `*.md`). |
| `traces/index.jsonl` | Append-only audit lines per run (gitignored). |
| `receipts/` | One execution receipt JSON per run (`<run_id>.json`); non-canonical summary; gitignored (see [execution-receipts](../../docs/runtime/execution-receipts.md)). |

**Doctrine:** [docs/runtime-worker.md](../../docs/runtime-worker.md)

**Commands:** `python3 scripts/runtime/grace_mar_runtime_worker.py --help` · preset **`--lens`** values: `notebook-health`, `inbox-day`, `quick-scan` (see [docs/runtime-worker.md](../../docs/runtime-worker.md)).
