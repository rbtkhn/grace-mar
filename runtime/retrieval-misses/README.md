# Retrieval-miss ledger

This directory stores **non-canonical** retrieval-miss records for debugging and observability.

## Purpose

- Record retrieval failures across non-canonical surfaces (prepared-context assembly, evidence lookup, artifact lookup, notebook/thread lookup).
- Classify misses with a small failure taxonomy for pattern analysis.
- Support debugging and iterative improvement of retrieval flows.

## Non-goals

- This is **not** a canonical Record surface (not SELF, SELF-LIBRARY, SKILLS, or EVIDENCE).
- This does **not** stage, promote, or merge anything into `recursion-gate.md`.
- This does **not** affect canonical promotion logic or governance.
- This does **not** build vector search, MCP, or hybrid retrieval.

## Storage

- `index.jsonl` — append-only ledger; **one JSON object per line**, validated against `schema-registry/retrieval-miss.v1.json`. **Gitignored** by default (operator-local); created on first log.
- Log entries with: `python scripts/runtime/log_retrieval_miss.py --help`
- Summarize with: `python scripts/runtime/summarize_retrieval_misses.py`
- Tests may set **`GRACE_MAR_RUNTIME_LEDGER_ROOT`** so the ledger path is isolated; schema still loads from the repo.

## Design rules

- **Non-canonical** — purely observability; no auto-staging, no Record mutation, no governance lane.
- **Lightweight** — small schema, append-only JSONL, manual or semi-automated recording.
- **Repo-native** — mirrors the `runtime/observations/` pattern exactly.

Full boundary doc: [docs/retrieval-miss-ledger.md](../../docs/retrieval-miss-ledger.md). Runtime vs Record map: [docs/runtime-vs-record.md](../../docs/runtime-vs-record.md).
