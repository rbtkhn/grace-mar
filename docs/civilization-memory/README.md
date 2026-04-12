# Civilization memory — Grace-Mar satellite (`docs/civilization-memory/`)

## Terminology (binding in this workspace)

**When you say “civ-mem” while working in Grace-Mar, that means the complete [`civilization_memory`](../../research/repos/civilization_memory) repository** — MEM files, CIV–CORE, CIV–STATE, CIV–SCHOLAR, ARC, templates, governance, tools: the **full** upstream corpus at `research/repos/civilization_memory/`.

**This folder** (`docs/civilization-memory/`) is **not** a second copy of that repo. It holds **Grace-Mar–owned** material versioned with this instance:

- **Essays and long-form** you edit here (theses, book drafts, panels).
- **Notes** (concepts, polyphony, face/category/blade, research briefs).
- **`minds/`** — **No mind files here.** Canonical **CIV-MIND** profiles for Grace-Mar live only under [`docs/skill-work/work-strategy/strategy-notebook/minds/`](../skill-work/work-strategy/strategy-notebook/minds/) (self-contained; **do not require** civ-mem). See [minds/README.md](minds/README.md).

Do not treat `docs/civilization-memory/` as the civ-mem corpus itself; treat it as **satellite prose** (essays, book, notes). **civ-mem** = full `research/repos/civilization_memory` when present; **minds** do not depend on it.

---

## Purpose

Civilization memory has **no monetary purpose**. Its purpose is **pure understanding of history** — patterns, causes, and lessons of civilizations, institutions, and coordination over time — as a resource for reflection and judgment, not for revenue. Content here deepens how we read the past so present decisions can be wiser.

---

| Path | Role |
|------|------|
| **`essays/`** | Operator essays (Simple Condition, Coordination Hypothesis, index). Edit in place. |
| **`notes/`** | Short conceptual notes (face/category/blade, polyphony, scripture-as-test, etc.). |
| **`minds/`** | **Redirect only** — canonical minds are under **work-strategy → strategy-notebook → minds**. See [minds/README.md](minds/README.md). |
| **`book/`** | Manuscript and applied-theology harvest artifacts tied to the book project. |
| **`content/`** | Optional — chunked or expanded material later (large regen may mirror here). |

---

## Tooling (this tree only)

**Encyclopedia regen (essays):**

```bash
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar --essays-only
```

**In-repo search index** (when full civ-mem checkout is unavailable; indexes **this** folder):

```bash
python3 scripts/build_civmem_inrepo_index.py build
```

Index: `docs/civilization-memory/.cache/inrepo_index.json`. Default `--cmc` is `docs/civilization-memory/`; override only if you fork layout.

---

## Provenance

Initial `essays/*.md` copied from civilization_memory (2026-03); subsequent edits are Grace-Mar commits unless synced upstream manually.
