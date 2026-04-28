"""Tests for scripts/mcp_manifest_admission.py — classification, gates, receipts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

pytest.importorskip("jsonschema")
pytest.importorskip("yaml")


@pytest.fixture(autouse=True)
def _scripts_on_path() -> None:
    p = str(REPO_ROOT / "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)


def _minimal_manifest() -> dict:
    return {
        "schema_version": 1,
        "server": {
            "id": "fixture-server",
            "name": "Fixture",
            "description": "Synthetic fixture manifest.",
            "local_or_cloud": "local",
        },
        "declared_capabilities": {"tools": [], "resources": [], "prompts": []},
        "permissions": {
            "network_access": "none",
            "credential_requirements": "none",
            "reads": [],
            "writes": [],
            "allowed_actions": [],
            "prohibited_actions": [],
        },
        "operator": {"intended_use": "Unit-test harness manifest admission gates."},
    }


def test_infer_github_readonly_mapping() -> None:
    import mcp_manifest_admission as mma

    manifest = _minimal_manifest()
    manifest["server"]["description"] = (
        "Read GitHub repository metadata — proposal-only manifest entry."
    )
    manifest["permissions"]["network_access"] = "read"
    manifest["permissions"]["credential_requirements"] = "required"
    manifest["permissions"]["reads"] = ["github_repository_metadata"]
    manifest["permissions"]["writes"] = []
    manifest["permissions"]["allowed_actions"] = ["read_repo", "inspect_diff", "list_releases_read_only"]
    manifest["permissions"]["prohibited_actions"] = [
        "merge_to_main",
        "force_push",
        "bypass_review",
        "write_file",
        "push_commit",
        "delete_branch",
    ]

    mid, reason = mma.infer_matched_capability_id(manifest)
    assert mid == "github_readonly"
    assert "scm" in reason.lower() or "github" in reason.lower()


def test_infer_shell_maps_shell_execution_prohibited() -> None:
    import mcp_manifest_admission as mma

    manifest = _minimal_manifest()
    manifest["permissions"]["allowed_actions"] = ["shell_execute", "noop"]

    mid, _ = mma.infer_matched_capability_id(manifest)
    assert mid == "shell_execution_prohibited"


def test_infer_memory_maps_memory_external() -> None:
    import mcp_manifest_admission as mma

    manifest = _minimal_manifest()
    manifest["permissions"]["allowed_actions"] = ["upsert_embedding_store"]

    mid, _ = mma.infer_matched_capability_id(manifest)
    assert mid == "memory_external_prohibited_by_default"


def test_merge_tokens_in_allowed_blocked_locally() -> None:
    import mcp_manifest_admission as mma

    manifest = _minimal_manifest()
    manifest["permissions"]["allowed_actions"] = ["merge_to_main"]

    reasons = mma.admission_local_blockers(manifest)
    assert any("merge_to_main" in r for r in reasons)


def test_users_grace_mar_path_blocked_locally() -> None:
    import mcp_manifest_admission as mma

    manifest = _minimal_manifest()
    manifest["permissions"]["reads"] = ["users/grace-mar/self.md"]

    reasons = mma.admission_local_blockers(manifest)
    assert any("users_grace_mar" in r for r in reasons)


def test_database_mutating_verbs_blocked_locally() -> None:
    import mcp_manifest_admission as mma

    manifest = _minimal_manifest()
    manifest["permissions"]["writes"] = ["insert_row_into_audit"]

    reasons = mma.admission_local_blockers(manifest)
    assert any("database_mutating" in r for r in reasons)


def test_validate_manifest_paths_rejects_dotdot() -> None:
    import mcp_manifest_admission as mma

    doc = {
        "schema_version": 1,
        "server": {
            "id": "x",
            "name": "x",
            "description": "d",
            "local_or_cloud": "local",
        },
        "declared_capabilities": {"tools": [], "resources": [], "prompts": []},
        "permissions": {
            "network_access": "none",
            "credential_requirements": "none",
            "reads": ["../evil"],
            "writes": [],
            "allowed_actions": [],
            "prohibited_actions": [],
        },
        "operator": {"intended_use": "bad paths"},
    }

    with pytest.raises(ValueError, match=r"\.\."):
        mma.validate_manifest_paths(doc)


def test_infer_needs_manual_classification() -> None:
    import mcp_manifest_admission as mma

    manifest = _minimal_manifest()
    manifest["server"]["description"] = "Generic local helper with no SCM/GitHub fingerprints."

    mid, _ = mma.infer_matched_capability_id(manifest)
    assert mid == mma.NEEDS_MANUAL


def test_requested_output_lane_widening_blocked(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import yaml

    import mcp_manifest_admission as mma

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(mma, "DEFAULT_RECEIPT_DIR", rec_dir)

    inp = tmp_path / "in.yaml"
    doc = yaml.safe_load(
        (REPO_ROOT / "examples" / "mcp-server-manifest.example.yaml").read_text(encoding="utf-8")
    )
    doc["operator"]["intended_use"] = "Lane widen probe.\n"
    doc["operator"]["requested_output_lane"] = "candidate_proposal"
    inp.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")

    out = tmp_path / "artifacts" / "mcp-admission" / "lane-block.md"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "mcp_manifest_admission.py",
            "--input",
            str(inp),
            "--output",
            str(out),
            "--repo-root",
            str(tmp_path),
            "--capabilities",
            str(REPO_ROOT / "config" / "mcp-capabilities.yaml"),
            "--bindings",
            str(REPO_ROOT / "config" / "mcp-authority-bindings.yaml"),
            "--policy",
            str(REPO_ROOT / "config" / "mcp-risk-policy.yaml"),
        ],
    )
    code = mma.main()
    assert code == 0

    receipt_paths = list(rec_dir.glob("*.json"))
    assert len(receipt_paths) == 1
    receipt = json.loads(receipt_paths[0].read_text(encoding="utf-8"))
    assert receipt["result"]["status"] == "blocked"
    body = out.read_text(encoding="utf-8")
    assert "requested_output_lane_exceeds_matched_capability_lane" in body


def test_github_readonly_example_packet_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import mcp_manifest_admission as mma

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(mma, "DEFAULT_RECEIPT_DIR", rec_dir)

    inp = tmp_path / "ex.yaml"
    inp.write_text(
        (REPO_ROOT / "examples" / "mcp-server-manifest.example.yaml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    out = tmp_path / "artifacts" / "mcp-admission" / "from-example.md"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "mcp_manifest_admission.py",
            "--input",
            str(inp),
            "--output",
            str(out),
            "--repo-root",
            str(tmp_path),
            "--capabilities",
            str(REPO_ROOT / "config" / "mcp-capabilities.yaml"),
            "--bindings",
            str(REPO_ROOT / "config" / "mcp-authority-bindings.yaml"),
            "--policy",
            str(REPO_ROOT / "config" / "mcp-risk-policy.yaml"),
        ],
    )

    assert mma.main() == 0
    body = out.read_text(encoding="utf-8")
    assert "MCP ADMISSION REVIEW · WORK ARTIFACT · NOT ENABLED · NOT APPROVED INTEGRATION" in body
    assert "github_readonly" in body

    receipts = list(rec_dir.glob("*.json"))
    assert len(receipts) == 1
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert receipt["result"]["status"] == "success"


def test_example_yaml_optional_cli_smoke() -> None:
    """Runs admission against repo example manifest into repo artifacts bucket."""
    import subprocess

    out_md = REPO_ROOT / "artifacts" / "mcp-admission" / "_pytest_smoke.md"
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "mcp_manifest_admission.py"),
            "--input",
            str(REPO_ROOT / "examples" / "mcp-server-manifest.example.yaml"),
            "--output",
            str(out_md),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert proc.returncode == 0, proc.stderr
    assert out_md.is_file()
    body = out_md.read_text(encoding="utf-8")
    assert "MCP ADMISSION REVIEW" in body
    out_md.unlink(missing_ok=True)
