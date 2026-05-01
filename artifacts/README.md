# Repository artifacts (derived)

This tree holds **rebuildable, non-canonical** outputs from operator scripts. Nothing here is **Record truth**; recovery always points back to source files under `users/`, `docs/`, `skills-portable/`, etc.

**Operator surface taxonomy:** Generated and operator-facing paths are classified in [docs/operator-surface-registry.md](../docs/operator-surface-registry.md). New dashboard-like artifacts should be registered there (and satisfy the **dashboard anti-sprawl policy** there) before being treated as part of the stable operator interface.

**Staleness:** Artifacts are often **generated snapshots**. If a file has **no** generation time or **unclear** source declaration, treat freshness as **unknown** or **possibly stale** and **verify** against the governing source files (e.g. `users/<id>/`, gate file) before relying on it for load-bearing operator decisions. Convention and levels: [docs/operator-surface-staleness.md](../docs/operator-surface-staleness.md).

**Structured-file validation:** Parses committed JSON under `artifacts/` (skipping very large blobs), `schema-registry/`, and workflow examples; validates `pyproject.toml`, `.pre-commit-config.yaml` when PyYAML is available; checks critical relative links in operator/workflow READMEs. Does not change doctrine.

```bash
python scripts/validate_structured_files.py
```

Primary doctrine stays **derived / rebuildable / non-canonical**. If you use `shadow layer` as an informal metaphor for these outputs, treat it as a glossary aid only, not a replacement term. It is **not** the same thing as `shadow-merges`, `shadow autonomy`, or any implied “shadow Record”.

**Important distinction:** the portable-record schema [`schema-registry/artifact-rationale.v1.json`](../schema-registry/artifact-rationale.v1.json) is about **demonstrated capability rationale** alongside EVIDENCE. It is **not** the schema for everything under `/artifacts/`.

Repo-owned derived regeneration may also emit per-artifact rebuild sidecars such as
`artifacts/library-index.md.derived-rationale.json`. Those sidecars follow
[`schema-registry/derived-artifact-rationale.v1.json`](../schema-registry/derived-artifact-rationale.v1.json)
and describe **how to rebuild a derived file**, not why an EVIDENCE artifact was good.

**Repo root `prepared-context/`** (not under `artifacts/`) may hold operator drafts and `last-budget-builds.json`; see [prepared-context/README.md](../prepared-context/README.md) and [context-budgeting.md](../docs/runtime/context-budgeting.md). **Policy mode defaults** (not Record): [`config/policy_modes/defaults.json`](../config/policy_modes/defaults.json), [docs/policy-modes.md](../docs/policy-modes.md).

