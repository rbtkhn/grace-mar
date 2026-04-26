# Compound gate candidate export (work-dev)

**Purpose:** Produce a **single read-only markdown file** that aggregates the text of compound notes whose front matter sets `gate_candidate` to a truthy value (`true`, `yes`, and common string forms — see `gate_candidate_truthy` in `scripts/work_dev/compound_notes.py`).

**Boundary:** This export is **not** canonical memory. It is a **staging aid** for review. It does **not** approve anything, does **not** write to the Record, SELF, SKILLS, EVIDENCE, the Library, or `users/grace-mar/recursion-gate.md`, and it does **not** merge or promote by itself. **Repetition in the export is not approval.**

## Relation to other artifacts

- **`python3 scripts/work_dev_compound_refresh.py`** — inventory, staleness heuristics, and duplicate-title hints; output: `artifacts/work-dev-compound-refresh.md`. Summarized **metadata**, not the full text of every candidate section.
- **`python3 scripts/export_work_dev_compound_gate_candidates.py`** — this document’s script — assembles **per-note blocks** (reusable pattern/lesson, gate recommendation) for **human review** of items flagged as gate candidates. Still **no merge**; use the normal companion / gate flow when you choose to **stage** something.

If you need to **stage** a candidate into the existing gate pipeline, use the project’s **companion** and **stage** scripts (e.g. `scripts/stage_gate_candidate.py` where appropriate) **manually**; this export does **not** call those scripts for you.

## Workflow

1. Author or update compound notes under `docs/skill-work/work-dev/compound-notes/`.
2. Set `gate_candidate: true` (or `yes`) in front matter when a note is meant as a **recommendation** for gate review, not a silent promotion.
3. Run `python3 scripts/export_work_dev_compound_gate_candidates.py` (default output: `artifacts/work-dev-compound-gate-candidates.md`).
4. Use `--include-all` to list every valid note, each with an explicit `gate_candidate: true|false` line.
5. Open the generated markdown and review `### Reusable pattern`, `### Reusable lesson`, and `### Gate recommendation` in context.
6. If promoting, follow the **normal** governed gate / companion process; treat `### Proposed staging disposition` in the export as a fixed reminder: **manual review, no auto-promote**.

## Warning

A note’s appearance in the export (or a high count of `gate_candidate` flags across sessions) is **not** the same as companion **approval** or **merge**. The gate remains the only durable promotion path for Record-related change.

## Command reference

| Flag | Meaning |
|------|---------|
| `--notes-dir` | Override the compound notes directory (default: `docs/skill-work/work-dev/compound-notes`). |
| `--output` | Override output path (default: `artifacts/work-dev-compound-gate-candidates.md`). Paths are resolved relative to the repo root when not absolute. |
| `--include-all` | Include every valid note, with a visible `gate_candidate` line in each block. |
