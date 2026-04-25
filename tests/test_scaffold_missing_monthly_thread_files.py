"""Tests for scripts/scaffold_missing_monthly_thread_files.py."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from migrate_thread_md_to_monthly import THREAD_MARKER_END, THREAD_MARKER_START  # noqa: E402
from scaffold_missing_monthly_thread_files import (  # noqa: E402
    _strip_backfill_from_segment,
    scaffold_missing,
)


def test_strip_backfill_from_segment() -> None:
    a = "journal\n\n---\n\n<!-- backfill:ritter:start -->\nmore"
    assert "backfill" not in _strip_backfill_from_segment(a)
    assert "journal" in _strip_backfill_from_segment(a)


def test_scaffold_missing_writes_only_absent_months(tmp_path: Path) -> None:
    nb = tmp_path / "notebook"
    ed = nb / "experts" / "xfoo"
    ed.mkdir(parents=True)
    (ed / "xfoo-thread-2026-01.md").write_text(
        f"# t\n{THREAD_MARKER_START}\n\n{THREAD_MARKER_END}\n",
        encoding="utf-8",
    )
    (ed / "thread.md").write_text(
        "intro\n## 2026-02\n\nbody feb\n## 2026-03\n\nbody mar\n",
        encoding="utf-8",
    )
    out = scaffold_missing(nb, "xfoo", apply=True)
    assert any("2026-02" in s for s in out)
    assert (ed / "xfoo-thread-2026-02.md").is_file()
    assert (ed / "xfoo-thread-2026-03.md").is_file()
    assert "2026-02" in (ed / "xfoo-thread-2026-02.md").read_text(encoding="utf-8")
    out2 = scaffold_missing(nb, "xfoo", apply=True)
    assert "nothing to scaffold" in " ".join(out2)


def test_scaffold_skips_without_monthly_layout(tmp_path: Path) -> None:
    nb = tmp_path / "notebook"
    nobody = nb / "experts" / "nobody"
    nobody.mkdir(parents=True)
    (nobody / "thread.md").write_text("## 2026-01\n\nx\n", encoding="utf-8")
    out = scaffold_missing(nb, "nobody", apply=True)
    assert any("no monthly layout" in s for s in out)
