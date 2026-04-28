"""Tests for scripts/mcp_mock_harness.py — fixtures, enforcement, receipts."""

from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

pytest.importorskip("jsonschema")


@pytest.fixture(autouse=True)
def _scripts_on_path() -> None:
    p = str(REPO_ROOT / "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)


def _base_github_good() -> dict:
    return json.loads(
        (REPO_ROOT / "examples" / "mcp-mock-run.github-readonly.example.json").read_text(encoding="utf-8")
    )


def _run_harness(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    doc: dict,
    *,
    out_name: str = "out.md",
) -> tuple[int, Path, Path]:
    import mcp_mock_harness as mmh

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(mmh, "DEFAULT_RECEIPT_DIR", rec_dir)

    inp = tmp_path / "run.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")
    outp = tmp_path / "artifacts" / "mcp-mock-runs" / out_name

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "mcp_mock_harness.py",
            "--input",
            str(inp),
            "--output",
            str(outp),
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
    code = mmh.main()
    return code, outp, rec_dir


def test_github_readonly_mock_run_packet_and_receipt(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    code, outp, rec_dir = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 0
    body = outp.read_text(encoding="utf-8")
    assert "MOCK MCP RUN · WORK ARTIFACT · NO LIVE SERVER · NOT APPROVED INTEGRATION" in body
    assert "NO LIVE SERVER" in body and "NOT APPROVED INTEGRATION" in body
    assert "receipt_id:" in body
    assert "github_readonly" in body

    receipts = list(rec_dir.glob("*.json"))
    assert len(receipts) == 1
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert receipt["capability"]["id"] == "mcp_mock_harness"
    assert receipt["result"]["status"] == "success"


def test_output_outside_mock_runs_bucket_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import mcp_mock_harness as mmh

    doc = _base_github_good()
    inp = tmp_path / "run.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")
    bad_out = tmp_path / "not-in-bucket.md"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "mcp_mock_harness.py",
            "--input",
            str(inp),
            "--output",
            str(bad_out),
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
    assert mmh.main() == 1


def test_http_resource_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["mock_request"]["resources_read"] = ["http://example.com/x"]
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_https_resource_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["mock_request"]["resources_read"] = ["https://example.com/x"]
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_absolute_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["mock_request"]["resources_read"] = ["/etc/passwd"]
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_dotdot_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["mock_request"]["resources_read"] = ["../escape"]
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_users_grace_mar_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["mock_request"]["resources_read"] = ["users/grace-mar/self.md"]
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_readonly_capability_resources_written_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["mock_request"]["resources_written"] = ["mock://github/outbox/write"]
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_network_access_exceeds_registry_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["mock_request"]["network_access"] = "full"
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_credential_use_exceeds_registry_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["mock_request"]["credential_use"] = "required"
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_prohibited_capability_success_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["run"]["capability_id"] = "shell_execution_prohibited"
    doc["run"]["tool_name"] = "describe_policy"
    doc["mock_response"]["status"] = "success"
    doc["mock_request"]["network_access"] = "none"
    doc["mock_request"]["credential_use"] = "none"
    doc["mock_request"]["resources_read"] = ["mock://policy/stance"]
    doc["mock_request"]["resources_written"] = []
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_shell_tool_success_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["run"]["tool_name"] = "shell_execute"
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_blocked_shell_mock_run_succeeds(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = json.loads(
        (REPO_ROOT / "examples" / "mcp-mock-run.shell-blocked.example.json").read_text(encoding="utf-8")
    )
    code, outp, rec_dir = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 0
    assert "shell_execution_prohibited" in outp.read_text(encoding="utf-8")
    receipt = json.loads(list(rec_dir.glob("*.json"))[0].read_text(encoding="utf-8"))
    assert receipt["result"]["status"] == "blocked"


def test_durable_state_true_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["governance_expectations"]["durable_state_write_attempted"] = True
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_canonical_record_touched_true_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_github_good()
    doc["governance_expectations"]["canonical_record_touched"] = True
    code, _, _ = _run_harness(monkeypatch, tmp_path, doc)
    assert code == 1


def test_validate_resource_token_mock_uri_ok() -> None:
    import mcp_mock_harness as mmh

    mmh.validate_resource_token("mock://github/a/b", ctx="test")


def test_enforce_mock_vs_registry_unit() -> None:
    import mcp_mock_harness as mmh

    from mcp_receipt_lib import capability_by_id, load_yaml

    caps_doc = load_yaml(REPO_ROOT / "config" / "mcp-capabilities.yaml")
    sim = capability_by_id(caps_doc, "github_readonly")
    assert sim is not None
    doc = _base_github_good()
    assert mmh.enforce_mock_vs_registry(doc, sim) == []

    bad = deepcopy(doc)
    bad["mock_response"]["status"] = "success"
    bad["run"]["capability_id"] = "shell_execution_prohibited"
    bad["run"]["tool_name"] = "x"
    bad["mock_request"]["network_access"] = "none"
    bad["mock_request"]["credential_use"] = "none"
    bad["mock_request"]["resources_read"] = ["mock://x"]
    bad["mock_request"]["resources_written"] = []
    sim2 = capability_by_id(caps_doc, "shell_execution_prohibited")
    assert sim2 is not None
    errs = mmh.enforce_mock_vs_registry(bad, sim2)
    assert any("prohibited" in e.lower() or "success" in e.lower() for e in errs)
