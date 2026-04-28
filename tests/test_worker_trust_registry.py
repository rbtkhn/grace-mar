"""Worker trust registry schema + policy verification."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNTIME = REPO_ROOT / "scripts" / "runtime"
VERIFY_SCRIPT = RUNTIME / "verify_worker_trust_registry.py"
REGISTRY_PATH = REPO_ROOT / "config" / "runtime_workers" / "worker-trust-registry.v1.json"
SCHEMA_PATH = REPO_ROOT / "schemas" / "worker-trust-registry.v1.schema.json"


@pytest.fixture
def verify_module():
    pytest.importorskip("jsonschema")
    if str(RUNTIME) not in sys.path:
        sys.path.insert(0, str(RUNTIME))
    import verify_worker_trust_registry as v

    return v


def test_verifier_script_exits_zero_on_repo_registry() -> None:
    pytest.importorskip("jsonschema")
    r = subprocess.run(
        [sys.executable, str(VERIFY_SCRIPT), "--repo-root", str(REPO_ROOT)],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    assert r.returncode == 0, r.stderr + r.stdout


def test_policy_forbidden_in_allowed(verify_module, tmp_path: Path) -> None:
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    reg["workers"][0]["allowed_actions"] = list(reg["workers"][0]["allowed_actions"]) + ["merge_candidate"]
    bad = Path(tmp_path / "bad.json")
    bad.write_text(json.dumps(reg), encoding="utf-8")
    errs = verify_module.verify_worker_trust_registry(
        REPO_ROOT,
        bad,
        SCHEMA_PATH,
        skip_yaml_parity=True,
    )
    assert any("forbidden actions in allowed_actions" in e for e in errs)


def test_policy_stage_without_gate(verify_module, tmp_path: Path) -> None:
    pytest.importorskip("jsonschema")
    reg = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    for w in reg["workers"]:
        if w["id"] == "tacit_worker":
            w["gate_review_required"] = False
            break
    bad = Path(tmp_path / "bad.json")
    bad.write_text(json.dumps(reg), encoding="utf-8")
    errs = verify_module.verify_worker_trust_registry(
        REPO_ROOT,
        bad,
        SCHEMA_PATH,
        skip_yaml_parity=True,
    )
    assert any("stage_candidate requires gate_review_required" in e for e in errs)


def test_schema_validation_failure(verify_module, tmp_path: Path) -> None:
    pytest.importorskip("jsonschema")
    bad = Path(tmp_path / "bad.json")
    bad.write_text(json.dumps({"version": 1}), encoding="utf-8")
    errs = verify_module.verify_worker_trust_registry(
        REPO_ROOT,
        bad,
        SCHEMA_PATH,
        skip_yaml_parity=True,
    )
    assert errs and any("schema:" in e for e in errs)
