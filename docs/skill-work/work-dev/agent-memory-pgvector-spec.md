# Agent memory — PostgreSQL 16+ / pgvector (flaw-fix spec)

**Territory:** work-dev (WORK / infrastructure). **Not** companion Record; facts about the companion still use RECURSION-GATE. **Companion:** [AGENTS.md](../../../AGENTS.md), [openclaw-integration.md](../../openclaw-integration.md).

**Implements:** the flaw-fix plan for persistent chunked memory (hybrid retrieval, audit trail, reflection governance, dual-repo scope). **Canonical SQL:** [sql/agent_memory_v1_initial.sql](sql/agent_memory_v1_initial.sql).

---

## 1. Principles (aligned with original draft)

| Principle | Implementation |
|-----------|----------------|
| Persistent & session-agnostic | Postgres is **system of record**; see Redis boundary below. |
| Chunked & updatable | Rows are chunks; `version` + `agent_memory_revisions` on content/metadata change. |
| Hybrid retrieval | Vector (HNSW) + FTS (`simple`) + `memory_relations`; **fusion in app** (RRF §5). |
| Auditable & editable | Revisions table, `content_hash`, `source_url` / tier in `metadata` (convention §8). |
| Compounding | Reflection rows with **governance** §7 — not unconstrained summaries. |

---

## 2. Redis vs Postgres

**Postgres** holds durable chunks, embeddings (when computed), relations, revisions.

**Redis** is for **ephemeral** cache, rate limits, locks, optional “current session pointer” — **not** the only copy of chunk text. Session-agnostic recall must hit Postgres.

---

## 3. Vector strategy (single model per table generation)

- Column `embedding_model` is **required**; dimension in `vector(N)` must match that model (e.g. 768 for `all-mpnet-base-v2`). OpenAI and other APIs use **parameter-specific** widths — do not mix in one column.
- **Model upgrade:** new migration (new table or alter type), then **re-embed job** over `content`; keep `embedding_model` in sync.
- **`embedding` nullable:** supports “insert chunk → async worker embeds” without blocking ingestion.

---

## 4. Metadata & JSON queries (fixed patterns)

**Invalid (do not use):** `metadata->>'theme_tags' @> $2` — `->>` returns text; `@>` is for **jsonb**.

**Valid examples:**

```sql
-- Single tag in JSON array theme_tags
WHERE (metadata->'theme_tags') @> '["china"]'::jsonb;

-- Whole-object containment
WHERE metadata @> '{"theme_tags": ["china"]}'::jsonb;

-- Prefer text[] for heavy tag queries (optional migration)
-- theme_tags text[] GENERATED ALWAYS AS (...) STORED
-- WHERE theme_tags && ARRAY['china', 'taiwan'];
```

**Required indexes (minimum):** `CREATE INDEX idx_memory_user_created ON agent_memory (user_id, created_at DESC);` plus `GIN (metadata jsonb_path_ops)` — see migration file.

---

## 5. Hybrid retrieval — explicit fusion (RRF)

Schema does not merge vector and FTS automatically. **Application pattern:**

1. **Vector leg:** `ORDER BY embedding <=> $query_vec` with `WHERE user_id = $u AND embedding IS NOT NULL` (and optional jsonb filters), `LIMIT k1`.
2. **FTS leg:** `ORDER BY ts_rank(to_tsvector('simple', content), plainto_tsquery('simple', $q)) DESC` (or `websearch_to_tsquery` if you prefer), `LIMIT k2`.
3. **Reciprocal rank fusion (RRF):** for each doc id, score `sum(1 / (k + rank_i))` over legs (typical `k` = 60), then sort descending.
4. **Dedupe** by `metadata->>'original_artifact_id'` or stable `content_hash` when the same source appears in both legs.

Tune `k1`, `k2`, and RRF `k` per workload.

---

## 6. Full-text search — multilingual baseline

English-only `to_tsvector('english', content)` underperforms on Italian/Latin/Chinese Vatican–China corpora.

**Baseline in migration:** `to_tsvector('simple', content)` index.

**Escalation paths:** per-language generated columns + indexes; or external engine (OpenSearch/Meilisearch) if FTS is first-class.

---

## 7. Reflection governance (high-stakes OSINT)

Unconstrained `reflection_summary` rows **cement hallucinations**. Convention for `metadata` on reflection chunks:

