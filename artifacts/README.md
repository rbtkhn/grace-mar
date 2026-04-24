# Repository artifacts (derived)

This tree holds **rebuildable, non-canonical** outputs from operator scripts. Nothing here is **Record truth**; recovery always points back to source files under `users/`, `docs/`, `skills-portable/`, etc.

Primary doctrine stays **derived / rebuildable / non-canonical**. If you use `shadow layer` as an informal metaphor for these outputs, treat it as a glossary aid only, not a replacement term. It is **not** the same thing as `shadow-merges`, `shadow autonomy`, or any implied “shadow Record”.

**Important distinction:** the portable-record schema [`schema-registry/artifact-rationale.v1.json`](../schema-registry/artifact-rationale.v1.json) is about **demonstrated capability rationale** alongside EVIDENCE. It is **not** the schema for everything under `/artifacts/`.

**Repo root `prepared-context/`** (not under `artifacts/`) may hold operator drafts and `last-budget-builds.json`; see [prepared-context/README.md](../prepared-context/README.md) and [context-budgeting.md](../docs/runtime/context-budgeting.md). **Policy mode defaults** (not Record): [`config/policy_modes/defaults.json`](../config/policy_modes/defaults.json), [docs/policy-modes.md](../docs/policy-modes.md).

| Path | Produced by | Policy |
|------|-------------|--------|
| `artifacts/work-notes/` | `scripts/new_work_note.py` | **Scratch** work notes from `docs/templates/work-note-template.md`. **Default:** `*.md` **gitignored**; `.gitkeep` preserves the directory. Not Record. |
| `artifacts/evidence-stubs/` | `scripts/new_evidence_stub.py` | **Pre-canonical** evidence stubs. **Default:** gitignored `*.md` like skill-cards. |
| `artifacts/candidate-drafts/` | `scripts/new_candidate_draft.py` | **Pre-gate** human drafts; does not stage `recursion-gate.md`. **Default:** gitignored `*.md`. |
| `artifacts/skill-cards/` | `scripts/build_skill_cards.py` | **Rebuild** after portable skill edits. **Default:** contents are **gitignored** (see repo `.gitignore`); only `.gitkeep` preserves the directory. Optional CI snapshots if you want diff review. |
| `artifacts/context/` | `scripts/compress_active_lane.py` | **Ephemeral operator memos** with source paths. **Default:** gitignored except `.gitkeep`. Regenerate as needed; not a substitute for lane READMEs or `self-work.md`. |
| `artifacts/work-dev/interface-artifacts/` | operator or future tooling | **Derived** interface artifacts and metadata for cross-lane prototypes; WORK-only, non-canonical, delete/regenerate as needed. Prefer lane-specific buckets when a lane already has one. |
| `artifacts/work-dev/rebuild-receipts/` | `scripts/regenerate_all_derived.py` | **Derived** receipts for repo-owned regeneration runs. Tracks changed paths, selected targets, and run status; not Record, not gate authority. |
| `artifacts/work-dev/derived-regeneration-manifest.json` | `scripts/build_derived_regeneration_manifest.py` | **Derived** manifest for repo-owned rebuild targets, watch patterns, outputs, and dependencies. Not Record; supports incremental regeneration. |
| `artifacts/work-dev/rebuild-health/` | `scripts/report_rebuild_health.py` | **Derived** rebuild-health telemetry from rebuild receipts and the regeneration manifest. Operator observability only; not Record truth. |
| `artifacts/work-strategy/strategy-notebook/` | `scripts/strategy_page.py`, `scripts/compile_strategy_view.py`, `scripts/build_strategy_notebook_graph.py` | **Derived** JSONL receipts, `graph.json`, and `views/` for the strategy-notebook lane — not SSOT; see [work-strategy/strategy-notebook/README.md](work-strategy/strategy-notebook/README.md), [docs/runtime-vs-record.md](../docs/runtime-vs-record.md). |
| `artifacts/strategy-runs/`, `artifacts/run-receipts/` | `scripts/strategy_run.py` | **Derived** per-run `state.json` and event receipts — session envelope for work-strategy, not SSOT; see [STRATEGY-RUN-ARCHITECTURE.md](../docs/skill-work/work-strategy/STRATEGY-RUN-ARCHITECTURE.md), [docs/run-contract.md](../docs/run-contract.md). |
| `artifacts/strategy-run-report.md` | `scripts/build_strategy_run_report.py` | **Derived** markdown table of recent runs; delete and rebuild. |
| `artifacts/library-index.md` | `scripts/build_library_index.py` | **Derived** scan-first dashboard (at-a-glance, Start here, recent, compact by lane + appendix inventory) from `users/<id>/self-library.md` entries YAML — not SELF-LIBRARY truth; regenerate after library edits. See [docs/operator-dashboards.md](../docs/operator-dashboards.md). |
| `artifacts/lane-dashboards/README.md` | `scripts/build_lane_dashboards.py` | **Derived** lane/runtime snapshot (+ optional `work-lanes-dashboard.json`). Not canonical. |
| `artifacts/review-dashboard.md` | `scripts/build_review_dashboard.py` | **Derived** view of `recursion-gate.md` — does not replace the gate file. |
| `artifacts/governance-posture.md` | `scripts/report_governance_posture.py` | **Derived** operator/partner one-pager (triad, gate, audit paths, verification commands) — not Record, not legal advice; [safety-story-ux.md](../docs/skill-work/work-dev/safety-story-ux.md). Regenerate after policy changes. |
| `artifacts/gate-board.md` | `scripts/build_gate_board.py` | **Kanban-style** candidate/review snapshot — not authoritative; [docs/gate-board.md](../docs/gate-board.md). |
| `artifacts/work-lanes-dashboard.json` | `scripts/build_work_lanes_dashboard.py` | **WORK** telemetry aggregate; input to lane dashboard script. |
| `artifacts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast artifact JSON** + optional `.summary.md` — WORK-layer; [policy](forecast/README.md), [lane](../docs/skill-work/work-forecast/README.md). |
| `artifacts/receipts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast run receipts** — legibility only; [policy](receipts/forecast/README.md). |
| `artifacts/uncertainty-reports/` | _(optional)_ operator / CI | **Optional** sidecars for uncertainty envelope JSON — not Record; [folder README](uncertainty-reports/README.md). |
| `artifacts/review-packets/` | `scripts/runtime/review_orchestrator.py` | **Optional** Markdown review packets (`--output`; **`--task-anchor` required**) — not Record; [folder README](review-packets/README.md). |
| `artifacts/shadow-merges/` | `scripts/runtime/shadow_merge_simulator.py` | **Optional** Markdown shadow-merge preview reports (`--output`) — not Record; [folder README](shadow-merges/README.md), [doc](../docs/orchestration/shadow-merge-simulator.md). |
| `artifacts/classification-reports/` | `scripts/runtime/surface_misclassification_detector.py` | **Optional** Markdown surface-classification risk reports (`--output`) — advisory, not Record; [folder README](classification-reports/README.md), [doc](../docs/orchestration/surface-misclassification-detector.md). |
| `artifacts/handoffs/` | `checkpoint_session.py`, `build_handoff_packet.py` | **Runtime** session checkpoints and handoff packets — not Record; [folder README](handoffs/README.md), [long-horizon doctrine](../docs/runtime/long-horizon-work.md). |
| `prepared-context/last-budget-builds.json` | `build_budgeted_context.py` | **Optional** per-lane receipt for last budgeted build (repo root); see [context-budgeting.md](../docs/runtime/context-budgeting.md). |

**Companion-specific large blobs** (e.g. under `users/<id>/artifacts/`) follow separate rules in `.gitignore` and instance docs — not this folder.

See also: [docs/skills/skill-card-spec.md](../docs/skills/skill-card-spec.md), [docs/skill-work/active-lane-compression.md](../docs/skill-work/active-lane-compression.md), [docs/operator-dashboards.md](../docs/operator-dashboards.md) (Library / lane / review Markdown dashboards).
