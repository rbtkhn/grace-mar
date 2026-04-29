# Review packet template (work-strategy)

**Lane:** WORK (`work-strategy`). **Not** durable Record truth, **not** gate approval, **not** a merge substitute.

## Purpose

A **review packet** is a **derived** handoff artifact that bundles what was run (task intake, declared paths, optional carry receipt, validation JSON, task-shape JSON) into one structured document for **human** review. It mirrors the JSON emitted by [`scripts/work_strategy/build_review_packet.py`](../../../scripts/work_strategy/build_review_packet.py) and exists so serious runs leave a **deterministic** trace without pretending strategic correctness.

See [runtime-vs-record.md](../../runtime-vs-record.md) for canonical vs derived surfaces.

## When to generate

- After a **serious** carry-harness or validator pass when you want a **single** artifact to attach to a thread, ticket, or notebook knot.
- **Optional but encouraged** before gate-prep thinking: use it to see uncertainties and contradictions surfaced by validators **before** drafting paste snippets.

The packet **may still be created** when structural validation was not run; readiness will reflect that (typically `needs_review`).

## Sections A–J (human outline)

These align with the JSON fields in [`schemas/work_strategy_review_packet.schema.json`](../../../schemas/work_strategy_review_packet.schema.json).

| Section | Role | JSON |
|---------|------|------|
| **A — Task statement** | Title and excerpt of the task intake; what job was scoped. | `task` |
| **B — Task shape** | Primary shape, confidence, secondary candidates when a task-shape report exists. | `task_shape` |
| **C — Inputs** | Declared paths (task, sources, artifacts, optional JSON inputs) and existence notes. | `inputs` |
| **D — Handoff summary** | Factual bullets only: paths, counts, statuses — no invented strategy. | `handoff_summary` |
| **E — Uncertainties** | From validator rows (`unresolved_marker_scan`, `task_shape_expectations`) and optional marker scans. | `uncertainties` |
| **F — Contradictions / tension** | From `contradiction_marker_scan` and related signals. | `contradictions` |
| **G — Validator summary** | Overall validation status and notable non-pass checks. | `validation` |
| **H — Gate prep** | Whether a gate snippet path was present and non-empty; paste-only reminder. | `gate_prep` |
| **I — Review readiness** | Aggregated `pass` / `needs_review` / `fail` with a short reason. | `review_readiness` |
| **J — Why this is not canonical** | Explicit membrane: derived WORK artifact; companion gate governs Record merges. | `record_boundary` |

## Related docs

- [carry-harness.md](carry-harness.md) — optional `--build-review-packet` on the harness
- [validator-contract.md](validator-contract.md) — validation JSON shape
- [task-shape-routing.md](task-shape-routing.md) — task-shape JSON shape
- [runtime-vs-record.md](../../runtime-vs-record.md) — Record boundary

## CLI

```bash
python3 scripts/work_strategy/build_review_packet.py --help
```

Typical inputs reuse the same `--task`, `--source`, `--artifact`, and `--gate-snippet` paths as the carry harness, plus optional `--validation-report`, `--task-shape-report`, and `--carry-receipt`.
