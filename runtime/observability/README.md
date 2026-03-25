# Runtime observability feeds (local / operator)

JSONL files in this directory are **gitignored**; they accumulate on the machine where tools run.

| File | Producer | Consumer |
|------|----------|----------|
| `lane_scope.jsonl` | `scripts/check_lane_scope.py` when `--append-observability` or `GRACE_MAR_LOG_LANE_VIOLATIONS=1` | `scripts/work_dev/build_dashboard.py` |
| `continuity_blocks.jsonl` | `append_continuity_block_event` from handback continuity gate | `build_dashboard.py` |

CI jobs may append lane violations during the lane-scope workflow; those are ephemeral unless uploaded as artifacts.
