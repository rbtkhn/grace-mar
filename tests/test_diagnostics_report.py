"""Diagnostics run + render."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_run_diagnostics_and_render(tmp_path: Path) -> None:
    cfg = REPO_ROOT / "examples" / "diagnostics" / "sample_input.yaml"
    jout = tmp_path / "d.json"
    subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "work_dev" / "run_diagnostics.py"),
            "--config",
            str(cfg),
            "--json-out",
            str(jout),
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    rout = tmp_path / "out.md"
    subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "work_dev" / "render_diagnostics_report.py"),
            "--input",
            str(jout),
            "-o",
            str(rout),
        ],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    text = rout.read_text(encoding="utf-8")
    assert "grace-mar" in text
    data = json.loads(jout.read_text(encoding="utf-8"))
    assert "overall_score" in data
