"""Tests for scripts/validate_operator_shell_manifest.py."""

from __future__ import annotations

import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _write_manifest(root: Path, content: str) -> None:
    cfg = root / "config"
    cfg.mkdir(parents=True, exist_ok=True)
    (cfg / "operator_shell_manifest.yaml").write_text(content, encoding="utf-8")


def test_validate_ok_minimal(tmp_path: Path) -> None:
    from validate_operator_shell_manifest import validate_operator_shell_manifest

    (tmp_path / "artifacts").mkdir(parents=True)
    (tmp_path / "artifacts" / "x.md").write_text("# x\n", encoding="utf-8")
    _write_manifest(
        tmp_path,
        textwrap.dedent(
            """\
            schema_version: "1.0.0"
            entries:
              - id: one
                title: One
                path: artifacts/x.md
            """
        ),
    )
    errs, warns = validate_operator_shell_manifest(tmp_path, require_files=True)
    assert not errs
    assert not warns


def test_validate_rejects_dotdot(tmp_path: Path) -> None:
    from validate_operator_shell_manifest import validate_operator_shell_manifest

    (tmp_path / "artifacts").mkdir(parents=True)
    (tmp_path / "artifacts" / "secret.md").write_text("x", encoding="utf-8")
    _write_manifest(
        tmp_path,
        textwrap.dedent(
            """\
            schema_version: "1.0.0"
            entries:
              - id: bad
                title: Bad
                path: artifacts/../artifacts/secret.md
            """
        ),
    )
    errs, _ = validate_operator_shell_manifest(tmp_path, require_files=True)
    assert any(".." in e for e in errs)


def test_validate_rejects_users_prefix(tmp_path: Path) -> None:
    from validate_operator_shell_manifest import validate_operator_shell_manifest

    _write_manifest(
        tmp_path,
        textwrap.dedent(
            """\
            schema_version: "1.0.0"
            entries:
              - id: bad
                title: Bad
                path: users/grace-mar/self.md
            """
        ),
    )
    errs, _ = validate_operator_shell_manifest(tmp_path, require_files=False)
    assert any("artifacts/" in e or "docs/" in e for e in errs)
