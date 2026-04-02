# Volume VI — Interviews #12 (Jay Shapiro × Jiang)

**Purpose:** Raw YouTube caption storage for **`oErKnj_uyPA`** — interview not hosted on [@PredictiveHistory](https://www.youtube.com/@PredictiveHistory/videos).

**Curated source of truth:** `research/external/work-jiang/lectures/interviews-12-j-shapiro-truth-myth-personal-path.md`

## Fetch / refresh

From repo root (deps: `pip install -e ".[youtube-research]"`):

```bash
python3 scripts/fetch_youtube_channel_transcripts.py \
  --input research/external/work-jiang/intake/urls-vi-12-j-shapiro.txt \
  --output-dir research/external/youtube-channels/vi-12-j-shapiro \
  --limit 1 --sleep 0.5
```

- **`transcripts/*.txt`** — gitignored; provenance header per pipeline.
- **`index.json`**, **`transcript_manifest.json`** — optional commit for dedup state.

## Verbatim markdown (work-jiang)

```bash
python3 scripts/work_jiang/sync_verbatim_transcripts.py --write \
  --only-glob 'interviews-12*' \
  --transcript-root research/external/youtube-channels/vi-12-j-shapiro
```

Output: `research/external/work-jiang/verbatim-transcripts/interviews-12-j-shapiro-truth-myth-personal-path.md` (body often gitignored — see `verbatim-transcripts/README.md`).

## Diff vs operator paste

If you saved an ASR paste from another tool, normalize to plain text and:

```bash
diff -u /path/to/operator-paste.txt research/external/youtube-channels/vi-12-j-shapiro/transcripts/oErKnj_uyPA_*.txt
```

Strip `#` header lines from the `.txt` first if you only want body comparison.
