# Predictive History — external transcripts

**Purpose:** Operator research corpus (YouTube captions). **Not** part of the companion Record; do not merge into SELF or treat as Voice knowledge.

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

## Generate / refresh

From repo root (install deps first: `pip install -e ".[youtube-research]"`):

```bash
python3 scripts/fetch_youtube_channel_transcripts.py \
  --channel "https://www.youtube.com/@PredictiveHistory/videos" \
  --output-dir research/external/youtube-channels/predictive-history
```

- **`transcripts/`** — one `.txt` per video (metadata header + plain text).
- **`index.json`** — machine-readable manifest with status per video (after full fetch) or listing-only rows after `--index-only`.

Options: `--limit N` (test), `--dry-run` (print TSV to stdout only), `--index-only` (write `index.json` + `CHANNEL-VIDEO-INDEX.md`), `--resume` (skip existing files), `--languages en,zh-CN`, `--sleep 0.5`.

## Git

Transcript text can be large; by default **`transcripts/*.txt` is gitignored**. Commit **`index.json`** if you want a pointer without blobs, or remove the ignore rule if you intentionally version text.

Respect YouTube’s Terms of Service and creator rights; use for analysis, not republication, unless you have rights to do so.
