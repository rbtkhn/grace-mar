"""Unit tests for scripts/validate_structured_files.py helpers."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from validate_structured_files import (
    iter_markdown_links,
    validate_json_file,
    validate_markdown_links,
)


def test_validate_json_file_ok(tmp_path: Path) -> None:
    p = tmp_path / "ok.json"
    p.write_text('{"a": 1}', encoding="utf-8")
    assert validate_json_file(p) is None


def test_validate_json_file_bad(tmp_path: Path) -> None:
    p = tmp_path / "bad.json"
    p.write_text("{not json", encoding="utf-8")
    err = validate_json_file(p)
    assert err is not None
    assert "JSON" in err


def test_iter_markdown_links_skips_fence(tmp_path: Path) -> None:
    p = tmp_path / "x.md"
    p.write_text(
        """See [in prose](exists.md).

```
[demo](ignored.md)
```

Tail [after](after.md).
""",
        encoding="utf-8",
    )
    targets = [t for _, t in iter_markdown_links(p)]
    assert "exists.md" in targets
    assert "ignored.md" not in targets
    assert "after.md" in targets


def test_validate_markdown_links_external_skipped(tmp_path: Path) -> None:
    base = tmp_path / "docs"
    base.mkdir()
    (base / "peer.md").write_text("ok\n", encoding="utf-8")
    md = base / "page.md"
    md.write_text(
        "[remote](https://example.com/foo) [local](./peer.md)",
        encoding="utf-8",
    )
    assert validate_markdown_links([md], repo_root=tmp_path) == []


def test_validate_markdown_links_anchor_strip(tmp_path: Path) -> None:
    md_dir = tmp_path / "d"
    md_dir.mkdir()
    target = md_dir / "target.md"
    target.write_text("# ok\n", encoding="utf-8")
    md = md_dir / "page.md"
    md.write_text("[x](target.md#sec)", encoding="utf-8")
    assert validate_markdown_links([md], repo_root=tmp_path) == []


def test_validate_markdown_links_missing(tmp_path: Path) -> None:
    md_dir = tmp_path / "d"
    md_dir.mkdir()
    md = md_dir / "page.md"
    md.write_text("[missing](./nowhere.md)", encoding="utf-8")
    errs = validate_markdown_links([md], repo_root=tmp_path)
    assert len(errs) >= 1
    assert any("nowhere.md" in e for e in errs)


def test_repo_validate_smoke() -> None:
    """Smoke: validator exits 0 on this repo tree."""
    root = Path(__file__).resolve().parent.parent
    proc = subprocess.run(
        [sys.executable, str(root / "scripts" / "validate_structured_files.py")],
        cwd=str(root),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
