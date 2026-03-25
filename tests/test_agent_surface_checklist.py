"""agent_surface_checklist.py — template path and validation."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_agent_surface_template_validates() -> None:
    tmpl = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "agent-surface-template.yaml"
    rc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "work_dev" / "agent_surface_checklist.py"),
            "--validate",
            str(tmpl),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert rc.returncode == 0, rc.stderr + rc.stdout


def test_agent_surface_validate_rejects_empty_root(tmp_path: Path) -> None:
    p = tmp_path / "x.yaml"
    p.write_text("foo: bar\n", encoding="utf-8")
    rc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "work_dev" / "agent_surface_checklist.py"),
            "--validate",
            str(p),
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert rc.returncode != 0
