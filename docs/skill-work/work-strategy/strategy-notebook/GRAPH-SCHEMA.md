# Strategy notebook — derived graph schema (v1)
<!-- word_count: 213 -->

WORK only; not Record. The graph is **rebuilt** from expert `thread.md` content via [strategy_page_reader.py](../../../../scripts/strategy_page_reader.py); do not hand-edit [graph.json](../../../../artifacts/work-strategy/strategy-notebook/graph.json).

## `graph.json` top level

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | e.g. `1.0.0-strategy-notebook-graph` |
| `generated_at` | string | ISO-8601 UTC when built |
| `notebook_dir` | string | Repo-relative directory scanned |
| `nodes` | array | Node objects (see below) |
| `edges` | array | Edge objects (see below) |

## Node types (v1)

| `type` | `id` pattern | Other fields |
|--------|----------------|-------------|
| `page` | Unique per **appearance**: `{expert_id}::{page_id}` | `page_id`, `expert_id`, `date`, `watch` (may be empty) |
| `expert` | `expert:{expert_id}` | — |
| `watch` | `watch:{watch_id}` | — |

## Edge types (v1)

| `type` | `from` | `to` |
|--------|--------|------|
| `belongs_to_expert` | page id | `expert:…` |
| `belongs_to_watch` | page id (only if `watch` non-empty) | `watch:…` |

## Generated views (same builder)

- **`views/watch-clusters.json`**: `Record<string, string[]>` — watch id → list of `page_id` (deduped) appearing under that watch.
- **`views/expert-convergence.json`**: `Record<string, string[]>` — `page_id` **→** expert ids when the same `page_id` appears in more than one expert thread (polyphony / duplicate blocks).

## Rebuild

```bash
python3 scripts/build_strategy_notebook_graph.py
python3 scripts/build_strategy_notebook_graph.py --notebook-dir docs/skill-work/work-strategy/strategy-notebook
```

## Links

- [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md)
- [PAGE-CONTRACT.md](PAGE-CONTRACT.md)
- [STRATEGY-NOTEBOOK-TRACE-CONTRACT.md](STRATEGY-NOTEBOOK-TRACE-CONTRACT.md)
