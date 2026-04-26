# Agent prompt: Compound refresh (Grace-Mar work-dev)

**Boundary:** Do not mutate canonical Record surfaces. This pass is **read/analyze** on existing compound notes; output is a **report** the operator can delete or regenerate.

**Boundary:** Do not “promote” items by writing to Record. Flag **stale / duplicate / gate-worthy** patterns in prose or point to `python3 scripts/work_dev_compound_refresh.py` output.

## Your job

1. **Read** (do not delete) `docs/skill-work/work-dev/compound-notes/*.md` and parse front matter.
2. **Classify:** stale notes, duplicate themes, `problem_type` clusters, notes that might deserve `gate_candidate: true` (recommendation only).
3. **Optional:** run or mirror `python3 scripts/work_dev_compound_refresh.py` and use `artifacts/work-dev-compound-refresh.md` as the canonical aggregate.
4. **Output:** a short markdown report: summary counts, top recurring types, “consider archiving” list, and **governance** reminder that nothing here merges automatically.

## References

- [compound-loop.md](../compound-loop.md)
- [work_dev_compound_refresh.py](../../../../scripts/work_dev_compound_refresh.py)
