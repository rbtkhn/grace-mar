# work-jiang — external research

Operator-curated **source texts** for the Jiang book/site project (not Voice knowledge until merged through the gate).

| Kind | Path |
|------|------|
| Lecture notes + transcripts | [lectures/](lectures/) — Geo-Strategy **#1–#12** only (e.g. [Geo-Strategy #1](lectures/geo-strategy-01-iran-strategy-matrix-2024-04-24.md) … [#12 — Psychohistory (END)](lectures/geo-strategy-12-psychohistory-the-science-of-imagining-the-future.md)) |
| Book / thesis / queue | [BOOK-ARCHITECTURE.md](BOOK-ARCHITECTURE.md), [THESIS-MAP.md](THESIS-MAP.md), [CHAPTER-QUEUE.md](CHAPTER-QUEUE.md), [STATUS.md](STATUS.md), [metadata/](metadata/) |
| Karpathy / No Priors (work-dev, not Jiang) | See [work-dev research-no-priors-karpathy-end-of-coding.md](../../docs/skill-work/work-dev/research-no-priors-karpathy-end-of-coding.md) and [research/external/work-dev/transcripts/](../work-dev/transcripts/) |
| Channel machine pulls | [../youtube-channels/predictive-history/](../youtube-channels/predictive-history/) |
| Transcript intake & analysis workflow | [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md) |
| CIV-MEM analytic lens (conditions, institutions, seams) | [CIV-MEM-LENS.md](CIV-MEM-LENS.md) |
| Influence over time (metrics snapshots) | [influence-tracking/README.md](influence-tracking/README.md) |
| Prediction accuracy (forecast registry) | [prediction-tracking/README.md](prediction-tracking/README.md) |
| Divergence from mainstream (comparison registry) | [divergence-tracking/README.md](divergence-tracking/README.md) |

See [users/grace-mar/work-jiang.md](../../../users/grace-mar/work-jiang.md) for project purpose and method.

## Production pipeline (book / site)

From repo root (requires `pyyaml`, e.g. `pip install -r requirements-dev.txt`):

```bash
python3 scripts/work_jiang/build_source_registry.py
python3 scripts/work_jiang/link_supporting_registries.py
python3 scripts/work_jiang/render_book_architecture.py
python3 scripts/work_jiang/render_thesis_map.py
python3 scripts/work_jiang/render_chapter_queue.py
python3 scripts/work_jiang/render_status_dashboard.py
python3 scripts/work_jiang/validate_work_jiang.py --require-analysis-frontmatter
python3 scripts/work_jiang/check_source_coverage.py          # add --strict when ready
python3 scripts/work_jiang/scaffold_outputs.py               # chapter/site stubs (skip if exists)
```

Optional: `python3 scripts/work_jiang/normalize_analysis_frontmatter.py --write` after adding analysis memos. Optional: `python3 scripts/work_jiang/update_work_jiang_lane.py --write` to sync `users/grace-mar/work-jiang.md` WORK Container status.
