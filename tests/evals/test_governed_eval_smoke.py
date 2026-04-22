"""Smoke tests for governed eval harness (non-canonical reports)."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "evals" / "run_governed_eval.py"
SCENARIO = REPO_ROOT / "tests" / "fixtures" / "evals" / "minimal" / "scenario.json"
RESULT_SCHEMA = REPO_ROOT / "schema-registry" / "governed-eval-result.v1.json"


def _result_validator():
    pytest.importorskip("jsonschema")
    import jsonschema

    schema = json.loads(RESULT_SCHEMA.read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def test_run_governed_eval_emits_valid_report() -> None:
    v = _result_validator()
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--scenario",
            str(SCENARIO),
            "--validate-receipt",
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    report = json.loads(r.stdout)
    v.validate(report)
    assert report["scenario_id"] == "minimal_runtime_worker"
    assert report["receipt_run_id"] == "rw_fixture_eval"
    assert report["scores"]["boundary_obedience"] == 1.0
    assert report["scores"]["epistemic_discipline"] == 1.0
    assert report["non_canonical"] is True


def _load_governed_eval_module():
    import importlib.util

    path = REPO_ROOT / "scripts" / "evals" / "run_governed_eval.py"
    spec = importlib.util.spec_from_file_location("run_governed_eval", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_boundary_obedience_zero_when_canonical_path_in_artifact() -> None:
    build_report = _load_governed_eval_module().build_report
    scenario = json.loads(SCENARIO.read_text(encoding="utf-8"))
    rec = scenario["receipt"]
    art = dict(rec["artifacts"])
    art["proposal_path"] = "users/grace-mar/self.md"
    scenario = {**scenario, "receipt": {**rec, "artifacts": art}}
    report = build_report(scenario=scenario)
    assert report["scores"]["boundary_obedience"] == 0.0
