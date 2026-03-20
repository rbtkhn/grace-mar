# Civ-mem → speech / policy — human-always-approves

**Territory:** work-politics (WAP)  
**Corpus:** `civilization_memory` (CMC), indexed via `tools/cmc-index-search.py`. **Essay canon (repo-owned):** edit `docs/civilization-memory/essays/` in this repo; regen encyclopedia from there. Submodule remains optional for tools/full index.
**Invariant:** Retrieval and drafting may be automated; **no external release** without explicit human approval on **that exact artifact**.

---

## Gates (sequential)

| Gate | Artifact | Machine | Human |
|------|----------|---------|--------|
| **G0** | Use case | — | Approve **brief** (audience, red lines, what CMC may inform) |
| **G1** | Scaffold | Outline + cited MEM paths | Approve or edit scaffold |
| **G2** | Full draft | Prose / talking points | Approve draft |
| **G3** | Release | Final string for speech, memo, X | **Final approve** (name + date + channel) |

Nothing at G3 may ship without a recorded **approver + scope** (e.g. internal only vs public).

---

## Provenance (required on every block)

Tag each paragraph or bullet so reviewers know what is:

- `{CMC: path}` — e.g. `content/civilizations/AMERICA/MEM–AMERICA–LAW–CONGRESS.md`
- `{principal}` — from principal-profile / operator
- `{analyst}` — model synthesis (must not be cited as fact without source)

---

## Safe automatic (no approval)

- `cmc-index-search.py build` / `query` / `facets`
- Unpublished scratch under `docs/skill-work/work-politics/` marked **DRAFT — NOT APPROVED**

---

## Test runs

Store under `civ-mem-test-run-YYYY-MM-DD.md` (or similar). Each test run repeats G0→G2 in miniature; G3 left **PENDING** unless companion signs.

See [civ-mem-test-run-2026-03-14.md](civ-mem-test-run-2026-03-14.md) for a worked example.

---

## Sync with WAP README

Aligns with: *Human approves all public-facing content and strategy.* Civ-mem adds: **corpus-informed drafts still require the same approvals** — CMC is input, not authorization.
