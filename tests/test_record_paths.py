"""Canonical Record path helpers (repo_io)."""

import os
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from repo_io import (  # noqa: E402
    CANONICAL_EVIDENCE_BASENAME,
    CANONICAL_RECORD_FILES_REQUIRED,
    assert_canonical_record_layout,
    missing_canonical_record_files,
    profile_dir,
)


def test_constants_match_documented_triple():
    assert CANONICAL_RECORD_FILES_REQUIRED == (
        "self.md",
        CANONICAL_EVIDENCE_BASENAME,
        "recursion-gate.md",
    )


def test_grace_mar_instance_has_required_files():
    mid = missing_canonical_record_files("grace-mar")
    assert mid == [], f"missing: {mid}"


def test_assert_passes_for_grace_mar():
    assert_canonical_record_layout("grace-mar", context="test")


def test_assert_skipped_when_env_set(monkeypatch):
    monkeypatch.setenv("GRACE_MAR_SKIP_PATH_CHECK", "1")
    # fake user with no dir — should not raise
    assert_canonical_record_layout("nonexistent-user-xyz-12345", context="test")


def test_assert_raises_for_missing_user_dir(monkeypatch):
    monkeypatch.delenv("GRACE_MAR_SKIP_PATH_CHECK", raising=False)
    with pytest.raises(RuntimeError, match="canonical Record files missing"):
        assert_canonical_record_layout("__no_such_fork_dir__", context="test")


def test_assert_raises_when_required_file_missing(monkeypatch, tmp_path):
    monkeypatch.delenv("GRACE_MAR_SKIP_PATH_CHECK", raising=False)
    fake_users = tmp_path / "users"
    fake_users.mkdir()
    (fake_users / "tmpfork").mkdir()
    (fake_users / "tmpfork" / "self.md").write_text("x", encoding="utf-8")
    (fake_users / "tmpfork" / CANONICAL_EVIDENCE_BASENAME).write_text("x", encoding="utf-8")
    # recursion-gate.md missing

    import repo_io as ri

    monkeypatch.setattr(ri, "USERS_DIR", fake_users)
    monkeypatch.setattr(ri, "REPO_ROOT", tmp_path)

    def _pd(uid: str) -> Path:
        return fake_users / uid

    monkeypatch.setattr(ri, "profile_dir", _pd)

    with pytest.raises(RuntimeError, match="recursion-gate"):
        ri.assert_canonical_record_layout("tmpfork")
