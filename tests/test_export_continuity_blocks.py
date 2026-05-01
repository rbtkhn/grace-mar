"""Tests for continuity-block observability export."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WD = REPO_ROOT / "scripts" / "work_dev"
if str(WD) not in sys.path:
    sys.path.insert(0, str(WD))

from export_continuity_blocks import export_continuity_blocks, load_events, render_markdown  # noqa: E402


def test_missing_feed_exports_empty_report(tmp_path: Path) -> None:
    source = tmp_path / "runtime" / "observability" / "continuity_blocks.jsonl"
    output = tmp_path / "artifacts" / "work-dev" / "continuity-observability" / "continuity-blocks.md"

    markdown = export_continuity_blocks(source, output, repo_root=tmp_path)

    assert output.is_file()
    assert "Continuity block events: `0`" in markdown
    assert "No continuity block events were observed" in markdown


def test_load_events_ignores_non_blocks_and_invalid_lines(tmp_path: Path) -> None:
    source = tmp_path / "continuity_blocks.jsonl"
    source.write_text(
        "\n".join(
            [
                json.dumps({"event": "continuity_block", "reason": "no receipt", "source": "openclaw_stage"}),
                json.dumps({"event": "other_event"}),
                "{not json",
            ]
        ),
        encoding="utf-8",
    )

    events, invalid = load_events(source)

    assert len(events) == 1
    assert invalid == 2


def test_render_markdown_summarizes_recent_events(tmp_path: Path) -> None:
    source = tmp_path / "runtime" / "observability" / "continuity_blocks.jsonl"
    events = [
        {
            "event": "continuity_block",
            "user_id": "grace-mar",
            "source": "openclaw_stage",
            "reason": "no valid continuity receipt",
            "ts": "2026-05-01T12:00:00Z",
        }
    ]

    markdown = render_markdown(
        events,
        invalid_lines=0,
        input_path=source,
        repo_root=tmp_path,
        generated_at="2026-05-01T12:01:00Z",
    )

    assert "WORK-derived operator artifact" in markdown
    assert "`no valid continuity receipt`: 1" in markdown
    assert "| `2026-05-01T12:00:00Z` | `grace-mar` | `openclaw_stage` | no valid continuity receipt |" in markdown
