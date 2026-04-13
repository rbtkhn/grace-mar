# work-civ-mem workspace

**Use:** Start here when managing `civilization_memory` from Grace-Mar.  
**Scope:** Repository stewardship only: audit, drift detection, contribution prep, workflow clarity.

---

## Start here

1. Read [`README.md`](README.md) for territory scope and boundary.
2. Read [`roadmap.md`](roadmap.md) for the current phase.
3. Check the target repo overview: [`research/repos/civilization_memory/README.md`](../../../research/repos/civilization_memory/README.md).

---

## Consumer contract (Grace-Mar / external tools)

Downstream automation (e.g. `scripts/suggest_civ_mem_from_relevance.py`, CI smoke tests) assumes:

- **`content/civilizations/<ENTITY>/MEM–RELEVANCE–<ENTITY>.md`** when present — primary index for tri-frame suggestions; **stability** of that path matters for pinned-SHA CI.
- Some entities (e.g. **ROME** at certain pins) may ship **CIV–STATE / SCHOLAR / CORE** without a **MEM–RELEVANCE** file — operators use **manual** MEM picks (see [`strategy-notebook/TRUMP-LEO-CIV-MEM-BARNES-DRILL.md`](../work-strategy/strategy-notebook/TRUMP-LEO-CIV-MEM-BARNES-DRILL.md)) until upstream adds the spine.

Optional upstream PR: a short note in `civilization_memory` **README** or **docs/guides/** that external consumers depend on these paths helps prevent accidental renames.

---

## Core repo surfaces

| Surface | Why it matters |
|---------|----------------|
| `research/repos/civilization_memory/README.md` | High-level structure, operating modes, validation commands |
| `research/repos/civilization_memory/docs/` | Governance, architecture, guides, templates, **taxonomy.md**, **essays/** |
| `research/repos/civilization_memory/content/` | Civilizational memory corpus, scholar ledgers, archive |
| `research/repos/civilization_memory/tools/` | CMC console and related application surfaces |
| `research/repos/civilization_memory/scripts/` | Validation, indexing, and maintenance scripts |

---

## Default stewardship loop

1. **Re-orient**  
   Confirm what part of `civilization_memory` you are touching: governance, docs, tools, or content-management workflow.

2. **Check current state**  
   Review repo structure and recent drift indicators before proposing changes.

3. **Run validation when relevant**  
   Use the repo's own checks before claiming a management task is complete.

4. **Capture outcomes clearly**  
   If the work becomes recurring, promote it into `audit-report.md` or extend this workspace doc.

---

## Validation commands

Run from the `civilization_memory` repo root when applicable:

```bash
tools/cmc-governance-checks.sh .
python3 tools/cmc-validate-corpus.py --changed-only
python3 tools/cmc-index-search.py build
python3 tools/cmc-index-search.py query "your terms"
```

For app/dev workflow:

```bash
cd tools/cmc-console
npm install
npm run dev
```

---

## Typical management tasks

| Task | First places to look |
|------|-----------------------|
| **Repo drift / stale docs** | `README.md`, `docs/`, validation scripts |
| **Governance mismatch** | `docs/governance/`, `.cursor/rules/`, repo root README |
| **Tooling confusion** | `tools/`, `scripts/`, Getting Started instructions |
| **Contribution prep** | target file(s), local validation path, commit/PR workflow |

---

## Boundary reminders

- This territory manages the repo; it does not import CMC runtime modes into Grace-Mar.
- Do not confuse Companion Self product strategy with CMC repo stewardship.
- Adjacent strategic priorities may inform sequencing, but this territory remains repository-scoped.

---

## Likely next docs

If this territory becomes active enough to need persistent reporting, add:

- `audit-report.md` — recurring drift / governance / maintenance snapshot
- `operator-workflow.md` or extend this file — step-by-step recurring workflow
