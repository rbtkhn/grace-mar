"""Tests for the retrieval-miss ledger: logger, schema validation, summary."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_RUNTIME = REPO_ROOT / "scripts" / "runtime"


@pytest.fixture(autouse=True)
def _isolate_ledger(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Route ledger writes to tmp_path so tests never touch the real runtime dir."""
    monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))


def _run_logger(*extra_args: str) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(SCRIPTS_RUNTIME / "log_retrieval_miss.py"),
        *extra_args,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def _run_summary(*extra_args: str) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        str(SCRIPTS_RUNTIME / "summarize_retrieval_misses.py"),
        *extra_args,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def _ledger_path(tmp_path: Path) -> Path:
    return tmp_path / "runtime" / "retrieval-misses" / "index.jsonl"


# --- Logger tests ---


class TestLogRetrievalMiss:
    def test_valid_record_created(self, tmp_path: Path) -> None:
        result = _run_logger(
            "--surface", "prepared_context",
            "--query", "Jiang lecture on sovereignty",
            "--failure-class", "vocabulary_mismatch",
            "--notes", "Query used sovereignty; indexed under zhuquan",
            "--lane", "work-jiang",
            "--recorded-by", "operator",
        )
        assert result.returncode == 0, result.stderr
        assert "logged rmiss_" in result.stdout

        ledger = _ledger_path(tmp_path)
        assert ledger.exists()
        rec = json.loads(ledger.read_text(encoding="utf-8").strip())
        assert rec["miss_id"].startswith("rmiss_")
        assert rec["retrieval_surface"] == "prepared_context"
        assert rec["query"] == "Jiang lecture on sovereignty"
        assert rec["failure_class"] == "vocabulary_mismatch"
        assert rec["lane_or_context"] == "work-jiang"
        assert rec["recorded_by"] == "operator"

    def test_minimal_required_fields(self, tmp_path: Path) -> None:
        result = _run_logger(
            "--surface", "evidence_lookup",
            "--query", "Barnes framing",
            "--failure-class", "unknown",
        )
        assert result.returncode == 0, result.stderr
        ledger = _ledger_path(tmp_path)
        rec = json.loads(ledger.read_text(encoding="utf-8").strip())
        assert rec["expected_target"] is None
        assert rec["notes"] is None
        assert rec["related_paths"] == []
        assert rec["lane_or_context"] is None
        assert rec["recorded_by"] is None

    def test_invalid_surface_rejected(self) -> None:
        result = _run_logger(
            "--surface", "invalid_surface",
            "--query", "anything",
            "--failure-class", "unknown",
        )
        assert result.returncode != 0
        assert "invalid surface" in result.stderr.lower()

    def test_invalid_failure_class_rejected(self) -> None:
        result = _run_logger(
            "--surface", "prepared_context",
            "--query", "anything",
            "--failure-class", "wrong_class",
        )
        assert result.returncode != 0
        assert "invalid failure_class" in result.stderr.lower()

    def test_validate_only_does_not_write(self, tmp_path: Path) -> None:
        result = _run_logger(
            "--surface", "notebook_lookup",
            "--query", "test query",
            "--failure-class", "scope_mismatch",
            "--validate-only",
        )
        assert result.returncode == 0
        payload = json.loads(result.stdout)
        assert payload["retrieval_surface"] == "notebook_lookup"
        assert not _ledger_path(tmp_path).exists()

    def test_related_paths_captured(self, tmp_path: Path) -> None:
        result = _run_logger(
            "--surface", "artifact_lookup",
            "--query", "skill card for work-strategy",
            "--failure-class", "missing_content",
            "--related-path", "artifacts/skill-cards/",
            "--related-path", "docs/skill-work/work-strategy/",
        )
        assert result.returncode == 0
        ledger = _ledger_path(tmp_path)
        rec = json.loads(ledger.read_text(encoding="utf-8").strip())
        assert len(rec["related_paths"]) == 2

    def test_multiple_records_appended(self, tmp_path: Path) -> None:
        for surface in ("prepared_context", "evidence_lookup", "artifact_lookup"):
            result = _run_logger(
                "--surface", surface,
                "--query", f"test {surface}",
                "--failure-class", "unknown",
            )
            assert result.returncode == 0

        ledger = _ledger_path(tmp_path)
        lines = [l for l in ledger.read_text(encoding="utf-8").splitlines() if l.strip()]
        assert len(lines) == 3


# --- Summary tests ---


class TestSummarizeRetrievalMisses:
    def _seed_ledger(self, tmp_path: Path, records: list[dict]) -> None:
        ledger = _ledger_path(tmp_path)
        ledger.parent.mkdir(parents=True, exist_ok=True)
        with ledger.open("w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec) + "\n")

    def test_empty_ledger_no_error(self) -> None:
        result = _run_summary()
        assert result.returncode == 0

    def test_counts_by_class_and_surface(self, tmp_path: Path) -> None:
        self._seed_ledger(tmp_path, [
            {"miss_id": "rmiss_20260414T100000Z_aabbccdd", "timestamp": "2026-04-14T10:00:00Z",
             "retrieval_surface": "prepared_context", "query": "q1", "failure_class": "vocabulary_mismatch"},
            {"miss_id": "rmiss_20260414T100100Z_11223344", "timestamp": "2026-04-14T10:01:00Z",
             "retrieval_surface": "prepared_context", "query": "q2", "failure_class": "vocabulary_mismatch"},
            {"miss_id": "rmiss_20260414T100200Z_55667788", "timestamp": "2026-04-14T10:02:00Z",
             "retrieval_surface": "notebook_lookup", "query": "q3", "failure_class": "scope_mismatch"},
        ])
        result = _run_summary("--json")
        assert result.returncode == 0
        out = json.loads(result.stdout)
        assert out["total"] == 3
        assert out["by_failure_class"]["vocabulary_mismatch"] == 2
        assert out["by_failure_class"]["scope_mismatch"] == 1
        assert out["by_retrieval_surface"]["prepared_context"] == 2
        assert out["by_retrieval_surface"]["notebook_lookup"] == 1

    def test_since_filter(self, tmp_path: Path) -> None:
        self._seed_ledger(tmp_path, [
            {"miss_id": "rmiss_20260410T100000Z_aabbccdd", "timestamp": "2026-04-10T10:00:00Z",
             "retrieval_surface": "prepared_context", "query": "old", "failure_class": "unknown"},
            {"miss_id": "rmiss_20260414T100000Z_11223344", "timestamp": "2026-04-14T10:00:00Z",
             "retrieval_surface": "evidence_lookup", "query": "new", "failure_class": "missing_content"},
        ])
        result = _run_summary("--since", "2026-04-13", "--json")
        assert result.returncode == 0
        out = json.loads(result.stdout)
        assert out["total"] == 1
        assert out["by_failure_class"]["missing_content"] == 1
