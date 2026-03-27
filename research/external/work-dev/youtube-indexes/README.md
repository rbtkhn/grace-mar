# work-dev — YouTube video indexes (per-episode registry)

**Purpose:** Keep a **durable, machine-readable** list of videos that informed early **work-dev** thinking — one row per video (`video_id`, `title`, `url`, duration, optional `upload_date`). Useful for provenance, re-fetching transcripts later, and **long-horizon research** (e.g. studying how this system’s external inputs evolved).

**Not Record truth.** These files are operator research inventory, not SELF or Voice knowledge. Channel home pages stay in [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md); this tree holds **episode-level** detail.

## Layout

| Channel (slug) | Listing (yt-dlp) | Manual ingestion state | Merged view (human + ML) |
|----------------|------------------|-------------------------|---------------------------|
| Nate B Jones | [nate-b-jones/CHANNEL-VIDEO-INDEX.md](nate-b-jones/CHANNEL-VIDEO-INDEX.md), [index.json](nate-b-jones/index.json) | [nate-b-jones/ingestion.json](nate-b-jones/ingestion.json) | [nate-b-jones/CHANNEL-CATALOG.md](nate-b-jones/CHANNEL-CATALOG.md), [episode-catalog.json](nate-b-jones/episode-catalog.json) |
| Peter H. Diamandis | [peter-h-diamandis/CHANNEL-VIDEO-INDEX.md](peter-h-diamandis/CHANNEL-VIDEO-INDEX.md), [index.json](peter-h-diamandis/index.json) | [peter-h-diamandis/ingestion.json](peter-h-diamandis/ingestion.json) | [peter-h-diamandis/CHANNEL-CATALOG.md](peter-h-diamandis/CHANNEL-CATALOG.md), [episode-catalog.json](peter-h-diamandis/episode-catalog.json) |

**Ingestion schema:** [ingestion.schema.json](ingestion.schema.json) — `by_video_id` maps YouTube `video_id` to `{ "ingested": bool, "artifacts": [repo-relative paths], "ingested_at_utc": optional }`. The fetch script **never** overwrites `ingestion.json`; only operators edit it after manually adding a digest or transcript.

**Merged catalog:** [scripts/render_youtube_work_dev_catalog.py](../../../scripts/render_youtube_work_dev_catalog.py) joins `index.json` + `ingestion.json` into `CHANNEL-CATALOG.md` (table with an **ingested** column) and `episode-catalog.json` (one object per video including `ingested` and `ingestion_artifacts` for downstream tooling).

## How it was generated

From repo root (requires `yt-dlp`; see [work-dev-sources.md](../../../docs/skill-work/work-dev/work-dev-sources.md)):

```bash
# Latest N videos per channel (fast listing; upload_date often empty)
python3 scripts/fetch_youtube_channel_transcripts.py --index-only \
  --channel "https://www.youtube.com/@NateBJones/videos" \
  -o research/external/work-dev/youtube-indexes/nate-b-jones --limit 30

python3 scripts/fetch_youtube_channel_transcripts.py --index-only \
  --channel "https://www.youtube.com/@peterdiamandis/videos" \
  -o research/external/work-dev/youtube-indexes/peter-h-diamandis --limit 30
```

**Full channel history:** omit `--limit` (larger repo footprint). **Fill `upload_date`:** add `--enrich-metadata` (slower; one metadata pull per video).

## Cross-links (curated digests)

When a transcript or memo exists in [../transcripts/](../transcripts/), record it in that channel’s `ingestion.json` for the matching `video_id`, then re-run **render**. Examples: [nate-b-jones-google-stitch-design-markdown-meeting-transcript-2026.txt](../transcripts/nate-b-jones-google-stitch-design-markdown-meeting-transcript-2026.txt) ↔ `CDClFY-R0dI` (*A Markdown File Just Replaced Your Most Expensive Design Meeting…*); digest [nate-b-jones-ai-job-market-seven-skills-2026.md](../transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md) ↔ `4cuT-LKcmWs`. See [nate-b-jones/CHANNEL-CATALOG.md](nate-b-jones/CHANNEL-CATALOG.md).

## Refresh policy

1. Re-run **fetch** when you want an updated channel listing; commit `index.json` and `CHANNEL-VIDEO-INDEX.md` together.
2. After you **manually ingest** an episode (new file under [transcripts/](../transcripts/) or similar), add or update that `video_id` in the channel’s `ingestion.json`.
3. Re-run **render** so the merged artifacts stay in sync:

```bash
python3 scripts/render_youtube_work_dev_catalog.py research/external/work-dev/youtube-indexes/nate-b-jones
python3 scripts/render_youtube_work_dev_catalog.py research/external/work-dev/youtube-indexes/peter-h-diamandis
```

Commit `ingestion.json` plus `CHANNEL-CATALOG.md` and `episode-catalog.json` together when you change ingestion state.

Respect YouTube terms of use; use listing/index mode for inventory, transcripts only where appropriate.
