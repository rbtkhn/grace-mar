# Strategy notebook — trace and receipts contract (v1)

WORK only; not Record. **Canonical** judgment lives in Git Markdown (expert `thread.md`, `strategy-page` fences, `chapters/…/days.md`). This contract describes **append-only machine receipts** for notebook-affecting commands so runs are **inspectable** and **separate** from [FOLD-LEARNING.md](FOLD-LEARNING.md) / `strategy-fold-events.jsonl` and [artifacts/work-strategy/strategy-observability.json](../../../../artifacts/work-strategy/strategy-observability.json) (separate channels; optional timestamp cross-link only).

## Receipt storage

- **Default path:** `artifacts/work-strategy/strategy-notebook/receipts/strategy-notebook-receipts.jsonl` (directory **gitignored**; regen optional).
- **Format:** one JSON object per line (JSONL), UTF-8, append-only.
- **Rebuild:** not required for correctness of the notebook; deleting receipts loses audit trail only.

## Required fields (v1)

| Field | Type | Description |
|-------|------|-------------|
| `ts` | string | ISO-8601 UTC timestamp when the run finished. |
| `entrypoint` | string | Script name, e.g. `strategy_page`, `compile_strategy_view`. |
| `page_operation` | string | See [STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md](STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md). |
| `status` | string | `ok` \| `failed` \| `dry_run`. |
| `sources_read` | array of string | Repo-relative paths read ( POSIX `/` ). |
| `outputs_touched` | array of string | Repo-relative paths written or would be written. |
| `decision` | string | Short human line (e.g. `inserted new strategy-page scaffolds`, `wrote bundle`). |

## Optional fields (v1)

| Field | Type | Description |
|-------|------|-------------|
| `model` | string or null | Model id if an LLM was used; else `null`. |
| `provider` | string or null | Provider if applicable. |
| `token_count` | number or null | If available. |
| `cost_usd` | number or null | If available. |
| `warning_flags` | array of string | e.g. `["missing_thread_file"]` |
| `details` | object | Free-form: `page_id`, `expert_ids`, `recipe_id`, etc. |
| `error` | string or null | Set when `status` is `failed`. |

## OpenTelemetry / GenAI alignment (non-blocking)

v1 receipts are **file-local**. Field names are chosen so a future adapter can map to OpenTelemetry **GenAI** and **MCP** semantic conventions (tool spans, optional attributes) without changing Markdown truth.

## Doctrine

- **No promotion** to Record, SELF, EVIDENCE, or `bot/prompt.py` from receipts. See [runtime-vs-record.md](../../../runtime-vs-record.md), [AGENTS.md](../../../../AGENTS.md).

## Links

- [STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md](STRATEGY-NOTEBOOK-PAGE-UPDATE-CONTRACT.md) — `PageOperation` values
- [PAGE-CONTRACT.md](PAGE-CONTRACT.md) — page vs thread
- [STRATEGY-NOTEBOOK-ARCHITECTURE.md](STRATEGY-NOTEBOOK-ARCHITECTURE.md) — default operating path
