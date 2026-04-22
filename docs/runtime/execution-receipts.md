# Execution receipts (runtime worker)

**Execution receipts** are **runtime-only** audit summaries emitted by [`grace_mar_runtime_worker.py`](../../scripts/runtime/grace_mar_runtime_worker.py) after each successful run. They are **non-canonical**: they do **not** merge into the Record, do **not** replace RECURSION-GATE, and do **not** confer merge authority. They summarize **one run** by linking its **trace ledger** (`traces/index.jsonl`), **proposal** (`proposals/<run_id>.md`), **scope** (root + caps), **worker routing** (when `--task-type` / overlay resolved routing), optional **`model_policy`** (tier / env-backed model — see [model-tier routing](model-tier-routing.md)), a small **epistemic** posture block, and **outcome**.

- **On disk (default):** `runtime/runtime-worker/receipts/<run_id>.json` (or under `GRACE_MAR_RUNTIME_WORKER_HOME/receipts/`).
- **Schema:** [`schema-registry/execution-receipt.v1.json`](../../schema-registry/execution-receipt.v1.json).
- **Audit atom:** The append-only **trace line** in `traces/index.jsonl` remains the low-level ledger; the receipt is a **projected**, schema-validated view for operators and tooling.

### `model_policy` field reference (runtime-only)

On the receipt, `model_policy` is **`null` or an object**; when present, every property in the object may be **null** per [`execution-receipt.v1.json`](../../schema-registry/execution-receipt.v1.json) (see schema for exact types and `additionalProperties: false`).

The object is produced by [`model_policy.resolve_model_policy`](../../scripts/runtime/model_policy.py) (or an equivalent hand-built projection in tests). **Non-canonical** policy projection for the run; it does not change which model an optional LLM summary uses until separately wired (see [model-tier routing](model-tier-routing.md)).

| Key | Meaning |
|-----|--------|
| `allowed_tier` | Tier letter from YAML policy: `A` (no model) … `D`, or `X` (forbidden action), or `null`. |
| `resolved_provider` | Preferred provider id for the tier (e.g. `openai`), or `null` if none. |
| `resolved_model` | Model id from the tier’s `model_env` at resolution time, or `null` if unset. |
| `fallback_chain` | Array: ordered tier fallbacks from `task_policy.yaml` defaults (empty when tier `X`). |
| `requires_human_review` | Subtype-driven flag (e.g. draft flows); `true`, `false`, or `null`. |

**Tooling (non-authoritative):** The [governed eval harness](../evals/governed-eval-harness.md) consumes `model_policy` when present for **reviewability** and **tier-based cost proxy** heuristics in its advisory score block only — not for merge, gate, or Record mutation.

### Verified scope (`scope_verification`, runtime-only)

Optional object on the receipt: **`null`** or a structured block produced by the worker for `inspect_work_area` runs. **Not** the Record, **not** merge authority, **not** a second governance system.

| Sub-block | Role |
|-----------|--------|
| `traversal` | **Worker-measured** counts: `files_seen` (candidates listed after collect), `files_opened` (readable files that contributed to the bundle), `chunks_read` (file sections read into the bundle), `paths_sample` (up to 20 repo-relative paths). |
| `stated_coverage` | `files_claimed` and `source` from **regex** on the proposal body (e.g. the worker’s `**files listed:** N` line). Treated as **narrative extract only**; not proof of disk access. `source` is `proposal_regex`, `absent`, or `parse_failed` (schema reserved; worker v1 usually uses `absent` or `proposal_regex`). |
| `coverage_ratio` | `0..1` or `null` when no comparison applies (e.g. no stated count). Heuristic, not a trust score. |
| `status` | `aligned`, `unstated`, `overclaim_suspected`, `underclaim_suspected`, or `parse_failed` — compared **stated** vs **verified** `files_opened` only. |
| `warnings` | Machine-readable reasons (I/O failure, char-cap truncation, mismatch notes). |

Do **not** use model or summary narration as the source of truth for these metrics; the worker’s traversal and optional regex extract are the only inputs.

**Related (orthogonal):** [Worker peer review](worker-peer-review.md) — a separate runtime pass on a **draft** proposal + receipt, distinct from the [review orchestrator](../../orchestration/review-orchestrator.md) (observations / gate packet path).

See also: [Runtime worker](../runtime-worker.md), [Runtime vs Record](../runtime-vs-record.md), [Worker routing](worker-routing.md), [Model tier routing](model-tier-routing.md).
