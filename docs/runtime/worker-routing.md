# Worker routing (runtime skeleton)

Grace-Mar’s **runtime** layer has many specialist scripts (retrieval, staging, review packets, handoffs). **Worker routing** gives an explicit, inspectable map of:

- **Shared workers** — governance/support roles that conceptually apply across many tasks (provenance, boundaries, budgets, task anchors).
- **Routed workers** — domain roles chosen by **task type** (`strategy`, `tacit`, `moonshot`, `contradiction`, `research`).

This is **architecture clarification**, not a second governance layer. Routing metadata is **non-canonical** and does **not** merge into the Record, change merge authority, or replace RECURSION-GATE.

## Where it lives

| Artifact | Role |
|----------|------|
| [`config/runtime_workers/registry.yaml`](../../config/runtime_workers/registry.yaml) | Declares shared + routed workers and **entrypoint** paths (existing scripts). |
| [`scripts/runtime/worker_registry.py`](../../scripts/runtime/worker_registry.py) | Loads YAML and validates entrypoint files exist. |
| [`scripts/runtime/worker_router.py`](../../scripts/runtime/worker_router.py) | Maps `task_type` → routed worker + lists shared workers. |

## v1 behavior

- **No** automatic execution of routed scripts from the registry.
- The **[runtime worker](runtime-worker.md)** [`grace_mar_runtime_worker.py`](../../scripts/runtime/grace_mar_runtime_worker.py) can take optional **`--task-type`**; it resolves routing and writes **`provenance.worker_routing`** on the trace line in `runtime/runtime-worker/traces/index.jsonl` (non-canonical).

**Pass overlays (optional):** **`--overlay`** supplies default scope/caps/task-type emphasis from [`overlays.yaml`](../../config/runtime_workers/overlays.yaml) — see [worker-overlays.md](worker-overlays.md). Routing still follows **`--task-type`** (overlay default or explicit).

## Task type mapping

| `--task-type` | Routed worker (registry key) |
|---------------|-------------------------------|
| `strategy` | `strategy_worker` |
| `tacit` | `tacit_worker` |
| `moonshot` | `moonshot_worker` |
| `contradiction` | `contradiction_worker` |
| `research` | `research_worker` |

Shared workers listed in the registry (e.g. `provenance_checker`, `boundary_checker`, `budget_enforcer`, `anchor_reinjector`) appear in the routing payload for every resolved route.

## Example

```bash
python3 scripts/runtime/grace_mar_runtime_worker.py \
  --task inspect_work_area \
  --task-type strategy \
  --dry-run \
  --lens quick-scan \
  --repo-root /path/to/grace-mar
```

Inspect the last JSON line in `runtime/runtime-worker/traces/index.jsonl` (or `GRACE_MAR_RUNTIME_WORKER_HOME/traces/index.jsonl`): `provenance.worker_routing` includes `routed_worker`, `shared_workers`, `entrypoints`, and `non_canonical: true`.

## See also

- [worker-overlays.md](worker-overlays.md) — pass defaults on the same worker spine
- [runtime-worker.md](runtime-worker.md) — proposals + traces
- [context-budgeting.md](context-budgeting.md) — budget vs policy vs workflow depth
