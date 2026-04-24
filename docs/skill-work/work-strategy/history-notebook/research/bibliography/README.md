# Bookshelf — formal bibliography (generated)

**WORK only;** not Record.

Markdown files in this directory are **generated** from [../bookshelf-catalog.yaml](../bookshelf-catalog.yaml). Do not edit them by hand.

| File | Use |
|------|-----|
| [REFERENCES-shelf-by-era.md](REFERENCES-shelf-by-era.md) | All shelf rows grouped by `era` (ancient → modern) |
| [REFERENCES-shelf-by-hnsrc-id.md](REFERENCES-shelf-by-hnsrc-id.md) | Same entries, sorted by `HNSRC-NNNN` |

**Regenerate:** `python3 scripts/build_hn_bookshelf_bibliography.py`  
**Check (CI):** `python3 scripts/build_hn_bookshelf_bibliography.py --check`

**Style:** Simplified Chicago *author–date*; optional imprint fields in YAML (`cite_as`, `place`, `publisher`, `edition`, `series`, `editor`, `translator`). For publication, treat this as a **working** list and strip the trailing `` `HNSRC-…` `` tags if the venue requires a clean *References* section.

Overview: [../BOOKSHELF.md](../BOOKSHELF.md).
