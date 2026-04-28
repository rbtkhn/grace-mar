"""Context failure diagnostics clinic — heuristic derived reports (non-canonical)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "runtime" / "context_failure_clinic.py"
SCHEMA_PATH = ROOT / "schemas" / "context-failure-report.v1.schema.json"


def load_module():
    spec = importlib.util.spec_from_file_location("context_failure_clinic", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_authority_drift_is_high_risk(tmp_path: Path) -> None:
    module = load_module()
    artifact = tmp_path / "bad.md"
    artifact.write_text(
        """# Candidate Output

This proposal should auto-approve and merge directly into the canonical Record.

It can update canonical memory without review.
""",
        encoding="utf-8",
    )
    report = module.evaluate_context(artifact)
    assert report.overall_risk == "high"
    assert report.category_scores["authority_drift"] >= 8
    assert any(finding.category == "authority_drift" for finding in report.findings)


def test_missing_evidence_detected_for_strong_claims(tmp_path: Path) -> None:
    module = load_module()
    artifact = tmp_path / "claim.md"
    artifact.write_text(
        """# Analysis

This clearly proves that the prior interpretation was wrong.

Therefore the new conclusion must be adopted.
""",
        encoding="utf-8",
    )
    report = module.evaluate_context(artifact)
    assert report.category_scores["missing_evidence"] >= 6
    assert any(finding.category == "missing_evidence" for finding in report.findings)


def test_compression_loss_detected_without_anchor_receipt(tmp_path: Path) -> None:
    module = load_module()
    artifact = tmp_path / "summary.md"
    artifact.write_text(
        """# Summary

This is a compressed digest of several source files.

It condenses the material into a brief.
""",
        encoding="utf-8",
    )
    report = module.evaluate_context(artifact)
    assert report.category_scores["compression_loss"] >= 5
    assert any(action.category == "compression_loss" for action in report.recommended_actions)


def test_surface_confusion_detected(tmp_path: Path) -> None:
    module = load_module()
    artifact = tmp_path / "surface.md"
    artifact.write_text(
        """# Runtime Note

This runtime note is now canonical.

The derived artifact is the Record.
""",
        encoding="utf-8",
    )
    report = module.evaluate_context(artifact)
    assert report.category_scores["surface_confusion"] >= 7
    assert any(finding.category == "surface_confusion" for finding in report.findings)


def test_json_report_shape(tmp_path: Path) -> None:
    module = load_module()
    artifact = tmp_path / "ok.md"
    artifact.write_text(
        """# Review Note

Source: raw-input/example.md

Evidence: quoted source line.

This is a candidate and requires review before durable adoption.
""",
        encoding="utf-8",
    )
    report = module.evaluate_context(artifact)
    jsonable = module.report_to_jsonable(report)
    assert jsonable["schema_version"] == "context-failure-report.v1"
    assert "overall_risk" in jsonable
    assert "category_scores" in jsonable
    assert "findings" in jsonable
    assert "recommended_actions" in jsonable
    assert "governance_note" in jsonable


def test_emitted_json_validates_against_schema(tmp_path: Path) -> None:
    pytest.importorskip("jsonschema")
    from jsonschema import Draft202012Validator

    module = load_module()
    artifact = tmp_path / "note.md"
    artifact.write_text(
        """# Note

Source: example.md

Candidate only. Review required.

Uncertainty: partial evidence.

Risk: routing ambiguity between work-strategy and strategy-notebook — not sure where this belongs.
""",
        encoding="utf-8",
    )
    report = module.evaluate_context(artifact)
    jsonable = module.report_to_jsonable(report)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(jsonable)


def test_markdown_report_contains_governance_note(tmp_path: Path) -> None:
    module = load_module()
    artifact = tmp_path / "note.md"
    artifact.write_text(
        """# Note

Source: example.md

Candidate only. Review required.
""",
        encoding="utf-8",
    )
    report = module.evaluate_context(artifact)
    markdown = module.report_to_markdown(report)
    assert "Context Failure Diagnostics Report" in markdown
    assert "Governance Note" in markdown
    assert "does not alter canonical" in markdown


def test_report_files_can_be_written(tmp_path: Path) -> None:
    module = load_module()
    artifact = tmp_path / "artifact.md"
    out = tmp_path / "report.json"
    md = tmp_path / "report.md"
    artifact.write_text(
        """# Artifact

This summary is compressed. Source: example.md. Review required.
""",
        encoding="utf-8",
    )
    report = module.evaluate_context(artifact)
    out.write_text(json.dumps(module.report_to_jsonable(report), indent=2), encoding="utf-8")
    md.write_text(module.report_to_markdown(report), encoding="utf-8")
    assert out.exists()
    assert md.exists()
    parsed = json.loads(out.read_text(encoding="utf-8"))
    assert parsed["schema_version"] == "context-failure-report.v1"


def test_cli_main_subprocess_smoke(tmp_path: Path) -> None:
    pytest.importorskip("jsonschema")
    artifact = tmp_path / "in.md"
    artifact.write_text(
        "# X\n\nRuntime note. Source: a.md. Evidence: b. Review required.\n",
        encoding="utf-8",
    )
    out_json = tmp_path / "out.json"
    out_md = tmp_path / "out.md"
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--input",
            str(artifact),
            "--out",
            str(out_json),
            "--markdown",
            str(out_md),
            "--repo-root",
            str(ROOT),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    assert out_json.is_file()
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["schema_version"] == "context-failure-report.v1"
