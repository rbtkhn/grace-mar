"""Read-only chunk store for generated chunk indexes.

Loads .chunks.jsonl files from runtime/chunks/<surface>/.
Parallel to observation_store.py.

Non-canonical; see runtime/chunks/README.md.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Iterator

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

import ledger_paths  # noqa: E402


def _iter_jsonl(path: Path) -> Iterator[dict]:
    if not path.is_file():
        return
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def chunks_available(surface: str) -> bool:
    """True if any .chunks.jsonl files exist for *surface*."""
    d = ledger_paths.chunks_dir(surface)
    if not d.is_dir():
        return False
    return any(d.glob("*.chunks.jsonl"))


def load_chunks(surface: str) -> list[dict]:
    """Load all chunk records for *surface*, sorted by source_path then chunk_index."""
    d = ledger_paths.chunks_dir(surface)
    if not d.is_dir():
        return []
    records: list[dict] = []
    for p in sorted(d.glob("*.chunks.jsonl")):
        records.extend(_iter_jsonl(p))
    records.sort(key=lambda r: (r.get("source_path", ""), r.get("chunk_index", 0)))
    return records


def load_chunks_for_file(surface: str, filename: str) -> list[dict]:
    """Load chunks from a specific .chunks.jsonl file."""
    d = ledger_paths.chunks_dir(surface)
    p = d / f"{filename}.chunks.jsonl"
    records = list(_iter_jsonl(p))
    records.sort(key=lambda r: r.get("chunk_index", 0))
    return records


def chunked_source_paths(surface: str) -> set[str]:
    """Return the set of source_path values that have chunks for *surface*."""
    chunks = load_chunks(surface)
    return {c["source_path"] for c in chunks if "source_path" in c}
