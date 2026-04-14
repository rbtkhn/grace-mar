# Surface Misclassification Detector

**Script:** [`scripts/runtime/surface_misclassification_detector.py`](../../scripts/runtime/surface_misclassification_detector.py)

## Invocation contract

| Field | Value |
|-------|--------|
| **Surface type** | Workflow / operator tooling (read-only) |
| **Primary purpose** | Assess whether a proposal appears to target the wrong Grace-Mar **canonical surface** |
| **When to use** | Before approving or heavily editing a candidate whose surface placement feels uncertain |
| **Inputs** | `--candidate CANDIDATE-NNNN` (pending block in `users/<id>/recursion-gate.md`), `--proposal-file` (schema-aligned JSON), or direct proposal (`--target-surface` + `--proposal-summary` + `--proposed-change`) |
| **Outputs** | A Markdown **Classification Risk Report** under `artifacts/classification-reports/` (default) or `--output` |
| **Mutation scope** | Writes **only** the report file. No gate merge, no Record writes. |
| **Canonical Record access** | Read-only gate + optional JSON; no gate-state mutation |
| **Typical next step** | Operator review, surface reclassification, or [Shadow Merge Simulator](shadow-merge-simulator.md) for consequence preview |
| **Do not use for** | Auto-rerouting, auto-approval, or replacing companion gate review |

## Why this exists

Grace-Mar depends on clear distinctions between:

- **SELF** — identity and self-knowledge  
- **SELF-LIBRARY** — governed reference and return-to sources  
- **SKILLS** — capability  
- **EVIDENCE** — activity and artifacts  
- **WORK_LAYER** (heuristic) — exploratory or under-evidenced material that should not yet be treated as durable Record

A proposal can be plausible and still be **mis-aimed** at the wrong ontological surface.

## Live repo integration

- **Canonical inbox:** `users/<id>/recursion-gate.md` via [`parse_review_candidates`](../../scripts/recursion_gate_review.py) — **not** a repo-root `recursion-gate.md`.
- When a gate row is loaded, optional **`boundary_review`** (misfile hints from [`recursion_gate_review.py`](../../scripts/recursion_gate_review.py)) is included in the report.

## What it does

The detector emits a report with:

- claimed vs predicted surface (signal scores including optional **WORK_LAYER**)
- risk level and recommendation (advisory)
- defensibility checklist
- operator question

## What it does not do

- It does **not** rewrite `target_surface` in the gate.
- It does **not** mutate canonical Record files.
- It does **not** change gate status.
- It does **not** replace operator judgment.

## Example usage

```bash
python scripts/runtime/surface_misclassification_detector.py \
  -u grace-mar \
  --candidate CANDIDATE-0042 \
  -o artifacts/classification-reports/CANDIDATE-0042.md
```

Default output when `-o` is omitted: `artifacts/classification-reports/<proposal-id>.md`.

**Direct text (no gate):**

```bash
python scripts/runtime/surface_misclassification_detector.py \
  --target-surface SELF \
  --proposal-summary "Add Roman continuity preference" \
  --proposed-change "Treat Roman imperial continuity as a governed reference tradition for future synthesis." \
  -o artifacts/classification-reports/roman-preview.md
```

## Pairing with Shadow Merge

| Tool | Question |
|------|----------|
| **Surface Misclassification Detector** | Am I aiming this at the right **ontological** place? |
| [Shadow Merge Simulator](shadow-merge-simulator.md) | What **happens** if I approve it there anyway? |

## Boundary reminder

Misclassification is a **governance** issue in Grace-Mar, not only a filing issue. This tool is **advisory**; durable changes remain **gated** per [AGENTS.md](../../AGENTS.md) and [`docs/runtime-vs-record.md`](../runtime-vs-record.md).
