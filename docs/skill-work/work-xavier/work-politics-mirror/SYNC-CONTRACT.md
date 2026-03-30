# work-politics sync contract (manual, daily-check)

**Goal:** Let Xavier manually and safely sync relevant `work-politics` updates from Grace-Mar.

**Template upstream for alignment checks:** `https://github.com/rbtkhn/companion-self` (ref: `main` unless pinned in `../SYNC-DAILY.md`).

Process:
- detect relevant updates
- propose a minimal sync set
- review before applying
- log decision

Never auto-apply Record changes.

---

## Daily good-morning sync check

Each `hey`, run a `work-politics` relevance scan and return:

1. **No relevant updates**, or
2. **Relevant updates found** (top updates to mirror)

Record outcome in [SYNC-LOG.md](SYNC-LOG.md).

Also run template alignment against companion-self sync-pack per [../GOOD-MORNING.md](../GOOD-MORNING.md).

---

## Relevance criteria

Relevant for Xavier when updates affect:

- content workflow or approval flow
- sourcing/receipt discipline
- stress-test or risk triage patterns
- KPI, budget, and weekly rhythm controls
- escalation and boundary language that affects ship safety

Usually not relevant:

- campaign-specific details not in Xavier scope
- deep implementation internals unrelated to operator workflow
- one-off historical notes with no process impact

---

## Xavier-only relevance scoring rubric

Score each candidate update on three axes (0-3 each):

- **impact**: effect on workflow safety/quality
- **urgency**: cost of waiting one week
- **xavier-readiness**: practical usability at current skill level

Total score = `impact + urgency + xavier-readiness` (0-9).

Decision rule:

- `0-3`: skip for now
- `4-5`: optional, batch into weekly sync
- `6-9`: sync this week (or today if safety-related)

---

## No-terminal scan prompt

```text
Run my daily work-politics mirror sync check.

Use:
- docs/skill-work/work-politics/
- docs/skill-work/work-xavier/work-politics-mirror/SYNC-CONTRACT.md
- docs/skill-work/work-xavier/work-politics-mirror/SYNC-LOG.md

Tasks:
1) Identify updates since last logged sync date.
2) Filter by relevance criteria in SYNC-CONTRACT.
3) Output:
   - no relevant updates OR
   - top 1-5 files to sync with one-line reasons
4) Score each proposed file (impact/urgency/xavier-readiness; total).
5) Propose minimal mirror edits (paths only), no apply.
6) Draft one SYNC-LOG row and one SYNC-DAILY update block.
```

---

## Optional terminal path (operator-supported)

From repo root:

```bash
git log --since="7 days ago" --name-only -- docs/skill-work/work-politics
```

Review candidates manually before mirroring.

---

## Safety rules

- Sync only into `work-xavier/work-politics-mirror/*` unless explicitly requested.
- No direct writes to **`her`** `users/xavier/self.md` during sync.
- If sync insight implies identity update, stage via **`her`** `users/xavier/recursion-gate.md`.
- Human approval remains required for public ship decisions.

