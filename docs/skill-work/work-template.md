# Work territory template — new `work-*` lane

**Purpose:** Checklist and README skeleton for adding a **new** WORK territory under `docs/skill-work/work-<name>/`. Reduces drift (missing history, unclear boundaries, wrong gate expectations).

**Not:** A replacement for [companion-self](https://github.com/rbtkhn/companion-self) `users/_template/` (that scaffolds **instances**, not skill-work lanes). **Not** Record truth.

---

## Before you create files

1. **Pick a stable folder name:** `work-<short-id>/` (lowercase, hyphenated). Avoid colliding with existing [skill-work README](README.md) rows.
2. **Decide lane scope:** one primary objective; what is in / out of bounds; whether content ever crosses into **SELF / EVIDENCE / prompt** (then **RECURSION-GATE** + companion approval only).
3. **Read once:** [skills-modularity.md](../skills-modularity.md) (WORK execution vs triad), [AGENTS.md](../../AGENTS.md) (gate), [work-menu-conventions.md](work-menu-conventions.md) if the lane joins operator menus.

---

## Required (minimum viable lane)

| Step | Artifact | Notes |
|------|----------|--------|
| 1 | `docs/skill-work/work-<id>/README.md` | Use [skeleton](#readme-skeleton) below; **Objective**, **Boundary**, **Not**. |
| 2 | `docs/skill-work/work-<id>/work-<id>-history.md` | Append-only log per [work-modules-history-principle.md](work-modules-history-principle.md). |
| 3 | Register the territory | Add a row to [skill-work README.md](README.md) submodule table (or legacy note if merged elsewhere). |
| 4 | Register history file | Add a row to the **Existing logs** table in [work-modules-history-principle.md](work-modules-history-principle.md). |

---

## Recommended (most lanes)

| Step | Artifact | When |
|------|----------|------|
| A | `LANE-CI.md` | PRs use GitHub label **`lane/work-<id>`**; mirror [work-strategy/LANE-CI.md](work-strategy/LANE-CI.md). |
| B | `work-<id>-sources.md` | External channels / feeds / accounts that orient the lane — [work-modules-sources-principle.md](work-modules-sources-principle.md). |
| C | Cross-links in README | Point to adjacent territories (e.g. work-dev, work-politics, work-strategy) and any scripts under `scripts/`. |

---

## Optional

- **Scripts** under `scripts/` or `scripts/work_<id>/` — document invocations in README; keep instance-specific paths explicit.
- **Cursor skill** under `.cursor/skills/` — only when the lane has a stable, repeatable operator trigger; see portable skill ladder in [skills-portable/README.md](../../skills-portable/README.md).
- **Companion-self / manifest** — if the new tree should ship to **every** template consumer, plan a separate merge slice per [MERGING-FROM-COMPANION-SELF.md](../merging-from-companion-self.md); instance-only lanes often stay grace-mar-only.

---

## README skeleton

Copy into `README.md` and replace placeholders.

```markdown
# work-<id>

**Objective:** _One sentence — what this lane is for._

_Not:_ Record truth; not Voice knowledge; not a substitute for `users/<id>/self.md` or RECURSION-GATE queue (unless you document explicit gate use).

---

## Purpose

| Role | Description |
|------|-------------|
| _Primary_ | _…_ |
| _Secondary (optional)_ | _…_ |

---

## Boundary

- **WORK-only** drafts and operator notes live here.
- **Promotion to Record / Voice:** only via **RECURSION-GATE** + companion approval + `process_approved_candidates.py` per AGENTS.
- **Relation to other lanes:** _e.g. reads work-strategy brief; does not merge into work-politics content without human sign-off._

---

## Contents _(optional table)_

| Doc / path | Role |
|------------|------|
| `README.md` | This file |
| `work-<id>-history.md` | Operator trail |
| `work-<id>-sources.md` | Authorized sources _(if present)_ |
| `LANE-CI.md` | PR label convention _(if present)_ |

---

## Related

- [work-template.md](../work-template.md) (this checklist)
- [work-modules-history-principle.md](../work-modules-history-principle.md)
- [work-menu-conventions.md](../work-menu-conventions.md)
```

---

## Governance reminder

- **Stage, do not merge** gate candidates unless the companion approves and the operator runs the merge script.
- **Lexile / knowledge boundary** for anything that could become Voice-facing: follow AGENTS and the gated pipeline; do not leak undocumentable claims into the Record from WORK drafts.

---

**Last updated:** 2026-04-04

**Upstream mirror:** A template-adapted copy (paths tuned for the public repo) lives in [companion-self `docs/skill-work/work-template.md`](https://github.com/rbtkhn/companion-self/blob/main/docs/skill-work/work-template.md) with [work-modules-history-principle.md](https://github.com/rbtkhn/companion-self/blob/main/docs/skill-work/work-modules-history-principle.md) and [work-modules-sources-principle.md](https://github.com/rbtkhn/companion-self/blob/main/docs/skill-work/work-modules-sources-principle.md). Refresh via `template_diff.py` / merge slices when intentionally aligning.
