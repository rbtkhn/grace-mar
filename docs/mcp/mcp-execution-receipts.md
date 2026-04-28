# MCP execution receipts (governance)

**Status:** Policy contract only. **`scripts/mcp_receipt.py` does not run MCP servers** or touch canonical Record files (`users/*/self.md`, gate merges, etc.). Receipts are **WORK/runtime audit artifacts**.

---

## Why receipts exist

**Capability is not authority.** The capability registry ([`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml)) describes posture classes; **authority surfaces** come from bindings ([`config/mcp-authority-bindings.yaml`](../../config/mcp-authority-bindings.yaml)). **Tool success is not governance approval.**

An MCP execution receipt records **what happened**, **under which capability lane**, and **which authority class governed** the action, so assistants and operators can audit tool-shaped work **without** conflating it with companion-approved merges.

---

## Distinction from other receipts

| Artifact | Role |
|----------|------|
| **`schemas/mcp-execution-receipt.v1.json`** (this PR) | MCP **policy/governance** receipt — derives authority from bindings + capability registry. |
| **`schema-registry/execution-receipt.v1.json`** | Runtime **worker** receipt (`grace_mar_runtime_worker.py`) — different schema and semantics — **do not interchange.** |

---

## Receipt lifecycle (recommended)

1. Tool-shaped action completes (or is blocked).
2. Emit receipt JSON via **`scripts/mcp_receipt.py`** (validated against schema + rules).
3. Optionally **`scripts/mcp_receipt_audit.py`** over **`artifacts/mcp-receipts/*.json`** for drift checks against current YAML configs.

Promotion paths ([imports](../imports-and-capture.md)): receipts may inform **evidence stubs** or **gate staging**, always behind explicit human review — receipts alone never merge Record truth.

---

## Receipt vs evidence stub vs candidate vs canonical approval

| Stage | Meaning |
|-------|---------|
| **Receipt** | Audit envelope; declares posture and declared reads/writes; **not** canonical IX/Evid facts. |
| **Evidence stub** | Pre-canonical draft artifact (`artifacts/evidence-stubs/` conventions); still gated for merge into [`users/*/self-archive.md`](../../users/grace-mar/self-archive.md). |
| **Candidate proposal** | Structured YAML/text destined for [`recursion-gate.md`](../../users/grace-mar/recursion-gate.md) staging — companion/process-approved merge applies separately. |
| **Canonical approval** | Companion approval via **`scripts/process_approved_candidates.py`** — receipts never bypass this. |

---

## Schema essentials (`schemas/mcp-execution-receipt.v1.json`)

Root keys include **`actor`**, **`capability`** (`id`, `category`, `output_lane`), **`authority`** (derived from bindings — **`authority` must match bindings**, no CLI override in **`mcp_receipt.py`**), **`access`** (**`network_access`**, **`credential_use`** bounded by registry posture tier-order `none < read < full` and `none < optional < required`), **`governance`** booleans, and **`integrity.receipt_hash`** (optional SHA-256 over canonical JSON **with `integrity.receipt_hash` omitted** from preimage).

Full constraints enforced in **`scripts/mcp_receipt_lib.py`** (`validate_mcp_receipt`).

---

## `integrity.receipt_hash`

Computation hashes **`sha256(canonical_json(receipt_without_integrity_hash_field))`**, writes hex into **`integrity.receipt_hash`**. Canonical JSON uses **`sort_keys=True`** and compact separators.

---

## Representative capability narratives

These match seeded IDs in **`config/mcp-capabilities.yaml`**.

### `github_readonly`

Runtime SCM reads within **`runtime_only`** / **`bridge_packets`** (`ephemeral_only`). Typical **`declared_intent`**: inspect issues/diffs. **`credential_use`** bounded by registry (**often `optional`**). **`resources_written`** should usually stay empty.

### `web_research`

Fetch/summarize with citations (**`work_artifact`** / **`prepared_context`**, **`draftable`**). Receipt summarizes fetched excerpts as WORK artifact posture — **not** merged IX-A facts without gate.

### `evidence_stub_operator_template`

Emits evidence-shaped stubs under governed paths (**`evidence_stub`** → **`evidence`** surface). **`governance.requires_gate_review`** must be **`true`** on receipts (`mcp_receipt.py` defaults this when lane is **`evidence_stub`**).

### `github_patch_proposal`

Draft PR branch carriers (**`candidate_proposal`** → **`governed_state`**, **`review_required`**). **`requires_human_review`** must be **`true`** (CLI defaults when lane is **`candidate_proposal`**).

### `coding_agent_patch_intake`

WORK-tree patches feeding proposals (**`candidate_proposal`**). Receipt emphasizes **`writes`** vs **`requires_receipt`** registry stance — tooling drafts remain proposals until gate.

### `shell_execution_prohibited` / blocked action

Lane **`prohibited`** / **`safety`** (**`human_only`**). Prefer **`result.status`** **`blocked`** or **`failed`**, **`prohibited_action_attempted`** / notes explaining refusal — **`success`** conflicts with **`prohibited_action_attempted`** and **`status`** **`success`** on **`prohibited`** lane.

---

## Commands

```bash
python3 scripts/mcp_receipt.py \
  --capability-id github_readonly \
  --actor-kind assistant \
  --actor-name chatgpt \
  --intent "Inspect repo MCP policy files" \
  --resources-read config/mcp-capabilities.yaml config/mcp-authority-bindings.yaml \
  --status success \
  --summary "Confirmed MCP registry and authority bindings exist."

python3 scripts/mcp_receipt_audit.py
```

Output directories: **[`artifacts/mcp-receipts/`](../../artifacts/mcp-receipts/)**, report **[`artifacts/mcp-receipt-report.md`](../../artifacts/mcp-receipt-report.md)**.
