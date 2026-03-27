#!/usr/bin/env python3
"""
List all videos on a YouTube channel/playlist and save captions/transcripts to disk.

Uses **yt-dlp** (listing) + **youtube-transcript-api** (timedtext) + optional tiers.
Implementation: `scripts/youtube_transcripts/`. Respect YouTube ToS; operator research only.

Install:

  pip install -e ".[youtube-research]"

Optional queue (RQ + Redis):

  pip install -e ".[transcript-pipeline]"

Examples:

  python3 scripts/fetch_youtube_channel_transcripts.py \\
    --channel "https://www.youtube.com/@PredictiveHistory/videos" \\
    -o research/external/youtube-channels/predictive-history

  python3 scripts/fetch_youtube_channel_transcripts.py --limit 5 --dry-run
  python3 scripts/fetch_youtube_channel_transcripts.py --index-only
  python3 scripts/fetch_youtube_channel_transcripts.py --index-only --enrich-metadata \\
    --channel "https://www.youtube.com/@NateBJones/videos" -o /path/to/out

  # Full channel table (titles + dates): use --index-only --enrich-metadata (dates are often
  # missing from fast flat listing without --enrich-metadata).
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from youtube_transcripts.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
