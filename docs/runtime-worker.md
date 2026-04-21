# Runtime worker (OpenAI / optional LLM)

**Purpose:** A thin, disposable **WORK** helper under `scripts/runtime/` that inspects bounded doc trees (default: full `docs/skill-work/work-strategy/strategy-notebook/`), optionally summarizes with an LLM when `OPENAI_API_KEY` is set, and writes **only** under `runtime/runtime-worker/` (or `GRACE_MAR_RUNTIME_WORKER_HOME`).

**Not:**

- **Not** SELF, EVIDENCE, SKILLS, MEMORY, or gate truth  
- **Not** a merge path, staging surface, or continuity store  
- **Not** authority for the Voice or companion-facing prompts  

**Artifacts:**

| Output | Path | Rule |
|--------|------|------|
| Proposal | `runtime/runtime-worker/proposals/<run_id>.md` | Operator paste / review; gitignored |
| Trace | `runtime/runtime-worker/traces/index.jsonl` | Append-only audit line per run; gitignored |
| Execution receipt | `runtime/runtime-worker/receipts/<run_id>.json` | One JSON summary per run; links trace + proposal; gitignored; [doc](runtime/execution-receipts.md) |

**Default CI / no-secret posture:** `--dry-run` skips the LLM and still writes proposal + trace (file list and excerpts). No API key required.

**Optional compose:** `--compose-with` runs one allowlisted script and appends bounded stdout:

- `scripts/validate_strategy_expert_threads.py` — `--dir <scope>`
- `scripts/verify_strategy_inbox_accumulator.py` — `--inbox <scope>/daily-strategy-inbox.md`

**Preset lenses (`--lens`):** bundled scope + caps + optional compose; override any field with explicit flags; `--no-compose` drops a lens’s compose step.

| Lens | Scope (default) | Caps | Compose |
|------|-----------------|------|---------|
| `notebook-health` | full strategy-notebook | 400 files / 200k chars | expert-thread validator |
| `inbox-day` | full strategy-notebook | 80 / 80k | inbox Accumulator date check |
| `quick-scan` | full strategy-notebook | 25 / 24k | none |

**Schemas:** `schema-registry/runtime-worker-trace.v1.json` (trace line) · `schema-registry/execution-receipt.v1.json` (per-run receipt, optional `model_policy`)

**Worker routing (optional):** `--task-type` records shared vs routed worker entrypoints under `provenance.worker_routing` on the trace line — see [worker-routing.md](runtime/worker-routing.md).

**Model tier policy (optional):** `--task-subtype` feeds `config/model_routing/task_policy.yaml` into the receipt’s `model_policy` block — see [model-tier-routing.md](runtime/model-tier-routing.md).

**Worker overlays (optional):** `--overlay strategy|moonshot|research|tacit` applies small defaults from [`config/runtime_workers/overlays.yaml`](../config/runtime_workers/overlays.yaml) (explicit CLI wins) — see [worker-overlays.md](runtime/worker-overlays.md).

**Commands:**

```bash
python3 scripts/runtime/grace_mar_runtime_worker.py --task inspect_work_area --dry-run
python3 scripts/runtime/grace_mar_runtime_worker.py --lens notebook-health --dry-run
python3 scripts/runtime/grace_mar_runtime_worker.py --lens inbox-day --dry-run
```

See `runtime/runtime-worker/README.md` for directory layout.
