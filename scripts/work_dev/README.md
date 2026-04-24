# `scripts/work_dev/` (work-dev operators)

| Script | Role |
|--------|------|
| `smoke_strategy_visualizer.py` | **Visualizer static smoke test** — read-only scan of the strategy-notebook workbench `strategy-notebook-visualizer.html` for dependency-free structure, fixture `fetch` reference, Workbench boundary text, and UI affordance markers (no browser, no network). [PREFLIGHT optional section](../../docs/skill-work/work-dev/workbench/PREFLIGHT.md#visualizer-smoke-test) |
| `preflight_workbench.py` | **Workbench preflight** — read-only checks for Workbench docs, strategy visualizer pilot, **static HTML** (`smoke_strategy_visualizer.py` by default, skip with `--skip-smoke`), fixture JSON, `workbench/examples/*.json` (delegates to `validate_workbench_receipt`), and (default) `generate_strategy_notebook_visualizer_fixture.py --check`. [Docs](../../docs/skill-work/work-dev/workbench/PREFLIGHT.md) |
| `validate_workbench_receipt.py` | Validate one [workbench receipt JSON](../../docs/skill-work/work-dev/workbench/WORKBENCH-RECEIPT-SPEC.md). |
| `new_workbench_receipt.py` | Scaffold a new workbench receipt. |

For the full list of integration and harness scripts, see the [work-dev README contents](../../docs/skill-work/work-dev/README.md#contents) and [workbench SCRIPT-USAGE.md](../../docs/skill-work/work-dev/workbench/SCRIPT-USAGE.md).
