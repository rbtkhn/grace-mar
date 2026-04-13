# Runtime memory retrieval

**Normative spec (SSOT)** for the runtime-memory workflow: progressive disclosure order, governance rules, default lane scope ([`runtime/memory_policy.json`](../../runtime/memory_policy.json)), and command surface. Other files under `docs/runtime/` and [`runtime/observations/README.md`](../../runtime/observations/README.md) **supplement** this document (boundaries, safety, or command-specific detail)—avoid restating full doctrine there; link here instead.

Grace-Mar runtime observations support a **progressive disclosure** workflow over `runtime/observations/index.jsonl`:

1. **`lane-search`** — compact index only (IDs, timestamps, lane, `source_kind`, title, one-line summary; optional score in JSON).
2. **`lane-timeline`** — chronological context around a selected observation (same lane by default).
3. **Full observation expansion** — `expand_observations` (explicit IDs; bounded fields) — see [observation-expansion.md](observation-expansion.md).
4. **Prepared-context bundle** — `build_context_from_observations.py` (lane-scoped Markdown, not Record truth).
5. **Provenance-backed gate staging** — `stage_candidate_from_observations.py` (explicit observation lineage into `recursion-gate.md`; see [provenance-staging.md](provenance-staging.md)).
6. **Read hints + memory brief** — `read_hint.py` (soft pre-read hints) and `memory_brief.py` (one bounded Markdown brief: search → timeline → expansion); see [read-hints.md](read-hints.md).

## Design intent

- Reduce token waste (survey before detail).
- Preserve lane boundaries (timeline defaults to the anchor’s lane; cross-lane requires `--cross-lane`).
- Improve auditability of work development without treating runtime rows as canonical Record truth.

## Rules

- Runtime retrieval does **not** mutate SELF, SELF-LIBRARY, SKILLS, or EVIDENCE.
- Runtime retrieval does **not** auto-stage changes into `recursion-gate.md`.
- Cross-lane retrieval must be **explicit** (`lane-search` without `--lane` searches all lanes; `lane-timeline` uses `--cross-lane` for a global chronological pool).
- Compact retrieval comes before full-detail expansion.

This is **operator / WORK scaffolding**, not Record truth. See [runtime/observations/README.md](../../runtime/observations/README.md) and [runtime-vs-record.md](../runtime-vs-record.md).

## Gate candidate and schema identifiers

Staged runtime proposals use **`gate_candidate_id`** values matching `^CANDIDATE-[0-9]{4}$` and YAML **`status: pending`**, per [`schema-registry/recursion-gate-candidate.schema.json`](../../schema-registry/recursion-gate-candidate.schema.json). Sequential four-digit IDs align with the existing gate merge pipeline and human scanning of `recursion-gate.md`.

**Alternatives considered:** Timestamp- or ULID-based IDs sort naturally in raw logs but require coordinated updates to the schema, staging emitters, and merge tooling. Adopt them only through an explicit change to the schema and related scripts—not by mixing formats in one gate file.

**Display vs payload:** Older prose may say “PENDING-REVIEW”; the structured payload uses `status: pending`. Treat the YAML in the gate block as authoritative for automation.

## Code layout and packaging

Runtime retrieval and staging logic live as **importable modules** next to CLIs under [`scripts/runtime/`](../../scripts/runtime/) (for example `observation_store.py`, `ledger_paths.py`). A dedicated installable package (for example `src/grace_mar/runtime/`) is **deferred** until import churn, duplicated test harnesses, or install boundaries justify the migration; until then, `scripts/runtime/` is the subsystem boundary.

## Commands

```bash
# Search (v1 scoring: phrase/term matches, tag bonuses, recency, confidence bump)
python3 scripts/runtime/lane_search.py \
  --lane work-strategy \
  --query "iran negotiation framing" \
  --limit 8

python3 scripts/runtime/lane_search.py \
  --lane history-notebook \
  --query "corridor connectivity" \
  --tag rome \
  --tag corridor \
  --limit 5

# Timeline around an anchor (same lane by default; --before / --after neighbors)
python3 scripts/runtime/lane_timeline.py \
  --anchor obs_20260413T184210Z_a1b2c3d4 \
  --before 2 \
  --after 2

# Resolve anchor from search (top hit unless --pick N)
python3 scripts/runtime/lane_timeline.py \
  --lane work-strategy \
  --query "iran negotiation framing" \
  --before 2 \
  --after 2
```

`--query` may be abbreviated as `-q`. Optional: `--source-kind`, `--since`, `--until` (ISO date-time), `--json` (a **single JSON array** of compact hit objects, each includes `score`; no full `notes` bodies).

`lane_timeline.py`: `--anchor` **or** `--query` (with optional `--lane`, `--pick`, filters); neighbors default to the **same lane** unless `--cross-lane`. JSON mode emits a compact array (no `notes`).

Optional: set `GRACE_MAR_RUNTIME_LEDGER_ROOT` so the ledger path is isolated (tests).

### Efficiency helpers (PR5)

```bash
python3 scripts/runtime/read_hint.py --lane work-strategy --path docs/strategy-notebook.md
python3 scripts/runtime/memory_brief.py --lane work-strategy --query "iran negotiation framing" \
  --output prepared-context/memory-brief.md
```

Details: [read-hints.md](read-hints.md).

## See also (supplements)

- [lane-boundaries.md](lane-boundaries.md) — lane default for higher-level tools (points here for full rules).
- [storage-boundaries.md](storage-boundaries.md) — ledger root and ambient-write safety.
- [observation-expansion.md](observation-expansion.md) — `expand_observations` + `build_context_from_observations`.
- [provenance-staging.md](provenance-staging.md) — `stage_candidate_from_observations.py` and gate blocks.
