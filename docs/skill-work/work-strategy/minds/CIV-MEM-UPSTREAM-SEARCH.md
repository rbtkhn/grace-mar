# Searching the upstream civilization_memory checkout

**Scope:** Full local tree at [`research/repos/civilization_memory/`](../../../../research/repos/civilization_memory/README.md) — [LIB-0157](../../../../users/grace-mar/self-library.md#operator-analytical-books). **Not** the Grace-Mar satellite under `docs/civilization-memory/` (that is [LIB-0132](../../../../users/grace-mar/self-library.md) and [`build_civmem_inrepo_index.py`](../../../../scripts/build_civmem_inrepo_index.py)).

**Tri-frame first opens** (which files matter before search): [CIV-MEM-TRI-FRAME-ROUTING.md](CIV-MEM-TRI-FRAME-ROUTING.md).

---

## 1. ripgrep (default)

From repo root, scope to the checkout:

```bash
rg -n "MEM–RELEVANCE" research/repos/civilization_memory/content
rg -n "CIV–STATE" research/repos/civilization_memory/content/civilizations
```

Use paths that match how you already navigate MEM / STATE (see routing doc). `rg --files -g '*.md'` lists markdown paths for orientation.

---

## 2. Optional JSON index (parallel to satellite indexer)

Build a **read-only** term-overlap index over all `.md` files under the checkout (same scoring style as the in-repo satellite indexer):

```bash
python3 scripts/build_civmem_upstream_index.py build
python3 scripts/build_civmem_upstream_index.py query "your question" --limit 5
```

Output path: `research/repos/civilization_memory/.cache/upstream_index.json` (gitignored). If the checkout is missing, `build` exits with an error.

**Compare:** `scripts/build_civmem_inrepo_index.py` indexes only `docs/civilization-memory/` → `docs/civilization-memory/.cache/inrepo_index.json`.

**GitHub Actions:** CI clones upstream at a **pinned SHA** (`docs/ci/civilization_memory_upstream.env`) before `scripts/test_civmem_tri_frame_routing.py` — see `scripts/ci/clone_civilization_memory.sh` and [`docs/ci/README.md`](../../../ci/README.md).

**Phase-4 helpers:** `python3 scripts/suggest_civ_mem_from_relevance.py [ENTITY]` — buckets **Primary MEMs** from `MEM–RELEVANCE–ENTITY` by tri-frame heuristic; `bash scripts/check_civ_mem_upstream_pin.sh` — local `HEAD` vs CI pin. Daily brief §**1b-civ** (when `civ_mem_entity_hint` is set) links these.

---

## Governance

Upstream text is **WORK / reference retrieval** — not SELF until gated. See [`docs/cmc-routing.md`](../../../cmc-routing.md) and [`users/grace-mar/SELF-LIBRARY/CIV-MEM.md`](../../../../users/grace-mar/SELF-LIBRARY/CIV-MEM.md).
