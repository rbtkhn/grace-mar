# Predictive History — external transcripts

**Purpose:** Operator research corpus (YouTube captions). **Not** part of the companion Record; do not merge into SELF or treat as Voice knowledge.

---

## Work-strategy wiring

**Predictive History** is the **default bulk transcript spine** for **[work-strategy](../../../../docs/skill-work/work-strategy/README.md)** — long-horizon lectures, game-theory arcs, and civilization framing that feed **Perceiver**, **LEARN MODE**, and **current-events** synthesis. **Curated, operator-clean lecture bodies** live under [work-jiang/lectures/](../../work-jiang/lectures/) (see [work-jiang README](../../work-jiang/README.md)); **raw caption pulls** from this folder diff against those before quotations ship.

| Doc / path | Role |
|------------|------|
| [common-inputs.md](../../../../docs/skill-work/work-strategy/common-inputs.md) | **§ Predictive History** — how PH reaches work-strategy vs work-politics |
| [work-strategy/transcripts/README.md](../../work-strategy/transcripts/README.md) | Downstream digests and “copy here or point to PH” ingest rule |
| [current-events-analysis.md](../../../../docs/skill-work/work-strategy/current-events-analysis.md) | Perceiver → hooks → synthesis; PH `.txt` is valid step-1 input |
| [LEARN_MODE_RULES.md](../../../../docs/skill-work/work-strategy/LEARN_MODE_RULES.md) | Extraction format when learning from PH-scale transcripts |
| [daily-brief-jiang-layer.md](../../../../docs/skill-work/work-strategy/daily-brief-jiang-layer.md) | **§1c** slow layer; PH lectures are the usual **work-jiang** book spine |
| [work-jiang-sources.md](../../../../docs/skill-work/work-jiang/work-jiang-sources.md) | Canonical channel URL + index/transcript CLI notes |

---

## Pipeline layout

| Layer | Role |
|-------|------|
| `scripts/youtube_transcripts/` | Library: discovery, tiers, quality, hash, manifest |
| `scripts/fetch_youtube_channel_transcripts.py` | CLI (sync; no Redis required) |
| `scripts/enqueue_youtube_transcripts.py` | Enqueue per-video jobs (RQ + Redis) |
| `scripts/run_transcript_rq_worker.py` | RQ worker process |
| `transcript_manifest.json` | Per-video `content_hash`, `quality`, `source_tier`, timestamps |
| `index.json` | Human/CI-facing index (CLI writes; enqueue does **not** — rebuild after queue jobs) |

**Transcript tiers (in order):** (1) `youtube-transcript-api` timedtext → (2) yt-dlp WebVTT (manual preferred, then auto) → (3) optional `whisper.cpp` on local audio (`WHISPER_CPP_BIN`, `WHISPER_CPP_MODEL`, `--enable-whisper`).

**Quality:** Heuristic score `0..1` per transcript; `TRANSCRIPT_MIN_QUALITY` (default `0.35`) gates low scores; `--keep-low-quality` writes `needs_review` instead of `rejected_low_quality`.

**Dedup:** `content_hash` = SHA-256 of `video_id | pipeline_version | normalized text`. Skip unchanged fetches when manifest hash matches and status was `ok` (unless `--force`).

## Raw transcripts (ASR audit trail)

Fetched caption text is written under [`transcripts/`](transcripts/) as `*.txt`. Those files are **gitignored** to avoid huge commits; keep them **on your machine** (or CI artifact) to diff against curated `work-jiang/lectures/*.md` and to verify lines before they become book quotations.

- **Layout and commands:** [transcripts/README.md](transcripts/README.md)
- **When to verify:** [work-jiang/ASR-VERIFICATION-RUBRIC.md](../../work-jiang/ASR-VERIFICATION-RUBRIC.md) (in-repo path: `research/external/work-jiang/ASR-VERIFICATION-RUBRIC.md`)

You can still commit **`index.json`** and **`transcript_manifest.json`** as lightweight pointers and dedup state.

## Environment variables

