#!/usr/bin/env python3
"""Backfill The Grayzone YouTube transcripts into raw-input/.

WORK only; not Record.
"""

from __future__ import annotations

import sys
from pathlib import Path

from backfill_youtube_channel_raw_input import main as youtube_main

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHANNEL_URL = "https://www.youtube.com/@TheGrayzone/videos"
DEFAULT_SHOW = "The Grayzone"
DEFAULT_HOST = "Max Blumenthal / Aaron Maté"


def main() -> int:
    return youtube_main(
        [
            "--channel-url",
            DEFAULT_CHANNEL_URL,
            "--channel-slug",
            "the-grayzone",
            "--show",
            DEFAULT_SHOW,
            "--host",
            DEFAULT_HOST,
            "--file-prefix",
            "youtube-the-grayzone",
            "--source-note",
            "Automated YouTube transcript fetch for The Grayzone hub capture.",
            "--work-dir",
            str(REPO_ROOT / ".codex-tmp" / "youtube-the-grayzone"),
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
