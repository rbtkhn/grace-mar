# work-jiang — external research

Operator-curated **source texts** for the Jiang book/site project (not Voice knowledge until merged through the gate). The book line is **Predictive History** — a **multivolume** work with **one volume per lecture series**; the material in this tree is **Volume 1 (Geo-Strategy)** unless a path or note names another series.

| Kind | Path |
|------|------|
| Lecture notes + transcripts | [lectures/](lectures/) — **Geo-Strategy** **#1–#12** (e.g. [#1](lectures/geo-strategy-01-iran-strategy-matrix-2024-04-24.md) … [#12](lectures/geo-strategy-12-psychohistory-the-science-of-imagining-the-future.md)); **Civilization** series — `civilization-*.md` + `civ-*` rows in `metadata/sources.yaml` (separate volume; see [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md) § Multi-series) |
| Book / thesis / queue | [BOOK-ARCHITECTURE.md](BOOK-ARCHITECTURE.md), [THESIS-MAP.md](THESIS-MAP.md), [CHAPTER-QUEUE.md](CHAPTER-QUEUE.md), [STATUS.md](STATUS.md), [metadata/](metadata/) |
| Book front matter | [PREFACE.md](PREFACE.md), [INTRODUCTION.md](INTRODUCTION.md) |
| Concept dictionary | [CONCEPT-DICTIONARY.md](CONCEPT-DICTIONARY.md), `metadata/concepts.yaml`, `metadata/concept-mentions.yaml` |
| Claims ledger | [CLAIMS-OVERVIEW.md](CLAIMS-OVERVIEW.md), [claims/registry/claims.jsonl](claims/registry/claims.jsonl), [claims/README.md](claims/README.md) |
| Chapter evidence packs | [evidence-packs/](evidence-packs/) — one file per book chapter (`ch01.md` …) |
| Karpathy / No Priors (work-dev, not Jiang) | See [work-dev research-no-priors-karpathy-end-of-coding.md](../../docs/skill-work/work-dev/research-no-priors-karpathy-end-of-coding.md) and [research/external/work-dev/transcripts/](../work-dev/transcripts/) |
| Channel machine pulls | [../youtube-channels/predictive-history/](../youtube-channels/predictive-history/) |
| Transcript intake & analysis workflow | [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md) |
| CIV-MEM analytic lens (conditions, institutions, seams) | [CIV-MEM-LENS.md](CIV-MEM-LENS.md) |
| Influence over time (metrics snapshots) | [influence-tracking/README.md](influence-tracking/README.md) |
| Prediction accuracy (forecast registry) | [prediction-tracking/README.md](prediction-tracking/README.md) |
| Divergence from mainstream (comparison registry) | [divergence-tracking/README.md](divergence-tracking/README.md) |
| Quotation bank (rendered) | [QUOTE-BANK.md](QUOTE-BANK.md), `metadata/quotes.yaml` |
| Counter-readings | [COUNTER-READINGS.md](COUNTER-READINGS.md), [counter-readings/README.md](counter-readings/README.md) |
| Intellectual chronology | [INTELLECTUAL-CHRONOLOGY.md](INTELLECTUAL-CHRONOLOGY.md), `metadata/chronology.yaml` |

See [users/grace-mar/work-jiang.md](../../../users/grace-mar/work-jiang.md) for project purpose and method.

## Boundaries (membrane)

Normative rules for this tree — **canonical here**; do not restate long policy in `users/grace-mar/work-jiang.md` except short pointers.

| May cross | Must stay separate |
|-----------|-------------------|
| **Operator research → book/site artifacts** — YAML, renders, evidence packs, dashboards | **Record / Voice / IX** — nothing here is companion truth until it passes [RECURSION-GATE](../../../users/grace-mar/recursion-gate.md) and merge scripts (see [AGENTS.md](../../../AGENTS.md)) |
| **Curated layer** — hand-edited `metadata/quotes.yaml`, `metadata/chronology.yaml`, claims registry | **Scored noise** — `metadata/quote-candidates.yaml` is machine-assist only; do not treat as polished quotations |
| **Argument layer** — concepts, claims, thesis links, packs | **Comparative layer** — quotes, counter-readings, chronology — keep generators and validators in sync; do not skip comparative validators if you touched that YAML |

