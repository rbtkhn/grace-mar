# MCP stack overview (Grace-Mar)

**Status:** Describes the **governed MCP substrate** in this repository — planning, policy, receipts, and offline adapters. **No live MCP server execution** is implied by these components; live integration remains a separate operator decision. Hub document: **[`governed-mcp-layer.md`](governed-mcp-layer.md)**.

---

## Purpose

Grace-Mar separates **tool-shaped capabilities** (registry classes, lanes, receipts) from **canonical Record authority** (`users/*/`, gate, merge scripts). The pieces below form a **consistent governance stack**: declare posture in YAML, bind lanes to authority surfaces, audit and risk-scan before admission, and emit **execution receipts** for offline/work artifacts — including adapters that perform **bounded local filesystem** operations under explicit allowlists.

---

## Layers (summary table)

| Layer | Purpose | Primary script(s) | Primary artifact(s) | Boundary |
|-------|---------|-------------------|----------------------|----------|
| **Capability registry** | Enumerate MCP-shaped capability classes; IDs, categories, network/credential posture. | [`scripts/mcp_capability_audit.py`](../../scripts/mcp_capability_audit.py) (audit) | [`artifacts/mcp-capability-report.md`](../../artifacts/mcp-capability-report.md) (default output) | Registry **does not** execute MCP; audit is read-only YAML + Markdown. |
| **Authority bindings** | Map each capability `output_lane` → `authority_surface` / [`authority-map.json`](../../config/authority-map.json). | [`scripts/mcp_authority_check.py`](../../scripts/mcp_authority_check.py) | [`artifacts/mcp-authority-report.md`](../../artifacts/mcp-authority-report.md) (default) | Cross-check only; **no** Record writes. |
| **Execution receipts** | Structured audit records (`capability.id`, access, governance flags). | [`scripts/mcp_receipt.py`](../../scripts/mcp_receipt.py); validators in [`scripts/mcp_receipt_lib.py`](../../scripts/mcp_receipt_lib.py); optional [`scripts/mcp_receipt_audit.py`](../../scripts/mcp_receipt_audit.py) over `artifacts/mcp-receipts/` | [`schemas/mcp-execution-receipt.v1.json`](../../schemas/mcp-execution-receipt.v1.json); JSON under **`artifacts/mcp-receipts/`** | Receipts are **WORK/runtime** metadata; **not** merge approval. |
| **Risk scanner** | Score registry capabilities vs [`config/mcp-risk-policy.yaml`](../../config/mcp-risk-policy.yaml). | [`scripts/mcp_risk_scan.py`](../../scripts/mcp_risk_scan.py) | [`artifacts/mcp-risk-report.md`](../../artifacts/mcp-risk-report.md); optional JSON | Read-only policy evaluation; exit non-zero when scan does not pass configured gates. |
| **Manifest admission** | Classify declared MCP manifests **without** launching servers. | [`scripts/mcp_manifest_admission.py`](../../scripts/mcp_manifest_admission.py) | Markdown under **`artifacts/mcp-admission/`** + receipt | Planning/admission only. |
| **Mock execution** | Exercise harness/receipt chain from fixture JSON (no MCP stdio). | [`scripts/mcp_mock_harness.py`](../../scripts/mcp_mock_harness.py) | Markdown under **`artifacts/mcp-mock-runs/`** + receipt | Fixture-only; capability **`mcp_mock_harness`**. |
| **Research → evidence stubs** | Structured research JSON → pre-canonical stub + receipt. | [`scripts/research_to_evidence_stub.py`](../../scripts/research_to_evidence_stub.py) | **`artifacts/evidence-stubs/`** + receipt | **Not** canonical evidence until gate pipeline. |
| **Coding-agent patch intake** | Intake JSON → patch-review packet + receipt (no apply). | [`scripts/coding_agent_patch_intake.py`](../../scripts/coding_agent_patch_intake.py) | **`artifacts/patch-intake/`** + receipt | No merge; no Record edits. |
| **Local read-only file adapter** | Bounded UTF-8 read from allowlisted repo paths. | [`scripts/mcp_local_readonly.py`](../../scripts/mcp_local_readonly.py) | **`artifacts/mcp-local-read/`** + receipt | **`filesystem_readonly`**; no network/credentials/shell. |
| **Local directory index adapter** | Metadata-only directory listing under allowlist. | [`scripts/mcp_local_index.py`](../../scripts/mcp_local_index.py) | **`artifacts/mcp-local-index/`** + receipt | Same posture as file adapter; **no** file bodies in packet. |

---

## Configuration SSOT

| File | Role |
|------|------|
| [`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml) | Capability registry |
| [`config/mcp-authority-bindings.yaml`](../../config/mcp-authority-bindings.yaml) | Lane ↔ authority |
| [`config/authority-map.json`](../../config/authority-map.json) | Authority surfaces |
| [`config/mcp-risk-policy.yaml`](../../config/mcp-risk-policy.yaml) | Risk scanner policy |
| [`config/mcp-local-read-allowlist.yaml`](../../config/mcp-local-read-allowlist.yaml) | Local read/index allowlist |

---

## Related docs

- **[`agent-substrate.md`](../agent-substrate.md)** - broader architecture framing for Grace-Mar as a governed personal agent substrate.

- **[`mcp-governance-runbook.md`](mcp-governance-runbook.md)** — operator sequence and one-shot **`scripts/run_mcp_governance_checks.py`** demo.
- Per-topic docs linked from **[`governed-mcp-layer.md`](governed-mcp-layer.md)** (execution receipts, manifest admission, mock harness, local adapters, risk scanner).
