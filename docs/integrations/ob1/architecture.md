# OB1 Bridge Architecture

**Type:** Asymmetric bridge (not bidirectional sync)
**Authority:** companion-self (git, human-gated Record)
**Runtime:** OB1 (Supabase + pgvector, MCP, thoughts)

---

## Design principles

1. **Asymmetric by design.** companion-self is the authority for durable identity. OB1 is a runtime memory surface with mixed-trust content. The bridge reflects this asymmetry in every data flow.
2. **Export-first.** Phase 1 (companion-self → OB1) ships before Phase 2 (OB1 → companion-self). Export is safe (read-only, downstream consumer); import requires governance.
3. **Stage-only return.** OB1 content entering companion-self is staged as proposals to RECURSION-GATE. It never writes directly to `self.md`, `self-archive.md`, or `bot/prompt.py`.
4. **No unattended sync.** No background polling, no cron, no automatic bidirectional loop. Every transfer is operator-initiated and observable.
5. **Provenance is mandatory.** Every exported chunk and every imported proposal carries source metadata, fingerprint, trust tier, and timestamp. No anonymous data crosses the bridge.

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
