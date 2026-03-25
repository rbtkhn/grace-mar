# Predictive History — Volume IV: Game Theory

**Corpus:** `series: game-theory` in `metadata/sources.yaml`; `source_id` pattern `gt-01` …; curated files `lectures/game-theory-NN-*.md` (wired in `build_source_registry.py`, `validate_work_jiang.py`, ASR normalizer).  
**Status:** title registered; ingest transcripts as they ship; Part II method still TBD (see setup checklist below).

## Volume intent

Volume IV extends the Predictive History multivolume architecture with the working title **Game Theory**. Part I should remain lecture-faithful, and Part II should use an explicit method appropriate to the claim type in this corpus.

## Setup checklist

1. ~~Define series key and corpus boundary in `metadata/sources.yaml`.~~ **Done:** `series: game-theory`, `source_id` `gt-NN`, filenames `lectures/game-theory-NN-*.md`.
2. Establish lecture filename pattern under `lectures/`.
3. Declare Part I chapter mapping policy (one chapter per lecture unless exceptions are documented).
4. Choose Part II evaluation mode:
   - prediction adjudication, or
   - divergence analysis, or
   - a distinct method with criteria.
5. Add chapter box template reference (prediction, divergence, or new box type).

## Relation to other volumes

| Volume | Series | Part I close |
|--------|--------|--------------|
| I | Geo-Strategy | Predictions |
| II | Civilization | Divergence |
| III | Secret History | TBD |
| IV | Game Theory | TBD (set during setup) |
| V | Great Books | TBD |

---

*Operator lane — not Voice knowledge until merged through the gate.*
