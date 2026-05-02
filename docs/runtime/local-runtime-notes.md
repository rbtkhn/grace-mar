# Local Runtime Notes

**Status:** Doc-first orientation. No health-check script or dashboard wiring in v1.

Local runtimes are useful when they make Grace-Mar more private, rebuildable, inspectable, or fast. They should complement the existing repository substrate, not become hidden owners of memory.

## Runtime Categories

| Category | Typical role | Notes |
|----------|--------------|-------|
| Ollama-style daily local | Routine local chat, drafts, summaries, small private loops | Good default for low-stakes local work if endpoint is available |
| LM Studio / eval local | Manual local model comparison and prompt/eval experiments | Useful for operator testing before formal routing |
| vLLM / server local | Higher-throughput local serving | Use when multiple tools need a shared endpoint |
| Embedding endpoint | Local vector indexing and retrieval experiments | Keep indexes rebuildable from source text |
| Cloud fallback | Frontier reasoning, hard coding, current research with citations | Treat as visitor; require receipts when it influences durable decisions |

## Manual Checks

These are examples, not an enforced workflow:

```powershell
# Ollama-style endpoint
Invoke-RestMethod http://127.0.0.1:11434/api/tags

# Generic OpenAI-compatible local endpoint
Invoke-RestMethod http://127.0.0.1:1234/v1/models
```

Do not wire these into coffee, bridge, or dashboards until the preferred local runtime is stable enough to avoid false alarms.

## Boundaries

- Local runtime memory is not Grace-Mar memory.
- Local indexes should be rebuildable from governed source files.
- Runtime logs and receipts may inform WORK decisions, but Record changes still require the gate.
- Secrets and provider credentials stay outside committed docs.
