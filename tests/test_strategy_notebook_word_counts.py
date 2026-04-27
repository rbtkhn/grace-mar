"""Tests for ``scripts/strategy/update_strategy_notebook_word_counts.py``."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
MOD = "scripts.strategy.update_strategy_notebook_word_counts"
WC = __import__(MOD, fromlist=["*"])


def test_count_excludes_front_matter() -> None:
    text = "---\ntitle: x\nword_count: 9\n---\n\n# Hello\n\nWorld test.\n"
    sp = WC._split_front_matter(text)
    assert sp is not None
    _i, body = sp
    n = WC.count_words_in_body(body)
    assert n == 4


def test_count_excludes_fenced_code() -> None:
    body = "Intro words.\n\n```\nnot counted here many tokens\n```\n\nOutro more.\n"
    n = WC.count_words_in_body(body)
    assert n == 4


def test_count_excludes_html_comments() -> None:
    body = "one two <!-- three four --> five\n"
    n = WC.count_words_in_body(body)
    assert n == 3


def test_count_replaces_link_with_visible_text() -> None:
    body = "See [the label](https://example.com/ignore) now.\n"
    n = WC.count_words_in_body(body)
    assert n == 4  # See the label now.


def test_count_excludes_table_dividers() -> None:
    body = "hello\n\n| --- | --- |\n\nworld\n"
    n = WC.count_words_in_body(body)
    assert n == 2


def test_yaml_insert_word_count() -> None:
    src = (
        "---\n"
        "title: T\n"
        "kind: note\n"
        "status: ok\n"
        "---\n\n"
        "# Body\n\n"
        "One two three.\n"
    )
    out = WC.build_updated_content(src)
    assert "word_count: 5" in out
    assert out.startswith("---\n")
    sp = WC._split_front_matter(out)
    assert sp is not None
    i, b = sp
    assert "word_count: 5" in i
    n2 = WC.build_updated_content(out)
    assert n2 == out


def test_yaml_update_stale() -> None:
    src = (
        "---\n"
        "title: T\n"
        "word_count: 0\n"
        "---\n\n# H\n\nalpha beta gamma delta.\n"
    )
    out = WC.build_updated_content(src)
    assert "word_count: 6" in out
    sp = WC._split_front_matter(out)
    assert sp is not None
    i, _ = sp
    assert "word_count: 6" in i
    assert "word_count: 0" not in i


def test_html_comment_after_h1() -> None:
    src = "# Title here\n\nParagraph one two.\n"
    out = WC.build_updated_content(src)
    assert out.startswith("# Title here\n")
    assert "<!-- word_count:" in out
    assert "word_count: 6" in out


def test_html_update_managed_line() -> None:
    src = (
        "# H\n"
        "<!-- word_count: 1 -->\n\n"
        "foo bar baz qux\n"
    )
    out = WC.build_updated_content(src)
    m = WC.RE_MANAGED_WC.search(out)
    assert m
    assert m.group(1) == "6"


def test_idempotent_second_run() -> None:
    src = "# Only\n\ntext here.\n"
    once = WC.build_updated_content(src)
    twice = WC.build_updated_content(once)
    assert once == twice
    assert "<!-- word_count:" in once


def test_is_eligible_skips_dated_raw_input() -> None:
    assert not WC._is_eligible_path(Path("raw-input/2026-01-19/capture.md"))
    assert not WC._is_eligible_path(Path("raw-input/_aired-pending/x.md"))
    assert WC._is_eligible_path(Path("raw-input/README.md"))
    assert WC._is_eligible_path(Path("chapters/2026-01/days.md"))


def test_check_fails_then_passes_after_update(tmp_path: Path) -> None:
    nb = tmp_path / "notebook"
    nb.mkdir()
    f = nb / "a.md"
    f.write_text("# H\n\none two\n", encoding="utf-8")
    stale = subprocess.run(
        [sys.executable, str(REPO / "scripts/strategy/update_strategy_notebook_word_counts.py"), "--check", "--root", str(nb)],
        capture_output=True,
        text=True,
    )
    assert stale.returncode == 1
    subprocess.run(
        [sys.executable, str(REPO / "scripts/strategy/update_strategy_notebook_word_counts.py"), "--root", str(nb)],
        check=True,
    )
    ok = subprocess.run(
        [sys.executable, str(REPO / "scripts/strategy/update_strategy_notebook_word_counts.py"), "--root", str(nb), "--check"],
        capture_output=True,
        text=True,
    )
    assert ok.returncode == 0


def test_dry_run_no_write(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    nb = tmp_path / "nb"
    nb.mkdir()
    p = nb / "x.md"
    p.write_text("# T\n\nhello\n", encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(REPO / "scripts/strategy/update_strategy_notebook_word_counts.py"), "--root", str(nb), "--dry-run"],
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0
    t = p.read_text(encoding="utf-8")
    assert "word_count" not in t
