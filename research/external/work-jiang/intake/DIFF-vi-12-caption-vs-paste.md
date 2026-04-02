# vi-12 — Diff YouTube captions vs operator ASR paste

**Video:** [oErKnj_uyPA](https://www.youtube.com/watch?v=oErKnj_uyPA)

## Canonical machine pull (repo)

After running the fetch in [`youtube-channels/vi-12-j-shapiro/README.md`](../../youtube-channels/vi-12-j-shapiro/README.md), raw text lives at:

`research/external/youtube-channels/vi-12-j-shapiro/transcripts/oErKnj_uyPA_*.txt`  
*(gitignored — present on machine after fetch; filename suffix matches YouTube title.)*

**Spot-check (2026-04-02):** First spoken line in the tier-1 pull matches the operator session paste (`That day also uh is when a blood moon…`), so the paste and YouTube captions are likely the same track; still run a full diff before merging curated dialogue.

## Compare to a saved paste

1. Save your alternate transcript as plain text, e.g. `tmp/vi-12-operator-paste.txt` (no markdown fences).
2. Strip the `# …` header from the fetched `.txt` (lines starting with `#` until the first blank line after headers).
3. Optional: normalize `>>` speaker hints and line breaks with `sed`/`perl` so `diff` is meaningful.

```bash
# Example: body-only from fetch (adjust path to your local .txt)
tail -n +11 "research/external/youtube-channels/vi-12-j-shapiro/transcripts/oErKnj_uyPA_"*.txt > /tmp/vi-12-youtube-body.txt

diff -u /tmp/vi-12-operator-paste.txt /tmp/vi-12-youtube-body.txt | less
```

## Lightly cleaned layer

Verbatim markdown (local, usually gitignored):

`python3 scripts/work_jiang/sync_verbatim_transcripts.py --write --only-glob 'interviews-12*' --transcript-root research/external/youtube-channels/vi-12-j-shapiro`

→ `verbatim-transcripts/interviews-12-j-shapiro-truth-myth-personal-path.md`

Use that for **editorial** diff against `lectures/…/## Full transcript` once you merge speaker labels.
