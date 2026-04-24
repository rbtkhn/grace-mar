# Work notebook (`dev-notebook/`) — multi-lane spec vault

**Path (historical name):** `docs/skill-work/work-dev/dev-notebook/`. The directory is named **`dev-notebook`** for stable links; the **role** is a **cross-lane notebook**: durable **prompts**, **instruction captures**, and **spec snapshots** grouped by the WORK territory they serve, plus the **work-dev day journal** in one tree.

**Contract — read before adding files**

This folder is **not** a second **strategy-notebook** or **cici-notebook**. **Day-scale, fold-at-dream surfaces** (days.md, `daily-*-inbox`, chapter threads) stay in their home territories. Here we only keep **reusable text** (paste-ready prompts, migration specs, “how we implemented X” references) and the **inward work-dev journal** (LIB-0155). **No secrets** in prose — env var names and paths only. **WORK only**; not Record, not Voice knowledge.

| Lane subfolder | Holds | Does **not** replace |
|----------------|-------|----------------------|
| **[work-dev/journal/](work-dev/journal/README.md)** | `YYYY-MM-DD-day-NN.md` day log, [daily dev journal inbox](work-dev/journal/daily-dev-journal-inbox.md), routing vs cici-notebook. | [work-dev-history.md](../work-dev-history.md) (milestones), [workspace.md](../workspace.md) (entrypoint). |
| **[work-cici/](work-cici/README.md)** | Cici/OB1 **prompts and spec PDFs** archived as markdown (e.g. Phase 1 governed-state). | [cici-notebook/](../../work-cici/cici-notebook/README.md) (daily coaching / digests). |
| **[work-strategy/](work-strategy/README.md)** | Optional **paste-ready** strategy prompts, rubrics, or spec fragments. | [strategy-notebook/](../../work-strategy/strategy-notebook/) (inbox, days, raw-input, weave). |

**Layout (tree)**

```text
dev-notebook/
  README.md                 ← this file (contract)
  work-dev/
    journal/                 ← dev journal (LIB-0155) + inbox + day-*.md
  work-cici/
    README.md
    cici-phase-1-git-first-governed-state-prompt.md
  work-strategy/
    README.md                ← add *.md here when a prompt belongs to strategy-work but not the rolling notebook
```

**Compatibility:** Older links to `dev-journal/` → [dev-journal/README.md](../dev-journal/README.md). **`SELF-LIBRARY/dev-journal`** symlink → `work-dev/journal/`.

## Index by lane

| Location | Summary |
|----------|---------|
| [work-dev/journal/README.md](work-dev/journal/README.md) | Inward work-dev learning log. |
| [work-cici/cici-phase-1-git-first-governed-state-prompt.md](work-cici/cici-phase-1-git-first-governed-state-prompt.md) | Cici Phase 1 — Git-first governed state (archived instruction prompt). |
| [work-cici/README.md](work-cici/README.md) | work-cici lane note. |
| [work-strategy/README.md](work-strategy/README.md) | work-strategy lane note (empty shell until you add files). |
