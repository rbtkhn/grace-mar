# `prepared-context/` (repository root)

This directory is a **placeholder** for the [state model](../docs/state-model.md) **prepared context layer** at the grace-mar **repo root**. Prepared context in practice appears as drafts, tool bundles, MEMORY, and normalized extracts under **`users/`**, **`docs/skill-work/`**, and related WORK surfaces — not necessarily as files dropped here.

**Why it exists:** Same as root [`evidence/`](../evidence/): tracked minimal footprint, no false promise of automated pipelines into this folder yet.

See [State model — Repo layout (grace-mar)](../docs/state-model.md#repo-layout-grace-mar).

## Progressive disclosure (runtime + WORK)

For **index-first** prepared context (runtime observation summaries before full notebook reads), see [progressive-disclosure.md](../docs/prepared-context/progressive-disclosure.md), `scripts/prepared_context/build_context_index.py`, and **`scripts/prepared_context/build_context_from_observations.py`** (expanded IDs → bounded Markdown). Example/template: [runtime-observation-context.md](runtime-observation-context.md). See [observation-expansion.md](../docs/runtime/observation-expansion.md).

**Operator-generated brief:** `python3 scripts/runtime/memory_brief.py ... --output prepared-context/memory-brief.md` may write a **runtime-only** Markdown brief here (not Record truth). The repo root `.gitignore` ignores `prepared-context/memory-brief.md` by default.
