# Export contract

Grace-Mar's outward portability layer: a coherent set of governed export classes over existing approved surfaces and existing exporters.

---

## Principle

Grace-Mar exports are **governed views** over companion-approved content — not raw memory dumps, not unreviewed runtime residue, not unfiltered candidate queues. Every export draws from the four canonical Record surfaces (SELF, SELF-LIBRARY, SKILLS, EVIDENCE) after content has passed through the gated pipeline.

Runtime-only material (warmup, memory briefs, skill cards, lane compression) may appear in runtime-aware export modes but is clearly marked as derived and non-canonical.

---

## Export classes

| Class | Purpose | Typical use |
|---|---|---|
| **Full governed profile** | Broad view across all approved surfaces, filtered by sensitivity | Primary runtime sideload, full fork handoff |
| **Task-limited profile** | Filtered slices from surfaces relevant to a specific task or role | Coach handoff, domain-specific onboarding |
| **Tool bootstrap profile** | Compact prompt encoding the Record for bootstrapping a new tool session | Pasting into a new LLM, agent cold start |
| **Demonstrated capability profile** | SKILLS + EVIDENCE focused — what this person can do and has done | Portfolio export, capability audit |
| **Internal-only** | Content approved into the Record but marked non-portable | Never exported; stays in the governed Record only |

---

## Allowed contents by class

| Surface | Full governed | Task-limited | Tool bootstrap | Demonstrated capability | Internal-only |
|---|---|---|---|---|---|
| **SELF** | Yes (sensitivity-filtered) | Relevant slices | Partial (core identity) | Minimal (context only) | May include non-portable entries |
| **SELF-LIBRARY** | Yes (sensitivity-filtered) | Relevant domains | Partial (key domains) | Minimal | May include non-portable entries |
| **SKILLS** | Yes | Relevant workflows | Selected skills | Yes — primary surface | May include non-portable entries |
| **EVIDENCE** | Yes (sensitivity-filtered) | Relevant artifacts | No (too large) | Yes — primary surface | May include non-portable entries |
| **Runtime** | Yes (marked derived) | No | No | No | N/A |

Sensitivity filtering: entries with `sensitivity_class: non_portable` or `portability_class: non_exportable` are excluded from all external-facing classes. `review_required` entries are included only after companion review clears them.

---

## Current export entry points

Each export class maps to existing scripts. No second export system is needed.

| Class | Script | Invocation |
|---|---|---|
| **Full governed profile** | [`export_runtime_bundle.py`](../../scripts/export_runtime_bundle.py) | `export.py bundle -- --mode portable_bundle_only` |
| **Full governed profile (with runtime)** | [`export_runtime_bundle.py`](../../scripts/export_runtime_bundle.py) | `export.py bundle -- --mode adjunct_runtime` |
| **Task-limited profile** | [`export_fork.py`](../../scripts/export_fork.py) | `export.py fork -- --format coach-handoff` |
| **Tool bootstrap profile** | [`export_prp.py`](../../scripts/export_prp.py) | `export.py prp` |
| **Demonstrated capability profile** | Rationale format and schema exist ([artifact-rationale.md](artifact-rationale.md)); dedicated export filtering not yet wired | Future: `export.py fork -- --export-class capability` |
| **Internal-only** | No export script — content stays in governed Record | By definition, not exported |

Additional exporters: `export_user_identity.py` (identity sections), `export_manifest.py` (policy manifest), `export_view.py` (audience views: `school`, `public`).

---

## Anti-duplication rule

This contract governs the existing export layer. It does not create a second export system:

- Export classes are **policy labels** over the existing `export.py` subcommands and their child scripts
- Filtering logic lives in the child scripts, not in a separate portability stack
- New export formats extend [`scripts/export.py`](../../scripts/export.py) as subcommands
- New schemas go in `schema-registry/`

---

## Future: CLI integration

When child scripts grow class-aware filtering, `export.py` can add a top-level `--export-class` flag that forwards to the child. The current dispatcher structure (pure subprocess forwarding) makes this a natural extension point.

Proposed future interface:

```
python scripts/export.py --export-class capability fork -- -o capability-export.json
```

This is a TODO, not a current feature. The export-class concept is documented here for contract clarity; the dispatcher does not yet interpret it.

---

## Related

- [current-capability-map.md](current-capability-map.md) — portability capability inventory
- [portable-working-identity.md](../portable-working-identity.md) — portability doctrine
- [runtime-vs-record.md](../runtime-vs-record.md) — canonical vs derived
- [EXPORT-CLI.md](../EXPORT-CLI.md) — unified CLI reference
- [portable-record-prompt.md](../portable-record-prompt.md) — PRP spec
