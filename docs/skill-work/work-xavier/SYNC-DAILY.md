# SYNC-DAILY (xavier only)

**Purpose:** Single daily sync control surface for Xavier.

Use this file during `hey` to aggregate `work-dev` and `work-politics` sync status in one place.

---

## Daily sync snapshot

Date: `YYYY-MM-DD`

### 1) work-dev mirror
- status: `no relevant updates` / `relevant updates found` / `blocked - needs operator review`
- score (impact + urgency + xavier-readiness): `_/9`
- proposed updates (max 5):
  - 
- action today:
  - 

### 2) work-politics mirror
- status: `no relevant updates` / `relevant updates found` / `blocked - needs operator review`
- score (impact + urgency + xavier-readiness): `_/9`
- proposed updates (max 5):
  - 
- action today:
  - 

### 3) Combined next action
- top sync task:
- owner:
- done by:

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

- ops-card status: `not started` / `drafted` / `finalized`
- selected top sync action:
- selected top execution action:
- selected top gate action:
- card path: [DAILY-OPS-CARD.md](DAILY-OPS-CARD.md)

