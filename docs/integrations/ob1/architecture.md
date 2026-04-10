# OB1 Bridge Architecture

**Type:** Asymmetric bridge (not bidirectional sync)
**Authority:** companion-self (git, human-gated Record)
**Runtime:** OB1 (Supabase + pgvector, MCP, thoughts)

**Doctrine:** Integration features must preserve the distinction between **mixed-trust runtime memory** (OB1) and **canonical Record** (companion-self). Normative framing—proposed vs interface-visible vs canonical state, merge contract, Voice as interface—is in [Architecture — State governance](../../architecture.md#state-governance-proposed-interface-and-canonical).

---

## Design principles

1. **Asymmetric by design.** companion-self is the authority for durable identity. OB1 is a runtime memory surface with mixed-trust content. The bridge reflects this asymmetry in every data flow.
2. **Export-first.** Phase 1 (companion-self → OB1) ships before Phase 2 (OB1 → companion-self). Export is safe (read-only, downstream consumer); import requires governance.
3. **Stage-only return.** OB1 content entering companion-self is staged as proposals to RECURSION-GATE. It never writes directly to `self.md`, `self-archive.md`, or `bot/prompt.py`.
4. **No unattended sync.** No background polling, no cron, no automatic bidirectional loop. Every transfer is operator-initiated and observable.
5. **Provenance is mandatory.** Every exported chunk and every imported proposal carries source metadata, fingerprint, trust tier, and timestamp. No anonymous data crosses the bridge.
6. **State-governance alignment.** Staging, approval, and integrity boundaries are not optional polish—they keep the bridge **inspectable**. See [Architecture — State governance](../../architecture.md#state-governance-proposed-interface-and-canonical) and [ADR: Asymmetric bridge](adr-asymmetric-bridge.md) § Doctrine alignment.

---

## Parallel pattern: Cici instance (external)

The **[Cici](https://github.com/Xavier-x01/Cici)** repository (Xavier’s OB1 **instance** documentation repo, Phase 1 on `main`, commit [`6379661`](https://github.com/Xavier-x01/Cici/commit/6379661)) encodes a **related** governance shape: **three layers** (raw evidence → prepared context → **governed state**), **proposals** for material durable changes, and an **authority map** separating canonical owner writes, proposal-only agent writes, operational DB writes, and ephemeral state. Its doctrine states that **Git-managed governed state is canonical** and that **operational databases are derivative**—Supabase stays a supported **bridge** for search, MCP, and runtime, but **if Supabase and governed files diverge, governed state wins**.

That **rhymes** with companion-self’s [state governance](../../architecture.md#state-governance-proposed-interface-and-canonical) (proposed vs canonical, human gate) and with this bridge’s asymmetry (Record authority vs OB1 runtime). It does **not** change grace-mar’s rule: **companion-self alone** governs this instance’s **Record**; Cici is not a second canonical fork inside grace-mar. Cross-read: [Cici — Governed State Model](https://github.com/Xavier-x01/Cici#governed-state-model-phase-1), [`docs/governed-state-doctrine.md` on Cici](https://github.com/Xavier-x01/Cici/blob/main/docs/governed-state-doctrine.md), [OB1 README — Related: Cici](README.md#related-cici-instance-external).

---

## Phase 1: companion-self → OB1

```
companion-self repo          Bridge (export)              OB1
┌──────────────────┐    ┌──────────────────────┐    ┌──────────────┐
│ self.md           │    │ Export script         │    │ Recipe or    │
│ self-archive.md   │───>│  - read-only walk    │───>│ manual       │
│ self-memory.md    │    │  - include/exclude    │    │ ingest       │
│ (governed files)  │    │  - fingerprint + id   │    │              │
└──────────────────┘    │  - metadata sidecars  │    │ Supabase     │
                        │  - deterministic      │    │ thoughts     │
                        └──────────────────────┘    └──────────────┘
                              │
                              ▼
                        ob1-export/
                          manifest.json
                          self.identity.md
                          self.identity.meta.json
                          evidence.timeline.md
                          evidence.timeline.meta.json
```

**Safety model:** The export script reads companion-self files and emits a deterministic bundle. OB1 is a downstream consumer. No companion-self state is modified. Governed surfaces (pending gate candidates, session-log) are excluded by default.

**Tier 1 (target):** Markdown/JSON export bundle ingested via OB1 recipe or adapted importer.
**Tier 2 (optional):** Direct Supabase insert — higher maintenance, pinned to OB1 schema version.

---

## Phase 2: OB1 → companion-self

```
OB1                         Bridge (import-stage)        companion-self repo
┌──────────────────┐    ┌──────────────────────┐    ┌──────────────────┐
│ Supabase         │    │ Import script         │    │ recursion-gate.md│
│ thoughts         │───>│  - local JSON or API  │───>│  (pending        │
│ (mixed trust)    │    │  - grounding filter   │    │   proposals)     │
└──────────────────┘    │  - trust tier assign  │    └────────┬─────────┘
                        │  - dedup by id+fp     │             │
                        │  - proposal object    │    companion reviews
                        └──────────────────────┘             │
                                                    ┌────────▼─────────┐
                                                    │ process_approved │
                                                    │ _candidates.py   │
                                                    │ (merge on        │
                                                    │  approval only)  │
                                                    └──────────────────┘
```

**Safety model:** The import script reads OB1 thoughts and writes proposal objects (not gate YAML directly). Proposals are staged for human review. Low-grounded or duplicate thoughts are filtered before staging. The companion approves or rejects each proposal through the existing RECURSION-GATE pipeline. The import script **never** writes to `self.md`, `self-archive.md`, or `bot/prompt.py`.

**Tier 1 (target):** Stage proposal objects from local OB1 export JSON.
**Tier 2 (optional):** Fetch via OB1 API/client with transport adapter.

---

## What this bridge is not

- **Not bidirectional sync.** There is no loop. Each direction is a discrete, operator-initiated action.
- **Not a merge path.** OB1 content is source material, not pre-approved Record. It enters through the same gate as any other candidate.
- **Not autonomous.** No background process, no webhook, no scheduled job.
- **Not a replacement for the gated pipeline.** The bridge feeds into the existing RECURSION-GATE → companion-approval → merge flow. It does not bypass it.

---

## Known technical risks

### Chunking (Phase 1 export)

Long personal markdown files (`self.md`, `self-archive.md`) are hard to chunk for vector retrieval. Poor chunking causes lost context ("lost in the middle" effect), diluted embeddings, and suboptimal OB1 retrieval quality. This is the most common failure point in personal RAG systems.

**Mitigation:** Before implementing PR 4 (exporter), run a **chunking spike** — export one real `self.md` into OB1 under each strategy (`full_file`, `per_section`, `per_entry`), measure retrieval precision on 10 test queries, and pick the strategy that scores highest. Do not ship the exporter without this spike. See [mapping.md](mapping.md) § chunk_strategy for the field definition.

### pgvector / Supabase at scale

pgvector has known weaknesses: slower than dedicated vector DBs at scale, filtering/index interactions can return fewer results than expected, and schema/extension updates can break queries. Embedding model or version drift between export and ingest produces inconsistent retrieval.

**Mitigation:** Pin the embedding model in the export manifest (`embedding_model` field). Document the OB1 Supabase version and pgvector extension version at deployment time. Re-run the chunking spike after any Supabase or pgvector upgrade. If retrieval quality degrades after a Record growth milestone (~2x entries), evaluate index configuration.

### Schema and dependency drift

The bridge depends on OB1's thought schema, recipe system, and Supabase extensions. Even with version pinning, upstream changes can break export/import without warning.

**Mitigation:** Pin to a specific OB1 commit or tagged release (not `main`). When OB1 updates, re-run the export + import test suite against the new version before upgrading. If the upstream project removes or renames fields the bridge depends on, the import script should fail loudly rather than silently dropping data.

---

## Asymmetric value acknowledgment

Phase 1 (export to OB1) delivers quick wins: semantic search across AIs, better retrieval in OB1-connected clients. Phase 2 (import proposals) adds friction with potentially limited upside — most OB1 thoughts are Tier C synthesized output that will be filtered or rejected. The harder direction is also the lower-value direction.

**Implication:** Do not over-engineer Phase 2 before Phase 1 has proven its value in real usage. If Phase 1 retrieval quality is poor (chunking, embeddings), Phase 2 is moot.

---

## Scope creep guardrail

Once the bridge exists, pressure may grow for incremental features: auto-re-ingest on Record changes, bidirectional observers, webhook-triggered sync, or OB1-side triggers. Each of these erodes the core invariant (no unattended sync, companion-self governs).

**Rule:** Any feature that introduces **automatic data flow** between the systems requires a **new ADR** with explicit companion approval. The asymmetric bridge ADR does not authorize extensions beyond manual, operator-initiated transfers.
