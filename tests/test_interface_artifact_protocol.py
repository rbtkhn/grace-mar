"""Tests for interface artifact metadata generator and validator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VALIDATE = REPO / "scripts" / "work_dev" / "validate_interface_artifact.py"
NEW = REPO / "scripts" / "work_dev" / "new_interface_artifact.py"


def _run(args: list[str | Path], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *map(str, args)],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=check,
    )


def _example_data() -> dict:
    return {
        "artifactId": "iface-20260424-example",
        "title": "Strategy Notebook Structure Map",
        "artifactKind": "html-visualizer",
        "status": "draft",
        "sourceInputs": ["docs/skill-work/work-strategy/strategy-notebook/"],
        "generatedPaths": [
            "artifacts/work-dev/interface-artifacts/strategy-notebook-map.html"
        ],
        "intendedUse": "Help the operator inspect strategy-notebook structure.",
        "mutationScope": "runtime-only",
        "canonicalRecordAccess": "none",
        "recordAuthority": "none",
        "gateEffect": "none",
        "inspectionStatus": "not-inspected",
        "relatedWorkbenchReceipt": None,
        "typicalNextStep": "inspect-in-workbench",
        "sourceContractRef": (
            "docs/skill-work/work-strategy/strategy-notebook/"
            "demo-runs/workbench-visualizer/README.md"
        ),
    }


def test_new_interface_artifact_creates_valid_json(tmp_path) -> None:
    out = tmp_path / "artifact.json"
    created = _run(
        [
            NEW,
            "--title",
            "Example Interface Artifact",
            "--artifact-kind",
            "html-visualizer",
            "--generated-path",
            "artifacts/work-dev/interface-artifacts/example.html",
            "--source-input",
            "docs/skill-work/work-strategy/strategy-notebook",
            "--intended-use",
            "Example protocol smoke test",
            "--output",
            out,
        ]
    )
    assert created.returncode == 0, created.stderr
    assert out.is_file()
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["artifactKind"] == "html-visualizer"
    assert data["status"] == "draft"
    assert data["recordAuthority"] == "none"
    assert data["gateEffect"] == "none"
    assert data["inspectionStatus"] == "not-inspected"
    assert data["typicalNextStep"] == "inspect-in-workbench"

    validated = _run([VALIDATE, out])
    assert validated.returncode == 0, validated.stderr
    assert "ok" in validated.stdout


def test_validator_rejects_record_authority_not_none(tmp_path) -> None:
    data = _example_data()
    data["recordAuthority"] = "full"
    bad = tmp_path / "bad-record.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    result = _run([VALIDATE, bad], check=False)
    assert result.returncode == 1
    assert "recordAuthority" in result.stderr


def test_validator_rejects_gate_effect_not_none(tmp_path) -> None:
    data = _example_data()
    data["gateEffect"] = "staged"
    bad = tmp_path / "bad-gate.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    result = _run([VALIDATE, bad], check=False)
    assert result.returncode == 1
    assert "gateEffect" in result.stderr


def test_validator_rejects_canonical_record_access_outside_allowed_values(
    tmp_path,
) -> None:
    data = _example_data()
    data["canonicalRecordAccess"] = "indirect via review flow"
    bad = tmp_path / "bad-access.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    result = _run([VALIDATE, bad], check=False)
    assert result.returncode == 1
    assert "canonicalRecordAccess" in result.stderr


def test_validator_rejects_unknown_artifact_kind(tmp_path) -> None:
    data = _example_data()
    data["artifactKind"] = "electron-app"
    bad = tmp_path / "bad-kind.json"
    bad.write_text(json.dumps(data), encoding="utf-8")
    result = _run([VALIDATE, bad], check=False)
    assert result.returncode == 1
    assert "artifactKind" in result.stderr
