# OB1 Chunking Spike — Query Baseline

Purpose: fixed retrieval baseline for the OB1 chunking spike across `full_file`, `per_section`, and `per_entry`.

## Scoring rubric

- `hit = 1.0` (top result lands in the expected section)
- `partial = 0.5` (result is adjacent or related but not exact)
- `miss = 0.0` (no useful grounding in the expected section)

## Test set (10 fixed queries)

Anchors match current `users/grace-mar/self.md` section headings (reseeded April 2026). If `self.md` structure changes again, update this table in the same PR.

| # | Query | Expected source in `users/grace-mar/self.md` |
|---|---|---|
| 1 | What work rhythm, decision style, and quality bar are documented? | `## II. PREFERENCES` |
| 2 | What family profile is recorded (including explicit empties)? | `## III. FAMILY` |
| 3 | What school or education profile exists? | `## IV. SCHOOL / EDUCATION` |
| 4 | What health-related profile exists? | `## V. HEALTH` |
| 5 | What is the life mission reference and list of intellectual values? | `## VI. PHILOSOPHY` |
| 6 | When was Self reseeded and what companion-freeze pointer exists? | `## VII. METADATA` |
| 7 | How do gated approvals merge into the Record? | `## VIII. GATED APPROVED LOG` |
| 8 | What knowledge entries are listed in IX-A? | `## IX-A. KNOWLEDGE` |
| 9 | What curiosity labels and lanes appear in IX-B? | `## IX-B. CURIOSITY` |
| 10 | What personality observations are listed in IX-C? | `## IX-C. PERSONALITY` |

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
| 1 | rhythm / decision / quality bar | `## II. PREFERENCES` |  |  |
| 2 | family profile | `## III. FAMILY` |  |  |
| 3 | school / education | `## IV. SCHOOL / EDUCATION` |  |  |
| 4 | health profile | `## V. HEALTH` |  |  |
| 5 | mission + intellectual values | `## VI. PHILOSOPHY` |  |  |
| 6 | reseed + companion freeze | `## VII. METADATA` |  |  |
| 7 | gated merge path | `## VIII. GATED APPROVED LOG` |  |  |
| 8 | IX-A knowledge entries | `## IX-A. KNOWLEDGE` |  |  |
| 9 | IX-B curiosity labels | `## IX-B. CURIOSITY` |  |  |
| 10 | IX-C personality observations | `## IX-C. PERSONALITY` |  |  |

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
| 1 | rhythm / decision / quality bar | `## II. PREFERENCES` |  |  |
| 2 | family profile | `## III. FAMILY` |  |  |
| 3 | school / education | `## IV. SCHOOL / EDUCATION` |  |  |
| 4 | health profile | `## V. HEALTH` |  |  |
| 5 | mission + intellectual values | `## VI. PHILOSOPHY` |  |  |
| 6 | reseed + companion freeze | `## VII. METADATA` |  |  |
| 7 | gated merge path | `## VIII. GATED APPROVED LOG` |  |  |
| 8 | IX-A knowledge entries | `## IX-A. KNOWLEDGE` |  |  |
| 9 | IX-B curiosity labels | `## IX-B. CURIOSITY` |  |  |
| 10 | IX-C personality observations | `## IX-C. PERSONALITY` |  |  |

Result summary:

- Total score: `__/10`
- Precision proxy: `__`
- Repeated misses:

## Third pass worksheet — `per_entry`

Status: blocked pending exporter implementation (`scripts/export_open_brain_bundle.py` is not present in this repo yet).

When exporter is available, run:

`python3 scripts/export_open_brain_bundle.py -u grace-mar -o ob1-export/ --chunk-strategy per_entry`

Then evaluate retrieval against the same 10 fixed queries above.

| # | Query (short) | Expected section | Score | Notes |
|---|---|---|---:|---|
| 1 | rhythm / decision / quality bar | `## II. PREFERENCES` |  |  |
| 2 | family profile | `## III. FAMILY` |  |  |
| 3 | school / education | `## IV. SCHOOL / EDUCATION` |  |  |
| 4 | health profile | `## V. HEALTH` |  |  |
| 5 | mission + intellectual values | `## VI. PHILOSOPHY` |  |  |
| 6 | reseed + companion freeze | `## VII. METADATA` |  |  |
| 7 | gated merge path | `## VIII. GATED APPROVED LOG` |  |  |
| 8 | IX-A knowledge entries | `## IX-A. KNOWLEDGE` |  |  |
| 9 | IX-B curiosity labels | `## IX-B. CURIOSITY` |  |  |
| 10 | IX-C personality observations | `## IX-C. PERSONALITY` |  |  |

Result summary:

- Total score: `__/10`
- Precision proxy: `__`
- Repeated misses:
