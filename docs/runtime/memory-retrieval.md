# Runtime memory retrieval

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

## See also

- [lane-boundaries.md](lane-boundaries.md) — default lane scope for higher-level tools.
- [storage-boundaries.md](storage-boundaries.md) — no ambient instruction files.
- [observation-expansion.md](observation-expansion.md) — `expand_observations` + `build_context_from_observations`.
