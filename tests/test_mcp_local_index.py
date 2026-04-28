"""Tests for scripts/mcp_local_index.py — allowlist, traversal, receipts."""

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


def _base_doc(path: str = "docs/root", **req_kw: object) -> dict:
    req = {
        "id": "t1",
        "declared_intent": "Index fixture.",
        "path": path,
        "recursive": False,
        "max_depth": 1,
        "include_file_hashes": False,
        "include_line_counts": False,
        "max_entries": 100,
    }
    req.update(req_kw)  # type: ignore[arg-type]
    return {"schema_version": 1, "request": req}


def _run(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    doc: dict,
    *,
    allow_cfg: dict | None = None,
    out_name: str = "packet.md",
) -> tuple[int, Path | None, Path]:
    import mcp_local_index as mli

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(mli, "DEFAULT_RECEIPT_DIR", rec_dir)

    inp = tmp_path / "req.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")
    outp = tmp_path / "artifacts" / "mcp-local-index" / out_name

    allow_path = _dump_allow(tmp_path, allow_cfg or _minimal_allowlist_yaml())

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "mcp_local_index.py",
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
    code = mli.main()
    return code, outp if outp.exists() else None, rec_dir


def test_valid_docs_dir_index_generates_packet(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "docs" / "root"
    root.mkdir(parents=True)
    (root / "a.txt").write_text("one\ntwo\n", encoding="utf-8")
    (root / "sub").mkdir()
    (root / "sub" / "b.txt").write_text("x", encoding="utf-8")

    doc = _base_doc("docs/root", recursive=False, max_entries=50)

    code, outp, rec_dir = _run(monkeypatch, tmp_path, doc)
    assert code == 0
    assert outp is not None
    body = outp.read_text(encoding="utf-8")
    banner = (
        "LOCAL READ-ONLY DIRECTORY INDEX · WORK ARTIFACT · NO NETWORK · NO CREDENTIALS · "
        "NOT APPROVED INTEGRATION"
    )
    assert banner in body
    assert "NO NETWORK" in body and "NO CREDENTIALS" in body and "NOT APPROVED INTEGRATION" in body
    assert "receipt_id:" in body
    assert "```text" not in body

    receipt_path = list(rec_dir.glob("*.json"))[0]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["capability"]["id"] == "filesystem_readonly"
    assert receipt["actor"]["name"] == "mcp_local_index.py"
    assert receipt["governance"]["canonical_record_touched"] is False
    assert receipt["access"]["resources_written"] == []
    rid = receipt["receipt_id"]
    assert rid in body


def test_absolute_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir(parents=True)
    doc = _base_doc("/etc")
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_dotdot_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_doc("docs/../outside")
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_users_grace_mar_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    doc = _base_doc("users/grace-mar/")
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_dotenv_root_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / ".env").mkdir()

    doc = _base_doc("docs/.env")
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_secret_pattern_skipped(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "docs" / "root"
    root.mkdir(parents=True)
    (root / "my-secret-notes.txt").write_text("x", encoding="utf-8")

    doc = _base_doc("docs/root", recursive=False)
    code, outp, _ = _run(monkeypatch, tmp_path, doc)
    assert code == 0
    assert outp is not None
    body = outp.read_text(encoding="utf-8")
    assert "my-secret-notes" not in body
    assert "Skipped entries:** 1" in body or "Skipped entries:** " in body


def test_outside_allowed_roots_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir(parents=True)

    doc = _base_doc("scripts")
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_non_directory_path_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "only.txt").write_text("x", encoding="utf-8")

    doc = _base_doc("docs/only.txt")
    assert _run(monkeypatch, tmp_path, doc)[0] == 1


