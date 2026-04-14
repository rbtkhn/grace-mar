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

## Modes

| Mode | Typical use |
|------|----------------|
| `compact` | Short sessions, summaries, low token load |
| `medium` | Synthesis, review prep |
| `deep` | Long analysis, contradiction-heavy work, handoff builds |

## Related

- Progressive retrieval: [memory-retrieval.md](memory-retrieval.md)
- Memory brief: [read-hints.md](read-hints.md), `scripts/runtime/memory_brief.py` (optional `--budgeted-follow-on`)
- Review orchestrator: [../orchestration/review-orchestrator.md](../orchestration/review-orchestrator.md) (`--context-mode`)
- Long-horizon checkpoints: [long-horizon-work.md](long-horizon-work.md)
- Config folder overview: [`config/context_budgets/README.md`](../../config/context_budgets/README.md)
- Policy modes: [policy-modes.md](../policy-modes.md), [`config/policy_modes/defaults.json`](../../config/policy_modes/defaults.json)
