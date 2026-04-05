# Evidence to Context Pipeline

**Companion-Self template · Reference flow**

A **reference** sequence from raw inputs to governed updates. Instances may use different tools; the **layer discipline** should hold (see [state-model.md](state-model.md)).

---

## Stages

1. **Collect** — evidence enters the [Evidence Layer](evidence-layer.md) (uploads, transcripts, notes, logs).  
2. **Normalize / clean** — dedupe, format, strip noise; keep provenance.  
3. **Extract or structure** — fields, summaries, tables, chunks.  
4. **Generate prepared context** — artifacts under operational control ([Prepared Context Layer](prepared-context-layer.md)).  
5. **Use for reasoning** — agents, retrieval, prompt assembly, proposals.  
6. **Route material changes** — proposals into **gate** or **change-review** before they become [Governed State](governed-state-layer.md).  

---

## Non-goals

- Prepared context is **not** the **Record**.  
- Prepared context is **not** silent approval.  
- Agent usability does **not** override provenance or governance.  

---

## Related

- [prepared-context-doctrine.md](prepared-context-doctrine.md)  
- [change-review-lifecycle.md](change-review-lifecycle.md)  
