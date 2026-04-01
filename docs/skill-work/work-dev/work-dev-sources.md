# work-dev — sources

YouTube channels, podcasts, and newsletters the operator tracks for **work-dev framing** (integration, offers, partner vocabulary). **Not** Record truth and **not** a substitute for [integration-status.md](integration-status.md) — see [external-signals.md](external-signals.md).

**Per-video registry (titles + canonical watch URLs, machine-readable JSON):** [research/external/work-dev/youtube-indexes/](../../../research/external/work-dev/youtube-indexes/) — one folder per channel; refresh listing with `fetch_youtube_channel_transcripts.py --index-only` (see that README). Each channel has **`ingestion.json`**: operator marks whether an episode has been **manually ingested** (digest/transcript in-repo) and links artifact paths; `render_youtube_work_dev_catalog.py` writes **`CHANNEL-CATALOG.md`** and **`episode-catalog.json`** with an `ingested` field per video. Keeps provenance for long-horizon research. The table below stays **channel-level** so this page stays scannable.

**Principle:** [Work modules — authorized sources lists](../work-modules-sources-principle.md).

| Source | URL | Notes |
|--------|-----|-------|
| AI News & Strategy Daily (Nate B Jones) | https://www.youtube.com/@NateBJones | AI news and strategy with a builder / PM / career lens; **digest (seven skills / K-shaped market):** [transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md](../../../research/external/work-dev/transcripts/nate-b-jones-ai-job-market-seven-skills-2026.md); **operator lane (job log / worksheets, not Record):** [work-career/README.md](../work-career/README.md) |
| Peter H. Diamandis | https://www.youtube.com/@peterdiamandis | Long-horizon exponential and moonshot discourse |
| The Innermost Loop (Dr. Alex Wissner-Gross) | https://theinnermostloop.substack.com/ | Substack — high-velocity intelligence / event-horizon curation; by Dr. Alex Wissner-Gross |

Add rows above or below as you like.

**Video list (titles + publication dates):** from repo root, with `yt-dlp` installed (`pip install -e ".[youtube-research]"`), run  
`python3 scripts/fetch_youtube_channel_transcripts.py --channel "<URL>/videos" --index-only --enrich-metadata -o <output-dir>`  
Outputs `CHANNEL-VIDEO-INDEX.md` and `index.json`. Use `--enrich-metadata` so dates are filled (flat listing alone often omits them).

**Parallel (work-politics):** [../work-politics/work-politics-sources.md](../work-politics/work-politics-sources.md)

**BrewMind (Philippines pilot):** These feeds are also bundled for **micro-lesson / curriculum depth** in [../work-xavier/brewmind-philippines-onboarding-guide.md](../work-xavier/brewmind-philippines-onboarding-guide.md) § *Operator depth — work-dev sources* — PH-facing AI content online is thin; **canonical list stays this file**.
