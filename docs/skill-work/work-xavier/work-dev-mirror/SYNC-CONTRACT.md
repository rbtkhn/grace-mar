# work-dev sync contract (manual, daily-check)

**Goal:** Let Xavier manually and safely sync relevant `work-dev` updates from Grace-Mar.

**Template upstream for alignment checks:** `https://github.com/rbtkhn/companion-self` (ref: `main` unless pinned in `../SYNC-DAILY.md`).

This is a **review-first** sync pattern:
- detect relevant updates
- decide sync set
- apply manually with review
- log result

Never auto-apply changes to Record files.

---

## Daily good-morning sync check

Every `good morning`, run a `work-dev` relevance scan and produce one of:

1. **No relevant updates**
2. **Relevant updates found** with recommended files to sync

Use [SYNC-LOG.md](SYNC-LOG.md) to record the result.

Also run template alignment against companion-self sync-pack per [../GOOD-MORNING.md](../GOOD-MORNING.md).

---

## Relevance criteria

A `work-dev` update is relevant to Xavier if it changes:

- gate discipline, staging, or approval flow
- reliability/stress-test methods
- provenance/source-integrity practices
- no-terminal operating prompts or checklists
- weekly operating rhythm that maps to LO-02..LO-06

Not relevant by default:

- deep implementation internals
- OpenClaw-specific technical wiring Xavier is not using yet
- CI-only changes without operator workflow impact

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
Scan for relevant updates in docs/skill-work/work-dev/ since my last sync.

Inputs:
- docs/skill-work/work-dev/
- docs/skill-work/work-xavier/work-dev-mirror/
- docs/skill-work/work-xavier/work-dev-mirror/SYNC-LOG.md

Tasks:
1) Identify what changed since last logged sync date.
2) Filter by relevance to Xavier using SYNC-CONTRACT criteria.
3) Output:
   - no relevant updates OR
   - top 1-5 files to sync with one-line reason each
4) Score each proposed file (impact/urgency/xavier-readiness; total).
5) Propose minimal mirror edits (file paths only), no apply.
6) Draft one SYNC-LOG row and one SYNC-DAILY update block.
```

---

## Optional terminal path (operator-supported)

From repo root:

```bash
git log --since="7 days ago" --name-only -- docs/skill-work/work-dev
```

Then manually review candidate files before mirroring into `work-xavier/work-dev-mirror/`.

---

## Safety rules

- Sync into `work-xavier/work-dev-mirror/*` only.
- Do not write to `users/xavier/self.md` during sync.
- If sync implies identity changes, stage candidates in `users/xavier/recursion-gate.md`.
- Human review required before finalizing consequential wording changes.

