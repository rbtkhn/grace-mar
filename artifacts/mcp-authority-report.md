# MCP authority binding report

- **Generated (UTC):** 2026-04-28T14:45:00Z
- **Git:** `a318f05c`
- **Status:** **PASS**

## Summary

- Capabilities checked: **9**
- Bindings (lanes): **5**
- Violations: **0**
- Warnings: **0**

## Lane → authority

| output_lane | authority_surface | authority_class | gate_for_record_change |
|---------------|--------------------|-----------------|-------------------------|
| `candidate_proposal` | `governed_state` | review_required | True |
| `evidence_stub` | `evidence` | draftable | True |
| `prohibited` | `safety` | human_only | True |
| `runtime_only` | `bridge_packets` | ephemeral_only | False |
| `work_artifact` | `prepared_context` | draftable | True |

## Capabilities by lane

- **`candidate_proposal`:** `coding_agent_patch_intake`, `github_patch_proposal`
- **`evidence_stub`:** `evidence_stub_operator_template`
- **`prohibited`:** `memory_external_prohibited_by_default`, `shell_execution_prohibited`
- **`runtime_only`:** `database_readonly`, `filesystem_readonly`, `github_readonly`
- **`work_artifact`:** `web_research`

## Violations

_None._

## Warnings

_None._
