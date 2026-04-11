# work-dev — capability registry

**Purpose:** Map **integration ids** (used in gaps and JSON) to surfaces and proof.

| ID | Surface | Status source | Notes |
|----|---------|---------------|-------|
| `openclaw_stage` | Staging / gate | [openclaw-integration.md](openclaw-integration.md) | Handback path |
| `continuity_read` | Session continuity | [continuity-log.jsonl](continuity-log.jsonl) | Proof-of-read |
| `sandbox_adapter` | Sandboxed execution | [sandbox-adapter spec](sandbox-adapter.md) | Governance at boundary |

Add rows as integrations harden. **Ids** use lowercase snake_case to match [schemas/work_dev/integration_status.schema.json](../../schemas/work_dev/integration_status.schema.json).
