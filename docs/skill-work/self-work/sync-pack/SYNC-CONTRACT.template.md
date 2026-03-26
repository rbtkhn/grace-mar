# {{territory}} sync contract (manual, review-first)

**Scope:** {{instance_or_workspace}}

**Goal:** Manually and safely sync relevant updates from `{{source_path}}` into `{{mirror_path}}`.

---

## Daily/weekly sync check cadence

Run a relevance scan and output one of:

1. `no relevant updates`
2. `relevant updates found`
3. `blocked - needs operator review`

Record every check in `{{mirror_path}}/SYNC-LOG.md`.

---

## Relevance criteria (customize)

Treat updates as relevant when they affect:

- {{criterion_1}}
- {{criterion_2}}
- {{criterion_3}}

Usually not relevant:

- deep implementation internals without workflow impact
- one-off historical notes with no process change
- features outside this instance's current maturity level

---

## Optional scoring rubric (recommended)

Score each candidate update:

- `impact` (0-3)
- `urgency` (0-3)
- `instance-readiness` (0-3)

Total = 0-9.

Decision guide:

- `0-3`: skip for now
- `4-5`: batch into weekly sync
- `6-9`: sync this week (or today if safety-related)

---

## No-terminal scan prompt

```text
Run a sync relevance check for {{territory}}.

Use:
- {{source_path}}
- {{mirror_path}}/SYNC-CONTRACT.md
- {{mirror_path}}/SYNC-LOG.md

Tasks:
1) Identify updates since last logged sync date.
2) Filter with relevance criteria.
3) Return status + top 1-5 candidate files.
4) Score candidates (impact/urgency/instance-readiness).
5) Propose mirror edit paths only (no apply).
6) Draft one SYNC-LOG row.
```

---

## Safety rules

- Sync into `{{mirror_path}}/*` only unless explicitly approved.
- Do not write identity truth files during sync.
- Stage any identity implications through gate flow.
- Require human review before consequential wording changes.

