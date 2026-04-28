# MCP risk / permission scan report

- **Generated (UTC):** 2026-04-28T15:50:42Z
- **Git:** `230fd78e`
- **Capabilities:** `config\mcp-capabilities.yaml`
- **Policy:** `config\mcp-risk-policy.yaml`

## Summary

| Metric | Value |
|--------|-------|
| **Pass (no hard blockers on admission-eligible capabilities)** | `true` |
| **Capabilities checked** | 9 |
| **Tier: low** | 7 |
| **Tier: medium** | 1 |
| **Tier: high** | 1 |
| **Tier: critical** | 0 |

| **Hard blocker hits (non-prohibition stance)** | 0 |

## Final status

**PASS** — no hard blockers on admission-eligible capabilities.

## Capability findings

### `coding_agent_patch_intake`

- **Score:** 4
- **Risk level:** `medium`
- **Recommendation:** `allow_with_restrictions`
- **PROHIBITED_BY_POLICY stance:** `false`
- **Hard blockers:** _none_
- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.

### `database_readonly`

- **Score:** 1
- **Risk level:** `low`
- **Recommendation:** `allow_with_receipt`
- **PROHIBITED_BY_POLICY stance:** `false`
- **Hard blockers:** _none_
- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.

### `evidence_stub_operator_template`

- **Score:** 3
- **Risk level:** `low`
- **Recommendation:** `allow_with_receipt`
- **PROHIBITED_BY_POLICY stance:** `false`
- **Hard blockers:** _none_
- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.

### `filesystem_readonly`

- **Score:** 0
- **Risk level:** `low`
- **Recommendation:** `allow_with_receipt`
- **PROHIBITED_BY_POLICY stance:** `false`
- **Hard blockers:** _none_
- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.

### `github_patch_proposal`

- **Score:** 10
- **Risk level:** `high`
- **Recommendation:** `restrict_and_require_human_review`
- **PROHIBITED_BY_POLICY stance:** `false`
- **Hard blockers:** _none_
- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.

### `github_readonly`

- **Score:** 1
- **Risk level:** `low`
- **Recommendation:** `allow_with_receipt`
- **PROHIBITED_BY_POLICY stance:** `false`
- **Hard blockers:** _none_
- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.

### `memory_external_prohibited_by_default`

- **Score:** 2
- **Risk level:** `low`
- **Recommendation:** `allow_with_receipt`
- **PROHIBITED_BY_POLICY stance:** `true`
- **Hard blockers:** _none_
- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.

### `shell_execution_prohibited`

- **Score:** 0
- **Risk level:** `low`
- **Recommendation:** `allow_with_receipt`
- **PROHIBITED_BY_POLICY stance:** `true`
- **Hard blockers:** _none_
- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.

### `web_research`

- **Score:** 2
- **Risk level:** `low`
- **Recommendation:** `allow_with_receipt`
- **PROHIBITED_BY_POLICY stance:** `false`
- **Hard blockers:** _none_
- **Required controls:** operator review; receipts + gate discipline per AGENTS.md.

## Notes

This scanner evaluates **permission posture**, not factual truth of MCP claims. Passing does **not** approve live MCP integration.
