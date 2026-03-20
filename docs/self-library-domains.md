# Library Domain Registry

**Status:** Canonical index of **installed knowledge domains** the fork may consult for reference (SELF-LIBRARY and related paths). **Not** SELF-KNOWLEDGE. Complements [boundary-self-knowledge-self-library.md](boundary-self-knowledge-self-library.md), [glossary.md](glossary.md), [library-integration.md](library-integration.md), [cmc-routing.md](cmc-routing.md).

**Machine-readable source:** [self-library-domains.json](self-library-domains.json) — validators and tooling should read JSON; this doc is the human-readable mirror.

---

## Governance rule

**No library domain may be routable unless it is declared in the registry** with:

- **surface** — where it lives (Record library, runtime helper, external integration)
- **authority** — canonical, advisory, experimental, or deprecated
- **mutation_policy** — retrieval only, stage-only, or eligible for gated merge

Add a new auto-routed domain → add JSON entry + routing doc + `docs/cmc-routing.md` or `bot/core.py` changes as appropriate; extend `scripts/validate_library_domain_registry.py` **required domain ids** if the code gains new routable domains.

---

## Six questions (each domain answers these)

| Question | Field in JSON |
|----------|----------------|
| What is it? | `id`, `name`, `what` |
| What kind of surface? | `surface`, `surface_detail` |
| What authority? | `authority` |
| How is it invoked? | `invocation`, `invocation_detail` |
| What can it update? | `mutation_policy`, `mutation_detail` |
| How fresh is it? | `freshness` (last_refresh, evidence_coverage, staleness) |

Plus **`owner`** (e.g. record, operator) and **`routing_docs`** / **`code_refs`** for traceability.

---

## Declared domains (summary)

| id | Name | Surface | Authority | Invocation | Mutation |
|----|------|---------|-----------|------------|----------|
| `civ_mem` | CIV-MEM | record_library | canonical | query-triggered (CMC) | retrieval only |
| `lib_entries` | LIB entries | record_library | canonical | query-triggered (analyst LIB summary) | retrieval; perimeter via gate |
| `books` | Books shelf | record_library | advisory | manual / title | retrieval + stage |

Full rows: **see [self-library-domains.json](self-library-domains.json)**.

---

## Related

- [architecture.md](architecture.md) — Record surfaces
- [identity-fork-protocol.md](identity-fork-protocol.md) — proposal_class for library vs identity
- [harness-inventory.md](harness-inventory.md) — Record bundle surfaces
