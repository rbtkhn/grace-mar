# Civ-mem encyclopedia — hybrid (fat file + skinny LIB rows)

**Pattern:** One **regenerated corpus** on disk (single source of truth) + **many LIB rows** (one per door / section) so lookup **scopes** match questions without pasting megabytes into `self-library.md`.

---

## Artifacts

| Artifact | Role |
|----------|------|
| **`users/grace-mar/artifacts/civ-mem-encyclopedia/ENCYCLOPEDIA.md`** | **Fat file** — concatenation of CMC markdown with clear **anchors** (`## CMC: …`). Regen overwrites. |
| **`users/grace-mar/artifacts/civ-mem-encyclopedia/lib-stubs.yaml`** | **Skinny rows** — generator output; **merge into** `self-library.md` **after** companion/operator gate if Voice perimeter should change. |
| **LIB rows (merged)** | Each row: **title** (short), **scope** (facets), **url** (GitHub canonical path), **notes** (anchor + one-line blurb). **lookup_priority** `medium` or `high` only for rows you want library-first to favor. |

---

## Regen

```bash
export CMC_ROOT=/path/to/civilization_memory   # or default: repos/civilization_memory
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar --essays-only   # small: docs/essays only
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar                 # all docs/
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar --include-content # + content/ (huge)
```

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
- [skill-work/work-political-consulting/civ-mem-draft-protocol.md](skill-work/work-political-consulting/civ-mem-draft-protocol.md)
