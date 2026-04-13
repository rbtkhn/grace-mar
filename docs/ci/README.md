# CI pins

- **`civilization_memory_upstream.env`** — URL + commit SHA for `scripts/ci/clone_civilization_memory.sh` (used by `.github/workflows/test.yml`). Bump the SHA when the tri-frame routing smoke test or upstream layout needs a newer revision.
- **`scripts/test_civmem_tri_frame_routing.py`** — With no arguments, runs **RUSSIA** (full spine + sample MEMs) then **ROME** (partial spine if `MEM–RELEVANCE–ROME.md` is absent; Barnes-oriented MEM paths). Tools that rely on `MEM–RELEVANCE–<X>.md` and `content/civilizations/<X>/` layout should re-run this after pin bumps.
- **Local vs pin** — Optional: `bash scripts/check_civ_mem_upstream_pin.sh` compares `research/repos/civilization_memory` `HEAD` to the env pin (exit `1` on mismatch; exit `0` with a skip message if no checkout). Use after pulling upstream or before a strategy/dream closeout when tri-frame routing depends on the clone.
