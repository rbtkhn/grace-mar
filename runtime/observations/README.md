# Runtime observations

This directory stores **non-canonical** runtime observations for Grace-Mar work lanes.

**Normative workflow and rules:** [docs/runtime/memory-retrieval.md](../../docs/runtime/memory-retrieval.md) (progressive disclosure, governance, commands). This README is a **quick orientation** for the ledger directory only.

## Purpose

- Capture compact, auditable notes from active work (manual, notebook, compression, evidence pointers, etc.).
- Support **search → timeline → expansion → prepared context** over the append-only ledger:
  - **`scripts/runtime/lane_search.py`** — compact index (scored, filterable; no full `notes` in default output).
  - **`scripts/runtime/lane_timeline.py`** — chronological window around an `--anchor` or a `--query` hit (same-lane by default).
  - **`scripts/runtime/expand_observations.py`** — bounded fields for explicit `--id` values (JSON or Markdown).
  - **`scripts/prepared_context/build_context_from_observations.py`** — lane-scoped Markdown bundle (see [observation-expansion.md](../../docs/runtime/observation-expansion.md)).
- Preserve provenance for possible future gate candidates (staging still requires human approval).

## Non-goals

- This is **not** a canonical Record surface (not SELF, SELF-LIBRARY, SKILLS, or EVIDENCE).
- This does **not** update `self.md`, `self-archive.md`, `self-skills.md`, or `bot/prompt.py`.
- This does **not** auto-stage changes into `recursion-gate.md`.
- This must **not** write instruction files (e.g. `CLAUDE.md`) outside this tree.

## Storage

- `index.jsonl` — append-only ledger; **one JSON object per line**, validated against `schema-registry/runtime-observation.v1.json`. **Gitignored** by default (operator-local); created on first log.
- Log entries with: `python scripts/runtime/log_observation.py --help`
- Tests may set **`GRACE_MAR_RUNTIME_LEDGER_ROOT`** so the ledger path is isolated; schema still loads from the repo.

## Design rules (summary)

- **Non-canonical** — Not SELF, SELF-LIBRARY, SKILLS, or EVIDENCE; no auto-staging into `recursion-gate.md`; lane-scoped by default; logger writes only to this ledger (no ambient instruction files). **Compact, not exhaustive.**

Full doctrine, cross-lane flags, and commands: [docs/runtime/memory-retrieval.md](../../docs/runtime/memory-retrieval.md). Runtime vs Record map: [docs/runtime-vs-record.md](../../docs/runtime-vs-record.md).
