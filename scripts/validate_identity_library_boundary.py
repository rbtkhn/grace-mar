#!/usr/bin/env python3
"""
Advisory checks: SELF-KNOWLEDGE (IX-A) should not hold domain-library dumps.

Warns when IX-A topics are oversized or contain corpus-like keywords.
Exit 0 always. See docs/boundary-self-knowledge-self-library.md

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


def _ix_a_block(self_md: str) -> str:
    i = self_md.find("### IX-A")
    if i < 0:
        return ""
    j = self_md.find("### IX-B", i)
    return self_md[i : j if j > 0 else i + 15000]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("-u", "--user", default="grace-mar")
    args = ap.parse_args()
    path = REPO / "users" / args.user / "self.md"
    if not path.is_file():
        print(f"skip: {path}", file=sys.stderr)
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    block = _ix_a_block(text)
    warnings = 0
    for m in re.finditer(
        r"topic:\s*[\"']([^\"']{1,8000})[\"']|topic:\s*([^\n]+)",
        block,
    ):
        topic = (m.group(1) or m.group(2) or "").strip().strip('"').strip("'")
        if len(topic) > TOPIC_MAX:
            print(
                f"WARN IX-A: topic length {len(topic)} (> {TOPIC_MAX}) — "
                "consider SELF-LIBRARY / CIV-MEM, not identity dump:",
                topic[:120] + ("…" if len(topic) > 120 else ""),
            )
            warnings += 1
        if CORPUS_HINT.search(topic):
            print(
                "WARN IX-A: corpus/library keyword in topic — belongs in SELF-LIBRARY:",
                topic[:200],
            )
            warnings += 1

    if warnings == 0:
        print("Identity/library boundary scan: OK (no IX-A corpus-style warnings).")
    else:
        print(
            f"Identity/library boundary: {warnings} warning(s). "
            "See docs/boundary-self-knowledge-self-library.md",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
