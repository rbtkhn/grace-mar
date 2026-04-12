"""Parity: validate.py ci argv tails vs .github/workflows/test.yml validation steps."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _tails_for_ci(user: str) -> list[list[str]]:
    from ci_validation_inventory import checks_for_group

    out = []
    for spec in checks_for_group("ci"):
        tail = spec.argv_builder(user)
        out.append([spec.script_relpath, *tail])
    return out


def test_ci_group_matches_test_workflow_order():
    """Steps and argv tails align with test.yml (Assert canonical paths … Validate work-dev)."""
    user = "grace-mar"
    tails = _tails_for_ci(user)
    assert tails == [
        ["scripts/assert_canonical_paths.py", "--user", user],
        ["scripts/validate-integrity.py", "--user", user, "--require-proposal-class"],
        ["scripts/validate_template_sync_contract.py"],
        ["scripts/governance_checker.py"],
        ["scripts/work_dev/validate_control_plane.py"],
    ]


def test_validate_ci_exits_zero_when_healthy():
    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "validate.py"), "--user", "grace-mar", "ci"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert r.returncode == 0, r.stderr + r.stdout


def test_validate_json_schema_version():
    r = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "validate.py"),
            "--user",
            "grace-mar",
            "--json",
            "fast",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        timeout=300,
    )
    assert r.returncode == 0, r.stderr
    data = json.loads(r.stdout)
    assert data["schema_version"] == "validation-run.v1"
    assert data["mode"] == "fast"
    assert "checks" in data
    for step in data["checks"]:
        assert "user_scope" in step
        assert step["status"] in ("pass", "fail", "timeout", "error", "skipped")


def test_expensive_skips_without_openai():
    env2 = os.environ.copy()
    env2.pop("OPENAI_API_KEY", None)
    r = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts" / "validate.py"),
            "--user",
            "grace-mar",
            "--json",
            "expensive",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        timeout=60,
        env=env2,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    data = json.loads(r.stdout)
    assert data["checks"][0]["status"] == "skipped"
