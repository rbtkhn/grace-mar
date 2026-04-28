"""Tests for scripts/mcp_local_readonly.py — allowlist, reads, receipts."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

pytest.importorskip("jsonschema")
pytest.importorskip("yaml")


@pytest.fixture(autouse=True)
def _scripts_on_path() -> None:
    p = str(REPO_ROOT / "scripts")
    if p not in sys.path:
        sys.path.insert(0, p)


def _minimal_allowlist_yaml(max_bytes: int = 250_000) -> dict:
    return {
        "version": 1,
        "allowed_roots": ["docs/"],
        "blocked_roots": [
            "users/grace-mar/",
            ".git/",
            "secrets/",
            "private/",
            "node_modules/",
            "venv/",
            ".venv/",
        ],
        "blocked_files": [".env", ".env.local", "id_rsa", "id_ed25519"],
        "blocked_name_patterns": ["*token*", "*secret*", "*credential*", "*.pem", "*.key"],
        "max_file_bytes": max_bytes,
    }


def _dump_allow(tmp_path: Path, cfg: dict) -> Path:
    import yaml

    p = tmp_path / "allowlist.yaml"
    p.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return p


def _run(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    doc: dict,
    *,
    allow_cfg: dict | None = None,
    out_name: str = "packet.md",
) -> tuple[int, Path | None, Path]:
    import mcp_local_readonly as mlr

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(mlr, "DEFAULT_RECEIPT_DIR", rec_dir)

    inp = tmp_path / "req.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")
    outp = tmp_path / "artifacts" / "mcp-local-read" / out_name

    allow_path = _dump_allow(tmp_path, allow_cfg or _minimal_allowlist_yaml())

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "mcp_local_readonly.py",
            "--input",
            str(inp),
            "--output",
            str(outp),
            "--repo-root",
            str(tmp_path),
            "--allowlist",
            str(allow_path),
            "--capabilities",
            str(REPO_ROOT / "config" / "mcp-capabilities.yaml"),
            "--bindings",
            str(REPO_ROOT / "config" / "mcp-authority-bindings.yaml"),
            "--policy",
            str(REPO_ROOT / "config" / "mcp-risk-policy.yaml"),
        ],
    )
    code = mlr.main()
    return code, outp if outp.exists() else None, rec_dir


def test_valid_docs_read_generates_packet(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir(parents=True)
    target = docs / "hello.txt"
    target.write_text("alpha\nbeta\n", encoding="utf-8")

    doc = {
        "schema_version": 1,
        "request": {
            "id": "t1",
            "declared_intent": "Read hello fixture.",
            "path": "docs/hello.txt",
            "include_excerpt": True,
            "max_excerpt_chars": 500,
        },
    }

    code, outp, rec_dir = _run(monkeypatch, tmp_path, doc)
    assert code == 0
    assert outp is not None
    body = outp.read_text(encoding="utf-8")
    assert "LOCAL READ-ONLY MCP-SHAPED RUN · WORK ARTIFACT · NO NETWORK · NO CREDENTIALS · NOT APPROVED INTEGRATION" in body
    assert "NO NETWORK" in body and "NO CREDENTIALS" in body and "NOT APPROVED INTEGRATION" in body
    assert "receipt_id:" in body

    receipt_path = list(rec_dir.glob("*.json"))[0]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["capability"]["id"] == "filesystem_readonly"
    assert receipt["governance"]["canonical_record_touched"] is False
    assert receipt["access"]["resources_written"] == []


def test_absolute_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir(parents=True)
    doc = {
        "schema_version": 1,
        "request": {
            "id": "bad",
            "declared_intent": "x",
            "path": "/etc/passwd",
            "include_excerpt": False,
            "max_excerpt_chars": 0,
        },
    }
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_dotdot_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = {
        "schema_version": 1,
        "request": {
            "id": "bad",
            "declared_intent": "x",
            "path": "docs/../outside.txt",
            "include_excerpt": False,
            "max_excerpt_chars": 0,
        },
    }
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_users_grace_mar_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = {
        "schema_version": 1,
        "request": {
            "id": "bad",
            "declared_intent": "x",
            "path": "users/grace-mar/self.md",
            "include_excerpt": False,
            "max_excerpt_chars": 0,
        },
    }
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_dotenv_basename_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / ".env").write_text("x=y\n", encoding="utf-8")
    doc = {
        "schema_version": 1,
        "request": {
            "id": "bad",
            "declared_intent": "x",
            "path": "docs/.env",
            "include_excerpt": False,
            "max_excerpt_chars": 0,
        },
    }
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_secret_pattern_basename_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "my-secret-notes.txt").write_text("x", encoding="utf-8")
    doc = {
        "schema_version": 1,
        "request": {
            "id": "bad",
            "declared_intent": "x",
            "path": "docs/my-secret-notes.txt",
            "include_excerpt": False,
            "max_excerpt_chars": 0,
        },
    }
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_outside_allowed_roots_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "x.py").write_text("# x", encoding="utf-8")
    doc = {
        "schema_version": 1,
        "request": {
            "id": "bad",
            "declared_intent": "x",
            "path": "scripts/x.py",
            "include_excerpt": False,
            "max_excerpt_chars": 0,
        },
    }
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_oversized_file_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "big.bin").write_bytes(b"x" * 50)

    doc = {
        "schema_version": 1,
        "request": {
            "id": "big",
            "declared_intent": "x",
            "path": "docs/big.bin",
            "include_excerpt": False,
            "max_excerpt_chars": 0,
        },
    }
    cfg = _minimal_allowlist_yaml(max_bytes=20)
    code, _, _ = _run(monkeypatch, tmp_path, doc, allow_cfg=cfg)
    assert code == 1


def test_excerpt_bounded(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "long.txt").write_text("abcdefghijklmnopqrstuvwxyz", encoding="utf-8")

    doc = {
        "schema_version": 1,
        "request": {
            "id": "ex",
            "declared_intent": "excerpt cap",
            "path": "docs/long.txt",
            "include_excerpt": True,
            "max_excerpt_chars": 5,
        },
    }

    code, outp, _ = _run(monkeypatch, tmp_path, doc)
    assert code == 0
    assert outp is not None
    body = outp.read_text(encoding="utf-8")
    parts = body.split("```text")
    assert len(parts) >= 2
    inner = parts[1].split("```", 1)[0].strip("\n")
    assert inner == "abcde"


@pytest.mark.skipif(
    sys.platform.startswith("win") and os.environ.get("GITHUB_ACTIONS"), reason="symlinks fragile on CI windows"
)
def test_symlink_escape_outside_repo_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import tempfile

    outside = Path(tempfile.gettempdir()) / f"_grace_local_read_outside_{os.getpid()}.txt"
    outside.write_text("secret-outside", encoding="utf-8")

    docs = tmp_path / "docs"
    docs.mkdir()
    link = docs / "outside_link.txt"
    try:
        os.symlink(outside, link, target_is_directory=False)
    except OSError:
        pytest.skip("symlink not supported")

    doc = {
        "schema_version": 1,
        "request": {
            "id": "sy",
            "declared_intent": "symlink escape",
            "path": "docs/outside_link.txt",
            "include_excerpt": False,
            "max_excerpt_chars": 0,
        },
    }

    try:
        code, _, _ = _run(monkeypatch, tmp_path, doc)
        assert code == 1
    finally:
        link.unlink(missing_ok=True)
        outside.unlink(missing_ok=True)


def test_repo_example_cli_smoke() -> None:
    """Runs adapter against committed example (writes ignored artifact paths)."""
    import subprocess

    out_md = REPO_ROOT / "artifacts" / "mcp-local-read" / "_pytest_smoke_pr9.md"
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "mcp_local_readonly.py"),
            "--input",
            str(REPO_ROOT / "examples" / "mcp-local-read-request.example.json"),
            "--output",
            str(out_md),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert proc.returncode == 0, proc.stderr
    body = out_md.read_text(encoding="utf-8")
    assert "governed-mcp-layer.md" in body
    out_md.unlink(missing_ok=True)
