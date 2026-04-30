# work-dev integration status

Current-state table for the Grace-Mar ↔ OpenClaw integration.

**Machine-readable:** [control-plane/integration_status.yaml](control-plane/integration_status.yaml) — generated copy: [generated/integration-status.generated.md](generated/integration-status.generated.md).

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
| **OpenClaw-specific provenance preserved into staged candidate metadata** | `implemented` | `integrations/openclaw_stage.py`, `scripts/handback_server.py`, `bot/core.py`, `users/grace-mar/recursion-gate.md` | When `source=openclaw_stage`, server passes staging_meta; _stage_candidate writes candidate_source, artifact_path, artifact_sha256, constitution_check_status, constitution_rule_ids into the candidate YAML block. |
| **OpenClaw-specific source tracking for gate review / benchmarks** | `implemented` | `scripts/recursion_gate_review.py`, `pipeline-events.jsonl` | parse_review_candidates extracts candidate_source, artifact_*, constitution_* from gate; dashboards and benchmarks can filter by openclaw. |
| **Session continuity startup checklist** | `implemented` | `docs/openclaw-integration.md`, `docs/skill-work/work-dev/README.md` | Checklist plus optional proof-of-read script. |
| **Session continuity read verification** | `implemented` | `scripts/continuity_read_log.py`, `scripts/continuity_preflight.py`, `scripts/verify_continuity_receipt.py`, `scripts/require_continuity_for_handback.py`, `scripts/handback_server.py`, `users/[id]/continuity-log.jsonl`, `tests/test_continuity_read_log.py`, `tests/test_continuity_receipts.py`, `tests/test_handback_requires_continuity.py` | **Preflight receipts:** `continuity_preflight.py` hashes `session-log.md`, `recursion-gate.md`, `self-evidence.md` into `runtime/continuity/receipts/*.json` (local, gitignored). **`/stage` (OpenClaw):** `handback_server` returns **428** without a valid receipt (default TTL 12h). **JSONL append:** still operator-side for `continuity_read_log.py` without `--dry-run`. |
| **Warmup launcher portability for operator continuity** | `implemented` | `scripts/operator_coffee.py`, `scripts/operator_daily_warmup.py`, `scripts/harness_warmup.py`, `scripts/operator_handoff_check.py` | Uses the active interpreter plus UTF-8 stdio so the coffee stack runs cleanly on Windows without shell-side encoding overrides. |
| **Compute-ledger cost instrumentation for export/handback** | `partial` | `economic-benchmarks.md`, `scripts/emit_compute_ledger.py`, `integrations/openclaw_hook.py`, `integrations/openclaw_stage.py`, `scripts/export_runtime_bundle.py`, `scripts/handback_server.py` | Integration paths append ledger rows (`bucket: integration`, `operation`, `wall_ms`, `bytes_processed`). Optional token fields when the host sets `GRACE_MAR_INTEGRATION_PROMPT_TOKENS`, `GRACE_MAR_INTEGRATION_COMPLETION_TOKENS`, `GRACE_MAR_INTEGRATION_TOTAL_TOKENS`, `GRACE_MAR_INTEGRATION_MODEL`. |
| **Local-local topology guidance** | `implemented` | `docs/openclaw-integration.md`, research notes | Preferred topology is clearly documented. |
| **VPS caveat handling** | `documented_only` | `docs/openclaw-integration.md`, research notes | Risks are documented, but there is no additional technical enforcement for remote handback paths. |

---

## Reading rule

If a row is not `implemented`, do not treat it as an operational guarantee.
