# Chunk indexes

This directory stores **non-canonical** generated chunk indexes for large documents.

## Purpose

- Split large markdown files into paragraph-boundary chunks for better retrieval precision.
- Support chunk-aware search via `hybrid_retrieve.py` — score individual sections instead of whole files.
- Preserve source traceability: every chunk records its `source_path`, `start_line`, `end_line`, and `section_hint`.

## Non-goals

- This is **not** a canonical Record surface (not SELF, SELF-LIBRARY, SKILLS, or EVIDENCE).
- This does **not** stage, promote, or merge anything into `recursion-gate.md`.
- This does **not** replace source files — chunks are derived retrieval aids.

## Storage

- `<surface>/<filename>.chunks.jsonl` — one JSON object per chunk per line. **Gitignored** by default (operator-local); generated on demand.
- Generate with: `python scripts/runtime/generate_chunks.py --surface <surface>` (or `--all`)
- Chunks are rebuildable from source files at any time.
- Tests may set **`GRACE_MAR_RUNTIME_LEDGER_ROOT`** so chunk paths are isolated.

## Design rules

- **Non-canonical** — purely retrieval aids; no auto-staging, no Record mutation.
- **Rebuildable** — delete and regenerate at any time from source files.
- **Traceable** — every chunk includes `source_path`, line ranges, and `section_hint`.

Full boundary doc: [docs/chunked-retrieval.md](../../docs/chunked-retrieval.md). Runtime vs Record map: [docs/runtime-vs-record.md](../../docs/runtime-vs-record.md).
