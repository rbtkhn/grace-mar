"""Skill card schema and builder — derived artifacts only."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO / "schema-registry" / "skill-card.v1.json"


@pytest.fixture(scope="module")
def jsonschema_validator():
    pytest.importorskip("yaml")
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def test_skill_card_schema_self_validates(jsonschema_validator):
    from jsonschema import validators

    meta = jsonschema_validator.schema
    validators.validator_for(meta).check_schema(meta)


def test_build_one_skill_card_validates(jsonschema_validator):
    import build_skill_cards

    rows = [
        {
            "name": "politics-massie",
            "source": "politics-massie/SKILL.md",
            "appendix": ".cursor/skills/politics-massie/CURSOR_APPENDIX.md",
            "target": ".cursor/skills/politics-massie/SKILL.md",
        }
    ]
    card = build_skill_cards.build_card_for_skill(rows[0])
    jsonschema_validator.validate(card)


def test_manifest_skills_emit_valid_cards(jsonschema_validator):
    pytest.importorskip("yaml")
    import build_skill_cards

    for row in build_skill_cards._load_manifest():
        card = build_skill_cards.build_card_for_skill(row)
        jsonschema_validator.validate(card)


def test_validate_card_catches_invalid():
    """_validate_card returns errors for invalid cards."""
    import build_skill_cards

    bad_card = {"skill_id": "x"}
    errs = build_skill_cards._validate_card(bad_card)
    assert len(errs) > 0, "should catch missing required fields"


def test_validate_card_passes_valid():
    """_validate_card returns empty list for valid cards."""
    import build_skill_cards

    rows = build_skill_cards._load_manifest()
    if rows:
        card = build_skill_cards.build_card_for_skill(rows[0])
        errs = build_skill_cards._validate_card(card)
        assert errs == [], f"unexpected errors: {errs}"


def test_completeness_score():
    """_completeness_score reports field presence."""
    import build_skill_cards

    card = {
        "skill_id": "test",
        "title": "Test",
        "purpose": "(no description in frontmatter)",
        "runtime_snippet": "snippet",
        "operator_view": "",
        "source_path": "skills-portable/test/SKILL.md",
        "last_updated": "2026-01-01T00:00:00Z",
    }
    score = build_skill_cards._completeness_score(card)
    assert score["has_purpose"] is False
    assert score["has_snippet"] is True
    assert score["has_operator_view"] is False
    assert score["has_source_path"] is True


def test_check_flag_subprocess(tmp_path):
    """--check flag validates all manifest cards and exits 0 if valid."""
    import subprocess, sys

    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "build_skill_cards.py"),
         "--out-dir", str(tmp_path), "--check"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr


def test_report_flag_subprocess(tmp_path):
    """--report flag emits completeness JSON."""
    import subprocess, sys, json

    r = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "build_skill_cards.py"),
         "--out-dir", str(tmp_path), "--report"],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    report = json.loads(r.stdout)
    assert "total_cards" in report
    assert "completeness_rate" in report
    assert report["completeness_rate"] >= 0.0
