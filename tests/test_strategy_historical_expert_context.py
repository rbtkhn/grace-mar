"""Tests for scripts/strategy_historical_expert_context.py."""

from __future__ import annotations

from pathlib import Path

from scripts.strategy_historical_expert_context import (
    Segment,
    extract_human_layer,
    filter_segments,
    parse_segments,
    render_single_month_artifact,
    strip_backfill_block,
)


def test_strip_backfill_removes_block() -> None:
    text = """## Segment 1

## 2026-01
- one

<!-- backfill:x:start -->
### 2026-01
SECRET
<!-- backfill:x:end -->

"""
    out = strip_backfill_block(text, "x")
    assert "SECRET" not in out
    assert "one" in out


def test_parse_segments_h2_prefers_h2() -> None:
    stripped = """## 2026-01
- [strength: high] Claim about mechanism.
## 2026-02
- tension versus other lane
"""
    segs, note = parse_segments(stripped)
    assert len(segs) == 2
    assert segs[0].segment_id == "2026-01"
    assert segs[0].strength_counts["high"] == 1
    assert "YYYY-MM" in note
    assert segs[0].source == "h2"


def test_parse_segments_h3_fallback() -> None:
    stripped = """### 2026-01
- bullet a
### 2026-02
- bullet b
"""
    segs, note = parse_segments(stripped)
    assert len(segs) == 2
    assert segs[0].source == "h3"
    assert "fallback" in note


def test_human_layer_excludes_machine_block() -> None:
    full = """# T
above
<!-- strategy-expert-thread:start -->
## Segment 2
inside
<!-- strategy-expert-thread:end -->
"""
    h = extract_human_layer(full)
    assert "inside" not in h
    assert "above" in h


def test_render_single_month_artifact_title() -> None:
    seg = Segment(
        segment_id="2026-02",
        raw_text="- x",
        bullets=["b1"],
        strength_counts={"high": 0, "medium": 0, "low": 0},
        signal_lines=[],
        tension_lines=[],
        shift_lines=[],
        source="h2",
    )
    md = render_single_month_artifact("e-id", seg, "docs/x.md", "note")
    assert md.startswith("# Historical expert context — `e-id` — `2026-02`")
    assert "Segments included: 2026-02" in md


def test_filter_segments_range() -> None:
    from scripts.strategy_historical_expert_context import Segment

    segs = [
        Segment(
            "2026-01",
            "",
            [],
            {"high": 0, "medium": 0, "low": 0},
            [],
            [],
            [],
            "h2",
        ),
        Segment(
            "2026-04",
            "",
            [],
            {"high": 0, "medium": 0, "low": 0},
            [],
            [],
            [],
            "h2",
        ),
    ]
    f = filter_segments(segs, "2026-01", "2026-03")
    assert len(f) == 1
    assert f[0].segment_id == "2026-01"


def test_fixture_file_roundtrip_skips_backfill(tmp_path: Path) -> None:
    """Last ## month body must not include backfill HTML."""
    p = tmp_path / "thread.md"
    p.write_text(
        """## 2026-03
- last month bullet

<!-- backfill:e:start -->
BACKFILL
<!-- backfill:e:end -->

<!-- strategy-expert-thread:start -->
MACHINE
<!-- strategy-expert-thread:end -->
""",
        encoding="utf-8",
    )
    text = p.read_text()
    human = extract_human_layer(text)
    stripped = strip_backfill_block(human, "e")
    segs, _ = parse_segments(stripped)
    assert len(segs) == 1
    assert segs[0].segment_id == "2026-03"
    assert "BACKFILL" not in segs[0].raw_text
    assert "last month bullet" in segs[0].raw_text