| Path | Produced by | Policy |
|------|-------------|--------|
| `artifacts/work-notes/` | `scripts/new_work_note.py` | **Scratch** work notes from `docs/templates/work-note-template.md`. **Default:** `*.md` **gitignored**; `.gitkeep` preserves the directory. Not Record. |
| `artifacts/evidence-stubs/` | `scripts/new_evidence_stub.py`, **`scripts/research_to_evidence_stub.py`** | **Pre-canonical** evidence stubs ([README](evidence-stubs/README.md)); **`research_to_evidence_stub`** consumes [`schemas/research-evidence-input.v1.json`](../schemas/research-evidence-input.v1.json); **Default:** gitignored `*.md` like skill-cards. |
| `artifacts/patch-intake/` | **`scripts/coding_agent_patch_intake.py`** | **Candidate-proposal** patch-review packets ([README](patch-intake/README.md)); consumes [`schemas/coding-agent-patch-intake.v1.json`](../schemas/coding-agent-patch-intake.v1.json); **Default:** gitignored `*.md` except README. |
| `artifacts/mcp-admission/` | **`scripts/mcp_manifest_admission.py`** | **Planning-only** MCP manifest admission packets ([README](mcp-admission/README.md)); consumes [`schemas/mcp-server-manifest.v1.json`](../schemas/mcp-server-manifest.v1.json); **Default:** gitignored `*.md` except README + `.gitkeep`. |
| `artifacts/mcp-mock-runs/` | **`scripts/mcp_mock_harness.py`** | **Fixture** MCP-shaped mock-run packets ([README](mcp-mock-runs/README.md)); consumes [`schemas/mcp-mock-run.v1.json`](../schemas/mcp-mock-run.v1.json); **Default:** gitignored `*.md` except README + `.gitkeep`. |
| `artifacts/mcp-local-read/` | **`scripts/mcp_local_readonly.py`** | **Bounded** UTF-8 read packets ([README](mcp-local-read/README.md)); allowlist [`config/mcp-local-read-allowlist.yaml`](../config/mcp-local-read-allowlist.yaml); **Default:** gitignored `*.md` except README + `.gitkeep`. |
| `artifacts/mcp-local-index/` | **`scripts/mcp_local_index.py`** | **Metadata-only** directory index packets ([README](mcp-local-index/README.md)); same allowlist as local read; **Default:** gitignored `*.md` except README + `.gitkeep`. |
| `artifacts/mcp-governance-demo/` | **`scripts/run_mcp_governance_checks.py`** (manual steps in runbook) | **Derived** capability/authority/risk demo outputs under audit prefix ([README](mcp-governance-demo/README.md)); adapter demos use `governance-demo-*` files in standard MCP buckets. |
| `artifacts/mcp-governance-demo-report.md` | **`scripts/run_mcp_governance_checks.py`** | **Aggregated** pass/fail Markdown for the full governance sequence — WORK/runtime only; **Default:** gitignored; see [mcp-governance-runbook.md](../docs/mcp/mcp-governance-runbook.md). |
| `artifacts/mcp-risk-report.md`, `artifacts/mcp-risk-report.json` | **`scripts/mcp_risk_scan.py`** | **Derived** permission-risk scan over [`config/mcp-capabilities.yaml`](../config/mcp-capabilities.yaml) + [`config/mcp-risk-policy.yaml`](../config/mcp-risk-policy.yaml); planning-only; regenerate after registry/policy edits; [docs/mcp/mcp-risk-permission-scanner.md](../docs/mcp/mcp-risk-permission-scanner.md). |
| `artifacts/candidate-drafts/` | `scripts/new_candidate_draft.py` | **Pre-gate** human drafts; does not stage `recursion-gate.md`. **Default:** gitignored `*.md`. |
| `artifacts/skill-cards/` | `scripts/build_skill_cards.py` | **Rebuild** after portable skill edits. **Default:** contents are **gitignored** (see repo `.gitignore`); only `.gitkeep` preserves the directory. Optional CI snapshots if you want diff review. |
| `artifacts/context/` | `scripts/compress_active_lane.py` | **Ephemeral operator memos** with source paths. **Default:** gitignored except `.gitkeep`. Regenerate as needed; not a substitute for lane READMEs or `self-work.md`. |
| `artifacts/work-dev/interface-artifacts/` | operator or future tooling | **Derived** interface artifacts and metadata for cross-lane prototypes; WORK-only, non-canonical, delete/regenerate as needed. Prefer lane-specific buckets when a lane already has one. |
| `artifacts/work-dev/rebuild-receipts/` | `scripts/regenerate_all_derived.py` | **Derived** receipts for repo-owned regeneration runs. Tracks changed paths, selected targets, and run status; not Record, not gate authority. |
| `artifacts/work-dev/derived-regeneration-manifest.json` | `scripts/build_derived_regeneration_manifest.py` | **Derived** manifest for repo-owned rebuild targets, watch patterns, outputs, and dependencies. Not Record; supports incremental regeneration. |
| `artifacts/work-dev/rebuild-health/` | `scripts/report_rebuild_health.py` | **Derived** rebuild-health telemetry from rebuild receipts and the regeneration manifest. Operator observability only; not Record truth. |
| `artifacts/observability/work-coffee/conductor-eval/` | **`scripts/run_conductor_eval_harness.py`** | **Derived** Conductor MCQ metrics JSON ([schema](../schema-registry/conductor-session-metrics.v1.json)); default `*.json` gitignored — [bucket README](observability/work-coffee/conductor-eval/README.md), [doc](../docs/skill-work/work-coffee/conductor-observability.md). |
| `artifacts/work-strategy/strategy-notebook/` | `scripts/strategy_page.py`, `scripts/compile_strategy_view.py`, `scripts/build_strategy_notebook_graph.py` | **Derived** JSONL receipts, `graph.json`, and `views/` for the strategy-notebook lane — not SSOT; see [work-strategy/strategy-notebook/README.md](work-strategy/strategy-notebook/README.md), [docs/runtime-vs-record.md](../docs/runtime-vs-record.md). |
| `artifacts/strategy-runs/`, `artifacts/run-receipts/` | `scripts/strategy_run.py` | **Derived** per-run `state.json` and event receipts — session envelope for work-strategy, not SSOT; see [STRATEGY-RUN-ARCHITECTURE.md](../docs/skill-work/work-strategy/STRATEGY-RUN-ARCHITECTURE.md), [docs/run-contract.md](../docs/run-contract.md). |
| `artifacts/strategy-run-report.md` | `scripts/build_strategy_run_report.py` | **Derived** markdown table of recent runs; delete and rebuild. |
| `artifacts/library-index.md` | `scripts/build_library_index.py` | **Derived** scan-first dashboard (at-a-glance, Start here, recent, compact by lane + appendix inventory) from `users/<id>/self-library.md` entries YAML — not SELF-LIBRARY truth; regenerate after library edits. See [docs/operator-dashboards.md](../docs/operator-dashboards.md). |
| `artifacts/lane-dashboards/README.md` | `scripts/build_lane_dashboards.py` | **Derived** lane/runtime snapshot (+ optional `work-lanes-dashboard.json`). Not canonical. |
| `artifacts/memory/memory-observability.md`, `artifacts/memory/memory-observability.json` | `scripts/build_memory_observability.py` | **Derived** continuity observability over cadence and handoff surfaces. Not Record, not MEMORY, and not a coffee/dream hook. |
| `artifacts/review-dashboard.md` | `scripts/build_review_dashboard.py` | **Derived** view of `recursion-gate.md` — does not replace the gate file. |
| `artifacts/governance-posture.md` | `scripts/report_governance_posture.py` | **Derived** operator/partner one-pager (triad, gate, audit paths, verification commands) — not Record, not legal advice; [safety-story-ux.md](../docs/skill-work/work-dev/safety-story-ux.md). Regenerate after policy changes. |
| `artifacts/mcp-capability-report.md` | `scripts/mcp_capability_audit.py` | **Derived** audit table + danger-flag heuristics over [`config/mcp-capabilities.yaml`](../config/mcp-capabilities.yaml); planning-only; [docs/mcp/governed-mcp-layer.md](../docs/mcp/governed-mcp-layer.md). Regenerate after registry edits. |
| `artifacts/mcp-authority-report.md` | `scripts/mcp_authority_check.py` | **Derived** lane ↔ authority-map cross-check over [`config/mcp-authority-bindings.yaml`](../config/mcp-authority-bindings.yaml) + registry + [`config/authority-map.json`](../config/authority-map.json); planning-only; [docs/mcp/mcp-authority-bindings.md](../docs/mcp/mcp-authority-bindings.md). Regenerate after bindings or map edits. |
| `artifacts/mcp-receipts/` | `scripts/mcp_receipt.py` | **Derived** MCP governance receipt JSON (audit metadata); WORK/runtime only; not Record — see [mcp-receipts/README.md](mcp-receipts/README.md), [docs/mcp/mcp-execution-receipts.md](../docs/mcp/mcp-execution-receipts.md). Optional committed examples under version control. |
| `artifacts/mcp-receipt-report.md` | `scripts/mcp_receipt_audit.py` | **Derived** validation summary over `artifacts/mcp-receipts/*.json`; regenerate after receipt edits. |
| `artifacts/gate-board.md` | `scripts/build_gate_board.py` | **Kanban-style** candidate/review snapshot — not authoritative; [docs/gate-board.md](../docs/gate-board.md). |
| `artifacts/work-lanes-dashboard.json` | `scripts/build_work_lanes_dashboard.py` | **WORK** telemetry aggregate; input to lane dashboard script. |
| `artifacts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast artifact JSON** + optional `.summary.md` — WORK-layer; [policy](forecast/README.md), [lane](../docs/skill-work/work-forecast/README.md). |
| `artifacts/receipts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast run receipts** — legibility only; [policy](receipts/forecast/README.md). |
| `artifacts/uncertainty-reports/` | _(optional)_ operator / CI | **Optional** sidecars for uncertainty envelope JSON — not Record; [folder README](uncertainty-reports/README.md). |
| `artifacts/review-packets/` | `scripts/runtime/review_orchestrator.py` | **Optional** Markdown review packets (`--output`; **`--task-anchor` required**) — not Record; [folder README](review-packets/README.md). |
| `artifacts/shadow-merges/` | `scripts/runtime/shadow_merge_simulator.py` | **Optional** Markdown shadow-merge preview reports (`--output`) — not Record; [folder README](shadow-merges/README.md), [doc](../docs/orchestration/shadow-merge-simulator.md). |
| `artifacts/classification-reports/` | `scripts/runtime/surface_misclassification_detector.py` | **Optional** Markdown surface-classification risk reports (`--output`) — advisory, not Record; [folder README](classification-reports/README.md), [doc](../docs/orchestration/surface-misclassification-detector.md). |
| `artifacts/route-recommendations/` | `scripts/recommend_route.py` | **Advisory** task-to-lane heuristic receipts (markdown); derived, gitignored defaults; see [bucket README](route-recommendations/README.md), [doc](../docs/route-recommendation.md). |
| `artifacts/skill-evals/` | `scripts/runtime/skill_eval_clinic.py` | **Optional** JSON/Markdown skill evaluation clinic reports — derived, not canonical skills; [skill-evaluation-clinic.md](../docs/skill-work/work-dev/skill-evaluation-clinic.md). |
| `artifacts/context-failure-reports/` | `scripts/runtime/context_failure_clinic.py` | **Optional** JSON/Markdown context-failure diagnostic reports — derived; [context-failure-diagnostics-clinic.md](../docs/runtime/context-failure-diagnostics-clinic.md). |
| `artifacts/example-context-output.md` | _(fixture)_ | Non-canonical sample Markdown for clinic docs and manual CLI runs (not Record). |
| `artifacts/external-codex/` | **`scripts/build_external_codex_neighborhood.py`**, **`scripts/build_external_codex_family_report.py`** | **Derived** structural neighborhood **JSON** / optional **`.neighborhood.md`** (single subject); **family** JSON / optional **`.family.md`** (cluster by selector); schemas [`external-codex-neighborhood-report.v1.json`](../schema-registry/external-codex-neighborhood-report.v1.json), [`external-codex-family-report.v1.json`](../schema-registry/external-codex-family-report.v1.json); [bucket README](external-codex/README.md), [doc](../docs/skill-work/work-dev/external-codex-explorer.md); **Default outputs** gitignored — committed **`examples/`** only. |
| `artifacts/handoffs/` | `checkpoint_session.py`, `build_handoff_packet.py` | **Runtime** session checkpoints and handoff packets — not Record; [folder README](handoffs/README.md), [long-horizon doctrine](../docs/runtime/long-horizon-work.md). |
| `prepared-context/last-budget-builds.json` | `build_budgeted_context.py` | **Optional** per-lane receipt for last budgeted build (repo root); see [context-budgeting.md](../docs/runtime/context-budgeting.md). |

