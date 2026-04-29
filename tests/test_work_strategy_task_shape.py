"""Tests for work-strategy task-shape classifier (derived reports; no Record writes)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _scripts_ws() -> Path:
    return REPO_ROOT / "scripts" / "work_strategy"


def _load_classifier():
    ws = str(_scripts_ws())
    if ws not in sys.path:
        sys.path.insert(0, ws)
    path = _scripts_ws() / "classify_task_shape.py"
    spec = importlib.util.spec_from_file_location("classify_task_shape", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cts = _load_classifier()


FIXTURES = [
    ("examples/work-strategy/task-shapes/sample-watch-update.md", "watch_update"),
    ("examples/work-strategy/task-shapes/sample-notebook-synthesis.md", "notebook_synthesis"),
    ("examples/work-strategy/task-shapes/sample-decision-point.md", "decision_point"),
    ("examples/work-strategy/task-shapes/sample-gate-candidate-prep.md", "gate_candidate_prep"),
    ("examples/work-strategy/task-shapes/sample-contradiction-review.md", "contradiction_review"),
    ("examples/work-strategy/task-shapes/sample-source-expansion.md", "source_expansion"),
]


@pytest.mark.parametrize("rel_task,expected_primary", FIXTURES)
def test_fixture_primary_shape(rel_task: str, expected_primary: str, tmp_path: Path) -> None:
    out = tmp_path / "ts.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "classify_task_shape.py"),
        "--task",
        rel_task,
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["classification"]["primary_shape"] == expected_primary


def test_frontmatter_overrides_keyword_noise(tmp_path: Path) -> None:
    out = tmp_path / "ts.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "classify_task_shape.py"),
        "--task",
        "examples/work-strategy/task-shapes/sample-frontmatter-override.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["classification"]["primary_shape"] == "notebook_synthesis"
    assert data["classification"]["confidence"] == "high"
    assert any(s.startswith("frontmatter:") for s in data["classification"]["matched_signals"])


def test_ambiguous_low_confidence(tmp_path: Path) -> None:
    out = tmp_path / "ts.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "classify_task_shape.py"),
        "--task",
        "examples/work-strategy/task-shapes/sample-ambiguous.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["classification"]["confidence"] == "low"
    assert data["classification"]["notes"]


def test_fail_on_ambiguous_nonzero(tmp_path: Path) -> None:
    out = tmp_path / "ts.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "classify_task_shape.py"),
        "--task",
        "examples/work-strategy/task-shapes/sample-ambiguous.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
        "--fail-on-ambiguous",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 1


def test_forbidden_out_users(tmp_path: Path) -> None:
    bad_out = REPO_ROOT / "users" / "grace-mar" / "_task_shape_forbidden_test.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "classify_task_shape.py"),
        "--task",
        "examples/work-strategy/task-shapes/sample-decision-point.md",
        "--out",
        str(bad_out),
        "--repo-root",
        str(REPO_ROOT),
        "--json",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 1
    assert bad_out.is_file() is False
    payload = json.loads(r.stdout)
    assert payload["record_boundary"]["canonical_write_violation"] is True


def test_json_stdout(tmp_path: Path) -> None:
    out = tmp_path / "ts.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "classify_task_shape.py"),
        "--task",
        "examples/work-strategy/task-shapes/sample-decision-point.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
        "--json",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    json.loads(r.stdout)


def test_carry_harness_classify_embeds_receipt(tmp_path: Path) -> None:
    receipt_path = tmp_path / "receipt.json"
    ts_path = tmp_path / "from-harness.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "run_carry_harness.py"),
        "--task",
        "examples/work-strategy/task-shapes/sample-decision-point.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--out",
        str(receipt_path),
        "--repo-root",
        str(REPO_ROOT),
        "--classify-task-shape",
        "--task-shape-report",
        str(ts_path),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["task_shape"] == "decision_point"
    assert receipt["task_shape_confidence"] in ("high", "medium", "low")
    assert receipt.get("task_shape_expected_outputs")
    assert ts_path.is_file()


def test_validator_task_shape_cli(tmp_path: Path) -> None:
    out = tmp_path / "val.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
        "--task",
        "examples/work-strategy/task-shapes/sample-decision-point.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
        "--task-shape",
        "decision_point",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data.get("task_shape", {}).get("primary_shape") == "decision_point"
    assert any(v["id"] == "task_shape_expectations" for v in data["validators"])
