# MCP governance runbook

**Purpose:** Run the **governed MCP toolchain** in a safe order using **committed examples only** — **no live MCP servers**, **no credentials**, **no network**, **no shell beyond `python` invoking repo scripts**. Canonical Record files under **`users/grace-mar/`** are not written by these steps.

**Automation:** From repo root:

```bash
python3 scripts/run_mcp_governance_checks.py
```

Writes an aggregated report to **`artifacts/mcp-governance-demo-report.md`**, audit outputs under **`artifacts/mcp-governance-demo/`**, and adapter packets under each script’s required bucket using **`governance-demo-*`** filenames (see table below).

**Related:** **[`mcp-stack-overview.md`](mcp-stack-overview.md)**, **[`governed-mcp-layer.md`](governed-mcp-layer.md)**.

---

## Why isolate outputs under `artifacts/mcp-governance-demo/`

Scripts such as [`scripts/mcp_capability_audit.py`](../../scripts/mcp_capability_audit.py) default to workspace paths like **`artifacts/mcp-capability-report.md`**. For exploratory or CI demo runs, direct **`--output` / `--markdown` / `--json`** overrides avoid overwriting long-lived derived reports. The orchestrator **`run_mcp_governance_checks.py`** uses the demo prefix consistently.

---

## Recommended sequence (manual)

Use **`python3`** or **`python`** as appropriate on your OS. Commands assume repository root as current working directory.

### 1. Capability audit

```bash
python3 scripts/mcp_capability_audit.py \
  -o artifacts/mcp-governance-demo/capability-report.md
```

Optional **`--strict`** fails if heuristic danger flags fire after validation.

### 2. Authority binding check

```bash
python3 scripts/mcp_authority_check.py \
  -o artifacts/mcp-governance-demo/authority-report.md
```

Optional **`--strict`** treats warnings as failure (non-default).

### 3. Risk scan

```bash
python3 scripts/mcp_risk_scan.py \
  --markdown artifacts/mcp-governance-demo/risk-report.md \
  --json artifacts/mcp-governance-demo/risk-report.json
```

Exit code **`1`** when the scan reports **`pass=false`** — treat as failure for governance gates.

| Adapter / tool | Demo output path |
|----------------|------------------|
| Manifest admission | **`artifacts/mcp-admission/governance-demo-manifest.md`** |
| Mock harness | **`artifacts/mcp-mock-runs/governance-demo-mock.md`** |
| Local read | **`artifacts/mcp-local-read/governance-demo-read.md`** |
| Local index | **`artifacts/mcp-local-index/governance-demo-index.md`** |
| Research stub | **`artifacts/evidence-stubs/governance-demo-stub.md`** |
| Patch intake | **`artifacts/patch-intake/governance-demo-intake.md`** |

### 4. Manifest admission (example)

```bash
python3 scripts/mcp_manifest_admission.py \
  --input examples/mcp-server-manifest.example.yaml \
  --output artifacts/mcp-admission/governance-demo-manifest.md
```

### 5. Mock execution harness (example)

Uses **shell-blocked** fixture (aligns with “no shell execution” messaging):

```bash
python3 scripts/mcp_mock_harness.py \
  --input examples/mcp-mock-run.shell-blocked.example.json \
  --output artifacts/mcp-mock-runs/governance-demo-mock.md
```

### 6. Local read-only adapter (example)

```bash
python3 scripts/mcp_local_readonly.py \
  --input examples/mcp-local-read-request.example.json \
  --output artifacts/mcp-local-read/governance-demo-read.md
```

### 7. Local directory index adapter (example)

```bash
python3 scripts/mcp_local_index.py \
  --input examples/mcp-local-index-request.example.json \
  --output artifacts/mcp-local-index/governance-demo-index.md
```

### 8. Optional — research → evidence stub (example)

If [`examples/research-evidence-input.example.json`](../../examples/research-evidence-input.example.json) exists:

```bash
python3 scripts/research_to_evidence_stub.py \
  --input examples/research-evidence-input.example.json \
  --output artifacts/evidence-stubs/governance-demo-stub.md
```

### 9. Optional — coding-agent patch intake (example)

If [`examples/coding-agent-patch-intake.example.json`](../../examples/coding-agent-patch-intake.example.json) exists:

```bash
python3 scripts/coding_agent_patch_intake.py \
  --input examples/coding-agent-patch-intake.example.json \
  --output artifacts/patch-intake/governance-demo-intake.md
```

---

## Receipts

Adapters and harness steps emit JSON under **`artifacts/mcp-receipts/`**. The orchestrator aggregates paths into **`artifacts/mcp-governance-demo-report.md`**. Receipts **do not** approve Record merges or live MCP integration.

---

## Boundaries (all steps)

- **No live MCP server execution** — subprocesses invoke **Python scripts** only.
- **No credentials** and **no network** — tooling is local repo config + filesystem under policy.
- **No canonical Record mutation** — adapters do not merge gate candidates or edit **`users/grace-mar/`** identity surfaces by design (see per-adapter docs).

Passing this runbook **does not** authorize arbitrary MCP integration; live MCP remains a **separate** operator decision.
