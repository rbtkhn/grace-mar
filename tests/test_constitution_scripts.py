"""Subprocess tests for generate-constitution.py and validate-constitution.py."""

from __future__ import annotations

import shutil
from pathlib import Path

from tests.conftest import REPO_ROOT, repo_python, run_cmd


def test_generate_then_validate_constitution_valid_minimal(tmp_path: Path) -> None:
    target = tmp_path / "seed-phase"
    shutil.copytree(REPO_ROOT / "tests/fixtures/seed-phase/valid-minimal", target)
    gen = run_cmd(
        [repo_python(), "scripts/generate-constitution.py", str(target)],
        cwd=REPO_ROOT,
    )
    assert gen.returncode == 0, gen.stderr
    val = run_cmd(
        [repo_python(), "scripts/validate-constitution.py", str(target)],
        cwd=REPO_ROOT,
    )
    assert val.returncode == 0, val.stderr
