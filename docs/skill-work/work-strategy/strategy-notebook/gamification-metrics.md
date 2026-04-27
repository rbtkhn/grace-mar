# Strategy notebook — seam / “gamification” trial (WORK only)
<!-- word_count: 200 -->

**Purpose:** Optional **observability** for weave quality and verify-first discipline — **not** a leaderboard. If a metric becomes the target, it stops measuring seam health (Goodhart risk). Prefer **falsifiable watches** in [`forecast-watch-log.md`](forecast-watch-log.md) over raw counts.

## Fields (legacy on-disk index file — v4+)

| Field | Meaning |
|--------|---------|
| **`weave_count`** | Optional manual tally of **outgoing** cross-link targets, or copy from `python3 scripts/knot_seam_metrics.py` (`out_links` column). |
| **`seam_integrity`** | Optional subjective **0–1** self-grade: did registers, scope, and falsifiers stay honest on this page? **Not** comparable across topics. |
| **`qoi_check`**, **`kac_check`** | Optional booleans mirroring the **strategy-page** template’s **Quality of information** and **Key assumptions** checklists. |

All keys are **optional**; existing rows validate without them.

## Scripts

- **`python3 scripts/validate_knot_index.py`** — schema gate for the legacy on-disk index (filename unchanged on disk).
- **`python3 scripts/knot_seam_metrics.py`** — read-only table: computed outgoing cross-links vs optional `weave_count`. **`--strict-drift`** exits non-zero when YAML `weave_count` disagrees with computed counts (used in CI).

## When **not** to use

- Do **not** optimize **volume** of weaves or **maximize** `weave_count` as a goal.
- Do **not** treat `seam_integrity` as proof of correctness — it is a **reflection** hook only.
