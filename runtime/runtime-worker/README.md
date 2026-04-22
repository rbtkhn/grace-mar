# Runtime worker (Grace-Mar)

**Non-canonical.** Disposable worker outputs: **proposals** (markdown) and **trace** lines (JSONL). **Not** SELF, EVIDENCE, SKILLS, or gate truth.

| Path | Role |
|------|------|
| `proposals/` | Operator-facing markdown snapshots (gitignored `*.md`). |
| `traces/index.jsonl` | Append-only audit lines per run (gitignored). |
| `receipts/` | One execution receipt JSON per run (`<run_id>.json`); non-canonical summary. Operator runs are gitignored except **`gov_eval_*.json`** — synthetic receipts checked in for the [governed eval harness](../../docs/evals/governed-eval-harness.md) (see [execution-receipts](../../docs/runtime/execution-receipts.md)). |
| `peer_reviews/` | Optional [worker peer review](../../docs/runtime/worker-peer-review.md) JSON (`<review_run_id>.json`); gitignored. |

**Doctrine:** [docs/runtime-worker.md](../../docs/runtime-worker.md)

**Commands:** `python3 scripts/runtime/grace_mar_runtime_worker.py --help` · preset **`--lens`** values: `notebook-health`, `inbox-day`, `quick-scan` (see [docs/runtime-worker.md](../../docs/runtime-worker.md)).
