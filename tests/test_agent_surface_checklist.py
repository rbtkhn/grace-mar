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


def test_agent_surface_validate_accepts_agent_species(tmp_path: Path) -> None:
    p = tmp_path / "ok.yaml"
    p.write_text(
        "\n".join(
            [
                "version: 1",
                "agent_species: coding_harness",
                "runtime: {placement: local}",
                "orchestration: {who_decides: self, notes: ''}",
                "interface: {channels: [], notes: ''}",
                "grace_mar:",
                "  record_authority: companion",
                "  staging_surface: x",
                "  merge_requires_companion_gate: true",
                "  continuity_contract: 'n/a'",
                "  observability: ''",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
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
    assert rc.returncode == 0, rc.stderr + rc.stdout


def test_agent_surface_validate_rejects_bad_agent_species(tmp_path: Path) -> None:
    p = tmp_path / "bad.yaml"
    p.write_text(
        "\n".join(
            [
                "version: 1",
                "agent_species: not_a_species",
                "runtime: {placement: local}",
                "orchestration: {who_decides: self, notes: ''}",
                "interface: {channels: [], notes: ''}",
                "grace_mar:",
                "  record_authority: companion",
                "  staging_surface: x",
                "  merge_requires_companion_gate: true",
                "  continuity_contract: 'n/a'",
                "  observability: ''",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
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
    assert "agent_species" in (rc.stderr + rc.stdout)
