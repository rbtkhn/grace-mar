"""End-to-end smoke: validate + dossier in a synthetic user dir."""

from __future__ import annotations

from tests.conftest import REPO_ROOT, copy_fixture, repo_python, run_cmd


def test_seed_phase_e2e_valid_fixture(tmp_path) -> None:
    user_dir = tmp_path / "users" / "synthetic-user" / "seed-phase"
    user_dir.mkdir(parents=True, exist_ok=True)
    copy_fixture("valid-minimal", user_dir)

    validate = run_cmd(
        [repo_python(), "scripts/validate-seed-phase.py", str(user_dir)],
        cwd=REPO_ROOT,
    )
    assert validate.returncode == 0, validate.stderr or validate.stdout

    dossier = run_cmd(
        [repo_python(), "scripts/generate-seed-dossier.py", str(user_dir)],
        cwd=REPO_ROOT,
    )
    assert dossier.returncode == 0, dossier.stderr or dossier.stdout

    assert (user_dir / "seed_dossier.md").exists()
    text = (user_dir / "seed_dossier.md").read_text(encoding="utf-8")
    assert "## Activation Recommendation" in text
