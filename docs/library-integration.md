# Library integration — how LIBRARY connects to the system

**Canonical file:** `users/[id]/self-library.md`  
**Schema:** [library-schema.md](library-schema.md)

**Ontology:** **SELF-LIBRARY** is the **reference-facing** Record surface (governed domains, return-to sources). It is **not** SELF-KNOWLEDGE (identity). **CIV-MEM** is a **sub-library** here: LIB rows + hybrid corpus under `docs/civilization-memory/`, not identity content. See [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md). **Declared domains:** [self-library-domains.md](self-library-domains.md) and [self-library-domains.json](self-library-domains.json).

---

## Already integrated (runtime)

| Surface | Role |
|---------|------|
| **`bot/core.py`** | Loads **active** LIB entries from `self-library.md` (`_load_library`). |
| **Lookup order** | **`SELF-LIBRARY → CIV-MEM (CMC) → full web`** (`_lookup_with_library_first`). After library miss, CMC is **the CIV-MEM domain of SELF-LIBRARY** (reference path), not an identity authority. Analyst prompt sees a **text summary** of every active entry: lane, lookup_priority, title, scope. If the analyst returns a hit, Voice rephrases from that text only — **no full web** for that turn. |
| **Scope + priority** | Entries sort into the summary by **lane** (reference first) then **lookup_priority** (high first). **Scope** tags steer which questions match which sources. |

So: **adding or editing LIB rows with good `scope` and `lookup_priority` directly changes lookup behavior** without prompt merges.

---

## Shelves (thematic, human scan)

Markdown sections in `self-library.md` (**Theology**, **Physics/chemistry/biology**, **History**) are **not** separate runtime tables — they document **which `scope` tags** to use so operators and future UIs stay consistent. Runtime still uses the single **Entries** YAML list.

---

## Recommended connections (light touch)

| Connection | Why |
|------------|-----|
| **EVIDENCE READ-#### ↔ LIB-####** | `read_id` in schema — links *consumed* to *return-to*; audit trail. |
| **Gate when perimeter shifts** | Large additions or Voice-facing policy (“only these shelves for school lookup”) → stage + approve like other Record-adjacent changes. |
| **Warmup / operator** | Weekly skim: high `lookup_priority` + one shelf — keeps LIB from drifting. |
| **Manifest / bundle** | `self-library.md` already in readable set; re-export after big LIB edits so adjunct runtimes see checksum refresh. |

---

## What not to do

- **Don’t** treat LIBRARY as SELF — a book in LIB does not mean the companion has read it or believes it; **EVIDENCE + gate** own that.
- **Don’t** paste the full YAML into SYSTEM prompt — summary path in core already bounds lookup; prompt bloat fights Lexile and boundary.

---

## Operator tooling

```bash
python3 scripts/library_shelf_summary.py -u grace-mar
```

Prints entry counts by shelf keyword (scope tags) and lookup_priority distribution.

- **Reorder by shelf:** `python3 scripts/reorder_library_by_shelf.py -u grace-mar -i` — reorders the Entries YAML block by shelf (Theology, Physics/biology, History, Computer Science, then Reference/Canon/Influence). Use without `-i` to print the new block only.
- **Regenerate shelf tables:** `python3 scripts/library_shelf_tables.py -u grace-mar` — prints markdown tables for Theology, Physics/biology, History, and Computer Science from the YAML; use `-i` to replace the Current entries blocks in-place (optional).

---

## Civ-mem hybrid encyclopedia

Fat corpus + skinny LIB stubs: [civ-mem-encyclopedia-hybrid.md](civ-mem-encyclopedia-hybrid.md) · `python3 scripts/generate_civmem_encyclopedia.py -u grace-mar`

---

## See also

- [lanes/README.md](lanes/README.md) — operator rhythm (LIB skim optional).
- [docs/cmc-routing.md](cmc-routing.md) — CMC after library miss.
