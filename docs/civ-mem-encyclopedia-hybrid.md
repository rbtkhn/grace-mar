# Civ-mem encyclopedia — hybrid (fat file + skinny LIB rows)

**Pattern:** One **regenerated corpus** on disk (single source of truth) + **many LIB rows** (one per door / section) so lookup **scopes** match questions without pasting megabytes into `self-library.md`.

---

## Artifacts

| Artifact | Role |
|----------|------|
| **`users/grace-mar/artifacts/civ-mem-encyclopedia/ENCYCLOPEDIA.md`** | **Fat file** — concatenation of **grace-mar–owned** `docs/civilization-memory/` markdown with anchors (`## CM:essays/…`). Regen overwrites. |
| **`users/grace-mar/artifacts/civ-mem-encyclopedia/lib-stubs.yaml`** | **Skinny rows** — generator output; **merge into** `self-library.md` **after** companion/operator gate if Voice perimeter should change. |
| **LIB rows (merged)** | Each row: **title** (short), **scope** (facets), **url** (GitHub canonical path), **notes** (anchor + one-line blurb). **lookup_priority** `medium` or `high` only for rows you want library-first to favor. |

---

## Regen

```bash
# Default content root: docs/civilization-memory/ (owned copy). Override: --cmc /other/path
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar --essays-only     # → ENCYCLOPEDIA.md
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar                   # → ENCYCLOPEDIA.docs.md (gitignored)
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar --include-content # + content/ (gitignored)
```

**Owned copy policy:** [docs/civilization-memory/README.md](civilization-memory/README.md)

Writes `ENCYCLOPEDIA.md` + `lib-stubs.yaml`. Does **not** edit `self-library.md` automatically.

---

## Lookup reality (today)

`bot/core.py` builds lookup summary from **title + scope** (and lane/priority). It does **not** load full markdown per row. So:

- **Skinny rows** improve **routing** (which door matches the question).
- **Answers** still depend on analyst + summary; for **faithful** quotes, use **CMC path** after hit or extend core later (e.g. include truncated **notes** in summary).

**Operator use:** Fat file is ideal for **search, RAG, and human read**; Voice is **incrementally** improved as stubs accrue and optional core tweaks land.

---

## Gate

Bulk LIB adds = **RECURSION-GATE** when Voice should honor new return-to sources. Doc-only regen of `ENCYCLOPEDIA.md` without merging stubs = no gate.

---

## See also

- [library-integration.md](library-integration.md)
- [skill-work/work-politics/civ-mem-draft-protocol.md](skill-work/work-politics/civ-mem-draft-protocol.md)
