# Prepared Context Layer

The **Prepared Context Layer** holds **cleaned or transformed** representations of evidence, intended for agent reasoning, retrieval, or prompt assembly.

**Examples:**

- Markdown-normalized documents  
- Extracted fields  
- Summaries **with** provenance pointers  
- Retrieval chunks  
- Context bundles (e.g. for IDE or bot)  

---

## Rules

- Prepared context must remain **traceable to evidence** where practical.
- It is **operational**, not authoritative as durable companion truth.
- Optimize for **reasoning and safety of use**; do **not** mistake it for the **Record**.
- Prefer designs where prepared artifacts are **replaceable or regenerable** from evidence.

Governed updates to identity, pedagogy, or memory rules still require **change review** or the **gate**, not “context refresh” alone.

See [state-model.md](state-model.md) and [prepared-context-doctrine.md](prepared-context-doctrine.md).
