"""Tests for scripts/coding_agent_patch_intake.py — intake validation, risk tiers, receipt emission."""

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


def _minimal_doc() -> dict:
    """Single MEDIUM-risk script path by default."""
    doc = {
        "schema_version": 1,
        "agent": {"name": "Fixture Agent", "kind": "assistant"},
        "task": {
            "title": "Fixture intake title",
            "operator_intent": "Exercise intake emission.",
            "claimed_summary": "Adjusted tooling docs.",
        },
        "repo": {"name": "grace-mar", "base_ref": "main"},
        "files_touched": [
            {
                "path": "scripts/mcp_receipt_lib.py",
                "change_type": "modified",
                "surface_hint": "library",
            }
        ],
        "tests": {
            "claimed": ["pytest tests/test_mcp_receipt.py"],
            "reported_results": ["all tests passed"],
        },
        "risks": ["Synthetic intake fixture."],
        "review_request": {"desired_action": "review_only", "requires_human_review": True},
    }
    return doc


def _run_main(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, doc: dict, argv_extra: list[str]) -> tuple[int, Path, Path]:
    import coding_agent_patch_intake as capi

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(capi, "DEFAULT_RECEIPT_DIR", rec_dir)

    inp = tmp_path / "input.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")

    pkt_parent = tmp_path / "artifacts" / "patch-intake"
    pkt_parent.mkdir(parents=True)
    out_pkt = pkt_parent / "packet.md"

    argv = [
        "coding_agent_patch_intake.py",
        "--input",
        str(inp),
        "--output",
        str(out_pkt),
        "--repo-root",
        str(tmp_path),
    ] + argv_extra
    monkeypatch.setattr(sys, "argv", argv)
    code = capi.main()
    return code, out_pkt, rec_dir


def test_valid_packet_and_receipt(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    code, pkt_path, rec_dir = _run_main(tmp_path, monkeypatch, _minimal_doc(), [])
    assert code == 0
    body = pkt_path.read_text(encoding="utf-8")
    assert "CANDIDATE PROPOSAL" in body and "NOT APPROVED RECORD" in body
    assert "mcp_receipt_id:" in body
    receipts = list(rec_dir.glob("*.json"))
    assert len(receipts) == 1
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert receipt["result"]["status"] == "success"
    assert receipt["result"]["summary"].startswith("Generated coding-agent patch intake packet.")
    assert receipt["governance"]["requires_human_review"] is True
    assert receipt["governance"]["requires_gate_review"] is True


def test_output_outside_patch_intake_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import coding_agent_patch_intake as capi

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(capi, "DEFAULT_RECEIPT_DIR", rec_dir)

    inp = tmp_path / "input.json"
    inp.write_text(json.dumps(_minimal_doc()), encoding="utf-8")
    bad = tmp_path / "artifacts" / "other.md"
    bad.parent.mkdir(parents=True)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "x",
            "--input",
            str(inp),
            "--output",
            str(bad),
            "--repo-root",
            str(tmp_path),
        ],
    )
    assert capi.main() == 1


def test_absolute_path_in_files_touched_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_doc()
    doc["files_touched"][0]["path"] = "/etc/passwd"
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_dotdot_path_in_files_touched_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_doc()
    doc["files_touched"][0]["path"] = "scripts/../../../evil.py"
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_merge_phrase_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_doc()
    doc["task"]["claimed_summary"] = "We direct merge this branch tonight."
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_canonical_approval_phrase_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_doc()
    doc["task"]["operator_intent"] = "canonical record approval is assumed."
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_secret_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_doc()
    doc["files_touched"] = [{"path": ".env", "change_type": "modified"}]
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_high_path_classifies_but_succeeds(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_doc()
    doc["files_touched"] = [
        {"path": "config/mcp-capabilities.yaml", "change_type": "modified"}
    ]
    code, pkt_path, rec_dir = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 0
    body = pkt_path.read_text(encoding="utf-8")
    assert "**HIGH**" in body
    receipt = json.loads(list(rec_dir.glob("*.json"))[0].read_text(encoding="utf-8"))
    assert receipt["result"]["status"] == "success"
    assert receipt["governance"]["canonical_record_touched"] is False


def test_critical_record_path_blocked_with_gate_touch(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_doc()
    doc["files_touched"] = [
        {"path": "users/grace-mar/self.md", "change_type": "modified"}
    ]
    code, pkt_path, rec_dir = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 0
    body = pkt_path.read_text(encoding="utf-8")
    assert "BLOCKED" in body and "CRITICAL" in body
    receipt = json.loads(list(rec_dir.glob("*.json"))[0].read_text(encoding="utf-8"))
    assert receipt["result"]["status"] == "blocked"
    assert receipt["governance"]["canonical_record_touched"] is True


def test_tests_claim_without_report_warns_only(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_doc()
    doc["tests"] = {
        "claimed": ["pytest foo"],
        "reported_results": [],
    }
    code, pkt_path, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 0
    assert "### Warning" in pkt_path.read_text(encoding="utf-8")


def test_wrong_capability_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    code, _, _ = _run_main(
        tmp_path,
        monkeypatch,
        _minimal_doc(),
        ["--capability-id", "evidence_stub_operator_template"],
    )
    assert code == 1


def test_classify_helpers() -> None:
    from coding_agent_patch_intake import classify_risk

    assert classify_risk("config/mcp-capabilities.yaml") == "HIGH"
    assert classify_risk("scripts/coding_agent_patch_intake.py") == "MEDIUM"
    assert classify_risk("docs/README.md") == "LOW"
