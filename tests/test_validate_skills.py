"""Ensure all skill metadata passes validation."""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "validate_skills.py"


def test_all_skills_valid():
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--json"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"Validation errors:\n{result.stdout}"
    import json
    errors = json.loads(result.stdout)
    real_errors = [e for e in errors if e["level"] == "error"]
    assert len(real_errors) == 0, f"Skill validation errors: {real_errors}"
