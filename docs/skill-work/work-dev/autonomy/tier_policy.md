# Autonomy tier policy (BUILD-AI-GAP-007)

Shadow mode compares **proposed agent action** vs **human action** on the same task class.

- **stay_shadow** — default until evidence meets thresholds in `tier_thresholds.yaml`.
- **limited_expand** — narrow tool scope with continued logging.
- **promote** — not used for merge authority; Record merge stays human-gated.

Log lines go to `runtime/autonomy/shadow_decisions.jsonl` (local, gitignored) via `scripts/work_dev/log_shadow_decision.py`.

## Evaluate tier from the log

`scripts/work_dev/evaluate_autonomy_tiers.py` reads the JSONL window and applies the named **profile** under `tiers` in [`tier_thresholds.yaml`](tier_thresholds.yaml) (`min_agreement_rate`, `max_high_risk_violations_in_window`, `window_cases`). Defaults: `--profile low_risk_staging_suggestions`, `--thresholds` pointing at this repo’s YAML.

```bash
# After appending shadow lines (or with a copy of the log)
python3 scripts/work_dev/evaluate_autonomy_tiers.py --log runtime/autonomy/shadow_decisions.jsonl

# Stricter operator drafting profile (larger window, higher agreement bar)
python3 scripts/work_dev/evaluate_autonomy_tiers.py --profile medium_risk_operator_drafting
```

Stdout is one of: `stay_shadow`, `limited_expand`, `insufficient_data`.

## Dashboard + warmup

- **work-dev dashboard** ([`scripts/work_dev/build_dashboard.py`](../../../../scripts/work_dev/build_dashboard.py)) includes an **Autonomy (GAP-007)** section: shadow JSONL line count and tier evaluation for the default profile.
- **`scripts/harness_warmup.py`** appends a one-line autonomy summary when `runtime/autonomy/shadow_decisions.jsonl` exists and is non-empty (same evaluation as the dashboard).
