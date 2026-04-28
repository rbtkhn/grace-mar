# MCP authority bindings

**Status:** Planning and policy only. This document describes how MCP **`output_lane`** values join **`config/authority-map.json`** — not live MCP wiring.

**Related:** [Governed MCP layer](governed-mcp-layer.md), [`config/mcp-authority-bindings.yaml`](../../config/mcp-authority-bindings.yaml), schema [`schemas/mcp-authority-bindings.v1.json`](../../schemas/mcp-authority-bindings.v1.json), checker [`scripts/mcp_authority_check.py`](../../scripts/mcp_authority_check.py).

---

## Why bindings exist

The capability registry assigns each integration class an **`output_lane`** (`runtime_only`, `work_artifact`, `evidence_stub`, `candidate_proposal`, **`prohibited`**). Without a join table, “lane” vocabulary could widen silently relative to Grace-Mar’s authority surfaces. **`mcp-authority-bindings.yaml`** fixes each lane to one **`authority_surface`** (a key in **`authority-map.json` → `surfaces`**) and the **`authority_class`** recorded there (`read_only`, `draftable`, `review_required`, `human_only`, `ephemeral_only`), plus optional allowed/prohibited output tokens and **`gate_required_for_record_change`**.

The checker **`mcp_authority_check.py`** validates YAML against the bindings schema, reconciles classes with **`authority-map.json`**, and applies capability rules (writes vs ephemeral lanes, durable writes vs gate, GitHub prohibited-action tokens, shell posture, external-memory id).

---

## Lane → surface mapping (committed defaults)

| output_lane | authority_surface (example) | authority_class | Role |
|-------------|-----------------------------|-----------------|------|
| `runtime_only` | `bridge_packets` | `ephemeral_only` | Session-scoped transit; not canonical Record. |
| `work_artifact` | `prepared_context` | `draftable` | WORK Markdown / operator-visible drafts. |
| `evidence_stub` | `evidence` | `draftable` | Pre-canonical evidence-shaped stubs under governed paths. |
| `candidate_proposal` | `governed_state` | `review_required` | Staged proposals for companion review / gate. |
| `prohibited` | `safety` | `human_only` | Policy-decline lane (e.g. shell or external memory denied). |

**`runtime_only` and `read_only`:** The authority-map schema allows **`read_only`**, but surfaces must exist as keys. **`mcp_operator_scratch`** → **`read_only`** was added so **`runtime_only`** may bind to **`ephemeral_only`** (e.g. **`bridge_packets`**) or, when documented, **`read_only`** scratch — without inventing silent widenings.

---

## Checker rules (summary)

- Every distinct **`output_lane`** used in **`mcp-capabilities.yaml`** appears exactly once in **`bindings`** (no duplicates; no missing lane).
- **`authority_surface`** exists under **`authority-map.json`** `surfaces`; **`authority_class`** matches unless **`authority_class_override`** is true with **`override_reason`**.
- Write-capable capabilities require **`requires_receipt: true`** and must not bind to **`ephemeral_only`** lanes.
- **`candidate_proposal`** binds to **`review_required`** (typically **`governed_state`**).
- **`runtime_only`** binds to **`ephemeral_only`** or **`read_only`**.
- **`durable_state_write: true`** implies **`gate_required_for_record_change`** and class **`review_required`** or **`human_only`**.
- Shell execution must stay prohibited for governed MCP (aligned with **`mcp_capability_audit.py`** heuristics).
- **`memory_external_prohibited_by_default`** must keep **`writes`** empty.
- **`github_readonly`** / **`github_patch_proposal`** must list **`merge_to_main`**, **`force_push`**, and **`bypass_review`** in **`prohibited_actions`** (substring match, case-insensitive).

Report output: **`artifacts/mcp-authority-report.md`**. Exit **1** on violations; **`--strict`** also fails on warnings (e.g. bindings unused by any capability).

---

## Edits

1. Update **`config/mcp-authority-bindings.yaml`** (and **`authority-map.json`** if adding surfaces).
2. Run **`python3 scripts/mcp_authority_check.py`** (and **`mcp_capability_audit.py`** after capability edits).
3. Commit regenerated **`artifacts/mcp-authority-report.md`** when checks pass.
