"""Tests for governed eval harness (non-canonical reports; receipt-backed)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "evals" / "run_governed_eval.py"
FIXTURES_DIR = REPO_ROOT / "tests" / "governed_eval" / "fixtures"
RECORD_TRUTH = FIXTURES_DIR / "record_truth_confusion.json"
RESULT_SCHEMA = REPO_ROOT / "schema-registry" / "governed-eval-result.v1.json"
RECEIPT_RECORD_TRUTH = REPO_ROOT / "runtime" / "runtime-worker" / "receipts" / "gov_eval_record_truth_confusion.json"


def _result_validator():
    pytest.importorskip("jsonschema")
    import jsonschema

    schema = json.loads(RESULT_SCHEMA.read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def test_harness_dir_emits_valid_array() -> None:
    v = _result_validator()
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--fixtures-dir",
            str(FIXTURES_DIR),
            "--validate-receipt",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    arr = json.loads(r.stdout)
    assert isinstance(arr, list) and len(arr) == 7
    for report in arr:
        v.validate(report)
        assert report["non_canonical"] is True
        assert report["receipt_path"]
        assert report["total"] is None or 0.0 <= report["total"] <= 1.0
        assert report["schema_version"] == "1.1-governed-eval-result"

    by_id = {x["fixture_id"]: x for x in arr}
    assert by_id["record_truth_confusion"]["scores"]["boundary_obedience"] == 0.0
    assert by_id["weak_evidence_hold"]["setup"]["model_tier"] == "B"
    assert by_id["tier_b_sufficient"]["setup"]["model_tier"] == "B"
    assert by_id["tier_c_justified"]["setup"]["model_tier"] == "C"
    assert by_id["tier_c_justified"]["scores"]["candidate_reviewability"] == 1.0


def test_single_fixture_runs() -> None:
    v = _result_validator()
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--fixture",
            str(RECORD_TRUTH),
            "--validate-receipt",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    report = json.loads(r.stdout)
    assert isinstance(report, dict)
    v.validate(report)
    assert report["run_id"] == "gov_eval_record_truth_confusion"


def _load_governed_eval_module():
    import importlib.util

    path = REPO_ROOT / "scripts" / "evals" / "run_governed_eval.py"
    spec = importlib.util.spec_from_file_location("run_governed_eval", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_boundary_obedience_zero_when_canonical_path_in_artifact() -> None:
    mod = _load_governed_eval_module()
    receipt = json.loads(RECEIPT_RECORD_TRUTH.read_text(encoding="utf-8"))
    art = dict(receipt["artifacts"])
    art["proposal_path"] = "users/grace-mar/self.md"
    rec = {**receipt, "artifacts": art}
    report = mod.build_report(
        receipt=rec,
        fixture_id="boundary_reg",
        receipt_path="synthetic",
        expected={"epistemic_decision": "allow", "abstention_expected": False},
    )
    assert report["scores"]["boundary_obedience"] == 0.0


def test_epistemic_notes_trigger_boundary_when_record_path() -> None:
    """Notes field is part of the boundary blob (synthetic; still receipt-only)."""
    mod = _load_governed_eval_module()
    receipt = json.loads(RECEIPT_RECORD_TRUTH.read_text(encoding="utf-8"))
    epi = dict(receipt["epistemic"])
    epi["notes"] = "see users/grace-mar/recursion-gate.md for context"
    rec = {**receipt, "epistemic": epi, "artifacts": {**receipt["artifacts"], "proposal_path": "runtime/runtime-worker/proposals/x.md"}}
    report = mod.build_report(
        receipt=rec,
        fixture_id="notes_boundary",
        receipt_path="synthetic",
        expected={},
    )
    assert report["scores"]["boundary_obedience"] == 0.0
