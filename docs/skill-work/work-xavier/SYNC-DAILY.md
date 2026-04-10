# SYNC-DAILY (xavier only)

**Purpose:** Single daily sync control surface for Xavier.

Use this file during **`coffee`** (work-start or signing-off) to aggregate `work-dev` and `work-politics` sync status in one place. Legacy **`hey`** still works as an alias for the same ritual.

---

## Daily sync snapshot

Date: **2026-04-10**

- **stale sync state:** `no` — both mirrors have a dated row in `SYNC-LOG.md` for this date (see [work-dev-mirror/SYNC-LOG.md](work-dev-mirror/SYNC-LOG.md), [work-politics-mirror/SYNC-LOG.md](work-politics-mirror/SYNC-LOG.md)).

### 1) work-dev mirror
- status: `no relevant updates`
- score (impact + urgency + xavier-readiness): `2/9`
- proposed updates (max 5):
  - _(none this scan)_
- action today:
  - Append sync-log row; optional deeper diff deferred until next relevant grace-mar work-dev change.

### 2) work-politics mirror
- status: `no relevant updates`
- score (impact + urgency + xavier-readiness): `2/9`
- proposed updates (max 5):
  - _(none this scan)_
- action today:
  - Append sync-log row; optional deeper diff deferred until next relevant grace-mar work-politics change.

### 3) Combined next action
- top sync task: Keep **≤3-day** rhythm on both `SYNC-LOG.md` files; re-run relevance scan if either log goes stale.
- owner: operator
- done by: next **`coffee`** or end-of-day touch

---

## Staleness guardrail

If either mirror has no new sync-log row for more than 3 days, mark:

- `stale sync state: yes`

and run a forced relevance scan before any other optimization tasks.

---

## Template alignment check (xavier only)

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
- selected top sync action: Mirror logs + snapshot updated (2026-04-10).
- selected top execution action: _(see card)_
- selected top gate action: _(none — grace-mar gate unchanged this pass)_
- card path: [DAILY-OPS-CARD.md](DAILY-OPS-CARD.md)