**Companion-specific large blobs** (e.g. under `users/<id>/artifacts/`) follow separate rules in `.gitignore` and instance docs — not this folder.

## Regeneration contract

For the current repo-owned target set, use:

```bash
python3 scripts/regenerate_all_derived.py --changed --dry-run
python3 scripts/regenerate_all_derived.py --all
```

That flow writes three distinct non-canonical metadata families:

- **Rebuild receipts** under `artifacts/work-dev/rebuild-receipts/` — one receipt per regeneration run
- **Target manifest** at `artifacts/work-dev/derived-regeneration-manifest.json` — the declared target registry
- **Derived-artifact rationale sidecars** next to covered outputs — one sidecar per rebuilt artifact path

## Derived-artifact rationale sidecars

Sidecar naming is intentionally literal:

- `artifacts/library-index.md`
- `artifacts/library-index.md.derived-rationale.json`

The sidecar records rebuild provenance only:

- `producer_script`
- `policy_mode`
- `generated_at`
- `artifact_path`
- `canonical_surfaces_touched` (always `false`)
- `rebuild_command`
- `inputs`
- `rationale`
- `human_review_required`

Schema: [`schema-registry/derived-artifact-rationale.v1.json`](../schema-registry/derived-artifact-rationale.v1.json)

## Cleanup rule

Derived regeneration is **target-owned**, not whole-tree destructive:

- single-file outputs are overwritten by their producer scripts
- directory cleanup is allowed only for files explicitly owned by the selected rebuild target
- `.gitkeep` and unrelated artifact families must be preserved

This is why repo-owned regeneration stays narrower than “delete all of `/artifacts/` and hope.”

See also: [docs/skills/skill-card-spec.md](../docs/skills/skill-card-spec.md), [docs/skill-work/active-lane-compression.md](../docs/skill-work/active-lane-compression.md), [docs/operator-dashboards.md](../docs/operator-dashboards.md) (Library / lane / review Markdown dashboards).
