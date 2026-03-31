# Rolling Daily Brief Analysis — Convergence Ledger v2 Spec

## Purpose

Turn daily briefs from passive snapshots into a repeatable production loop that improves content quality and decision speed over time.

This spec defines a skill-shaped workflow for:
- rapid content extraction (campaign-ready),
- structured synthesis (signal over noise),
- recursive learning (feedback updates the next run).

This version adopts a **Convergence Ledger** pattern so companion signals and agent interpretations can co-exist without blurring authority.

## Scope and authority model

**In scope (WORK lane):**
- Read last 3-7 `daily-brief-YYYY-MM-DD.md` files.
- Generate a rolling synthesis and content outputs.
- Capture what changed in assumptions and messaging posture.
- Record convergence decisions (`accept|defer|reject`) with rationale and review timing.

**Out of scope:**
- Automatic publishing.
- Record merges or gate processing.
- Claims without source citation in public-facing copy.

**Authority model:**
- Companion is decision authority.
- Agent outputs are provisional until convergence decision is recorded.

## Inputs

- Primary: latest daily brief files in `docs/skill-work/work-strategy/`.
- Optional: `daily-brief-focus.md`, `daily-brief-config.json`, `work-politics/content-queue.md`.
- Optional performance context: prior drafted outputs and operator accept/reject notes.

## Outputs (per run)

1. **Rolling synthesis** (250-400 words):
   - persistent themes (what stayed true),
   - new deltas (what changed in last 24-72h),
   - disproportion callout (which shift matters most),
   - one recommended posture.

2. **Content pack (minimum):**
   - 1 principal memo paragraph,
   - 2-3 candidate post hooks,
   - 1 counter-frame line for opposition narrative.
   - style labels required: `narrative-stance` for principal paragraph, `public-hook` for short hooks.

3. **Learning delta (required):**
   - "what changed in our model today" (3 bullets max),
   - "what to test tomorrow" (1-2 items).

4. **Convergence Ledger entries** (1-3 entries):
   - only for high-value disagreements, high-impact shifts, or repeated stale frames.

## Convergence Ledger v2 schema

Each ledger entry must include:
- `id`
- `timestamp`
- `domain` (`work-strategy`, `work-politics`, `work-dev`, or mixed)
- `companion_signal`
- `agent_interpretation`
- `decision` (`accept|defer|reject`)
- `rationale`
- `confidence` (`high|medium|low`)
- `impact` (`high|medium|low`)
- `next_test`
- `review_by` (required when `decision=defer`)
- `supersedes` (optional)
- `source_briefs` (paths/dates)

## Process (v2)

1. Ingest last N briefs (default N=3; expandable to 7).
2. Extract recurring entities, conflict lines, deadlines, and unresolved tasks.
3. Classify items as:
   - **stable** (carry forward),
   - **new** (requires response),
   - **stale** (stop repeating unless revalidated).
4. Draft synthesis + content pack.
5. Select at most 1-3 high-value convergence decisions:
   - high impact + high uncertainty,
   - companion/agent disagreement,
   - repeated stale frame that keeps resurfacing.
6. Write ledger entries and learning delta note.
7. Link any superseded entries to prevent contradiction sprawl.

## Quality bar

- Every claim in synthesis links to at least one brief/source reference.
- Content hooks must be tied to current cycle dates or active themes.
- No generic "trend talk" without action implication.
- Keep language concise and operator-ready (decision support, not essay mode).
- Do not log low-signal noise; if an item has no next test, it should usually not enter the ledger.
- Preserve mode separation: governance and ledger rationale stay `operator-brief`; narrative paragraph must be `narrative-stance`.

## Success metrics (2-week trial)

- Time from brief generation to first usable draft decreases.
- Percentage of runs producing at least one adopted content item.
- Reduction in repeated stale talking points.
- Clearer day-over-day model updates (learning delta present every run).
- `disagreement_rate`: companion vs agent mismatch rate.
- `time_to_resolution`: age from `defer` to resolved state.

## Operational guardrails

- WORK-only artifact; do not treat as Record input.
- Human review required before any public posting.
- If source certainty is low, mark explicitly as provisional.
- No automatic promotion from ledger to SELF/EVIDENCE.
- Weekly sweep must review all deferred entries (`close|extend|promote`).

## Related implementation files

- Narrative log template target: `docs/skill-work/work-strategy/narrative-feedback-loop.md`
- Ops rhythm target: `docs/skill-work/work-strategy/narrative-feedback-loop-ops.md`
- Skill draft target: `skills-portable/_drafts/skill-narrative/SKILL.md`
