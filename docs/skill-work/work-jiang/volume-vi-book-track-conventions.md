# Volume VI (Interviews) — book-track conventions

Operator WORK — Predictive History. Canonical prose spec: [`research/external/work-jiang/book/VOLUME-VI-INTERVIEWS.md`](../../../research/external/work-jiang/book/VOLUME-VI-INTERVIEWS.md).

## Naming (locked)

| Item | Convention |
|------|------------|
| YAML block key | `volume_6_interviews` under [`metadata/book-architecture.yaml`](../../../research/external/work-jiang/metadata/book-architecture.yaml) |
| Chapter IDs | `vi-ch01` … `vi-ch12` — one chapter per `vi-NN` source row (two-digit episode; order follows registry) |
| `source_ids` | Exactly `[vi-NN]` matching [`metadata/sources.yaml`](../../../research/external/work-jiang/metadata/sources.yaml) |
| Evidence packs | `evidence-packs/vi-chNN.md` |
| Outline / draft paths | `chapters-volume-vi/vi-chNN/outline.md` and `draft.md` |
| Part II anchor | `part_2.after_chapter` — last Part I interview chapter in this queue (e.g. `vi-ch12`) |

**Kind / priority (emitter default):** exposition **1–4**, analysis **5–11**; all chapters **`medium`** until quote/counter-reading wiring satisfies `validate_comparative_layer`.

## Part I / II contract (default)

- **Part I end-of-chapter box:** **Divergence** (mirrors Volumes II–V). See [`CHAPTER-DIVERGENCE-BOX.md`](../../../research/external/work-jiang/CHAPTER-DIVERGENCE-BOX.md).
- **Part II:** Operator-locked in [`book/VOLUME-VI-INTERVIEWS.md`](../../../research/external/work-jiang/book/VOLUME-VI-INTERVIEWS.md).

## Rendered artifacts (Volume VI)

| Output | Script |
|--------|--------|
| [`BOOK-ARCHITECTURE-VOLUME-VI.md`](../../../research/external/work-jiang/BOOK-ARCHITECTURE-VOLUME-VI.md) | [`render_book_architecture.py`](../../../scripts/work_jiang/render_book_architecture.py) |
| [`CHAPTER-QUEUE-VOLUME-VI.md`](../../../research/external/work-jiang/CHAPTER-QUEUE-VOLUME-VI.md) | [`render_chapter_queue.py`](../../../scripts/work_jiang/render_chapter_queue.py) |

## Source map

[`metadata/source-map.yaml`](../../../research/external/work-jiang/metadata/source-map.yaml) `chapter_map` includes every `vi-chNN` → `[vi-NN]` for evidence-pack and validator consistency.

## Regenerating chapter rows

If `vi-*` sources are added or renumbered, regenerate the nested block with:

`python3 scripts/work_jiang/emit_volume6_chapters_yaml.py`

Then merge the emitted YAML into `volume_6_interviews.book.chapters` (before `volume_7_essays`) and refresh `source-map.yaml` accordingly.

## Tooling (Volume VI parity)

| Script | Role |
|--------|------|
| [`arch_chapters.py`](../../../scripts/work_jiang/arch_chapters.py) | `volume_6_interviews` in `VOLUME_BLOCK_KEYS` |
| [`emit_volume6_chapters_yaml.py`](../../../scripts/work_jiang/emit_volume6_chapters_yaml.py) | Emit full nested YAML from `vi-*` sources |
| [`build_evidence_pack.py`](../../../scripts/work_jiang/build_evidence_pack.py) | `vi-ch*` open questions / spillover |
| [`validate_argument_layer.py`](../../../scripts/work_jiang/validate_argument_layer.py) | Evidence packs; `` `vi-NN` `` source ids |
| [`validate_work_jiang.py`](../../../scripts/work_jiang/validate_work_jiang.py) | Drift for Volume VI renders |
| [`render_status_dashboard.py`](../../../scripts/work_jiang/render_status_dashboard.py) | Volume VI pack counts |

## Phase 1 pilot (per-source vertical slice)

Same sequence as prior volumes (memo → claims → thesis subclaim → divergence JSONL → `link_supporting_registries.py` → evidence pack → validators), with **`vi-01` / `vi-ch01`** as reference pilot.

**Thesis subclaim:** `t08` in [`metadata/thesis-map.yaml`](../../../research/external/work-jiang/metadata/thesis-map.yaml).
