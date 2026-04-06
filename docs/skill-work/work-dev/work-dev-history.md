# work-dev-history — operator log

> **Append-only** log for the **work-dev** territory (OpenClaw, integration, exports, harness, transcripts). **Not** Record truth; **not** companion [self-memory](../../../users/grace-mar/self-memory.md). **Rotatable** — prune older sections when the file grows.

**Distinct from:** [work-dev-sources.md](work-dev-sources.md) (authorized sources only). **Operator rhythm:** [coffee](../../../.cursor/skills/coffee/SKILL.md) (**`coffee`**; legacy **`hey`** still works). **Per-lane log:** this file — [work-modules-history-principle.md](../work-modules-history-principle.md).

## How to append

- Use **`## YYYY-MM-DD`**; **`### Session 2`** (or UTC time) if multiple blocks the same day.
- **Scope:** integration steps, digest ingests, staging/merge protocol notes, CI/harness changes, cross-repo handbacks — **this lane only**.
- **Prefer:** one line per artifact (path, commit SHA, brief outcome).

## Log

_(Append below this line.)_

- **2026-04-06** — Positioning doc from external six-layer agent-infrastructure analysis: `positioning-governed-state-os.md` — "governed state OS" framing, companion-first vs infrastructure-first fork, gap map, accepted framings; README contents row added. Three actionable gaps added to `known-gaps.md`: GAP-008 (capability contracts), GAP-009 (compute ledger per-task cost), GAP-010 (sandbox adapter layer); triage note with six-layer priority order.
- **2026-04-06** — GAP-008 closed: capability contract template (`control-plane/capability-contract-template.yaml`) + two retrofits (`capability-contract-openclaw-export.yaml`, `capability-contract-openclaw-stage.yaml`) + `--validate-contracts` CLI wired into `agent_surface_checklist.py`. README index rows added. GAP-008 status → `implemented`.
- **2026-04-06** — GAP-009 closed: `emit_compute_ledger.py` extended with `task_id`, `task_type`, `outcome_confidence` (clamped 0–1, optional); `scripts/compute_ledger_summary.py` rollup (group by bucket/operation/task_type/task_id/date/model, `--since`, `--json`); three new tests. `economic-benchmarks.md` updated. GAP-009 status → `implemented`.
- **2026-04-06** — GAP-010 closed: `sandbox-adapter-spec.md` (spec) + `scripts/work_dev/sandbox_adapter.py` (adapter core + DryRunBackend + LocalDockerBackend stub). Authority check, pre/post pipeline receipts, compute-ledger row, backend registry. CLI: `sandbox_adapter.py --backend dry_run --command "…"`. 15 tests (`tests/test_sandbox_adapter.py`). GAP-010 status → `implemented`.
- **2026-04-06** — Wired `task_type` into all four `append_integration_ledger` callers: `openclaw_hook.py` (export), `openclaw_stage.py` (stage), `handback_server.py` (handback), `export_runtime_bundle.py` (export). New ledger rows carry task context for `--by task_type` summary grouping.
- **2026-04-06** — Capability contracts for sandbox backends: `capability-contract-sandbox-dry-run.yaml` (active), `capability-contract-sandbox-docker.yaml` (planned). Updated openclaw-export and openclaw-stage contracts with `task_type` receipt info. All 4 contracts validate.
- **2026-04-04** — Agent memory PostgreSQL/pgvector spec and v1 migration: `agent-memory-pgvector-spec.md`, `sql/agent_memory_v1_initial.sql`; README contents row (flaw-fix plan implementation).
- **2026-03-30** — Added Huang / Lex #494 digest and OpenClaw/Grace-Mar diff: `research/external/work-dev/transcripts/lex-fridman-494-jensen-huang-DIGEST.md`; README index row; commits through `51de012` (operator thread).
