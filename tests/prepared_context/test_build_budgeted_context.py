"""Tests for scripts/prepared_context/build_budgeted_context.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SCRIPT = REPO_ROOT / "scripts" / "prepared_context" / "build_budgeted_context.py"
SWEEP_SCRIPT = REPO_ROOT / "scripts" / "prepared_context" / "sweep_budgets.py"
SEED_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "observations-seed.jsonl"


def _minimal_obs(oid: str, lane: str, title: str, summary: str) -> dict:
    return {
        "obs_id": oid,
        "timestamp": "2026-04-01T12:00:00Z",
        "lane": lane,
        "source_kind": "test",
        "title": title,
        "summary": summary,
        "record_mutation_candidate": False,
        "source_path": None,
        "source_refs": [],
        "tags": [],
        "confidence": 0.9,
        "contradiction_refs": [],
        "notes": None,
    }


def test_build_budgeted_context_subprocess(tmp_path: Path) -> None:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    a = _minimal_obs("obs_test_001", "lane-x", "T1", "summary one about iran")
    b = _minimal_obs("obs_test_002", "lane-x", "T2", "summary two")
    b["timestamp"] = "2026-04-02T12:00:00Z"
    (obs_dir / "index.jsonl").write_text(
        json.dumps(a) + "\n" + json.dumps(b) + "\n", encoding="utf-8"
    )
    out = tmp_path / "prepared-context" / "out.md"
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--repo-root",
            str(tmp_path),
            "--lane",
            "lane-x",
            "--mode",
            "compact",
            "--query",
            "iran",
            "-o",
            str(out),
            "--budgets-file",
            str(REPO_ROOT / "config" / "context_budgets" / "lane-defaults.json"),
        ],
        env=env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr + r.stdout
    text = out.read_text(encoding="utf-8")
    assert "# Budgeted Context" in text
    assert "Policy mode: operator_only" in text
    assert "## Included" in text
    assert "## Excluded" in text
    assert "## Context Block" in text
    assert "Budget Notes" in text
    receipt = tmp_path / "prepared-context" / "last-budget-builds.json"
    assert receipt.is_file()
    data = json.loads(receipt.read_text(encoding="utf-8"))
    assert data["lanes"]["lane-x"]["mode"] == "compact"
    assert data["lanes"]["lane-x"].get("policy_mode") == "operator_only"
    assert "exclusions" in data["lanes"]["lane-x"]
    scores = data["lanes"]["lane-x"].get("scores")
    assert scores is not None, "receipt must contain benchmark scores"
    assert 0.0 <= scores["utilization"] <= 2.0
    assert 0.0 <= scores["coverage"] <= 1.0
    assert scores["included_count"] >= 0
    assert scores["total_candidates"] >= scores["included_count"]


def _seed_obs_dir(tmp_path: Path) -> Path:
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    (obs_dir / "index.jsonl").write_text(
        SEED_FIXTURE.read_text(encoding="utf-8"), encoding="utf-8"
    )
    return obs_dir


def test_score_flag_prints_json(tmp_path: Path) -> None:
    """--score flag emits benchmark metrics to stdout."""
    _seed_obs_dir(tmp_path)
    out = tmp_path / "prepared-context" / "out.md"
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable, str(SCRIPT),
            "--repo-root", str(tmp_path),
            "--lane", "work-strategy",
            "--mode", "compact",
            "-o", str(out),
            "--budgets-file", str(REPO_ROOT / "config" / "context_budgets" / "lane-defaults.json"),
            "--score",
        ],
        env=env, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    score_data = json.loads(r.stdout)
    assert score_data["lane"] == "work-strategy"
    assert score_data["mode"] == "compact"
    assert "utilization" in score_data
    assert "coverage" in score_data
    assert "mean_included_rank" in score_data
    assert score_data["utilization"] > 0, "seed data should produce non-zero utilization"
    assert score_data["coverage"] > 0, "seed data should produce non-zero coverage"


def test_benchmark_scores_across_modes(tmp_path: Path) -> None:
    """Deeper budget modes should include more content (higher utilization)."""
    _seed_obs_dir(tmp_path)
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    scores_by_mode: dict[str, dict] = {}
    for mode in ("compact", "medium", "deep"):
        out = tmp_path / "prepared-context" / f"out-{mode}.md"
        r = subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--repo-root", str(tmp_path),
                "--lane", "work-strategy",
                "--mode", mode,
                "-o", str(out),
                "--budgets-file", str(REPO_ROOT / "config" / "context_budgets" / "lane-defaults.json"),
                "--score",
            ],
            env=env, capture_output=True, text=True,
        )
        assert r.returncode == 0, f"{mode} failed: {r.stderr}"
        scores_by_mode[mode] = json.loads(r.stdout)
    assert scores_by_mode["deep"]["chars_included"] >= scores_by_mode["compact"]["chars_included"]


def test_sweep_budgets_json(tmp_path: Path) -> None:
    """sweep_budgets.py --json produces valid JSON with score rows."""
    r = subprocess.run(
        [
            sys.executable, str(SWEEP_SCRIPT),
            "--lanes", "work-strategy",
            "--observations", str(SEED_FIXTURE),
            "--budgets-file", str(REPO_ROOT / "config" / "context_budgets" / "lane-defaults.json"),
            "--json",
        ],
        capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    rows = json.loads(r.stdout)
    assert len(rows) == 3, "should have compact + medium + deep"
    for row in rows:
        assert "utilization" in row
        assert "coverage" in row
        assert "mean_included_rank" in row


def test_compute_benchmark_scores_unit() -> None:
    """Unit test for compute_benchmark_scores with synthetic pieces."""
    sys.path.insert(0, str(REPO_ROOT / "scripts" / "prepared_context"))
    sys.path.insert(0, str(REPO_ROOT / "scripts" / "runtime"))
    from build_budgeted_context import RankedPiece, compute_benchmark_scores

    included = [
        RankedPiece(sort_key=-2.0, label="a", kind="obs", text="x" * 500, meta={"rank": 2.0}),
        RankedPiece(sort_key=-1.0, label="b", kind="obs", text="x" * 300, meta={"rank": 1.0}),
    ]
    excluded = [
        RankedPiece(sort_key=-0.5, label="c", kind="obs", text="x" * 200, meta={"rank": 0.5}),
    ]
    scores = compute_benchmark_scores(included, excluded, budget=1000)
    assert scores["utilization"] == 0.8
    assert scores["coverage"] == round(2 / 3, 4)
    assert scores["mean_included_rank"] == 1.5
    assert scores["included_count"] == 2
    assert scores["excluded_count"] == 1
    assert scores["total_candidates"] == 3
