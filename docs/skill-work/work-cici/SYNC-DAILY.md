# SYNC-DAILY (Cici advisor lane)

**Purpose:** Single daily sync control surface for the Cici advisor lane.
Community activation tracking companion: [cici-ai-community-dashboard.md](cici-ai-community-dashboard.md).

**Legacy note: formerly Xavier.** Historical snapshots in this file may still contain older labels.

Use this file during **`coffee`** (work-start or signing-off) to aggregate `work-dev` and `work-politics` sync status in one place. Legacy **`hey`** still works as an alias for the same ritual.

---

## Daily sync snapshot

Date: **2026-04-12**

- **stale sync state:** `no` — both mirrors have a fresh row in `SYNC-LOG.md` for this date (see [work-dev-mirror/SYNC-LOG.md](work-dev-mirror/SYNC-LOG.md), [work-politics-mirror/SYNC-LOG.md](work-politics-mirror/SYNC-LOG.md)).

### 1) work-dev mirror
- status: `relevant updates found`
- score (impact + urgency + cici-readiness): `5/9`
- proposed updates (max 5):
  - `docs/skill-work/work-dev/workspace.md`
  - `docs/skill-work/work-dev/implementation-ledger.md`
  - `docs/skill-work/work-dev/handback-analysis-checklist.md`
  - `docs/skill-work/work-dev/dev-notebook/work-dev/journal/README.md`, `daily-dev-journal-inbox.md`
  - _(optional)_ `known-gaps.md` / `work-dev-history.md` if tracking GAP-005/006 alignment
- action today:
  - Logged 2026-04-12 row; pick a minimal copy set into [work-dev-mirror](work-dev-mirror/) on next advisor pass—skip deep CI/scenario-only churn unless needed.

### 2) work-politics mirror
- status: `relevant updates found`
- score (impact + urgency + cici-readiness): `4/9`
- proposed updates (max 5):
  - `docs/skill-work/work-politics/workspace.md`
  - `docs/skill-work/work-politics/polling-and-markets.md`
  - `docs/skill-work/work-politics/brief-source-registry.md`
  - _(defer)_ campaign-only deltas unless Cici is on KY-4 brief cadence this week
- action today:
  - Logged 2026-04-12 row; refresh mirror copies when she is actively on Massie/brief workflow.

### 3) Combined next action
- top sync task: After grace-mar **04-11** batch, prioritize **work-dev** `workspace.md` + handback checklist if her stack touches agent handback; otherwise next **`coffee`** touch.
- owner: operator
- done by: next **`coffee`** or explicit mirror edit session

---

## Staleness guardrail

If either mirror has no new sync-log row for more than 3 days, mark:

- `stale sync state: yes`

and run a forced relevance scan before any other optimization tasks.

---

## Template alignment check (Cici advisor lane)

- template upstream repo: `https://github.com/rbtkhn/companion-self`
- template upstream ref: `main` (or pinned tag/commit)
- status: `aligned` / `minor drift` / `major drift`
- drift items (max 5):
  - 
- proposed alignment edits (paths only):
  - 
- action timing: `today` / `weekly batch`

---

## Daily Ops handoff

- ops-card status: `drafted`
- selected top sync action: Both `SYNC-LOG.md` rows + snapshot updated (2026-04-12); relevance = **found** on both lanes—copy set TBD on next mirror pass.
- selected top execution action: _(see card)_
- selected top gate action: _(none — grace-mar gate unchanged this pass)_
- card path: [DAILY-OPS-CARD.md](DAILY-OPS-CARD.md)

