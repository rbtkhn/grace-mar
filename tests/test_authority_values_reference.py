from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_reference() -> dict:
    path = REPO_ROOT / "schema-registry" / "authority-values.v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


def test_authority_values_reference_parses_as_json() -> None:
    data = _load_reference()
    assert data["version"] == "authority-values-v1"


def test_authority_values_reference_has_required_top_level_keys() -> None:
    data = _load_reference()
    assert set(data) >= {"version", "fields", "safe_combinations", "unsafe_values"}


def test_authority_values_reference_lists_expected_fields() -> None:
    data = _load_reference()
    fields = data["fields"]
    assert set(fields) >= {
        "recordAuthority",
        "gateEffect",
        "mergeAuthority",
        "canonicalRecordAccess",
        "proposalAuthority",
        "contradictionAuthority",
        "workLaneAuthority",
        "simulationOnly",
        "requires_human_review",
    }


def test_merge_authority_allows_only_none() -> None:
    data = _load_reference()
    assert data["fields"]["mergeAuthority"] == ["none"]


def test_record_authority_allows_only_none() -> None:
    data = _load_reference()
    assert data["fields"]["recordAuthority"] == ["none"]


def test_simulation_only_allows_only_true() -> None:
    data = _load_reference()
    assert data["fields"]["simulationOnly"] == [True]


def test_portable_emulation_safe_combination_has_no_merge_authority() -> None:
    data = _load_reference()
    combo = data["safe_combinations"]["portable_emulation"]
    assert combo["mergeAuthority"] == "none"


def test_counterfactual_simulation_safe_combination_is_simulation_only() -> None:
    data = _load_reference()
    combo = data["safe_combinations"]["counterfactual_simulation"]
    assert combo["simulationOnly"] is True


def test_interface_artifact_safe_combination_keeps_non_authority_boundary() -> None:
    data = _load_reference()
    combo = data["safe_combinations"]["interface_artifact"]
    assert combo["recordAuthority"] == "none"
    assert combo["gateEffect"] == "none"
