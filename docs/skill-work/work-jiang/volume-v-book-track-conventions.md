# Volume V (Great Books) — book-track conventions

Operator WORK — Predictive History. Canonical prose spec: [`research/external/work-jiang/book/VOLUME-V-GREAT-BOOKS.md`](../../../research/external/work-jiang/book/VOLUME-V-GREAT-BOOKS.md).

## Naming (locked)

| Item | Convention |
|------|------------|
| YAML block key | `volume_5_great_books` under [`metadata/book-architecture.yaml`](../../../research/external/work-jiang/metadata/book-architecture.yaml) |
| Chapter IDs | `gb-ch01` … `gb-ch08` — one chapter per `gb-NN` source row (two-digit episode) |
| `source_ids` | Exactly `[gb-NN]` matching [`metadata/sources.yaml`](../../../research/external/work-jiang/metadata/sources.yaml) |
| Evidence packs | `evidence-packs/gb-chNN.md` |
| Outline / draft paths | `chapters-volume-v/gb-chNN/outline.md` and `draft.md` |
| Part II anchor | `part_2.after_chapter` — last Part I Great Books chapter in this queue (e.g. `gb-ch08`) |

**Kind / priority (emitter default):** exposition **1–4**, analysis **5–8**; all chapters **`medium`** until quote/counter-reading wiring satisfies `validate_comparative_layer`.

## Part I / II contract (default)

- **Part I end-of-chapter box:** **Divergence** (mirrors Volumes II–IV). See [`CHAPTER-DIVERGENCE-BOX.md`](../../../research/external/work-jiang/CHAPTER-DIVERGENCE-BOX.md).
- **Part II:** Operator-locked in [`book/VOLUME-V-GREAT-BOOKS.md`](../../../research/external/work-jiang/book/VOLUME-V-GREAT-BOOKS.md).

## Rendered artifacts (Volume V)

| Output | Script |
|--------|--------|
| [`BOOK-ARCHITECTURE-VOLUME-V.md`](../../../research/external/work-jiang/BOOK-ARCHITECTURE-VOLUME-V.md) | [`render_book_architecture.py`](../../../scripts/work_jiang/render_book_architecture.py) |
| [`CHAPTER-QUEUE-VOLUME-V.md`](../../../research/external/work-jiang/CHAPTER-QUEUE-VOLUME-V.md) | [`render_chapter_queue.py`](../../../scripts/work_jiang/render_chapter_queue.py) |

## Source map

[`metadata/source-map.yaml`](../../../research/external/work-jiang/metadata/source-map.yaml) `chapter_map` includes every `gb-chNN` → `[gb-NN]` for evidence-pack and validator consistency.

## Regenerating chapter rows

If `gb-*` sources are added or renumbered, regenerate the nested block with:

`python3 scripts/work_jiang/emit_volume5_chapters_yaml.py`

Then merge the emitted YAML into `volume_5_great_books.book.chapters` (before `volume_7_essays`) and refresh `source-map.yaml` accordingly.

## Tooling (Volume V parity)

| Script | Role |
|--------|------|
| [`arch_chapters.py`](../../../scripts/work_jiang/arch_chapters.py) | `volume_5_great_books` in `VOLUME_BLOCK_KEYS` |
| [`emit_volume5_chapters_yaml.py`](../../../scripts/work_jiang/emit_volume5_chapters_yaml.py) | Emit full nested YAML from `gb-*` sources |
| [`build_evidence_pack.py`](../../../scripts/work_jiang/build_evidence_pack.py) | `gb-ch*` open questions / spillover |
| [`validate_argument_layer.py`](../../../scripts/work_jiang/validate_argument_layer.py) | Evidence packs; `` `gb-NN` `` source ids |
| [`validate_work_jiang.py`](../../../scripts/work_jiang/validate_work_jiang.py) | Drift for Volume V renders |
| [`render_status_dashboard.py`](../../../scripts/work_jiang/render_status_dashboard.py) | Volume V pack counts |

## Phase 1 pilot (per-source vertical slice)

Same sequence as Volumes II–IV (memo → claims → thesis subclaim → divergence JSONL → `link_supporting_registries.py` → evidence pack → validators), with **`gb-01` / `gb-ch01`** as reference pilot.

**Thesis subclaim:** `t07` in [`metadata/thesis-map.yaml`](../../../research/external/work-jiang/metadata/thesis-map.yaml).
