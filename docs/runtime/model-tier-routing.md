# Model tier routing (runtime-only)

**Non-canonical WORK policy.** Maps `task_type` / optional `task_subtype` / optional `action` to an allowed **model tier** (A–D, X), a **preferred provider/model** from environment variables, and a **fallback chain**. Used by the runtime worker’s **execution receipt** (`model_policy` block). Does **not** merge into the Record, does **not** change RECURSION-GATE, and does **not** by itself invoke or switch providers.

## Tiers (v1)

| Tier | Meaning |
|------|--------|
| **A** | Deterministic / no model |
| **B** | Cheap public model |
| **C** | Reliable frontier model |
| **D** | Privileged / restricted (no default providers in v1 YAML) |
| **X** | Forbidden (e.g. disallowed `action`) |

## Config

| File | Role |
|------|------|
| [`config/model_routing/model_tiers.yaml`](../../config/model_routing/model_tiers.yaml) | Tier labels, provider rows, `model_env` names |
| [`config/model_routing/task_policy.yaml`](../../config/model_routing/task_policy.yaml) | Per-task default tier, subtypes, `forbidden_actions`, default `fallback_chain` |

**Resolver:** [`scripts/runtime/model_policy.py`](../../scripts/runtime/model_policy.py) — `resolve_model_policy(repo_root=..., task_type=..., task_subtype=..., action=...)`.

**Env vars (examples):** `OPENAI_CHEAP_MODEL` (tier B), `OPENAI_DEFAULT_MODEL` (tier C). Values are read at resolution time; unset env → `resolved_model: null` in the receipt.

## Relation to other surfaces

- **Worker routing** ([`worker_router.py`](../../scripts/runtime/worker_router.py)): maps `task_type` → worker **entrypoints**. Model policy maps the same task family → **tier/model policy**. Keep task names aligned between `TASK_TYPE_TO_ROUTED` and `task_policy.yaml` `tasks:` to avoid drift.
- **LLM summary** ([`agents_sdk_adapter.py`](../../scripts/runtime/agents_sdk_adapter.py)): still uses `OPENAI_MODEL` (default `gpt-4o-mini`) for the optional summary until a future change wires calls to tier/env. Receipt `model_policy` may therefore **differ** from the model actually used for summarization — PR2 is policy + receipt projection only.

## CLI

[`grace_mar_runtime_worker.py`](../../scripts/runtime/grace_mar_runtime_worker.py): optional `--task-subtype` (e.g. `quick_scan`, `contradiction_review`) feeds the resolver and receipt `task_subtype`.

## Non-goals (v1)

- No multi-provider failover execution, token/cost accounting, or eval harness.
- No automatic vendor switching; no gate or merge behavior changes.

See also: [execution receipts](execution-receipts.md), [runtime worker](../runtime-worker.md), [runtime vs Record](../runtime-vs-record.md).
