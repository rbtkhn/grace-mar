"""Ritter refined pages: manifest + optional page-shape checks."""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def _load_verifier():
    path = REPO / "scripts/strategy/verify_ritter_refined_pages.py"
    spec = importlib.util.spec_from_file_location("verify_ritter_refined_pages", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_verify_ritter_refined_pages_exits_zero() -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts/strategy/verify_ritter_refined_pages.py")],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_verify_mearsheimer_refined_pages_exits_zero() -> None:
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO / "scripts/strategy/verify_ritter_refined_pages.py"),
            "--expert",
            "mearsheimer",
        ],
        cwd=str(REPO),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr


def test_verify_page_content_minimal_passes() -> None:
    mod = _load_verifier()
    ch = " ".join(f"w{i}" for i in range(20))
    tail = (
        "### Reflection\n\na b\n\n### Foresight\n\nc d\n\n---\n\n### Appendix\n\n- e\n"
    )
    core = f"# T\n\n---\n\n### Verbatim\n\n{ch}\n\n{tail}"
    n = len(re.findall(r"\S+", core))
    md = f"# T\n\n**Words:** {n}\n\n---\n\n### Verbatim\n\n{ch}\n\n{tail}"
    errs, warns = mod.verify_page_content("fixture.md", md)
    assert not errs
    assert not warns


def test_verify_page_content_missing_verbatim_fails() -> None:
    mod = _load_verifier()
    md = (
        "**Words:** 4\n\n---\n\n### Reflection\n\na\n\n### Foresight\n\nb\n\n---\n\n"
        "### Appendix\n\nc\n"
    )
    errs, _ = mod.verify_page_content("bad.md", md)
    assert any("Verbatim" in e for e in errs)


def test_verify_page_content_digest_without_words_passes() -> None:
    mod = _load_verifier()
    md = (
        "# T\n\n---\n\n### Verbatim\n\n"
        "one two three four five.\n\n"
        "### Reflection\n\nsix seven.\n\n### Foresight\n\n- eight\n\n---\n\n"
        "### Appendix\n\n- nine\n"
    )
    errs, warns = mod.verify_page_content("digest.md", md)
    assert not errs
    assert not warns


def test_verify_page_long_file_no_soft_cap_warning() -> None:
    mod = _load_verifier()
    long_ch = "word " * 3200
    tail = (
        "### Reflection\n\nkeep short.\n\n### Foresight\n\n- x\n\n---\n\n### Appendix\n\n- y\n"
    )
    core = f"# T\n\n---\n\n### Verbatim\n\n{long_ch}\n\n{tail}"
    n = len(re.findall(r"\S+", core))
    md = f"# T\n\n**Words:** {n}\n\n---\n\n### Verbatim\n\n{long_ch}\n\n{tail}"
    errs, warns = mod.verify_page_content("long.md", md)
    assert not errs
    assert not any("soft cap" in w.lower() for w in warns)
