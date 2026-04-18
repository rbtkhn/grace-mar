#!/usr/bin/env python3
"""Generate chunk indexes for large non-canonical markdown files.

Splits files on paragraph boundaries, preserves heading context and source
line ranges, writes one .chunks.jsonl per source file under runtime/chunks/.

Non-canonical; does not touch Record or recursion-gate.
See docs/chunked-retrieval.md.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_RUNTIME_DIR = Path(__file__).resolve().parent
if str(_RUNTIME_DIR) not in sys.path:
    sys.path.insert(0, str(_RUNTIME_DIR))

import ledger_paths  # noqa: E402

REPO_ROOT = ledger_paths.REPO_ROOT
ARTIFACTS_DIR = REPO_ROOT / "artifacts"
NOTEBOOK_CHAPTERS = REPO_ROOT / "docs" / "skill-work" / "work-strategy" / "strategy-notebook" / "chapters"

SURFACE_ROOTS: dict[str, Path] = {
    "artifact_lookup": ARTIFACTS_DIR,
    "notebook_lookup": NOTEBOOK_CHAPTERS,
}

SUPPORTED_SUFFIXES = frozenset({".md", ".txt"})
SKIP_DIRS = frozenset({".git", "node_modules", ".cache", "__pycache__"})

DEFAULT_MIN_FILE_SIZE = 4096  # 4 KB — don't chunk small files
DEFAULT_TARGET_CHUNK = 1200   # target chars per chunk
DEFAULT_MIN_CHUNK = 800
DEFAULT_MAX_CHUNK = 2000

HEADING_RE = re.compile(r"^(#{1,4})\s+(.+)$")


def source_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:12]


def _split_paragraphs(text: str) -> list[tuple[str, int, int]]:
    """Split text into paragraphs on blank-line boundaries.

    Returns (paragraph_text, start_line_1based, end_line_1based).
    """
    lines = text.splitlines(keepends=True)
    paragraphs: list[tuple[str, int, int]] = []
    buf: list[str] = []
    start = 1

    for i, line in enumerate(lines, 1):
        if line.strip() == "":
            if buf:
                paragraphs.append(("".join(buf), start, i - 1))
                buf = []
            start = i + 1
        else:
            if not buf:
                start = i
            buf.append(line)

    if buf:
        paragraphs.append(("".join(buf), start, len(lines)))

    return paragraphs


def chunk_file(
    text: str,
    *,
    target: int = DEFAULT_TARGET_CHUNK,
    min_size: int = DEFAULT_MIN_CHUNK,
    max_size: int = DEFAULT_MAX_CHUNK,
) -> list[dict[str, Any]]:
    """Chunk *text* into paragraph-boundary groups with heading context."""
    paragraphs = _split_paragraphs(text)
    if not paragraphs:
        return []

    s_hash = source_hash(text)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    chunks: list[dict[str, Any]] = []
    current_heading = ""
    buf_text = ""
    buf_start = paragraphs[0][1]
    buf_end = paragraphs[0][2]
    buf_heading = ""

    def _flush() -> None:
        nonlocal buf_text, buf_start, buf_end, buf_heading
        if not buf_text.strip():
            return
        idx = len(chunks)
        chunks.append({
            "chunk_id": f"chk_{s_hash[:8]}_{idx:04d}",
            "source_hash": s_hash,
            "chunk_index": idx,
            "start_line": buf_start,
            "end_line": buf_end,
            "section_hint": buf_heading,
            "content": buf_text,
            "char_count": len(buf_text),
            "generated_at": now,
        })
        buf_text = ""

    for para_text, p_start, p_end in paragraphs:
        heading_match = HEADING_RE.match(para_text.strip().splitlines()[0] if para_text.strip() else "")
        if heading_match:
            current_heading = heading_match.group(0).strip()

        if not buf_text:
            buf_text = para_text
            buf_start = p_start
            buf_end = p_end
            buf_heading = current_heading
            continue

        combined_len = len(buf_text) + len(para_text) + 1
        if combined_len <= max_size:
            buf_text += "\n" + para_text
            buf_end = p_end
        else:
            if len(buf_text) >= min_size:
                _flush()
                buf_text = para_text
                buf_start = p_start
                buf_end = p_end
                buf_heading = current_heading
            else:
                buf_text += "\n" + para_text
                buf_end = p_end

    _flush()

    total = len(chunks)
    for c in chunks:
        c["total_chunks"] = total

    return chunks


def generate_for_file(
    src: Path,
    surface: str,
    out_dir: Path,
    *,
    min_file_size: int = DEFAULT_MIN_FILE_SIZE,
) -> int:
    """Generate chunks for one file. Returns number of chunks written."""
    if not src.is_file():
        return 0
    if src.suffix not in SUPPORTED_SUFFIXES:
        return 0
    if src.stat().st_size < min_file_size:
        return 0

    try:
        text = src.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0

    chunks = chunk_file(text)
    if not chunks:
        return 0

    try:
        rel = str(src.relative_to(REPO_ROOT))
    except ValueError:
        rel = str(src)

    for c in chunks:
        c["source_path"] = rel

    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{src.name}.chunks.jsonl"
    with out_file.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    return len(chunks)


def generate_for_surface(surface: str, *, min_file_size: int = DEFAULT_MIN_FILE_SIZE) -> dict[str, int]:
    root = SURFACE_ROOTS.get(surface)
    if root is None:
        raise ValueError(f"unsupported surface: {surface}. allowed: {', '.join(sorted(SURFACE_ROOTS))}")
    if not root.is_dir():
        return {}

    out_base = ledger_paths.chunks_dir(surface)
    stats: dict[str, int] = {}

    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        n = generate_for_file(p, surface, out_base, min_file_size=min_file_size)
        if n > 0:
            try:
                rel = str(p.relative_to(REPO_ROOT))
            except ValueError:
                rel = str(p)
            stats[rel] = n

    return stats


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate chunk indexes for large non-canonical documents.")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--surface", choices=sorted(SURFACE_ROOTS), help="Surface to chunk")
    group.add_argument("--path", type=Path, help="Single file to chunk (writes to stdout surface)")
    group.add_argument("--all", action="store_true", help="Regenerate all surfaces")
    ap.add_argument("--min-size", type=int, default=DEFAULT_MIN_FILE_SIZE, dest="min_size",
                    help=f"Minimum file size in bytes to chunk (default {DEFAULT_MIN_FILE_SIZE})")
    args = ap.parse_args()

    if args.path:
        p = args.path.resolve()
        out_dir = ledger_paths.chunks_dir("manual")
        n = generate_for_file(p, "manual", out_dir, min_file_size=args.min_size)
        if n:
            print(f"chunked {p.name} -> {n} chunks in {out_dir}", file=sys.stderr)
        else:
            print(f"skipped {p.name} (too small, unsupported, or empty)", file=sys.stderr)
        return 0

    surfaces = sorted(SURFACE_ROOTS) if args.all else [args.surface]
    total_files = 0
    total_chunks = 0
    for surface in surfaces:
        stats = generate_for_surface(surface, min_file_size=args.min_size)
        for rel, n in stats.items():
            print(f"  {rel} -> {n} chunks", file=sys.stderr)
            total_chunks += n
        total_files += len(stats)
        if stats:
            print(f"surface={surface}: {len(stats)} files, {sum(stats.values())} chunks", file=sys.stderr)
        else:
            print(f"surface={surface}: no files chunked", file=sys.stderr)

    print(f"\ntotal: {total_files} files, {total_chunks} chunks", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
