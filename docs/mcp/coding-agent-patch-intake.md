# Coding-agent patch intake (adapter)

**Status:** WORK/runtime tooling only. This script **does not** invoke Cursor, Claude Code, shell agents, live MCP servers, or GitHub; it **does not** apply patches or merge pull requests.

---

## Why this workbench exists

Coding assistants routinely emit summaries of edits (“files touched”, “tests run”). Those summaries are **not** governance artifacts by themselves. This adapter turns **structured intake JSON** into:

1. A **Markdown patch-review packet** under [`artifacts/patch-intake/`](../../artifacts/patch-intake/) — labeled **candidate proposal**, **not merged**, **not approved Record**.
2. An **MCP execution receipt** under [`artifacts/mcp-receipts/`](../../artifacts/mcp-receipts/) with capability **`coding_agent_patch_intake`** — receipts are audit metadata only ([`mcp-execution-receipts.md`](mcp-execution-receipts.md)).

That preserves visibility without handing agents implicit merge authority.

---

## Input format

- **JSON Schema:** [`schemas/coding-agent-patch-intake.v1.json`](../../schemas/coding-agent-patch-intake.v1.json)
- **Example:** [`examples/coding-agent-patch-intake.example.json`](../../examples/coding-agent-patch-intake.example.json)

Paths under **`files_touched`** must be **repo-relative** (POSIX-style logic): no absolute paths, no **`..`**, no obvious secret paths (`.env`, `secrets/`, common key filenames).

Substring scans reject narratives implying **canonical approval**, **approved Record updates**, or **direct merges outside review**.

---

## Output format

- **Markdown packet** with YAML front matter (`mcp_receipt_id`, `intake_status`, etc.) and a banner line:  
  **`CANDIDATE PROPOSAL · WORK ARTIFACT · NOT MERGED · NOT APPROVED RECORD`**
- **Risk classification** per touched path (`CRITICAL` … `LOW`): canonical **`users/grace-mar/`** Record gates, secrets/env material (blocked posture), MCP/config hotspots (**HIGH**), common tooling dirs (**MEDIUM**), docs/readme-style (**LOW**). **`HIGH` surfaces alone do not fail intake** — they raise classification visibility.

When **`files_touched`** lists any **`CRITICAL`** path (including canonical Record paths), the receipt **`result.status`** is **`blocked`**, **`intake_status`** is **`blocked`**, and the packet includes a **BLOCKED — DO NOT MERGE AS-IS** recommendation. **`governance.canonical_record_touched`** is **`true`** only when canonical **`users/grace-mar`** Record-shaped paths appear (not merely `.env`-style CRITICAL exposure alone).

---

## Risk classification (summary)

| Tier | Illustrative signals |
|------|----------------------|
| CRITICAL | Listed canonical Record paths, `.env`, `secrets/`, private key filenames |
| HIGH | `config/authority-map.json`, MCP YAML configs, `process_approved_candidates.py`, `schemas/` |
| MEDIUM | `scripts/`, `docs/mcp/`, `artifacts/evidence-stubs/`, `tests/`, `examples/` |
| LOW | `README.md`, general `docs/`, `artifacts/patch-intake/` |

---

## Receipt behavior

Each successful write emits a validated receipt with **`capability.id`** **`coding_agent_patch_intake`**, **`output_lane`** **`candidate_proposal`**, **`requires_human_review: true`**, **`requires_gate_review: true`**. **`canonical_record_touched`** reflects canonical-path listings only.

---

## Patch packet vs candidate proposal vs gate candidate vs merge

| Concept | Role |
|---------|------|
| **Patch-review packet** (this adapter) | Human-readable WORK summary + risk labels — **not** approval. |
| **Candidate proposal** | Capability posture (`candidate_proposal` lane); still **not** merged Record truth. |
| **Gate candidate** | Companion-reviewed YAML/text destined for [`users/grace-mar/recursion-gate.md`](../../users/grace-mar/recursion-gate.md) **pipeline**, staged deliberately — adapter never edits this file. |
| **Approved merge** | Companion-approved **`process_approved_candidates.py`** apply only — outside this tool. |

**Agents ≠ authority.** Paste structured intake JSON here **after** the assistant responds so operators retain classification + receipts **without** conflating model narration with governance outcomes.

---

## Related registry row

[`coding_agent_patch_intake`](../../config/mcp-capabilities.yaml) — proposes **diff-shaped work** in worktrees only in governed MCP narratives; this repo implements the **offline intake packet + receipt** subset without calling remote helpers.
