# Work-Strategy Carry Harness

**Lane:** WORK (`work-strategy`) — **not** durable Record. Receipts are **derived**, **rebuildable**, and **non-canonical**.

**Purpose:** Provide a **narrow, deterministic** check that a messy strategy task produced **minimum legible handoff artifacts** from intake toward review readiness — without proving strategic correctness, approving merges, or staging gate candidates.

---

## What “carry” means

1. **Intake** — A task description file is readable (typically Markdown).
2. **Artifact expectations** — Explicit paths to sources and expected outputs are declared on the CLI (and echoed in the receipt).
3. **Derived review posture** — The harness does **not** judge judgment quality; it only checks **presence** and **non-trivial bulk** where applicable.
4. **Gate-snippet readiness (optional)** — If you pass `--gate-snippet`, the harness checks that the snippet file exists and is **non-empty** (paste-ready text). It does **not** stage or approve anything.
5. **Receipt** — A JSON document describes checks, summary counts, and overall `pass` / `fail` / `needs_review`.

Canonical doctrine for Record vs runtime: [runtime-vs-record.md](../../runtime-vs-record.md), [AGENTS.md](../../../AGENTS.md).

---

## Relationship to other strategy tooling

| Tool | Role |
|------|------|
| [`scripts/build_strategy_observability.py`](../../../scripts/build_strategy_observability.py) | Lane-wide notebook health metrics → `artifacts/work-strategy/strategy-observability.json`. |
| [`scripts/build_strategy_run_report.py`](../../../scripts/build_strategy_run_report.py) | Summarizes recent `artifacts/strategy-runs/*/state.json` runs. |
| **`run_carry_harness.py`** | **Task-scoped**: explicit `--task`, `--source`, `--artifact` paths and a **carry receipt** under `runtime/work-strategy/`. |

These are **different slices**; the carry harness does not replace observability or strategy-run reports.

---

## What this harness measures

- Task file readable?
- Optional source paths exist?
- Expected artifact paths exist?
- For Markdown/text artifacts: **word count** ≥ **50** (heuristic for “non-trivial”)?
- If `--gate-snippet` was passed: snippet non-empty?
- Output receipt path **not** under forbidden canonical roots (`users/**`, specific `bot/` files)?
- This script **never** writes to Record surfaces or `recursion-gate.md`; it may include **gate-ready paste text inside the receipt only** as captured from your snippet file.

---

## What this harness does **not** do

- Prove strategic correctness or falsify geopolitical claims.
- Merge, approve, or stage `RECURSION-GATE` candidates.
- Call an LLM or the network.
- Replace [`scripts/emit_work_strategy_gate_paste_snippet.py`](../../../scripts/emit_work_strategy_gate_paste_snippet.py) (that script may write **staging** paste files under `users/` when **you** run it operator-side).

---

## Schema

Receipt shape: [`schemas/work_strategy_carry_receipt.schema.json`](../../../schemas/work_strategy_carry_receipt.schema.json).

Top-level fields include `checks`, `summary`, `gate_snippet`, `record_boundary`, and `result`. **`checks`** are authoritative per-condition outcomes; **`summary`** rolls up counts; **`result`** drives exit code behavior with `--fail-on-result`.

---

## How to run

From repo root:

```bash
python3 scripts/work_strategy/run_carry_harness.py \
  --task examples/work-strategy/carry-harness/sample-task.md \
  --source examples/work-strategy/carry-harness/sample-source.md \
  --artifact examples/work-strategy/carry-harness/sample-artifact.md \
  --gate-snippet examples/work-strategy/carry-harness/sample-gate-snippet.md \
  --out runtime/work-strategy/carry-receipts/sample-receipt.json \
  --json
```

Options:

| Flag | Meaning |
|------|---------|
| `--task PATH` | Task intake file (recommended). |
| `--source PATH` | Repeatable; expected to exist (`needs_review` if missing). |
| `--artifact PATH` | Repeatable; expected outputs (`fail` if missing). |
| `--gate-snippet PATH` | Optional; if provided, must be non-empty (`needs_review` otherwise). |
| `--out PATH` | Receipt JSON output (**refused** if under forbidden roots). |
| `--run-id STRING` | Stable id for logs (default: generated). |
| `--repo-root PATH` | Repo root (default: inferred from script location). |
| `--json` | Print receipt JSON to stdout. |
| `--fail-on-result fail\|needs_review\|never` | Exit code policy (default `fail`: nonzero only on `result==fail`). |

---

## Interpreting failures

- **`fail`** — Hard precondition broken (unreadable task, missing expected artifact, forbidden `--out`, etc.). Fix inputs or path before counting as “carried.”
- **`needs_review`** — Soft signals: missing optional sources, thin text artifacts (&lt;50 words), empty gate snippet when requested. Human decides whether to accept or iterate.
- **`pass`** — All checks passed; still **not** proof of good strategy.

---

## Receipt field notes

- **`record_boundary.canonical_write_violation`** — `true` if `--out` pointed at a forbidden path; no file is written there.
- **`record_boundary.canonical_paths_written`** — Always empty for this harness (it does not write Record paths).
- **`gate_snippet.text`** — Copy of snippet content when read successfully (WORK-only paste aid).
