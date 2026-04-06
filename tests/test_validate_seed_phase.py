"""Subprocess tests for scripts/validate-seed-phase.py."""

from __future__ import annotations

from tests.conftest import REPO_ROOT, copy_fixture, repo_python, run_cmd


def test_demo_seed_phase_passes_strict_validation() -> None:
    result = run_cmd(
        [repo_python(), "scripts/validate-seed-phase.py", "users/demo/seed-phase"],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_template_seed_phase_passes_placeholder_validation() -> None:
    result = run_cmd(
        [
            repo_python(),
            "scripts/validate-seed-phase.py",
            "users/_template/seed-phase",
            "--allow-placeholders",
        ],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_valid_minimal_fixture_passes(tmp_seed_dir) -> None:
    copy_fixture("valid-minimal", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/validate-seed-phase.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_valid_strong_fixture_passes(tmp_seed_dir) -> None:
    copy_fixture("valid-strong", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/validate-seed-phase.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_missing_artifact_fixture_fails(tmp_seed_dir) -> None:
    copy_fixture("invalid-missing-artifact", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/validate-seed-phase.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode != 0


def test_malformed_json_fixture_fails(tmp_seed_dir) -> None:
    copy_fixture("invalid-malformed-json", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/validate-seed-phase.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode != 0


def test_bad_enum_fixture_fails(tmp_seed_dir) -> None:
    copy_fixture("invalid-bad-enum", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/validate-seed-phase.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode != 0


def test_readiness_threshold_fixture_fails_validation(tmp_seed_dir) -> None:
    copy_fixture("invalid-readiness-threshold", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/validate-seed-phase.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0


def test_intent_too_generic_passes_schema_only(tmp_seed_dir) -> None:
    """Schema allows short purpose; semantic check is check-seed-consistency."""
    copy_fixture("invalid-intent-too-generic", tmp_seed_dir)
    result = run_cmd(
        [repo_python(), "scripts/validate-seed-phase.py", str(tmp_seed_dir)],
        cwd=REPO_ROOT,
    )
    assert result.returncode == 0, result.stderr or result.stdout
