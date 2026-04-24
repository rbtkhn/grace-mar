from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(rel_path: str) -> dict:
    return json.loads((REPO_ROOT / rel_path).read_text(encoding="utf-8"))


def _validator(rel_path: str):
    jsonschema = pytest.importorskip("jsonschema")
    schema = _load_json(rel_path)
    jsonschema.validators.validator_for(schema).check_schema(schema)
    return jsonschema.Draft202012Validator(schema)


def _valid_docs_contract() -> dict:
    return {
        "metadata": {
            "fork_id": "grace-mar",
            "bundle_version": "1.0.0",
            "exported_at": "2026-04-24T16:00:00Z",
            "checksum": "sha256:test",
        },
        "source": {
            "repo": "grace-mar",
            "branch": "main",
            "commit": "deadbeef",
            "exporter": "scripts/export_emulation_bundle.py",
            "export_mode": "portable_bundle_only",
        },
        "authority": {
            "recordAuthority": "none",
            "gateEffect": "none",
            "canonicalRecordAccess": "read-only",
            "mergeAuthority": "none",
            "proposalAuthority": "stage-only",
            "contradictionAuthority": "proposal-only",
            "workLaneAuthority": "local-runtime-only",
        },
        "bundle": {
            "record_snapshot": "record/fork-export.json",
            "runtime_bundle": "bundle.json",
            "portable_record_prompt": "record/grace-mar-llm.txt",
            "authority_map": "policy/authority-map.json",
            "proposal_schema_ref": "policy/change-proposal.v1.json",
        },
        "behavior_spec": {
            "core_constitution": "behavior-spec/v1-core-constitution.md",
            "record_boundaries": "behavior-spec/v1-record-boundaries.md",
            "contradiction_policy": "behavior-spec/v1-contradiction-policy.md",
            "proposal_envelope": "behavior-spec/v1-proposal-envelope.md",
            "work_lane_policy": "behavior-spec/v1-work-lane-policy.md",
        },
        "governance": {
            "proposal_schema_ref": "policy/change-proposal.v1.json",
            "authority_map_ref": "policy/authority-map.json",
            "import_path_ref": "scripts/runtime/import_runtime_observation.py",
            "review_path_ref": "users/grace-mar/recursion-gate.md",
        },
        "audit": {
            "manifest": "manifest.json",
            "checksums": ["bundle.json:sha256:test"],
            "export_receipt": "receipt.json",
            "warnings": [],
        },
    }


def _valid_emitted_envelope() -> dict:
    return {
        "$schema": "schema-registry/emulation-bundle-envelope.v1.json",
        "schemaVersion": "1.0.0",
        "format": "grace-mar-emulation-bundle",
        "generatedAt": "2026-04-24T16:00:00Z",
        "userId": "grace-mar",
        "runtimeMode": "portable_bundle_only",
        "runtimeBundlePath": "bundle.json",
        "references": {
            "prpPath": "record/grace-mar-llm.txt",
            "forkExportPath": "record/fork-export.json",
            "authorityMapPath": "policy/authority-map.json",
            "changeProposalSchemaPath": "policy/change-proposal.v1.json",
        },
        "boundaryNotice": "Foreign runtimes remain non-authoritative.",
        "proposalReturn": {
            "schemaPath": "policy/change-proposal.v1.json",
            "humanReviewRequired": True,
            "canonicalSurfacesTouched": False,
        },
        "runtimeObservationReturn": {
            "importScript": "scripts/runtime/import_runtime_observation.py",
            "humanReviewRequired": True,
            "canonicalSurfacesTouched": False,
        },
        "adapterExamples": [],
    }


def test_emulation_contract_schema_parses() -> None:
    schema = _load_json("docs/portability/emulation/emulation-bundle-schema.v1.json")
    assert schema["title"] == "Portable emulation bundle contract"
    assert schema["type"] == "object"


def test_emulation_contract_schema_enforces_authority_constants() -> None:
    schema = _load_json("docs/portability/emulation/emulation-bundle-schema.v1.json")
    authority = schema["properties"]["authority"]["properties"]
    assert authority["recordAuthority"]["const"] == "none"
    assert authority["gateEffect"]["const"] == "none"
    assert authority["mergeAuthority"]["const"] == "none"
    assert authority["proposalAuthority"]["const"] == "stage-only"
    assert authority["contradictionAuthority"]["const"] == "proposal-only"
    assert authority["workLaneAuthority"]["const"] == "local-runtime-only"
    assert authority["canonicalRecordAccess"]["enum"] == ["read-only", "none"]


def test_current_emitted_envelope_schema_still_parses() -> None:
    schema = _load_json("schema-registry/emulation-bundle-envelope.v1.json")
    assert schema["properties"]["format"]["const"] == "grace-mar-emulation-bundle"
    assert schema["properties"]["proposalReturn"]["properties"]["humanReviewRequired"]["const"] is True
    assert (
        schema["properties"]["runtimeObservationReturn"]["properties"]["canonicalSurfacesTouched"]["const"]
        is False
    )


def test_docs_contract_validator_accepts_minimal_valid_instance() -> None:
    _validator("docs/portability/emulation/emulation-bundle-schema.v1.json").validate(
        _valid_docs_contract()
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("recordAuthority", "read-only"),
        ("gateEffect", "review-required"),
        ("mergeAuthority", "human-review"),
    ],
)
def test_docs_contract_rejects_authority_escalation(field: str, value: str) -> None:
    validator = _validator("docs/portability/emulation/emulation-bundle-schema.v1.json")
    jsonschema = pytest.importorskip("jsonschema")
    bad = copy.deepcopy(_valid_docs_contract())
    bad["authority"][field] = value
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad)


def test_emitted_envelope_validator_accepts_valid_instance() -> None:
    _validator("schema-registry/emulation-bundle-envelope.v1.json").validate(
        _valid_emitted_envelope()
    )


def test_emitted_envelope_rejects_proposal_return_without_human_review() -> None:
    validator = _validator("schema-registry/emulation-bundle-envelope.v1.json")
    jsonschema = pytest.importorskip("jsonschema")
    bad = copy.deepcopy(_valid_emitted_envelope())
    bad["proposalReturn"]["humanReviewRequired"] = False
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad)


def test_emitted_envelope_rejects_runtime_observation_touching_canonical_surfaces() -> None:
    validator = _validator("schema-registry/emulation-bundle-envelope.v1.json")
    jsonschema = pytest.importorskip("jsonschema")
    bad = copy.deepcopy(_valid_emitted_envelope())
    bad["runtimeObservationReturn"]["canonicalSurfacesTouched"] = True
    with pytest.raises(jsonschema.ValidationError):
        validator.validate(bad)