**Enforcement:** Run the [production pipeline](#production-pipeline-book--site) after metadata or script edits. `validate_work_jiang.py`, `validate_argument_layer.py`, and `validate_comparative_layer.py` are the membrane — treat failures like CI failures before stacking more changes.

**Repo-wide context:** How grace-mar relates to template and other instance lanes (not Jiang-specific) lives in [docs/audit-boundary-grace-mar-companion-xavier-companion-self.md](../../../docs/audit-boundary-grace-mar-companion-xavier-companion-self.md).

**Session:** If a thread edits `users/grace-mar/` (SELF, gate, pipeline) or merges narrative into companion-facing Record files, run `python3 scripts/harness_warmup.py -u grace-mar` once and paste the output in that thread.

**New agent thread:** [bootstrap/work-jiang-bootstrap.md](../../bootstrap/work-jiang-bootstrap.md) — paste-in checklist, read order, verify block reference.

## Production pipeline (book / site)

From repo root (requires `pyyaml`, e.g. `pip install -r requirements-dev.txt`):

```bash
python3 scripts/work_jiang/build_source_registry.py
python3 scripts/work_jiang/link_supporting_registries.py
python3 scripts/work_jiang/extract_concept_mentions.py
python3 scripts/work_jiang/render_concept_dictionary.py
python3 scripts/work_jiang/link_claims_to_thesis.py
python3 scripts/work_jiang/render_claims_overview.py
python3 scripts/work_jiang/render_book_architecture.py
python3 scripts/work_jiang/render_thesis_map.py
python3 scripts/work_jiang/render_chapter_queue.py
python3 scripts/work_jiang/build_all_evidence_packs.py
python3 scripts/work_jiang/render_status_dashboard.py
python3 scripts/work_jiang/extract_quote_candidates.py
python3 scripts/work_jiang/render_quote_bank.py
python3 scripts/work_jiang/link_quotes_to_chapters.py
python3 scripts/work_jiang/render_counter_readings.py
python3 scripts/work_jiang/link_counter_readings.py
python3 scripts/work_jiang/render_intellectual_chronology.py
python3 scripts/work_jiang/validate_work_jiang.py --require-analysis-frontmatter
python3 scripts/work_jiang/validate_argument_layer.py
python3 scripts/work_jiang/validate_comparative_layer.py
python3 scripts/work_jiang/check_source_coverage.py          # add --strict when ready
python3 scripts/work_jiang/scaffold_outputs.py               # chapter/site stubs (skip if exists)
```

**Argument layer (concepts + claims + packs):** edit `metadata/concepts.yaml` and `claims/registry/claims.jsonl`; keep `linked_claim_ids` on each thesis subclaim in `metadata/thesis-map.yaml` in sync with claims. Single pack: `python3 scripts/work_jiang/build_evidence_pack.py --chapter ch02`.

**Comparative layer (quotes + counter-readings + chronology):** curated `metadata/quotes.yaml` (bootstrap helper: `python3 scripts/work_jiang/bootstrap_quotes_from_candidates.py` after refreshing candidates); renders [QUOTE-BANK.md](QUOTE-BANK.md), [COUNTER-READINGS.md](COUNTER-READINGS.md), [INTELLECTUAL-CHRONOLOGY.md](INTELLECTUAL-CHRONOLOGY.md); link YAML under `metadata/chapter-quote-links.yaml` and `metadata/counter-reading-links.yaml`. CI runs `validate_comparative_layer.py` after the argument-layer validator.

Optional: `python3 scripts/work_jiang/normalize_analysis_frontmatter.py --write` after adding analysis memos. Optional: `python3 scripts/work_jiang/update_work_jiang_lane.py --write` to sync `users/grace-mar/work-jiang.md` WORK Container status.
