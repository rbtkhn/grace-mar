# Prepared Context Doctrine

**Companion-Self template**

[Prepared context](prepared-context-layer.md) is the **staging layer** between [raw evidence](evidence-layer.md) and [governed state](governed-state-layer.md). It is optimized for agents and tools; it is **not** the Record and **not** silent approval.

---

## Principles

1. **Raw evidence is not automatically good agent context.** Normalize, scope, and cite provenance before heavy use.
2. **Prepared context should be optimized for reasoning**, not mistaken for durable truth or the **Record** (see [concept.md](concept.md)).
3. **Preserve provenance** wherever practical (source path, date, extractor version).
4. **Prefer regenerability** — prepared bundles should often be rebuildable from evidence plus scripts.
5. **Material changes to governed state** still require **gate** or **change-review** pathways ([change-review.md](change-review.md)); refreshing context does not merge identity.

---

## Examples

- PDF converted to markdown for analysis  
- Transcript compressed into structured notes with pointers to source  
- Retrieval chunks generated from an evidence corpus  
- Seed survey answers normalized into schema-conformant JSON (seed-phase artifacts are **pre-activation**; after activation, governed updates use the pipeline)  

---

## See also

- [evidence-to-context-pipeline.md](evidence-to-context-pipeline.md)  
- [state-model.md](state-model.md)  
- Starter staging script: `scripts/stage-evidence.py` (optional; creates JSON stubs under `prepared-context/`)
