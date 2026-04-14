# Repository artifacts (derived)

This tree holds **rebuildable, non-canonical** outputs from operator scripts. Nothing here is **Record truth**; recovery always points back to source files under `users/`, `docs/`, `skills-portable/`, etc.

**Repo root `prepared-context/`** (not under `artifacts/`) may hold operator drafts and `last-budget-builds.json`; see [prepared-context/README.md](../prepared-context/README.md) and [context-budgeting.md](../docs/runtime/context-budgeting.md). **Policy mode defaults** (not Record): [`config/policy_modes/defaults.json`](../config/policy_modes/defaults.json), [docs/policy-modes.md](../docs/policy-modes.md).

| Path | Produced by | Policy |
|------|-------------|--------|
| `artifacts/work-notes/` | `scripts/new_work_note.py` | **Scratch** work notes from `docs/templates/work-note-template.md`. **Default:** `*.md` **gitignored**; `.gitkeep` preserves the directory. Not Record. |
| `artifacts/evidence-stubs/` | `scripts/new_evidence_stub.py` | **Pre-canonical** evidence stubs. **Default:** gitignored `*.md` like skill-cards. |
| `artifacts/candidate-drafts/` | `scripts/new_candidate_draft.py` | **Pre-gate** human drafts; does not stage `recursion-gate.md`. **Default:** gitignored `*.md`. |
| `artifacts/skill-cards/` | `scripts/build_skill_cards.py` | **Rebuild** after portable skill edits. **Default:** contents are **gitignored** (see repo `.gitignore`); only `.gitkeep` preserves the directory. Optional CI snapshots if you want diff review. |
| `artifacts/context/` | `scripts/compress_active_lane.py` | **Ephemeral operator memos** with source paths. **Default:** gitignored except `.gitkeep`. Regenerate as needed; not a substitute for lane READMEs or `self-work.md`. |
| `artifacts/library-index.md` | `scripts/build_library_index.py` | **Derived** Library overview from `users/<id>/self-library.md` entries YAML — not SELF-LIBRARY truth; regenerate after library edits. See [docs/operator-dashboards.md](../docs/operator-dashboards.md). |
| `artifacts/lane-dashboards/README.md` | `scripts/build_lane_dashboards.py` | **Derived** lane/runtime snapshot (+ optional `work-lanes-dashboard.json`). Not canonical. |
| `artifacts/review-dashboard.md` | `scripts/build_review_dashboard.py` | **Derived** view of `recursion-gate.md` — does not replace the gate file. |
| `artifacts/gate-board.md` | `scripts/build_gate_board.py` | **Kanban-style** candidate/review snapshot — not authoritative; [docs/gate-board.md](../docs/gate-board.md). |
| `artifacts/work-lanes-dashboard.json` | `scripts/build_work_lanes_dashboard.py` | **WORK** telemetry aggregate; input to lane dashboard script. |
| `artifacts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast artifact JSON** + optional `.summary.md` — WORK-layer; [policy](forecast/README.md), [lane](../docs/skill-work/work-forecast/README.md). |
| `artifacts/receipts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast run receipts** — legibility only; [policy](receipts/forecast/README.md). |
| `artifacts/uncertainty-reports/` | _(optional)_ operator / CI | **Optional** sidecars for uncertainty envelope JSON — not Record; [folder README](uncertainty-reports/README.md). |
| `artifacts/review-packets/` | `scripts/runtime/review_orchestrator.py` | **Optional** Markdown review packets (`--output`) — not Record; [folder README](review-packets/README.md). |
| `artifacts/handoffs/` | `checkpoint_session.py`, `build_handoff_packet.py` | **Runtime** session checkpoints and handoff packets — not Record; [folder README](handoffs/README.md), [long-horizon doctrine](../docs/runtime/long-horizon-work.md). |
| `prepared-context/last-budget-builds.json` | `build_budgeted_context.py` | **Optional** per-lane receipt for last budgeted build (repo root); see [context-budgeting.md](../docs/runtime/context-budgeting.md). |

**Companion-specific large blobs** (e.g. under `users/<id>/artifacts/`) follow separate rules in `.gitignore` and instance docs — not this folder.

See also: [docs/skills/skill-card-spec.md](../docs/skills/skill-card-spec.md), [docs/skill-work/active-lane-compression.md](../docs/skill-work/active-lane-compression.md), [docs/operator-dashboards.md](../docs/operator-dashboards.md) (Library / lane / review Markdown dashboards).
