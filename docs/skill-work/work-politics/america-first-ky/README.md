# America First Kentucky — guardrail methodology (WORK)

This folder holds **WORK-only** methodology for `@usa_first_ky` / Massie pilot outputs: factorial **stress-testing**, **proactive-loop** scheduling discipline, and human guardrails inspired by independent clinical AI safety research (see [guardrail-stress-test.md](guardrail-stress-test.md)).

**Not** part of the companion Record unless merged via RECURSION-GATE. **Not** enforced by `governance_checker.py`.

## Contents

| File | Purpose |
|------|---------|
| [proactive-loop.md](proactive-loop.md) | Scheduled-loop **framework**: memory, proactivity, tools — all gated; where to log ([loop-history.md](loop-history.md)) |
| [massie-advisor-prompt.md](massie-advisor-prompt.md) | **WORK-only** Massie / KY-4 drafting voice for external LLM sessions — **not** `bot/prompt.py`; never merge without explicit governance |
| [scheduled-habit.md](scheduled-habit.md) | Optional **cron / habit** examples (daily brief, scaffolds, loop events) — no auto-merge |
| [templates/daily-loop-brief.md](templates/daily-loop-brief.md) | Template for a single cycle brief (three lenses + stress-test fields) |
| [loop-history.md](loop-history.md) | Append-only WORK log for cycle notes (not `self-evidence.md`) |
| [guardrail-stress-test.md](guardrail-stress-test.md) | Framework: four failure modes, factorial variations, operator checklist |
| [stress-test-brief-template.md](stress-test-brief-template.md) | Paste template for high-stakes briefs |
| [AGENT-SESSION-BRIEF.md](AGENT-SESSION-BRIEF.md) | **Start here for the next agent session** — compliant implementation plan |

## Pipeline events (operator-only audit)

`scripts/emit_pipeline_event.py` accepts arbitrary `event_type` strings; no code change required for stress-test or loop logging. Suggested types (see [guardrail-stress-test.md](guardrail-stress-test.md#suggested-pipeline-events-optional)):

- `stress_test_proposed`
- `stress_test_passed` / `stress_test_failed`
- `guardrail_mismatch_detected`

**Proactive loop** (optional — see [proactive-loop.md](proactive-loop.md)):

- `loop_cycle_started`
- `loop_cycle_staged`
- `loop_cycle_approved`

Example (adjust `-u` if needed):

```bash
python scripts/emit_pipeline_event.py stress_test_passed none brief=weekly-2026-03-20 territory=wap
```

```bash
python scripts/emit_pipeline_event.py loop_cycle_staged none territory=wap cycle=daily-loop-brief
```

## Scaffolds (optional, WORK only)

| Command | Output |
|---------|--------|
| `python scripts/scaffold_stress_test_brief.py <issue-slug>` | Dated `stress-test-brief-YYYY-MM-DD-<slug>.md` from [stress-test-brief-template.md](stress-test-brief-template.md) |
| `python scripts/scaffold_daily_loop_brief.py [optional-slug]` | Dated `daily-loop-brief-YYYY-MM-DD.md` or `daily-loop-brief-YYYY-MM-DD-<slug>.md` from [templates/daily-loop-brief.md](templates/daily-loop-brief.md); prepends the date into the **Cycle** line |

Both write only under this folder; they do not touch the Record. See `--dry-run`, `--date`, `--force` in each script’s `--help`.

**Loop pipeline helper (optional):** `python scripts/emit_loop_event.py --phase started|staged|approved` wraps [`emit_pipeline_event.py`](../../../../scripts/emit_pipeline_event.py) via subprocess — see [scheduled-habit.md](scheduled-habit.md).

## Quick link

- External SMM pack: `docs/externals/massie/smm-training/`
- Advisor-facing summary (four failure modes + factorial table): [guardrail-stress-test-advisor-one-pager.md](../../../externals/massie/guardrail-stress-test-advisor-one-pager.md)
