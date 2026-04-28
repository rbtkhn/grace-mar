# Governed MCP layer (Grace-Mar)

**Status:** Planning and policy surface only. This document does **not** connect MCP servers or execute external tools.

**Related:** Read-only export adapter — [`integrations/mcp-adapter.md`](../integrations/mcp-adapter.md). Internal worker trust (different domain) — [`schemas/worker-trust-registry.v1.schema.json`](../../schemas/worker-trust-registry.v1.schema.json). Capability registry — [`config/mcp-capabilities.yaml`](../../config/mcp-capabilities.yaml), schema [`schemas/mcp-capability.v1.json`](../../schemas/mcp-capability.v1.json).

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

## Audit

Regenerate the Markdown report after editing the registry:

```bash
python3 scripts/mcp_capability_audit.py
```

Output: [`artifacts/mcp-capability-report.md`](../../artifacts/mcp-capability-report.md). Use `--strict` in CI if you want the process to fail when heuristics flag risk.
