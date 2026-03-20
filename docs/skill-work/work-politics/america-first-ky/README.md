# America First Kentucky — guardrail methodology (WORK)

This folder holds **WORK-only** methodology for `@usa_first_ky` / Massie pilot outputs: factorial **stress-testing** and human guardrails inspired by independent clinical AI safety research (see [guardrail-stress-test.md](guardrail-stress-test.md)).

**Not** part of the companion Record unless merged via RECURSION-GATE. **Not** enforced by `governance_checker.py`.

## Contents

| File | Purpose |
|------|---------|
| [guardrail-stress-test.md](guardrail-stress-test.md) | Framework: four failure modes, factorial variations, operator checklist |
| [stress-test-brief-template.md](stress-test-brief-template.md) | Paste template for high-stakes briefs |
| [AGENT-SESSION-BRIEF.md](AGENT-SESSION-BRIEF.md) | **Start here for the next agent session** — compliant implementation plan |

## Pipeline events (operator-only audit)

`scripts/emit_pipeline_event.py` accepts arbitrary `event_type` strings; no code change required for stress-test logging. Suggested types (see [guardrail-stress-test.md](guardrail-stress-test.md#suggested-pipeline-events-optional)):

- `stress_test_proposed`
- `stress_test_passed` / `stress_test_failed`
- `guardrail_mismatch_detected`

Example (adjust `-u` if needed):

```bash
python scripts/emit_pipeline_event.py stress_test_passed none brief=weekly-2026-03-20 territory=wap
```

## Quick link

- External SMM pack: `docs/externals/massie/smm-training/`
- Advisor-facing summary (four failure modes + factorial table): [guardrail-stress-test-advisor-one-pager.md](../../../externals/massie/guardrail-stress-test-advisor-one-pager.md)
