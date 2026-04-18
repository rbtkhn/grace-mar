"""Tests for the chunked retrieval layer: chunk generation, chunk store, hybrid integration."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_RUNTIME = REPO_ROOT / "scripts" / "runtime"

sys.path.insert(0, str(SCRIPTS_RUNTIME))
from generate_chunks import chunk_file, source_hash  # noqa: E402


# ── chunk generation unit tests ───────────────────────────────────────


SMALL_DOC = "# Title\n\nOne short paragraph."

LARGE_DOC = "\n\n".join([
    "# Main heading",
    "## Section one\n\nFirst paragraph of section one with enough content to be meaningful. " * 5,
    "## Section two\n\nSecond section has different content about sovereignty and lectures. " * 5,
    "## Section three\n\nThird section discusses Iran sanctions and liability framing. " * 5,
    "## Section four\n\nFourth section covers strategy notebook entries and daily analysis. " * 5,
    "## Section five\n\nFifth section has Barnes countercurrent and jurisdiction history. " * 5,
])


class TestChunkFile:
    def test_large_doc_produces_multiple_chunks(self) -> None:
        chunks = chunk_file(LARGE_DOC)
        assert len(chunks) > 1

    def test_small_doc_produces_one_chunk(self) -> None:
        chunks = chunk_file(SMALL_DOC)
        assert len(chunks) == 1

    def test_empty_doc_produces_no_chunks(self) -> None:
        chunks = chunk_file("")
        assert chunks == []

    def test_chunk_order_preserved(self) -> None:
        chunks = chunk_file(LARGE_DOC)
        indices = [c["chunk_index"] for c in chunks]
        assert indices == list(range(len(chunks)))

    def test_chunk_has_required_fields(self) -> None:
        chunks = chunk_file(LARGE_DOC)
        required = {"chunk_id", "source_hash", "chunk_index", "total_chunks",
                     "start_line", "end_line", "section_hint", "content",
                     "char_count", "generated_at"}
        for c in chunks:
            assert required.issubset(c.keys()), f"missing fields: {required - c.keys()}"

    def test_total_chunks_consistent(self) -> None:
        chunks = chunk_file(LARGE_DOC)
        total = chunks[0]["total_chunks"]
        assert total == len(chunks)
        assert all(c["total_chunks"] == total for c in chunks)

    def test_section_hints_captured(self) -> None:
        chunks = chunk_file(LARGE_DOC)
        hints = [c["section_hint"] for c in chunks if c["section_hint"]]
        assert len(hints) > 0
        assert any("Section" in h for h in hints)

    def test_line_ranges_non_overlapping(self) -> None:
        chunks = chunk_file(LARGE_DOC)
        for i in range(1, len(chunks)):
            assert chunks[i]["start_line"] > chunks[i - 1]["end_line"] or \
                   chunks[i]["start_line"] == chunks[i - 1]["end_line"]

    def test_source_hash_stable(self) -> None:
        h1 = source_hash(LARGE_DOC)
        h2 = source_hash(LARGE_DOC)
        assert h1 == h2
        assert len(h1) == 12

    def test_chunk_id_format(self) -> None:
        chunks = chunk_file(LARGE_DOC)
        for c in chunks:
            assert c["chunk_id"].startswith("chk_")
            parts = c["chunk_id"].split("_")
            assert len(parts) == 3

    def test_content_not_empty(self) -> None:
        chunks = chunk_file(LARGE_DOC)
        for c in chunks:
            assert len(c["content"].strip()) > 0
            assert c["char_count"] > 0


# ── chunk store tests ─────────────────────────────────────────────────


class TestChunkStore:
    def test_no_chunks_available(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))
        import importlib
        import chunk_store
        importlib.reload(chunk_store)
        assert chunk_store.chunks_available("notebook_lookup") is False
        assert chunk_store.load_chunks("notebook_lookup") == []

    def test_load_generated_chunks(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))
        import importlib
        import ledger_paths
        import chunk_store
        importlib.reload(ledger_paths)
        importlib.reload(chunk_store)

        chunks = chunk_file(LARGE_DOC)
        for c in chunks:
            c["source_path"] = "test/large.md"

        out_dir = ledger_paths.chunks_dir("notebook_lookup")
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "large.md.chunks.jsonl"
        with out_file.open("w") as f:
            for c in chunks:
                f.write(json.dumps(c) + "\n")

        assert chunk_store.chunks_available("notebook_lookup") is True
        loaded = chunk_store.load_chunks("notebook_lookup")
        assert len(loaded) == len(chunks)
        assert all(c["source_path"] == "test/large.md" for c in loaded)

    def test_chunked_source_paths(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))
        import importlib
        import ledger_paths
        import chunk_store
        importlib.reload(ledger_paths)
        importlib.reload(chunk_store)

        out_dir = ledger_paths.chunks_dir("artifact_lookup")
        out_dir.mkdir(parents=True, exist_ok=True)
        record = {"chunk_id": "chk_test_0000", "source_path": "artifacts/test.md",
                   "chunk_index": 0, "content": "test"}
        (out_dir / "test.md.chunks.jsonl").write_text(json.dumps(record) + "\n")

        paths = chunk_store.chunked_source_paths("artifact_lookup")
        assert "artifacts/test.md" in paths


# ── CLI integration tests ─────────────────────────────────────────────


class TestGenerateChunksCLI:
    def test_single_file_chunking(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))
        large_file = tmp_path / "big.md"
        large_file.write_text(LARGE_DOC)

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_RUNTIME / "generate_chunks.py"),
             "--path", str(large_file), "--min-size", "100"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "chunks" in result.stderr.lower()

        out_dir = tmp_path / "runtime" / "chunks" / "manual"
        jsonl_files = list(out_dir.glob("*.chunks.jsonl"))
        assert len(jsonl_files) == 1
        lines = [l for l in jsonl_files[0].read_text().splitlines() if l.strip()]
        assert len(lines) > 1

    def test_small_file_skipped(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))
        small_file = tmp_path / "tiny.md"
        small_file.write_text(SMALL_DOC)

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_RUNTIME / "generate_chunks.py"),
             "--path", str(small_file)],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "skipped" in result.stderr.lower()


# ── hybrid retrieval chunk integration ────────────────────────────────


class TestHybridChunkIntegration:
    def test_chunk_aware_search(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """When chunks exist, hybrid retrieval scores at chunk level."""
        monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))
        import importlib
        import ledger_paths
        import chunk_store
        importlib.reload(ledger_paths)
        importlib.reload(chunk_store)

        from hybrid_retrieve import _scan_md_files, REPO_ROOT as HR_ROOT

        doc_dir = tmp_path / "docs"
        doc_dir.mkdir()
        large_file = doc_dir / "strategy.md"
        large_file.write_text(LARGE_DOC)

        chunks = chunk_file(LARGE_DOC)
        try:
            rel = str(large_file.relative_to(HR_ROOT))
        except ValueError:
            rel = str(large_file)
        for c in chunks:
            c["source_path"] = rel

        out_dir = ledger_paths.chunks_dir("notebook_lookup")
        out_dir.mkdir(parents=True, exist_ok=True)
        with (out_dir / "strategy.md.chunks.jsonl").open("w") as f:
            for c in chunks:
                f.write(json.dumps(c) + "\n")

        results = _scan_md_files(
            doc_dir, "sovereignty lectures", 10, "notebook_lookup",
            use_recency=False, weights=(1.0, 0.0, 0.0),
        )

        chunk_results = [r for r in results if r.meta.get("chunk_id")]
        assert len(chunk_results) > 0
        for r in chunk_results:
            assert ":" in r.path  # has line range
            assert r.meta.get("source_path") is not None
            assert r.meta.get("chunk_index") is not None

    def test_fallback_without_chunks(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        """Without chunks, hybrid retrieval falls back to whole-file scoring."""
        monkeypatch.setenv("GRACE_MAR_RUNTIME_LEDGER_ROOT", str(tmp_path))
        import importlib
        import ledger_paths
        import chunk_store
        importlib.reload(ledger_paths)
        importlib.reload(chunk_store)

        from hybrid_retrieve import _scan_md_files

        doc_dir = tmp_path / "docs"
        doc_dir.mkdir()
        (doc_dir / "small.md").write_text("# Sovereignty\n\nA short note about sovereignty.")

        results = _scan_md_files(
            doc_dir, "sovereignty", 5, "notebook_lookup",
            use_recency=False, weights=(1.0, 0.0, 0.0),
        )

        assert len(results) > 0
        for r in results:
            assert r.meta.get("chunk_id") is None  # whole-file result
            assert ":" not in r.path
