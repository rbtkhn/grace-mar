# Runtime: work-strategy

Derived harness outputs for the strategy WORK lane (non-canonical).

| Path | Role |
|------|------|
| `carry-receipts/` | JSON receipts from [`scripts/work_strategy/run_carry_harness.py`](../../scripts/work_strategy/run_carry_harness.py). Safe to gitignore locally; omit secrets. |
| `validation-reports/` | JSON validation reports from [`scripts/work_strategy/validate_strategy_packet.py`](../../scripts/work_strategy/validate_strategy_packet.py). Derived only; omit secrets. |
| `task-shape-reports/` | JSON task-shape classifications from [`scripts/work_strategy/classify_task_shape.py`](../../scripts/work_strategy/classify_task_shape.py). Derived only; omit secrets. |

See [`carry-harness.md`](../../docs/skill-work/work-strategy/carry-harness.md), [`validator-contract.md`](../../docs/skill-work/work-strategy/validator-contract.md), and [`task-shape-routing.md`](../../docs/skill-work/work-strategy/task-shape-routing.md).
