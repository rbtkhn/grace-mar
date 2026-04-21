# Execution receipts (runtime worker)

**Execution receipts** are **runtime-only** audit summaries emitted by [`grace_mar_runtime_worker.py`](../../scripts/runtime/grace_mar_runtime_worker.py) after each successful run. They are **non-canonical**: they do **not** merge into the Record, do **not** replace RECURSION-GATE, and do **not** confer merge authority. They summarize **one run** by linking its **trace ledger** (`traces/index.jsonl`), **proposal** (`proposals/<run_id>.md`), **scope** (root + caps), **worker routing** (when `--task-type` / overlay resolved routing), a small **epistemic** posture block, and **outcome**.

- **On disk (default):** `runtime/runtime-worker/receipts/<run_id>.json` (or under `GRACE_MAR_RUNTIME_WORKER_HOME/receipts/`).
- **Schema:** [`schema-registry/execution-receipt.v1.json`](../../schema-registry/execution-receipt.v1.json).
- **Audit atom:** The append-only **trace line** in `traces/index.jsonl` remains the low-level ledger; the receipt is a **projected**, schema-validated view for operators and tooling.

See also: [Runtime worker](../runtime-worker.md), [Runtime vs Record](../runtime-vs-record.md), [Worker routing](worker-routing.md).
