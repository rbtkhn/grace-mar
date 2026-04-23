# Runtime complements (membrane v1)

**Status:** **Runtime-only** — not the Record, not a substitute for the gate. See [docs/runtime/runtime-complements.md](../../docs/runtime/runtime-complements.md).

## Layout

| Path | Role |
|------|------|
| `exports/` | Generated **context bundles** (JSON) for external runtimes — produced by the export script |
| `inbox/` | **Imported** observations from runtimes (JSON) — produced by the import script |
| `receipts/` | **Receipts** proving each import (JSON) — [schema](../../schema-registry/runtime-complement-receipt.v1.json) |
| `examples/` | **Sample** payloads; not live secrets — safe to commit |

**Guardrails:** Files here are **not** canonical truth. Inbox files are **candidate** material. **Promotion** to SELF, EVIDENCE, SKILLS, or the Voice goes only through the **existing** [recursion-gate](../../users/grace-mar/recursion-gate.md) and companion-approved merge. This directory is **not** a second Record.

## Export (bundle for a runtime)

From repo root:

```bash
python3 scripts/runtime/export_runtime_context.py --help
python3 scripts/runtime/export_runtime_context.py --name demo
python3 scripts/runtime/export_runtime_context.py --name demo --include-doc docs/runtime-vs-record.md
python3 scripts/runtime/export_runtime_context.py --name strategy-console --include-doc docs/skill-work/work-strategy/strategy-notebook/strategy-console/README.md
```

Output path is printed (under `exports/`). Bundles are **allow-listed** by `--include-doc` only; the script does **not** auto-export the whole Record.

## Import (observation from a runtime)

From repo root (examples are committed under `examples/`):

```bash
python3 scripts/runtime/import_runtime_observation.py --source letta --input runtime/runtime-complements/examples/letta-session-summary.example.json
python3 scripts/runtime/import_runtime_observation.py --source mem0 --input runtime/runtime-complements/examples/mem0-quick-recall.example.json
python3 scripts/runtime/import_runtime_observation.py --source thoth --input runtime/runtime-complements/examples/thoth-approval-pattern.example.json
```

Both **inbox** and **receipts** paths are printed. **`canonical_surfaces_touched`** is always **false**; **`human_review_required`** is **true**; **`promotion_status`** defaults to **runtime_only**.

## What not to do

- Do not treat `inbox/` as merged evidence.
- Do not point vendor SDKs at `users/` for direct write.
- Do not add Docker or required cloud services here — this folder is a **file-based membrane** only in v1.

## See also

- [import_runtime_observation.py](../../scripts/runtime/import_runtime_observation.py) · [export_runtime_context.py](../../scripts/runtime/export_runtime_context.py) · [runtime-complements.md](../../docs/runtime/runtime-complements.md)
