# Context budgeting (operator efficiency)

**Purpose:** Make prepared-context assembly **explicit** about how much material fits, **what was included**, **what was excluded**, and **why** — without treating budget as a truth filter.

## Doctrine

- **Legibility, not judgment:** Budget caps are **operator-efficiency** and **repeatability** tools. They do **not** decide what is true, what may enter the Record, or what passes abstention checks.
- **Lane-aware defaults:** Default character targets per lane and mode live in [`config/context_budgets/lane-defaults.json`](../../config/context_budgets/lane-defaults.json). Tune numbers as needed; the important part is **reproducible** behavior for the same lane + mode.
- **Compact default:** **Compact** mode is appropriate for routine work, quick review, and short sessions. **Deep** mode is **explicit** — use for long analysis, difficult contradictions, or handoff preparation — not as a silent default.
- **Visible exclusion:** When items are dropped for budget pressure, the output lists them under **Excluded** so operators can rerun in **medium** or **deep** or narrow inputs.
- **Governance unchanged:** Budgeting does **not** bypass [abstention policy](../abstention-policy.md), [memory retrieval](memory-retrieval.md) doctrine, or **RECURSION-GATE** review.

### Policy mode (governance envelope)

Each budgeted artifact lists an active **[policy mode](../policy-modes.md)** (`--policy-mode` or `GRACE_MAR_POLICY_MODE`, default `operator_only`). That is **separate** from budget class (`compact` / `medium` / `deep`): budget caps size; policy mode describes staging/abstention posture for the session.

## Command

```bash
python3 scripts/prepared_context/build_budgeted_context.py \
  --lane work-strategy \
  --mode compact \
  --policy-mode operator_only \
  --query "iran negotiation framing" \
  -o prepared-context/budgeted-work-strategy.md
```

Optional file inputs (ranked with observations):

- `--include-memory-brief prepared-context/memory-brief.md`
- `--include-checkpoint artifacts/handoffs/checkpoints/YYYY-MM-DD-lane-title.md`
- `--include-handoff` for handoff packets

Each successful run updates `prepared-context/last-budget-builds.json` (per-lane receipt for dashboards).

## Workflow depth (adaptive halting)

Optional **`--workflow-depth`** (alias **`--depth`**) on [`build_budgeted_context.py`](../../scripts/prepared_context/build_budgeted_context.py) adds **named phases**, a **task anchor** (and optional **constraint**), and an append-only receipt at `runtime/workflow-depth/index.jsonl` (or `GRACE_MAR_WORKFLOW_DEPTH_HOME`). This is **runtime weather** — not a second governance layer and not Record truth.

**See also:** [workflow-depth.md](workflow-depth.md) — when to pick each depth mode and example commands; [workflow-depth-contract.md](workflow-depth-contract.md) — shared routing vocabulary.

| Flag | Meaning |
|------|---------|
| `--workflow-depth shallow` (or `--depth shallow`) | Map to **compact** (and depth-specific max observation count) |
| `normal` | **medium** |
| `deep` | **deep** |
| `exhaustive` | **deep** with higher candidate cap |
| `auto` | Compact dry-pack → heuristic halt/continue → optional escalation to **medium** |

**Requires** `--task-anchor` (operator problem statement). **`--mode` is ignored** when `--workflow-depth` or `--depth` is set.

**Work-strategy calibration:** Heuristics for `auto` are tuned first against [`lane-defaults.json`](../../config/context_budgets/lane-defaults.json) **work-strategy** budgets.

Example (work-strategy, auto depth):

```bash
python3 scripts/prepared_context/build_budgeted_context.py \
  --lane work-strategy \
  --workflow-depth auto \
  --task-anchor "Compare Iran framing across two briefs" \
  -q "iran" \
  -o /tmp/demo-budgeted.md
```

Receipt schema: [`schema-registry/workflow-depth-receipt.v1.json`](../../schema-registry/workflow-depth-receipt.v1.json).

## Modes

| Mode | Typical use |
|------|----------------|
| `compact` | Short sessions, summaries, low token load |
| `medium` | Synthesis, review prep |
| `deep` | Long analysis, contradiction-heavy work, handoff builds |

## Related

- Workflow depth modes: [workflow-depth.md](workflow-depth.md)
- Progressive retrieval: [memory-retrieval.md](memory-retrieval.md)
- Memory brief: [read-hints.md](read-hints.md), `scripts/runtime/memory_brief.py` (optional `--budgeted-follow-on`)
- Review orchestrator: [../orchestration/review-orchestrator.md](../orchestration/review-orchestrator.md) (`--context-mode`)
- Long-horizon checkpoints: [long-horizon-work.md](long-horizon-work.md)
- Config folder overview: [`config/context_budgets/README.md`](../../config/context_budgets/README.md)
- Policy modes: [policy-modes.md](../policy-modes.md), [`config/policy_modes/defaults.json`](../../config/policy_modes/defaults.json)