def test_max_entries_enforced(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "docs" / "many"
    root.mkdir(parents=True)
    for i in range(6):
        (root / f"f{i}.txt").write_text("x", encoding="utf-8")

    doc = _base_doc("docs/many", recursive=False, max_entries=2)
    code, outp, _ = _run(monkeypatch, tmp_path, doc)
    assert code == 0
    assert outp is not None
    body = outp.read_text(encoding="utf-8")
    assert "**Total entries emitted:** 2" in body


def test_max_depth_enforced(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "docs" / "deep"
    root.mkdir(parents=True)
    sub = root / "sub"
    sub.mkdir()
    (sub / "inner.txt").write_text("deep", encoding="utf-8")

    doc = _base_doc("docs/deep", recursive=True, max_depth=0, max_entries=50)
    code, outp, _ = _run(monkeypatch, tmp_path, doc)
    assert code == 0
    assert outp is not None
    body = outp.read_text(encoding="utf-8")
    assert "inner.txt" not in body


def test_oversized_line_count_placeholder(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "docs" / "big"
    root.mkdir(parents=True)
    (root / "big.txt").write_bytes(b"x" * 500)

    doc = _base_doc("docs/big", recursive=False, include_line_counts=True, max_entries=10)
    cfg = _minimal_allowlist_yaml(max_bytes=20)
    import mcp_local_index as mli

    rec_dir = tmp_path / "mcp-receipts"
    rec_dir.mkdir(parents=True)
    monkeypatch.setattr(mli, "DEFAULT_RECEIPT_DIR", rec_dir)

    inp = tmp_path / "req.json"
    inp.write_text(json.dumps(doc), encoding="utf-8")
    outp = tmp_path / "artifacts" / "mcp-local-index" / "p.md"
    allow_path = _dump_allow(tmp_path, cfg)

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "mcp_local_index.py",
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
    assert mli.main() == 0
    body = outp.read_text(encoding="utf-8")
    assert "over max_file_bytes" in body


@pytest.mark.skipif(
    sys.platform.startswith("win") and os.environ.get("GITHUB_ACTIONS"), reason="symlinks fragile on CI windows"
)
def test_symlink_escape_target_fails(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    import tempfile

    outside = Path(tempfile.gettempdir()) / f"_grace_local_idx_out_{os.getpid()}"
    outside.mkdir(exist_ok=True)
    (outside / "nested").write_text("outside", encoding="utf-8")

    docs = tmp_path / "docs"
    docs.mkdir()
    link = docs / "outside_dir"
    try:
        os.symlink(outside, link, target_is_directory=True)
    except OSError:
        pytest.skip("symlink not supported")

    doc = _base_doc("docs/outside_dir")
    try:
        assert _run(monkeypatch, tmp_path, doc)[0] == 1
    finally:
        link.unlink(missing_ok=True)
        (outside / "nested").unlink(missing_ok=True)
        outside.rmdir()


@pytest.mark.skipif(
    sys.platform.startswith("win") and os.environ.get("GITHUB_ACTIONS"), reason="symlinks fragile on CI windows"
)
def test_symlink_child_skipped(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    root = tmp_path / "docs" / "sl"
    root.mkdir(parents=True)
    (root / "real.txt").write_text("ok", encoding="utf-8")
    try:
        os.symlink(REPO_ROOT / "README.md", root / "readme_link.md")
    except OSError:
        pytest.skip("symlink not supported")

    doc = _base_doc("docs/sl", recursive=False)
    code, outp, _ = _run(monkeypatch, tmp_path, doc)
    assert code == 0
    assert outp is not None
    body = outp.read_text(encoding="utf-8")
    assert "readme_link" not in body.lower()


def test_repo_example_cli_smoke() -> None:
    """Runs adapter against committed example (writes ignored artifact paths)."""
    import subprocess

    out_md = REPO_ROOT / "artifacts" / "mcp-local-index" / "_pytest_smoke_pr10.md"
    proc = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "mcp_local_index.py"),
            "--input",
            str(REPO_ROOT / "examples" / "mcp-local-index-request.example.json"),
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
    assert "LOCAL READ-ONLY DIRECTORY INDEX" in body
    assert "mcp-local-index-adapter.md" in body or "docs/mcp" in body
    out_md.unlink(missing_ok=True)
