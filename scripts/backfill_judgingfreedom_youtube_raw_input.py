#!/usr/bin/env python3
"""Backfill Judging Freedom YouTube transcripts into raw-input/.

WORK only; not Record.
"""

from __future__ import annotations

import sys
from pathlib import Path

from backfill_youtube_channel_raw_input import main as youtube_main

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CHANNEL_URL = "https://www.youtube.com/@judgingfreedom/videos"
DEFAULT_SHOW = "Judging Freedom"
DEFAULT_HOST = "Judge Andrew Napolitano"


def main() -> int:
    return youtube_main(
        [
            "--channel-url",
            DEFAULT_CHANNEL_URL,
            "--channel-slug",
            "judging-freedom",
            "--show",
            DEFAULT_SHOW,
            "--host",
            DEFAULT_HOST,
            "--file-prefix",
            "youtube-judging-freedom",
            "--source-note",
            "Automated YouTube transcript fetch for Judging Freedom hub capture.",
            "--work-dir",
            str(REPO_ROOT / ".codex-tmp" / "youtube-judging-freedom"),
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
