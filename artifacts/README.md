# Repository artifacts (derived)

This tree holds **rebuildable, non-canonical** outputs from operator scripts. Nothing here is **Record truth**; recovery always points back to source files under `users/`, `docs/`, `skills-portable/`, etc.

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

**Companion-specific large blobs** (e.g. under `users/<id>/artifacts/`) follow separate rules in `.gitignore` and instance docs — not this folder.

See also: [docs/skills/skill-card-spec.md](../docs/skills/skill-card-spec.md), [docs/skill-work/active-lane-compression.md](../docs/skill-work/active-lane-compression.md), [docs/operator-dashboards.md](../docs/operator-dashboards.md) (Library / lane / review Markdown dashboards).
