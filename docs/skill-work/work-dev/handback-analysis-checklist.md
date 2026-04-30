# Handback analysis checklist (BUILD-AI-GAP-006)

Use before approving OpenClaw-sourced candidates or when debugging a bad stage.

**Automated slice:** `python scripts/work_dev/validate_handback_analysis.py --file payload.json` (or stdin JSON with `content`, optional `summary` / `analysis` / `reasoning`, optional `constitution_check_status`, optional `staged_risk_tier`). When `staged_risk_tier` is supplied, the validator checks obvious two-way narrative mismatches: approval-like tiers with high-concern phrasing, and manual/high tiers with approval-like phrasing.

## Before merge review

1. **Structured vs narrative** - Risk or approval should match **structured** fields (`constitution_check_status`, artifact hashes), not only free-text reassurance.
2. **Constitution line** - If `constitution_check_status` is `advisory_flagged`, the staged `content` must include the `CONSTITUTION_ADVISORY:` line produced by `openclaw_stage.py` (validator enforces consistency).
3. **Human minimize / authority** - If the text adds "low risk" or "VP approved" without new facts, compare to the base scenario without that clause (variation-types V-01, V-02).
4. **Reasoning vs action** - If the narrative warns or rejects but the implied staging outcome is approval-like, treat as a reasoning-action mismatch; do not merge until reconciled.

## Payload shape for the validator

Minimal JSON:

```json
{
  "content": "... full staged text including CONSTITUTION_ADVISORY if any ...",
  "constitution_check_status": "advisory_clear",
  "staged_risk_tier": "low"
}
```

Optional narrative fields:

```json
{
  "content": "... staged content ...",
  "summary": "... staged candidate summary ...",
  "analysis": "... handback analysis text ...",
  "reasoning": "... model reasoning summary ...",
  "staged_risk_tier": "manual_escalate"
}
```

Omit `staged_risk_tier` if the pipeline does not yet classify risk. When set to `low`, `medium`, or `quick_merge_eligible`, obvious high-concern wording fails validation. When set to `manual_escalate`, `high`, `advisory_flagged`, `reject`, or `blocked`, obvious approval-like wording fails validation.

Fields mirror the OpenClaw stage payload / gate candidate body where applicable.

## Automation in-repo (vs remaining gap)

**Implemented today**

- Validator: [`scripts/work_dev/validate_handback_analysis.py`](../../../scripts/work_dev/validate_handback_analysis.py) - checks **embedded** `CONSTITUTION_ADVISORY: status = ...` against `constitution_check_status`, and that `advisory_flagged` implies an advisory line in `content`. Optional **`staged_risk_tier`**: if set, rejects obvious two-way phrase mismatches between free-text reasoning fields and structured risk tier (reasoning-action guard; not full NLP).
- Tests: [`tests/test_validate_handback_analysis.py`](../../../tests/test_validate_handback_analysis.py).
- **CI:** Those tests run on every push and pull request to `main` as part of `pytest tests/` in [`.github/workflows/test.yml`](../../../.github/workflows/test.yml) (job `Tests` -> step "Run pytest").

**Still open (BUILD-AI-GAP-006 "partial")**

- Full semantic alignment between narrative and classification (beyond phrase heuristics and optional `staged_risk_tier`). Manual review still uses **Before merge review** items 3-4 for edge cases and when `staged_risk_tier` is omitted.
