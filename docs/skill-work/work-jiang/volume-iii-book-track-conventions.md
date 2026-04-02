# Volume III (Secret History) — book-track conventions

Operator WORK — Predictive History. Canonical prose spec: [`research/external/work-jiang/book/VOLUME-III-SECRET-HISTORY.md`](../../../research/external/work-jiang/book/VOLUME-III-SECRET-HISTORY.md).

## Naming (locked)

| Item | Convention |
|------|------------|
| YAML block key | `volume_3_secret_history` under [`metadata/book-architecture.yaml`](../../../research/external/work-jiang/metadata/book-architecture.yaml) |
| Chapter IDs | `sh-ch01` … `sh-ch28` — one chapter per `sh-NN` source row (two-digit episode) |
| `source_ids` | Exactly `[sh-NN]` matching [`metadata/sources.yaml`](../../../research/external/work-jiang/metadata/sources.yaml) |
| Evidence packs | `evidence-packs/sh-chNN.md` |
| Outline / draft paths | `chapters-volume-iii/sh-chNN/outline.md` and `draft.md` |
| Part II anchor | `part_2.after_chapter: sh-ch28` — begins after last Part I Secret History chapter in this queue |

## Part I / II contract (default)

- **Part I end-of-chapter box:** **Divergence** (mirrors Volume II; not Geo-style prediction scorecards by default). See [`CHAPTER-DIVERGENCE-BOX.md`](../../../research/external/work-jiang/CHAPTER-DIVERGENCE-BOX.md).
- **Part II:** Operator-locked in [`book/VOLUME-III-SECRET-HISTORY.md`](../../../research/external/work-jiang/book/VOLUME-III-SECRET-HISTORY.md) — may add adjudication or hybrid; do not assume Geo registry semantics.

## Rendered artifacts (Volume III)

| Output | Script |
|--------|--------|
| [`BOOK-ARCHITECTURE-VOLUME-III.md`](../../../research/external/work-jiang/BOOK-ARCHITECTURE-VOLUME-III.md) | [`render_book_architecture.py`](../../../scripts/work_jiang/render_book_architecture.py) |
| [`CHAPTER-QUEUE-VOLUME-III.md`](../../../research/external/work-jiang/CHAPTER-QUEUE-VOLUME-III.md) | [`render_chapter_queue.py`](../../../scripts/work_jiang/render_chapter_queue.py) |

## Source map

[`metadata/source-map.yaml`](../../../research/external/work-jiang/metadata/source-map.yaml) `chapter_map` includes every `sh-chNN` → `[sh-NN]` for evidence-pack and validator consistency.

## Regenerating chapter rows

If `sh-*` sources are added or renumbered, regenerate the nested block with:

`python3 scripts/work_jiang/emit_volume3_chapters_yaml.py`

Then merge the emitted YAML into `volume_3_secret_history.book.chapters` (before `volume_4_game_theory`) and refresh `source-map.yaml` accordingly.

## Tooling (Volume III parity)

| Script | Role |
|--------|------|
| [`arch_chapters.py`](../../../scripts/work_jiang/arch_chapters.py) | `volume_3_secret_history` in `VOLUME_BLOCK_KEYS` |
| [`emit_volume3_chapters_yaml.py`](../../../scripts/work_jiang/emit_volume3_chapters_yaml.py) | Emit full nested YAML from `sh-*` sources |
| [`build_evidence_pack.py`](../../../scripts/work_jiang/build_evidence_pack.py) | `sh-ch*` open questions / spillover |
| [`validate_argument_layer.py`](../../../scripts/work_jiang/validate_argument_layer.py) | Evidence packs; `` `sh-NN` `` source ids |
| [`validate_work_jiang.py`](../../../scripts/work_jiang/validate_work_jiang.py) | Drift for Volume III renders |
| [`render_status_dashboard.py`](../../../scripts/work_jiang/render_status_dashboard.py) | Volume III pack counts |

## After Phase 1 pilot (per-source vertical slice)

Same sequence as Volume II (memo → claims → thesis subclaim → divergence JSONL → `link_supporting_registries.py` → evidence pack → validators), with `sh-01` / `sh-ch01` as reference pilot.

**Arc / through-lines:** [`chapters-volume-iii/VOLUME-III-ARC-THROUGH-LINES.md`](../../../research/external/work-jiang/chapters-volume-iii/VOLUME-III-ARC-THROUGH-LINES.md)
