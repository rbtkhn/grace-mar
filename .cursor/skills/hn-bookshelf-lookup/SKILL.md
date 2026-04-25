---
name: hn-bookshelf-lookup
description: History notebook writer ergonomics — resolve HNSRC shelf ids to catalog cards, list print anchors for an hn-* chapter, or generate paste lines and cited-fragments. Triggers: hn hnsrc, shelf lookup, HNSRC-NNNN, shelf anchors, bookshelf chapter.
---

# History notebook — Bookshelf writer lookup

**WORK only;** not Record. **SSOT:** [bookshelf-catalog.yaml](docs/skill-work/work-strategy/history-notebook/research/bookshelf-catalog.yaml) (HNSRC rows) and [book-architecture.yaml](docs/skill-work/work-strategy/history-notebook/book-architecture.yaml) (chapter ids and `file` paths).

## When to use

- Operator or agent is drafting an `hn-*` chapter and needs **which owned-print rows** (HNSRC) are tagged to that chapter via `candidate_hn_chapters`.
- A bare **`HNSRC-NNNN`** appears in chat — resolve **title, author, era, planning chapters, notes** without opening the full YAML.
- Build a **short References fragment** for a finished piece from a list of HNSRC ids.

## Commands (run from repo root)

| Goal | Command |
|------|---------|
| **One shelf “card”** | `python3 scripts/hn_shelf_anchors.py --hnsrc HNSRC-0001` |
| **All HNSRC rows for a chapter** | `python3 scripts/hn_shelf_anchors.py --chapter hn-i-v1-01` |
| **One line to paste** under the chapter id in a draft `.md` | `python3 scripts/hn_shelf_anchors.py --stub-line hn-i-v1-01` |
| **Regenerate inverse index** (all chapters) | `python3 scripts/hn_shelf_anchors.py` |
| **Cited-works bibliography fragment** | `python3 scripts/build_hn_bookshelf_bibliography.py --cited-ids HNSRC-1,HNSRC-2` or `--cited-ids-file path.txt` |

## Artifacts (read)

- [SHELF-ANCHORS-BY-CHAPTER.md](docs/skill-work/work-strategy/history-notebook/research/SHELF-ANCHORS-BY-CHAPTER.md) — `hn-*` → HNSRC list (generated).
- [BOOKSHELF.md](docs/skill-work/work-strategy/history-notebook/research/BOOKSHELF.md) — collection rules.

## Rules

- `candidate_hn_chapters` is **planning** only; [book-architecture.yaml](docs/skill-work/work-strategy/history-notebook/book-architecture.yaml) and chapter prose remain SSOT.
- Do not merge catalog facts into the **Record** without the recursion-gate pipeline.
