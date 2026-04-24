# OB1 Bridge — Canonical Mapping Specification

Defines the object schemas for both bridge directions. Every field has a definition, a type, and a note on whether it is required or optional.

**Related:** [architecture.md](architecture.md) (data flow), [trust-tiers.md](trust-tiers.md) (classification system), [operator-runbook.md](operator-runbook.md) (usage).

---

## Conceptual map (OB1, Cici, grace-mar)

This section is **not** part of the bridge object schemas. It orients operators and advisors so **upstream OB1**, **Xavier’s instance repo (Cici)**, and **grace-mar** are not conflated.

**One-line stack:** OB1 is the **shared memory substrate**; Cici is a **personal governed instance** on top of that substrate; grace-mar is the most ambitious attempt in this family to turn that general area into a **full cognitive-governance architecture** (Record theory, gate, four surfaces, not just memory tooling).

**Role in the stack**

| Repo | Primary role |
|------|----------------|
| **[OB1](https://github.com/NateBJones-Projects/OB1)** (upstream) | Public **memory substrate** — Supabase + pgvector + MCP, extensions/recipes/skills/dashboards as a **contribution ecosystem**. Not a cognitive-fork Record system. |
| **[Cici](https://github.com/Xavier-x01/Cici)** (external instance) | **Personal OB1 instance layer** — config/docs in git; durable captured memory in private Supabase. Phase 1 adds **git-first governed state** (evidence / prepared context / `users/<instance>/governed-state`, proposals). |
| **grace-mar** (this repo) | **Governed cognitive-architecture instance** — four Record surfaces (SELF, SELF-LIBRARY, SKILLS, EVIDENCE), RECURSION-GATE, Voice, work territories; [state model](../../state-model.md) three layers **in doctrine**, not necessarily the same paths as Cici. |

**Where “governed truth” is supposed to live**

| Repo | Canonical durable truth | Operational / derivative |
|------|-------------------------|---------------------------|
| **OB1** (platform) | User’s **thoughts** in **their** Postgres (typical deployment); repo holds **contributions**, not personal memory. | Edge functions, dashboards, recipes — deployment-specific. |
| **Cici** | **Git-managed governed state** per [Cici doctrine](https://github.com/Xavier-x01/Cici/blob/main/docs/governed-state-doctrine.md) (if git and Supabase diverge, **governed files win**). | Supabase as **operational bridge** (search, MCP, etc.). |
| **grace-mar** | **Record** under `users/grace-mar/` (and gated merge path) — **companion-self** authority model. | MEMORY, WORK drafts, exports; OB1 downstream of export is **not** canonical for identity. |

**Structural caution:** Cici’s Phase 1 **folder names** resemble grace-mar’s **state-model vocabulary** (evidence, prepared context, governed state). In grace-mar, **root** [`evidence/`](../../../evidence/) and [`prepared-context/`](../../../prepared-context/) are **reserved placeholders** only — see [state model § Repo layout](../../state-model.md#repo-layout-grace-mar). Territory-scoped evidence (e.g. work-cici) lives under `docs/skill-work/.../evidence/`. **Do not** assume Cici-style routing exists at the repo root without reading those docs.

---

## Direction A: companion-self → OB1 (export object)

Each exported chunk produces one **export object** — a content file plus a metadata sidecar. The manifest lists all objects in the bundle.

### Export object fields

| Field | Type | Required | Definition |
|-------|------|----------|------------|
| `source_system` | string | yes | Always `"companion-self"`. Identifies the origin system. |
| `user_id` | string | yes | The companion-self user directory name (e.g. `"grace-mar"`). |
| `source_path` | string | yes | Repo-relative path of the source file (e.g. `"users/grace-mar/self.md"`). |
| `surface_class` | string | yes | Semantic classification of the source surface. One of: `identity`, `evidence`, `skills`, `memory`, `work`, `archive`. See surface class table below. |
| `content_type` | string | yes | MIME-like type of the exported content. Typically `"text/markdown"` or `"application/json"`. |
| `git_commit` | string | yes | The git commit SHA at export time. Ties the export to an auditable repo state. |
| `exported_at` | string (ISO 8601) | yes | UTC timestamp of the export run. |
| `stable_id` | string | yes | Deterministic identifier derived from `source_path` + `surface_class`. Remains constant across exports of the same source. Used for dedup and update detection in OB1. |
| `fingerprint_sha256` | string | yes | SHA-256 hash of the exported content. Changes when content changes; stable when content is unchanged. Enables dedup and change detection. |
| `chunk_strategy` | string | yes | How the source was chunked for export. One of: `full_file`, `per_entry`, `per_section`. Determines granularity of OB1 thoughts. |
| `trust_tier` | string | yes | Trust classification of the exported content. One of: `A` (raw evidence), `B` (structured summary), `C` (synthesized output). See [trust-tiers.md](trust-tiers.md). |
| `transform_level` | string | yes | Degree of transformation from source. One of: `verbatim` (exact copy), `extracted` (subset of source), `reformatted` (structure changed, content preserved). |

### Surface class table

| `surface_class` | Source paths | Trust tier | Notes |
|-----------------|-------------|------------|-------|
| `identity` | `self.md` (§I-IX) | A | Core Record — companion-approved identity |
| `evidence` | `self-archive.md` (EVIDENCE) | A | Immutable dated entries (ACT, READ, WRITE, CREATE, MEDIA) |
| `skills` | `self-skills.md` | A | Capability claims — upgrade only, never downgrade |
| `memory` | `self-memory.md` | B | Ephemeral continuity, not durable Record; excluded by default |
| `work` | `work-*.md`, `docs/skill-work/` | C | Operator work product; mixed trust; excluded by default |
| `archive` | Artifacts under `users/<id>/artifacts/` | A | Companion-produced artifacts (drawings, writing samples) |

### Manifest schema

The `manifest.json` file in the export bundle root:

| Field | Type | Definition |
|-------|------|------------|
| `export_version` | string | Schema version of this manifest (e.g. `"1.0"`). |
| `source_system` | string | Always `"companion-self"`. |
| `user_id` | string | Companion-self user directory name. |
| `git_commit` | string | Commit SHA at export time. |
| `exported_at` | string (ISO 8601) | UTC timestamp. |
| `chunk_strategy` | string | Default strategy for this export run. |
| `objects` | array | List of `{ stable_id, source_path, surface_class, fingerprint_sha256, content_file, meta_file }`. |
| `excluded_surfaces` | array | List of `{ source_path, reason }` for surfaces excluded by default or by `--exclude`. |

---

## Direction B: OB1 → companion-self (import proposal object)

Each OB1 thought that passes grounding filters produces one **proposal object** — a structured record staged for human review. The proposal object is the canonical form; any rendered markdown summary is derived from it.

### Import proposal fields

| Field | Type | Required | Definition |
|-------|------|----------|------------|
| `proposal_id` | string | yes | Unique identifier for this proposal (e.g. `"OB1-PROP-0001"`). Assigned by the import script. |
| `source_system` | string | yes | Always `"ob1"`. Identifies the origin system. |
| `ob1_thought_id` | string | yes | The original thought ID from OB1's database. Used for dedup and provenance tracing. |
| `source_metadata` | object | yes | Preserved OB1 metadata: `{ created_at, updated_at, tags, embedding_model, ... }`. Structure mirrors OB1's thought schema. |
| `captured_at` | string (ISO 8601) | yes | When the thought was originally created in OB1. |
| `imported_at` | string (ISO 8601) | yes | When this proposal was generated by the import script. |
| `target_surface` | string | yes | Recommended companion-self destination. One of: `IX-A` (knowledge), `IX-B` (curiosity), `IX-C` (personality), `evidence` (ACT/READ/WRITE/CREATE), `memory` (self-memory, non-Record), `reject`. |
| `proposal_type` | string | yes | Classification of what the thought contributes. One of: `knowledge_claim`, `curiosity_signal`, `personality_observation`, `activity_record`, `memory_pointer`, `unclassified`. |
| `summary` | string | yes | One-line human-readable summary of the thought's content. |
| `full_content` | string | yes | Complete thought text from OB1. Preserved verbatim for review. |
| `provenance` | object | yes | `{ source_system, ob1_thought_id, captured_at, imported_at, import_script_version, trust_tier, grounding_score }`. Full chain of custody. |
| `trust_tier` | string | yes | Trust classification. One of: `A`, `B`, `C`. See [trust-tiers.md](trust-tiers.md). |
| `grounding_signals` | object | yes | Output of grounding filter: `{ score, is_grounded, evidence_refs, flags[] }`. Explains why the thought passed or was flagged. |
| `review_status` | string | yes | Current review state. One of: `pending`, `approved`, `rejected`, `deferred`. Set to `pending` on import. |
| `human_action_required` | boolean | yes | Always `true` on import. A proposal cannot auto-merge. |

### Target surface assignment rules

| Condition | `target_surface` | Rationale |
|-----------|-----------------|-----------|
| Thought contains a factual claim about the companion's knowledge or learning | `IX-A` | Knowledge dimension |
| Thought describes a topic the companion showed interest in | `IX-B` | Curiosity dimension |
| Thought describes a behavioral pattern, preference, or personality trait | `IX-C` | Personality dimension |
| Thought records a specific activity with date and context | `evidence` | Activity log entry |
| Thought is contextual/operational but not identity-bearing | `memory` | Ephemeral, non-Record |
| Thought is speculative, ungrounded, or model-generated without companion input | `reject` | Does not meet Record threshold |

### Deduplication rules

A proposal is a duplicate if **any** of these match an existing proposal or merged Record entry:
- Same `ob1_thought_id` (exact OB1 source match)
- Same `fingerprint_sha256` of `full_content` (content-identical regardless of OB1 id)
- Same `summary` + `target_surface` within 24 hours of `captured_at` (near-duplicate)

Duplicates are logged and skipped, not staged.

---

## Field-level provenance chain

For any piece of data that crosses the bridge, the provenance chain must be reconstructable:

**Export (CS → OB1):**
`self.md §IX-A` → `export_open_brain_bundle.py` → `ob1-export/self.identity.md` + `self.identity.meta.json` → OB1 recipe ingest → OB1 thought

At each step: `source_path`, `git_commit`, `fingerprint_sha256`, `exported_at`.

**Import (OB1 → CS):**
OB1 thought → `import_ob1_to_proposals.py` → proposal object (JSON) → operator review → RECURSION-GATE candidate → `process_approved_candidates.py` → `self.md`

At each step: `ob1_thought_id`, `captured_at`, `imported_at`, `trust_tier`, `grounding_score`, `review_status`.

---

## Chunking guidance (Phase 1 export)

The `chunk_strategy` field determines how source files are split for OB1 ingest. Choosing wrong causes poor retrieval quality — the single most common failure point in personal RAG systems.

| Strategy | When to use | Risk |
|----------|-------------|------|
| `full_file` | Short files (< 2,000 tokens): `self-skills.md`, individual artifacts | Safe default; fails on long files (embedding dilution) |
| `per_section` | Structured files with clear headings: `self.md` (§I through §IX), `self-archive.md` (per category) | Good balance; requires reliable heading detection |
| `per_entry` | Log-shaped files with dated entries: `self-archive.md` EVIDENCE entries (ACT-*, READ-*, etc.) | Highest granularity; best for retrieval precision; may lose cross-entry context |

**Blocking prerequisite (PR 4):** Before shipping the exporter, run a **chunking spike** — export one real `self.md` under each strategy, ingest into OB1, run 10 retrieval test queries, and measure precision. Do not ship without this data. See [architecture.md](architecture.md) § Known technical risks.

**Near-miss deduplication:** When content is reformatted or lightly edited between exports, `fingerprint_sha256` changes even though the semantic content is the same. The `stable_id` (derived from `source_path` + `surface_class`) handles update-in-place for the same source. For content that moved between files, dedup relies on the OB1-side recipe to detect near-duplicates by embedding similarity — this is outside the bridge's scope but should be noted in the operator runbook.

---

## Idempotency contract

Repeated export runs with the same source content must produce identical output:
- Same `stable_id` values
- Same `fingerprint_sha256` values
- Same manifest content (modulo `exported_at` timestamp)

The `exported_at` field is metadata, not content — it should not affect fingerprints. If determinism breaks, the likely cause is non-deterministic file walking order or timestamp leakage into content fields. The export test suite (PR 5) must include a "run twice, diff output" test.
