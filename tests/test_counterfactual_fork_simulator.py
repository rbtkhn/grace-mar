from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SIMULATOR = REPO_ROOT / "scripts" / "simulate_counterfactual_fork.py"
SCHEMA_PATH = REPO_ROOT / "schema-registry" / "counterfactual-simulation-report.v1.json"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _build_repo(root: Path) -> None:
    user_dir = root / "users" / "grace-mar"
    user_dir.mkdir(parents=True, exist_ok=True)
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "example.md").write_text("# Example\n", encoding="utf-8")
    (user_dir / "self.md").write_text("# self\n", encoding="utf-8")
    (user_dir / "self-library.md").write_text("# self-library\n", encoding="utf-8")
    (user_dir / "recursion-gate.md").write_text("# recursion-gate\n", encoding="utf-8")


def _proposal(
    proposal_id: str = "example-proposal",
    *,
    proposal_kind: str = "doctrine_change",
    target_paths: list[str] | None = None,
    target_surfaces: list[str] | None = None,
    summary: str = "Add a narrow documentation clarification.",
    patch_text: str = "",
) -> dict:
    return {
        "proposal_id": proposal_id,
        "proposal_kind": proposal_kind,
        "target_paths": target_paths if target_paths is not None else ["docs/example.md"],
        "target_surfaces": target_surfaces if target_surfaces is not None else ["SELF-LIBRARY"],
        "proposed_change_summary": summary,
        "proposed_patch_text": patch_text,
        "evidence_refs": [],
        "operator_question": "What would this affect if accepted?",
    }


def _run(repo_root: Path, proposal_path: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SIMULATOR),
            "--repo-root",
            str(repo_root),
            "--proposal",
            str(proposal_path),
            *extra,
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def test_clean_narrow_docs_proposal_produces_non_authoritative_report(tmp_path: Path) -> None:
    _build_repo(tmp_path)
    proposal_path = tmp_path / "proposal.json"
    _write_json(proposal_path, _proposal())

    result = _run(tmp_path, proposal_path)
    assert result.returncode == 0, result.stderr

    out = tmp_path / "artifacts" / "counterfactual-simulations" / "example-proposal-simulation.json"
    assert out.is_file()
    report = json.loads(out.read_text(encoding="utf-8"))
    assert report["authority"]["recordAuthority"] == "none"
    assert report["authority"]["gateEffect"] == "none"
    assert report["authority"]["mergeAuthority"] == "none"
    assert report["authority"]["simulationOnly"] is True
    assert report["recommendation"]["decision"] == "accept"


def test_merge_authority_language_produces_reject_risk(tmp_path: Path) -> None:
    _build_repo(tmp_path)
    proposal_path = tmp_path / "proposal.json"
    _write_json(
        proposal_path,
        _proposal(
            summary="Grant extra authority to the runtime.",
            patch_text="mergeAuthority: write",
        ),
    )

    result = _run(tmp_path, proposal_path)
    assert result.returncode == 0, result.stderr
    out = tmp_path / "artifacts" / "counterfactual-simulations" / "example-proposal-simulation.json"
    report = json.loads(out.read_text(encoding="utf-8"))
    assert report["recommendation"]["decision"] == "reject"
    assert any("mergeAuthority" in item for item in report["doctrine_drift_risks"])


def test_interface_artifact_non_none_record_authority_creates_drift_risk(tmp_path: Path) -> None:
    _build_repo(tmp_path)
    proposal_path = tmp_path / "proposal.json"
    _write_json(
        proposal_path,
        _proposal(
            proposal_kind="interface_artifact",
            summary="Add a new interface artifact.",
            patch_text="recordAuthority: full",
        ),
    )

    result = _run(tmp_path, proposal_path)
    assert result.returncode == 0, result.stderr
    out = tmp_path / "artifacts" / "counterfactual-simulations" / "example-proposal-simulation.json"
    report = json.loads(out.read_text(encoding="utf-8"))
    assert report["doctrine_drift_risks"]
    assert any("recordAuthority" in item or "Interface artifact" in item for item in report["doctrine_drift_risks"])


def test_empty_target_surfaces_produces_needs_review(tmp_path: Path) -> None:
    _build_repo(tmp_path)
    proposal_path = tmp_path / "proposal.json"
    _write_json(proposal_path, _proposal(target_surfaces=[]))

    result = _run(tmp_path, proposal_path)
    assert result.returncode == 0, result.stderr
    out = tmp_path / "artifacts" / "counterfactual-simulations" / "example-proposal-simulation.json"
    report = json.loads(out.read_text(encoding="utf-8"))
    assert report["recommendation"]["decision"] == "needs_review"


def test_refuses_output_outside_counterfactual_artifacts_dir(tmp_path: Path) -> None:
    _build_repo(tmp_path)
    proposal_path = tmp_path / "proposal.json"
    _write_json(proposal_path, _proposal())
    forbidden = tmp_path / "outside.json"

    result = _run(tmp_path, proposal_path, "--output", str(forbidden))
    assert result.returncode == 1
    assert "artifacts/counterfactual-simulations" in result.stderr
    assert not forbidden.exists()


def test_report_validates_against_schema_when_jsonschema_available(tmp_path: Path) -> None:
    jsonschema = pytest.importorskip("jsonschema")
    _build_repo(tmp_path)
    proposal_path = tmp_path / "proposal.json"
    _write_json(proposal_path, _proposal())

    result = _run(tmp_path, proposal_path)
    assert result.returncode == 0, result.stderr
    out = tmp_path / "artifacts" / "counterfactual-simulations" / "example-proposal-simulation.json"
    report = json.loads(out.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(instance=report, schema=schema)


def test_script_does_not_modify_gate_or_canonical_record_files(tmp_path: Path) -> None:
    _build_repo(tmp_path)
    proposal_path = tmp_path / "proposal.json"
    _write_json(proposal_path, _proposal())

    user_dir = tmp_path / "users" / "grace-mar"
    self_path = user_dir / "self.md"
    library_path = user_dir / "self-library.md"
    gate_path = user_dir / "recursion-gate.md"
    before_self = self_path.read_bytes()
    before_library = library_path.read_bytes()
    before_gate = gate_path.read_bytes()

    result = _run(tmp_path, proposal_path)
    assert result.returncode == 0, result.stderr
    assert self_path.read_bytes() == before_self
    assert library_path.read_bytes() == before_library
    assert gate_path.read_bytes() == before_gate
