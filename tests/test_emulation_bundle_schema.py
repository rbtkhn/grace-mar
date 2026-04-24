from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import export_emulation_bundle as emulation_module  # noqa: E402


def _envelope_validator():
    jsonschema = pytest.importorskip("jsonschema")
    schema = json.loads(emulation_module.SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validators.validator_for(schema).check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def _valid_emitted_envelope() -> dict:
    return emulation_module.build_emulation_envelope(
        user_id="grace-mar",
        runtime_mode="portable_bundle_only",
        generated_at="2026-04-24T16:00:00Z",
    )


def test_emitted_envelope_validates_against_registry_schema() -> None:
    _envelope_validator().validate(_valid_emitted_envelope())


def test_proposal_return_requires_human_review() -> None:
    validator = _envelope_validator()
    jsonschema = pytest.importorskip("jsonschema")
    bad = copy.deepcopy(_valid_emitted_envelope())
    bad["proposalReturn"]["humanReviewRequired"] = False
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad)


def test_proposal_return_rejects_canonical_surface_touch() -> None:
    validator = _envelope_validator()
    jsonschema = pytest.importorskip("jsonschema")
    bad = copy.deepcopy(_valid_emitted_envelope())
    bad["proposalReturn"]["canonicalSurfacesTouched"] = True
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad)


def test_runtime_observation_requires_human_review() -> None:
    validator = _envelope_validator()
    jsonschema = pytest.importorskip("jsonschema")
    bad = copy.deepcopy(_valid_emitted_envelope())
    bad["runtimeObservationReturn"]["humanReviewRequired"] = False
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad)


def test_runtime_observation_rejects_canonical_surface_touch() -> None:
    validator = _envelope_validator()
    jsonschema = pytest.importorskip("jsonschema")
    bad = copy.deepcopy(_valid_emitted_envelope())
    bad["runtimeObservationReturn"]["canonicalSurfacesTouched"] = True
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad)


def test_unknown_top_level_properties_are_rejected() -> None:
    validator = _envelope_validator()
    jsonschema = pytest.importorskip("jsonschema")
    bad = copy.deepcopy(_valid_emitted_envelope())
    bad["unexpectedTopLevelProperty"] = "not allowed"
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad)
