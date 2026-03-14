# work-build-ai integration status

Current-state table for the Grace-Mar ↔ OpenClaw integration.

Status vocabulary:

- `implemented`
- `partial`
- `documented_only`
- `needs_verification`
- `blocked`

---

## Status table

| Surface | Status | Source of truth | Notes |
|--------|--------|-----------------|-------|
| **Identity export via `openclaw_hook.py`** | `implemented` | `integrations/openclaw_hook.py`, `docs/openclaw-integration.md` | Export path exists and emits runtime compatibility audit events. |
| **Runtime bundle export for OpenClaw consumption** | `implemented` | `integrations/openclaw_hook.py`, `scripts/export_runtime_bundle.py` | OpenClaw is now a consumer of the generic runtime bundle contract. |
| **Pipeline-level export audit (`runtime_compat_export`)** | `implemented` | `integrations/openclaw_hook.py`, `pipeline-events.jsonl`, harness events | Export audit naming is aligned with the portable runtime contract. |
| **Stage-only handback via `openclaw_stage.py`** | `implemented` | `integrations/openclaw_stage.py`, `scripts/handback_server.py` | OpenClaw can stage through `/stage`; merge authority stays human-gated. |
| **Constitution advisory event emission** | `implemented` | `integrations/openclaw_stage.py`, `pipeline-events.jsonl` | `intent_constitutional_critique` events are emitted before staging. |
| **OpenClaw-specific provenance preserved into staged candidate metadata** | `partial` | `integrations/openclaw_stage.py`, `scripts/handback_server.py`, `users/grace-mar/recursion-gate.md` | Sender emits metadata, but the handback server does not preserve most of it into the candidate block. |
| **OpenClaw-specific source tracking for gate review / benchmarks** | `partial` | `scripts/recursion_gate_review.py`, `pipeline-events.jsonl` | Event-level hints exist, but candidate-level provenance is not yet reliable. |
| **Session continuity startup checklist** | `documented_only` | `docs/openclaw-integration.md`, `docs/skill-work/work-build-ai/README.md` | Strong prose and checklist guidance exist, but no repo-local enforcement or proof-of-read hook. |
| **Session continuity read verification** | `blocked` | none yet | No local OpenClaw runtime hook or log proves that the recommended files were actually read. |
| **Compute-ledger cost instrumentation for export/handback** | `documented_only` | `economic-benchmarks.md` | Benchmarks expect it, but the integration scripts do not emit compute-ledger entries. |
| **Local-local topology guidance** | `implemented` | `docs/openclaw-integration.md`, research notes | Preferred topology is clearly documented. |
| **VPS caveat handling** | `documented_only` | `docs/openclaw-integration.md`, research notes | Risks are documented, but there is no additional technical enforcement for remote handback paths. |

---

## Reading rule

If a row is not `implemented`, do not treat it as an operational guarantee.
