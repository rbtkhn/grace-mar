"""Smoke tests for skill-think validators and builders."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / name), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_validate_think_claims() -> None:
    pytest.importorskip("jsonschema")
    cp = _run("validate_think_claims.py", "--skill-think-md", "users/grace-mar/skill-think.md")
    assert cp.returncode == 0, cp.stderr


def test_build_think_observability() -> None:
    cp = _run("build_think_observability.py")
    assert cp.returncode == 0, cp.stderr
    out = REPO_ROOT / "artifacts/skill-think/think-observability.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    sv = data.get("schemaVersion", "")
    assert sv.startswith("1.") and "skill-think" in sv
    assert "metrics" in data


def test_propose_think_claims_from_read_stdout_json() -> None:
    cp = _run("propose_think_claims_from_read.py", "--max-ids", "3")
    assert cp.returncode == 0
    data = json.loads(cp.stdout)
    assert "proposed_think_claims" in data
