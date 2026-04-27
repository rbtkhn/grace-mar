# Workflow registration template

Copy this file to a new path under `docs/workflows/known-path-workflows/` (or a lane-specific doc tree if policy allows), replace placeholders, and run the [workflow fitness test](workflow-fitness-test.md) before setting `status` to `active`.

```yaml
---
workflow_id: ""
title: ""
status: proposed
version: "0.1"
owner: operator
reviewer: ""
cadence: operator_invoked
trigger: ""
authority_class: draftable
maximum_action: ""
input_surfaces: []
output_surfaces: []
related_existing_surfaces:
  - runtime_vs_record
  - authority_map
  - recursion_gate
  - action_receipts
---
```

**`cadence` values (suggested):** `daily`, `weekly`, `monthly`, `event_driven`, `operator_invoked` (use **snake_case** in machine-facing YAML; prose may spell out “operator-invoked”).

**`authority_class` values (normative):** `read_only` | `draftable` | `review_required` | `human_only` | `ephemeral_only` — see [authority map](../../authority-map.md).

---

# [Workflow Title]

## 1. Purpose

_Why this workflow exists and what problem it solves._

## 2. Known path

_Numbered or bulleted steps. No vague “analyze the repo.” Each step names inputs and outputs._

## 3. Inputs

_List paths, inboxes, scripts, or runtime surfaces read. Link to docs or `config/` as needed._

## 4. Output

_Describe artifact type, default path, and how “good” is verified._

## 5. Human reviewer

_Name or role, expected review time, escalation if unavailable._

## 6. Authority boundary

- **`authority_class`:** (must match frontmatter)
- **`maximum_action`:** (must match frontmatter; one paragraph max)

## 7. Non-authority statement

This workflow may draft, summarize, route, or prepare reviewable material only within its declared **authority class**. It does **not** bypass [recursion-gate](../../../users/grace-mar/recursion-gate.md), does **not** write directly to durable Record surfaces (`self.md`, `self-archive.md`, `self-skills.md`, `bot/prompt.py`, or other canonical paths except through the governed merge path), and does **not** promote candidates without **human approval**.

## 8. Load-lift evaluation

| Field | Value |
|--------|--------|
| Manual time normally required | |
| Expected review time | |
| Review burden acceptable if | |
| Workflow should be retired if | |

## 9. Failure modes

_What can go wrong; how the operator detects it; what to do (stop, revert draft, open gate review, etc.)._

## 10. Receipts / audit trail

_Optional receipt types, paths under `artifacts/` or logs, pointers to [action receipts](../../action-receipts.md)._

## 11. Promotion path

_Exact handoff: e.g. “stage `CANDIDATE-XXXX` in recursion-gate” or “open PR”; link to [AGENTS.md](../../../AGENTS.md) merge rules._

## 12. Example run

_One short fictional or redacted walkthrough._

---

**Schema:** When this frontmatter is expressed as JSON for tooling, validate against [`schema-registry/known-path-workflow.v1.json`](../../../schema-registry/known-path-workflow.v1.json) (Draft 2020-12; optional keys `related_existing_surfaces`, `load_lift_metrics`, `promotion_path`).
