"""Gated approved log rotation (self-evidence § VIII or legacy self-archive)."""

import gzip

import pytest


def _archive_body(n: int) -> str:
    blocks = []
    for i in range(n):
        blocks.append(f"**[2024-01-{i+1:02d} 12:00:00]** Entry {i}\n> line\n")
    return "# SELF-ARCHIVE\n\n---\n\n" + "\n\n".join(blocks)


def _evidence_with_viii(n: int) -> str:
    blocks = []
    for i in range(n):
        blocks.append(f"**[2024-01-{i+1:02d} 12:00:00]** Entry {i}\n> line\n")
    gated = (
        "## VIII. GATED APPROVED LOG (SELF-ARCHIVE)\n\n"
        "> test\n\n---\n\n"
        + "\n\n".join(blocks)
        + "\n"
    )
    return "# EVIDENCE\n\n## I. X\n\n```yaml\nx: 1\n```\n\n" + gated + "\nEND OF FILE\n"


def test_rotate_embedded_viii_compress_writes_gz(tmp_path, monkeypatch):
    import rotate_telegram_archive as ra

    monkeypatch.setattr(ra, "REPO_ROOT", tmp_path)
    uid = "rot-test"
    ud = tmp_path / "users" / uid
    ud.mkdir(parents=True)
    (ud / "self-evidence.md").write_text(_evidence_with_viii(6), encoding="utf-8")

    r = ra.rotate_archive(
        user_id=uid,
        apply=True,
        max_entries=3,
        max_bytes=10_000_000,
        keep_recent=2,
        compress=True,
    )
    assert r["rotated"] >= 1
    assert r.get("source") == "self-evidence"
    gz = ud / "archives" / "SELF-ARCHIVE-2024-01.md.gz"
    assert gz.is_file()
    with gzip.open(gz, "rt", encoding="utf-8") as f:
        text = f.read()
    assert "Entry 0" in text or "2024-01-01" in text


def test_rotate_legacy_standalone_plain_md(tmp_path, monkeypatch):
    import rotate_telegram_archive as ra

    monkeypatch.setattr(ra, "REPO_ROOT", tmp_path)
    uid = "rot-test"
    ud = tmp_path / "users" / uid
    ud.mkdir(parents=True)
    (ud / "self-evidence.md").write_text("# EVIDENCE\n\nno section viii\n", encoding="utf-8")
    (ud / "self-archive.md").write_text(_archive_body(6), encoding="utf-8")

    r = ra.rotate_archive(
        user_id=uid,
        apply=True,
        max_entries=3,
        max_bytes=10_000_000,
        keep_recent=2,
        compress=False,
    )
    assert r["rotated"] >= 1
    assert r.get("source") == "self-archive.md"
    assert (ud / "archives" / "SELF-ARCHIVE-2024-01.md").is_file()
