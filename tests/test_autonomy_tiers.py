"""Autonomy tier evaluation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from work_dev.evaluate_autonomy_tiers import evaluate  # noqa: E402


def test_evaluate_insufficient_when_empty(tmp_path: Path) -> None:
    assert evaluate(tmp_path / "missing.jsonl") == "insufficient_data"


def test_evaluate_stay_shadow_on_high_risk_divergence(tmp_path: Path) -> None:
    p = tmp_path / "s.jsonl"
    lines = []
    for _ in range(10):
        lines.append(
            json.dumps(
                {
                    "agent_action": "approve",
                    "human_action": "reject",
                    "risk_level": "high",
                }
            )
        )
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert evaluate(p, window=20) == "stay_shadow"


def test_evaluate_limited_expand_when_high_agreement(tmp_path: Path) -> None:
    p = tmp_path / "a.jsonl"
    lines = [json.dumps({"agent_action": "x", "human_action": "x", "risk_level": "low"}) for _ in range(10)]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert evaluate(p, window=20) == "limited_expand"
