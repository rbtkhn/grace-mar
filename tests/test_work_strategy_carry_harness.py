"""Tests for work-strategy carry harness (derived receipts; no Record writes)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_carry_module():
    ws = str(REPO_ROOT / "scripts" / "work_strategy")
    if ws not in sys.path:
        sys.path.insert(0, ws)
    path = REPO_ROOT / "scripts" / "work_strategy" / "run_carry_harness.py"
    spec = importlib.util.spec_from_file_location("run_carry_harness", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


carry = _load_carry_module()


def test_word_count_basic() -> None:
    assert carry.word_count("one two three") == 3
    assert carry.word_count("") == 0


@pytest.mark.parametrize(
    "rel",
    [
        "users/grace-mar/x.json",
        "users/foo/bar.txt",
    ],
)
def test_is_forbidden_record_path_users(rel: str) -> None:
    p = REPO_ROOT / rel
    assert carry.is_forbidden_record_path(p, REPO_ROOT) is True


def test_is_forbidden_record_path_bot_prompt() -> None:
    p = REPO_ROOT / "bot" / "prompt.py"
    assert carry.is_forbidden_record_path(p, REPO_ROOT) is True


def test_is_forbidden_runtime_ok() -> None:
    p = REPO_ROOT / "runtime" / "work-strategy" / "carry-receipts" / "x.json"
    assert carry.is_forbidden_record_path(p, REPO_ROOT) is False


def test_sample_pass_receipt(tmp_path: Path) -> None:
    out = tmp_path / "receipt.json"
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/work_strategy/run_carry_harness.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--source",
        "examples/work-strategy/carry-harness/sample-source.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--gate-snippet",
        "examples/work-strategy/carry-harness/sample-gate-snippet.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["result"] == "pass"
    assert data["schema_version"] == "work-strategy-carry-receipt.v1"
    assert data["lane"] == "work-strategy"


def test_missing_artifact_fail(tmp_path: Path) -> None:
    out = tmp_path / "receipt.json"
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/work_strategy/run_carry_harness.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--artifact",
        "examples/work-strategy/carry-harness/does-not-exist-artifact.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 1
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["result"] == "fail"


def test_thin_artifact_needs_review(tmp_path: Path) -> None:
    thin = tmp_path / "thin.md"
    thin.write_text("short.", encoding="utf-8")
    out = tmp_path / "receipt.json"
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/work_strategy/run_carry_harness.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--artifact",
        str(thin),
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["result"] == "needs_review"


def test_forbidden_out_no_write(tmp_path: Path) -> None:
    bad_out = REPO_ROOT / "users" / "grace-mar" / "_carry_harness_forbidden_test.json"
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/work_strategy/run_carry_harness.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
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
    out = tmp_path / "receipt.json"
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/work_strategy/run_carry_harness.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
        "--json",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    json.loads(r.stdout)


def test_fail_on_result_never(tmp_path: Path) -> None:
    out = tmp_path / "receipt.json"
    cmd = [
        sys.executable,
        str(REPO_ROOT / "scripts/work_strategy/run_carry_harness.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--artifact",
        "examples/work-strategy/carry-harness/does-not-exist-artifact.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
        "--fail-on-result",
        "never",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["result"] == "fail"


def test_inspect_artifact(tmp_path: Path) -> None:
    p = tmp_path / "x.md"
    p.write_text("word " * 60, encoding="utf-8")
    obs = carry.inspect_artifact(p, tmp_path)
    assert obs["exists"] is True
    assert obs["word_count"] == 60

