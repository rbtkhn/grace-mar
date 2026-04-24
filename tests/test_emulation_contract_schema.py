from __future__ import annotations

import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_json(rel_path: str) -> dict:
    return json.loads((REPO_ROOT / rel_path).read_text(encoding="utf-8"))


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
