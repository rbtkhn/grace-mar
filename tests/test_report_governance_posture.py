"""Smoke tests for scripts/report_governance_posture.py."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from report_governance_posture import build_governance_posture_markdown  # noqa: E402


def test_build_governance_posture_contains_core_sections(tmp_path: Path) -> None:
    uid = "fixture-user"
    prof = tmp_path / "users" / uid
    prof.mkdir(parents=True)
    (prof / "recursion-gate.md").write_text("# gate\n", encoding="utf-8")
    (prof / "self.md").write_text("x", encoding="utf-8")

    md = build_governance_posture_markdown(
        tmp_path,
        uid,
        generated_at_utc="2099-01-01T00:00:00Z",
        git_ref="testref",
        profile_override=prof,
    )

    assert "# Governance posture (generated)" in md
    assert f"`{uid}`" in md
    assert "## Triad (where authority sits)" in md
    assert "## No silent merge" in md
    assert "## Inspectability" in md
    assert "## Audit file presence" in md
    assert f"users/{uid}/recursion-gate.md" in md
    assert "present" in md
    assert "validate-integrity.py" in md
    assert "run_voice_benchmark.py" in md
    assert "replay_harness_event.py" in md
    assert "2099-01-01" in md
    assert "testref" in md
    assert "_Operator / audit lane only" in md
