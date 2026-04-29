"""Tests for work-strategy review packet builder (derived artifacts; no Record writes)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _scripts_ws() -> Path:
    return REPO_ROOT / "scripts" / "work_strategy"


def _load_builder():
    ws = str(_scripts_ws())
    if ws not in sys.path:
        sys.path.insert(0, ws)
    path = _scripts_ws() / "build_review_packet.py"
    spec = importlib.util.spec_from_file_location("build_review_packet", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


brp = _load_builder()


def test_minimal_task_and_artifact_subprocess(tmp_path: Path) -> None:
    out = tmp_path / "rp.json"
    md = tmp_path / "rp.md"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "build_review_packet.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--out",
        str(out),
        "--markdown-out",
        str(md),
        "--repo-root",
        str(REPO_ROOT),
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["schema_version"] == "work-strategy-review-packet.v1"
    assert data["review_readiness"]["status"] == "needs_review"
    body = md.read_text(encoding="utf-8")
    for label in ("## A —", "## B —", "## C —", "## D —", "## E —", "## F —", "## G —", "## H —", "## I —", "## J —"):
        assert label in body


def test_with_validation_fixture_pass_readiness(tmp_path: Path) -> None:
    out = tmp_path / "rp.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "build_review_packet.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--validation-report",
        "runtime/work-strategy/validation-reports/sample-validation.json",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
        "--fail-on-readiness",
        "never",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["validation"]["status"] == "pass"
    assert data["review_readiness"]["status"] == "pass"


def test_with_task_shape_report(tmp_path: Path) -> None:
    out = tmp_path / "rp.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "build_review_packet.py"),
        "--task",
        "examples/work-strategy/task-shapes/sample-decision-point.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--validation-report",
        "runtime/work-strategy/validation-reports/sample-validation.json",
        "--task-shape-report",
        "runtime/work-strategy/task-shape-reports/sample-decision-point.json",
        "--out",
        str(out),
        "--repo-root",
        str(REPO_ROOT),
        "--fail-on-readiness",
        "never",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["task_shape"]["primary"] == "decision_point"


def test_forbidden_out_under_users(tmp_path: Path) -> None:
    out_path = REPO_ROOT / "users/grace-mar/__review_packet_forbidden_test__.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "build_review_packet.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--out",
        str(out_path.relative_to(REPO_ROOT)),
        "--repo-root",
        str(REPO_ROOT),
        "--fail-on-readiness",
        "never",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    assert not out_path.exists()


def test_json_stdout(tmp_path: Path) -> None:
    cmd = [
        sys.executable,
        str(_scripts_ws() / "build_review_packet.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--json",
        "--repo-root",
        str(REPO_ROOT),
        "--fail-on-readiness",
        "never",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    data = json.loads(r.stdout)
    assert data["lane"] == "work-strategy"


def test_fail_on_readiness_never(tmp_path: Path) -> None:
    """needs_review readiness still exits 0 when policy is never."""
    cmd = [
        sys.executable,
        str(_scripts_ws() / "build_review_packet.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--json",
        "--repo-root",
        str(REPO_ROOT),
        "--fail-on-readiness",
        "never",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data["review_readiness"]["status"] == "needs_review"


def test_harness_build_review_packet_receipt_keys(tmp_path: Path) -> None:
    rec = tmp_path / "carry.json"
    rp = tmp_path / "review.json"
    cmd = [
        sys.executable,
        str(_scripts_ws() / "run_carry_harness.py"),
        "--task",
        "examples/work-strategy/carry-harness/sample-task.md",
        "--source",
        "examples/work-strategy/carry-harness/sample-source.md",
        "--artifact",
        "examples/work-strategy/carry-harness/sample-artifact.md",
        "--out",
        str(rec),
        "--repo-root",
        str(REPO_ROOT),
        "--build-review-packet",
        "--review-packet",
        str(rp),
        "--fail-on-result",
        "never",
    ]
    r = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr + r.stdout
    receipt = json.loads(rec.read_text(encoding="utf-8"))
    assert "review_packet_path" in receipt
    assert "review_readiness" in receipt
    assert receipt["review_readiness"]["status"] in ("pass", "needs_review", "fail")
    assert rp.is_file()


def test_render_has_standard_headings() -> None:
    pkt = brp.build_review_packet_dict(
        repo_root=REPO_ROOT,
        run_id="rid",
        created_at="2026-01-01T00:00:00+00:00",
        task_arg="examples/work-strategy/carry-harness/sample-task.md",
        sources=[],
        artifacts=["examples/work-strategy/carry-harness/sample-artifact.md"],
        gate_snippet_arg=None,
        carry_receipt_arg=None,
        validation_report_arg=None,
        task_shape_report_arg=None,
        title_override=None,
        json_out=None,
        markdown_out=None,
    )
    md = brp.render_review_packet_markdown(pkt)
    assert "## A — Task statement" in md
    assert "## J — Why this is not canonical" in md
