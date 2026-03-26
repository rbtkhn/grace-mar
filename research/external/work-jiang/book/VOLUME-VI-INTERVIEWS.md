# Predictive History — Volume VI: Interviews

**Scope:** Volume VI includes **curated long-form interviews** with Jiang Xueqin — **any host or channel** (not limited to Predictive History–hosted shows). Same chapter pattern as below.

**Corpus:** `series: interviews` in `metadata/sources.yaml`; `source_id` `vi-NN` matches **`interviews-NN`** (same index as `build_source_registry.py`). Curated files `lectures/interviews-NN-*.md` (wired in `build_source_registry.py`, `validate_work_jiang.py`, ASR normalizer).  
**Status:** Part I **sources** are long-form **interview** transcripts (operator-supplied); **one chapter per interview** unless exceptions are documented in `metadata/source-map.yaml`.

**Chapter order:** `interviews-NN` and **Interviews #N** follow **YouTube publication date** (earliest → latest). **`vi-NN` = chapter number** (first published video = `vi-01` = `interviews-01`).

## Corpus snapshot (registry)

| Range | `source_id` | Lecture path pattern |
|-------|-------------|----------------------|
| Interviews #1–#N | `vi-01` … `vi-NN` | `lectures/interviews-NN-*.md` (`NN` = chronological order by upload date) |

**Analysis memos:** `{video_id}-interviews-NN-analysis.md` when a YouTube `watch?v=` link exists in the lecture file; otherwise `interviews-NN-analysis.md` (no leading video id).

## Relation to other volumes

| Volume | Series | Notes |
|--------|--------|--------|
| VI | Interviews | Curated long-form **dialogue / Q&A** (any show); same **Predictive History** intellectual frame as lecture volumes |

See also [VOLUME-IV-GAME-THEORY.md](VOLUME-IV-GAME-THEORY.md) for the multivolume **stub** pattern.
