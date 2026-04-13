# Repository artifacts (derived)

This tree holds **rebuildable, non-canonical** outputs from operator scripts. Nothing here is **Record truth**; recovery always points back to source files under `users/`, `docs/`, `skills-portable/`, etc.

| Path | Produced by | Policy |
|------|-------------|--------|
| `artifacts/skill-cards/` | `scripts/build_skill_cards.py` | **Rebuild** after portable skill edits. **Default:** contents are **gitignored** (see repo `.gitignore`); only `.gitkeep` preserves the directory. Optional CI snapshots if you want diff review. |
| `artifacts/context/` | `scripts/compress_active_lane.py` | **Ephemeral operator memos** with source paths. **Default:** gitignored except `.gitkeep`. Regenerate as needed; not a substitute for lane READMEs or `self-work.md`. |
| `artifacts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast artifact JSON** + optional `.summary.md` — WORK-layer; [policy](forecast/README.md), [lane](../docs/skill-work/work-forecast/README.md). |
| `artifacts/receipts/forecast/` | `scripts/run_forecast_baselines.py` | **Forecast run receipts** — legibility only; [policy](receipts/forecast/README.md). |

**Companion-specific large blobs** (e.g. under `users/<id>/artifacts/`) follow separate rules in `.gitignore` and instance docs — not this folder.

See also: [docs/skills/skill-card-spec.md](../docs/skills/skill-card-spec.md), [docs/skill-work/active-lane-compression.md](../docs/skill-work/active-lane-compression.md).
