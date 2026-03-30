# WORK-MEMORY — grace-mar

> **Append-only log** of operator sessions started with **`hey`** (WORK rhythm, [operator-cadence](../../../.cursor/skills/operator-cadence/SKILL.md)). **`hey`** is the **only trigger**; log **work-start** vs **closeout** intent, and optional modifiers (**`hey light`**, **`hey minimal`**, **`hey survey`**) in the **Trigger** field below. **Not** part of the Record. **Not** [self-memory](self-memory.md) (companion continuity). **Rotatable** — prune older months if the file grows. Canonical path pattern: `users/[id]/work-memory.md` — [canonical-paths.md](../../../docs/canonical-paths.md).

**Distinct from:**

- **`session-transcript.md`** — raw operator/bot lines and optional `### [WORK-choice]` blocks from [`log_operator_choice.py`](../../../scripts/log_operator_choice.py).
- **`session-log.md`** — structured companion/operator interaction history and pipeline notes.
- **Per-lane logs** — `docs/skill-work/work-*/work-*-history.md` (e.g. [work-dev-history.md](../../docs/skill-work/work-dev/work-dev-history.md)); append **territory-scoped** milestones there. Convention: [work-modules-history-principle.md](../../docs/skill-work/work-modules-history-principle.md).

---

## How to append

After **F** closes a session (or at a natural pause), add a block under [Log](#log):

- Use **`## YYYY-MM-DD`** as the heading; if more than one session that calendar day, add **`### Session 2`** (or time UTC) under the same date.
- **Trigger:** **`hey`** — note **work-start** vs **closeout**; optional modifiers — `hey light` | `hey minimal` | `hey survey`
- **Step 1:** scripts run (e.g. `operator_daily_warmup.py`, `harness_warmup.py`, `operator_handoff_check.py`) — note skipped/light/minimal if applicable
- **Menu path:** letter picks in order until **F** (e.g. `C → E → F`)
- **Artifacts:** repo paths, commits, or generated files (if any)
- **Recursion feed (optional):** gate staging, merges, skill extraction, doc reconciliation — one line each

For **granular** menu picks without a full session summary, you can still use `log_operator_choice.py` into `session-transcript.md` ([work-menu-conventions.md](../../../docs/skill-work/work-menu-conventions.md) § Auditing picks).

---

## Log

_(Append new sessions below this line.)_
