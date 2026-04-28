"""Tests for scripts/mcp_authority_check.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _run_authority_check(
    *,
    capabilities: Path,
    bindings: Path,
    authority_map: Path | None = None,
    output: Path | None = None,
    strict: bool = False,
) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts" / "mcp_authority_check.py"),
        "--capabilities",
        str(capabilities),
        "--bindings",
        str(bindings),
    ]
    if authority_map is not None:
        cmd.extend(["--authority-map", str(authority_map)])
    if output is not None:
        cmd.extend(["-o", str(output)])
    if strict:
        cmd.append("--strict")
    return subprocess.run(
        cmd,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )


def test_authority_check_smoke_repo_defaults(tmp_path: Path) -> None:
    out = tmp_path / "report.md"
    proc = _run_authority_check(
        capabilities=REPO_ROOT / "config" / "mcp-capabilities.yaml",
        bindings=REPO_ROOT / "config" / "mcp-authority-bindings.yaml",
        authority_map=REPO_ROOT / "config" / "authority-map.json",
        output=out,
        strict=True,
    )
    assert proc.returncode == 0, proc.stderr
    text = out.read_text(encoding="utf-8")
    assert "**PASS**" in text
    assert "## Lane → authority" in text


def test_duplicate_binding_lane_fails(tmp_path: Path) -> None:
    bindings = tmp_path / "dup.yaml"
    bindings.write_text(
        """version: 1
description: fixture
bindings:
  - output_lane: runtime_only
    authority_surface: bridge_packets
    authority_class: ephemeral_only
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: false
    notes: a
  - output_lane: runtime_only
    authority_surface: bridge_packets
    authority_class: ephemeral_only
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: false
    notes: b
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.md"
    proc = _run_authority_check(
        capabilities=REPO_ROOT / "config" / "mcp-capabilities.yaml",
        bindings=bindings,
        output=out,
    )
    assert proc.returncode == 1
    assert "duplicate binding" in out.read_text(encoding="utf-8").lower()


def test_unknown_authority_surface_fails(tmp_path: Path) -> None:
    bindings = tmp_path / "bad-surf.yaml"
    bindings.write_text(
        """version: 1
description: fixture
bindings:
  - output_lane: runtime_only
    authority_surface: not_a_real_surface_key_zzz
    authority_class: ephemeral_only
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: false
    notes: a
  - output_lane: work_artifact
    authority_surface: prepared_context
    authority_class: draftable
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: b
  - output_lane: evidence_stub
    authority_surface: evidence
    authority_class: draftable
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: c
  - output_lane: candidate_proposal
    authority_surface: governed_state
    authority_class: review_required
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: d
  - output_lane: prohibited
    authority_surface: safety
    authority_class: human_only
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: e
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.md"
    proc = _run_authority_check(
        capabilities=REPO_ROOT / "config" / "mcp-capabilities.yaml",
        bindings=bindings,
        output=out,
    )
    assert proc.returncode == 1
    body = out.read_text(encoding="utf-8")
    assert "unknown authority_surface" in body.lower() or "not in authority-map" in body.lower()


def test_class_mismatch_without_override_fails(tmp_path: Path) -> None:
    bindings = tmp_path / "bad-class.yaml"
    bindings.write_text(
        """version: 1
description: fixture
bindings:
  - output_lane: runtime_only
    authority_surface: bridge_packets
    authority_class: draftable
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: false
    notes: wrong class for surface
  - output_lane: work_artifact
    authority_surface: prepared_context
    authority_class: draftable
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: b
  - output_lane: evidence_stub
    authority_surface: evidence
    authority_class: draftable
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: c
  - output_lane: candidate_proposal
    authority_surface: governed_state
    authority_class: review_required
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: d
  - output_lane: prohibited
    authority_surface: safety
    authority_class: human_only
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: e
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.md"
    proc = _run_authority_check(
        capabilities=REPO_ROOT / "config" / "mcp-capabilities.yaml",
        bindings=bindings,
        output=out,
    )
    assert proc.returncode == 1
    assert "authority-map" in out.read_text(encoding="utf-8").lower()


def test_capability_lane_missing_binding_fails(tmp_path: Path) -> None:
    """Bindings omit work_artifact while repo caps include web_research on that lane."""
    bindings = tmp_path / "partial.yaml"
    bindings.write_text(
        """version: 1
description: fixture
bindings:
  - output_lane: runtime_only
    authority_surface: bridge_packets
    authority_class: ephemeral_only
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: false
    notes: a
  - output_lane: evidence_stub
    authority_surface: evidence
    authority_class: draftable
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: b
  - output_lane: candidate_proposal
    authority_surface: governed_state
    authority_class: review_required
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: c
  - output_lane: prohibited
    authority_surface: safety
    authority_class: human_only
    allowed_outputs: [x]
    prohibited_outputs: [y]
    gate_required_for_record_change: true
    notes: d
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.md"
    proc = _run_authority_check(
        capabilities=REPO_ROOT / "config" / "mcp-capabilities.yaml",
        bindings=bindings,
        output=out,
    )
    assert proc.returncode == 1
    assert "no entry in mcp-authority-bindings" in out.read_text(encoding="utf-8").lower()


def test_write_without_receipt_fails(tmp_path: Path) -> None:
    caps = tmp_path / "caps.yaml"
    caps.write_text(
        """version: 1
description: fixture
capabilities:
  - id: bad_writer
    name: Bad
    category: filesystem
    local_or_cloud: local
    trust_tier: low
    allowed_actions: [write_tmp]
    prohibited_actions: []
    reads: []
    writes: [scratch]
    network_access: none
    credential_requirements: none
    durable_state_write: false
    output_lane: work_artifact
    requires_receipt: false
    gate_required_for_record_change: true
    notes: fixture
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.md"
    proc = _run_authority_check(
        capabilities=caps,
        bindings=REPO_ROOT / "config" / "mcp-authority-bindings.yaml",
        output=out,
    )
    assert proc.returncode == 1
    assert "requires_receipt" in out.read_text(encoding="utf-8").lower()


def test_github_readonly_requires_merge_tokens(tmp_path: Path) -> None:
    caps = tmp_path / "caps.yaml"
    caps.write_text(
        """version: 1
description: fixture
capabilities:
  - id: github_readonly
    name: GH
    category: scm
    local_or_cloud: hybrid
    trust_tier: medium
    allowed_actions: [list_repos]
    prohibited_actions: [merge_pr]
    reads: [meta]
    writes: []
    network_access: read
    credential_requirements: optional
    durable_state_write: false
    output_lane: runtime_only
    requires_receipt: true
    gate_required_for_record_change: true
    notes: missing tokens
""",
        encoding="utf-8",
    )
    out = tmp_path / "out.md"
    proc = _run_authority_check(
        capabilities=caps,
        bindings=REPO_ROOT / "config" / "mcp-authority-bindings.yaml",
        output=out,
    )
    assert proc.returncode == 1
    body = out.read_text(encoding="utf-8").lower()
    assert "merge_to_main" in body or "prohibited_actions must include" in body
