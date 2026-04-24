# Letta Adapter Contract

## Status

Runtime complement only.

## Allowed inputs

- Runtime export bundles from `runtime/runtime-complements/exports/`
  (JSON from [`export_runtime_context.py`](../../../scripts/runtime/export_runtime_context.py))
- Operator-provided Letta summary JSON
  (session or observation shape your operator agrees on; must remain valid
  for the import script)
- Example payloads in this adapter folder (safe to copy and edit)

## Allowed outputs

- **Letta seed** JSON under `runtime/runtime-complements/exports/`
  (from [`letta_prepare_seed.py`](../../../scripts/runtime/letta_prepare_seed.py))
- **Inbox** JSON under `runtime/runtime-complements/inbox/`
  when using the import script (not by writing those paths by hand in v1)
- **Runtime observation imports** only through
  [`import_runtime_observation.py`](../../../scripts/runtime/import_runtime_observation.py)
- **Receipts** under `runtime/runtime-complements/receipts/`
  (written by the import script)

## Prohibited actions

- No canonical Record writes
- No direct edits to `users/` Record trees for bulk or surreptitious ingest
- No direct edits to canonical identity, evidence, skill, or library files
  (e.g. `self.md`, `self-archive.md`, `self-skills.md`, `self-library.md`) —
  see [runtime complements doctrine](../../../docs/runtime/runtime-complements.md)
- No direct edits to `recursion-gate.md` (except the normal human-driven
  companion/operator flow outside this adapter)
- No `bot` or prompt edits
- No automatic memory promotion
- No SDK or API dependency in v1
- No Docker service in v1

## Memory block boundary

Letta **memory blocks** (if you map them in a Letta runtime) are **runtime
context** only. They may help a Letta agent stay consistent in-session. They
are not Grace-Mar **SELF**, **EVIDENCE**, **SKILLS**, or **SELF-LIBRARY**.

## Import boundary

All imports of Letta session summaries or observations into Grace-Mar's
**runtime complement** must use:

```bash
python3 scripts/runtime/import_runtime_observation.py --source letta --input <file>
```

The wrapper [`letta_import_summary.py`](../../../scripts/runtime/letta_import_summary.py)
calls that script with `sys.executable` and repo-root resolution. There is
no alternate merge path in v1.

## Review requirement

Every imported Letta summary processed by the import script must result in a
receipt with at least:

- `canonical_surfaces_touched: false`
- `human_review_required: true`
- `promotion_status: runtime_only`
