-- Agent memory v1 — PostgreSQL 16+ with pgvector
-- Spec: docs/skill-work/work-dev/agent-memory-pgvector-spec.md
-- Adjust vector(N) to match your embedding model before applying.
--
-- Triggers use EXECUTE PROCEDURE (standard). On some builds, EXECUTE FUNCTION
-- is accepted instead (see PostgreSQL CREATE TRIGGER docs).

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ---------------------------------------------------------------------------
-- Core memory table
-- ---------------------------------------------------------------------------
CREATE TABLE agent_memory (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         TEXT NOT NULL,
    session_id      TEXT,
    content         TEXT NOT NULL,
    -- Nullable until async embedder runs; dimension MUST match embedding_model output
    embedding       vector(768),
    embedding_model TEXT NOT NULL DEFAULT 'sentence-transformers/all-mpnet-base-v2',
    content_hash    TEXT,
    metadata        JSONB NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    version         INTEGER NOT NULL DEFAULT 1
);

COMMENT ON COLUMN agent_memory.embedding IS 'NULL allowed for chunk-first / embed-async pipelines.';
COMMENT ON COLUMN agent_memory.content_hash IS 'Hash of normalized text for re-ingest / drift detection.';
COMMENT ON COLUMN agent_memory.embedding_model IS 'Single model per table generation; change model => migration + re-embed job.';

CREATE INDEX idx_memory_user_created ON agent_memory (user_id, created_at DESC);
CREATE INDEX idx_memory_user_session ON agent_memory (user_id, session_id) WHERE session_id IS NOT NULL;

-- Multilingual baseline: simple text config (plan §4)
CREATE INDEX idx_memory_fts_simple ON agent_memory USING GIN (to_tsvector('simple', content));

-- Optional: English-only leg (drop if you only use simple)
-- CREATE INDEX idx_memory_fts_en ON agent_memory USING GIN (to_tsvector('english', content));

-- JSONB path queries on metadata (tags, source_type, etc.)
CREATE INDEX idx_memory_metadata_path ON agent_memory USING GIN (metadata jsonb_path_ops);

-- Vector index only where embedding present (plan §2)
CREATE INDEX idx_memory_embedding_hnsw ON agent_memory
    USING hnsw (embedding vector_cosine_ops)
    WHERE embedding IS NOT NULL;

-- ---------------------------------------------------------------------------
-- Append-only revisions (plan §3 — Lindy / audit)
-- ---------------------------------------------------------------------------
CREATE TABLE agent_memory_revisions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    memory_id       UUID NOT NULL REFERENCES agent_memory(id) ON DELETE CASCADE,
    content         TEXT NOT NULL,
    metadata        JSONB NOT NULL DEFAULT '{}',
    content_hash    TEXT,
    version_before  INTEGER NOT NULL,
    saved_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_revisions_memory_saved ON agent_memory_revisions (memory_id, saved_at DESC);

-- ---------------------------------------------------------------------------
-- Graph edges (plan §6 — Postgres-first; no Neo4j until needed)
-- ---------------------------------------------------------------------------
CREATE TABLE memory_relations (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id       UUID NOT NULL REFERENCES agent_memory(id) ON DELETE CASCADE,
    target_id       UUID NOT NULL REFERENCES agent_memory(id) ON DELETE CASCADE,
    relation_type   TEXT NOT NULL,
    weight          DOUBLE PRECISION NOT NULL DEFAULT 1.0,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT memory_relations_no_self_loop CHECK (source_id <> target_id)
);

CREATE INDEX idx_relations_source ON memory_relations (source_id);
CREATE INDEX idx_relations_target ON memory_relations (target_id);
CREATE INDEX idx_relations_type ON memory_relations (relation_type);

-- ---------------------------------------------------------------------------
-- updated_at + version bump (plan §3)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION agent_memory_touch()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := NOW();
    IF TG_OP = 'UPDATE' THEN
        IF OLD.content IS DISTINCT FROM NEW.content OR OLD.metadata IS DISTINCT FROM NEW.metadata THEN
            NEW.version := OLD.version + 1;
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_agent_memory_touch
    BEFORE UPDATE ON agent_memory
    FOR EACH ROW
    EXECUTE PROCEDURE agent_memory_touch();

