# Predictive History — Volume IV: Game Theory

**Corpus:** `series: game-theory` in `metadata/sources.yaml`; `source_id` `gt-01` … `gt-19`; curated files `lectures/game-theory-NN-*.md` (wired in `build_source_registry.py`, `validate_work_jiang.py`, ASR normalizer).  
**Status:** Part I **sources** include **Game Theory #1–#19** (`@PredictiveHistory`; **#19** ingested 2026-04-08 with YouTube auto-captions). **`gt-19` analysis** memo exists (**draft** quality — expand claims / registry on next pass). **Book** Part I (draft chapters) and **Part II** evaluation mode remain open.

## Corpus snapshot (registry)

| Range | `source_id` | Lecture path pattern |
|-------|-------------|----------------------|
| Game Theory #1–#19 | `gt-01` … `gt-19` | `lectures/game-theory-NN-*.md` |

**Per-row status (`metadata/sources.yaml`):** For **`gt-01`–`gt-18`**, `transcript` and `curated_lecture` are **complete**, **`chapter_mapping: complete`**, and **`analysis: complete`** with on-disk memos under **`analysis/{video_id}-game-theory-NN-analysis.md`**. For **`gt-19`**, transcript, curated lecture, and on-disk **analysis** memo are **complete** (`analysis/0HYET47Cc-E-game-theory-19-analysis.md`; operator marked **`quality_level: draft`**). **Book** Part I (draft chapters), **comparative layer**, and **Part II** evaluation mode remain open.

**Book stub (machine-readable):** `metadata/book-architecture.yaml` → key `volume_4_game_theory` (Part I chapters `gt-ch01`–`gt-ch19` mapped to `gt-01`–`gt-19`; **`part_2.after_chapter: gt-ch19`**). Top-level `project` / `book` in that file remain Volume I (Geo-Strategy) for existing renderers where noted.

## Volume intent

Volume IV extends the Predictive History multivolume architecture with the working title **Game Theory**. Part I should remain lecture-faithful, and Part II should use an explicit method appropriate to the claim type in this corpus.

## Setup checklist

1. ~~Define series key and corpus boundary in `metadata/sources.yaml`.~~ **Done:** `series: game-theory`, `source_id` `gt-NN`, filenames `lectures/game-theory-NN-*.md`.
2. ~~Establish lecture filename pattern under `lectures/`.~~ **Done:** `game-theory-NN-<slug>.md` with `NN` zero-padded to two digits, matching `episode` in YAML.
3. ~~Declare Part I chapter mapping policy (one chapter per lecture unless exceptions are documented).~~ **Done (default):** one Part I chapter per lecture; `gt-ch01`–`gt-ch19` ↔ `gt-01`–`gt-19` in `source-map.yaml` and `book-architecture.yaml`.
4. Choose Part II evaluation mode:
   - prediction adjudication, or
   - divergence analysis, or
   - a distinct method with criteria.
5. Add chapter box template reference (prediction, divergence, or new box type).

*When new Game Theory uploads ship beyond the current run, add `gt-NN` in `sources.yaml`, ingest per [WORKFLOW-transcripts.md](../WORKFLOW-transcripts.md), and refresh [CHANNEL-VIDEO-INDEX.md](../../youtube-channels/predictive-history/CHANNEL-VIDEO-INDEX.md).*

## Relation to other volumes

| Volume | Series | Part I close |
|--------|--------|--------------|
| I | Geo-Strategy | Predictions |
| II | Civilization | Divergence |
| III | Secret History | TBD |
| IV | Game Theory | TBD (Part II method; sources **#1–#19** ingested; **#19** analysis draft) |
| V | Great Books | TBD |

---

*Operator lane — not Voice knowledge until merged through the gate.*
