# OB1 Chunking Spike — Query Baseline

Purpose: fixed retrieval baseline for the OB1 chunking spike across `full_file`, `per_section`, and `per_entry`.

## Scoring rubric

- `hit = 1.0` (top result lands in the expected section)
- `partial = 0.5` (result is adjacent or related but not exact)
- `miss = 0.0` (no useful grounding in the expected section)

## Test set (10 fixed queries)

| # | Query | Expected source in `users/grace-mar/self.md` |
|---|---|---|
| 1 | What are Grace-Mar's favorite books and media? | `## II. PREFERENCES` |
| 2 | How does Grace-Mar prefer to write and speak? | `## III. LINGUISTIC STYLE` |
| 3 | What recurring personality patterns are documented? | `## IV. PERSONALITY` |
| 4 | What are the strongest core interests right now? | `## V. INTERESTS` |
| 5 | What values guide difficult decisions? | `## VI. VALUES` |
| 6 | What reasoning style appears during conflict? | `## VII. REASONING PATTERNS` |
| 7 | What family and memory narrative anchors exist? | `## VIII. NARRATIVE` |
| 8 | What knowledge has been added in IX-A recently? | `### IX-A. KNOWLEDGE` |
| 9 | What curiosity threads are active in IX-B? | `### IX-B. CURIOSITY` |
| 10 | What observed behavior changes show up in IX-C? | `### IX-C. PERSONALITY (Observed)` |

## Run sheet

Use this same query set for each chunk strategy:

1. `chunk_strategy=full_file`
2. `chunk_strategy=per_section`
3. `chunk_strategy=per_entry`

For each run, score all 10 queries with the rubric above and compute:

- Total score (max 10)
- Precision proxy (`total / 10`)
- Notes on repeated misses (if any)

## First pass worksheet — `full_file`

Status: blocked pending exporter implementation (`scripts/export_open_brain_bundle.py` is not present in this repo yet).

When exporter is available, run:

`python3 scripts/export_open_brain_bundle.py -u grace-mar -o ob1-export/ --chunk-strategy full_file`

Then evaluate retrieval against the 10 fixed queries above.

| # | Query (short) | Expected section | Score | Notes |
|---|---|---|---:|---|
| 1 | favorites/media | `## II. PREFERENCES` |  |  |
| 2 | writing/speaking style | `## III. LINGUISTIC STYLE` |  |  |
| 3 | personality patterns | `## IV. PERSONALITY` |  |  |
| 4 | active interests | `## V. INTERESTS` |  |  |
| 5 | decision values | `## VI. VALUES` |  |  |
| 6 | conflict reasoning style | `## VII. REASONING PATTERNS` |  |  |
| 7 | family/memory anchors | `## VIII. NARRATIVE` |  |  |
| 8 | IX-A knowledge additions | `### IX-A. KNOWLEDGE` |  |  |
| 9 | IX-B curiosity threads | `### IX-B. CURIOSITY` |  |  |
| 10 | IX-C behavior changes | `### IX-C. PERSONALITY (Observed)` |  |  |

Result summary:

- Total score: `__/10`
- Precision proxy: `__`
- Repeated misses:

## Second pass worksheet — `per_section`

Status: blocked pending exporter implementation (`scripts/export_open_brain_bundle.py` is not present in this repo yet).

When exporter is available, run:

`python3 scripts/export_open_brain_bundle.py -u grace-mar -o ob1-export/ --chunk-strategy per_section`

Then evaluate retrieval against the same 10 fixed queries above.

| # | Query (short) | Expected section | Score | Notes |
|---|---|---|---:|---|
| 1 | favorites/media | `## II. PREFERENCES` |  |  |
| 2 | writing/speaking style | `## III. LINGUISTIC STYLE` |  |  |
| 3 | personality patterns | `## IV. PERSONALITY` |  |  |
| 4 | active interests | `## V. INTERESTS` |  |  |
| 5 | decision values | `## VI. VALUES` |  |  |
| 6 | conflict reasoning style | `## VII. REASONING PATTERNS` |  |  |
| 7 | family/memory anchors | `## VIII. NARRATIVE` |  |  |
| 8 | IX-A knowledge additions | `### IX-A. KNOWLEDGE` |  |  |
| 9 | IX-B curiosity threads | `### IX-B. CURIOSITY` |  |  |
| 10 | IX-C behavior changes | `### IX-C. PERSONALITY (Observed)` |  |  |

Result summary:

- Total score: `__/10`
- Precision proxy: `__`
- Repeated misses:
