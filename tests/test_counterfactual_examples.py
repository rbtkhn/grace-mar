from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SIMULATOR = REPO_ROOT / "scripts" / "simulate_counterfactual_fork.py"
EXAMPLES = REPO_ROOT / "examples" / "diagnostics"

EXAMPLE_PATHS = [
    EXAMPLES / "counterfactual-clean-docs.example.json",
    EXAMPLES / "counterfactual-dangerous-merge-authority.example.json",
    EXAMPLES / "counterfactual-portable-emulation.example.json",
    EXAMPLES / "counterfactual-proposal.example.json",
]

REQUIRED_KEYS = [
    "proposal_id",
    "proposal_kind",
    "target_paths",
    "target_surfaces",
    "proposed_change_summary",
    "proposed_patch_text",
    "evidence_refs",
    "operator_question",
]


def _load_example(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_on_repo(proposal: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SIMULATOR),
            "--repo-root",
            str(REPO_ROOT),
            "--proposal",
            str(proposal),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def _report_from_run(proc: subprocess.CompletedProcess[str]) -> dict:
    assert proc.returncode == 0, proc.stderr
    out_line = proc.stdout.strip().splitlines()[-1] if proc.stdout.strip() else ""
    out_path = Path(out_line)
    if not out_path.is_file():
        out_path = REPO_ROOT / out_line
    assert out_path.is_file(), f"no report at {out_line!r}"
    return json.loads(out_path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("path", EXAMPLE_PATHS, ids=[p.stem for p in EXAMPLE_PATHS])
def test_example_json_parses(path: Path) -> None:
    assert path.is_file()
    data = _load_example(path)
    assert isinstance(data, dict)


def _assert_required_fields(data: dict) -> None:
    for key in REQUIRED_KEYS:
        assert key in data, f"missing {key}"
    assert isinstance(data["proposal_id"], str) and data["proposal_id"].strip()
    assert isinstance(data["proposal_kind"], str) and data["proposal_kind"].strip()
    assert isinstance(data["proposed_change_summary"], str)
    assert isinstance(data["proposed_patch_text"], str)
    assert isinstance(data["operator_question"], str)
    assert isinstance(data["target_paths"], list) and all(
        isinstance(p, str) for p in data["target_paths"]
    )
    assert isinstance(data["target_surfaces"], list) and all(
        isinstance(s, str) for s in data["target_surfaces"]
    )
    assert isinstance(data["evidence_refs"], list) and all(
        isinstance(s, str) for s in data["evidence_refs"]
    )


@pytest.mark.parametrize("path", EXAMPLE_PATHS, ids=[p.stem for p in EXAMPLE_PATHS])
def test_example_has_required_fields(path: Path) -> None:
    _assert_required_fields(_load_example(path))


def test_clean_docs_exits_zero_advisory_authority() -> None:
    proc = _run_on_repo(EXAMPLES / "counterfactual-clean-docs.example.json")
    report = _report_from_run(proc)
    auth = report["authority"]
    assert auth["recordAuthority"] == "none"
    assert auth["gateEffect"] == "none"
    assert auth["mergeAuthority"] == "none"
    assert auth["simulationOnly"] is True


def test_dangerous_merge_authority_risk_and_reject_or_revise() -> None:
    proc = _run_on_repo(EXAMPLES / "counterfactual-dangerous-merge-authority.example.json")
    report = _report_from_run(proc)
    assert report["doctrine_drift_risks"]
    assert report["recommendation"]["decision"] in ("reject", "revise")


def test_portable_emulation_clarification_not_spurious_reject() -> None:
    proc = _run_on_repo(EXAMPLES / "counterfactual-portable-emulation.example.json")
    report = _report_from_run(proc)
    auth = report["authority"]
    assert auth["recordAuthority"] == "none"
    assert auth["gateEffect"] == "none"
    assert auth["mergeAuthority"] == "none"
    assert auth["simulationOnly"] is True
    assert report["recommendation"]["decision"] != "reject"


def test_examples_avoid_approval_merged_corpus_claims() -> None:
    """Examples must not claim the proposal is already approved or merged."""
    bad_substrings = (
        '"status": "approved"',
        '"is_approved": true',
        "this proposal is approved",
        "has been merged to main",
    )
    for path in EXAMPLE_PATHS:
        text = path.read_text(encoding="utf-8").lower()
        for bad in bad_substrings:
            assert bad.lower() not in text, f"{path.name} contains {bad!r}"
