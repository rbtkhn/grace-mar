# Work modules — territory history logs

**Design principle:** Each **work** territory (`work-*`) may carry a single **append-only operator log** — significant sessions, ingest milestones, ship notes, and pointers to commits or artifacts **scoped to that lane**.

| Convention | Meaning |
|------------|---------|
| **Filename** | `work-<territory>-history.md` (e.g. `work-dev-history.md`, `work-politics-history.md`) |
| **Location** | `docs/skill-work/<territory>/` alongside that territory’s README and `*-sources.md` (if present) |
| **Content** | Dated sections under **Log**; short bullets; optional SHAs and paths |
| **Not** | Record truth, Voice knowledge, or automatic pipeline output. **Not** a substitute for `users/[id]/session-log.md` or RECURSION-GATE. |

**Fence:** History files document **what the operator did or noted in this lane** — not what is canonically true. Facts about the companion belong in the gated Record; integration status belongs in tables such as [work-dev/integration-status.md](work-dev/integration-status.md).

**Relation to instance WORK cadence:** Sessions opened with **`hey`** (operator-cadence) log in **`users/[id]/work-memory.md`** — **territory-wide** rhythm. **`*-history.md`** is **per-lane** breadcrumbs (e.g. “ingested Karpathy digest,” “weekly brief run,” “Jiang CI change”) so ML or humans can scan **where** work landed without merging lanes.

**Existing logs:**

| Territory | File |
|-----------|------|
| work-dev | [work-dev/work-dev-history.md](work-dev/work-dev-history.md) |
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

**Legacy / merged territories** (no dedicated history file; use **work-dev** or parent): `work-build-ai` → work-dev; `work-grace-gems` → work-business/grace-gems (log in **work-business-history** or gem-specific notes).

**Cross-reference:** Authorized sources lists — [work-modules-sources-principle.md](work-modules-sources-principle.md).
