# Predictive History — Volume V: Great Books

**Corpus:** `metadata/sources.yaml` — `gb-01` … `gb-08` (Great Books **#1–#8**); curated files `lectures/great-books-NN-*.md`  
**Status:** ingest through **#8** complete (registry + tooling); Part I chapter mapping and Part II method still open.

## Volume intent

Volume V extends the Predictive History multivolume architecture with the working title **Great Books**. Part I should preserve lecture order and argument flow, while Part II should apply an explicit and documented evaluation method.

## Setup checklist

1. ~~Define series key and corpus boundary in `metadata/sources.yaml`.~~ Done — `series: great-books`, `gb-*`, through **#8** in registry.
2. ~~Establish lecture filename pattern under `lectures/`.~~ Done — `great-books-NN-<slug>.md`.
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
| IV | Game Theory | TBD (Part II method; sources #1–#15 ingested) |
| V | Great Books | TBD (set during setup) |

---

*Operator lane — not Voice knowledge until merged through the gate.*
