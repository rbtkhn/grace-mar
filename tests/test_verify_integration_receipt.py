"""Tests for scripts/verify_integration_receipt.py."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import verify_integration_receipt as vir  # noqa: E402


def _sha(s: str) -> str:
    return vir.sha256_text(s)


def test_verify_worktree_match(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "users" / "u").mkdir(parents=True)
    f = repo / "users" / "u" / "self.md"
    content = "# hello\n"
    f.write_text(content, encoding="utf-8")
    rel = "users/u/self.md"
    receipt = {"after_hashes": {rel: _sha(content)}}
    rpath = repo / "receipt.json"
    rpath.write_text(json.dumps(receipt), encoding="utf-8")

    import sys as _sys

    old = _sys.argv
    try:
        _sys.argv = [
            "verify_integration_receipt.py",
            "--receipt",
            str(rpath),
            "--repo-root",
            str(repo),
        ]
        assert vir.main() == 0
    finally:
        _sys.argv = old


def test_verify_mismatch(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    (repo / "users" / "u").mkdir(parents=True)
    f = repo / "users" / "u" / "self.md"
    f.write_text("# a\n", encoding="utf-8")
    receipt = {"after_hashes": {"users/u/self.md": _sha("# b\n")}}
    rpath = repo / "receipt.json"
    rpath.write_text(json.dumps(receipt), encoding="utf-8")

    import sys as _sys

    old = _sys.argv
    try:
        _sys.argv = [
            "verify_integration_receipt.py",
            "--receipt",
            str(rpath),
            "--repo-root",
            str(repo),
        ]
        assert vir.main() == 1
    finally:
        _sys.argv = old


def test_verify_empty_after_hashes_exit_2(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    rpath = repo / "receipt.json"
    repo.mkdir(parents=True)
    rpath.write_text(json.dumps({"after_hashes": {}}), encoding="utf-8")

    import sys as _sys

    old = _sys.argv
    try:
        _sys.argv = [
            "verify_integration_receipt.py",
            "--receipt",
            str(rpath),
            "--repo-root",
            str(repo),
        ]
        assert vir.main() == 2
    finally:
        _sys.argv = old


def test_verify_hashes_helper_match(tmp_path: Path) -> None:
    p = tmp_path / "a" / "b.txt"
    p.parent.mkdir(parents=True)
    p.write_text("x", encoding="utf-8")
    ok, lines = vir.verify_hashes(
        {"a/b.txt": vir.sha256_text("x")},
        repo_root=tmp_path,
        git_ref=None,
    )
    assert ok
    assert "OK" in lines[0]
