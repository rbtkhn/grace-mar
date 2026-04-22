# Execution receipts (runtime worker)

**Execution receipts** are **runtime-only** audit summaries emitted by [`grace_mar_runtime_worker.py`](../../scripts/runtime/grace_mar_runtime_worker.py) after each successful run. They are **non-canonical**: they do **not** merge into the Record, do **not** replace RECURSION-GATE, and do **not** confer merge authority. They summarize **one run** by linking its **trace ledger** (`traces/index.jsonl`), **proposal** (`proposals/<run_id>.md`), **scope** (root + caps), **worker routing** (when `--task-type` / overlay resolved routing), optional **`model_policy`** (tier / env-backed model — see [model-tier routing](model-tier-routing.md)), a small **epistemic** posture block, and **outcome**.

- **On disk (default):** `runtime/runtime-worker/receipts/<run_id>.json` (or under `GRACE_MAR_RUNTIME_WORKER_HOME/receipts/`).
- **Schema:** [`schema-registry/execution-receipt.v1.json`](../../schema-registry/execution-receipt.v1.json).
- **Audit atom:** The append-only **trace line** in `traces/index.jsonl` remains the low-level ledger; the receipt is a **projected**, schema-validated view for operators and tooling.

### `model_policy` field reference (runtime-only)

Nullable object from [`model_policy.resolve_model_policy`](../../scripts/runtime/model_policy.py). **Non-canonical** policy projection for the run; does not change which model the optional LLM summary uses until separately wired (see [model-tier routing](model-tier-routing.md)).

| Key | Meaning |
|-----|--------|
| `allowed_tier` | Tier letter from YAML policy: `A` (no model) … `D`, or `X` (forbidden action). |
| `resolved_provider` | Preferred provider id for the tier (e.g. `openai`), or null if none. |
| `resolved_model` | Model id from the tier’s `model_env` at resolution time, or null if unset. |
| `fallback_chain` | Ordered tier fallbacks from `task_policy.yaml` defaults (empty when tier `X`). |
| `requires_human_review` | Subtype-driven flag (e.g. draft flows); boolean. |

See also: [Runtime worker](../runtime-worker.md), [Runtime vs Record](../runtime-vs-record.md), [Worker routing](worker-routing.md), [Model tier routing](model-tier-routing.md).
