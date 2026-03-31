# Template change-review queue (scaffold)

**Default path for routine merges:** **`recursion-gate.md`** (see [identity-fork-protocol.md](../../docs/identity-fork-protocol.md)). The agent stages candidates there; the companion approves; `process_approved_candidates.py` applies merges.

**This directory** holds **material change-review** artifacts — escalated edits that need structured proposals, decisions, and diffs (contradictions, cross-surface moves, policy/prompt shifts). It is **not** a second gate and **not** a replacement for `recursion-gate.md`. See [gate-vs-change-review.md](../../docs/gate-vs-change-review.md) and IFP §4.3 (material change escalation).

## Canonical filenames (validators)

| File / directory | Role |
|------------------|------|
| `change_review_queue.json` | Queue index (schema: `schema-registry/change-review-queue.v1.json`) |
| `change_event_log.json` | Append-only event log (`change-event-log.v1.json`) |
| `proposals/` | One JSON file per proposal (`change-proposal.v1.json`) |
| `decisions/` | Decision records (`change-decision.v1.json`) |
| `diffs/` | Identity diffs (`identity-diff.v1.json`) |

Do **not** rename these to `queue.json` or `event-log.jsonl` — `scripts/validate-change-review.py` expects the names above.

## Empty scaffold

`proposals/`, `decisions/`, and `diffs/` may be empty until the instance adds governed-change artifacts.

```bash
python3 scripts/validate-change-review.py users/_template/review-queue --allow-empty
```

## Pre-decision bundle

When `proposals/` and `diffs/` each have at least one JSON file but `decisions/` is still empty, validate with `--allow-missing-decisions` so strict checks run on artifacts without inventing decision files:

```bash
python3 scripts/validate-change-review.py users/<fork_id>/review-queue --allow-missing-decisions
```

## Live instance

Copy this tree under `users/<fork_id>/review-queue/` when you need change-review parity; keep `userSlug` in the JSON files aligned with `<fork_id>`.

## Docs

- [change-review-validation.md](../../docs/change-review-validation.md)
- [boundary-review-queue.md](../../docs/boundary-review-queue.md)
