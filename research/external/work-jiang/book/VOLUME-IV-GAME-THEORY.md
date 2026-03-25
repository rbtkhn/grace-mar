# Predictive History — Volume IV: Game Theory

**Corpus:** `series: game-theory` in `metadata/sources.yaml`; `source_id` `gt-01` … `gt-15`; curated files `lectures/game-theory-NN-*.md` (wired in `build_source_registry.py`, `validate_work_jiang.py`, ASR normalizer).  
**Status:** Part I **sources** are complete for the public **Game Theory #1–#15** run (`@PredictiveHistory`; channel index shows **#1–#15** only at last refresh—re-run index if **#16+** appears). Transcripts ingested and `validate_work_jiang.py` clean. **Book** Part I (draft chapters), per-lecture **analysis** files, **chapter mapping**, and **Part II** evaluation mode remain open.

## Corpus snapshot (registry)

| Range | `source_id` | Lecture path pattern |
|-------|-------------|----------------------|
| Game Theory #1–#15 | `gt-01` … `gt-15` | `lectures/game-theory-NN-*.md` |

Each row: `transcript: complete`, `curated_lecture: complete`, `analysis_path: null`, `chapter_mapping: not_started` until the book lane catches up.

**Book stub (machine-readable):** `metadata/book-architecture.yaml` → key `volume_4_game_theory` (15 chapter placeholders `gt-ch01`–`gt-ch15` → `gt-01`–`gt-15`). Top-level `project` / `book` in that file remain Volume I (Geo-Strategy) for existing renderers until the stub is promoted.

## Volume intent

Volume IV extends the Predictive History multivolume architecture with the working title **Game Theory**. Part I should remain lecture-faithful, and Part II should use an explicit method appropriate to the claim type in this corpus.

## Setup checklist

1. ~~Define series key and corpus boundary in `metadata/sources.yaml`.~~ **Done:** `series: game-theory`, `source_id` `gt-NN`, filenames `lectures/game-theory-NN-*.md`.
2. ~~Establish lecture filename pattern under `lectures/`.~~ **Done:** `game-theory-NN-<slug>.md` with `NN` zero-padded to two digits, matching `episode` in YAML.
3. Declare Part I chapter mapping policy (one chapter per lecture unless exceptions are documented).
4. Choose Part II evaluation mode:
   - prediction adjudication, or
   - divergence analysis, or
   - a distinct method with criteria.
5. Add chapter box template reference (prediction, divergence, or new box type).

*When new Game Theory uploads ship beyond **#15**, add `gt-16` … in `sources.yaml`, ingest per [WORKFLOW-transcripts.md](../WORKFLOW-transcripts.md), and refresh [CHANNEL-VIDEO-INDEX.md](../../youtube-channels/predictive-history/CHANNEL-VIDEO-INDEX.md).*

## Relation to other volumes

| Volume | Series | Part I close |
|--------|--------|--------------|
| I | Geo-Strategy | Predictions |
| II | Civilization | Divergence |
| III | Secret History | TBD |
| IV | Game Theory | TBD (Part II method; sources #1–#15 ingested) |
| V | Great Books | TBD |

---

*Operator lane — not Voice knowledge until merged through the gate.*
