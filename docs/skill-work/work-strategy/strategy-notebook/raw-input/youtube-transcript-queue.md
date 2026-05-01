# YouTube transcript queue
<!-- word_count: ~920 -->

WORK only; not Record.

## Purpose

This queue is the graph-first source registry for YouTube transcript automation. The goal is not to ingest every upload on every channel. The goal is to capture substantial episodes from the channels that sit at the center of the interview network, then route the resulting `raw-input/` files into expert lanes only when that routing is meaningful.

## Queue order

Priority balances graph centrality, transcript volume, and ease of automation.

| Rank | Channel | Primary graph role | Default routing | Automation posture | Compute posture |
|---:|---|---|---|---|---|
| 1 | Dialogue Works | Host hub | `thread:alkorshid` | Existing direct lane; thin wrapper over the generic helper | Cheap, caption-first |
| 2 | Judging Freedom | Host hub | threadless until guest routing is clear | Discovery hub; capture substantial episodes, route later | Cheap to moderate |
| 3 | The Duran | Host hub | threadless until speaker routing is clear | Discovery hub with recurring Mercouris-centered episodes | Cheap to moderate |
| 4 | Daniel Davis Deep Dive | Direct expert lane | `thread:davis` | Direct lane; easiest expert endpoint after Dialogue Works | Cheap, caption-first |
| 5 | Glenn Diesen | Direct expert lane | `thread:diesen` | Direct lane; useful both as speaker and bridge node | Cheap, caption-first |
| 6 | The Grayzone | Shared hub | threadless until guest routing is clear | Shared Blumenthal / Maté network; good graph node, not a single lane | Cheap to moderate |
| 7 | Breaking Points | Shared hub | threadless until guest routing is clear | High-volume hub; selective capture only, because many clips are not worth preserving | Moderate |

## Resource estimate

The transcript pipeline is efficient as long as the common path stays caption-first:

| Tier | What it uses | Expected cost |
|---|---|---|
| Tier 1 | `youtube-transcript-api` | Low CPU, low memory, mostly network-bound |
| Tier 2 | `yt-dlp` subtitle download | Still cheap; a little slower and more variable than Tier 1 |
| Tier 3 | Whisper fallback | CPU-heavy; use only when captions/subtitles fail |

Rule of thumb:
- Tier 1 and Tier 2 should make the queue feel lightweight.
- Whisper should remain the exception path, not the default path.
- Throughput is typically gated by network latency and transcript availability, not local compute, unless a hub falls back to Whisper often.

## Routing rules

- Automated capture writes `raw-input/` only.
- Pages and thread files are composed later in a separate pass.
- Host hubs may omit `thread:` when a single expert lane is not the right routing target yet.
- Direct expert lanes should use `thread:` by default.
- Keep the queue selective: substantial episodes only, not completeness-by-default.

## Runner suggestions

Use the generic helper for the majority of cases:

- `scripts/backfill_youtube_channel_raw_input.py`

Thin wrappers exist for the first direct lanes and the major hubs:

- `scripts/backfill_alkorshid_youtube_raw_input.py`
- `scripts/backfill_davis_youtube_raw_input.py`
- `scripts/backfill_diesen_youtube_raw_input.py`
- `scripts/backfill_judgingfreedom_youtube_raw_input.py`
- `scripts/backfill_the_duran_youtube_raw_input.py`
- `scripts/backfill_grayzone_youtube_raw_input.py`
- `scripts/backfill_breaking_points_youtube_raw_input.py`

## Rollout note

Roll out one hub at a time so fallback rates and transcript quality can be observed before the queue expands. The queue order above is the default graph-first ordering, not a mandate to run every channel at once.
