"""work-dev dashboard builder."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_build_dashboard_empty_pipeline(tmp_path: Path) -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from work_dev.build_dashboard import build_dashboard

    # Minimal tree: control-plane only (copy from repo)
    root = tmp_path / "r"
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
    (root / "users" / "u1").mkdir(parents=True)
    d = build_dashboard(user_id="u1", repo_root=root)
    assert d.pipeline_event_counts == {}
    assert "implemented" in d.integration_status_counts
    assert 0.0 <= d.provenance_completeness_score <= 1.0


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
