# Known-path workflow registry

**Purpose:** A first-class, **documentation-first** place to describe **known-path workflows**: repeatable Grace-Mar processes where inputs, output shape, reviewer, **authority class**, and pass/fail signals are explicit enough that **operators or tools may draft or coordinate** work **without** acquiring durable Record merge authority.

**Not in scope for this registry:** autonomous agents, new merge paths, or changes to [`config/authority-map.json`](../../config/authority-map.json). Registering a workflow here does **not** widen write policy.

---

## Definition

A **known-path workflow** is a repeatable Grace-Mar process whose **inputs**, **output shape**, **reviewer**, **authority class**, and **evaluation criteria** are explicit enough that **runtime assistance** may draft or coordinate the work **without** gaining durable merge authority.

Open-ended reasoning (exploratory strategy, ambiguous ownership, “keep thinking until it feels right”) stays **outside** this registry until it can be narrowed to a stable path and a fitness test passes.

---

## Why Grace-Mar distinguishes known-path from open-ended work

Grace-Mar separates **runtime / WORK** surfaces from the **durable Record** and the **gated pipeline** ([runtime vs Record](../../runtime-vs-record.md), [AGENTS.md](../../../AGENTS.md)). Assistance is useful when the **path is stable** and outputs are **reviewable**; it is risky when steps, reviewers, or authority are implicit. This registry names **eligibility** and **load-lift** so operators do not confuse **speed** with **authority**.

---

## Eligibility (summary)

A process is a candidate for known-path treatment only when:

1. It **recurs** on a recognizable cadence or trigger.
2. **Input surfaces** are nameable (paths, inboxes, artifacts).
3. **Output type** is predictable and a reviewer can tell good from bad.
4. A **named reviewer** (human operator or explicit role) owns final judgment.
5. **`authority_class`** is one of the normative classes in [authority map](../../authority-map.md) (`read_only`, `draftable`, `review_required`, `human_only`, `ephemeral_only`), and **`maximum_action`** is stated in plain language.
6. The workflow **does not** bypass [recursion-gate](../../../users/grace-mar/recursion-gate.md), **does not** write canonical Record surfaces directly, and **does not** self-promote candidates.

Full gate: [workflow-fitness-test.md](workflow-fitness-test.md).

**Legacy alias:** Some external docs use hyphenated authority labels (`read-only`). In this repo, prefer **snake_case** to match [authority map](../../authority-map.md) and tooling language.

---

## Load-lift evaluation

A workflow is worth registering only if it **saves more operator time than it creates in review burden**. Capture:

- **Manual time** the workflow would otherwise cost (honest estimate).
- **Review time** each run or batch is expected to need.
- **Retirement condition:** when the operator would **not miss** the workflow if it were disabled.

If review burden cannot be estimated, treat the process as **not yet known-path** (manual checklist only).

## Load-Lift Receipts

Known-path workflows should be **evaluated** by whether they **lift operator load**: time saved vs review time, plus governance checks (missed signals, false confidence, authority drift). **Load-Lift Receipts** record those numbers and a **`continue` / `revise` / `narrow` / `retire` / `manual_only`** decision after a run. They **do not** approve durable Record changes or bypass the gate.

- Spec: [load-lift-receipts.md](load-lift-receipts.md)
- Schema: [`schema-registry/load-lift-receipt.v1.json`](../../../schema-registry/load-lift-receipt.v1.json)
- Example: [examples/load-lift-receipt-daily-strategy-thread-synthesis.json](examples/load-lift-receipt-daily-strategy-thread-synthesis.json)

---

## Relationship to existing Grace-Mar concepts

| Concept | Role relative to known-path workflows |
|--------|----------------------------------------|
| [Runtime vs Record](../../runtime-vs-record.md) | Drafts and receipts stay **runtime / WORK** unless promoted through the gate. |
| [Authority map](../../authority-map.md) | **`authority_class`** on a workflow aligns with these classes; it does **not** add new config keys. |
| [Recursion-gate](../../../users/grace-mar/recursion-gate.md) | Staging and companion approval remain **unchanged**. |
| [Action receipts](../../action-receipts.md) | General doctrine for meaningful-action audit stubs; **Load-Lift Receipts** are a **specialized** evaluation type for known-path runs ([load-lift-receipts.md](load-lift-receipts.md)). Neither substitutes for gate approval. |
| [Operator dashboards](../../operator-dashboards.md) | Future dashboards might list **active** workflows; this registry is the doc SSOT until then. |
| [Strategy notebook](../../skill-work/work-strategy/strategy-notebook/README.md) | Example workflows may **read** notebook paths and **write** reviewable drafts only where authority allows. |

**Workflow depth (different axis):** [Workflow depth contract](../../runtime/workflow-depth-contract.md) and related runtime docs describe **tier / observability** for execution depth. **Known-path** here means **eligibility and governance shape** for a *repeatable* process. The two ideas complement each other; do not merge the doc sets.

---

## Lifecycle

1. **Propose** — Author fills [workflow-agent-template.md](workflow-agent-template.md) with `status: proposed`.
2. **Run fitness test** — Walk [workflow-fitness-test.md](workflow-fitness-test.md); record classification.
3. **Register** — Commit the workflow doc under this tree (or link from runbooks); set `status` to `example` or `active` only when policy matches reality.
4. **Run manually or semi-automatically** — Operator or scripts follow the documented path; no merge authority implied.
5. **Produce draft / reviewable output** — Within declared `authority_class` and `maximum_action`.
6. **Emit optional receipt** — E.g. [Load-Lift Receipt](load-lift-receipts.md) after a pilot or recurring run; or other audit stubs; keep it **non-authoritative** per [runtime vs Record](../../runtime-vs-record.md).
7. **Human approves, rejects, revises, or promotes** — Through existing gates ([AGENTS.md](../../../AGENTS.md)); `process_approved_candidates.py` (or companion receipt flow) remains the merge path for Record changes.

---

## Schema

Machine shape for registry entries (optional for doc-only workflows; required if you emit JSON instances):

- [`schema-registry/known-path-workflow.v1.json`](../../../schema-registry/known-path-workflow.v1.json)
- **Load-lift (per run):** [`schema-registry/load-lift-receipt.v1.json`](../../../schema-registry/load-lift-receipt.v1.json) — see [load-lift-receipts.md](load-lift-receipts.md)

Developers may validate a YAML/JSON instance with `jsonschema` Draft 2020-12 locally; this repo does not require a dedicated validator script for the registry in the initial drop.

---

## Examples (patterns only)

| Example | File |
|--------|------|
| Daily strategy thread synthesis | [examples/daily-strategy-thread-synthesis.md](examples/daily-strategy-thread-synthesis.md) |
| Gate candidate intake | [examples/gate-candidate-intake.md](examples/gate-candidate-intake.md) |

Examples use `status: example`. They are **not** activated automation.

---

## See also

- [Workflow catalog](../../workflow-catalog.md) — broader recipe index
- [Load-lift receipts](load-lift-receipts.md)
- [Workflow fitness test](workflow-fitness-test.md)
- [Workflow registration template](workflow-agent-template.md)
