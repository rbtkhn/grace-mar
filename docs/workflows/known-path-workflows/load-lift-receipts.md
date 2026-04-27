# Load-Lift Receipts

**WORK only; not Record.** A Load-Lift Receipt is an **evaluation artifact** for a [known-path workflow](README.md) run. It does **not** approve durable changes, does **not** stage merge candidates, and does **not** change workflow or surface authority. See [Governance override](#6-governance-override) below.

Machine schema: [`schema-registry/load-lift-receipt.v1.json`](../../../schema-registry/load-lift-receipt.v1.json) (JSON Schema Draft 2020-12).

**Authority class spelling:** use **snake_case** values aligned with [authority map](../../authority-map.md) and [`known-path-workflow.v1.json`](../../../schema-registry/known-path-workflow.v1.json) (`read_only`, `draftable`, `review_required`, `human_only`, `ephemeral_only`).

---

## 1. Definition

A **Load-Lift Receipt** is a **review artifact** that records whether a known-path workflow **reduced operator burden** without weakening governance, increasing review cost beyond saved time, or creating **hidden authority drift** (e.g. implying merge, gate skip, or canonical write).

---

## 2. Scope

- **Load-Lift Receipts evaluate workflow usefulness** after (or in trial of) a run — time, quality flags, and a disposition decision.
- They do **not** approve durable SELF, EVIDENCE, SKILLS, or prompt changes.
- They do **not** promote [recursion-gate](../../../users/grace-mar/recursion-gate.md) candidates.
- They do **not** change workflow **`authority_class`** or [`config/authority-map.json`](../../config/authority-map.json).
- They **may** support later human decisions to **continue**, **revise**, **narrow**, or **retire** a workflow, or to keep it **manual_only**.

---

## 3. When to emit

A Load-Lift Receipt may be emitted when:

- a known-path workflow **runs for the first time** (pilot);
- a workflow **changes scope**;
- a workflow **produces a recurring output** and the operator is tracking quality over time;
- the operator wants to **compare** manual effort against **review** effort;
- a workflow is being considered for **`status: active`**, **retirement**, or **narrowing**.

Emit **manually** (fill JSON or copy template) or, in a later PR, from optional tooling. **This repo does not require automation.**

---

## 4. Required fields

| Field | Meaning |
|--------|--------|
| `receipt_id` | Unique id for this receipt (e.g. `load-lift-<workflow_id>-<YYYY-MM-DD>`). |
| `workflow_id` | Matches the workflow’s `workflow_id` in its registry / template. |
| `workflow_title` | Human-readable title. |
| `run_date` | Date of the run (`YYYY-MM-DD`). |
| `run_trigger` | Free string (e.g. `operator_invoked`, `daily`, event name). |
| `authority_class` | As declared for the workflow; must match [authority map](../../authority-map.md) classes (snake_case). |
| `reviewer` | Person or role that judged the output and times. |
| `manual_baseline_minutes` | Honest estimate of time **without** this workflow for the same task. |
| `workflow_run_minutes` | Time spent on the assisted path (operator + tool wall-clock, as recorded). |
| `review_minutes` | Time spent **reviewing** the workflow output. |
| `net_time_saved_minutes` | See [Load-lift formula](#5-load-lift-formula); may be precomputed. |
| `output_accepted` | Whether the output was acceptable enough to use or build on. |
| `output_required_revision` | Whether non-trivial revision was required. |
| `missed_major_signal` | Whether an important signal was **missed** in the output. |
| `false_promotion_risk` | `none` \| `low` \| `medium` \| `high` — risk the output could be mistaken for an approved or canonical state. |
| `authority_boundary_issue` | Any observed overreach vs declared `maximum_action` / [runtime vs Record](../../runtime-vs-record.md). |
| `operator_would_miss_if_disabled` | Subjective: would the operator miss this workflow if turned off. |
| `decision` | `continue` \| `revise` \| `narrow` \| `retire` \| `manual_only` — see [Final classification](workflow-fitness-test.md#final-classification) in the fitness test. |

**Optional fields (schema):** `reviewer_notes` (string), `related_artifacts` (array of paths or URIs to drafts, run logs, or workflow doc).

---

## 5. Load-lift formula

**net_time_saved_minutes = manual_baseline_minutes - (workflow_run_minutes + review_minutes)**

Clarifications:

- A **positive** `net_time_saved_minutes` does **not** automatically mean the workflow should **continue**. Governance failures override raw time math.
- **`missed_major_signal`**, elevated **`false_promotion_risk`**, or **`authority_boundary_issue: true`** should usually push the **`decision`** toward **`revise`**, **`narrow`**, **`retire`**, or **`manual_only`**, not **`continue`**, even if time saved is positive.
- Rounding: document if estimates are banded; consistency matters more than false precision.

**Optional cross-check** with the workflow’s planned metrics in [workflow-fitness-test.md](workflow-fitness-test.md) § Load-lift check.

---

## 6. Governance override

A Load-Lift Receipt **must not** be interpreted as:

- **approval** to write [durable Record](README.md#relationship-to-existing-grace-mar-concepts) surfaces,
- **bypass** of [recursion-gate](../../../users/grace-mar/recursion-gate.md) or [AGENTS.md](../../../AGENTS.md) merge rules,
- **expansion** of [authority](README.md#relationship-to-existing-grace-mar-concepts) to draft or stage beyond the workflow’s declared class.

Any authority expansion requires **explicit** review through existing Grace-Mar governance — not a receipt in this format.

**Relation to [action receipts](../../action-receipts.md):** Load-lift receipts are a **specialized** evaluation type for known-path **workflow runs**. They are **not** a replacement for other action or pipeline audit records.

---

## 7. Example receipt

Illustrative JSON for workflow **`daily-strategy-thread-synthesis`** (example values; not a claim that the workflow is active in production):

See [examples/load-lift-receipt-daily-strategy-thread-synthesis.json](examples/load-lift-receipt-daily-strategy-thread-synthesis.json).

Narrative summary: baseline **45** min, run **3** min, review **9** min → **net 33** min saved; **minor revision** was needed; **no** missed major signal; **low** false-promotion risk; **no** authority issue; operator **would** miss the workflow; **`decision`: `continue`**.

---

## 8. Retire / narrow conditions

Consider **`narrow`**, **`retire`**, or **`manual_only`** if:

- **Review time** repeatedly **exceeds** time saved.
- **Outputs** require **extensive correction** relative to value.
- **Major signals** are **missed** in repeated runs.
- **Authority boundaries** are unclear or repeatedly tested.
- The **reviewer** often **cannot** tell good output from bad.
- The workflow creates **more cognitive load** than it removes (even if wall-clock is flat).

Document the rationale in `reviewer_notes` and set **`decision`** accordingly.

---

## See also

- [Known-path workflow registry (README)](README.md)
- [Workflow fitness test](workflow-fitness-test.md)
- [Action receipts (doctrine)](../../action-receipts.md)
