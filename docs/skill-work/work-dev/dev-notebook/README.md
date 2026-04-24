# Work notebook (`dev-notebook/`) — multi-lane spec vault

**Path (historical name):** `docs/skill-work/work-dev/dev-notebook/`. The directory is named **`dev-notebook`** for stable links; the **role** is a **cross-lane notebook**: durable **prompts**, **instruction captures**, and **spec snapshots** grouped by the WORK territory they serve, plus the **work-dev day journal** in one tree.

**Contract — read before adding files**

This folder is **not** a second **strategy-notebook** or **cici-notebook**. **Day-scale, fold-at-dream surfaces** (days.md, `daily-*-inbox`, chapter threads) stay in their home territories. Here we only keep **reusable text** (paste-ready prompts, migration specs, “how we implemented X” references) and the **inward work-dev journal** (LIB-0155). **No secrets** in prose — env var names and paths only. **WORK only**; not Record, not Voice knowledge.

| Lane subfolder | Holds | Does **not** replace |
|----------------|-------|----------------------|
| **[work-dev/](work-dev/README.md)** | Lane shell: [SURFACE-MAP](work-dev/SURFACE-MAP.md) (canonical in-repo paths) + [HISTORY-ANCHORS](work-dev/HISTORY-ANCHORS.md); pointers to the territory. | [work-dev README](../README.md) (objective, Contents) — or [workspace.md](../workspace.md) as the live next-actions surface. |
| **[work-dev/journal/](work-dev/journal/README.md)** | `YYYY-MM-DD-day-NN.md` day log, [daily dev journal inbox](work-dev/journal/daily-dev-journal-inbox.md), routing vs cici-notebook. | [work-dev-history.md](../work-dev-history.md) (milestones), [workspace.md](../workspace.md) (entrypoint). |
| **[work-cici/](work-cici/README.md)** | Cici/OB1 **prompts** (e.g. Phase 1) + **Cici `main` map** and **milestone table**; pointers into [work-cici/](../../work-cici/). | [cici-notebook/](../../work-cici/cici-notebook/README.md) (daily coaching / digests). |
| **[work-strategy/](work-strategy/README.md)** | Optional **paste-ready** strategy prompts; [SURFACE-MAP](work-strategy/SURFACE-MAP.md) + [HISTORY-ANCHORS](work-strategy/HISTORY-ANCHORS.md) into the territory. | [strategy-notebook/](../../work-strategy/strategy-notebook/) (inbox, days, raw-input, weave). |

**Layout (tree)**

```text
dev-notebook/
  README.md                 ← this file (contract)
  work-dev/
    README.md
    SURFACE-MAP.md
    HISTORY-ANCHORS.md
    identity-fork-protocol-ifp-2026-04-24.md   ← IFP spec (WORK)
    journal/                 ← dev journal (LIB-0155) + inbox + day-*.md
  work-cici/
    README.md
    UPSTREAM-MAP.md
    HISTORY-ANCHORS.md
    cici-phase-1-git-first-governed-state-prompt.md
  work-strategy/
    README.md
    SURFACE-MAP.md
    HISTORY-ANCHORS.md
    ← add *.md prompts here when they belong in strategy but not the rolling notebook
```

**Compatibility:** Older links to `dev-journal/` → [dev-journal/README.md](../dev-journal/README.md). **`SELF-LIBRARY/dev-journal`** symlink → `work-dev/journal/`.

## Index by lane

| Location | Summary |
|----------|---------|
| [work-dev/README.md](work-dev/README.md) | work-dev lane shell: map + history anchors, pointers to [work-dev/](../) territory. |
| [work-dev/SURFACE-MAP.md](work-dev/SURFACE-MAP.md) | work-dev **surface map** (workspace, control-plane, journal symlink, key scripts) — in-repo, not a Git `main` tree. |
| [work-dev/HISTORY-ANCHORS.md](work-dev/HISTORY-ANCHORS.md) | work-dev milestones from [work-dev-history.md](../work-dev-history.md). |
| [work-dev/identity-fork-protocol-ifp-2026-04-24.md](work-dev/identity-fork-protocol-ifp-2026-04-24.md) | **Identity Fork Protocol (IFP)** — structured spec + comparisons (WORK only; not Record). |
| [work-dev/journal/README.md](work-dev/journal/README.md) | Inward work-dev **day** learning log. |
| [work-cici/README.md](work-cici/README.md) | work-cici subfolder: contract, handoff pointers, links into [work-cici/](../../work-cici/INDEX.md). |
| [work-cici/UPSTREAM-MAP.md](work-cici/UPSTREAM-MAP.md) | Cici GitHub `main` path table (prompts, governed-state, `.claude/`, scripts) + regen recipe. |
| [work-cici/HISTORY-ANCHORS.md](work-cici/HISTORY-ANCHORS.md) | Milestone table keyed to [work-cici-history.md](../../work-cici/work-cici-history.md) with Cici and evidence links. |
| [work-cici/cici-phase-1-git-first-governed-state-prompt.md](work-cici/cici-phase-1-git-first-governed-state-prompt.md) | Cici Phase 1 — Git-first governed state (archived instruction prompt). |
| [work-strategy/README.md](work-strategy/README.md) | work-strategy lane: contract, hooks; map + **history** pointers into [work-strategy README](../../work-strategy/README.md) territory. |
| [work-strategy/SURFACE-MAP.md](work-strategy/SURFACE-MAP.md) | work-strategy **surface map** (notebook, rome, research, LANE-CI, minds). |
| [work-strategy/HISTORY-ANCHORS.md](work-strategy/HISTORY-ANCHORS.md) | work-strategy milestones from [work-strategy-history.md](../../work-strategy/work-strategy-history.md). |
