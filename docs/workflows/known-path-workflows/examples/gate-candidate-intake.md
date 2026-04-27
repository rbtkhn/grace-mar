---
workflow_id: gate-candidate-intake
title: Gate Candidate Intake
status: example
version: "0.1"
owner: operator
reviewer: human operator
cadence: weekly
trigger: "Weekly steward pass or operator-invoked after batch WORK edits"
authority_class: review_required
maximum_action: "Prepare candidate summaries and suggested YAML blocks for human paste into recursion-gate; never append to users/*/recursion-gate.md without operator action."
input_surfaces:
  - docs/skill-work/work-*/**/*-history.md
  - artifacts/
  - docs/skill-work/work-strategy/strategy-notebook/
output_surfaces:
  - operator clipboard or scratch markdown only
related_existing_surfaces:
  - runtime_vs_record
  - authority_map
  - recursion_gate
  - action_receipts
load_lift_metrics:
  manual_time_minutes: 60
  review_time_minutes: 25
  missed_signal_check: true
  false_promotion_check: true
promotion_path: "Operator pastes or edits users/grace-mar/recursion-gate.md; companion approves; merge via scripts/process_approved_candidates.py per AGENTS.md."
---

# Gate Candidate Intake (example)

**This file is an example pattern (`status: example`).** It is not an activated automation.

## Purpose

Scan **eligible WORK artifacts** (lane histories, derived summaries, notebook captures) for **signals that might become** `CANDIDATE-XXXX` blocks, prepare **summaries and draft YAML**, and **route them for operator review**—without writing to the canonical gate file or merging.

## Known path

1. Enumerate **read-only** inputs listed in `input_surfaces` for the chosen window (no writes).
2. For each plausible signal, draft a **candidate block** (id placeholder, summary, suggested `kind`, **no** `status: pending` applied to disk by automation unless policy explicitly allows scripted append—default: **operator pastes**).
3. Produce a **single review packet** (Markdown or text) listing: suggested id, one-line summary, evidence paths, channel_key if applicable.
4. Operator **edits** [`users/grace-mar/recursion-gate.md`](../../../../users/grace-mar/recursion-gate.md) or defers.
5. No `process_approved_candidates.py` until companion approval exists.

## Inputs

| Surface | Use |
|---------|-----|
| `docs/skill-work/work-*/*-history.md` | Recent WORK events |
| `artifacts/` | Derived rebuildables that may motivate staging |
| Strategy notebook paths | Judgment / ingest signals (read-only) |

## Output

- **Type:** Review packet (Markdown list of proposed candidates + evidence links).
- **Good output:** Each row links to files/lines; disambiguates companion vs operator channel; no auto-append to gate.
- **Bad output:** Silent writes to `recursion-gate.md`, or “approve” language without companion action.

## Human reviewer

**Human operator** (and **companion** for merge authority). Reviewer applies **gate policy** and decides paste vs reject.

## Authority boundary

- **`authority_class`:** `review_required`
- **`maximum_action`:** As in frontmatter: preparation and routing only.

## Load-lift evaluation

| Field | Value |
|--------|--------|
| Manual time normally required | ~60 min/week scanning scattered WORK surfaces |
| Expected review time | ~25 min if packet is short and well-cited |
| Review burden acceptable if | Operator can discard entire packet with no repo cleanup |
| Workflow should be retired if | Packet routinely duplicates existing pending candidates |

## Failure modes

- **Duplicate CANDIDATE ids:** Mitigate by grepping `recursion-gate.md` before paste.
- **False positives from derived artifacts:** Label tier; prefer primary WORK prose over skill-cards when ambiguous.

## Example run

_After a week of strategy ingests, assistant lists three hypothetical candidates with paths to `raw-input/` files. Operator pastes one into `recursion-gate.md` as `CANDIDATE-00XX`, rejects two. No script touches the gate file._
