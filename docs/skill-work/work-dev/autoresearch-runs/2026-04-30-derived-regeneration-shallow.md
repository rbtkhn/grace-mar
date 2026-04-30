# Autoresearch Run Note: Derived Regeneration Shallow Edges

**Status:** WORK-layer dry run artifact. **Not** Record truth. **Not** approval.

## Run Metadata

| Field | Value |
|-------|-------|
| **Date** | 2026-04-30 |
| **Lane** | work-dev |
| **Hypothesis / question** | Where is derived regeneration still shallow? |
| **Mode** | discovery |
| **Success metric** | Identify one inspectable next wedge from existing docs without running regeneration commands. |
| **Proxy metric** | A next wedge is useful if it has a named source, target, dry-run check, and stop condition. |
| **Baseline** | `derived-regeneration.md` says Phase 1 is intentionally small and runtime rebuild requests are deferred. |
| **Time budget** | One bounded documentation pass. |
| **Operator** | Codex / Kleiber dry run |
| **Log path** | This file |
| **Trajectory / state artifact** | `docs/skill-work/work-dev/derived-regeneration.md` |
| **Source skill reference** | Orchestra Research Autoresearch used as WORK reference only |

## Source List

| Source | Why it matters | Checked date |
|--------|----------------|--------------|
| `docs/skill-work/work-dev/derived-regeneration.md` | Contract, current target set, roadmap, guardrails. | 2026-04-30 |
| `docs/skill-work/work-dev/workspace.md` | Current work-dev state and derived-regeneration blocker summary. | 2026-04-30 |
| `docs/skill-work/work-dev/research-orchestra-ai-research-skills.md` | Autoresearch adapter boundary and proof bar. | 2026-04-30 |

## Findings

What did the run find?

- The shallow edge is not the existence of regeneration scripts; those already exist. The shallow edge is target coverage and incremental confidence: `derived-regeneration.md` names the current set as small and says expansion should happen only where source -> artifact mapping is clear.
- The most useful next wedge is to choose one additional derived target and prove the full sequence: register target, confirm change detector inputs, run changed incremental dry-run, then decide whether it becomes live.
- Runtime-triggered rebuild requests should remain deferred. The docs explicitly say they come later, after local target coverage and receipts are stable.

Result label:

- exploratory

## Experiment Protocol Summary

| Field | Value |
|-------|-------|
| **Prediction** | The next weakness would be target coverage rather than missing scripts. |
| **Why this test** | It tests whether the Autoresearch packet can convert a broad question into one bounded work-dev wedge. |
| **Measurement** | One source-backed next wedge with stop condition and no status inflation. |
| **Sanity check** | Do not claim commands were run; this pass inspected docs only. |

## Uncertainty And Null Results

What did the run fail to prove, falsify, or inspect?

- It did not run `canonical_change_detector.py` or `regenerate_all_derived.py --changed --incremental --dry-run`.
- It did not identify the best next target by scanning all derived artifacts.
- It did not update `known-gaps.md`, `integration-status.md`, or any generated artifact.

## Status

Choose one:

- documented-only

Status rationale:

This dry run produced an inspectable WORK note and a proposed next wedge. It did not execute scripts or change derived-regeneration coverage.

## Judgment

What mattered in this run?

- The adapter forced a sharper distinction between "regeneration exists" and "regeneration coverage is mature."

What changed because of this run?

- The likely next work-dev move became more concrete: expand one clearly mapped target and prove changed incremental dry-run behavior before adding runtime rebuild requests.

What should happen next?

- Pick one candidate derived target and run the documented sequence in `derived-regeneration.md` only when the operator wants execution.

## Direction Decision

Choose one:

- deepen

Decision rationale:

The current system has enough foundation to deepen one target path. Broadening to runtime requests would skip the stated maturity condition.

## Next Wedge

The smallest useful next step is:

- Choose one derived artifact with an obvious source -> output mapping, register it in the manifest, then run the changed incremental dry-run path before any live regeneration claim.

## Gate Decision

Choose one:

- stay WORK-only

Rationale:

This is an operator process finding, not companion Record material.
