# Inference Modes

Grace-Mar supports three LLM provider backends. Set `LLM_PROVIDER` in your `.env` to select one.

## Providers

| Provider | `LLM_PROVIDER` | Status | Voice chat | Analyst | Lookup | Transcription |
|----------|----------------|--------|------------|---------|--------|---------------|
| OpenAI   | `openai` (default) | Production | Yes | Yes | Yes | Yes (Whisper) |
| Ollama   | `ollama` | Functional | Yes | Yes | Yes | No |
| Edge     | `edge` | Stub | No | No | No | No |

## OpenAI (default)

Standard cloud API. Requires `OPENAI_API_KEY`.

```
LLM_PROVIDER=openai
OPENAI_MODEL=gpt-4o
OPENAI_ANALYST_MODEL=gpt-4o-mini
```

## Ollama (local inference)

Local server with an OpenAI-compatible API. No API key required. Privacy-preserving: all inference stays on-device.

```
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=gemma3:4b
OLLAMA_ANALYST_MODEL=gemma3:4b
```

### Setup

1. Install Ollama: https://ollama.com
2. Pull a model: `ollama pull gemma3:4b`
3. Start the server: `ollama serve`
4. Set env vars as above

### Model resolution

When `LLM_PROVIDER=ollama`, `_resolve_model()` in `bot/core.py` maps OpenAI model names to Ollama equivalents:
- Main chat uses `OLLAMA_MODEL` (falls back to `OPENAI_MODEL` if unset)
- Analyst pipeline uses `OLLAMA_ANALYST_MODEL` (falls back to `OLLAMA_MODEL`, then `OPENAI_ANALYST_MODEL`)

### Graceful degradation

| Feature | Behavior on Ollama |
|---------|-------------------|
| Voice transcription | Disabled (Whisper requires OpenAI). Returns `None`; callers handle gracefully. |
| Context window | Model-dependent. Gemma 3 4B: 8K tokens. May truncate long conversations. |
| Analyst quality | Lower than GPT-4o-mini on structured YAML extraction. Expect more `NONE` responses. |
| Lexile control | Prompt-enforced; smaller models may drift above ceiling more often. |
| Constitutional pass | Uses the same local model; quality depends on model capability. |

### Recommended local models

| Model | Size | Context | Quality | Notes |
|-------|------|---------|---------|-------|
| `gemma3:4b` | 2.4 GB | 8K | Good | Fast, decent for Voice emulation |
| `gemma3:12b` | 7.3 GB | 8K | Better | Stronger analyst and boundary adherence |
| `llama3.2:3b` | 2 GB | 128K | Moderate | Large context but lower reasoning |
| `mistral:7b` | 4.1 GB | 32K | Good | Balanced quality and speed |

## Edge (Google AI Edge SDK)

Reserved for Phase 4 — on-device inference via Gemini Nano on Android (ML Kit GenAI / AICore) or iOS equivalent. Not yet wired in `bot/core.py`.

For desktop local-first testing, use `LLM_PROVIDER=ollama` with a Gemma model instead. See `scripts/inference_providers/edge_provider.py` for the provider stub and contract.

```
LLM_PROVIDER=edge
EDGE_MODEL=gemini-nano-4b
```

## Provider architecture

```
bot/core.py
  _get_client()         → OpenAI-compatible client (openai or ollama)
  _resolve_model(name)  → maps model names per provider

scripts/inference_providers/
  base.py               → InferenceProvider ABC + InferenceResult
  openai_provider.py    → OpenAI wrapper (not used by core.py yet)
  ollama_provider.py    → Ollama wrapper (not used by core.py yet)
  edge_provider.py      → Stub (NotImplementedError)
```

The `scripts/inference_providers/` module defines a clean provider interface (`InferenceProvider`) that future versions of `bot/core.py` may adopt for unified routing. Currently, `core.py` uses the OpenAI SDK directly with `_get_client()` branching on `LLM_PROVIDER`.

## Boundary regression

After switching providers or models, run the boundary regression check to verify abstention behavior hasn't degraded:

```bash
python3 scripts/runtime/boundary_regression.py          # fast set (5 probes)
python3 scripts/runtime/boundary_regression.py --full    # all 27 probes
```

See `scripts/counterfactual_pack/probes.json` for the probe definitions.
