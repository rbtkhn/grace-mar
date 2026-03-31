# Narrative Feedback Loop — Operating Protocol

## Purpose

Define a repeatable cadence for using the Convergence Ledger with rolling daily-brief synthesis.

## Daily protocol (10-20 minutes)

1. **Select window**
   - Default: last 3 briefs.
   - Escalation mode: last 7 briefs when volatility is high.

2. **Produce run outputs**
   - Rolling synthesis (250-400 words).
   - Content pack (1 principal paragraph, 2-3 hooks, 1 counter-frame).
   - Learning delta ("what changed", "what to test next").

3. **Triage for ledger logging**
   - Log only 1-3 items where at least one is true:
     - high impact + high uncertainty,
     - companion/agent disagreement,
     - repeated stale frame.

4. **Write Convergence Ledger entries**
   - Use template in `narrative-feedback-loop.md`.
   - `defer` requires `review_by`.
   - Keep rationale concise and testable.

5. **Close daily run**
   - Confirm at least one concrete next test is queued.
   - If no high-value decisions emerged, skip ledger write and note "no log-worthy delta."

## Weekly defer sweep (20-30 minutes)

1. Filter all `decision=defer` entries.
2. Resolve each as:
   - `close` (resolved, no further action),
   - `extend` (new `review_by` + reason),
   - `promote` (high-confidence pattern to operating default).
3. Fill `Weekly Defer Sweep` block in `narrative-feedback-loop.md`.
4. Move closed items to Archive section.
5. Capture 1-3 model updates for the next week.

## Decision-state semantics

- `accept`: operational default for upcoming runs.
- `defer`: unresolved uncertainty; must have explicit review date.
- `reject`: explicitly not adopted; keep rationale to avoid rediscovering same dead end.

## Metrics collection (2-week trial)

Track these in the trial period:
- `adoption_rate`: accepted outputs used / total generated outputs.
- `disagreement_rate`: entries where companion and agent diverged.
- `time_to_resolution`: days from defer entry to close/accept/reject.
- `stale_frame_recurrence`: repeated stale frames per week.

## Guardrails

- WORK-only process log; not Record truth.
- No auto-promotion to SELF/EVIDENCE.
- Any public-facing copy requires human review and source checks.
