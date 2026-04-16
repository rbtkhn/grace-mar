"""Tests for scripts/score_backfilled_thread_sources.py."""

from __future__ import annotations

from scripts.score_backfilled_thread_sources import (
    marker_block_end,
    marker_block_start,
    render_scored_block,
    score_from_source_stub,
)


def test_score_from_source_stub() -> None:
    assert score_from_source_stub("transcript: `x.md`") == "high"
    assert score_from_source_stub("days: `chapters/2026-04/days.md`") == "high"
    assert score_from_source_stub("knot: `k.md`") == "medium"
    assert score_from_source_stub("git: `k.md` (last touch 2026-01-01 abcdef12)") == "low"
    assert score_from_source_stub("unknown: `z.md`") == "low"


def test_render_scored_block_plain_months() -> None:
    inner = """## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `x` from **2026-01-01** through **2026-01-31**.
**Status:** Test.
**Rules:** Bullets only.

### 2026-01

- **2026-01-10** — Alpha.  \n  _Source:_ transcript: `t.md`
- **2026-01-11** — Beta.  \n  _Source:_ git: `g.md`
"""
    block = marker_block_start("x") + inner + marker_block_end("x")
    out = render_scored_block("x", block)
    assert out is not None
    assert "[strength: high]" in out
    assert "[strength: low]" in out
    assert "**Score totals (window):** high=1, medium=0, low=1." in out
    assert "_Strength mix:_ high=1, medium=0, low=1" in out


def test_render_scored_block_none_without_months() -> None:
    inner = """## Title

_No eligible evidence._
"""
    block = marker_block_start("x") + inner + marker_block_end("x")
    assert render_scored_block("x", block) is None


def test_render_preserves_month_level_arc_section() -> None:
    inner = """## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `x` from **2026-01-01** through **2026-01-31**.
**Status:** Test.
**Rules:** Bullets only.

### 2026-01

#### Month-level arc

- Arc point one.

#### Dated evidence

- **2026-01-10** — Alpha.  \n  _Source:_ knot: `k.md`
"""
    block = marker_block_start("x") + inner + marker_block_end("x")
    out = render_scored_block("x", block)
    assert out is not None
    assert "#### Month-level arc" in out
    assert "Arc point one." in out
    assert "[strength: medium]" in out


def test_rescore_strips_prior_strength_tag() -> None:
    inner = """## Backfilled historical arc (reconstructed from notebook artifacts)

**Scope:** `x` from **2026-01-01** through **2026-01-31**.
**Status:** Test.
**Rules:** Bullets only.

### 2026-01

- **2026-01-10** — [strength: low] Wrong prior.  \n  _Source:_ transcript: `t.md`
"""
    block = marker_block_start("x") + inner + marker_block_end("x")
    out = render_scored_block("x", block)
    assert out is not None
    assert "[strength: high]" in out
    assert "Wrong prior." in out
    assert "[strength: low] Wrong prior." not in out
