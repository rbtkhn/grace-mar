# Artifact rationale — portable demonstrated capability

A lightweight format for recording not just *that* an artifact exists, but *why* it was judged good and *what transferable pattern* it demonstrates.

This format is **separate** from `/artifacts/` directory policy. Here, `artifact` means a **demonstrated capability artifact** linked to EVIDENCE, not every rebuildable file under `artifacts/`.

---

## What it is

An artifact rationale is a structured companion to an EVIDENCE entry. Where EVIDENCE says "this was produced" (a concrete artifact trace), the rationale says:

- **Why it was good** — the quality signal
- **What trade-offs were made** — what was chosen and what was rejected
- **What transferable pattern it demonstrates** — the reusable insight, abstracted from the specific context

## Why it matters

Portable working intelligence is not just knowledge and preferences — it includes **demonstrated capability**. But a bare artifact list ("built X, wrote Y") loses the judgment that made those artifacts good. The rationale preserves the judgment signal so it can transfer across tools, roles, and contexts.

Without rationale, a capability portfolio is a list of nouns. With rationale, it becomes evidence of *how someone thinks and decides*.

## How it differs from the artifact itself

| | Artifact | Rationale |
|---|---|---|
| **What it records** | The thing that was produced | Why it was produced well |
| **Where it lives** | EVIDENCE (self-archive.md) | Alongside or linked from EVIDENCE |
| **Portability** | Often context-bound (code, domain) | Abstracts the transferable pattern |
| **Sensitivity** | May contain employer-bound content | Strips non-portable details explicitly |

The rationale is not a replacement for the artifact — it is a portable lens over it.

## How to use it

1. When adding an EVIDENCE entry that represents demonstrated capability, optionally create a rationale using the [template](../templates/artifact-rationale-template.md)
2. The rationale follows the [JSON Schema](../../schema-registry/artifact-rationale.v1.json) for machine-readable use
3. Rationales are particularly useful for the **demonstrated capability** export class (see [export-contract.md](export-contract.md))

Rationales are not mandatory for every EVIDENCE entry. Use them when the *why* and *transferable pattern* matter for portability — typically for substantial artifacts, not minor log entries.

## Integration with exports

Rationales support the **demonstrated capability profile** export class defined in the [export contract](export-contract.md). When a capability export is requested, SKILLS + EVIDENCE entries with rationales provide richer signal than bare artifact lists.

The `export_class` field in the schema aligns with the five export classes defined in the contract: `full_governed`, `task_limited`, `tool_bootstrap`, `capability`, `internal_only`.

---

## Related

- [export-contract.md](export-contract.md) — export classes and the portability surface
- [promotion-rules.md](promotion-rules.md) — where approved candidates land (EVIDENCE section)
- [working-identity-candidates.md](working-identity-candidates.md) — candidate lifecycle
- [`schema-registry/artifact-rationale.v1.json`](../../schema-registry/artifact-rationale.v1.json) — JSON Schema
- [`docs/templates/artifact-rationale-template.md`](../templates/artifact-rationale-template.md) — fill-in template
