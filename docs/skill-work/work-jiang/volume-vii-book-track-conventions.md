# Volume VII (Essays) — book-track conventions

Operator WORK — Predictive History. Canonical prose spec: [`research/external/work-jiang/book/VOLUME-VII-ESSAYS.md`](../../../research/external/work-jiang/book/VOLUME-VII-ESSAYS.md).

## Naming (locked)

| Item | Convention |
|------|------------|
| YAML block key | `volume_7_essays` under [`metadata/book-architecture.yaml`](../../../research/external/work-jiang/metadata/book-architecture.yaml) |
| Source IDs | `es-01` … `es-NN` — publication order (see essay front matter `publication_date`, then `substack_slug`); emitted by [`build_source_registry.py`](../../../scripts/work_jiang/build_source_registry.py) from `substack/essays/*.md` |
| Chapter IDs | `es-ch01` … `es-chNN` — one chapter per `es-NN` row (two-digit episode; order follows registry) |
| `source_ids` | Exactly `[es-NN]` matching [`metadata/sources.yaml`](../../../research/external/work-jiang/metadata/sources.yaml) |
| Evidence packs | `evidence-packs/es-chNN.md` |
| Outline / draft paths | `chapters-volume-vii/es-chNN/outline.md` and `draft.md` |
| Part II anchor | `part_2.after_chapter` — last Part I essay chapter in this queue (e.g. `es-ch31`) |

**Kind / priority (emitter default):** all chapters **`analysis`** + **`medium`** until quote/counter-reading wiring satisfies `validate_comparative_layer`.

## Part I / II contract (default)

- **Part I end-of-chapter box:** **Divergence** (mirrors Volumes II–VI). See [`CHAPTER-DIVERGENCE-BOX.md`](../../../research/external/work-jiang/CHAPTER-DIVERGENCE-BOX.md).
- **Part II:** Operator-locked in [`book/VOLUME-VII-ESSAYS.md`](../../../research/external/work-jiang/book/VOLUME-VII-ESSAYS.md).

## Rendered artifacts (Volume VII)

| Output | Script |
|--------|--------|
| [`BOOK-ARCHITECTURE-VOLUME-VII.md`](../../../research/external/work-jiang/BOOK-ARCHITECTURE-VOLUME-VII.md) | [`render_book_architecture.py`](../../../scripts/work_jiang/render_book_architecture.py) |
| [`CHAPTER-QUEUE-VOLUME-VII.md`](../../../research/external/work-jiang/CHAPTER-QUEUE-VOLUME-VII.md) | [`render_chapter_queue.py`](../../../scripts/work_jiang/render_chapter_queue.py) |

## Source map

[`metadata/source-map.yaml`](../../../research/external/work-jiang/metadata/source-map.yaml) `chapter_map` includes every `es-chNN` → `[es-NN]` for evidence-pack and validator consistency.

## Regenerating chapter rows

If `es-*` sources are added or renumbered, refresh registry then regenerate the nested block:

1. `python3 scripts/work_jiang/build_source_registry.py`
2. `python3 scripts/work_jiang/emit_volume7_chapters_yaml.py` → merge into `volume_7_essays` in `book-architecture.yaml`
3. Update `source-map.yaml` `chapter_map` for new `es-chNN` keys

## Tooling (Volume VII parity)

| Script | Role |
|--------|------|
| [`arch_chapters.py`](../../../scripts/work_jiang/arch_chapters.py) | `volume_7_essays` in `VOLUME_BLOCK_KEYS` |
| [`build_source_registry.py`](../../../scripts/work_jiang/build_source_registry.py) | Append `es-*` from `substack/essays` + `essay-*-analysis.md` |
| [`emit_volume7_chapters_yaml.py`](../../../scripts/work_jiang/emit_volume7_chapters_yaml.py) | Emit full nested YAML from `es-*` sources |
| [`build_evidence_pack.py`](../../../scripts/work_jiang/build_evidence_pack.py) | `es-ch*` open questions / spillover |
| [`validate_argument_layer.py`](../../../scripts/work_jiang/validate_argument_layer.py) | Evidence packs; `` `es-NN` `` source ids |
| [`validate_work_jiang.py`](../../../scripts/work_jiang/validate_work_jiang.py) | Drift for Volume VII renders; essay paths in `sources.yaml` |
| [`render_status_dashboard.py`](../../../scripts/work_jiang/render_status_dashboard.py) | Volume VII pack counts |

## Phase 1 pilot (per-source vertical slice)

Same sequence as prior volumes (memo → claims → thesis subclaim → divergence JSONL → `link_supporting_registries.py` → evidence pack → validators), with **`es-01` / `es-ch01`** as reference pilot.
