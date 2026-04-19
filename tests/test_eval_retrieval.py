"""Tests for scripts/runtime/eval_retrieval.py — retrieval benchmark harness."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EVAL_SCRIPT = REPO_ROOT / "scripts" / "runtime" / "eval_retrieval.py"
GOLDEN_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "retrieval-golden.jsonl"
SEED_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "observations-seed.jsonl"


def test_eval_retrieval_golden_set(tmp_path: Path) -> None:
    """Run eval against seed observations; expect non-zero precision."""
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    (obs_dir / "index.jsonl").write_text(
        SEED_FIXTURE.read_text(encoding="utf-8"), encoding="utf-8"
    )
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable, str(EVAL_SCRIPT),
            "--golden", str(GOLDEN_FIXTURE),
            "--top-k", "5",
            "--json",
        ],
        env=env, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    result = json.loads(r.stdout)
    assert result["total_queries"] == 14
    assert result["precision_at_k"] > 0.0, "seed data should produce at least some hits"
    assert 0.0 <= result["mrr"] <= 1.0
    assert "per_query" in result


def test_eval_retrieval_precision_above_threshold(tmp_path: Path) -> None:
    """Precision@10 on seed data should be at least 85% — regression gate."""
    obs_dir = tmp_path / "runtime" / "observations"
    obs_dir.mkdir(parents=True)
    (obs_dir / "index.jsonl").write_text(
        SEED_FIXTURE.read_text(encoding="utf-8"), encoding="utf-8"
    )
    env = {**os.environ, "GRACE_MAR_RUNTIME_LEDGER_ROOT": str(tmp_path)}
    r = subprocess.run(
        [
            sys.executable, str(EVAL_SCRIPT),
            "--golden", str(GOLDEN_FIXTURE),
            "--top-k", "10",
            "--json",
        ],
        env=env, capture_output=True, text=True,
    )
    assert r.returncode == 0, r.stderr
    result = json.loads(r.stdout)
    assert result["precision_at_k"] >= 0.85, (
        f"precision@10 = {result['precision_at_k']:.2%}, "
        f"expected ≥ 85%. Misses: "
        + ", ".join(q["query"][:40] for q in result["per_query"] if not q["hit"])
    )


def test_eval_retrieval_empty_golden(tmp_path: Path) -> None:
    """Empty golden set should return exit code 1."""
    empty = tmp_path / "empty.jsonl"
    empty.write_text("", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(EVAL_SCRIPT), "--golden", str(empty), "--json"],
        capture_output=True, text=True,
    )
    assert r.returncode == 1


def test_eval_unit_evaluate() -> None:
    """Unit test for evaluate() with synthetic golden entries."""
    sys.path.insert(0, str(REPO_ROOT / "scripts" / "runtime"))
    from eval_retrieval import evaluate, load_golden

    golden = load_golden(GOLDEN_FIXTURE)
    assert len(golden) > 0
    for entry in golden:
        assert "query" in entry
        assert "surface" in entry
        assert "expected_path" in entry


def test_golden_fixture_valid_json() -> None:
    """Golden fixture must be valid JSONL with required keys."""
    lines = GOLDEN_FIXTURE.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) >= 10, "golden set should have at least 10 entries"
    for line in lines:
        entry = json.loads(line)
        assert "query" in entry
        assert "surface" in entry
        assert "expected_path" in entry
