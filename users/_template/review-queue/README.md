# Template change-review queue (scaffold)

**Default path for routine merges:** **`recursion-gate.md`** (see [identity-fork-protocol.md](../../docs/identity-fork-protocol.md)). The agent stages candidates there; the companion approves; merge runs per instance pipeline.

**This directory** holds **material change-review** artifacts — escalated edits that need structured proposals, decisions, and diffs. It is **not** a second gate and **not** a replacement for `recursion-gate.md`. See [gate-vs-change-review.md](../../docs/gate-vs-change-review.md).

## Canonical filenames (validators)

| File / directory | Role |
|------------------|------|
| `change_review_queue.json` | Queue index |
| `change_event_log.json` | Append-only event log |
| `proposals/` | One JSON file per proposal |
| `decisions/` | Decision records |
| `diffs/` | Identity diffs |

Do **not** rename these to `queue.json` or `event-log.jsonl` — `scripts/validate-change-review.py` expects the names above.

## Empty scaffold

`proposals/`, `decisions/`, and `diffs/` may be empty until the instance adds governed-change artifacts.

```bash
python3 scripts/validate-change-review.py users/_template/review-queue --allow-empty
```

## Docs

- [change-review-validation.md](../../docs/change-review-validation.md)
