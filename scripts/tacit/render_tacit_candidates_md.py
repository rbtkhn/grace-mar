#!/usr/bin/env python3
"""
Render tacit candidate JSON files as markdown for human review / copy-paste.

Does not write recursion-gate.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def render(candidates: list[dict]) -> str:
    lines = [
        "# Tacit-derived candidates (non-canonical)",
        "",
        "_Copy sections into `recursion-gate.md` only after companion review; do not treat as Record._",
        "",
    ]
    for i, c in enumerate(candidates, 1):
        lines.extend(
            [
                f"## Candidate {i}: `{c.get('candidate_type')}`",
                "",
                f"- **Title:** {c.get('title')}",
                f"- **Claim:** {c.get('distilled_claim')}",
                f"- **Rationale:** {c.get('rationale')}",
                f"- **Proposed surface:** `{c.get('proposed_destination_surface')}`",
                f"- **Confidence:** {c.get('confidence')}",
                f"- **Provenance tacit id:** `{c.get('provenance_tacit_id')}`",
                "",
                "**Review questions:**",
            ]
        )
        for q in c.get("review_questions") or []:
            lines.append(f"- {q}")
        lines.extend(["", "**Supporting excerpts:**", ""])
        for ex in c.get("supporting_excerpts") or []:
            lines.append(f"> {ex}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Render tacit candidates JSON to markdown.")
    ap.add_argument("inputs", nargs="+", type=Path, help="Candidate .json files")
    ap.add_argument("-o", "--output", type=Path, default=None, help="Output .md path (default stdout)")
    args = ap.parse_args()

    all_c: list[dict] = []
    for p in args.inputs:
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list):
            all_c.extend(data)
        else:
            all_c.append(data)

    md = render(all_c)
    if args.output:
        args.output.write_text(md, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
