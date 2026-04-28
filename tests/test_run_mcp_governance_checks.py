"""Safety and wiring tests for scripts/run_mcp_governance_checks.py."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _scripts_on_path() -> None:
    p = str(REPO_ROOT / "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)


def test_report_path_under_artifacts() -> None:
    import run_mcp_governance_checks as r

    assert str(r.REPORT_PATH).replace("\\", "/").startswith(
        str(REPO_ROOT / "artifacts").replace("\\", "/")
    )
    assert r.REPORT_PATH.name == "mcp-governance-demo-report.md"


def test_subprocess_uses_shell_false_only() -> None:
    src = (REPO_ROOT / "scripts" / "run_mcp_governance_checks.py").read_text(encoding="utf-8")
    assert "shell=False" in src
    assert "shell=True" not in src


def test_operator_record_path_not_embedded_in_script() -> None:
    """Avoid hardcoding instance paths; orchestrator targets artifacts only."""
    src = (REPO_ROOT / "scripts" / "run_mcp_governance_checks.py").read_text(encoding="utf-8")
    assert "users/grace-mar" not in src


def test_no_http_urls_in_executable_logic() -> None:
    """Orchestrator must not treat URLs as invocation targets."""
    src = (REPO_ROOT / "scripts" / "run_mcp_governance_checks.py").read_text(encoding="utf-8")
    assert "http://" not in src and "https://" not in src


def test_main_with_stubbed_subprocess(monkeypatch: pytest.MonkeyPatch) -> None:
    import run_mcp_governance_checks as r

    monkeypatch.setattr(sys, "argv", ["run_mcp_governance_checks.py"])

    def fake_run(
        cmd: list[str],
        cwd: str | None = None,
        shell: bool = False,
        capture_output: bool = False,
        text: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        assert shell is False
        return subprocess.CompletedProcess(
            cmd,
            0,
            stdout="artifacts/mcp-receipts/fake-receipt.json\n",
            stderr="",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert r.main() == 0
