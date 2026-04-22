"""Tests for run_runtime_peer_review (non-canonical draft review)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PEER_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "run_runtime_peer_review.py"
PEER_SCHEMA = REPO_ROOT / "schema-registry" / "runtime-peer-review.v1.json"

_MINI_RECEIPT_BASE = {
    "run_id": "draft_x",
    "timestamp": "2026-01-01T00:00:00Z",
    "task_mode": "inspect_work_area",
    "task_subtype": None,
    "scope": {
        "root": "docs",
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
        "decision": "allow",
        "abstained": False,
        "evidence_state": None,
        "notes": None,
    },
    "artifacts": {
        "trace_path": "runtime/runtime-worker/traces/index.jsonl",
        "proposal_path": "runtime/runtime-worker/proposals/draft_x.md",
    },
    "outcome": {"status": "ok", "error": None},
    "model_policy": {
        "allowed_tier": "A",
        "resolved_provider": None,
        "resolved_model": None,
        "fallback_chain": ["B", "A"],
        "requires_human_review": False,
    },
    "non_canonical": True,
}


def _peer_schema_validator():
    pytest.importorskip("jsonschema")
    import jsonschema

    s = json.loads(PEER_SCHEMA.read_text(encoding="utf-8"))
    return jsonschema.Draft202012Validator(s)


def test_peer_review_overclaim_flagged(tmp_path: Path) -> None:
    v = _peer_schema_validator()
    wh = tmp_path / "runtime-worker"
    (wh / "receipts").mkdir(parents=True)
    (wh / "proposals").mkdir(parents=True)
    rec = {
        **_MINI_RECEIPT_BASE,
        "scope_verification": {
            "traversal": {
                "files_seen": 2,
                "files_opened": 1,
                "chunks_read": 1,
                "paths_sample": ["docs/a.md"],
            },
            "stated_coverage": {"files_claimed": 100, "source": "proposal_regex"},
            "coverage_ratio": 0.01,
            "status": "overclaim_suspected",
            "warnings": ["stated file count (100) exceeds opened count (1) — overclaim"],
        },
    }
    (wh / "receipts" / "draft_x.json").write_text(json.dumps(rec, indent=2), encoding="utf-8")
    (wh / "proposals" / "draft_x.md").write_text(
        "# p\n- **files listed:** 100\n", encoding="utf-8"
    )
    env = {**os.environ, "GRACE_MAR_RUNTIME_WORKER_HOME": str(wh)}
    r = subprocess.run(
        [
            sys.executable,
            str(PEER_SCRIPT),
            "--repo-root",
            str(REPO_ROOT),
            "--draft-run-id",
            "draft_x",
            "--task",
            "read scope",
        ],
        env=env,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    out = json.loads(r.stdout)
    v.validate(out)
    assert out["verdict"] == "flagged"
    assert out["overclaim"]["detected"] is True
    assert out["review_run_id"].startswith("pr_")
    assert out["draft_run_id"] == "draft_x"


def test_peer_review_draft_mentions_self_flagged(tmp_path: Path) -> None:
    v = _peer_schema_validator()
    wh = tmp_path / "runtime-worker"
    (wh / "receipts").mkdir(parents=True)
    (wh / "proposals").mkdir(parents=True)
    rec = {**_MINI_RECEIPT_BASE, "scope_verification": None}
    (wh / "receipts" / "draft_y.json").write_text(
        json.dumps({**rec, "run_id": "draft_y"}), encoding="utf-8"
    )
    (wh / "proposals" / "draft_y.md").write_text("see users/grace-mar/self.md", encoding="utf-8")
    env = {**os.environ, "GRACE_MAR_RUNTIME_WORKER_HOME": str(wh)}
    r = subprocess.run(
        [
            sys.executable,
            str(PEER_SCRIPT),
            "--repo-root",
            str(REPO_ROOT),
            "--draft-run-id",
            "draft_y",
            "--task",
            "t",
        ],
        env=env,
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    out = json.loads(r.stdout)
    v.validate(out)
    assert out["verdict"] == "flagged"
    assert any("self.md" in f for f in out["flags"])
