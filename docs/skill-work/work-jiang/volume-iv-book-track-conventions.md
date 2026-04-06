# Volume IV (Game Theory) — book-track conventions

Operator WORK — Predictive History. Canonical prose spec: [`research/external/work-jiang/book/VOLUME-IV-GAME-THEORY.md`](../../../research/external/work-jiang/book/VOLUME-IV-GAME-THEORY.md).

## Naming (locked)

| Item | Convention |
|------|------------|
| YAML block key | `volume_4_game_theory` under [`metadata/book-architecture.yaml`](../../../research/external/work-jiang/metadata/book-architecture.yaml) |
| Chapter IDs | `gt-ch01` … `gt-ch18` — one chapter per `gt-NN` source row (two-digit episode) |
| `source_ids` | Exactly `[gt-NN]` matching [`metadata/sources.yaml`](../../../research/external/work-jiang/metadata/sources.yaml) |
| Evidence packs | `evidence-packs/gt-chNN.md` |
| Outline / draft paths | `chapters-volume-iv/gt-chNN/outline.md` and `draft.md` |
| Part II anchor | `part_2.after_chapter` — last Part I Game Theory chapter in this queue (`gt-ch18` for the Spring 2026 run) |

**Analysis priority:** Volume IV analysis chapters default to **`medium`** in `book-architecture.yaml` until [`chapter-quote-links.yaml`](../../../research/external/work-jiang/metadata/chapter-quote-links.yaml) and [`counter-reading-links.yaml`](../../../research/external/work-jiang/metadata/counter-reading-links.yaml) satisfy `validate_comparative_layer` for that chapter; then promote to **`high`** if desired (same pattern as other volumes).

## Part I / II contract (default)

- **Part I end-of-chapter box:** **Divergence** (mirrors Volumes II–III). See [`CHAPTER-DIVERGENCE-BOX.md`](../../../research/external/work-jiang/CHAPTER-DIVERGENCE-BOX.md).
- **Part II:** Operator-locked in [`book/VOLUME-IV-GAME-THEORY.md`](../../../research/external/work-jiang/book/VOLUME-IV-GAME-THEORY.md).

## Rendered artifacts (Volume IV)

| Output | Script |
|--------|--------|
| [`BOOK-ARCHITECTURE-VOLUME-IV.md`](../../../research/external/work-jiang/BOOK-ARCHITECTURE-VOLUME-IV.md) | [`render_book_architecture.py`](../../../scripts/work_jiang/render_book_architecture.py) |
| [`CHAPTER-QUEUE-VOLUME-IV.md`](../../../research/external/work-jiang/CHAPTER-QUEUE-VOLUME-IV.md) | [`render_chapter_queue.py`](../../../scripts/work_jiang/render_chapter_queue.py) |

## Source map

[`metadata/source-map.yaml`](../../../research/external/work-jiang/metadata/source-map.yaml) `chapter_map` includes every `gt-chNN` → `[gt-NN]` for evidence-pack and validator consistency.

## Regenerating chapter rows

If `gt-*` sources are added or renumbered, regenerate the nested block with:

`python3 scripts/work_jiang/emit_volume4_chapters_yaml.py`

Then merge the emitted YAML into `volume_4_game_theory.book.chapters` (before `volume_7_essays`) and refresh `source-map.yaml` accordingly.

## Tooling (Volume IV parity)

| Script | Role |
|--------|------|
| [`arch_chapters.py`](../../../scripts/work_jiang/arch_chapters.py) | `volume_4_game_theory` in `VOLUME_BLOCK_KEYS` |
| [`emit_volume4_chapters_yaml.py`](../../../scripts/work_jiang/emit_volume4_chapters_yaml.py) | Emit full nested YAML from `gt-*` sources |
| [`build_evidence_pack.py`](../../../scripts/work_jiang/build_evidence_pack.py) | `gt-ch*` open questions / spillover |
| [`validate_argument_layer.py`](../../../scripts/work_jiang/validate_argument_layer.py) | Evidence packs; `` `gt-NN` `` source ids |
| [`validate_work_jiang.py`](../../../scripts/work_jiang/validate_work_jiang.py) | Drift for Volume IV renders |
| [`render_status_dashboard.py`](../../../scripts/work_jiang/render_status_dashboard.py) | Volume IV pack counts |

## After Phase 1 pilot (per-source vertical slice)

Same sequence as Volumes II–III (memo → claims → thesis subclaim → divergence JSONL → `link_supporting_registries.py` → evidence pack → validators), with `gt-01` / `gt-ch01` as reference pilot.

**Thesis subclaim:** `t06` in [`metadata/thesis-map.yaml`](../../../research/external/work-jiang/metadata/thesis-map.yaml).
