"""Tests for Workbench receipt generator and validator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VALIDATE = REPO / "scripts" / "work_dev" / "validate_workbench_receipt.py"
NEW = REPO / "scripts" / "work_dev" / "new_workbench_receipt.py"
EXAMPLE = (
    REPO
    / "docs"
    / "skill-work"
    / "work-dev"
    / "workbench"
    / "examples"
    / "strategy-notebook-visualizer-receipt.example.json"
)
PILOT_EXAMPLE = (
    REPO
    / "docs"
    / "skill-work"
    / "work-dev"
    / "workbench"
    / "examples"
    / "strategy-notebook-visualizer-workbench-receipt.example.json"
)


def _run(args: list[str | Path], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *map(str, args)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=check,
    )


def test_validate_example_fixture_passes() -> None:
    p = _run([VALIDATE, EXAMPLE])
    assert p.returncode == 0, p.stderr
    assert "ok" in p.stdout


def test_validate_pilot_workbench_receipt_passes() -> None:
    p = _run([VALIDATE, PILOT_EXAMPLE])
    assert p.returncode == 0, p.stderr
    assert "ok" in p.stdout


def test_validate_fails_on_bad_record_authority(tmp_path) -> None:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["recordAuthority"] = "full"
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    p = _run([VALIDATE, bad], check=False)
    assert p.returncode == 1
    assert "recordAuthority" in p.stderr or "recordAuthority" in p.stdout


def test_validate_fails_on_bad_gate_effect(tmp_path) -> None:
    data = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    data["gateEffect"] = "staged"
    bad = tmp_path / "bad2.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    p = _run([VALIDATE, bad], check=False)
    assert p.returncode == 1


def test_generator_produces_valid_receipt_at_custom_output(tmp_path) -> None:
    out = tmp_path / "gen.json"
    p = _run(
        [
            NEW,
            "-o",
            out,
            "--artifact-type",
            "cli",
            "--launch-command",
            "python3 -c 'print(1)'",
        ]
    )
    assert p.returncode == 0, p.stderr
    assert out.is_file()
    v = _run([VALIDATE, out])
    assert v.returncode == 0, v.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["receiptKind"] == "workbench"
    assert data["status"] == "draft"
    assert data["recordAuthority"] == "none"
    assert data["gateEffect"] == "none"
    assert data["inspection"]["method"] == "pending"


def test_generator_refuses_protected_path() -> None:
    target = (
        REPO
        / "users"
        / "grace-mar"
        / "self.md"
    )
    p = _run(
        [NEW, "-o", target, "--artifact-type", "x"],
        check=False,
    )
    assert p.returncode == 1
    assert "refuse" in p.stderr.lower() or "protected" in p.stderr.lower()
