# Compiled views (derived)

**Territory:** WORK — refreshable markdown **snapshots** for browsing (Obsidian, handoff). **Not** the source of truth.

**Workflow placement:** **Polyphony** (multiple expert lines, preserved tensions) and **conducting** (your EOD judgment, emphasis, promotion) **primarily happen** in expert **`thread.md` Journal layers**, **`strategy-page`** blocks, **`days.md`**, and **`meta.md`** — during the **EOD strategy session**. **Compiled views** are **optional navigation**: `compile_strategy_view.py` **stitches** sources into one file; it does **not** move authority into the bundle. For a file-by-file map, see [SYNTHESIS-OPERATING-MODEL.md § Where this shows up in your workflow](../SYNTHESIS-OPERATING-MODEL.md#where-this-shows-up-in-your-workflow).

## What lives here

| Kind | Role |
|------|------|
| **`recipes/`** | Human + agent instructions for building a snapshot (inputs, polyphony rules, output shape). |
| **`examples/`** | Hypothetical examples only — **not** Record truth. |
| **Generated `expert-polyphony-synthesis-YYYY-MM-DD.md`** | Dated output from the bundler + optional narrative pass. **Do not edit by hand** — fix sources and regenerate. |

## Source of truth (SSOT)

- [`daily-strategy-inbox.md`](../daily-strategy-inbox.md)
- [`raw-input/`](../raw-input/README.md)
- Expert [`transcript.md`](../strategy-expert-template.md) and **`experts/<expert_id>/thread.md`** (or monthly thread files) — **Journal** (above the machine fence) + **Machine** layer (between `<!-- strategy-expert-thread:start -->` … `end`)
- **`strategy-page`** blocks in thread files
- [`chapters/YYYY-MM/days.md`](../chapters/2026-04/days.md) and **`meta.md`**

## Conductor’s role

The **operator** remains the **conductor**: they decide whether a snapshot is useful, whether sources need correction, and when material promotes upward. **Assistants and scripts are not the conductor** — see [SYNTHESIS-OPERATING-MODEL.md § Operator as conductor](../SYNTHESIS-OPERATING-MODEL.md#8-operator-as-conductor).

## Regeneration

Dated outputs `expert-polyphony-synthesis-YYYY-MM-DD.md` are **machine-generated**; this repo’s `.gitignore` ignores them by default so they are not committed accidentally. Remove the ignore rule if you want to track a snapshot.

**Deterministic bundle** (no LLM):

```bash
python3 scripts/compile_strategy_view.py --notebook-dir docs/skill-work/work-strategy/strategy-notebook
```

Optional: `--date YYYY-MM-DD`, `--out path`, `--experts mercouris,marandi`.

**Narrative “Symphony Snapshot”** sections (Executive Summary, convergences, tensions) follow the recipe in [`recipes/expert-polyphony-synthesis.md`](recipes/expert-polyphony-synthesis.md), using the bundle as input — operator- or assistant-governed.

## See also

- [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Compiled views (derived)](../STRATEGY-NOTEBOOK-ARCHITECTURE.md#compiled-views-derived)
- [SYNTHESIS-OPERATING-MODEL.md § Polyphony synthesis rules](../SYNTHESIS-OPERATING-MODEL.md#7-polyphony-synthesis-rules)
- [SYNTHESIS-OPERATING-MODEL.md § Operator as conductor](../SYNTHESIS-OPERATING-MODEL.md#8-operator-as-conductor)
- Recipe: [`recipes/expert-polyphony-synthesis.md`](recipes/expert-polyphony-synthesis.md)
- Examples: [`examples/expert-polyphony-synthesis-EXAMPLE.md`](examples/expert-polyphony-synthesis-EXAMPLE.md), [`examples/conductor-eod-session-EXAMPLE.md`](examples/conductor-eod-session-EXAMPLE.md)
