# Verbatim transcripts (lightly cleaned)

One markdown file per curated lecture in [`../lectures/`](../lectures/), **same basename**, built from **raw YouTube caption** files under [`../../youtube-channels/predictive-history/transcripts/`](../../youtube-channels/predictive-history/transcripts/README.md).

**Purpose:** Diff this layer against curated lectures and against `## Full transcript` when checking ASR. See [`../ASR-VERIFICATION-RUBRIC.md`](../ASR-VERIFICATION-RUBRIC.md) and [`../WORKFLOW-transcripts.md`](../WORKFLOW-transcripts.md).

## Generate

1. Fetch or refresh raw `.txt` (gitignored in the channel repo) — [predictive-history README](../../youtube-channels/predictive-history/README.md).
2. From repo root:

   ```bash
   python3 scripts/work_jiang/sync_verbatim_transcripts.py --dry-run
   python3 scripts/work_jiang/sync_verbatim_transcripts.py --write
   ```

   Default is dry-run when `--write` is omitted; `--dry-run` is explicit (same mode). Do not combine `--write` and `--dry-run`.

   Use `--force` to overwrite existing files. Use `--only-glob 'civilization-31*'` to scope. Use `--fail-on-missing-raw` in CI only if raw transcripts are present in the environment.

**Git:** `*.md` in this directory is ignored except this `README.md`, so generated bodies stay local unless you remove the ignore rule to commit them (check size with `du -sh .` first).
