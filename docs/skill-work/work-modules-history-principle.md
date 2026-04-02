# Work modules — territory history logs

**Design principle:** Each **work** territory (`work-*`) may carry a single **append-only operator log** — significant sessions, ingest milestones, ship notes, and pointers to commits or artifacts **scoped to that lane**. **New lane scaffold:** [work-template.md](work-template.md).

| Convention | Meaning |
|------------|---------|
| **Filename** | `work-<territory>-history.md` (e.g. `work-dev-history.md`, `work-politics-history.md`) |
| **Location** | `docs/skill-work/<territory>/` alongside that territory’s README and `*-sources.md` (if present) |
| **Content** | Dated sections under **Log**; short bullets; optional SHAs and paths |
| **Not** | Record truth, Voice knowledge, or automatic pipeline output. **Not** a substitute for `users/[id]/session-log.md` or RECURSION-GATE. |

**Fence:** History files document **what the operator did or noted in this lane** — not what is canonically true. Facts about the companion belong in the gated Record; integration status belongs in tables such as [work-dev/integration-status.md](work-dev/integration-status.md).

**Relation to operator rhythm:** Sessions opened with **`coffee`** follow [coffee](../../.cursor/skills/coffee/SKILL.md); legacy **`hey`** still works as an alias. There is **no** dedicated instance-wide **`work-memory.md`** file: append **per-territory** milestones under **`docs/skill-work/work-*/*-history.md`**. Raw continuity and **`[WORK-choice]`** blocks may still go to **`users/[id]/session-transcript.md`** (see `log_operator_choice.py`). **`*-history.md`** is **per-lane** breadcrumbs (e.g. “ingested Karpathy digest,” “weekly brief run,” “Jiang CI change”) so ML or humans can scan **where** work landed without merging lanes.

**Existing logs:**

| Territory | File |
|-----------|------|
| work-dev | [work-dev/work-dev-history.md](work-dev/work-dev-history.md) |
| work-coffee | [work-coffee/work-coffee-history.md](work-coffee/work-coffee-history.md) |
| work-politics | [work-politics/work-politics-history.md](work-politics/work-politics-history.md) |
| work-jiang | [work-jiang/work-jiang-history.md](work-jiang/work-jiang-history.md) |
| work-strategy | [work-strategy/work-strategy-history.md](work-strategy/work-strategy-history.md) |
| work-business | [work-business/work-business-history.md](work-business/work-business-history.md) |
| work-career | [work-career/work-career-history.md](work-career/work-career-history.md) |
| work-companion-self | [work-companion-self/work-companion-self-history.md](work-companion-self/work-companion-self-history.md) |
| work-curate-library | [work-curate-library/work-curate-library-history.md](work-curate-library/work-curate-library-history.md) |
| work-health-fitness | [work-health-fitness/work-health-fitness-history.md](work-health-fitness/work-health-fitness-history.md) |
| work-human-teacher | [work-human-teacher/work-human-teacher-history.md](work-human-teacher/work-human-teacher-history.md) |
| work-xavier | [work-xavier/work-xavier-history.md](work-xavier/work-xavier-history.md) |
| work-civ-mem | [work-civ-mem/work-civ-mem-history.md](work-civ-mem/work-civ-mem-history.md) |
| work-alpha-school | [work-alpha-school/work-alpha-school-history.md](work-alpha-school/work-alpha-school-history.md) |
| work-cadence | [work-cadence/work-cadence-events.md](work-cadence/work-cadence-events.md) *(per-run telemetry, not design history)* |

**Cadence run telemetry:** Per-run audit of `coffee`, `dream`, and `bridge` invocations lives in [work-cadence/work-cadence-events.md](work-cadence/work-cadence-events.md), appended by `scripts/log_cadence_event.py`. This is distinct from per-ritual *design* history (`work-coffee-history.md`, `work-dream-history.md`) which tracks architecture changes, not every run. Cadence events are not Record truth, not self-memory, and not a replacement for `session-transcript.md`.

**Legacy / merged territories** (no dedicated history file; use **work-dev** or parent): `work-build-ai` → work-dev; `work-grace-gems` → work-business/grace-gems (log in **work-business-history** or gem-specific notes).

**Cross-reference:** Authorized sources lists — [work-modules-sources-principle.md](work-modules-sources-principle.md).

**Optional downstream rollup:** Per-instance **`users/[id]/self-history.md`** may **densely aggregate** these territory logs into one timeline alongside a **gate-approved companion** thread — **derived**, not Record; see [canonical-paths.md](../canonical-paths.md) and **AGENTS.md** § 11a. Regenerate log bodies with **`python3 scripts/draft_self_history.py -u <id>`** (default: print to stdout; **`--write`** replaces log sections; **`--companion-style per-act --max N`** for line-by-line ACT index).
