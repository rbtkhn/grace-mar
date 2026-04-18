# Chunked retrieval layer

Lightweight, non-canonical chunk generation and chunk-aware search for large documents in Grace-Mar.

## What it is

A chunk generation script (`scripts/runtime/generate_chunks.py`) that splits large non-canonical markdown files into paragraph-boundary chunks, writes chunk metadata as JSONL under `runtime/chunks/`, and integrates with `hybrid_retrieve.py` so retrieval can score individual sections instead of whole files.

## What it is NOT

- **Not Record.** Does not touch SELF, EVIDENCE, SKILLS, SELF-LIBRARY, or `recursion-gate.md`.
- **Not promotion logic.** Does not stage candidates, auto-merge, or mutate canonical surfaces.
- **Not a replacement** for source files — chunks are derived retrieval aids, rebuildable at any time.
- **Not a vector database.** No embedding model, no vector store, no external indexing service.
- **Not an NLP pipeline.** Uses simple paragraph-boundary splitting with heading context.

## Why chunk?

When `hybrid_retrieve.py` searches a 155 KB file (e.g. strategy-notebook `days.md`), TF-IDF cosine over the whole file dilutes term relevance across thousands of tokens, and the snippet always comes from the first 300 characters. Chunking lets retrieval:

- Score the **relevant section** of a large file
- Return a **meaningful snippet** from the matching chunk
- Report **exact line ranges** and **section headings** for traceability

## Chunking strategy (v1)

- **Split on blank-line paragraph boundaries** (double newline)
- **Combine adjacent paragraphs** into chunks targeting ~1200 chars (range 800-2000)
- **Preserve markdown heading context**: the last `#`/`##`/`###`/`####` heading above each chunk is recorded as `section_hint`
- **Record line ranges**: `start_line` and `end_line` (1-based) for source traceability
- **Source hash**: first 12 hex of SHA-256 of full source content for staleness detection
- **No overlap** in v1 — paragraph boundaries are clean enough

## Chunk record shape

```json
{
  "chunk_id": "chk_a1b2c3d4_0003",
  "source_path": "docs/skill-work/work-strategy/strategy-notebook/chapters/2026-04/days.md",
  "source_hash": "a1b2c3d4e5f6",
  "chunk_index": 3,
  "total_chunks": 12,
  "start_line": 45,
  "end_line": 78,
  "section_hint": "## 2026-04-14",
  "content": "...(chunk text)...",
  "char_count": 1180,
  "generated_at": "2026-04-18T06:30:00Z"
}
```

## Surfaces (v1)

| Surface | Source directory | Chunked |
|---|---|---|
| `artifact_lookup` | `artifacts/` | Yes — `.md` and `.txt` files over 4 KB |
| `notebook_lookup` | `docs/skill-work/work-strategy/strategy-notebook/chapters/` | Yes — `.md` and `.txt` files over 4 KB |
| `prepared_context` | `runtime/observations/index.jsonl` | No — already entry-level via observation store |
| `evidence_lookup` | `users/<id>/self-archive.md` | No — already entry-level via evidence parser |

## Usage

### Generate chunks

```bash
# Chunk one surface
python scripts/runtime/generate_chunks.py --surface notebook_lookup

# Chunk all supported surfaces
python scripts/runtime/generate_chunks.py --all

# Chunk a single file
python scripts/runtime/generate_chunks.py --path path/to/large-file.md

# Lower the size threshold (default 4 KB)
python scripts/runtime/generate_chunks.py --surface artifact_lookup --min-size 2048
```

### Search with chunks

Once chunks are generated, `hybrid_retrieve.py` automatically uses them — no extra flags needed.

```bash
python scripts/runtime/hybrid_retrieve.py \
  --surface notebook_lookup \
  --query "Iran sanctions framing" \
  --json
```

Results from chunked files include line ranges and section hints:

```json
{
  "path": "docs/skill-work/.../days.md:45-78",
  "label": "## 2026-04-14",
  "meta": {
    "chunk_id": "chk_a1b2c3d4_0003",
    "chunk_index": 3,
    "total_chunks": 12,
    "section_hint": "## 2026-04-14",
    "source_path": "docs/skill-work/.../days.md"
  }
}
```

### Fallback behavior

Files that are too small to chunk (under the size threshold) or that don't have generated chunks are scored as whole files, exactly as before. Chunk-aware search and whole-file search results are merged and ranked together.

## Storage

- **Location:** `runtime/chunks/<surface>/<filename>.chunks.jsonl`
- **Gitignored:** Yes — operator-local, rebuildable data.
- **Path resolution:** `scripts/runtime/ledger_paths.py` (`chunks_dir_root()`, `chunks_dir(surface)`).

## Relationship to other systems

- **Hybrid retrieval** (PR 2): Chunk-aware search is integrated into `_scan_md_files` in `hybrid_retrieve.py`. When chunks are available, the function scores chunks instead of whole files for those sources.
- **Retrieval-miss ledger** (PR 1): Chunking can reduce `aggregation_failure` (relevant content scattered across a large file) and `stale_ranking` (relevant section buried in a large document). Miss records from chunked surfaces include chunk metadata for diagnosis.
- **Runtime conventions**: Chunk indexes follow the same `runtime/` pattern as observations and retrieval-misses — gitignored, non-canonical, rebuildable.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/runtime/generate_chunks.py` | Generate chunk indexes for large files |
| `scripts/runtime/chunk_store.py` | Read-only chunk loading module |
| `scripts/runtime/hybrid_retrieve.py` | Chunk-aware hybrid search (automatic when chunks exist) |

## PR 4 recommendation (not implemented)

Connected-context hints: when a chunk hit is returned, also surface sibling chunks (`chunk_index` +/- 1) as context hints, so the operator can expand the retrieval window without re-running the full search.
