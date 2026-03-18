"""Tests for record integrity: validate-integrity and governance_checker."""
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"


def test_validate_integrity_exits_zero():
    """validate-integrity.py exits 0 when record is valid."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate-integrity.py"), "--user", "grace-mar"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"validate-integrity failed: {result.stderr or result.stdout}"


def test_governance_checker_exits_zero():
    """governance_checker.py exits 0 when no violations."""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "governance_checker.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"governance_checker failed: {result.stderr or result.stdout}"


def test_validate_integrity_json_mode():
    """validate-integrity --json emits valid JSON with ok and errors."""
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate-integrity.py"),
            "--user",
            "grace-mar",
            "--json",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert "ok" in data
    assert "errors" in data
    assert isinstance(data["errors"], list)
    assert "identity_library_boundary" in data
    assert "ix_a_ok" in data["identity_library_boundary"]
