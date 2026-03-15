# Civilization memory — grace-mar–owned copy

**Canonical for this repo:** Essay and long-form **content you edit here** lives under **`docs/civilization-memory/`** (versioned with grace-mar).

**Purpose:** Civilization memory has **no monetary purpose**. Its purpose is **pure understanding of history** — the patterns, causes, and lessons of civilizations, institutions, and human coordination over time. That understanding can **help leaders’ wisdom**: it is a resource for reflection, analogy, and judgment, not for revenue or product. The essays and notes here exist to deepen how we see the past so that those who lead, teach, or advise can see the present more clearly.

---

| Path | Role |
|------|------|
| **`essays/`** | Operator essays (Simple Condition, Coordination Hypothesis, index). Edit in place. |
| **`notes/`** | Short conceptual notes: face/category/blade; exercise for school children (see the face); lens: *God's Debris* (Scott Adams) applied to the Condition. |
| **`minds/`** | Three mind profiles ported from upstream (Mercouris, Mearsheimer, Barnes): polyphonic cognition implementation; reference for STATE-evolved assistant brain. See [minds/README.md](minds/README.md). |
| **`content/`** | Optional — add chunked or expanded material later (gitignored large regen can mirror here if you want). |

**Upstream:** `repos/civilization_memory/` may remain a **sibling project** or submodule for tools, apps, and history. **LIBRARY + encyclopedia regen default to this folder**, not the submodule.

**Regen fat file (essays):**

```bash
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar --essays-only
```

Default `--cmc` is `docs/civilization-memory/`. Override with `--cmc /other/path` only if you fork layout.

**Provenance:** Initial `essays/*.md` copied from civilization_memory (2026-03); future edits are grace-mar commits unless you sync back upstream manually.
