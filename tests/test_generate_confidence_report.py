"""Optional tests for scripts/generate-confidence-report.py (requires plotly)."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from tests.conftest import REPO_ROOT, repo_python, run_cmd

plotly = pytest.importorskip("plotly")


def test_confidence_report_writes_html(tmp_path) -> None:
    target = tmp_path / "seed-phase"
    shutil.copytree(REPO_ROOT / "users" / "demo" / "seed-phase", target)
    result = run_cmd(
        [repo_python(), "scripts/generate-confidence-report.py", str(target)],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr
    html = target / "confidence-report.html"
    assert html.is_file() and html.stat().st_size > 100
