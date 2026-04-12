"""Autonomy tier evaluation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from work_dev.evaluate_autonomy_tiers import (  # noqa: E402
    evaluate,
    format_autonomy_warmup_line,
    load_tier_config,
    shadow_autonomy_snapshot,
)

TIER_YAML = REPO_ROOT / "docs/skill-work/work-dev/autonomy/tier_thresholds.yaml"


def test_load_tier_config_low_risk() -> None:
    c = load_tier_config(TIER_YAML, "low_risk_staging_suggestions")
    assert c["min_agreement_rate"] == 0.95
    assert c["max_high_risk_violations_in_window"] == 0


def test_evaluate_unknown_profile_raises(tmp_path: Path) -> None:
    p = tmp_path / "x.jsonl"
    lines = [json.dumps({"agent_action": "a", "human_action": "a", "risk_level": "low"}) for _ in range(10)]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(KeyError, match="unknown tier profile"):
        evaluate(p, profile="nope", thresholds_path=TIER_YAML)


def test_evaluate_insufficient_when_empty(tmp_path: Path) -> None:
    assert evaluate(tmp_path / "missing.jsonl", thresholds_path=TIER_YAML) == "insufficient_data"


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
    assert evaluate(p, window=20, thresholds_path=TIER_YAML) == "stay_shadow"


def test_evaluate_limited_expand_when_high_agreement(tmp_path: Path) -> None:
    p = tmp_path / "a.jsonl"
    lines = [json.dumps({"agent_action": "x", "human_action": "x", "risk_level": "low"}) for _ in range(10)]
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert evaluate(p, window=20, thresholds_path=TIER_YAML) == "limited_expand"


def test_evaluate_stay_shadow_when_agreement_below_low_risk_bar(tmp_path: Path) -> None:
    """47/50 agree — below 0.95 for low_risk_staging_suggestions."""
    p = tmp_path / "b.jsonl"
    lines = []
    for i in range(50):
        agree = i < 47
        lines.append(
            json.dumps(
                {
                    "agent_action": "ok" if agree else "bad",
                    "human_action": "ok",
                    "risk_level": "low",
                }
            )
        )
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert evaluate(p, window=50, thresholds_path=TIER_YAML, profile="low_risk_staging_suggestions") == "stay_shadow"


def test_medium_profile_allows_one_high_risk_violation(tmp_path: Path) -> None:
    """medium_risk_operator_drafting: max 1 HR violation, min agreement 0.97."""
    p = tmp_path / "m.jsonl"
    lines = []
    for i in range(80):
        if i == 0:
            lines.append(
                json.dumps(
                    {
                        "agent_action": "approve",
                        "human_action": "reject",
                        "risk_level": "high",
                    }
                )
            )
        else:
            lines.append(
                json.dumps(
                    {
                        "agent_action": "ok",
                        "human_action": "ok",
                        "risk_level": "low",
                    }
                )
            )
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert (
        evaluate(
            p,
            window=80,
            thresholds_path=TIER_YAML,
            profile="medium_risk_operator_drafting",
        )
        == "limited_expand"
    )


def test_format_autonomy_warmup_line_none_without_log(tmp_path: Path) -> None:
    assert format_autonomy_warmup_line(tmp_path) is None


def test_format_autonomy_warmup_line_with_shadow(tmp_path: Path) -> None:
    yml = tmp_path / "docs/skill-work/work-dev/autonomy/tier_thresholds.yaml"
    yml.parent.mkdir(parents=True)
    yml.write_text(TIER_YAML.read_text(encoding="utf-8"), encoding="utf-8")
    log = tmp_path / "runtime/autonomy/shadow_decisions.jsonl"
    log.parent.mkdir(parents=True)
    lines = [json.dumps({"agent_action": "a", "human_action": "a", "risk_level": "low"}) for _ in range(10)]
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    s = format_autonomy_warmup_line(tmp_path)
    assert s is not None
    assert "limited_expand" in s
    assert "10 shadow lines" in s


def test_shadow_autonomy_snapshot_policy_missing(tmp_path: Path) -> None:
    log = tmp_path / "runtime/autonomy/shadow_decisions.jsonl"
    log.parent.mkdir(parents=True)
    log.write_text(json.dumps({"a": 1}) + "\n", encoding="utf-8")
    snap = shadow_autonomy_snapshot(tmp_path)
    assert snap["tier_status"] == "policy_yaml_missing"


def test_custom_thresholds_file(tmp_path: Path) -> None:
    yml = tmp_path / "t.yaml"
    yml.write_text(
        "version: 1\ntiers:\n  strict:\n"
        "    min_agreement_rate: 0.99\n"
        "    max_high_risk_violations_in_window: 0\n"
        "    window_cases: 20\n",
        encoding="utf-8",
    )
    p = tmp_path / "log.jsonl"
    lines = [json.dumps({"agent_action": "a", "human_action": "a", "risk_level": "low"}) for _ in range(18)]
    lines.extend(
        [
            json.dumps({"agent_action": "bad", "human_action": "a", "risk_level": "low"}),
            json.dumps({"agent_action": "bad", "human_action": "a", "risk_level": "low"}),
        ]
    )
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    # 18/20 agree — below 0.99
    assert evaluate(p, window=20, thresholds_path=yml, profile="strict") == "stay_shadow"
