"""Tests for MCP execution receipt schema and mcp_receipt_lib validation."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

pytest.importorskip("jsonschema")


@pytest.fixture(autouse=True)
def _scripts_on_path() -> None:
    p = str(REPO_ROOT / "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)


def _load_configs():
    from mcp_receipt_lib import BINDINGS_PATH, CAPABILITIES_PATH, load_yaml

    return load_yaml(CAPABILITIES_PATH), load_yaml(BINDINGS_PATH)


def test_valid_github_readonly_receipt_passes() -> None:
    from mcp_receipt_lib import RECEIPT_SCHEMA_PATH, capability_by_id, validate_mcp_receipt

    caps, binds = _load_configs()
    cap = capability_by_id(caps, "github_readonly")
    assert cap is not None

    receipt = {
        "schema_version": 1,
        "receipt_id": "fixture_github_ro",
        "created_at_utc": "2026-04-28T12:00:00Z",
        "actor": {"kind": "assistant", "name": "test"},
        "capability": {
            "id": "github_readonly",
            "category": cap["category"],
            "output_lane": cap["output_lane"],
        },
        "authority": {
            "authority_surface": "bridge_packets",
            "authority_class": "ephemeral_only",
            "gate_required_for_record_change": False,
        },
        "declared_intent": "Read issues",
        "inputs": {"operator_supplied_refs": ["config/foo.yaml"]},
        "access": {
            "network_access": "read",
            "credential_use": "optional",
            "resources_read": ["config/foo.yaml"],
            "resources_written": [],
        },
        "result": {"status": "success", "summary": "ok", "artifacts": []},
        "governance": {
            "durable_state_write_attempted": False,
            "canonical_record_touched": False,
            "requires_human_review": False,
            "requires_gate_review": False,
            "prohibited_action_attempted": False,
            "prohibited_action_notes": [],
        },
        "integrity": {"repo_git_ref": "abc1234"},
    }
    viols, _warns = validate_mcp_receipt(receipt, caps, binds, schema_path=RECEIPT_SCHEMA_PATH)
    assert viols == []


def test_unknown_capability_fails() -> None:
    from mcp_receipt_lib import RECEIPT_SCHEMA_PATH, validate_mcp_receipt

    caps, binds = _load_configs()
    receipt = {
        "schema_version": 1,
        "receipt_id": "x",
        "created_at_utc": "2026-04-28T12:00:00Z",
        "actor": {"kind": "script", "name": "t"},
        "capability": {"id": "no_such_capability_xyz", "category": "web", "output_lane": "runtime_only"},
        "authority": {
            "authority_surface": "bridge_packets",
            "authority_class": "ephemeral_only",
            "gate_required_for_record_change": False,
        },
        "declared_intent": "x",
        "inputs": {"operator_supplied_refs": []},
        "access": {
            "network_access": "none",
            "credential_use": "none",
            "resources_read": [],
            "resources_written": [],
        },
        "result": {"status": "failed", "summary": "x", "artifacts": []},
        "governance": {
            "durable_state_write_attempted": False,
            "canonical_record_touched": False,
            "requires_human_review": False,
            "requires_gate_review": False,
            "prohibited_action_attempted": False,
            "prohibited_action_notes": [],
        },
        "integrity": {"repo_git_ref": "abc"},
    }
    viols, _ = validate_mcp_receipt(receipt, caps, binds, schema_path=RECEIPT_SCHEMA_PATH)
    assert any("unknown capability" in v.lower() for v in viols)


def test_readonly_writes_nonempty_fails() -> None:
    from mcp_receipt_lib import RECEIPT_SCHEMA_PATH, capability_by_id, validate_mcp_receipt

    caps, binds = _load_configs()
    cap = capability_by_id(caps, "filesystem_readonly")
    assert cap is not None
    receipt = {
        "schema_version": 1,
        "receipt_id": "w",
        "created_at_utc": "2026-04-28T12:00:00Z",
        "actor": {"kind": "assistant", "name": "t"},
        "capability": {
            "id": "filesystem_readonly",
            "category": cap["category"],
            "output_lane": cap["output_lane"],
        },
        "authority": {
            "authority_surface": "bridge_packets",
            "authority_class": "ephemeral_only",
            "gate_required_for_record_change": False,
        },
        "declared_intent": "x",
        "inputs": {"operator_supplied_refs": []},
        "access": {
            "network_access": "none",
            "credential_use": "none",
            "resources_read": [],
            "resources_written": ["/tmp/oops"],
        },
        "result": {"status": "success", "summary": "bad", "artifacts": []},
        "governance": {
            "durable_state_write_attempted": False,
            "canonical_record_touched": False,
            "requires_human_review": False,
            "requires_gate_review": False,
            "prohibited_action_attempted": False,
            "prohibited_action_notes": [],
        },
        "integrity": {"repo_git_ref": "abc"},
    }
    viols, _ = validate_mcp_receipt(receipt, caps, binds, schema_path=RECEIPT_SCHEMA_PATH)
    assert any("resources_written must be empty" in v for v in viols)


def test_candidate_proposal_without_human_review_fails() -> None:
    from mcp_receipt_lib import RECEIPT_SCHEMA_PATH, capability_by_id, validate_mcp_receipt

    caps, binds = _load_configs()
    cap = capability_by_id(caps, "github_patch_proposal")
    assert cap is not None
    receipt = {
        "schema_version": 1,
        "receipt_id": "cp",
        "created_at_utc": "2026-04-28T12:00:00Z",
        "actor": {"kind": "coding_agent", "name": "t"},
        "capability": {
            "id": "github_patch_proposal",
            "category": cap["category"],
            "output_lane": cap["output_lane"],
        },
        "authority": {
            "authority_surface": "governed_state",
            "authority_class": "review_required",
            "gate_required_for_record_change": True,
        },
        "declared_intent": "draft pr",
        "inputs": {"operator_supplied_refs": []},
        "access": {
            "network_access": "full",
            "credential_use": "required",
            "resources_read": [],
            "resources_written": ["draft_branch_only"],
        },
        "result": {"status": "partial", "summary": "draft", "artifacts": []},
        "governance": {
            "durable_state_write_attempted": False,
            "canonical_record_touched": False,
            "requires_human_review": False,
            "requires_gate_review": True,
            "prohibited_action_attempted": False,
            "prohibited_action_notes": [],
        },
        "integrity": {"repo_git_ref": "abc"},
    }
    viols, _ = validate_mcp_receipt(receipt, caps, binds, schema_path=RECEIPT_SCHEMA_PATH)
    assert any("requires_human_review" in v for v in viols)


def test_evidence_stub_without_gate_review_fails() -> None:
    from mcp_receipt_lib import RECEIPT_SCHEMA_PATH, capability_by_id, validate_mcp_receipt

    caps, binds = _load_configs()
    cap = capability_by_id(caps, "evidence_stub_operator_template")
    assert cap is not None
    receipt = {
        "schema_version": 1,
        "receipt_id": "ev",
        "created_at_utc": "2026-04-28T12:00:00Z",
        "actor": {"kind": "assistant", "name": "t"},
        "capability": {
            "id": "evidence_stub_operator_template",
            "category": cap["category"],
            "output_lane": cap["output_lane"],
        },
        "authority": {
            "authority_surface": "evidence",
            "authority_class": "draftable",
            "gate_required_for_record_change": True,
        },
        "declared_intent": "stub",
        "inputs": {"operator_supplied_refs": []},
        "access": {
            "network_access": "none",
            "credential_use": "none",
            "resources_read": [],
            "resources_written": ["artifacts/evidence-stubs/x.md"],
        },
        "result": {"status": "success", "summary": "stubbed", "artifacts": []},
        "governance": {
            "durable_state_write_attempted": False,
            "canonical_record_touched": False,
            "requires_human_review": False,
            "requires_gate_review": False,
            "prohibited_action_attempted": False,
            "prohibited_action_notes": [],
        },
        "integrity": {"repo_git_ref": "abc"},
    }
    viols, _ = validate_mcp_receipt(receipt, caps, binds, schema_path=RECEIPT_SCHEMA_PATH)
    assert any("evidence_stub" in v and "requires_gate_review" in v for v in viols)


def test_durable_attempt_wrong_authority_class_fails() -> None:
    from mcp_receipt_lib import RECEIPT_SCHEMA_PATH, capability_by_id, validate_mcp_receipt

    caps, binds = _load_configs()
    cap = capability_by_id(caps, "github_readonly")
    assert cap is not None
    receipt = {
        "schema_version": 1,
        "receipt_id": "d",
        "created_at_utc": "2026-04-28T12:00:00Z",
        "actor": {"kind": "assistant", "name": "t"},
        "capability": {
            "id": "github_readonly",
            "category": cap["category"],
            "output_lane": cap["output_lane"],
        },
        "authority": {
            "authority_surface": "bridge_packets",
            "authority_class": "ephemeral_only",
            "gate_required_for_record_change": False,
        },
        "declared_intent": "x",
        "inputs": {"operator_supplied_refs": []},
        "access": {
            "network_access": "read",
            "credential_use": "optional",
            "resources_read": [],
            "resources_written": [],
        },
        "result": {"status": "partial", "summary": "x", "artifacts": []},
        "governance": {
            "durable_state_write_attempted": True,
            "canonical_record_touched": False,
            "requires_human_review": False,
            "requires_gate_review": False,
            "prohibited_action_attempted": False,
            "prohibited_action_notes": [],
        },
        "integrity": {"repo_git_ref": "abc"},
    }
    viols, _ = validate_mcp_receipt(receipt, caps, binds, schema_path=RECEIPT_SCHEMA_PATH)
    assert any("durable_state_write_attempted" in v for v in viols)


def test_success_with_prohibited_action_attempted_fails() -> None:
    from mcp_receipt_lib import RECEIPT_SCHEMA_PATH, capability_by_id, validate_mcp_receipt

    caps, binds = _load_configs()
    cap = capability_by_id(caps, "web_research")
    assert cap is not None
    receipt = {
        "schema_version": 1,
        "receipt_id": "bad",
        "created_at_utc": "2026-04-28T12:00:00Z",
        "actor": {"kind": "assistant", "name": "t"},
        "capability": {
            "id": "web_research",
            "category": cap["category"],
            "output_lane": cap["output_lane"],
        },
        "authority": {
            "authority_surface": "prepared_context",
            "authority_class": "draftable",
            "gate_required_for_record_change": True,
        },
        "declared_intent": "fetch",
        "inputs": {"operator_supplied_refs": []},
        "access": {
            "network_access": "read",
            "credential_use": "none",
            "resources_read": [],
            "resources_written": [],
        },
        "result": {"status": "success", "summary": "nope", "artifacts": []},
        "governance": {
            "durable_state_write_attempted": False,
            "canonical_record_touched": False,
            "requires_human_review": False,
            "requires_gate_review": False,
            "prohibited_action_attempted": True,
            "prohibited_action_notes": ["blocked"],
        },
        "integrity": {"repo_git_ref": "abc"},
    }
    viols, _ = validate_mcp_receipt(receipt, caps, binds, schema_path=RECEIPT_SCHEMA_PATH)
    assert any("success" in v.lower() and "prohibited" in v.lower() for v in viols)


def test_credential_use_exceeds_capability_none_fails() -> None:
    from mcp_receipt_lib import RECEIPT_SCHEMA_PATH, capability_by_id, validate_mcp_receipt

    caps, binds = _load_configs()
    cap = capability_by_id(caps, "filesystem_readonly")
    assert cap is not None
    receipt = {
        "schema_version": 1,
        "receipt_id": "cred",
        "created_at_utc": "2026-04-28T12:00:00Z",
        "actor": {"kind": "assistant", "name": "t"},
        "capability": {
            "id": "filesystem_readonly",
            "category": cap["category"],
            "output_lane": cap["output_lane"],
        },
        "authority": {
            "authority_surface": "bridge_packets",
            "authority_class": "ephemeral_only",
            "gate_required_for_record_change": False,
        },
        "declared_intent": "x",
        "inputs": {"operator_supplied_refs": []},
        "access": {
            "network_access": "none",
            "credential_use": "optional",
            "resources_read": [],
            "resources_written": [],
        },
        "result": {"status": "failed", "summary": "no", "artifacts": []},
        "governance": {
            "durable_state_write_attempted": False,
            "canonical_record_touched": False,
            "requires_human_review": False,
            "requires_gate_review": False,
            "prohibited_action_attempted": False,
            "prohibited_action_notes": [],
        },
        "integrity": {"repo_git_ref": "abc"},
    }
    viols, _ = validate_mcp_receipt(receipt, caps, binds, schema_path=RECEIPT_SCHEMA_PATH)
    assert any("credential_use" in v for v in viols)


def test_generated_receipt_resolves_authority_like_binding(tmp_path: Path) -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "mcp_receipt.py"),
            "--capability-id",
            "database_readonly",
            "--actor-kind",
            "script",
            "--actor-name",
            "pytest",
            "--intent",
            "fixture",
            "--resources-read",
            "config/mcp-capabilities.yaml",
            "--status",
            "success",
            "--summary",
            "authority binding check",
            "-o",
            str(tmp_path / "db.json"),
            "--repo-root",
            str(REPO_ROOT),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads((tmp_path / "db.json").read_text(encoding="utf-8"))
    assert data["authority"]["authority_surface"] == "bridge_packets"
    assert data["authority"]["authority_class"] == "ephemeral_only"
    assert data["authority"]["gate_required_for_record_change"] is False


def test_receipt_hash_roundtrip() -> None:
    from mcp_receipt_lib import capability_by_id, receipt_sha256_hex

    caps, binds = _load_configs()
    cap = capability_by_id(caps, "filesystem_readonly")
    assert cap is not None
    receipt = {
        "schema_version": 1,
        "receipt_id": "h",
        "created_at_utc": "2026-04-28T12:00:00Z",
        "actor": {"kind": "assistant", "name": "t"},
        "capability": {
            "id": "filesystem_readonly",
            "category": cap["category"],
            "output_lane": cap["output_lane"],
        },
        "authority": {
            "authority_surface": "bridge_packets",
            "authority_class": "ephemeral_only",
            "gate_required_for_record_change": False,
        },
        "declared_intent": "x",
        "inputs": {"operator_supplied_refs": []},
        "access": {
            "network_access": "none",
            "credential_use": "none",
            "resources_read": [],
            "resources_written": [],
        },
        "result": {"status": "success", "summary": "ok", "artifacts": []},
        "governance": {
            "durable_state_write_attempted": False,
            "canonical_record_touched": False,
            "requires_human_review": False,
            "requires_gate_review": False,
            "prohibited_action_attempted": False,
            "prohibited_action_notes": [],
        },
        "integrity": {"repo_git_ref": "abc"},
    }
    h = receipt_sha256_hex(receipt)
    receipt["integrity"]["receipt_hash"] = h
    assert receipt_sha256_hex(receipt) == h

