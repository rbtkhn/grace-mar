---
workflow_id: daily-strategy-thread-synthesis
title: Daily Strategy Thread Synthesis
status: example
version: "0.1"
owner: operator
reviewer: human operator
cadence: daily
trigger: "End of strategy day or operator-invoked before EOD compose"
authority_class: draftable
maximum_action: "Produce a single reviewable draft markdown file summarizing signals; never merge into expert threads or days.md without operator weave and gate rules."
input_surfaces:
  - docs/skill-work/work-strategy/strategy-notebook/chapters/
  - docs/skill-work/work-strategy/strategy-notebook/raw-input/
  - docs/skill-work/work-strategy/strategy-notebook/inbox/
  - docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md
output_surfaces:
  - docs/skill-work/work-strategy/strategy-notebook/raw-input/
related_existing_surfaces:
  - runtime_vs_record
  - authority_map
  - recursion_gate
  - action_receipts
  - strategy_notebook
load_lift_metrics:
  manual_time_minutes: 45
  review_time_minutes: 15
  missed_signal_check: true
  false_promotion_check: true
promotion_path: "Operator edits days.md or expert thread.md using existing notebook weave; Record changes only via recursion-gate approval and merge script per AGENTS.md."
---

# Daily Strategy Thread Synthesis (example)

**This file is an example pattern (`status: example`).** It is not an activated automation.

## Purpose

Consolidate **recent strategy-notebook inputs** (chapter `days.md` pointers, `raw-input/`, `inbox/`, optional daily brief) into **one reviewable synthesis draft** that surfaces thread updates, tensions, missing signals, and proposed next actions—without writing canonical expert files or merging gate candidates.

## Known path

1. Read **compose-day** scope from [NOTEBOOK-PREFERENCES](../../../skill-work/work-strategy/strategy-notebook/NOTEBOOK-PREFERENCES.md) and active `chapters/YYYY-MM/days.md` (read-only).
2. Scan **inbox** and **raw-input** for the same window (read-only).
3. Optionally read `docs/skill-work/work-strategy/daily-brief-YYYY-MM-DD.md` for §1d–§1h anchors (read-only).
4. Emit **one** draft file under `strategy-notebook/raw-input/` (or operator-chosen draft path) with sections: Chronicle summary, Open threads, Tensions, Missing signals, Proposed next actions (all draft).
5. Operator **reviews**; operator **weaves** into `days.md` / expert `thread.md` using existing repo conventions; **no** direct append to expert threads by the workflow as executed.

## Inputs

| Surface | Use |
|---------|-----|
| `strategy-notebook/chapters/…/days.md` | Continuity and compose day |
| `strategy-notebook/raw-input/`, `inbox/` | Fresh captures |
| `daily-brief-YYYY-MM-DD.md` | Optional same-day work-politics / watch context |

## Output

- **Type:** Single Markdown draft (suggested path pattern: `strategy-notebook/raw-input/YYYY-MM-DD-strategy-synthesis-draft.md`).
- **Good output:** Distinguishable sections, every factual claim has a **path or link** back to source material, explicit “draft / not merged” header.
- **Bad output:** Unsourced claims, silent edits to `experts/*/thread.md`, or language that implies companion approval.

## Human reviewer

**Human operator** — owns EOD compose and notebook policy. Expected review **~10–20 minutes** per draft if inputs were bounded.

## Authority boundary

- **`authority_class`:** `draftable`
- **`maximum_action`:** As in frontmatter: one draft file only; no canonical thread writes, no gate merges.

## Load-lift evaluation

| Field | Value |
|--------|--------|
| Manual time normally required | ~45 min to re-read inbox + raw-input + days without a scaffold |
| Expected review time | ~15 min if draft is well-cited |
| Review burden acceptable if | Every claim traceable; operator can reject the whole draft without cleanup |
| Workflow should be retired if | Drafts routinely omit sources or push toward auto-merge language |

## Failure modes

- **Hallucinated links:** Mitigate by requiring path citations in the draft rubric.
- **Wrong compose day:** Mitigate by pinning the date in the filename and first heading.
- **Scope creep into Record:** Treat as disqualifier; stop and re-run [fitness test](../workflow-fitness-test.md).

## Example run

_Operator asks for a synthesis for 2026-04-27. Assistant reads `chapters/2026-04/days.md`, `raw-input/2026-04-27/`, and inbox rows, then writes `raw-input/2026-04-27-strategy-synthesis-draft.md` with labeled sections. Operator deletes two bullets, weaves two paragraphs into `days.md` Reflection, and does not touch `recursion-gate.md` in that pass._
