# Workflow depth (operator control)

**Workflow depth** selects how much prepared-context assembly runs before packing: fixed budget classes (`shallow` … `exhaustive`) or **`auto`** adaptive halt/continue. It is **runtime / WORK** only — not Record truth, not a merge gate.

Use [`build_budgeted_context.py`](../../scripts/prepared_context/build_budgeted_context.py) with **`--workflow-depth`** or the short alias **`--depth`**. **`--task-anchor` is required** whenever depth is set (operator problem statement; reinjected into output and receipts).

## When to use each mode

| Depth | Role |
|-------|------|
| **`shallow`** | Cheapest pass: maps to **compact** budget class and the depth default max observation count. Good for quick scans. |
| **`normal`** | Standard operator path: **medium** budget class. |
| **`deep`** | Broader excerpts and more room for contradiction-heavy review. |
| **`exhaustive`** | Maximum **bounded** expansion (deep class with a higher observation cap). |
| **`auto`** | Adaptive control: compact dry-pack, metrics, optional escalation to medium, plus quality-guard halts when deeper expansion looks repetitive or off-anchor. |

With any fixed depth, **`--mode` is ignored** (depth chooses the effective budget class). With **`auto`**, stop reasons and phases are recorded in the workflow-depth receipt.

## Receipts (non-canonical)

Append-only JSONL under `runtime/workflow-depth/index.jsonl` (or `GRACE_MAR_WORKFLOW_DEPTH_HOME`). Typical fields include:

- **`workflow_depth`** — requested value (`shallow`, `normal`, `deep`, `exhaustive`, `auto`)
- **`effective_mode`** — resulting budget class (`compact`, `medium`, `deep`)
- **`phases`** — named phase log (halt/continue summaries)
- **`stop_reason`** — why the run stopped at that depth (fixed-preset prefix for non-auto, or heuristic names for `auto`)

See also [context-budgeting.md](context-budgeting.md) for budget doctrine and [workflow_depth_control.py](../../scripts/prepared_context/workflow_depth_control.py) for heuristics.

**Shared contract:** [workflow-depth-contract.md](workflow-depth-contract.md).

## Memory brief follow-on

[`memory_brief.py`](../../scripts/runtime/memory_brief.py) can run a budgeted prepared-context build after the brief using **`--budgeted-follow-on`**. When you set **`--workflow-depth`** / **`--depth`**, you must also pass **`--task-anchor`** (and keep **`-o`**). The child build uses the shared depth routing contract; receipts may show **`sourceWorkflow`: `memory_brief`**.

## Examples

**Auto depth (alias):**

```bash
python3 scripts/prepared_context/build_budgeted_context.py \
  --lane work-strategy \
  --depth auto \
  --task-anchor "Assess whether deeper context expansion is justified." \
  -o prepared-context/budgeted-review-context.md
```

**Deep fixed depth:**

```bash
python3 scripts/prepared_context/build_budgeted_context.py \
  --lane work-strategy \
  --depth deep \
  --task-anchor "Build a fuller contradiction-aware context for this strategy session." \
  -o prepared-context/budgeted-deep.md
```

**Long flag (same behavior):**

```bash
python3 scripts/prepared_context/build_budgeted_context.py \
  --lane work-strategy \
  --workflow-depth shallow \
  --task-anchor "Minimal context for a quick check." \
  -o prepared-context/budgeted-shallow.md
```
