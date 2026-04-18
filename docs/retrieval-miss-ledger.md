# Retrieval-miss ledger

Lightweight, non-canonical observability for retrieval failures in Grace-Mar.

## What it is

An append-only JSONL ledger (`runtime/retrieval-misses/index.jsonl`) that records cases where a retrieval flow — prepared-context assembly, evidence lookup, artifact lookup, or notebook/thread lookup — failed to surface expected material.

Each miss is classified with a small failure taxonomy and stored for later debugging and pattern analysis.

## What it is NOT

- **Not Record.** Does not touch SELF, EVIDENCE, SKILLS, SELF-LIBRARY, or `recursion-gate.md`.
- **Not promotion logic.** Does not stage candidates, auto-merge, or mutate canonical surfaces.
- **Not canonical truth.** A miss record is a debugging observation, not a durable fact about the companion.
- **Not a governance lane.** No approval workflow; no companion gate. Just structured notes about retrieval failures.
- **Not vector search / MCP / hybrid retrieval.** The ledger records misses; it does not build a retrieval engine.

## Failure taxonomy (v1)

| Class | Meaning |
|---|---|
| `vocabulary_mismatch` | Relevant material exists but query terms did not match how it was stored |
| `scope_mismatch` | Retrieval searched the wrong lane, domain, or surface |
| `stale_ranking` | Relevant result exists but ranked too low to surface |
| `missing_content` | Expected content is truly absent from searchable surfaces |
| `aggregation_failure` | Relevant pieces exist separately but were not combined into a useful answer |
| `unknown` | Insufficient evidence to classify |

## Retrieval surfaces (v1)

| Surface | What it covers |
|---|---|
| `prepared_context` | Context-assembly scripts (e.g. `build_context_from_observations.py`, `strategy_context.py`) |
| `evidence_lookup` | Searching or referencing EVIDENCE entries (`self-archive.md`, evidence indexes) |
| `artifact_lookup` | Looking up derived artifacts (`artifacts/`, skill cards, compressed lane output) |
| `notebook_lookup` | Strategy-notebook, thread, or session retrieval (e.g. `lane_search.py`, timeline queries) |

## Schema

`schema-registry/retrieval-miss.v1.json` — JSON Schema (Draft 2020-12) for miss records.

Required fields: `miss_id`, `timestamp`, `retrieval_surface`, `query`, `failure_class`.

Optional fields: `expected_target`, `notes`, `related_paths`, `lane_or_context`, `recorded_by`.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/runtime/log_retrieval_miss.py` | Append a miss record (CLI) |
| `scripts/runtime/summarize_retrieval_misses.py` | Count by failure class and surface |

### Logging a miss

```bash
python scripts/runtime/log_retrieval_miss.py \
  --surface prepared_context \
  --query "Jiang lecture on sovereignty" \
  --failure-class vocabulary_mismatch \
  --expected-target "research/external/work-jiang/lectures/vol-iii/lecture-42.md" \
  --notes "Query used 'sovereignty'; content indexed under 'zhuquan' (主权)" \
  --lane work-jiang \
  --recorded-by operator
```

### Summarizing

```bash
python scripts/runtime/summarize_retrieval_misses.py
python scripts/runtime/summarize_retrieval_misses.py --since 2026-04-01
python scripts/runtime/summarize_retrieval_misses.py --json
```

## Example records

### Example 1: vocabulary mismatch

```json
{
  "miss_id": "rmiss_20260414T143022Z_a1b2c3d4",
  "timestamp": "2026-04-14T14:30:22Z",
  "retrieval_surface": "prepared_context",
  "query": "Jiang lecture on sovereignty",
  "expected_target": "research/external/work-jiang/lectures/vol-iii/lecture-42.md",
  "failure_class": "vocabulary_mismatch",
  "notes": "Query used 'sovereignty'; content indexed under 'zhuquan'",
  "related_paths": ["research/external/work-jiang/lectures/vol-iii/"],
  "lane_or_context": "work-jiang",
  "recorded_by": "operator"
}
```

### Example 2: aggregation failure

```json
{
  "miss_id": "rmiss_20260415T091500Z_e5f6a7b8",
  "timestamp": "2026-04-15T09:15:00Z",
  "retrieval_surface": "notebook_lookup",
  "query": "Barnes liability framing for Iran sanctions",
  "expected_target": null,
  "failure_class": "aggregation_failure",
  "notes": "Barnes entries in strategy-notebook scattered across 3 days; lane_search returned individual hits but no combined view",
  "related_paths": [
    "docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/",
    "docs/skill-work/work-strategy/strategy-notebook/minds/CIV-MIND-BARNES.md"
  ],
  "lane_or_context": "work-strategy",
  "recorded_by": "operator"
}
```

## Storage

- **Location:** `runtime/retrieval-misses/index.jsonl`
- **Gitignored:** Yes — operator-local data, not committed.
- **Created:** On first log call.
- **Path resolution:** `scripts/runtime/ledger_paths.py` (`retrieval_misses_dir()`, `retrieval_misses_jsonl()`, `retrieval_miss_schema()`).

## Relation to other systems

- Mirrors the `runtime/observations/` pattern (same directory convention, schema-registry, ledger_paths, CLI style).
- Listed in `docs/runtime-vs-record.md` under "Runtime-only and derived."
- Does not replace or duplicate the observation ledger; retrieval misses are a separate concern.
