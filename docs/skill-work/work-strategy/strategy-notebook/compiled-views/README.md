# Compiled views (derived)
<!-- word_count: 539 -->

**Territory:** WORK — refreshable markdown **snapshots** for browsing (Obsidian, handoff). **Not** the source of truth.

**Workflow placement:** **Polyphony** (multiple expert lines, preserved tensions) and **conducting** (your EOD judgment, emphasis, promotion) **primarily happen** in expert **`thread.md` Journal layers**, **`strategy-page`** blocks, **`days.md`**, and **`meta.md`** — during the **EOD strategy session**. **Compiled views** are **optional navigation**: `compile_strategy_view.py` **stitches** sources into one file; it does **not** move authority into the bundle. For a file-by-file map, see [SYNTHESIS-OPERATING-MODEL.md § Where this shows up in your workflow](../SYNTHESIS-OPERATING-MODEL.md#where-this-shows-up-in-your-workflow).

## When to use compiled views

Use them for **long reads**, **handoff**, and **browsing** — not to replace on-disk **thread** + **`strategy-page`** truth. If you need “what is this watch across experts?”, use [`strategy_watch.py`](../../../../scripts/strategy_watch.py) first; if you need a **single bundled markdown** for a date or a subset of experts, regenerate with `compile_strategy_view.py` (below).

<a id="browse-intent--mechanism"></a>

## Browse intent → mechanism

| Intent | Mechanism (from repo root) | Notes |
|--------|----------------------------|--------|
| **By watch** (pages grouped by `watch=`) | `python3 scripts/strategy_watch.py` / `... --watch <id>` / `... --tensions-only` / `... --json` | Cross-expert positions; [watches — Recovery quick path](../watches/README.md#recovery-quick-path) |
| **By expert** (polyphony bundle) | `python3 scripts/compile_strategy_view.py --notebook-dir docs/skill-work/work-strategy/strategy-notebook` with optional `--experts id1,id2` | Dated `expert-polyphony-synthesis-*.md` under this folder (gitignored by default) |
| **Recent chronology** | Tail of active [`chapters/YYYY-MM/days.md`](../chapters/2026-04/days.md), [STATUS.md](../STATUS.md), [daily-strategy-inbox.md](../daily-strategy-inbox.md) | **SSOT** for “what we committed this month” — not a compiled file |
| **Tensions** | `python3 scripts/strategy_watch.py --tensions-only` (optional `knot-connections.yaml` relations) | Does not replace reading expert threads |

**Stable artifacts:** prefer **a few** dated bundles + [recipes/](recipes/) over ad-hoc copies.

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

**Narrative “Symphony Snapshot”** (operator- or assistant-governed, using the bundle as input) usually follows **[`recipes/expert-polyphony-synthesis-five-conductors.md`](recipes/expert-polyphony-synthesis-five-conductors.md)** (**003** — **preferred** for multi-lens reads + **prioritization** via the five movement map, plus optional **Unhobbling** from `unhobbling-queue.md`). The original **[`recipes/expert-polyphony-synthesis.md`](recipes/expert-polyphony-synthesis.md)** (**001**) remains available for the **Executive Summary** / six-section step structure. `compile_strategy_view.py` embeds the **003** recipe id and points its skeleton at **003** Step 3.

## See also

- [STRATEGY-NOTEBOOK-ARCHITECTURE.md § Compiled views (derived)](../STRATEGY-NOTEBOOK-ARCHITECTURE.md#compiled-views-derived)
- [SYNTHESIS-OPERATING-MODEL.md § Polyphony synthesis rules](../SYNTHESIS-OPERATING-MODEL.md#7-polyphony-synthesis-rules)
- [SYNTHESIS-OPERATING-MODEL.md § Operator as conductor](../SYNTHESIS-OPERATING-MODEL.md#8-operator-as-conductor)
- Recipes: [`recipes/expert-polyphony-synthesis-five-conductors.md`](recipes/expert-polyphony-synthesis-five-conductors.md) (003, preferred) · [`recipes/expert-polyphony-synthesis.md`](recipes/expert-polyphony-synthesis.md) (001, starter)
- Examples: [`examples/expert-polyphony-synthesis-EXAMPLE.md`](examples/expert-polyphony-synthesis-EXAMPLE.md), [`examples/conductor-eod-session-EXAMPLE.md`](examples/conductor-eod-session-EXAMPLE.md)
