"""Subprocess tests for scripts/generate-seed-dossier.py (tmp dirs only — never users/demo)."""

from __future__ import annotations

import shutil

from tests.conftest import REPO_ROOT, copy_fixture, repo_python, run_cmd


def test_generate_seed_dossier_demo_copy_has_expected_sections(tmp_path) -> None:
    target = tmp_path / "seed-phase"
    shutil.copytree(REPO_ROOT / "users" / "demo" / "seed-phase", target)
    result = run_cmd(
        [repo_python(), "scripts/generate-seed-dossier.py", str(target)],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    text = (target / "seed_dossier.md").read_text(encoding="utf-8")
    assert "# Seed Dossier" in text
    assert "## Seed intent" in text
    assert "## Identity Summary" in text
    assert "## Activation Recommendation" in text


def test_generate_seed_dossier_for_valid_minimal_fixture(tmp_seed_dir) -> None:
    copy_fixture("valid-minimal", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/generate-seed-dossier.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    dossier = tmp_seed_dir / "seed_dossier.md"
    assert dossier.exists()
    text = dossier.read_text(encoding="utf-8")
    assert "## Status" in text
    assert "## Seed intent" in text
    assert "## Work dev context" in text
    assert "## Work business context" in text


def test_generate_seed_dossier_fails_on_missing_required_json(tmp_seed_dir) -> None:
    copy_fixture("invalid-missing-artifact", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/generate-seed-dossier.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode != 0
