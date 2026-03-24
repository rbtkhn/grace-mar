# Raw transcript cache (Predictive History)

This directory holds **verbatim YouTube caption / ASR pulls** — one `.txt` per video when you run the sync fetch CLI.

## Git

`*.txt` files here are **gitignored** (see [../.gitignore](../.gitignore)). That keeps the repo small; you still get an audit trail **on disk** for ASR checks and diffs against curated lectures.

**Do commit** when useful for the team:

- [../index.json](../index.json) — channel listing (optional but common)
- [../transcript_manifest.json](../transcript_manifest.json) — dedup hashes and fetch status
- [../CHANNEL-VIDEO-INDEX.md](../CHANNEL-VIDEO-INDEX.md) — human-readable index

## Populate locally

From repo root (deps: `pip install -e ".[youtube-research]"`):

```bash
python3 scripts/fetch_youtube_channel_transcripts.py \
  --channel "https://www.youtube.com/@PredictiveHistory/videos" \
  --output-dir research/external/youtube-channels/predictive-history \
  --resume --sleep 0.5
```

- **`--resume`** — skip videos that already have a transcript file.
- **`--force`** — refetch even when the manifest says content unchanged.
- **`--index-only`** — updates `index.json` / `CHANNEL-VIDEO-INDEX.md` only (no `.txt` here).

Single-video fetch (e.g. after ingest with `--fetch`):

```bash
python3 scripts/fetch_youtube_channel_transcripts.py \
  --input /path/to/one-url-per-line.txt \
  --output-dir research/external/youtube-channels/predictive-history \
  --limit 1 --resume
```

## Using with work-jiang

See [ASR-VERIFICATION-RUBRIC.md](../../../external/work-jiang/ASR-VERIFICATION-RUBRIC.md) and [WORKFLOW-transcripts.md](../../../external/work-jiang/WORKFLOW-transcripts.md): compare **raw `.txt`** ↔ **curated `lectures/*.md`** for names, numbers, and anything promoted to `metadata/quotes.yaml`.
