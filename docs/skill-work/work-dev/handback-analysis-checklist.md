# Handback analysis checklist (BUILD-AI-GAP-006)

Use before approving OpenClaw-sourced candidates or when debugging a bad stage.

**Automated slice:** `python scripts/work_dev/validate_handback_analysis.py --file payload.json` (or stdin JSON with `content` and optional `constitution_check_status`).

## Before merge review

1. **Structured vs narrative** — Risk or approval should match **structured** fields (`constitution_check_status`, artifact hashes), not only free-text reassurance.
2. **Constitution line** — If `constitution_check_status` is `advisory_flagged`, the staged `content` must include the `CONSTITUTION_ADVISORY:` line produced by `openclaw_stage.py` (validator enforces consistency).
3. **Human minimize / authority** — If the text adds “low risk” or “VP approved” without new facts, compare to the base scenario without that clause (variation-types V-01, V-02).
4. **Reasoning vs action** — If the narrative warns or rejects but the implied staging outcome is approval-like, treat as a reasoning–action mismatch; do not merge until reconciled.

## Payload shape for the validator

Minimal JSON:

```json
{
  "content": "... full staged text including CONSTITUTION_ADVISORY if any ...",
  "constitution_check_status": "advisory_clear"
}
```

Fields mirror the OpenClaw stage payload / gate candidate body where applicable.
