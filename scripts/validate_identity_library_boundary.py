#!/usr/bin/env python3
"""
SELF-KNOWLEDGE vs SELF-LIBRARY: IX-A must not hold domain/corpus dumps.

User-facing copy may say "Library" for SELF-LIBRARY; validators and file paths stay canonical.
See scripts/surface_aliases.py. See docs/boundary-self-knowledge-self-library.md

  python3 scripts/validate_identity_library_boundary.py -u grace-mar
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TOPIC_MAX = 380
CORPUS_HINT = re.compile(
    r"\b(encyclopedia|corpus|codex|CIV-MEM|CMC|ENCYCLOPEDIA\.md|"
    r"civilization.memory|full.text.of|see\s+docs/civilization-memory)\b",
    re.I,
)
# CIV-MEM / library paths must not appear in IX-A topics (belongs in self-library.md)
PATH_LEAK = re.compile(
    r"docs/civilization-memory[/\"'\s]|artifacts/civ-mem|lib-stubs\.yaml|/civ-mem-encyclopedia",
    re.I,
)


def _ix_a_block(self_md: str) -> str:
    i = self_md.find("### IX-A")
    if i < 0:
        return ""
    j = self_md.find("### IX-B", i)
    return self_md[i : j if j > 0 else i + 15000]


def collect_identity_library_violations(
    user_dir: Path,
    *,
    repo_root: Path | None = None,
) -> list[str]:
    """
    Return human-readable violation strings for self.md IX-A in user_dir.
    Empty if OK.
    """
    repo_root = repo_root or REPO
    rel = lambda p: str(p.relative_to(repo_root)).replace("\\", "/")
    path = user_dir / "self.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    block = _ix_a_block(text)
    out: list[str] = []
    for m in re.finditer(
        r"topic:\s*[\"']([^\"']{1,8000})[\"']|topic:\s*([^\n]+)",
        block,
    ):
        topic = (m.group(1) or m.group(2) or "").strip().strip('"').strip("'")
        long_ = len(topic) > TOPIC_MAX
        corpus = bool(CORPUS_HINT.search(topic))
        path_leak = bool(PATH_LEAK.search(topic))
        if not long_ and not corpus and not path_leak:
            continue
        bits = []
        if long_:
            bits.append(f"length {len(topic)}>{TOPIC_MAX}")
        if corpus:
            bits.append("corpus/library keyword")
        if path_leak:
            bits.append("CIV-MEM/library path in identity topic")
        snippet = (topic[:120] + "…") if len(topic) > 120 else topic
        out.append(
            f"{rel(path)} IX-A ({', '.join(bits)}): SELF-LIBRARY/CIV-MEM not "
            f"SELF-KNOWLEDGE — {snippet}"
        )
    return out


def collect_self_library_file_warnings(user_dir: Path, repo_root: Path) -> list[str]:
    """Warn when identity file exists but canonical SELF-LIBRARY file is missing."""
    self_p = user_dir / "self.md"
    lib_p = user_dir / "self-library.md"
    if not self_p.is_file() or lib_p.is_file():
        return []
    rel = str(user_dir.relative_to(repo_root)).replace("\\", "/")
    return [
        f"{rel}: self-library.md missing — SELF-LIBRARY surface absent; "
        "LIB→CMC routing requires LIB entries in self-library.md"
    ]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default="grace-mar")
    args = ap.parse_args()
    ud = REPO / "users" / args.user
    viol = collect_identity_library_violations(ud)
    if not viol:
        print("Identity/library boundary scan: OK (no IX-A corpus-style violations).")
        return 0
    for v in viol:
        print(v, file=sys.stderr)
    print(
        f"Identity/library boundary: {len(viol)} violation(s). "
        "See docs/boundary-self-knowledge-self-library.md",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
