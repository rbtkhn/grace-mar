"""Tests for scripts/gated_record_rules.py and PR checker wiring."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from gated_record_rules import allowed_gated_commit_message, is_gated_record_path


@pytest.mark.parametrize(
    "rel,expected",
    [
        ("users/grace-mar/self.md", True),
        ("users/grace-mar/self-archive.md", True),
        ("users/grace-mar/merge-receipts.jsonl", True),
        ("users/grace-mar/grace-mar-llm.txt", True),
        ("bot/prompt.py", True),
        ("grace-mar-llm.txt", True),
        ("docs/foo.md", False),
        ("users/grace-mar/self-memory.md", False),
        ("users/grace-mar/recursion-gate.md", False),
    ],
)
def test_is_gated_record_path(rel: str, expected: bool) -> None:
    assert is_gated_record_path(rel) is expected


@pytest.mark.parametrize(
    "msg,ok",
    [
        ("feat: [gated-merge] apply candidate", True),
        ("run process_approved_candidates.py --apply", True),
        ("MERGE-RECEIPT: abc", True),
        ("SNAPSHOT: daily", True),
        ("chore: tweak self.md by hand", False),
    ],
)
def test_allowed_gated_commit_message(msg: str, ok: bool) -> None:
    assert allowed_gated_commit_message(msg) is ok


def test_check_gated_record_pr_passes_clean_range(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "t@e.st"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=tmp_path,
        check=True,
    )
    (tmp_path / "a.txt").write_text("1\n")
    subprocess.run(["git", "add", "a.txt"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    (tmp_path / "b.txt").write_text("2\n")
    subprocess.run(["git", "add", "b.txt"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "second"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    env = {**os.environ, "PYTHONPATH": str(SCRIPTS)}
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "check_gated_record_pr.py"),
            "--repo",
            str(tmp_path),
            "--base",
            base,
            "--head",
            head,
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stderr


def test_check_gated_record_pr_fails_without_token(tmp_path: Path) -> None:
    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "t@e.st"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=tmp_path,
        check=True,
    )
    (tmp_path / "README.md").write_text("# t\n")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    base = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    u = tmp_path / "users" / "x"
    u.mkdir(parents=True)
    (u / "self.md").write_text("# x\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-m", "bad: edit self without token"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()

    env = {**os.environ, "PYTHONPATH": str(SCRIPTS)}
    r = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "check_gated_record_pr.py"),
            "--repo",
            str(tmp_path),
            "--base",
            base,
            "--head",
            head,
        ],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 1, r.stdout
