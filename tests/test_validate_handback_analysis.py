"""validate_handback_analysis — constitution line vs meta."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "work_dev" / "validate_handback_analysis.py"


def _run(stdin_json: str) -> tuple[int, str, str]:
    p = subprocess.run(
        [sys.executable, str(SCRIPT)],
        input=stdin_json,
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
        check=False,
    )
    return p.returncode, p.stdout, p.stderr


def test_validate_ok_clear() -> None:
    payload = {
        "content": "summary\n\nCONSTITUTION_ADVISORY: status=advisory_clear; rule_ids=none",
        "constitution_check_status": "advisory_clear",
    }
    rc, out, err = _run(json.dumps(payload))
    assert rc == 0
    assert err == ""


def test_validate_mismatch_fails() -> None:
    payload = {
        "content": "CONSTITUTION_ADVISORY: status=advisory_flagged; rule_ids=R1",
        "constitution_check_status": "advisory_clear",
    }
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "embedded" in err.lower() or "advisory" in err.lower()


def test_validate_flagged_without_line_fails() -> None:
    payload = {
        "content": "no advisory line here",
        "constitution_check_status": "advisory_flagged",
    }
    rc, _, err = _run(json.dumps(payload))
    assert rc == 1
    assert "advisory_flagged" in err
