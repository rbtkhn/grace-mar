# Optional offload: GPU, APIs, and cost (work-jiang / transcripts)

Default paths stay **local CPU** and **no paid API**. Use these only when you opt in.

## Environment variables

| Variable | Values | Purpose |
|----------|--------|---------|
| `TRANSCRIPT_WHISPER_BACKEND` | `local` (default) \| `openai` \| other | Where ASR runs: local whisper.cpp vs remote API. Wire in `scripts/fetch_youtube_channel_transcripts.py` / worker when implemented. |
| `WORK_JIANG_ANALYSIS_LLM` | `local` \| `openai` \| other | Future: which backend generates `-analysis.json` sidecars. |
| `WORK_JIANG_REGISTRY_PREFER_SQLITE` | unset \| `1` | When `1`, `link_supporting_registries.py` reads prediction/divergence **payloads** from `registry/work_jiang_metrics.sqlite` (run `rebuild_registry_db.py` first). JSONL remains canonical for edits. |
| `WORK_JIANG_EXTRACTOR_SERIES` | e.g. `geo-strategy` | Force extractor plugin for dispatch smoke tests (overrides `source_id` prefix rules). |

## Docker Compose GPU profile

Optional NVIDIA runtime for whisper / local LLM containers:

```bash
docker compose -f docker-compose.transcripts.yml --profile gpu up -d whisper-gpu
```

Requires Linux host, `nvidia-container-toolkit`, and an image suited to your workload (the bundled service is a **placeholder** CUDA runtime).

## Cost logging

- Work-jiang ledger: `python3 scripts/work_jiang/log_operator_compute.py --tokens 1200 --backend openai`
- Optional mirror into companion energy ledger: add `--mirror-grace-mar-ledger` (operator lane; not Record until gated).

See also [WORKFLOW-transcripts.md](WORKFLOW-transcripts.md) and [docs/skill-work/work-jiang/extractors.md](../../docs/skill-work/work-jiang/extractors.md).