```json
{
  "memory_kind": "reflection_summary",
  "confidence": 0.0,
  "evidence_chunk_ids": ["uuid", "uuid"],
  "human_approved": false,
  "contradicts_memory_id": null
}
```

- **Trusted context** for downstream prompts: only use reflections with `human_approved: true` or cap `confidence` by policy.
- **Contradictions:** insert a new row and a `memory_relations` edge with `relation_type = 'contradicts'` (optional `contradicts_memory_id` in metadata for quick UI).
- **Decay:** TTL or periodic review job; stale reflections down-ranked or archived.

Aligns with Grace-Mar: **machine proposes, human approves** for policy-like memory.

---

## 8. Source provenance (Grace-Mar / OSINT)

For Vatican–China or similar streams, preserve evidence tier in metadata (mirror work-politics practice):

```json
{
  "source_type": "vatican_bollettino",
  "source_url": "https://press.vatican.va/...",
  "source_fetched_at": "2026-04-04T12:00:00Z",
  "evidence_tier": "A",
  "theme_tags": ["china", "bishop_appointment"]
}
```

**Never** promote tier via reflection (e.g. C → “magisterial”) without a new primary artifact.

---

## 9. Graph edges — avoid over-linking

Do **not** link “every China mention” to a single Agreement hub automatically. **Rules:** threshold on confidence / NER match; cap **out-degree** per chunk; one **canonical** Agreement chunk with stable `id` for intentional links.

`memory_relations`: `ON DELETE CASCADE`, `CHECK (source_id <> target_id)` — see SQL file.

**Neo4j / GraphDB:** defer until Postgres proves insufficient for your query shape; if added, **one writer** + idempotent sync.

---

## 10. Row-level security

Migration enables RLS on `agent_memory`, `agent_memory_revisions`, `memory_relations`.

**Application:** per session, set tenant (example):

```sql
SET app.tenant_id = 'operator_or_tenant_slug';
```

Use a **restricted** DB role without `BYPASSRLS` for app traffic. The **table owner** bypasses RLS unless `ALTER TABLE ... FORCE ROW LEVEL SECURITY` — prefer a non-owner application role so policies actually enforce. Migrations/batch jobs may use a privileged role with care.

---

## 11. Query examples (Python / psycopg — illustrative)

**Semantic + tag filter (jsonb correct):**

```python
# $1 = query embedding vector literal, $2 = user_id, $3 optional tag
cur.execute(
    """
    SELECT id, content, metadata,
           1 - (embedding <=> %s::vector) AS similarity
    FROM agent_memory
    WHERE user_id = %s
      AND embedding IS NOT NULL
      AND (metadata->'theme_tags') @> %s::jsonb
    ORDER BY embedding <=> %s::vector
    LIMIT 8
    """,
    (query_vec, user_id, '["china"]', query_vec),
)
```

**Compound context (pattern):** recent rows by time + optional filter `metadata->>'memory_kind' = 'reflection_summary'` with governance flags — implement in DAO; no single SQL fits every app.

---

## 12. Cost & operations

Separate **VPS/RAM** (self-hosted embedders), **API embedding spend**, and **operator time** (re-embed, migration). A low VPS headline does not include heavy API embedding volume.

---

## 13. Orchestration stack

Pick **one** primary framework (LangGraph *or* LlamaIndex *or* other) for ingest/query glue — avoid three parallel sources of truth. Evaluation: spot-check “memory used this run” logs.

---

## 14. Dual-repo scope (grace-mar + companion-self)

Dual-repo rules in [docs/operator-agent-lanes.md](../../operator-agent-lanes.md) are **git / push hygiene** — they do **not** auto-require this stack in both repos.

**EXECUTE** messages should name **grace-mar only**, **companion-self only**, or **both** and the **order** of landing migrations/docs. After cross-repo edits, run [work-companion-self/README.md](../work-companion-self/README.md) and `scripts/template_diff.py` (from repo root; see `--help`) as usual.

**Canonical home:** choose one repo for **authoritative** `agent_memory_v1_initial.sql` + this spec; the other **links or imports** — avoid divergent DDL without a written sync rule.

---

## 15. Revision log (this artifact)

| Date | Change |
|------|--------|
| 2026-04-04 | Initial spec + `sql/agent_memory_v1_initial.sql` from flaw-fix plan. |
