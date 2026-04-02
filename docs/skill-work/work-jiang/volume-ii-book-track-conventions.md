# Volume II (Civilization) — book-track conventions

Operator WORK — Predictive History. Canonical prose spec: [`research/external/work-jiang/book/VOLUME-II-CIVILIZATION.md`](../../../research/external/work-jiang/book/VOLUME-II-CIVILIZATION.md).

## Naming (locked)

| Item | Convention |
|------|------------|
| YAML block key | `volume_2_civilization` under [`metadata/book-architecture.yaml`](../../../research/external/work-jiang/metadata/book-architecture.yaml) |
| Chapter IDs | `civ-ch01` … `civ-ch60` — one chapter per `civ-NN` source row (two-digit episode) |
| `source_ids` | Exactly `[civ-NN]` matching [`metadata/sources.yaml`](../../../research/external/work-jiang/metadata/sources.yaml) |
| Evidence packs | `evidence-packs/civ-chNN.md` (prefix avoids collision with Volume I `ch01` …) |
| Outline / draft paths | `chapters-volume-ii/civ-chNN/outline.md` and `draft.md` |
| Part II anchor | `part_2.after_chapter: civ-ch60` — begins after last Part I Civilization chapter in this queue |

## Part I / II contract (vs Volume I)

- **Part I end-of-chapter box:** **Divergence** (not predictions). See [`CHAPTER-DIVERGENCE-BOX.md`](../../../research/external/work-jiang/CHAPTER-DIVERGENCE-BOX.md).
- **Part II:** Historiographic divergence — [`PART-II-CIVILIZATION-DIVERGENCE.md`](../../../research/external/work-jiang/book/PART-II-CIVILIZATION-DIVERGENCE.md). Do **not** reuse Geo-Strategy prediction adjudication prose for Volume II.
- Nested `chapter_end_divergence` in `volume_2_civilization` documents this; top-level `chapter_end_predictions` remains Volume I only.

## Rendered artifacts (Volume II)

After `metadata/book-architecture.yaml` edits, run renderers (or `rebuild_all.py`):

| Output | Script |
|--------|--------|
| [`BOOK-ARCHITECTURE-VOLUME-II.md`](../../../research/external/work-jiang/BOOK-ARCHITECTURE-VOLUME-II.md) | [`render_book_architecture.py`](../../../scripts/work_jiang/render_book_architecture.py) |
| [`CHAPTER-QUEUE-VOLUME-II.md`](../../../research/external/work-jiang/CHAPTER-QUEUE-VOLUME-II.md) | [`render_chapter_queue.py`](../../../scripts/work_jiang/render_chapter_queue.py) |

Volume I outputs are unchanged: `BOOK-ARCHITECTURE.md`, `CHAPTER-QUEUE.md`.

## Source map

[`metadata/source-map.yaml`](../../../research/external/work-jiang/metadata/source-map.yaml) `chapter_map` includes every `civ-chNN` → `[civ-NN]` for evidence-pack and validator consistency.

## Regenerating chapter rows

If `civ-*` sources are added or renumbered, regenerate the chapter list with:

`python3 scripts/work_jiang/emit_volume2_chapters_yaml.py`

Then merge the emitted YAML into `volume_2_civilization.book.chapters` (or replace the list) and refresh `source-map.yaml` accordingly.

## Tooling touched for Volume II parity

