# YouTube transcript queue
<!-- word_count: ~780 -->

WORK only; not Record.

## Purpose

These are the canonical input channels for strategy-notebook. The queue is a rollout list for YouTube transcript automation and metadata capture, not a taxonomy of different roles.

## Canonical input channels

- Dialogue Works
- Daniel Davis Deep Dive
- Glenn Diesen
- Alex Mercouris
- The Duran / Mercouris
- Judging Freedom / Judge Napolitano

## Additional channels

Other channels can be added when useful, but they are not part of the canonical five above.

- The Grayzone
- Breaking Points

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
- Throughput is typically gated by network latency and transcript availability, not local compute, unless a channel falls back to Whisper often.

## Routing rules

- Automated capture writes `raw-input/` only.
- Pages and thread files are composed later in a separate pass.
- Keep the queue selective: substantial episodes only, not completeness-by-default.

## Runner suggestions

Use the generic helper for the majority of cases:

- `scripts/backfill_youtube_channel_raw_input.py`

Thin wrappers exist for the common rollout targets:

- `scripts/backfill_alkorshid_youtube_raw_input.py`
- `scripts/backfill_alexmercouris_youtube_raw_input.py`
- `scripts/backfill_davis_youtube_raw_input.py`
- `scripts/backfill_diesen_youtube_raw_input.py`
- `scripts/backfill_judgingfreedom_youtube_raw_input.py`
- `scripts/backfill_the_duran_youtube_raw_input.py`
- `scripts/backfill_grayzone_youtube_raw_input.py`
- `scripts/backfill_breaking_points_youtube_raw_input.py`

## Rollout note

Roll out one channel at a time so fallback rates and transcript quality can be observed before the queue expands. The list above is the default canonical set, not a mandate to run every channel at once.
