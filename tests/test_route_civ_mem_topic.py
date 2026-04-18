"""Tests for scripts/route_civ_mem_topic.py (topic routing)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from route_civ_mem_topic import (  # noqa: E402
    _focus_is_valid,
    _pick_profile,
    _score_profile,
    extract_mem_connection_ids,
)


MINIMAL_CFG = {
    "routing_rules_version": 1,
    "default_profile": "latin_catholic_sphere",
    "profiles": {
        "latin_catholic_sphere": {
            "priority": 20,
            "required_tokens": [],
            "keywords": ["pope", "vatican", "italy", "mexico"],
            "primary_civ": "ROME",
            "secondary_civs": ["FRANCE", "AMERICA"],
            "attention_pct": {"rome": 70, "france": 15, "america": 15},
            "max_cross_civ_edges": 4,
        },
        "mediterranean_islam_christian_encounter": {
            "priority": 25,
            "required_tokens": [],
            "keywords": ["mosque", "islam", "algiers", "maghreb"],
            "primary_civ": "ISLAM",
            "secondary_civs": ["ROME", "FRANCE"],
            "attention_pct": {"islam": 45, "rome": 35, "france": 10},
            "max_cross_civ_edges": 4,
        },
    },
}


def test_pick_profile_papal_latin() -> None:
    pid, prof, _audit = _pick_profile(
        MINIMAL_CFG, "Pope Leo Vatican visit Italy", None, None, focus_active=False
    )
    assert pid == "latin_catholic_sphere"
    assert prof["primary_civ"] == "ROME"


def test_pick_profile_mosque_islam() -> None:
    pid, prof, _audit = _pick_profile(
        MINIMAL_CFG, "Grand mosque Algiers islam dialogue", None, None, focus_active=False
    )
    assert pid == "mediterranean_islam_christian_encounter"
    assert prof["primary_civ"] == "ISLAM"


def test_pick_profile_override() -> None:
    pid, prof, audit = _pick_profile(
        MINIMAL_CFG, "anything", "latin_catholic_sphere", None, focus_active=False
    )
    assert pid == "latin_catholic_sphere"
    assert audit.get("reason") == "profile_override"


def test_pick_profile_default_when_no_keyword_match() -> None:
    pid, prof, _audit = _pick_profile(
        MINIMAL_CFG, "quantum computing", None, None, focus_active=False
    )
    assert pid == "latin_catholic_sphere"


def test_focus_expired_no_bonus() -> None:
    focus = {
        "focus_version": 1,
        "valid_from": "2000-01-01",
        "valid_until": "2000-12-31",
        "profile_overlap_bonus": {"latin_catholic_sphere": 99},
        "sticky_keywords": [],
    }
    pid, _prof, audit = _pick_profile(
        MINIMAL_CFG, "quantum computing", None, focus, focus_active=_focus_is_valid(focus)
    )
    assert pid == "latin_catholic_sphere"
    assert audit["per_profile"]["latin_catholic_sphere"]["effective_overlap"] == 0


def test_focus_bonus_flips_to_mediterranean() -> None:
    focus = {
        "focus_version": 1,
        "valid_from": "2000-01-01",
        "valid_until": "2099-12-31",
        "profile_overlap_bonus": {"mediterranean_islam_christian_encounter": 3},
        "sticky_keywords": [],
    }
    active = _focus_is_valid(focus)
    pid, prof, audit = _pick_profile(
        MINIMAL_CFG, "quantum computing", None, focus, focus_active=active
    )
    assert active is True
    assert pid == "mediterranean_islam_christian_encounter"
    assert prof["primary_civ"] == "ISLAM"
    assert audit["per_profile"]["mediterranean_islam_christian_encounter"][
        "effective_overlap"
    ] == 3


def test_sticky_keyword_bonus() -> None:
    focus = {
        "focus_version": 1,
        "valid_from": "2000-01-01",
        "valid_until": "2099-12-31",
        "profile_overlap_bonus": {},
        "sticky_keywords": [
            {"keyword": "hormuz", "profile": "latin_catholic_sphere", "bonus": 2}
        ],
    }
    active = _focus_is_valid(focus)
    pid, _prof, audit = _pick_profile(
        MINIMAL_CFG, "Strait of Hormuz traffic", None, focus, focus_active=active
    )
    assert pid == "latin_catholic_sphere"
    assert audit["per_profile"]["latin_catholic_sphere"]["sticky_bonus"] == 2
    assert audit["per_profile"]["latin_catholic_sphere"]["effective_overlap"] == 2


def test_extract_mem_connections_ordering() -> None:
    fixture = """
MEM CONNECTIONS
• MEM–RUSSIA–THIRD–ROME — rival
• MEM–ROME–CRUSADES — test
• MEM–ROME–CITY — anchor
"""
    ids = extract_mem_connection_ids(
        fixture, max_edges=10, prefer_rome_prefix=True
    )
    assert ids[0].startswith("MEM–ROME–")
    assert "MEM–RUSSIA–THIRD–ROME" in ids


def test_score_profile_required_tokens_disqualifies() -> None:
    cfg = {
        "priority": 10,
        "required_tokens": ["musthave"],
        "keywords": ["foo"],
    }
    overlap, pri = _score_profile(cfg, "foo bar")
    assert overlap == -1


@pytest.mark.skipif(
    not (REPO_ROOT / "config" / "civ_mem_topic_routes.yaml").is_file(),
    reason="config missing",
)
def test_yaml_loads() -> None:
    import yaml

    p = REPO_ROOT / "config" / "civ_mem_topic_routes.yaml"
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    assert "profiles" in data
    assert "latin_catholic_sphere" in data["profiles"]
