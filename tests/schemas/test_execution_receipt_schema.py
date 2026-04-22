"""Execution receipt schema + runtime worker emission (non-canonical)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RECEIPT_SCHEMA = REPO_ROOT / "schema-registry" / "execution-receipt.v1.json"
WORKER_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "grace_mar_runtime_worker.py"


def _receipt_validator():
    pytest.importorskip("jsonschema")
    import jsonschema

    schema = json.loads(RECEIPT_SCHEMA.read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(schema)


def _minimal_valid_receipt() -> dict:
    return {
        "run_id": "rw_fixture",
        "timestamp": "2026-01-01T00:00:00Z",
        "task_mode": "inspect_work_area",
        "scope": {
            "root": "docs/skill-work/work-strategy/strategy-notebook",
            "max_files": 10,
            "max_chars": 1000,
        },
        "worker_route": {
            "resolved": False,
            "task_type": None,
            "shared_workers": [],
            "routed_worker": None,
            "entrypoints": {},
        },
        "epistemic": {
            "decision": "allow_with_review",
            "abstained": False,
            "evidence_state": None,
            "notes": None,
        },
        "artifacts": {
            "trace_path": "runtime/runtime-worker/traces/index.jsonl",
            "proposal_path": "runtime/runtime-worker/proposals/rw_fixture.md",
        },
        "outcome": {"status": "ok", "error": None},
        "model_policy": {
            "allowed_tier": "A",
            "resolved_provider": None,
            "resolved_model": None,
            "fallback_chain": ["B", "A"],
            "requires_human_review": False,
        },
        "scope_verification": None,
        "non_canonical": True,
    }


def test_schema_and_minimal_instance_validate() -> None:
    v = _receipt_validator()
    import jsonschema

    meta = v.schema
    jsonschema.validators.validator_for(meta).check_schema(meta)
    v.validate(_minimal_valid_receipt())
    # nullable model_policy on schema — explicit null is valid
    alt = {**_minimal_valid_receipt(), "model_policy": None}
    v.validate(alt)


@pytest.fixture
def worker_env(tmp_path: Path) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k != "OPENAI_API_KEY"}
    env["GRACE_MAR_RUNTIME_WORKER_HOME"] = str(tmp_path / "runtime-worker")
    return env


def test_dry_run_writes_receipt(tmp_path: Path, worker_env: dict[str, str]) -> None:
    v = _receipt_validator()
    r = subprocess.run(
        [
            sys.executable,
            str(WORKER_SCRIPT),
            "--task",
            "inspect_work_area",
            "--dry-run",
            "--repo-root",
            str(REPO_ROOT),
            "--scope",
            "docs/skill-work/work-strategy/strategy-notebook",
            "--max-files",
            "8",
            "--max-chars",
            "12000",
        ],
        cwd=str(REPO_ROOT),
        env=worker_env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    wh = Path(worker_env["GRACE_MAR_RUNTIME_WORKER_HOME"])
    proposals = list((wh / "proposals").glob("rw_*.md"))
    assert len(proposals) == 1
    run_id = proposals[0].stem
    receipt_path = wh / "receipts" / f"{run_id}.json"
    assert receipt_path.is_file()
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    v.validate(receipt)
    assert receipt["artifacts"]["proposal_path"].endswith(f"{run_id}.md")
    sv = receipt.get("scope_verification")
    assert isinstance(sv, dict)
    assert sv["traversal"]["files_seen"] >= 1
    assert sv["traversal"]["files_opened"] >= 1
    assert sv.get("status") in (
        "aligned",
        "unstated",
        "overclaim_suspected",
        "underclaim_suspected",
        "parse_failed",
    )


def test_task_type_strategy_receipt_routing(tmp_path: Path, worker_env: dict[str, str]) -> None:
    v = _receipt_validator()
    r = subprocess.run(
        [
            sys.executable,
            str(WORKER_SCRIPT),
            "--task",
            "inspect_work_area",
            "--task-type",
            "strategy",
            "--dry-run",
            "--repo-root",
            str(REPO_ROOT),
            "--scope",
            "docs/skill-work/work-strategy/strategy-notebook",
            "--max-files",
            "8",
            "--max-chars",
            "12000",
        ],
        cwd=str(REPO_ROOT),
        env=worker_env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    wh = Path(worker_env["GRACE_MAR_RUNTIME_WORKER_HOME"])
    proposals = list((wh / "proposals").glob("rw_*.md"))
    run_id = proposals[0].stem
    receipt = json.loads((wh / "receipts" / f"{run_id}.json").read_text(encoding="utf-8"))
    v.validate(receipt)
    wr = receipt["worker_route"]
    assert wr["resolved"] is True
    assert wr["task_type"] == "strategy"
    assert wr["routed_worker"] == "strategy_worker"
    assert receipt["model_policy"]["allowed_tier"] == "B"


def test_task_type_strategy_quick_scan_receipt_model_policy(tmp_path: Path, worker_env: dict[str, str]) -> None:
    v = _receipt_validator()
    r = subprocess.run(
        [
            sys.executable,
            str(WORKER_SCRIPT),
            "--task",
            "inspect_work_area",
            "--task-type",
            "strategy",
            "--task-subtype",
            "quick_scan",
            "--dry-run",
            "--repo-root",
            str(REPO_ROOT),
            "--scope",
            "docs/skill-work/work-strategy/strategy-notebook",
            "--max-files",
            "8",
            "--max-chars",
            "12000",
        ],
        cwd=str(REPO_ROOT),
        env=worker_env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    wh = Path(worker_env["GRACE_MAR_RUNTIME_WORKER_HOME"])
    run_id = next((wh / "proposals").glob("rw_*.md")).stem
    receipt = json.loads((wh / "receipts" / f"{run_id}.json").read_text(encoding="utf-8"))
    v.validate(receipt)
    assert receipt["model_policy"]["allowed_tier"] == "B"
    assert receipt.get("task_subtype") == "quick_scan"
