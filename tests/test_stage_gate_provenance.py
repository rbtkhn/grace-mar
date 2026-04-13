"""Gate candidate build_block provenance extension."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from stage_gate_candidate import build_block  # noqa: E402


def test_build_block_includes_provenance_yaml() -> None:
    block = build_block(
        candidate_id="CANDIDATE-0999",
        title="Test",
        summary="Summary line",
        body="Body text",
        mind_category="knowledge",
        channel_key="operator:cursor:test",
        territory=None,
        timestamp="2026-01-01 00:00:00",
        provenance={
            "source_observation_ids": ["obs_20260101T000000Z_aabbccdd"],
            "timeline_anchor": "obs_20260101T000000Z_aabbccdd",
            "lane_origin": "work-strategy",
            "supporting_evidence_refs": ["ACT-0001"],
            "contradiction_refs": [],
        },
    )
    assert "source_observation_ids:" in block
    assert "obs_20260101T000000Z_aabbccdd" in block
    assert "lane_origin:" in block
