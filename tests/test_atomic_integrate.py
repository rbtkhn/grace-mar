"""Tests for scripts/atomic_integrate.py (mocked merge subprocess, isolated paths)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from subprocess import CompletedProcess

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import atomic_integrate as ai  # noqa: E402


@pytest.fixture
def fake_repo(tmp_path: Path) -> tuple[Path, str]:
    r = tmp_path / "repo"
    (r / "bot").mkdir(parents=True)
    (r / "bot" / "prompt.py").write_text("# prompt\n", encoding="utf-8")
    uid = "testuser"
    ur = r / "users" / uid
    ur.mkdir(parents=True)
    for name in ("self.md", "self-archive.md", "recursion-gate.md", "session-log.md"):
        (ur / name).write_text(f"# {name}\n", encoding="utf-8")
    (r / "testuser-llm.txt").write_text("prp\n", encoding="utf-8")
    return r, uid


def test_dry_run_writes_receipt(monkeypatch: pytest.MonkeyPatch, fake_repo: tuple[Path, str]) -> None:
    r, uid = fake_repo
    monkeypatch.setattr(ai, "REPO_ROOT", r)
    monkeypatch.setattr(ai, "BOT_PROMPT", r / "bot" / "prompt.py")
    monkeypatch.setattr(ai, "profile_dir", lambda u: r / "users" / u)

    def _prp(u: str) -> Path:
        return r / f"{u}-llm.txt"

    monkeypatch.setattr(ai, "_prp_path", _prp)
    monkeypatch.setattr(ai, "_preflight", lambda *a, **k: None)

    code = ai.run(uid, "CANDIDATE-0001", "tester", apply=False, territory="all", skip_integrity=True)
    assert code == 0
    receipts = list((r / "users" / uid / "integration-receipts").glob("integration-receipt-*.json"))
    assert len(receipts) == 1
    data = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert data["dry_run"] is True
    assert data["success"] is True
    assert "process_approved_candidates.py" in " ".join(data["merge_command"])


def test_apply_success_backup_and_receipt(
    monkeypatch: pytest.MonkeyPatch, fake_repo: tuple[Path, str]
) -> None:
    r, uid = fake_repo

    monkeypatch.setattr(ai, "REPO_ROOT", r)
    monkeypatch.setattr(ai, "BOT_PROMPT", r / "bot" / "prompt.py")
    monkeypatch.setattr(ai, "profile_dir", lambda u: r / "users" / u)

    def _prp(u: str) -> Path:
        return r / f"{u}-llm.txt"

    monkeypatch.setattr(ai, "_prp_path", _prp)
    monkeypatch.setattr(ai, "_preflight", lambda *a, **k: None)

    def runner(cmd: list[str], **kwargs: object) -> CompletedProcess[str]:
        return CompletedProcess(cmd, 0, stdout="merge ok\n", stderr="")

    code = ai.run(
        uid,
        "CANDIDATE-0001",
        "tester",
        apply=True,
        territory="all",
        skip_integrity=True,
        merge_runner=runner,
    )
    assert code == 0
    backups = list((r / "users" / uid / ".integration-backups").glob("*"))
    assert len(backups) == 1
    assert (backups[0] / "users" / uid / "self.md").is_file()
    receipts = list((r / "users" / uid / "integration-receipts").glob("*.json"))
    assert len(receipts) == 1
    data = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert data["success"] is True
    assert data["merge_returncode"] == 0
    assert data["dry_run"] is False


def test_apply_merge_failure(monkeypatch: pytest.MonkeyPatch, fake_repo: tuple[Path, str]) -> None:
    r, uid = fake_repo
    monkeypatch.setattr(ai, "REPO_ROOT", r)
    monkeypatch.setattr(ai, "BOT_PROMPT", r / "bot" / "prompt.py")
    monkeypatch.setattr(ai, "profile_dir", lambda u: r / "users" / u)

    def _prp(u: str) -> Path:
        return r / f"{u}-llm.txt"

    monkeypatch.setattr(ai, "_prp_path", _prp)
    monkeypatch.setattr(ai, "_preflight", lambda *a, **k: None)

    def runner(cmd: list[str], **kwargs: object) -> CompletedProcess[str]:
        return CompletedProcess(cmd, 1, stdout="", stderr="merge failed")

    code = ai.run(
        uid,
        "CANDIDATE-0001",
        "tester",
        apply=True,
        territory="all",
        skip_integrity=True,
        merge_runner=runner,
    )
    assert code == 1
    receipts = list((r / "users" / uid / "integration-receipts").glob("*.json"))
    assert len(receipts) == 1
    data = json.loads(receipts[0].read_text(encoding="utf-8"))
    assert data["success"] is False
    assert data["merge_returncode"] == 1
