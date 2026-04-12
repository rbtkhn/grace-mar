"""Tests for scripts/prune_self_memory.py (no writes to real user dirs)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import prune_self_memory as ps  # noqa: E402


def test_split_horizons_roundtrip() -> None:
    text = """# H\n\n## Short-term\n\nA line\n\n## Medium-term\n\nB line\n\n## Long-term\n\nC line\n"""
    sp = ps._split_horizons(text)
    assert sp is not None
    preamble, sections = sp
    assert "Short" in preamble or preamble.startswith("#")
    assert [s[0] for s in sections] == ["short", "medium", "long"]
    rebuilt = ps._rebuild(preamble, sections)
    assert "A line" in rebuilt and "B line" in rebuilt


def test_prune_over_max(tmp_path: Path) -> None:
    user = tmp_path / "users" / "u1"
    user.mkdir(parents=True)
    big = "x" * 500 + "\n"
    mem = (
        "# M\n\n## Short-term\n"
        + big
        + "\n## Medium-term\n\nm\n\n## Long-term\n\nl\n"
    )
    (user / "self-memory.md").write_text(mem, encoding="utf-8")

    new_t, pruned, msg, hz = ps.run_prune(user, max_chars=400, target_chars=200)
    assert hz
    assert len(pruned) > 0
    assert len(new_t) <= 400
    assert "m" in new_t and "l" in new_t


def test_no_prune_under_max(tmp_path: Path) -> None:
    user = tmp_path / "users" / "u2"
    user.mkdir(parents=True)
    (user / "self-memory.md").write_text(
        "# M\n\n## Short-term\n\nok\n",
        encoding="utf-8",
    )
    new_t, pruned, _msg, _ = ps.run_prune(user, max_chars=9000, target_chars=8000)
    assert pruned == ""
    assert new_t == (user / "self-memory.md").read_text(encoding="utf-8")


def test_legacy_prune(tmp_path: Path) -> None:
    user = tmp_path / "users" / "u3"
    user.mkdir(parents=True)
    body = "y" * 600
    (user / "self-memory.md").write_text("# Title\n\n" + body, encoding="utf-8")
    new_t, pruned, msg, hz = ps.run_prune(user, max_chars=400, target_chars=200)
    assert not hz
    assert "legacy" in msg
    assert len(pruned) > 0
    assert len(new_t) < len("# Title\n\n" + body)
