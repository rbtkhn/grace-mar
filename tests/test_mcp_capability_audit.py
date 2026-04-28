"""Tests for scripts/mcp_capability_audit.py."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _scripts_on_path() -> None:
    p = str(REPO_ROOT / "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)


def test_danger_flags_r3_durable_without_gate() -> None:
    from mcp_capability_audit import danger_flags

    bad = {
        "id": "bad_durable",
        "name": "Bad",
        "category": "memory",
        "local_or_cloud": "local",
        "trust_tier": "low",
        "allowed_actions": [],
        "prohibited_actions": ["x"],
        "reads": [],
        "writes": [],
        "network_access": "none",
        "credential_requirements": "none",
        "durable_state_write": True,
        "output_lane": "runtime_only",
        "requires_receipt": True,
        "gate_required_for_record_change": False,
        "notes": "",
    }
    msgs = danger_flags([bad])
    assert any("R3[bad_durable]" in m for m in msgs)


def test_danger_flags_r4_write_without_receipt() -> None:
    from mcp_capability_audit import danger_flags

    bad = {
        "id": "bad_write",
        "name": "Bad",
        "category": "filesystem",
        "local_or_cloud": "local",
        "trust_tier": "low",
        "allowed_actions": ["write_tmp"],
        "prohibited_actions": [],
        "reads": [],
        "writes": ["scratch"],
        "network_access": "none",
        "credential_requirements": "none",
        "durable_state_write": False,
        "output_lane": "work_artifact",
        "requires_receipt": False,
        "gate_required_for_record_change": True,
        "notes": "",
    }
    msgs = danger_flags([bad])
    assert any("R4[bad_write]" in m for m in msgs)


def test_shell_execution_prohibited_no_r2() -> None:
    from mcp_capability_audit import danger_flags

    seed_row = {
        "id": "shell_execution_prohibited",
        "name": "Shell prohibited",
        "category": "policy",
        "local_or_cloud": "local",
        "trust_tier": "operator_only",
        "allowed_actions": [],
        "prohibited_actions": ["shell_execute"],
        "reads": [],
        "writes": [],
        "network_access": "none",
        "credential_requirements": "none",
        "durable_state_write": False,
        "output_lane": "runtime_only",
        "requires_receipt": True,
        "gate_required_for_record_change": True,
        "notes": "",
    }
    assert not any("R2[shell_execution_prohibited]" in m for m in danger_flags([seed_row]))


def test_schema_validation_rejects_extra_keys(tmp_path: Path) -> None:
    from mcp_capability_audit import validate_document

    schema_path = REPO_ROOT / "schemas" / "mcp-capability.v1.json"
    bad_doc = {
        "version": 1,
        "capabilities": [
            {
                "id": "x",
                "name": "X",
                "category": "filesystem",
                "local_or_cloud": "local",
                "trust_tier": "low",
                "allowed_actions": [],
                "prohibited_actions": ["p"],
                "reads": [],
                "writes": [],
                "network_access": "none",
                "credential_requirements": "none",
                "durable_state_write": False,
                "output_lane": "runtime_only",
                "requires_receipt": True,
                "gate_required_for_record_change": True,
                "notes": "",
                "unexpected_field": 1,
            }
        ],
    }
    with pytest.raises(Exception):
        validate_document(bad_doc, schema_path)


def test_audit_script_smoke_tmp_output(tmp_path: Path) -> None:
    out = tmp_path / "report.md"
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "mcp_capability_audit.py"),
            "-o",
            str(out),
            "--config",
            str(REPO_ROOT / "config" / "mcp-capabilities.yaml"),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    text = out.read_text(encoding="utf-8")
    assert "## Danger flags" in text


def test_strict_exits_nonzero_when_flags(tmp_path: Path) -> None:
    """Synthetic doc triggers R3; strict mode should exit 1."""
    cfg = tmp_path / "bad.yaml"
    cfg.write_text(
        """version: 1
description: fixture
capabilities:
  - id: leaky
    name: Leaky
    category: memory
    local_or_cloud: local
    trust_tier: low
    allowed_actions: []
    prohibited_actions: [x]
    reads: []
    writes: []
    network_access: none
    credential_requirements: none
    durable_state_write: true
    output_lane: runtime_only
    requires_receipt: true
    gate_required_for_record_change: false
    notes: fixture
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.md"
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "mcp_capability_audit.py"),
            "--config",
            str(cfg),
            "-o",
            str(out),
            "--strict",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 1
    assert "R3" in out.read_text(encoding="utf-8")
