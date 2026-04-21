# Worker candidates (future — documentation only)

Grace-Mar **does not** ship a shared worker registry or routed worker framework in-repo today. This note lists **behaviors that often correlate with workflow-depth escalation** or repeated operator passes — candidates to revisit **if** a future design introduces explicit background workers.

**Non-goals here:** no router, no daemon, no automatic merge or gate side effects.

## Candidate patterns

| Pattern | Why a worker might help later | Today |
|---------|----------------------------------|--------|
| Contradiction-heavy escalation | Many `contradiction_refs` or repeated `auto` escalation to medium | Operator runs review orchestrator + budgeted context manually |
| Provenance-heavy escalation | Thin `source_refs`, envelope pressure | Manual evidence pass; abstention policy |
| Research-cockpit escalation | Broad lane search + deep packs | Manual `build_budgeted_context.py` with `deep` / `exhaustive` |
| Handoff-build escalation | Checkpoint / handoff includes included in pack | Manual includes via CLI |

## Relation to workflow depth

Depth receipts (`runtime/workflow-depth/index.jsonl`) and audit reports (`scripts/build_workflow_depth_report.py`) help operators see **where** these patterns concentrate — they do **not** enqueue work.

## See also

- [workflow-depth-contract.md](workflow-depth-contract.md)
- [workflow-depth-implementation-note.md](workflow-depth-implementation-note.md)
