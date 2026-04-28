"""Tests for scripts/mcp_risk_scan.py — scoring, hard blockers, PROHIBITED_BY_POLICY nuance."""

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


@pytest.fixture(scope="module")
def policy_doc() -> dict:
    from mcp_risk_scan import DEFAULT_POLICY, DEFAULT_POLICY_SCHEMA, load_yaml, validate_json_schema

    doc = load_yaml(DEFAULT_POLICY.resolve())
    validate_json_schema(doc, DEFAULT_POLICY_SCHEMA.resolve())
    return doc


def _base_capability(cid: str = "test_cap") -> dict:
    """Minimal valid capability-shaped dict for scanner evaluation."""
    return {
        "id": cid,
        "name": "Test",
        "category": "filesystem",
        "local_or_cloud": "local",
        "trust_tier": "medium",
        "allowed_actions": ["read_file"],
        "prohibited_actions": ["write_file"],
        "reads": ["repo"],
        "writes": [],
        "network_access": "none",
        "credential_requirements": "none",
        "durable_state_write": False,
        "output_lane": "runtime_only",
        "requires_receipt": True,
        "gate_required_for_record_change": True,
        "notes": "fixture",
    }


def test_readonly_like_low(policy_doc: dict) -> None:
    from mcp_risk_scan import evaluate_capability

    f = evaluate_capability(_base_capability("fs_ro"), policy_doc)
    assert f["risk_level"] == "low"
    assert f["hard_blockers"] == []
    assert not f["prohibited_by_policy"]


def test_github_patch_style_high_no_blockers(policy_doc: dict) -> None:
    from mcp_risk_scan import evaluate_capability, scan_passes

    cap = _base_capability("gh_patch")
    cap["category"] = "scm"
    cap["local_or_cloud"] = "hybrid"
    cap["credential_requirements"] = "required"
    cap["network_access"] = "full"
    cap["writes"] = ["draft_branch_only"]
    cap["allowed_actions"] = ["open_draft_pr", "comment_patch"]
    cap["prohibited_actions"] = [
        "merge_to_main",
        "force_push",
        "bypass_review",
        "merge_pr",
        "push_commit",
        "delete_branch",
    ]
    cap["output_lane"] = "candidate_proposal"
    f = evaluate_capability(cap, policy_doc)
    assert f["risk_level"] == "high"
    assert f["hard_blockers"] == []
    assert scan_passes([f])


def test_shell_in_allowed_hard_fails(policy_doc: dict) -> None:
    from mcp_risk_scan import evaluate_capability, scan_passes

    cap = _base_capability("evil_shell")
    cap["allowed_actions"] = ["shell_execute", "read_file"]
    f = evaluate_capability(cap, policy_doc)
    assert "shell_execute" in f["hard_blockers"]
    assert not scan_passes([f])


def test_write_without_receipt_blocks(policy_doc: dict) -> None:
    from mcp_risk_scan import evaluate_capability, scan_passes

    cap = _base_capability("no_rcpt")
    cap["writes"] = ["artifacts/foo"]
    cap["requires_receipt"] = False
    f = evaluate_capability(cap, policy_doc)
    assert "write_without_receipt" in f["hard_blockers"]
    assert not scan_passes([f])


def test_durable_without_gate_blocks(policy_doc: dict) -> None:
    from mcp_risk_scan import evaluate_capability, scan_passes

    cap = _base_capability("bad_gate")
    cap["durable_state_write"] = True
    cap["gate_required_for_record_change"] = False
    f = evaluate_capability(cap, policy_doc)
    assert "durable_state_write_without_gate" in f["hard_blockers"]
    assert not scan_passes([f])


def test_canonical_record_writes_block(policy_doc: dict) -> None:
    from mcp_risk_scan import evaluate_capability, scan_passes

    cap = _base_capability("canon")
    cap["writes"] = ["users/grace-mar/self.md"]
    f = evaluate_capability(cap, policy_doc)
    assert "write_users_grace_mar_self_md" in f["hard_blockers"]
    assert not scan_passes([f])


def test_prohibited_shell_stance_no_permissive_blockers(policy_doc: dict) -> None:
    from mcp_risk_scan import evaluate_capability, scan_passes

    cap = _base_capability("shell_execution_prohibited_fixture")
    cap["category"] = "policy"
    cap["output_lane"] = "prohibited"
    cap["allowed_actions"] = []
    cap["prohibited_actions"] = ["shell_execute", "subprocess_spawn", "interactive_terminal"]
    cap["trust_tier"] = "operator_only"
    f = evaluate_capability(cap, policy_doc)
    assert f["prohibited_by_policy"] is True
    assert f["hard_blockers"] == []
    assert scan_passes([f])


def test_external_memory_write_without_review_blocks(policy_doc: dict) -> None:
    from mcp_risk_scan import evaluate_capability, scan_passes

    cap = _base_capability("mem_bad")
    cap["category"] = "memory"
    cap["local_or_cloud"] = "cloud"
    cap["allowed_actions"] = ["upsert_embedding_store"]
    cap["writes"] = ["vector_store"]
    cap["prohibited_actions"] = []
    f = evaluate_capability(cap, policy_doc)
    assert "external_memory_write_without_review" in f["hard_blockers"]
    assert not scan_passes([f])


def test_scm_missing_github_prohibition_warning(policy_doc: dict) -> None:
    from mcp_risk_scan import evaluate_capability

    cap = _base_capability("scm_sloppy")
    cap["category"] = "scm"
    cap["network_access"] = "full"
    cap["writes"] = ["draft"]
    cap["prohibited_actions"] = ["merge_to_main"]
    f = evaluate_capability(cap, policy_doc)
    assert any("missing recommended tokens" in w for w in f["warnings"])
    assert f["score"] >= 8


def test_build_json_report_shape(policy_doc: dict) -> None:
    from mcp_risk_scan import build_json_report, evaluate_capability

    f = evaluate_capability(_base_capability(), policy_doc)
    js = build_json_report(
        findings=[f],
        passes=True,
        caps_path=REPO_ROOT / "config" / "mcp-capabilities.yaml",
        policy_path=REPO_ROOT / "config" / "mcp-risk-policy.yaml",
        generated_at_utc="2026-04-28T12:00:00Z",
        git_ref="abc1234",
    )
    assert js["pass"] is True
    assert js["capabilities_checked"] == 1
    assert "findings" in js and len(js["findings"]) == 1
    assert "blockers" in js and "warnings" in js


def test_live_registry_scan_passes() -> None:
    """Committed registry should clear blocker rules (definition of done)."""
    import subprocess

    r = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "mcp_risk_scan.py"), "--json"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    jp = REPO_ROOT / "artifacts" / "mcp-risk-report.json"
    assert jp.is_file()
    data = json.loads(jp.read_text(encoding="utf-8"))
    assert data["pass"] is True
