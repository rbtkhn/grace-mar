# Runtime worker peer review (non-canonical)

A **heuristic, runtime-only** pass that evaluates a **completed worker draft** (proposal markdown + [execution receipt](execution-receipts.md) for the same `run_id`). It emits JSON validated by `schema-registry/runtime-peer-review.v1.json`.

**Not** [RECURSION-GATE](../../users/grace-mar/recursion-gate.md) review, **not** merge authority, and **not** the [review orchestrator](../orchestration/review-orchestrator.md) (which builds multi-phase **observation / candidate** packets).

**Entry:** [`scripts/runtime/run_runtime_peer_review.py`](../../scripts/runtime/run_runtime_peer_review.py) — see `--help`.

**Outputs:** `verdict`, `flags`, `overclaim` (from `scope_verification` when present), and `evidence_discipline` heuristics. Optional `--save` writes `runtime/runtime-worker/peer_reviews/<review_run_id>.json` (or under `GRACE_MAR_RUNTIME_WORKER_HOME/peer_reviews/`).

**Linkage:** Each result includes `review_run_id`, `draft_run_id`, and `linkage` paths so a draft and its review artifact can be found together. Runtime-only; nothing here approves or merges into the Record.
