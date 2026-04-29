"""Tests for work-strategy validate_strategy_packet (derived reports; no Record writes)."""

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


def _load_validator_module():
    ws = str(_scripts_ws())
    if ws not in sys.path:
        sys.path.insert(0, ws)
    path = _scripts_ws() / "validate_strategy_packet.py"
    spec = importlib.util.spec_from_file_location("validate_strategy_packet", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


vsp = _load_validator_module()


def test_word_count_helper() -> None:
    assert vsp.word_count("one two three") == 3


def test_read_text_if_possible(tmp_path: Path) -> None:
    p = tmp_path / "x.md"
    p.write_text("hello", encoding="utf-8")
    assert vsp.read_text_if_possible(p) == "hello"
    assert vsp.read_text_if_possible(tmp_path / "missing.md") is None


def test_scan_markers_unresolved() -> None:
    r = vsp.scan_markers("TODO fix\nNEEDS REVIEW here\n???", vsp.UNRESOLVED_MARKERS)
    assert r["total_hits"] >= 3


def test_summarize_validator_status_order() -> None:
    assert (
        vsp.summarize_validator_status(
            [
                {"status": "pass"},
                {"status": "needs_review"},
            ]
        )
        == "needs_review"
    )
    assert (
        vsp.summarize_validator_status(
            [
                {"status": "needs_review"},
                {"status": "fail"},
            ]
        )
        == "fail"
    )


def test_pass_carry_harness_fixture(tmp_path: Path) -> None:
    out = tmp_path / "val.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
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
    assert data["schema_version"] == "work-strategy-validation-report.v1"
    assert data["summary"]["status"] == "pass"


def test_missing_artifact_fail(tmp_path: Path) -> None:
    out = tmp_path / "val.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
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
    assert data["summary"]["status"] == "fail"


def test_missing_source_needs_review(tmp_path: Path) -> None:
    out = tmp_path / "val.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
        "--source",
        "examples/work-strategy/carry-harness/no-such-source.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["status"] == "needs_review"


def test_thin_artifact_needs_review(tmp_path: Path) -> None:
    out = tmp_path / "val.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
        "--artifact",
        "examples/work-strategy/validators/sample-artifact-thin.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["status"] == "needs_review"


def test_unresolved_markers_needs_review(tmp_path: Path) -> None:
    out = tmp_path / "val.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
        "--artifact",
        "examples/work-strategy/validators/sample-artifact-unresolved.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["status"] == "needs_review"
    ids = [v["id"] for v in data["validators"]]
    assert "unresolved_marker_scan" in ids


def test_contradiction_markers_needs_review(tmp_path: Path) -> None:
    art = tmp_path / "tension.md"
    text = "# Heading\n\n"
    text += " ".join(["word"] * 55)
    text += "\n\nThere is contradiction between two narratives worth revisiting.\n"
    art.write_text(text, encoding="utf-8")
    out = tmp_path / "val.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
        "--artifact",
        str(art),
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["status"] == "needs_review"
    assert any(v["id"] == "contradiction_marker_scan" for v in data["validators"])


def test_forbidden_out_under_users(tmp_path: Path) -> None:
    bad_out = REPO_ROOT / "users" / "grace-mar" / "_validator_forbidden_test.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
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
    assert payload["summary"]["status"] == "fail"


def test_json_stdout(tmp_path: Path) -> None:
    out = tmp_path / "val.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
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


def test_fail_on_status_never(tmp_path: Path) -> None:
    out = tmp_path / "val.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "validate_strategy_packet.py"),
        "--artifact",
        "examples/work-strategy/carry-harness/does-not-exist-artifact.md",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
        "--fail-on-status",
        "never",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["status"] == "fail"


def test_carry_harness_run_validators_embeds_summary(tmp_path: Path) -> None:
    receipt_path = tmp_path / "receipt.json"
    val_path = tmp_path / "from-harness.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "run_carry_harness.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--source",
        "examples/work-strategy/carry-harness/sample-source.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--gate-snippet",
        "examples/work-strategy/carry-harness/sample-gate-snippet.md",
        "--out",
        str(receipt_path),
        "--repo-root",
        str(REPO_ROOT),
        "--run-validators",
        "--validation-report",
        str(val_path),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert "validation_summary" in receipt
    assert receipt["validation_summary"]["status"] == "pass"
    assert receipt.get("validation_report_path") is not None
    assert val_path.is_file()
    val_data = json.loads(val_path.read_text(encoding="utf-8"))
    assert val_data["schema_version"] == "work-strategy-validation-report.v1"


def test_validate_packet_forbidden_output(tmp_path: Path) -> None:
    from packet_common import is_forbidden_record_path

    bad = REPO_ROOT / "users" / "grace-mar" / "x.json"
    rep = vsp.validate_packet(
        repo_root=REPO_ROOT,
        task_arg=None,
        sources=[],
        artifacts=["examples/work-strategy/carry-harness/sample-artifact.md"],
        gate_snippet_arg=None,
        run_id="test-run",
        validation_out_path=bad,
    )
    assert rep["summary"]["status"] == "fail"
    assert rep["record_boundary"]["canonical_write_violation"] is True
    assert is_forbidden_record_path(bad, REPO_ROOT) is True
