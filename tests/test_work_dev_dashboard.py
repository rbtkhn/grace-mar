"""work-dev dashboard builder."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _copy_control_plane(root: Path) -> None:
    cp = root / "docs" / "skill-work" / "work-dev" / "control-plane"
    cp.mkdir(parents=True)
    src_cp = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "control-plane"
    for name in (
        "integration_status.yaml",
        "known_gaps.yaml",
        "target_registry.yaml",
        "proof_ledger.yaml",
    ):
        (cp / name).write_text((src_cp / name).read_text(encoding="utf-8"), encoding="utf-8")


def test_build_dashboard_empty_pipeline(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from work_dev.build_dashboard import build_dashboard

    root = tmp_path / "r"
    _copy_control_plane(root)
    (root / "users" / "u1").mkdir(parents=True)
    d = build_dashboard(user_id="u1", repo_root=root)
    assert d.pipeline_event_counts == {}
    assert "implemented" in d.integration_status_counts
    assert 0.0 <= d.provenance_completeness_score <= 1.0
    assert d.provenance_from_gate is False
    assert d.lane_violation_count == 0
    assert d.continuity_block_count == 0
    assert d.autonomy_shadow_line_count == 0
    assert d.autonomy_tier_status == "no_log"


def test_build_dashboard_counts_lane_violations(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from work_dev.build_dashboard import build_dashboard

    root = tmp_path / "r"
    _copy_control_plane(root)
    (root / "users" / "u1").mkdir(parents=True)
    obs = root / "runtime" / "observability"
    obs.mkdir(parents=True)
    (obs / "lane_scope.jsonl").write_text(
        '{"event":"lane_violation"}\n{"event":"lane_violation"}\n',
        encoding="utf-8",
    )
    d = build_dashboard(user_id="u1", repo_root=root)
    assert d.lane_violation_count == 2


def test_build_dashboard_counts_continuity_blocks(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from work_dev.build_dashboard import build_dashboard

    root = tmp_path / "r"
    _copy_control_plane(root)
    (root / "users" / "u1").mkdir(parents=True)
    obs = root / "runtime" / "observability"
    obs.mkdir(parents=True)
    (obs / "continuity_blocks.jsonl").write_text(
        '{"event":"continuity_block"}\n',
        encoding="utf-8",
    )
    d = build_dashboard(user_id="u1", repo_root=root)
    assert d.continuity_block_count == 1


def test_count_jsonl_events_skips_malformed(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from work_dev.build_dashboard import count_jsonl_events

    p = tmp_path / "bad.jsonl"
    p.write_text(
        '{"event":"lane_violation"}\nnot-json\n{"event":"lane_violation"}\n',
        encoding="utf-8",
    )
    assert count_jsonl_events(p, event_name="lane_violation") == 2


def test_build_dashboard_provenance_from_recursion_gate(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from work_dev.build_dashboard import build_dashboard

    root = tmp_path / "r"
    _copy_control_plane(root)
    (root / "users" / "u1").mkdir(parents=True)
    gate = root / "users" / "u1" / "recursion-gate.md"
    # Two pending blocks: full metadata vs minimal
    gate.write_text(
        """## Candidates\n\n### CANDIDATE-1\n```yaml\nstatus: pending\ncandidate_source: \"openclaw\"\nartifact_path: \"a\"\nartifact_sha256: \"x\"\ncontinuity_receipt_path: \"r.json\"\nconstitution_check_status: \"ok\"\n```\n\n### CANDIDATE-2\n```yaml\nstatus: pending\ncandidate_source: \"x\"\n```\n\n## Processed\n\n""",
        encoding="utf-8",
    )
    d = build_dashboard(user_id="u1", repo_root=root)
    assert d.provenance_from_gate is True
    # Block1: 1.0, Block2: 0.2 => 0.6
    assert abs(d.provenance_completeness_score - 0.6) < 1e-6


def test_build_dashboard_autonomy_with_shadow_log(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from work_dev.build_dashboard import build_dashboard

    root = tmp_path / "r"
    _copy_control_plane(root)
    (root / "users" / "u1").mkdir(parents=True)
    aut = root / "docs" / "skill-work" / "work-dev" / "autonomy"
    aut.mkdir(parents=True)
    (aut / "tier_thresholds.yaml").write_text(
        (REPO_ROOT / "docs/skill-work/work-dev/autonomy/tier_thresholds.yaml").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )
    slog = root / "runtime" / "autonomy"
    slog.mkdir(parents=True)
    import json

    lines = [
        json.dumps({"agent_action": "x", "human_action": "x", "risk_level": "low"})
        for _ in range(10)
    ]
    (slog / "shadow_decisions.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
    d = build_dashboard(user_id="u1", repo_root=root)
    assert d.autonomy_shadow_line_count == 10
    assert d.autonomy_tier_status == "limited_expand"


def test_build_dashboard_markdown_reflects_feed_counts(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from work_dev.build_dashboard import build_dashboard, render_markdown

    root = tmp_path / "r"
    _copy_control_plane(root)
    (root / "users" / "u1").mkdir(parents=True)
    obs = root / "runtime" / "observability"
    obs.mkdir(parents=True)
    (obs / "lane_scope.jsonl").write_text('{"event":"lane_violation"}\n', encoding="utf-8")
    d = build_dashboard(user_id="u1", repo_root=root)
    md = render_markdown(d)
    assert "Lane violation count (observability feed): 1" in md
    assert "Continuity block count (observability feed): 0" in md


def test_build_dashboard_cli_writes_artifacts() -> None:
    rc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "work_dev" / "build_dashboard.py"), "-u", "grace-mar"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert rc.returncode == 0, rc.stderr
    j = REPO_ROOT / "artifacts" / "work_dev_dashboard.json"
    assert j.is_file()
    data = json.loads(j.read_text(encoding="utf-8"))
    assert "integration_status_counts" in data
    assert "provenance_from_gate" in data
    assert "lane_violation_count" in data
    assert "autonomy_tier_status" in data
