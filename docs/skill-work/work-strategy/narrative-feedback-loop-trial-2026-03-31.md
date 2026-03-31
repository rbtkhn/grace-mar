# Narrative Feedback Loop — 2-Week Pilot Tracker

**Pilot window:** 2026-03-31 to 2026-04-13  
**Model:** Convergence Ledger v2  
**Primary references:** `rolling-daily-brief-analysis-spec.md`, `narrative-feedback-loop.md`, `narrative-feedback-loop-ops.md`

## Goal

Validate whether `skill-narrative` improves content throughput and learning quality versus baseline daily-brief workflow.

## Success metrics

- `adoption_rate` = used outputs / generated outputs
- `disagreement_rate` = disagreement entries / total ledger entries
- `time_to_resolution` = avg days from `defer` to resolved state
- `stale_frame_recurrence` = repeated stale frames per week
- `model_update_clarity` = days with non-empty learning delta / total run days

## Daily run log

| Date | Brief window (N) | Generated outputs (count) | Used outputs (count) | Ledger entries (count) | Disagreements (count) | Defers open | Learning delta present (Y/N) | Notes |
|------|-------------------|---------------------------|----------------------|------------------------|-----------------------|-------------|------------------------------|-------|
| 2026-03-31 | 3 | 4 | TBD | 1 | TBD | TBD | Y | Pilot initialized with v2 schema and first accepted entry in ledger template. |
| 2026-04-01 | | | | | | | | |
| 2026-04-02 | | | | | | | | |
| 2026-04-03 | | | | | | | | |
| 2026-04-04 | | | | | | | | |
| 2026-04-05 | | | | | | | | |
| 2026-04-06 | | | | | | | | |
| 2026-04-07 | | | | | | | | |
| 2026-04-08 | | | | | | | | |
| 2026-04-09 | | | | | | | | |
| 2026-04-10 | | | | | | | | |
| 2026-04-11 | | | | | | | | |
| 2026-04-12 | | | | | | | | |
| 2026-04-13 | | | | | | | | |

## Weekly defer sweep checkpoints

| Sweep date | Deferred reviewed | Closed | Extended | Promoted | Notes |
|------------|-------------------|--------|----------|----------|-------|
| 2026-04-06 | TBD | TBD | TBD | TBD | Week 1 sweep |
| 2026-04-13 | TBD | TBD | TBD | TBD | Week 2 sweep |

## Final evaluation (fill on 2026-04-13)

- `adoption_rate`: TBD
- `disagreement_rate`: TBD
- `time_to_resolution`: TBD
- `stale_frame_recurrence`: TBD
- `model_update_clarity`: TBD

### Verdict

- **Keep as default / keep with changes / sunset:** TBD
- **Top 3 gains:** TBD
- **Top 3 failure modes:** TBD
- **Next iteration changes:** TBD