| Variable | Purpose |
|----------|---------|
| `GOOGLE_API_KEY` or `YOUTUBE_DATA_API_KEY` | Optional `videos.list` for extra snippet/duration |
| `TRANSCRIPT_MIN_QUALITY` | Default minimum quality (default `0.35`) |
| `REDIS_URL` | RQ enqueue/worker (default `redis://localhost:6379/0`) |
| `WHISPER_CPP_BIN` | Path to whisper.cpp CLI (default `whisper-cli`) |
| `WHISPER_CPP_MODEL` | Path to `.bin` model (required for tier 3) |

## Full channel listing (no downloads)

Human-readable table of **all** videos on the channel (regenerate after new uploads):

- [CHANNEL-VIDEO-INDEX.md](CHANNEL-VIDEO-INDEX.md) — full table: `video_id`, title, duration, watch URL.
- **`index.json`** — same listing in JSON (`--index-only` writes both files).

Refresh listing from YouTube (no transcript downloads):

```bash
python3 scripts/fetch_youtube_channel_transcripts.py --index-only \
  --channel "https://www.youtube.com/@PredictiveHistory/videos" \
  --output-dir research/external/youtube-channels/predictive-history
```

The entry script adds `scripts/` to `sys.path` so `youtube_transcripts` imports resolve.

## Generate / refresh (sync CLI)

From repo root (install deps: `pip install -e ".[youtube-research]"`):

```bash
python3 scripts/fetch_youtube_channel_transcripts.py \
  --channel "https://www.youtube.com/@PredictiveHistory/videos" \
  --output-dir research/external/youtube-channels/predictive-history
```

- **`transcripts/`** — one `.txt` per video (header includes `quality`, `source_tier` when available).
- **`index.json`** — machine-readable rows per video.
- **`transcript_manifest.json`** — dedup + manifest state.

**Inputs:** `--channel` URL (default Predictive History), or `--input path/to/urls.txt` (one channel, playlist, or watch URL per line). **Playlist URLs** are supported.

**Options:** `--limit N`, `--dry-run`, `--index-only`, `--resume` (skip existing `.txt`), `--force`, `--languages`, `--languages-tier2`, `--sleep`, `--enable-whisper`, `--keep-low-quality`, `--max-attempts-listing`.

## Redis + RQ (optional)

Install: `pip install -e ".[transcript-pipeline]"`

Start Redis (example):

```bash
docker compose -f docker-compose.transcripts.yml up -d
export REDIS_URL=redis://127.0.0.1:6379/0
```

Enqueue jobs (one per video):

```bash
python3 scripts/enqueue_youtube_transcripts.py --limit 5
```

Run worker(s):

```bash
python3 scripts/run_transcript_rq_worker.py
```

**Manifest locking:** Jobs take a file lock on `transcript_manifest.json` while updating it (parallel workers serialize manifest writes).

**Rebuild `index.json` after RQ:** run the sync CLI over the same scope with `--resume` so it skips re-downloads but refreshes `index.json`:

```bash
python3 scripts/fetch_youtube_channel_transcripts.py \
  --channel "https://www.youtube.com/@PredictiveHistory/videos" \
  --output-dir research/external/youtube-channels/predictive-history
```

## Daily / cron refresh

Use the same CLI; optional `--since-last-run` is not implemented — use manifest `last_run_utc` in `transcript_manifest.json` manually or re-run `--index-only` to detect new IDs, then fetch.

## See also

- **[work-strategy](../../../../docs/skill-work/work-strategy/README.md)** — territory README; **Predictive History** is indexed as **work-strategy–first** in [common-inputs.md § PH](../../../../docs/skill-work/work-strategy/common-inputs.md).
- **[tucker-carlson-book](../tucker-carlson-book/README.md)** — curated Tucker Carlson Network transcript volume (operator book; sibling under `youtube-channels/`).

## Git

Transcript text can be large; by default **`transcripts/*.txt` is gitignored**. Commit **`index.json`** if you want a pointer without blobs, or remove the ignore rule if you intentionally version text.

Respect YouTube’s Terms of Service and creator rights; use for analysis, not republication, unless you have rights to do so. Whisper tier downloads audio locally; ensure your use complies with copyright and platform rules.
