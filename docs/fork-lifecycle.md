# Fork lifecycle (fork history)

Grace-Mar treats each cognitive fork under `users/<fork_id>/` as a **versioned, evidence-grounded record** with an explicit lifecycle.

## Concepts

- **Fork history** — product language for how the Record evolved (sessions, merges, snapshots).
- **Lineage** — append-only engineering ledger: `fork-lineage.jsonl`.

## Files

| File | Role |
|------|------|
| `fork_state.json` | Current phase, counters, drift snapshot, policies |
| `fork-lineage.jsonl` | One JSON object per line (session_started, merge_applied, snapshot_created, …) |
| `sessions/YYYY/MM/session-<id>.json` | Lifecycle session manifest |
| `snapshots/<tag>.json` | Snapshot manifest (checksums, git commit, drift) |
| `drift-report.json` | Heuristic drift score and components |

## Phases

Valid phases: `seed`, `interact`, `diverge`, `merge_pending`, `snapshotted`. Transitions are enforced in `src/grace_mar/fork_lifecycle.py`.

## CLI

Global `--user` must appear **before** the subcommand:

```bash
python scripts/fork_lifecycle.py -u grace-mar init
python scripts/fork_lifecycle.py -u grace-mar begin-session --channel telegram
python scripts/fork_lifecycle.py -u grace-mar end-session --session-id SES-YYYYMMDD-NNN
python scripts/fork_lifecycle.py -u grace-mar measure-drift
python scripts/fork_lifecycle.py -u grace-mar snapshot --tag my-tag --no-git-tag
python scripts/fork_lifecycle.py -u grace-mar status
```

## Merge receipts

`process_approved_candidates.py` emits receipts with `receipt_id` (`MR-####`), `session_ids`, `fork_phase_before` / `fork_phase_after`, `lineage_summary`, and a `receipt_hash` chain.

Optional **`--require-lifecycle-fields`** requires each merged candidate YAML to include:

- `origin` (e.g. `session_interaction`, `operator_observation`)
- `lineage_class` (e.g. `fork_native`, `real_world_update`)
- `session_id` **or** `operator_source`

## Integrity

```bash
python scripts/validate-integrity.py --user grace-mar --strict-lifecycle --json
```

`--strict-lifecycle` enforces `fork_state.json`, pending candidate lineage fields, and drift report shape where applicable.

## Gated edits

Commit messages for direct edits to canonical files (`self.md`, **`self-archive.md`**, `self-skills.md`, `skills.md`, `self-evidence.md`, `self-library.md`, …) must include `[gated-merge]`, `process_approved_candidates`, `MERGE-RECEIPT:`, or `SNAPSHOT:` — see `scripts/check_gated_record_commit_msg.py`.
