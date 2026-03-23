"""Tests for scripts/stage_gate_candidate.py"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from stage_gate_candidate import (  # noqa: E402
    build_block,
    insert_before_processed,
    next_candidate_id,
)


def test_next_candidate_id_empty():
    assert next_candidate_id("") == "CANDIDATE-0001"


def test_next_candidate_id_max():
    assert next_candidate_id("CANDIDATE-0009\nCANDIDATE-0002") == "CANDIDATE-0010"


def test_insert_before_processed():
    md = "# G\n\n## Candidates\n\n## Processed\n\nold\n"
    block = "### X\n\n```yaml\nstatus: pending\n```\n\n"
    out = insert_before_processed(md, block)
    assert out.index("### X") < out.index("## Processed")
    assert "## Processed" in out


def test_build_block_work_politics_territory():
    b = build_block(
        candidate_id="CANDIDATE-0099",
        title="t",
        summary="sum",
        body="line",
        mind_category="curiosity",
        channel_key="operator:wap:stage-paste",
        territory="work-politics",
        timestamp="2026-01-01 12:00:00",
    )
    assert "territory: work-politics" in b
    assert "mind_category: curiosity" in b
    assert "operator:wap:stage-paste" in b


def test_insert_raises_without_processed():
    with pytest.raises(ValueError, match="## Processed"):
        insert_before_processed("no marker", "x")


def test_build_block_proposal_class():
    b = build_block(
        candidate_id="CANDIDATE-0001",
        title="t",
        summary="sum",
        body="line",
        mind_category="knowledge",
        channel_key="operator:cursor:stage-paste",
        territory=None,
        timestamp="2026-01-01 12:00:00",
        proposal_class="SIMULATION_RESULT",
    )
    assert "proposal_class: SIMULATION_RESULT" in b
