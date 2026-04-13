# Memory Brief → Gate Candidate Demo

This walkthrough shows how Grace-Mar turns runtime observations into bounded context and, only if warranted, into a reviewable gate candidate.

Normative progressive-disclosure order and rules: [docs/runtime/memory-retrieval.md](../runtime/memory-retrieval.md). Provenance staging details: [docs/runtime/provenance-staging.md](../runtime/provenance-staging.md).

## Why this demo exists

Grace-Mar separates runtime memory from canonical Record truth. This flow shows the boundary in action:

- retrieve compactly
- inspect context
- expand selectively
- build prepared context
- stage a candidate **only** for review (optional, explicit operator choice)

For a single command that bundles search → timeline → bounded expansion into one Markdown file, see `scripts/runtime/memory_brief.py` and [read-hints.md](../runtime/read-hints.md). This document spells out **each script** so the orchestration is visible.

## Scenario

You are working in `work-strategy` and want to revisit a recurring theme: cleaner notebook writing boundaries for `skill-strategy`.

You need a ledger with relevant observations (see `scripts/runtime/log_observation.py` and [runtime/observations/README.md](../../runtime/observations/README.md)). Replace placeholders like `<best_obs_id>` with IDs from your search results.

## Step 1 — Search runtime observations

```bash
python3 scripts/runtime/lane_search.py \
  --lane work-strategy \
  --query "skill strategy notebook boundary" \
  --limit 5
```

**Expected result:**

- Compact hits only (no raw `notes` dump in the default path).
- Scored lines you can scan quickly.
- One likely **anchor** observation to inspect in context (top hit or best match).

## Step 2 — Inspect timeline context

```bash
python3 scripts/runtime/lane_timeline.py \
  --anchor <best_obs_id> \
  --before 2 \
  --after 2
```

**Expected result:**

- Surrounding observations in chronological order (same lane by default).
- Enough context to see whether the idea is isolated or recurring.

## Step 3 — Expand selected observations

```bash
python3 scripts/runtime/expand_observations.py \
  --id <obs_id_1> \
  --id <obs_id_2> \
  --id <obs_id_3> \
  --markdown
```

**Expected result:**

- Richer detail for a few chosen observations only (stdout unless you add `-o` / `--output`).
- Source refs, tags, notes, contradictions if present on those rows.

## Step 4 — Build bounded prepared context

```bash
python3 scripts/prepared_context/build_context_from_observations.py \
  --lane work-strategy \
  --id <obs_id_1> \
  --id <obs_id_2> \
  --id <obs_id_3> \
  --output prepared-context/runtime-observation-context.md
```

**Expected result:**

- A **runtime-only** context artifact (inspectable Markdown).
- Compact brief, key points, and an explicit boundary notice that this is **not** canonical Record truth.

Treat the file as operator scratch unless you intentionally commit it.

## Step 5 — Decide whether a gate candidate is warranted

Only run this if observations converge on a **durable** change worth companion review — not for every lookup.

```bash
python3 scripts/runtime/stage_candidate_from_observations.py \
  -u grace-mar \
  --lane work-strategy \
  --candidate-type skill_update \
  --target-surface SKILLS \
  --target-path skills-portable/skill-strategy.md \
  --id <obs_id_1> \
  --id <obs_id_2> \
  --id <obs_id_3> \
  --proposal-summary "Refine skill-strategy notebook writing boundary" \
  --proposed-change "Skill-strategy should write compact notebook-linked summaries and avoid raw prose dumps into strategy-notebook." \
  --why-now "Multiple recent observations converge on the same notebook hygiene issue."
```

**Expected result:**

- A new **`### CANDIDATE-NNNN`** block in `users/grace-mar/recursion-gate.md` with YAML `status: pending` (pending review; see [provenance-staging.md](../runtime/provenance-staging.md)).
- Explicit provenance (`source_observation_ids`, etc.).
- **No** automatic mutation of SKILLS, SELF, or other Record surfaces — `RUNTIME_OBSERVATION_PROPOSAL` candidates follow the merge-skip path until a human applies the change after approval.

Default user id is `grace-mar` (or `GRACE_MAR_USER_ID`); `-u` makes the fork explicit.

## What this demo teaches

- **Runtime memory** is useful, but not canonical.
- **Retrieval** is progressive: survey before detail.
- **Prepared context** is explicit and inspectable.
- **Durable change** still flows through **review** (`recursion-gate.md`), not silent writes.

## Claude Code translation

If you think in Claude Code terms, this flow is roughly:

| Phase | Claude Code mental model | This demo |
|-------|--------------------------|-----------|
| Entry | command / workflow | shell steps from repo root |
| Recall | memory lookup | `lane_search` → `lane_timeline` |
| Focus | context narrowing | `expand_observations` on chosen IDs |
| Bundle | bounded context artifact | `build_context_from_observations` |
| Handoff | review queue | optional `stage_candidate_from_observations` → gate |

In Grace-Mar terms, the important distinction is that **runtime assistance does not bypass the gate**.

## Files involved

| Piece | Role |
|-------|------|
| [scripts/runtime/lane_search.py](../../scripts/runtime/lane_search.py) | Compact ledger search |
| [scripts/runtime/lane_timeline.py](../../scripts/runtime/lane_timeline.py) | Chronological window |
| [scripts/runtime/expand_observations.py](../../scripts/runtime/expand_observations.py) | Bounded field expansion |
| [scripts/prepared_context/build_context_from_observations.py](../../scripts/prepared_context/build_context_from_observations.py) | Prepared-context Markdown |
| [scripts/runtime/stage_candidate_from_observations.py](../../scripts/runtime/stage_candidate_from_observations.py) | Provenance-backed gate staging |
| `prepared-context/runtime-observation-context.md` | Example output path (operator-local unless committed) |
| `users/grace-mar/recursion-gate.md` | Approval Inbox target when staging |

## Boundary reminder

This demo does **not** update SELF, SELF-LIBRARY, SKILLS, or EVIDENCE directly. It shows how runtime memory can **support** reviewable change without becoming governed truth on its own.
