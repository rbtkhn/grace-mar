---
name: skill-narrative
preferred_activation: narrative loop
description: Compile rolling daily briefs into a convergence-led narrative with content outputs and explicit accept/defer/reject decisions for recursive learning.
portable: true
version: 0.1.0
tags:
- operator
- work-strategy
- narrative
- feedback
portable_source: skills-portable/skill-narrative/SKILL.md
synced_by: sync_portable_skills.py
---
# Skill-Narrative (Convergence Ledger v2)

**Preferred activation (operator):** say **`narrative loop`**.

Use this skill to convert recent daily briefs into actionable narrative outputs while preserving a decision trail that improves future runs.

## When to run

- You have 3-7 recent daily briefs and need current narrative posture.
- You need content outputs plus a learning loop, not just summary text.
- You want explicit companion/agent convergence decisions (`accept|defer|reject`).

## Inputs

- Recent daily briefs (`daily-brief-YYYY-MM-DD.md`).
- Optional focus/config docs for keyword and strategy context.
- Optional prior ledger entries for continuity.

## Outputs (each run)

1. Rolling synthesis (persistent themes + deltas + recommended posture).
2. Content pack:
   - 1 principal memo paragraph,
   - 2-3 post hooks,
   - 1 counter-frame line.
3. Learning delta:
   - what changed today,
   - what to test next.
4. Convergence Ledger entries (1-3 high-value items only).

## Linguistic style modes (required)

Use explicit mode labels so tone is intentional and stable:

- `operator-brief` (default internal mode)
  - Tone: sober, analytic, compact.
  - Use for: synthesis diagnostics, decision support, ledger rationale.
  - Constraint: minimal rhetoric; emphasize clarity and provenance.

- `narrative-stance` (distinct narrative mode)
  - Tone: slightly warmer, human-scale, forward-leaning.
  - Use for: principal memo paragraph and narrative posture lines.
  - Constraint: still evidence-bound; no theatrical language; no persona roleplay.

- `public-hook`
  - Tone: concise, persuasive, high-signal.
  - Use for: short hooks/candidate posts.
  - Constraint: draft-only; requires human review before publication.

Mode policy:
- Always produce outputs with mode labels.
- Keep `operator-brief` for governance/decision blocks.
- Require at least one `narrative-stance` paragraph each run so this skill remains distinct from pure operator analytics.

## Method

1. Ingest last N briefs (`N=3` default, `N=7` in high volatility).
2. Extract:
   - stable themes,
   - new deltas,
   - stale/repeating frames.
3. Draft synthesis + content outputs.
   - Synthesis can remain `operator-brief`.
   - Principal narrative paragraph must be `narrative-stance`.
   - Short hooks should be `public-hook`.
4. Log only high-value decisions:
   - high-impact + high-uncertainty,
   - companion/agent disagreement,
   - repeated stale frame.
5. Record each decision with rationale and next test.
6. For deferred items, set a required review date.

## Convergence Ledger schema

Each entry should include:
- `id`
- `timestamp`
- `domain`
- `companion_signal`
- `agent_interpretation`
- `decision` (`accept|defer|reject`)
- `rationale`
- `confidence`
- `impact`
- `next_test`
- `review_by` (required if `decision=defer`)
- `supersedes` (optional)
- `source_briefs`

## Cadence

- **Daily:** run synthesis + content pack + 1-3 ledger entries.
- **Weekly:** sweep all deferred entries (`close|extend|promote`) and archive resolved ones.

## Guardrails

- WORK-only process layer; do not treat outputs as Record truth.
- No automatic promotion to SELF/EVIDENCE.
- Public-facing copy still requires human review and source checks.
- If an item has no clear `next_test`, usually do not log it.


## Cursor / grace-mar instance

Grace-mar paths and runbook links for this repository (from `.cursor/skills/skill-narrative/`).

| Topic | Path |
|--------|------|
| Core v2 spec | [docs/skill-work/work-strategy/rolling-daily-brief-analysis-spec.md](../../../docs/skill-work/work-strategy/rolling-daily-brief-analysis-spec.md) |
| Ledger file | [docs/skill-work/work-strategy/narrative-feedback-loop.md](../../../docs/skill-work/work-strategy/narrative-feedback-loop.md) |
| Ops protocol | [docs/skill-work/work-strategy/narrative-feedback-loop-ops.md](../../../docs/skill-work/work-strategy/narrative-feedback-loop-ops.md) |
| Daily briefs directory | [docs/skill-work/work-strategy/](../../../docs/skill-work/work-strategy/) |
| Work-domain histories | [work-strategy-history](../../../docs/skill-work/work-strategy/work-strategy-history.md), [work-politics-history](../../../docs/skill-work/work-politics/work-politics-history.md), [work-dev-history](../../../docs/skill-work/work-dev/work-dev-history.md) |
| Portable manifest | [skills-portable/manifest.yaml](../../../skills-portable/manifest.yaml) |
| Sync implementation | [scripts/sync_portable_skills.py](../../../scripts/sync_portable_skills.py) |

**Run reminder:** keep ledger entries sparse (1-3 high-value items per run) and enforce `review_by` on all `defer` decisions.
