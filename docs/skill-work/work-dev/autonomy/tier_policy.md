# Autonomy tier policy (BUILD-AI-GAP-007)

Shadow mode compares **proposed agent action** vs **human action** on the same task class.

- **stay_shadow** — default until evidence meets thresholds in `tier_thresholds.yaml`.
- **limited_expand** — narrow tool scope with continued logging.
- **promote** — not used for merge authority; Record merge stays human-gated.

Log lines go to `runtime/autonomy/shadow_decisions.jsonl` (local, gitignored) via `scripts/work_dev/log_shadow_decision.py`.
