"""Subprocess tests for scripts/check-seed-consistency.py."""

from __future__ import annotations

import shutil

from tests.conftest import REPO_ROOT, copy_fixture, repo_python, run_cmd


def test_check_consistency_passes_for_demo_copy(tmp_path) -> None:
    target = tmp_path / "seed-phase"
    shutil.copytree(REPO_ROOT / "users" / "demo" / "seed-phase", target)
    result = run_cmd(
        [repo_python(), "scripts/check-seed-consistency.py", str(target)],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_check_consistency_fails_for_generic_intent_with_pass(tmp_seed_dir) -> None:
    copy_fixture("invalid-intent-too-generic", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/check-seed-consistency.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode != 0
