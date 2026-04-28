# Governed MCP layer (Grace-Mar)

**Status:** Planning and policy surface only. This document does **not** connect MCP servers or execute external tools.

**Related:** Read-only export adapter — [`integrations/mcp-adapter.md`](../integrations/mcp-adapter.md). Internal worker trust (different domain) — [`schemas/worker-trust-registry.v1.schema.json`](../../schemas/worker-trust-registry.v1.schema.json). Capability registry — [`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml), schema [`schemas/mcp-capability.v1.json`](../../schemas/mcp-capability.v1.json). Lane ↔ authority bindings — [`config/mcp-authority-bindings.yaml`](../../config/mcp-authority-bindings.yaml), [`mcp-authority-bindings.md`](mcp-authority-bindings.md). Execution receipts — [`schemas/mcp-execution-receipt.v1.json`](../../schemas/mcp-execution-receipt.v1.json), [`mcp-execution-receipts.md`](mcp-execution-receipts.md).

---

## What MCP is

**Model Context Protocol (MCP)** is a host–tool protocol: clients (IDEs, assistants) discover tools and exchange structured requests/responses. It is **not** merge authority and **not** Grace-Mar’s Record.

---

## Why MCP must stay governed

Grace-Mar separates **interface/runtime assistance** from **canonical durable state**. MCP tools may speed retrieval, drafting, and WORK-layer coordination; they must **not** become a silent path into `self.md`, EVIDENCE, `bot/prompt.py`, or other gated surfaces. Merge authority stays with the companion and the governed pipeline ([`AGENTS.md`](../../AGENTS.md)).

---

## Runtime vs Record

| Side | Role |
|------|------|
| **Runtime / WORK** | Sessions, scripts, exports, assistant drafts, receipts, scratch patches — visible and inspectable. |
| **Record (canonical)** | Approved identity and evidence — merged only via [`recursion-gate.md`](../../users/grace-mar/recursion-gate.md) and [`process_approved_candidates.py`](../../scripts/process_approved_candidates.py) (human gate). |

MCP outputs belong on the **runtime / WORK** side until promoted through the gate.

---

## MCP authority ladder (informal)

1. **Read-only retrieval** — governed exports, public URLs, read-only DB/GH views (receipts encouraged).
2. **Work artifacts** — Markdown/JSON under WORK lanes, logs, operator-visible drafts.
3. **Evidence stubs / prepared context** — pre-canonical material feeding review.
4. **Candidate proposals** — YAML/text staged for [`recursion-gate.md`](../../users/grace-mar/recursion-gate.md).
5. **Canonical merge** — companion-approved apply only.

Skipping steps 4–5 for “durable identity truth” is an anti-pattern.

---

## Allowed vs prohibited (examples)

Illustrative capability **classes** live in [`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml). Examples:

| Intent | Allowed posture | Prohibited |
|--------|-----------------|------------|
| Browse repo / docs | Read-only paths, export views | Writing into `users/*/self.md` without gate |
| SCM | Read issues/PRs; draft branches as **proposals** | Merge to default branch as Record truth |
| Web | Fetch/summarize with citations | Treating fetched text as merged IX-A |
| Shell | **Policy default:** not enabled for governed MCP (`shell_execution_prohibited` class) | Arbitrary subprocess on operator machine |
| External memory | Policy class rejects silent sync | Implying retrieval = gate approval |

---

## How MCP outputs become stubs, artifacts, or candidates

- **Evidence stubs / prepared context:** Operator tooling may emit structured drafts; they remain **non-canonical** until merged.
- **Work artifacts:** Logs, dashboards, lane files — rebuildable, non-Record ([`artifacts/README.md`](../../artifacts/README.md)).
- **Gate candidates:** YAML blocks or drafts appended via staging conventions — **never** auto-merge.

---

## Why durable mutation requires review

Durable changes encode **identity and accountability**. Tooling cannot substitute for companion consent; “the model wrote it” or “MCP returned success” is **not** approval. Review preserves auditability and aligns with [`authority-values.md`](../authority-values.md) and source-of-truth rules.

---

## Authority binding (lanes ↔ `authority-map.json`)

Each **`output_lane`** in [`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml) must map to exactly one row in [`config/mcp-authority-bindings.yaml`](../../config/mcp-authority-bindings.yaml). Bindings pin lanes to **`authority_surface`** keys from [`config/authority-map.json`](../../config/authority-map.json) so capability posture cannot drift into wider write classes without an explicit policy edit.

Cross-check (writes [`artifacts/mcp-authority-report.md`](../../artifacts/mcp-authority-report.md)):

```bash
python3 scripts/mcp_authority_check.py
```

Use **`--strict`** to fail when informational warnings fire (e.g. unused binding lanes). Full rationale and mapping table: **[`mcp-authority-bindings.md`](mcp-authority-bindings.md)**.

---

## Execution receipts

Every capability class that may emit tool-shaped work should produce **execution receipts** ([`schemas/mcp-execution-receipt.v1.json`](../../schemas/mcp-execution-receipt.v1.json)): structured audit metadata linking **`capability.id`**, **`output_lane`**, and **authority** resolved from bindings. Receipts live under **[`artifacts/mcp-receipts/`](../../artifacts/mcp-receipts/)** — **WORK/runtime artifacts**, not canonical Record. **Receipts do not grant approval**; durable Record change still requires recursion-gate review and companion-approved merge.

Before enabling **live MCP integration**, receipt generation and validation (`scripts/mcp_receipt.py`, `scripts/mcp_receipt_audit.py`) should be part of the operator workflow so posture cannot drift unseen. Full semantics: **[`mcp-execution-receipts.md`](mcp-execution-receipts.md)**.

---

## Audit

Regenerate the Markdown report after editing the registry:

```bash
python3 scripts/mcp_capability_audit.py
```

Output: [`artifacts/mcp-capability-report.md`](../../artifacts/mcp-capability-report.md). Use `--strict` in CI if you want the process to fail when heuristics flag risk.

After changing bindings or `authority-map.json`, run **`mcp_authority_check.py`** as well (see **Authority binding** above).
