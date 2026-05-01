#!/usr/bin/env python3
"""Backfill Glenn Diesen YouTube transcripts into raw-input/.

WORK only; not Record.
"""

from __future__ import annotations

import sys
from pathlib import Path

from backfill_youtube_channel_raw_input import main as youtube_main

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHANNEL_URL = "https://www.youtube.com/@GDiesen1/videos"
DEFAULT_SHOW = "Glenn Diesen"
DEFAULT_HOST = "Glenn Diesen"


def main() -> int:
    return youtube_main(
        [
            "--channel-url",
            DEFAULT_CHANNEL_URL,
            "--channel-slug",
            "glenn-diesen",
            "--show",
            DEFAULT_SHOW,
            "--host",
            DEFAULT_HOST,
            "--thread",
            "diesen",
            "--file-prefix",
            "youtube-glenn-diesen",
            "--source-note",
            "Automated YouTube transcript fetch for Glenn Diesen.",
            "--work-dir",
            str(REPO_ROOT / ".codex-tmp" / "youtube-glenn-diesen"),
            "--notebook-root",
            str(REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"),
            "--limit",
            "20",
            "--sleep",
            "0.25",
            "--infer-guest",
            *sys.argv[1:],
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
