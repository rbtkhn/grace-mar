"""Tests for scripts/record_slice_loader.py."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from record_slice_loader import load_record_slices_for_lesson


def test_err_user_not_found() -> None:
    out = load_record_slices_for_lesson("nonexistent-fork-xyz", max_chars=1000)
    assert out["ok"] is False
    assert out["error"] == "ERR_USER_NOT_FOUND"


def test_tmp_user_truncation(tmp_path) -> None:
    ud = tmp_path / "u1"
    ud.mkdir()
    (ud / "self.md").write_text("x" * 5000, encoding="utf-8")
    (ud / "skill-think.md").write_text("y" * 2000, encoding="utf-8")
    (ud / "self-skills.md").write_text("z" * 1000, encoding="utf-8")

    # Patch profile_dir via monkeypatch on the module under test
    import record_slice_loader as rsl

    orig = rsl.profile_dir

    def fake_profile(uid: str):
        assert uid == "u1"
        return ud

    rsl.profile_dir = fake_profile
    try:
        out = load_record_slices_for_lesson("u1", max_chars=2000)
        assert out["ok"] is True
        total = sum(len(v) for v in out["slices"].values())
        assert total <= 2100  # small slack for truncation suffix
    finally:
        rsl.profile_dir = orig
