"""Scenario matrix generator — factorial expansion and CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from work_dev.generate_scenarios import build_matrix  # noqa: E402


def test_build_matrix_cartesian_dimensions(tmp_path: Path) -> None:
    base = tmp_path / "baseline_scenarios"
    base.mkdir(parents=True)

    scenario = {
        "scenario_id": "continuity_failure",
        "failure_family": "continuity receipt failure",
        "severity": "high",
        "required_checks": ["continuity_required"],
        "dimensions": {
            "receipt_state": ["valid", "missing"],
            "topology": ["local", "remote"],
        },
        "exclude": [
            {"runtime": "cursor", "topology": "remote"},
        ],
    }
    (base / "continuity_failure.yaml").write_text(yaml.safe_dump(scenario), encoding="utf-8")

    rows = build_matrix(
        scenario_filter="",
        runtimes=["openclaw", "cursor"],
        base_dir=base,
    )

    # openclaw gets 4 combinations; cursor loses both remote rows (valid+remote, missing+remote)
    assert len(rows) == 6
    assert {r.runtime for r in rows} == {"openclaw", "cursor"}
    assert any(r.variation == "receipt_state=missing__topology=remote" for r in rows)
    assert not any(
        r.runtime == "cursor" and r.variation == "receipt_state=valid__topology=remote"
        for r in rows
    )


def test_build_matrix_explicit_variations_override_cartesian(tmp_path: Path) -> None:
    base = tmp_path / "baseline_scenarios"
    base.mkdir(parents=True)

    scenario = {
        "scenario_id": "reasoning_action_mismatch",
        "expected_failure_mode": "rationale and staged action diverge",
        "severity": "critical",
        "required_checks": ["shadow_log", "autonomy_tiers"],
        "variations": [
            {
                "id": "approve_but_warns",
                "values": {"agent_action": "approve", "reasoning_polarity": "warn"},
            },
            {
                "id": "reject_but_praises",
                "values": {"agent_action": "reject", "reasoning_polarity": "praise"},
                "severity": "high",
            },
        ],
    }
    (base / "reasoning_action_mismatch.yaml").write_text(yaml.safe_dump(scenario), encoding="utf-8")

    rows = build_matrix(
        scenario_filter="reasoning_action",
        runtimes=["openclaw"],
        base_dir=base,
    )

    assert len(rows) == 2
    assert rows[0].scenario_id == "reasoning_action_mismatch"
    assert {r.variation for r in rows} == {"approve_but_warns", "reject_but_praises"}
    assert any(r.severity == "high" for r in rows)
    assert all("shadow_log" in r.required_checks for r in rows)


def test_generate_scenarios_cli_json_stable_v2() -> None:
    p1 = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "work_dev" / "generate_scenarios.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    p2 = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "work_dev" / "generate_scenarios.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert p1.stdout == p2.stdout
    data = json.loads(p1.stdout)
    assert data["version"] == 2
    assert len(data["rows"]) >= 1 * 3  # at least one scenario × default runtimes
