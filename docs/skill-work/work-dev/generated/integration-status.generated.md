<!-- GENERATED FILE — do not edit by hand. Source: docs/skill-work/work-dev/control-plane/*.yaml — run: python scripts/work_dev/render_control_plane_docs.py -->

# Integration status (generated)
Status vocabulary: `implemented`, `partial`, `documented_only`, `needs_verification`, `blocked`.

| id | title | surface | status |
|---|---|---|---|
| `compute_ledger_export_handback` | Compute-ledger cost instrumentation for export/handback | observability | `partial` |
| `constitution_advisory_events` | Constitution advisory event emission | handback | `implemented` |
| `identity_export_openclaw_hook` | Identity export via openclaw_hook.py | export | `implemented` |
| `local_local_topology` | Local-local topology guidance | ops | `implemented` |
| `openclaw_gate_review_tracking` | OpenClaw source tracking for gate review | gate | `implemented` |
| `openclaw_provenance_metadata` | OpenClaw provenance in staged candidate metadata | gate | `implemented` |
| `pipeline_export_audit` | Pipeline-level export audit (runtime_compat_export) | export | `implemented` |
| `runtime_bundle_export` | Runtime bundle export for OpenClaw consumption | export | `implemented` |
| `session_continuity_checklist` | Session continuity startup checklist | runtime_continuity | `implemented` |
| `session_continuity_event_logging` | Session continuity block / event logging (observability feed) | runtime_continuity | `partial` |
| `session_continuity_read_log` | Session continuity read log (operator) | runtime_continuity | `implemented` |
| `session_continuity_receipts` | Session continuity receipt enforcement (handback) | runtime_continuity | `implemented` |
| `stage_only_handback` | Stage-only handback via openclaw_stage.py | handback | `implemented` |
| `vps_caveat` | VPS caveat handling | ops | `documented_only` |

## Details

### `compute_ledger_export_handback`

- **Status:** `partial`
- **Source of truth:** `docs/skill-work/work-dev/economic-benchmarks.md`, `scripts/emit_compute_ledger.py`, `integrations/openclaw_hook.py`, `integrations/openclaw_stage.py`, `scripts/export_runtime_bundle.py`, `scripts/handback_server.py`
- Integration paths append ledger rows (operation, runtime, wall_ms, bytes_processed). Optional token fields via GRACE_MAR_INTEGRATION_PROMPT_TOKENS, GRACE_MAR_INTEGRATION_COMPLETION_TOKENS, GRACE_MAR_INTEGRATION_TOTAL_TOKENS, GRACE_MAR_INTEGRATION_MODEL.

### `constitution_advisory_events`

- **Status:** `implemented`
- **Source of truth:** `integrations/openclaw_stage.py`
- intent_constitutional_critique events before staging.

### `identity_export_openclaw_hook`

- **Status:** `implemented`
- **Source of truth:** `integrations/openclaw_hook.py`, `docs/openclaw-integration.md`
- Export path exists and emits runtime compatibility audit events.

### `local_local_topology`

- **Status:** `implemented`
- **Source of truth:** `docs/openclaw-integration.md`
- Preferred topology documented.

### `openclaw_gate_review_tracking`

- **Status:** `implemented`
- **Source of truth:** `scripts/recursion_gate_review.py`
- parse_review_candidates extracts OpenClaw fields.

### `openclaw_provenance_metadata`

- **Status:** `implemented`
- **Source of truth:** `integrations/openclaw_stage.py`, `scripts/handback_server.py`, `bot/core.py`
- candidate_source, artifact_*, constitution_* in gate YAML.

### `pipeline_export_audit`

- **Status:** `implemented`
- **Source of truth:** `integrations/openclaw_hook.py`
- Aligns with portable runtime contract naming.

### `runtime_bundle_export`

- **Status:** `implemented`
- **Source of truth:** `integrations/openclaw_hook.py`, `scripts/export_runtime_bundle.py`
- OpenClaw consumes the generic runtime bundle contract.

### `session_continuity_checklist`

- **Status:** `implemented`
- **Source of truth:** `docs/openclaw-integration.md`, `docs/skill-work/work-dev/README.md`
- Human checklist before OpenClaw work.

### `session_continuity_event_logging`

- **Status:** `partial`
- **Source of truth:** `runtime/observability/continuity_blocks.jsonl`, `scripts/require_continuity_for_handback.py`, `tests/test_handback_requires_continuity.py`
- Structured block events append when handback denies /stage; feed is local/gitignored unless exported.

### `session_continuity_read_log`

- **Status:** `implemented`
- **Source of truth:** `scripts/continuity_read_log.py`, `scripts/openclaw_session_continuity.sh`, `tests/test_continuity_read_log.py`
- Human-readable read log; separate from receipt enforcement. Optional shell wrapper appends JSONL then execs the rest of the command.

### `session_continuity_receipts`

- **Status:** `implemented`
- **Source of truth:** `scripts/continuity_preflight.py`, `scripts/verify_continuity_receipt.py`, `scripts/require_continuity_for_handback.py`, `scripts/handback_server.py`, `tests/test_continuity_receipts.py`, `tests/test_handback_requires_continuity.py`
- Fresh valid receipt required for OpenClaw /stage (428 without valid receipt).

### `stage_only_handback`

- **Status:** `implemented`
- **Source of truth:** `integrations/openclaw_stage.py`, `scripts/handback_server.py`
- Merge authority stays human-gated.

### `vps_caveat`

- **Status:** `documented_only`
- **Source of truth:** `docs/openclaw-integration.md`
- Risks documented; limited technical enforcement for remote handback.

