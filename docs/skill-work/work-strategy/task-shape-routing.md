# Task-shape routing (work-strategy)

**Lane:** WORK (`work-strategy`) — **not** durable Record. Task-shape routing produces **derived** classification JSON and metadata only; it does **not** grant permission to merge into [`users/`](../../../users/) or alter Voice surfaces.

## What task-shape routing is

**Task-shape routing** answers a narrow question before validation and review: **what kind of strategy job is this run?** Shapes are labels for **expectations** (inputs, derived outputs, validator emphasis, review posture), not claims about strategic correctness.

Classification is **deterministic** (keywords, optional YAML frontmatter, filename cues) and **inspectable**. It is intentionally **not** an LLM judgment.

## Why the lane benefits

work-strategy already separates doctrine, seams, and notebook discipline ([`DEFAULT-PATH.md`](DEFAULT-PATH.md), [`strategy-notebook/README.md`](strategy-notebook/README.md)). Task-shape routing adds a **first-class “job kind”** signal so operators and tooling can align artifact expectations and review posture **before** deep weave work — improving clarity without collapsing judgment into a rubric.

## Task shape vs model / provider routing

| Dimension | Task-shape routing | Model/provider routing |
|-----------|-------------------|-------------------------|
| Answers | What **kind of work** is this? | Which **model or API** to call |
| Scope | Strategy WORK artifacts + receipts | Execution / infra (out of scope for this PR) |
| Output | Shape label + contract hints | Provider IDs, tiers, keys |

These layers are **orthogonal**. Task-shape routing does **not** select models.

## Influence on expectations (not on judgment)

- Shapes inform **what to look for** in a handoff (e.g. gate paste vs synthesis vs watch delta).
- They do **not** replace VERIFY discipline, notebook weave rules, or companion gate approval.
- Mixed-intent runs still pick a **primary** shape; secondary candidates and notes preserve ambiguity ([`validator-contract.md`](validator-contract.md), [`carry-harness.md`](carry-harness.md)).

## Runtime vs Record membrane

Task-shape reports live under **runtime** / operator-chosen paths outside forbidden roots — see [`runtime-vs-record.md`](../../runtime-vs-record.md). Routing output is **rebuildable** and **non-canonical**, like carry receipts and validation reports.

## Relation to carry harness and validators

- [**Carry harness**](carry-harness.md): optional **`--classify-task-shape`** embeds **`task_shape`**, **`task_shape_confidence`**, **`task_shape_expected_outputs`**, and **`task_shape_report_path`** on the receipt when classification runs.
- [**Validators**](validator-contract.md): optional **`--task-shape`** / **`--task-shape-report`** annotates the validation report and applies a light **`task_shape_expectations`** check when a shape implies outputs but no artifacts were declared.

---

## Task shapes (initial set)

### A. `watch_update`

| | |
|--|--|
| **Typical intent** | Refresh an active watch, threshold, or ongoing scan. |
| **Minimum inputs** | What is watched; baseline or prior state pointer. |
| **Expected derived outputs** | Watch delta note; optional threshold crossing summary. |
| **Validator emphasis** | Sources present; artifact substance; unresolved markers. |
| **Default review posture** | Confirm deltas against prior watch state; factual claims may need VERIFY. |
| **Do not use for** | Greenfield synthesis with no watch object; one-off essays unrelated to monitoring. |

### B. `notebook_synthesis`

| | |
|--|--|
| **Typical intent** | Weave sources or threads into strategy-notebook-style prose. |
| **Minimum inputs** | Source material or thread references. |
| **Expected derived outputs** | Notebook section / knot draft; optional cross-links. |
| **Validator emphasis** | Substance; markdown headings; contradiction/tension surfacing. |
| **Default review posture** | Editorial pass on seams (Chronicle vs Reflection); promotion remains manual. |
| **Do not use for** | Automatic edits to canonical notebook files; Record merges. |

### C. `decision_point`

| | |
|--|--|
| **Typical intent** | Frame options, tradeoffs, risks, recommendations. |
| **Minimum inputs** | Decision question or scope boundary. |
| **Expected derived outputs** | Option matrix or branches; explicit risk notes. |
| **Validator emphasis** | Substance; contradiction/tension markers; unresolved markers. |
| **Default review posture** | Validate assumptions; numeric claims may need VERIFY. |
| **Do not use for** | Substituting for governance approval or gate merges. |

### D. `gate_candidate_prep`

| | |
|--|--|
| **Typical intent** | Produce paste-ready gate / bridge material **without staging**. |
| **Minimum inputs** | Stub or outline for the candidate. |
| **Expected derived outputs** | Paste-ready snippet or bridge doc. |
| **Validator emphasis** | Gate snippet checks; output path safety. |
| **Default review posture** | Operator-only paste; companion owns merge. |
| **Do not use for** | Implying approval, merge, or automatic staging. |

### E. `contradiction_review`

| | |
|--|--|
| **Typical intent** | Surface or preserve tensions across sources or judgments. |
| **Minimum inputs** | At least two distinguishable positions or sources. |
| **Expected derived outputs** | Comparison / tension map; intentional ambiguity where appropriate. |
| **Validator emphasis** | Contradiction/tension scans; unresolved markers. |
| **Default review posture** | Preserve disproportion; avoid forced synthesis. |
| **Do not use for** | Erasing conflicts for narrative convenience. |

### F. `source_expansion`

| | |
|--|--|
| **Typical intent** | Broaden coverage or fill evidence gaps before synthesis. |
| **Minimum inputs** | Gap statement or search vector. |
| **Expected derived outputs** | Source log / bibliography; optional gap-closure notes. |
| **Validator emphasis** | Sources present; artifact substance. |
| **Default review posture** | Spot-check sources before downstream synthesis claims. |
| **Do not use for** | Claiming synthesis completeness without later synthesis work. |

---

## Doctrine

- Task shape is a **runtime classification**, not a truth claim.
- Shapes affect **expectations**, not permission to change Record.
- One run may feel mixed; the router still emits a **primary** shape and may list **secondary** candidates.
- **Ambiguity** is surfaced (`confidence: low`, notes), not hidden.

Configuration (human-editable): [`config/work_strategy_task_shapes.yaml`](../../../config/work_strategy_task_shapes.yaml). Classifier CLI: [`scripts/work_strategy/classify_task_shape.py`](../../../scripts/work_strategy/classify_task_shape.py). Report schema: [`schemas/work_strategy_task_shape_report.schema.json`](../../../schemas/work_strategy_task_shape_report.schema.json).
