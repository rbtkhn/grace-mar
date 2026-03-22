"""Daily brief: G-scoring and civ-mem config merge."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from generate_wap_daily_brief import (  # noqa: E402
    DEFAULT_GEO_MILITARY_PHRASES,
    _civ_mem_resonance_lines,
    _load_full_config,
    _score_keywords,
)


def test_geo_extra_merges_with_defaults() -> None:
    cfg = REPO_ROOT / "docs/skill-work/work-strategy/daily-brief-config.json"
    *_, geo, geo_loc = _load_full_config(cfg)
    assert "pentagon" in geo
    assert "idf" in geo
    assert isinstance(geo_loc, dict)


def test_score_g_counts_geo_phrases() -> None:
    blob = "The Pentagon announced new naval deployments near NATO waters."
    g = _score_keywords(blob.lower(), tuple(DEFAULT_GEO_MILITARY_PHRASES))
    assert g >= 2


def test_civ_mem_resonance_returns_lines() -> None:
    lines = _civ_mem_resonance_lines(
        ["war powers congress military intervention alliance structure"],
        limit_per_seed=2,
        max_rows=6,
    )
    assert isinstance(lines, list)
    assert len(lines) >= 1
