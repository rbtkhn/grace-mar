"""Sandbox adapter — governance loop, authority checks, DryRunBackend."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
WD = REPO_ROOT / "scripts" / "work_dev"
for p in (SCRIPTS, WD):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from work_dev.sandbox_adapter import (
    DryRunBackend,
    SandboxRequest,
    SandboxResult,
    check_authority,
    execute,
)


# ── Authority checks ───────────────────────────────────────────────────


class TestAuthority:
    def test_operator_read_write_allowed(self) -> None:
        req = SandboxRequest(command="ls", authority_class="operator", record_access="read_write")
        assert check_authority(req) is None

    def test_agent_supervised_read_only_allowed(self) -> None:
        req = SandboxRequest(command="ls", authority_class="agent_supervised", record_access="read_only")
        assert check_authority(req) is None

    def test_agent_supervised_read_write_denied(self) -> None:
        req = SandboxRequest(command="ls", authority_class="agent_supervised", record_access="read_write")
        err = check_authority(req)
        assert err is not None
        assert "read_write" in err

    def test_agent_autonomous_none_allowed(self) -> None:
        req = SandboxRequest(command="ls", authority_class="agent_autonomous", record_access="none")
        assert check_authority(req) is None

    def test_agent_autonomous_read_only_denied(self) -> None:
        req = SandboxRequest(command="ls", authority_class="agent_autonomous", record_access="read_only")
        err = check_authority(req)
        assert err is not None
        assert "agent_autonomous" in err

    def test_unknown_authority_class(self) -> None:
        req = SandboxRequest(command="ls", authority_class="root", record_access="none")
        err = check_authority(req)
        assert err is not None
        assert "unknown authority_class" in err

    def test_unknown_record_access(self) -> None:
        req = SandboxRequest(command="ls", authority_class="operator", record_access="full")
        err = check_authority(req)
        assert err is not None
        assert "unknown record_access" in err


# ── DryRunBackend ──────────────────────────────────────────────────────


class TestDryRunBackend:
    def test_execute_returns_mock(self) -> None:
        b = DryRunBackend()
        result = b.execute("echo hello", [], 0, {})
        assert result["exit_code"] == 0
        assert "echo hello" in result["stdout"]

    def test_health(self) -> None:
        b = DryRunBackend()
        h = b.health()
        assert h["ok"] is True


# ── Adapter execute ────────────────────────────────────────────────────


class TestExecute:
    def test_dry_run_success(self, tmp_path: Path) -> None:
        req = SandboxRequest(command="echo hi", backend="dry_run", task_id="T1", task_type="test")
        result = execute("test-user", req, emit_receipts=False)
        assert result.success
        assert result.exit_code == 0
        assert "echo hi" in result.stdout

    def test_authority_denied_returns_error(self) -> None:
        req = SandboxRequest(
            command="rm -rf /",
            authority_class="agent_autonomous",
            record_access="read_write",
        )
        result = execute("test-user", req, emit_receipts=False)
        assert not result.success
        assert "authority_denied" in result.error

    def test_unknown_backend_returns_error(self) -> None:
        req = SandboxRequest(command="ls", backend="nonexistent")
        result = execute("test-user", req, emit_receipts=False)
        assert not result.success
        assert "unknown_backend" in result.error

    def test_not_implemented_backend_returns_error(self) -> None:
        req = SandboxRequest(command="ls", backend="docker")
        result = execute("test-user", req, emit_receipts=False)
        assert not result.success
        assert "not_implemented" in result.error

    def test_receipts_emitted(self, tmp_path: Path) -> None:
        events_dir = tmp_path / "users" / "u1"
        events_dir.mkdir(parents=True)
        (events_dir / "pipeline-events.jsonl").write_text("", encoding="utf-8")
        (events_dir / "compute-ledger.jsonl").write_text("", encoding="utf-8")

        import work_dev.sandbox_adapter as sa
        import emit_pipeline_event as epe
        import emit_compute_ledger as ecl

        orig_repo_epe = epe.REPO_ROOT
        orig_repo_ecl = ecl.REPO_ROOT
        orig_repo_sa = sa.REPO_ROOT
        epe.REPO_ROOT = tmp_path
        ecl.REPO_ROOT = tmp_path
        sa.REPO_ROOT = tmp_path
        try:
            req = SandboxRequest(
                command="test", backend="dry_run",
                task_id="T-RECEIPT", task_type="receipt_test",
            )
            result = execute("u1", req, emit_receipts=True)
            assert result.success

            events = (events_dir / "pipeline-events.jsonl").read_text(encoding="utf-8").strip().splitlines()
            assert len(events) >= 2
            pre = json.loads(events[-2])
            post = json.loads(events[-1])
            assert pre["event"] == "sandbox_execution_pre"
            assert post["event"] == "sandbox_execution_post"
            assert pre["request_id"] == post["request_id"]
            assert post["task_id"] == "T-RECEIPT"

            ledger = (events_dir / "compute-ledger.jsonl").read_text(encoding="utf-8").strip().splitlines()
            assert len(ledger) >= 1
            row = json.loads(ledger[-1])
            assert row["operation"] == "sandbox_execution"
            assert row["task_id"] == "T-RECEIPT"
            assert row["outcome_confidence"] == 1.0
        finally:
            epe.REPO_ROOT = orig_repo_epe
            ecl.REPO_ROOT = orig_repo_ecl
            sa.REPO_ROOT = orig_repo_sa

    def test_result_dataclass_fields(self) -> None:
        req = SandboxRequest(command="x", backend="dry_run")
        result = execute("u", req, emit_receipts=False)
        assert result.request_id == req.request_id
        assert result.backend == "dry_run"
        assert isinstance(result.wall_ms, int)
