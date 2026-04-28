# MCP risk / permission scanner

**Status:** Planning-only governance tooling. This scanner **does not** execute MCP servers, call GitHub, open network connections, or mutate canonical Record files.

---

## Why this scanner exists

[`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml) lists **hypothetical** MCP integration classes. Admitting a capability into that registry is **not neutral**: each row implies permission posture (network, credentials, writes). Before treating a row as acceptable policy text, Grace-Mar needs **numeric risk scoring**, **tier classification**, **hard blocker** detection, and **recommendations** aligned with [`config/mcp-risk-policy.yaml`](../../config/mcp-risk-policy.yaml).

---

## How this differs from other MCP scripts

| Tool | Purpose |
|------|---------|
| [`scripts/mcp_capability_audit.py`](../../scripts/mcp_capability_audit.py) | Validates registry YAML against [`schemas/mcp-capability.v1.json`](../../schemas/mcp-capability.v1.json); emits heuristic **danger flags** (R1–R4). |
| [`scripts/mcp_authority_check.py`](../../scripts/mcp_authority_check.py) | Cross-checks [`config/mcp-authority-bindings.yaml`](../../config/mcp-authority-bindings.yaml) ↔ capability **output_lane** ↔ [`config/authority-map.json`](../../config/authority-map.json). |
| **`scripts/mcp_risk_scan.py`** (this PR) | Computes **risk scores**, **LOW/MEDIUM/HIGH/CRITICAL** tiers, **recommendations**, and **hard blocker tokens** from explicit policy weights — admission posture, not schema shape alone. |

---

## Risk scoring model

Weights and thresholds live in [`config/mcp-risk-policy.yaml`](../../config/mcp-risk-policy.yaml). Signals include credential requirement, full network access, non-empty writes, durable state writes, cloud/hybrid posture, shell/merge patterns in **allowed** surfaces, canonical-path fragments in **writes**, missing receipts/gates, and incomplete GitHub prohibitions on SCM rows.

Scores map to tiers (**LOW** 0–3, **MEDIUM** 4–7, **HIGH** 8–12, **CRITICAL** 13+) and to recommendation strings (`allow_with_receipt`, …).

---

## Hard blockers

Hard blockers are semantic tokens (see policy file). Examples: **`shell_execute`** when shell-like execution appears in **allowed_actions** / **writes**, **`write_without_receipt`** when `writes` is non-empty and `requires_receipt` is false, **`durable_state_write_without_gate`** when `durable_state_write` is true but `gate_required_for_record_change` is false, canonical Record path hints in **writes**, or **`external_memory_write_without_review`** for memory-category upsert surfaces without matching prohibitions.

The scanner exits **nonzero** if **any admission-eligible capability** (not **`PROHIBITED_BY_POLICY`**) carries a hard blocker.

---

## Intentionally prohibited capabilities

Registry rows such as **`shell_execution_prohibited`** and **`memory_external_prohibited_by_default`** use **`output_lane: prohibited`** and declare danger under **`prohibited_actions`** only. These are classified as **`PROHIBITED_BY_POLICY`**: permissive hard blockers are suppressed so the scan **does not fail** merely because the row names a dangerous class. Contradictions still fail (e.g. merge verbs in **`allowed_actions`** on a prohibited lane).

---

## Outputs

- **Markdown:** [`artifacts/mcp-risk-report.md`](../../artifacts/mcp-risk-report.md) — timestamp, summary, per-capability findings.
- **JSON (optional):** `python scripts/mcp_risk_scan.py --json` writes [`artifacts/mcp-risk-report.json`](../../artifacts/mcp-risk-report.json).

---

## Usage (before any live MCP integration)

```bash
python3 scripts/mcp_risk_scan.py
python3 scripts/mcp_risk_scan.py --json
```

Passing this scan **does not** authorize live MCP wiring — it only says the **registry policy text** clears structured blocker rules. **Runtime vs Record** separation remains per [`AGENTS.md`](../../AGENTS.md): durable Record change stays gated.
