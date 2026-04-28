"""Skill evaluation clinic — heuristic rubric + derived reports (non-canonical)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "runtime" / "skill_eval_clinic.py"
SCHEMA_PATH = ROOT / "schemas" / "skill-eval-report.v1.schema.json"


def load_module():
    spec = importlib.util.spec_from_file_location("skill_eval_clinic", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_strong_skill_scores_high(tmp_path: Path) -> None:
    module = load_module()
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        """# Test Skill

## When to use

Use this skill for advisory work-lane analysis.

## Boundary rule

This skill may generate staged candidates and derived reports, but it must not alter canonical Record surfaces.

## Evidence posture

Include sources, evidence, warrants, receipts, and uncertainty notes.

## Gate rule

Durable changes must go through the review gate. This skill cannot approve or merge its own recommendations.

## Output

Produce a report with findings and candidate improvements.

## Failure modes

Avoid treating runtime context as durable truth. Do not bypass review.
""",
        encoding="utf-8",
    )
    report = module.evaluate_skill(skill)
    assert report.overall_score >= 85
    assert report.schema_version == "skill-eval-report.v1"


def test_weak_skill_generates_candidate_improvements(tmp_path: Path) -> None:
    module = load_module()
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        """# Weak Skill

Do the thing quickly.
""",
        encoding="utf-8",
    )
    report = module.evaluate_skill(skill)
    assert report.overall_score < 70
    assert len(report.candidate_improvements) >= 3


def test_report_json_shape(tmp_path: Path) -> None:
    module = load_module()
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        """# Minimal Skill

Use this to produce a report. Do not merge anything. Send changes to review.

Evidence and source references are required. Known risk: stale runtime context.
""",
        encoding="utf-8",
    )
    report = module.evaluate_skill(skill)
    jsonable = module.report_to_jsonable(report)
    assert jsonable["schema_version"] == "skill-eval-report.v1"
    assert "scores" in jsonable
    assert "findings" in jsonable
    assert "candidate_improvements" in jsonable
    assert "governance_note" in jsonable


def test_emitted_json_validates_against_schema(tmp_path: Path) -> None:
    pytest.importorskip("jsonschema")
    from jsonschema import Draft202012Validator

    module = load_module()
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        """# Skill

Use this skill to produce advisory reports.

Evidence is required.

Review is required.

Do not edit canonical Record surfaces.

Known failure mode: over-promotion of runtime context.
""",
        encoding="utf-8",
    )
    report = module.evaluate_skill(skill)
    jsonable = module.report_to_jsonable(report)
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(jsonable)


def test_markdown_report_contains_governance_note(tmp_path: Path) -> None:
    module = load_module()
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        """# Skill

Use this skill to produce advisory reports.

Evidence is required.

Review is required.

Do not edit canonical Record surfaces.

Known failure mode: over-promotion of runtime context.
""",
        encoding="utf-8",
    )
    report = module.evaluate_skill(skill)
    markdown = module.report_to_markdown(report)
    assert "Governance Note" in markdown
    assert "does not edit, approve, or merge" in markdown


def test_cli_writes_reports(tmp_path: Path) -> None:
    pytest.importorskip("jsonschema")
    module = load_module()
    skill = tmp_path / "SKILL.md"
    out = tmp_path / "report.json"
    md = tmp_path / "report.md"
    skill.write_text(
        """# Skill

Use this skill when a candidate report is needed.

It must not alter canonical Record surfaces.

It requires evidence, source references, and receipts.

Durable changes must go through review gate approval.

Output a derived report.

Known failure mode: treating runtime context as durable truth.
""",
        encoding="utf-8",
    )
    report = module.evaluate_skill(skill)
    out.write_text(json.dumps(module.report_to_jsonable(report), indent=2), encoding="utf-8")
    md.write_text(module.report_to_markdown(report), encoding="utf-8")
    assert out.exists()
    assert md.exists()
    parsed = json.loads(out.read_text(encoding="utf-8"))
    assert parsed["schema_version"] == "skill-eval-report.v1"


def test_cli_main_subprocess_smoke(tmp_path: Path) -> None:
    pytest.importorskip("jsonschema")
    skill = tmp_path / "SKILL.md"
    skill.write_text(
        "# Skill\n\nUse this skill for advisory runtime analysis.\n\n"
        "Canonical Record surfaces must not be edited.\n\n"
        "Evidence and sources required.\n\n"
        "Gate and review required before merge.\n\n"
        "Output a report.\n\n"
        "Risk: misuse of staged candidates.\n",
        encoding="utf-8",
    )
    out_json = tmp_path / "cli-out.json"
    out_md = tmp_path / "cli-out.md"
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--skill",
            str(skill),
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
    assert out_md.is_file()
    data = json.loads(out_json.read_text(encoding="utf-8"))
    assert data["schema_version"] == "skill-eval-report.v1"
