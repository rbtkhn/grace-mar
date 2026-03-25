"""Tests for continuity receipt preflight and verification."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from continuity_preflight import build_receipt, write_receipt  # noqa: E402
from verify_continuity_receipt import verify_receipt_file  # noqa: E402


def test_build_receipt_hashes_user_files(tmp_path: Path) -> None:
    ud = tmp_path / "users" / "u1"
    ud.mkdir(parents=True)
    for name in ("session-log.md", "recursion-gate.md", "self-evidence.md"):
        (ud / name).write_text(f"content-{name}\n", encoding="utf-8")
    receipt, errs = build_receipt(
        user_id="u1",
        runtime="openclaw",
        session_id="s1",
        repo_root=tmp_path,
    )
    assert not errs
    assert receipt["version"] == 1
    assert len(receipt["required_paths"]) == 3


def test_verify_receipt_ttl_expired(tmp_path: Path) -> None:
    import hashlib

    ud = tmp_path / "users" / "u"
    ud.mkdir(parents=True)
    (ud / "a.md").write_text("stable", encoding="utf-8")
    h = hashlib.sha256((ud / "a.md").read_bytes()).hexdigest()
    old = (datetime.now(timezone.utc) - timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%SZ")
    rdir = tmp_path / "r"
    rdir.mkdir()
    p = rdir / "rcpt.json"
    p.write_text(
        json.dumps(
            {
                "version": 1,
                "session_id": "s",
                "user_id": "u",
                "runtime": "openclaw",
                "created_at": old,
                "required_paths": [{"path": "users/u/a.md", "sha256": h}],
                "reader": {"tool": "t", "version": "1"},
            }
        ),
        encoding="utf-8",
    )
    ok, msg = verify_receipt_file(p, repo_root=tmp_path, ttl_hours=8)
    assert not ok
    assert "expired" in msg.lower()


def test_verify_receipt_hash_mismatch(tmp_path: Path) -> None:
    ud = tmp_path / "users" / "u1"
    ud.mkdir(parents=True)
    (ud / "session-log.md").write_text("hello", encoding="utf-8")
    receipt, _ = build_receipt(
        user_id="u1",
        runtime="openclaw",
        session_id="s1",
        repo_root=tmp_path,
    )
    out = tmp_path / "out.json"
    write_receipt(receipt, out_path=out, repo_root=tmp_path)
    (ud / "session-log.md").write_text("changed", encoding="utf-8")
    ok, msg = verify_receipt_file(out, repo_root=tmp_path, ttl_hours=24)
    assert not ok
    assert "mismatch" in msg.lower()


def test_verify_receipt_ok(tmp_path: Path) -> None:
    ud = tmp_path / "users" / "u1"
    ud.mkdir(parents=True)
    for name in ("session-log.md", "recursion-gate.md", "self-evidence.md"):
        (ud / name).write_text(f"x-{name}", encoding="utf-8")
    receipt, _ = build_receipt(
        user_id="u1",
        runtime="openclaw",
        session_id="s1",
        repo_root=tmp_path,
    )
    out = tmp_path / "out.json"
    write_receipt(receipt, out_path=out, repo_root=tmp_path)
    ok, msg = verify_receipt_file(out, repo_root=tmp_path, ttl_hours=24)
    assert ok, msg
