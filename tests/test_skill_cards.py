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
