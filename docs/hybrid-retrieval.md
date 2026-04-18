# Hybrid retrieval layer

Lightweight, non-canonical ranked search across Grace-Mar's runtime surfaces.

## What it is

A single CLI (`scripts/runtime/hybrid_retrieve.py`) that dispatches queries to the appropriate non-canonical data source, scores results with a consistent lexical + recency formula, and returns ranked results with enough metadata for debugging.

## What it is NOT

- **Not Record.** Does not touch SELF, EVIDENCE, SKILLS, SELF-LIBRARY, or `recursion-gate.md`.
- **Not promotion logic.** Does not stage candidates, auto-merge, or mutate canonical surfaces.
- **Not canonical truth.** Search results are retrieval aids, not durable facts.
- **Not a vector database.** No embedding model, no vector store, no external search backend.
- **Not a replacement** for existing search scripts (`lane_search.py`, `search_evidence.py`). Those continue to work independently; this layer unifies them behind a consistent interface.

## v1 component status

| Component | Status | Implementation |
|---|---|---|
| **Lexical scoring** | Active | TF-IDF cosine (evidence, artifacts, notebook) or keyword match (observations) — stdlib-only |
| **Semantic scoring** | Stub | `hybrid_scoring.semantic_score()` returns 0.0; clean interface for future activation |
| **Recency influence** | Active | 7-day linear decay from timestamps (ISO strings or file mtime) |

## Scoring formula

```
final = w_lex * lexical + w_sem * semantic + w_rec * recency
```

Default weights: `(0.80, 0.15, 0.05)` — tunable via `--weights`.

When semantic scoring is unavailable (v1), lexical weight automatically absorbs the semantic share: effective weights become `(0.95, 0.00, 0.05)`.

All lexical scores are min-max normalised to 0-1 within each query's result set before combination.

## Surfaces (v1)

| Surface | Data source | Lexical method | Recency source |
|---|---|---|---|
| `prepared_context` | `runtime/observations/index.jsonl` | `search_scoring.score_observation()` (keyword + tag + confidence) | Observation timestamp |
| `evidence_lookup` | `users/<id>/self-archive.md` | `search_evidence.search()` (TF-IDF + cosine) | Entry date |
| `artifact_lookup` | `artifacts/**/*.{md,json,yaml}` | TF-IDF cosine over tokenised file content | File mtime |
| `notebook_lookup` | `docs/skill-work/work-strategy/strategy-notebook/chapters/**/*.md` | TF-IDF cosine over tokenised file content | File mtime |

## Usage

### Basic search

```bash
python scripts/runtime/hybrid_retrieve.py \
  --surface prepared_context \
  --query "Jiang sovereignty lecture"
```

### JSON output with custom weights

```bash
python scripts/runtime/hybrid_retrieve.py \
  --surface evidence_lookup \
  --query "swimming" \
  --top-k 3 \
  --weights "0.70,0.20,0.10" \
  --json
```

### Disable recency

```bash
python scripts/runtime/hybrid_retrieve.py \
  --surface notebook_lookup \
  --query "Iran sanctions framing" \
  --use-recency off
```

### Log a miss when results are sparse

```bash
python scripts/runtime/hybrid_retrieve.py \
  --surface artifact_lookup \
  --query "skill card for work-strategy" \
  --log-miss
```

When `--log-miss` is set and results are fewer than `--top-k`, a retrieval-miss record is appended to `runtime/retrieval-misses/index.jsonl` with `failure_class: unknown` for later operator classification.

## Relationship to the retrieval-miss ledger

- The **miss ledger** (PR 1) records and classifies retrieval failures for pattern analysis.
- The **hybrid retrieval layer** (this, PR 2) improves retrieval quality by combining lexical, semantic, and recency signals.
- Neither affects canonical promotion. They are complementary: hybrid retrieval reduces misses; the miss ledger diagnoses remaining failures.
- The `--log-miss` flag bridges the two: when hybrid retrieval falls short, it can automatically record a miss for debugging.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/runtime/hybrid_retrieve.py` | Main CLI — surface dispatch, ranked results |
| `scripts/runtime/hybrid_scoring.py` | Shared scoring: `HybridResult`, `combine_scores()`, `semantic_score()` (stub), recency helpers |

## Adding semantic scoring (future)

To activate semantic scoring:

1. Implement `hybrid_scoring.semantic_score(query, text)` to return a 0-1 similarity value.
2. Set `hybrid_scoring.semantic_available()` to return `True`.
3. The scoring formula will automatically use the semantic weight instead of redistributing it to lexical.

No other changes are needed — the combination logic, CLI flags, and output format already support semantic scores.

## PR 3 recommendation (not implemented)

Chunked long-document retrieval: split large `.md` files (lectures, chapters) into overlapping chunks before scoring, improving recall for long documents where term-overlap dilutes across the full file.
