"""Tests for scripts/refine_backfilled_thread_arc.py — bullet parsing and no-op paths."""

from __future__ import annotations

import pytest

from scripts.refine_backfilled_thread_arc import (
    marker_block_end,
    marker_block_start,
    parse_bullets,
    render_refined_block,
)


def test_parse_bullets_matches_backfill_format_bullet() -> None:
    # Mirrors scripts/backfill_expert_thread.format_bullet (two spaces before \n).
    section = """### 2026-01

- **2026-01-15** — First claim.  \n  _Source:_ transcript: `foo/bar.md`
- **2026-01-20** — Second claim with git tail.  \n  _Source:_ knot: `knots/x.md` (last touch 2026-01-22 abcdef123456)
"""
    bullets = parse_bullets(section)
    assert len(bullets) == 2
    assert bullets[0].date == "2026-01-15"
    assert bullets[0].summary == "First claim."
    assert "transcript:" in bullets[0].source
    assert bullets[1].date == "2026-01-20"
    assert "abcdef123456" in bullets[1].source


def test_render_refined_block_none_when_no_month_headings() -> None:
    inner = """## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `x` from **2026-01-01** through **2026-03-31**.

**Status:** Reconstructed summary.

**Rules:** Dated bullets only.

_No eligible evidence found in the requested window._
"""
    block = marker_block_start("x") + inner + marker_block_end("x")
    assert render_refined_block("x", block) is None


def test_render_refined_block_roundtrip_has_months() -> None:
    inner = """## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `ritter` from **2026-01-01** through **2026-01-31**.

**Status:** Test.

**Rules:** Dated bullets only.

### 2026-01

- **2026-01-10** — Alpha.  \n  _Source:_ transcript: `t.md`
"""
    block = marker_block_start("ritter") + inner + marker_block_end("ritter")
    out = render_refined_block("ritter", block)
    assert out is not None
    assert "<!-- backfill:ritter:start -->" in out
    assert "#### Month-level arc" in out
    assert "#### Dated evidence" in out
    assert "**2026-01-10** — Alpha." in out


@pytest.mark.parametrize(
    "summary_ws",
    [
        "Summary text.  ",  # trailing spaces before line break (loose path)
    ],
)
def test_parse_bullets_loose_optional_whitespace(summary_ws: str) -> None:
    section = f"""### 2026-02

- **2026-02-01** — {summary_ws} \n  _Source:_ knot: `p.md`
"""
    bullets = parse_bullets(section)
    assert len(bullets) == 1
    assert bullets[0].summary.strip() == "Summary text."