-- ---------------------------------------------------------------------------
-- Revision log on content/metadata change
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION agent_memory_log_revision()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE'
       AND (OLD.content IS DISTINCT FROM NEW.content OR OLD.metadata IS DISTINCT FROM NEW.metadata) THEN
        INSERT INTO agent_memory_revisions (memory_id, content, metadata, content_hash, version_before)
        VALUES (OLD.id, OLD.content, OLD.metadata, OLD.content_hash, OLD.version);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tr_agent_memory_revision
    BEFORE UPDATE ON agent_memory
    FOR EACH ROW
    EXECUTE PROCEDURE agent_memory_log_revision();

-- ---------------------------------------------------------------------------
-- Row-level security (plan §10) — app must SET app.tenant_id per session
-- ---------------------------------------------------------------------------
ALTER TABLE agent_memory ENABLE ROW LEVEL SECURITY;
ALTER TABLE agent_memory_revisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE memory_relations ENABLE ROW LEVEL SECURITY;

CREATE POLICY memory_isolation_select ON agent_memory
    FOR SELECT
    USING (user_id = current_setting('app.tenant_id', true));

CREATE POLICY memory_isolation_insert ON agent_memory
    FOR INSERT
    WITH CHECK (user_id = current_setting('app.tenant_id', true));

CREATE POLICY memory_isolation_update ON agent_memory
    FOR UPDATE
    USING (user_id = current_setting('app.tenant_id', true))
    WITH CHECK (user_id = current_setting('app.tenant_id', true));

CREATE POLICY memory_isolation_delete ON agent_memory
    FOR DELETE
    USING (user_id = current_setting('app.tenant_id', true));

-- Revisions: same tenant as parent row
CREATE POLICY revisions_isolation_select ON agent_memory_revisions
    FOR SELECT
    USING (
        EXISTS (
            SELECT 1 FROM agent_memory m
            WHERE m.id = memory_id AND m.user_id = current_setting('app.tenant_id', true)
        )
    );

CREATE POLICY revisions_isolation_insert ON agent_memory_revisions
    FOR INSERT
    WITH CHECK (
        EXISTS (
            SELECT 1 FROM agent_memory m
            WHERE m.id = memory_id AND m.user_id = current_setting('app.tenant_id', true)
        )
    );

CREATE POLICY revisions_isolation_delete ON agent_memory_revisions
    FOR DELETE
    USING (
        EXISTS (
            SELECT 1 FROM agent_memory m
            WHERE m.id = memory_id AND m.user_id = current_setting('app.tenant_id', true)
        )
    );

-- Relations: both endpoints must belong to tenant
CREATE POLICY relations_isolation_select ON memory_relations
    FOR SELECT
    USING (
        EXISTS (SELECT 1 FROM agent_memory s WHERE s.id = source_id AND s.user_id = current_setting('app.tenant_id', true))
        AND EXISTS (SELECT 1 FROM agent_memory t WHERE t.id = target_id AND t.user_id = current_setting('app.tenant_id', true))
    );

CREATE POLICY relations_isolation_insert ON memory_relations
    FOR INSERT
    WITH CHECK (
        EXISTS (SELECT 1 FROM agent_memory s WHERE s.id = source_id AND s.user_id = current_setting('app.tenant_id', true))
        AND EXISTS (SELECT 1 FROM agent_memory t WHERE t.id = target_id AND t.user_id = current_setting('app.tenant_id', true))
    );

CREATE POLICY relations_isolation_update ON memory_relations
    FOR UPDATE
    USING (
        EXISTS (SELECT 1 FROM agent_memory s WHERE s.id = source_id AND s.user_id = current_setting('app.tenant_id', true))
        AND EXISTS (SELECT 1 FROM agent_memory t WHERE t.id = target_id AND t.user_id = current_setting('app.tenant_id', true))
    );

CREATE POLICY relations_isolation_delete ON memory_relations
    FOR DELETE
    USING (
        EXISTS (SELECT 1 FROM agent_memory s WHERE s.id = source_id AND s.user_id = current_setting('app.tenant_id', true))
        AND EXISTS (SELECT 1 FROM agent_memory t WHERE t.id = target_id AND t.user_id = current_setting('app.tenant_id', true))
    );
