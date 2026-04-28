"""Tests for scripts/research_to_evidence_stub.py — validation, paths, stub + receipt emission."""

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


def _minimal_valid_doc() -> dict:
    return {
        "schema_version": 1,
        "topic": "PR4 adapter test topic",
        "research_kind": "policy_capture",
        "operator_intent": "Exercise stub emission with isolated paths.",
        "sources": [
            {
                "source_id": "s1",
                "title": "Local README",
                "source_type": "repo_doc",
                "reliability": "primary",
                "local_path": "README.md",
                "claims": ["Repo exists."],
                "short_excerpts": ["Grace-Mar companion-self cognitive fork."],
            }
        ],
        "candidate_claims": [
            {
                "claim": "Stub pipeline stays pre-canonical.",
                "supporting_sources": ["s1"],
                "confidence": "medium",
                "record_action": "keep_as_work",
            }
        ],
        "risks_or_uncertainties": ["Tests use synthetic paths."],
        "suggested_gate_action": "keep_as_work",
    }


def _run_main(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, doc: dict, argv_tail: list[str]) -> tuple[int, Path, Path]:
    """Run main with receipt dir under tmp_path; returns exit code, stub path, receipt path."""
    import research_to_evidence_stub as rtes

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(rtes, "DEFAULT_RECEIPT_DIR", rec_dir)

    inp = tmp_path / "input.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")

    stub_parent = tmp_path / "artifacts" / "evidence-stubs"
    stub_parent.mkdir(parents=True)
    out_stub = stub_parent / "test-out.md"

    argv = [
        "research_to_evidence_stub.py",
        "--input",
        str(inp),
        "--output",
        str(out_stub),
        "--repo-root",
        str(tmp_path),
    ] + argv_tail
    monkeypatch.setattr(sys, "argv", argv)
    code = rtes.main()
    return code, out_stub, rec_dir


def test_valid_input_writes_stub_and_receipt(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    code, stub_path, rec_dir = _run_main(tmp_path, monkeypatch, _minimal_valid_doc(), [])
    assert code == 0
    assert stub_path.is_file()
    body = stub_path.read_text(encoding="utf-8")
    assert "PRE-CANONICAL" in body and "NOT APPROVED RECORD" in body
    assert "mcp_receipt_id:" in body
    # One receipt JSON
    receipts = list(rec_dir.glob("*.json"))
    assert len(receipts) == 1
    receipt = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert receipt["result"]["status"] == "success"
    assert receipt["result"]["summary"] == "Generated pre-canonical evidence stub."
    # Front matter id matches file
    stub_rid = None
    for line in body.splitlines():
        if line.startswith("mcp_receipt_id:"):
            stub_rid = line.split(":", 1)[1].strip().strip('"')
            break
    assert stub_rid == receipts[0].stem


def test_output_outside_evidence_stubs_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import research_to_evidence_stub as rtes

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(rtes, "DEFAULT_RECEIPT_DIR", rec_dir)

    bad_out = tmp_path / "artifacts" / "elsewhere.md"
    bad_out.parent.mkdir(parents=True)
    inp = tmp_path / "input.json"
    inp.write_text(json.dumps(_minimal_valid_doc()), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "x",
            "--input",
            str(inp),
            "--output",
            str(bad_out),
            "--repo-root",
            str(tmp_path),
        ],
    )
    assert rtes.main() == 1


def test_missing_source_title_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_valid_doc()
    doc["sources"][0]["title"] = ""
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_source_without_url_or_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_valid_doc()
    del doc["sources"][0]["local_path"]
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_claim_unknown_supporting_source_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_valid_doc()
    doc["candidate_claims"][0]["supporting_sources"] = ["no-such-id"]
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_bad_confidence_enum_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_valid_doc()
    doc["candidate_claims"][0]["confidence"] = "maybe"
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_excerpt_over_300_chars_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_valid_doc()
    doc["sources"][0]["short_excerpts"] = ["x" * 301]
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_output_path_touching_self_md_segment_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import research_to_evidence_stub as rtes

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(rtes, "DEFAULT_RECEIPT_DIR", rec_dir)

    stub_bad = tmp_path / "artifacts" / "evidence-stubs" / "self.md"
    stub_bad.parent.mkdir(parents=True)
    inp = tmp_path / "input.json"
    inp.write_text(json.dumps(_minimal_valid_doc()), encoding="utf-8")

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "x",
            "--input",
            str(inp),
            "--output",
            str(stub_bad),
            "--repo-root",
            str(tmp_path),
        ],
    )
    assert rtes.main() == 1


def test_denylist_rejects_canonical_approval_phrase(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _minimal_valid_doc()
    doc["topic"] = "Discussion of canonical record approval in theory only."
    code, _, _ = _run_main(tmp_path, monkeypatch, doc, [])
    assert code == 1


def test_wrong_capability_lane_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    code, _, _ = _run_main(
        tmp_path,
        monkeypatch,
        _minimal_valid_doc(),
        ["--capability-id", "github_readonly"],
    )
    assert code == 1


def test_validate_extra_rules_direct() -> None:
    from research_to_evidence_stub import validate_extra_rules

    doc = _minimal_valid_doc()
    validate_extra_rules(doc)
    doc["candidate_claims"][0]["supporting_sources"] = ["ghost"]
    with pytest.raises(ValueError, match="unknown source_id"):
        validate_extra_rules(doc)


def test_subprocess_smoke_matches_example() -> None:
    """Integration-style: real repo root and paths (example JSON + repo configs)."""
    example = REPO_ROOT / "examples" / "research-evidence-input.example.json"
    assert example.is_file()
    out = REPO_ROOT / "artifacts" / "evidence-stubs" / "_pytest-research-stub-smoke.md"
    import subprocess

    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "research_to_evidence_stub.py"),
            "--input",
            str(example),
            "--output",
            str(out),
            "--repo-root",
            str(REPO_ROOT),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr
    assert out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "PRE-CANONICAL" in text
    lines = [ln.strip() for ln in r.stdout.strip().splitlines() if ln.strip()]
    assert len(lines) >= 2
    receipt_path = REPO_ROOT.joinpath(*lines[1].split("/"))
    assert receipt_path.is_file()
    receipt_path.unlink(missing_ok=True)
    out.unlink(missing_ok=True)
