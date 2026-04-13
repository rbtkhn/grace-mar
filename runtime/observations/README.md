# Runtime observations

This directory stores **non-canonical** runtime observations for Grace-Mar work lanes.

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

## Design rules

1. **Runtime only** — Draft memory for operators and agents, not governed truth.
2. **No automatic promotion** — Nothing here merges into the Record without the normal gate pipeline.
3. **Lane-scoped by default** — Each observation has one `lane` string; cross-lane use is explicit in higher-level tools.
4. **No ambient writes** — The logger appends **only** to `runtime/observations/index.jsonl` under the repo.
5. **Compact, not exhaustive** — Deliberate notes, not “capture everything the model does.”

See [docs/runtime-vs-record.md](../../docs/runtime-vs-record.md) for the full runtime vs. Record map.
