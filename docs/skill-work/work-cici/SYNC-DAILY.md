# SYNC-DAILY (Cici advisor lane)

**Purpose:** Single daily sync control surface for the Cici advisor lane.
Community activation tracking companion: [cici-ai-community-dashboard.md](cici-ai-community-dashboard.md).

**Legacy note: formerly Xavier.** Historical snapshots in this file may still contain older labels.

Use this file during **`coffee`** (work-start or signing-off) to aggregate `work-dev` and `work-politics` sync status in one place. Legacy **`hey`** still works as an alias for the same ritual.

---

## Daily sync snapshot

Date: **2026-04-30**

- **stale sync state:** `yes` — latest mirror rows are still 2026-04-12 (see [work-dev-mirror/SYNC-LOG.md](work-dev-mirror/SYNC-LOG.md), [work-politics-mirror/SYNC-LOG.md](work-politics-mirror/SYNC-LOG.md)); run forced relevance scans before treating any mirror recommendation as current.

### 1) work-dev mirror
- status: `stale - forced scan required`
- score (impact + urgency + cici-readiness): `pending`
- proposed updates (max 5):
  - forced scan: `docs/skill-work/work-dev/workspace.md`
  - forced scan: `docs/skill-work/work-dev/known-gaps.md`
  - forced scan: `docs/skill-work/work-dev/integration-status.md`
  - forced scan: changed warmup scripts if Cici-facing handback or beginner-safe guidance changed
- action today:
  - Add a dated 2026-04-30 [work-dev-mirror/SYNC-LOG.md](work-dev-mirror/SYNC-LOG.md) row after the scan; mirror only Cici-readable deltas, not deep CI churn.

### 2) work-politics mirror
- status: `stale - forced scan required`
- score (impact + urgency + cici-readiness): `pending`
- proposed updates (max 5):
  - forced scan: `docs/skill-work/work-politics/workspace.md`
  - forced scan: `docs/skill-work/work-politics/polling-and-markets.md`
  - forced scan: `docs/skill-work/work-politics/brief-source-registry.md`
  - defer campaign-only deltas unless Cici is actively on KY-4 brief cadence
- action today:
  - Add a dated 2026-04-30 [work-politics-mirror/SYNC-LOG.md](work-politics-mirror/SYNC-LOG.md) row after the scan; mirror only material she can actually use.

### 3) Combined next action
- top sync task: Run forced relevance scans for both mirrors, append 2026-04-30 sync-log rows, then refresh this snapshot with scored update candidates before any optimization work.
- owner: operator
- done by: next **`coffee D`** / work-cici mirror edit session

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

- ops-card status: `refreshed-stale`
- selected top sync action: Forced relevance scans for both mirrors; do not reuse 2026-04-12 recommendations as current.
- selected top execution action: Update [DAILY-OPS-CARD.md](DAILY-OPS-CARD.md) after the scan with the selected mirror copy set.
- selected top gate action: _(none — grace-mar gate unchanged this pass)_
- card path: [DAILY-OPS-CARD.md](DAILY-OPS-CARD.md)

