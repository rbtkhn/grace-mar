# MCP capability audit report

- **Generated (UTC):** 2026-04-28T17:42:35Z
- **Git:** `e85922da`
- **Config:** `config\mcp-capabilities.yaml`
- **Schema:** `schemas\mcp-capability.v1.json`
- **Capabilities:** 11

## Summary

Planning-only registry classes — not live MCP wiring. Durable Record changes remain gated.

## Capability classes

| id | category | local/cloud | trust | network | creds | durable write | gate for Record | receipt | output lane |
|----|----------|-------------|-------|---------|-------|---------------|-----------------|---------|-------------|
| `coding_agent_patch_intake` | coding_agent | hybrid | high | read | optional | false | true | true | candidate_proposal |
| `database_readonly` | database | hybrid | high | read | optional | false | true | true | runtime_only |
| `evidence_stub_operator_template` | policy | local | medium | none | none | false | true | true | evidence_stub |
| `filesystem_readonly` | filesystem | local | medium | none | none | false | true | true | runtime_only |
| `github_patch_proposal` | scm | hybrid | high | full | required | false | true | true | candidate_proposal |
| `github_readonly` | scm | hybrid | medium | read | optional | false | true | true | runtime_only |
| `mcp_manifest_admission` | policy | local | operator_only | none | none | false | true | true | work_artifact |
| `mcp_mock_harness` | policy | local | operator_only | none | none | false | true | true | work_artifact |
| `memory_external_prohibited_by_default` | memory | cloud | low | none | none | false | true | true | prohibited |
| `shell_execution_prohibited` | policy | local | operator_only | none | none | false | true | true | prohibited |
| `web_research` | web | cloud | low | read | none | false | true | true | work_artifact |

## Danger flags

*None detected by heuristic rules (R1–R4).*

## Notes

Seed registry of illustrative MCP capability classes for Grace-Mar governance review.