| Script | Change |
|--------|--------|
| [`arch_chapters.py`](../../../scripts/work_jiang/arch_chapters.py) | New — `all_chapters_flat`, `chapter_by_id`, `all_chapter_ids`, nested `volume_*` keys |
| [`build_evidence_pack.py`](../../../scripts/work_jiang/build_evidence_pack.py) | Resolves chapters across volumes; Volume II open questions / spillover text |
| [`build_all_evidence_packs.py`](../../../scripts/work_jiang/build_all_evidence_packs.py) | Iterates all volumes’ chapters |
| [`render_chapter_queue.py`](../../../scripts/work_jiang/render_chapter_queue.py) | Writes [`CHAPTER-QUEUE-VOLUME-II.md`](../../../research/external/work-jiang/CHAPTER-QUEUE-VOLUME-II.md) |
| [`render_book_architecture.py`](../../../scripts/work_jiang/render_book_architecture.py) | Writes [`BOOK-ARCHITECTURE-VOLUME-II.md`](../../../research/external/work-jiang/BOOK-ARCHITECTURE-VOLUME-II.md) |
| [`render_status_dashboard.py`](../../../scripts/work_jiang/render_status_dashboard.py) | Counts `civ-ch*.md` packs; Volume II subsection |
| [`validate_work_jiang.py`](../../../scripts/work_jiang/validate_work_jiang.py) | `all_chapter_ids` / `all_chapters_flat`; drift check for Volume II renders |
| [`validate_argument_layer.py`](../../../scripts/work_jiang/validate_argument_layer.py) | All chapters; `outline_pending` civ packs scaffold-only; `civ-*` source ids in packs when strict |
| [`validate_comparative_layer.py`](../../../scripts/work_jiang/validate_comparative_layer.py) | `all_chapter_ids` / `all_chapters_flat` for quote links |
| [`create_chapter_scaffold.py`](../../../scripts/work_jiang/create_chapter_scaffold.py) | `chapter_by_id`; `chapters-volume-ii/…` out dir from `outline_path` |

**Still Volume I–only (acceptable until promoted):** [`scaffold_outputs.py`](../../../scripts/work_jiang/scaffold_outputs.py) flat `chapters/*.md` stubs, [`render_analysis_backlog.py`](../../../scripts/work_jiang/render_analysis_backlog.py), [`assemble_context_pack.py`](../../../scripts/work_jiang/assemble_context_pack.py), [`seed_task_manifest.py`](../../../scripts/work_jiang/seed_task_manifest.py), [`update_work_jiang_lane.py`](../../../scripts/work_jiang/update_work_jiang_lane.py), [`validate_book_consistency.py`](../../../scripts/work_jiang/validate_book_consistency.py).

## After Phase 1 pilot (per-source vertical slice)

Use this checklist when bringing a **single** `civ-NN` chapter onto the argument spine (pilot: `civ-01` / `civ-ch01`):

1. **Analysis memo** — Add `analysis/<video_id>-civilization-NN-analysis.md` with front matter (`source_id`, `chapter_candidates`, themes) per [`lecture-analysis-json-schema.md`](lecture-analysis-json-schema.md) and existing Geo memos.
2. **Sources** — In `metadata/sources.yaml`, set `analysis_path` and `status.analysis: complete` for that `source_id`.
3. **Claims** — Append rows to `claims/registry/claims.jsonl` with `source_id`, `analysis_id`, `chapter_candidates: [civ-chNN]`, stable `clm-*` ids, conservative `status`.
4. **Thesis** — Add or extend a subclaim in `metadata/thesis-map.yaml` with **non-empty** `linked_claim_ids` pointing only at real `clm-*` rows (`validate_argument_layer.py` enforces this).
5. **Divergence** — Append a row to `divergence-tracking/registry/divergences.jsonl` (do **not** hand-edit `metadata/divergence-links.yaml`; it is generated).
6. **Registries** — `python3 scripts/work_jiang/link_supporting_registries.py`
7. **Evidence pack** — `python3 scripts/work_jiang/build_evidence_pack.py --chapter civ-chNN`
8. **Renders (cadence)** — `python3 scripts/work_jiang/render_thesis_map.py`, `python3 scripts/work_jiang/render_claims_overview.py` as needed
9. **Verify** — `python3 scripts/work_jiang/validate_work_jiang.py`, `validate_argument_layer.py`, `validate_comparative_layer.py`

**Arc / through-lines (documentation-only):** [`chapters-volume-ii/VOLUME-II-ARC-THROUGH-LINES.md`](../../../research/external/work-jiang/chapters-volume-ii/VOLUME-II-ARC-THROUGH-LINES.md)
