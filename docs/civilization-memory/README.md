# Civilization memory — grace-mar–owned copy

**Canonical for this repo:** Essay and long-form **content you edit here** lives under **`docs/civilization-memory/`** (versioned with grace-mar).

| Path | Role |
|------|------|
| **`essays/`** | Operator essays (Simple Condition, Coordination Hypothesis, index). Edit in place. |
| **`content/`** | Optional — add chunked or expanded material later (gitignored large regen can mirror here if you want). |

**Upstream:** `repos/civilization_memory/` may remain a **sibling project** or submodule for tools, apps, and history. **LIBRARY + encyclopedia regen default to this folder**, not the submodule.

**Regen fat file (essays):**

```bash
python3 scripts/generate_civmem_encyclopedia.py -u grace-mar --essays-only
```

Default `--cmc` is `docs/civilization-memory/`. Override with `--cmc /other/path` only if you fork layout.

**Provenance:** Initial `essays/*.md` copied from civilization_memory (2026-03); future edits are grace-mar commits unless you sync back upstream manually.
