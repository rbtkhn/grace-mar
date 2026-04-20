# Worker overlays (runtime)

**Worker overlays** are small, **config-driven** default bundles for the [runtime worker](../runtime-worker.md) (`scripts/runtime/grace_mar_runtime_worker.py`). They tune **scope, caps, default task type, and emphasis flags** for a pass (strategy, moonshot, research, tacit) without adding new workers or changing merge authority.

## How this differs from routed workers

| Concept | Role |
|--------|------|
| **Overlay** | Optional defaults and emphasis hints (this doc); lives in [`config/runtime_workers/overlays.yaml`](../../config/runtime_workers/overlays.yaml). |
| **Routed worker** | Which **existing script** corresponds to a `--task-type` — see [worker-routing.md](worker-routing.md) and [`registry.yaml`](../../config/runtime_workers/registry.yaml). |

Overlays **do not** replace the router. Resolved routing still comes from `task_type` → [`worker_router.py`](../../scripts/runtime/worker_router.py). Overlays may supply a **default** `task_type` when you omit `--task-type`.

## Precedence (highest first)

1. **Explicit CLI** — `--scope`, `--max-files`, `--max-chars`, `--task-type`, `--lens`, `--compose-with`, etc.
2. **Overlay defaults** — from `overlays.yaml` for any of the above that are still unset.
3. **Built-in worker defaults** — e.g. default strategy-notebook scope, lens presets.

If you use **`--lens`**, the lens wins over the overlay for **scope** and **caps**; the overlay may still set **`--task-type`** when omitted.

## Governance

Overlays are **WORK-only**, **non-canonical**, and **inspectable** in the trace (`provenance.runtime_receipt`, `provenance.worker_routing`). They do **not** write SELF, EVIDENCE, SKILLS, gate, or prompt surfaces, and they do **not** change companion merge authority.

## Available overlays (v1)

| Overlay | Intent (short) |
|---------|------------------|
| `strategy` | Strategy-notebook scope; anchor + contradiction emphasis |
| `moonshot` | Same default scope as strategy in-repo; mission-context emphasis |
| `research` | `research/` tree; provenance + evidence-density emphasis |
| `tacit` | `runtime/tacit`; candidate extraction + grounding emphasis |

## Examples

**Strategy overlay + explicit scope** (overlay supplies default `task_type` = strategy if you omit `--task-type`):

```bash
python3 scripts/runtime/grace_mar_runtime_worker.py \
  --overlay strategy \
  --scope docs/skill-work/work-strategy/strategy-notebook \
  --dry-run \
  --repo-root /path/to/grace-mar
```

**Research overlay with explicit `--task-type`** (CLI overrides overlay default task type):

```bash
python3 scripts/runtime/grace_mar_runtime_worker.py \
  --overlay research \
  --task-type contradiction \
  --scope research \
  --dry-run \
  --repo-root /path/to/grace-mar
```

## See also

- [worker-routing.md](worker-routing.md) — `task_type` → routed worker mapping
- [runtime-worker.md](runtime-worker.md) — proposals and traces

## Deferred

Dynamic overlay composition, prompt-stack overlays, autonomous overlay workers, and repo-wide propagation beyond this runtime worker are out of scope for v1.
