# Portability — current-state capability map

What Grace-Mar already solves, what remains incomplete, and what must not be duplicated.

---

## Already solved

These capabilities are live in the grace-mar instance.

| Capability | Implementation | Status |
|---|---|---|
| **Governed canonical Record** | Four first-class surfaces: SELF, SELF-LIBRARY, SKILLS, EVIDENCE. Companion approval required for all durable changes. | Live |
| **Runtime vs Record split** | Durable Record governed by the pipeline; runtime artifacts (skill cards, lane compression, memory briefs, warmup output) are derived and rebuildable. | Live — [runtime-vs-record.md](../runtime-vs-record.md) |
| **Prepared selective retrieval** | Progressive-disclosure index, budgeted context builds, memory briefs. Runtime-only; not Record. | Live — [prepared-context/](../../prepared-context/), [progressive-disclosure.md](../prepared-context/progressive-disclosure.md) |
| **PRP export** | Single pasteable prompt encoding the Record for any LLM. URL bootstrap supported. | Live — [`scripts/export_prp.py`](../../scripts/export_prp.py), [portable-record-prompt.md](../portable-record-prompt.md) |
| **Runtime bundle export** | Structured export with `record/`, `policy/`, `runtime/`, `audit/` directories. | Live — [`scripts/export_runtime_bundle.py`](../../scripts/export_runtime_bundle.py) |
| **JSON fork export** | Machine-readable Record snapshot. Optional JSON-LD output. | Live — [`scripts/export_fork.py`](../../scripts/export_fork.py), [EXPORT-CLI.md](../EXPORT-CLI.md) |
| **Unified export CLI** | Single dispatcher across all export modules. | Live — [`scripts/export.py`](../../scripts/export.py), [EXPORT-CLI.md](../EXPORT-CLI.md) |
| **Approval Inbox / recursion-gate** | Staging queue with YAML candidates, companion approval, merge script. | Live — [`users/grace-mar/recursion-gate.md`](../../users/grace-mar/recursion-gate.md), [`scripts/process_approved_candidates.py`](../../scripts/process_approved_candidates.py) |
| **Integrity validation** | 12-check validator covering boundary, convenience-path, and export freshness. | Live — [`scripts/validate-integrity.py`](../../scripts/validate-integrity.py) |
| **Export contract** | Five export classes (full governed, task-limited, tool bootstrap, demonstrated capability, internal-only) over existing exporters. | Live — [export-contract.md](export-contract.md) |

---

## Still incomplete

| Gap | Description | Priority |
|---|---|---|
| **External-AI extraction prompt pack** | Structured prompt for extracting portable working-intelligence from other AI systems into candidate objects. | This PR set |
| **Working-identity candidate schema** | Normalized JSON Schema for imported context that enters gate review before promotion to Record. | This PR set |
| **Thin MCP adapter** | Read-only connector over approved surfaces for tool-using agents. | Future |
| **Artifact-rationale format** | Structured format for demonstrated capability with provenance (why something was built, not just that it exists). | This PR set — [artifact-rationale.md](artifact-rationale.md) |

---

## Anti-duplication rule

Do not build a second memory system, a second export pipeline, or a second prepared-context layer. Extend the existing architecture:

- New export formats extend [`scripts/export.py`](../../scripts/export.py)
- New retrieval paths extend the prepared-context pipeline
- New candidate types use `recursion-gate.md` staging and `process_approved_candidates.py`
- New schemas go in `schema-registry/`

---

## Related

- [portable-working-identity.md](../portable-working-identity.md) — portability doctrine and four-layer mapping
- [architecture.md](../architecture.md) — system architecture
- [runtime-vs-record.md](../runtime-vs-record.md) — canonical vs derived
- [export-contract.md](export-contract.md) — export classes and the portability surface
- [artifact-rationale.md](artifact-rationale.md) — portable rationale format for demonstrated capability
