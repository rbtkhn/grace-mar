# Runtime: work-strategy

Derived harness outputs for the strategy WORK lane (non-canonical).

| Path | Role |
|------|------|
| `carry-receipts/` | JSON receipts from [`scripts/work_strategy/run_carry_harness.py`](../../scripts/work_strategy/run_carry_harness.py). Safe to gitignore locally; omit secrets. |
| `validation-reports/` | JSON validation reports from [`scripts/work_strategy/validate_strategy_packet.py`](../../scripts/work_strategy/validate_strategy_packet.py). Derived only; omit secrets. |
| `task-shape-reports/` | JSON task-shape classifications from [`scripts/work_strategy/classify_task_shape.py`](../../scripts/work_strategy/classify_task_shape.py). Derived only; omit secrets. |
| `review-packets/` | JSON/Markdown review packets from [`scripts/work_strategy/build_review_packet.py`](../../scripts/work_strategy/build_review_packet.py); optional harness [`--build-review-packet`](../../docs/skill-work/work-strategy/carry-harness.md). Derived only; omit secrets. |
| `observability/` | JSON/Markdown summaries from [`scripts/work_strategy/summarize_carry_receipts.py`](../../scripts/work_strategy/summarize_carry_receipts.py). Derived only; safe to gitignore locally. |

See [`carry-harness.md`](../../docs/skill-work/work-strategy/carry-harness.md), [`validator-contract.md`](../../docs/skill-work/work-strategy/validator-contract.md), [`task-shape-routing.md`](../../docs/skill-work/work-strategy/task-shape-routing.md), [`review-packet-template.md`](../../docs/skill-work/work-strategy/review-packet-template.md), and [`observability.md`](../../docs/skill-work/work-strategy/observability.md).
