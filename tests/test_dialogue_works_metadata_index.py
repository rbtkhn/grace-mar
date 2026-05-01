"""Tests for the Dialogue Works metadata-only index builder."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_dialogue_works_metadata_index import (  # noqa: E402
    build_rows,
    infer_guest_from_title,
    render_table,
)


def _write_crawl_index(path: Path) -> None:
    payload = {
        "videos": [
            {
                "video_id": "late0000001",
                "title": "Scott Ritter: This Is the Moment the West Started Losing",
                "upload_date": "20260126",
                "url": "https://www.youtube.com/watch?v=late0000001",
            },
            {
                "video_id": "early0000002",
                "title": "Amb. Chas Freeman: Countdown to War between The US and Iran - History Is Repeating Itself",
                "upload_date": "20260129",
                "url": "https://www.youtube.com/watch?v=early0000002",
            },
        ]
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_infer_guest_from_title_handles_dialogue_works_patterns() -> None:
    assert infer_guest_from_title("Nima x Glenn Diesen - Iran, War, and Order") == "Glenn Diesen"
    assert (
        infer_guest_from_title("Larry C. Johnson & Col. Larry Wilkerson: One Strike Away")
        == "Larry C. Johnson & Col. Larry Wilkerson"
    )


def test_build_rows_orders_oldest_first_and_marks_capture(tmp_path: Path) -> None:
    crawl = tmp_path / "index.json"
    raw_root = tmp_path / "raw-input"
    _write_crawl_index(crawl)

    mirrored = raw_root / "2026-01-26" / "substack-ritter.md"
    mirrored.parent.mkdir(parents=True, exist_ok=True)
    mirrored.write_text(
        "---\nsource_url: \"https://www.youtube.com/watch?v=late0000001\"\n---\n",
        encoding="utf-8",
    )

    rows = build_rows(crawl_index=crawl, raw_input_root=raw_root)

    assert [r.pub_date for r in rows] == ["2026-01-26", "2026-01-29"]
    assert rows[0].guest == "Scott Ritter"
    assert rows[0].routing_note == "thread: ritter"
    assert rows[0].raw_input_note == "mirrored"
    assert rows[1].guest == "Amb. Chas Freeman"
    assert rows[1].routing_note == "thread: freeman"
    assert rows[1].raw_input_note == "needs capture"


def test_render_table_includes_links_and_marker(tmp_path: Path) -> None:
    crawl = tmp_path / "index.json"
    raw_root = tmp_path / "raw-input"
    _write_crawl_index(crawl)
    rows = build_rows(crawl_index=crawl, raw_input_root=raw_root)

    table = render_table(rows)
    assert "[https://www.youtube.com/watch?v=late0000001](https://www.youtube.com/watch?v=late0000001)" in table
    assert "needs capture" in table
