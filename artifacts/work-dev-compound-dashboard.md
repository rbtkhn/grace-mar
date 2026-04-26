---
derived: true
recordAuthority: none
gateEffect: none
artifact_kind: work_dev_compound_dashboard
---
# Work-Dev Compound Dashboard

> **Boundary:** This dashboard is a derived **WORK** artifact. It does not update
> canonical **Record** surfaces, does not **approve** gate candidates, does not
> write to `recursion-gate.md`, and does not **promote** anything into durable memory.

## 1. Summary

- **Generated (UTC date):** 2026-04-25
- **Total compound notes:** 0
- **Gate-candidate notes (`gate_candidate` truthy):** 0
- **Stale review candidates (>90d, not gate, date or file mtime):** 0
- **Duplicate title groups (normalized, 2+ files):** 0
- **Duplicate `reusable_pattern` groups (normalized, 2+ files):** 0
- **Refresh report artifact:** present
- **Gate-candidate export artifact:** present

## 2. Compound notes inventory

There are **no** compound notes in the configured `compound-notes/` path, or the directory is missing. This is OK — add notes as you complete work.

## 3. Gate-candidate notes

> `gate_candidate: true` (or `yes`, etc.) means **review recommended**, not **approved**.

_(none)_

## 4. Stale review candidates

Notes older than **90** days with `gate_candidate` false. If the front matter `date` is missing, **file mtime** is used for the age check.

_(none)_

## 5. Duplicate hints (not modifications)

Review only; this dashboard does not edit note files.

### Normalized title duplicates

_(none detected)_

### Normalized `reusable_pattern` duplicates

_(none detected)_

## 6. Generated reports (artifacts)

- **work-dev-compound-refresh.md** — present — `artifacts/work-dev-compound-refresh.md` — last modified: 2026-04-26 04:42 UTC
- **work-dev-compound-gate-candidates.md** — present — `artifacts/work-dev-compound-gate-candidates.md` — last modified: 2026-04-26 04:42 UTC
- **work-dev-compound-dashboard.md** — present — `artifacts/work-dev-compound-dashboard.md` — last modified: 2026-04-26 02:39 UTC

## 7. Related work-dev compound docs

- **three-compounding-loops.md** — present — `docs/skill-work/work-dev/three-compounding-loops.md` — Record vs WORK vs CI compounding — mtime: 2026-04-26 01:51 UTC
- **derived-regeneration.md** — present — `docs/skill-work/work-dev/derived-regeneration.md` — Derived regeneration roadmap / rebuildability — mtime: 2026-04-24 16:17 UTC
- **compound-loop.md** — present — `docs/skill-work/work-dev/compound-loop.md` — Compound work loop process and boundary — mtime: 2026-04-26 02:38 UTC
- **compound-gate-export.md** — present — `docs/skill-work/work-dev/compound-gate-export.md` — Gate candidate export — boundary and command — mtime: 2026-04-26 04:41 UTC
- **reviewer-matrix.md** — present — `docs/skill-work/work-dev/reviewer-matrix.md` — Review lenses and promotion rules — mtime: 2026-04-26 01:48 UTC
- **compound-note-template.md** — present — `docs/skill-work/work-dev/compound-note-template.md` — Compound note front matter and sections — mtime: 2026-04-26 01:48 UTC

## 8. Scripts (compound layer)

- **`new_work_dev_compound_note.py`** — present — `scripts/new_work_dev_compound_note.py` — `python3 scripts/new_work_dev_compound_note.py --title "…"`
- **`work_dev_compound_refresh.py`** — present — `scripts/work_dev_compound_refresh.py` — `python3 scripts/work_dev_compound_refresh.py`
- **`export_work_dev_compound_gate_candidates.py`** — present — `scripts/export_work_dev_compound_gate_candidates.py` — `python3 scripts/export_work_dev_compound_gate_candidates.py`
- **`build_work_dev_compound_dashboard.py`** — present — `scripts/build_work_dev_compound_dashboard.py` — `python3 scripts/build_work_dev_compound_dashboard.py`

## 9. Suggested next actions

- After the next completed PR, create the first real compound note: `python3 scripts/new_work_dev_compound_note.py --title "…"`
- After **refresh** or **export** runs, regenerate this dashboard: `python3 scripts/build_work_dev_compound_dashboard.py`

