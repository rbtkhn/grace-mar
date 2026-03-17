#!/usr/bin/env python3
"""
Scaffold a WRITE-* or CREATE-* evidence block for users/grace-mar/self-evidence.md.

Given an artifact path (and optional title, context, evidence_tier), generates the correct
YAML block. Infers next ID from existing id: WRITE-N / id: CREATE-N in self-evidence.md.
Follows docs/pipeline-map.md artifact naming and docs/evidence-template.md structure.

Usage:
  python scripts/scaffold_evidence_entry.py --artifact users/grace-mar/artifacts/write-0007-my-story.png --kind write --title "My story"
  python scripts/scaffold_evidence_entry.py --artifact artifacts/create-0011-something.jpg --kind create --title "Something" --evidence-tier 4
  python scripts/scaffold_evidence_entry.py -a artifacts/write-0008.png -k write -t "Journal" --output /tmp/new_entry.yaml

Output: printed to stdout, or appended to --output file.
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _next_id(content: str, prefix: str) -> str:
    ids = [int(m.group(1)) for m in re.finditer(rf"{prefix}-(\d+)", content)]
    n = max(ids, default=0) + 1
    return f"{prefix}-{n:04d}"


def _normalize_image_file(artifact_path: str, user_id: str) -> str:
    """Return path as stored in evidence: artifacts/<basename> or artifacts/write-N-slug.ext."""
    p = Path(artifact_path)
    if not p.suffix:
        p = p.with_suffix(".png")
    base = p.name
    if not base.startswith(("write-", "create-")):
        return f"artifacts/{base}"
    return f"artifacts/{base}"


def scaffold_write(
    evidence_path: Path,
    artifact_path: str,
    title: str,
    context: str,
    evidence_tier: int,
    next_id: str,
) -> str:
    content = evidence_path.read_text(encoding="utf-8")
    image_file = _normalize_image_file(artifact_path, "grace-mar")
    created = date.today().isoformat()
    block = f"""  - id: {next_id}
    type: original  # or retell, journal, etc.
    title: "{title}"
    created_at: {created}
    word_count: 0  # fill in
    image_file: {image_file}
    evidence_tier: {evidence_tier}  # OBSERVED = 4

    full_text: ""  # child's exact text

    decoded_text: ""  # corrected spelling/grammar

    context: "{context}"
"""
    return block


def scaffold_create(
    evidence_path: Path,
    artifact_path: str,
    title: str,
    context: str,
    evidence_tier: int,
    next_id: str,
) -> str:
    image_file = _normalize_image_file(artifact_path, "grace-mar")
    created = date.today().isoformat()
    block = f"""  - id: {next_id}
    type: drawing  # or collage, etc.
    title: "{title}"
    description: ""  # describe what's in the image
    image_file: {image_file}
    created_at: {created}
    evidence_tier: {evidence_tier}  # OBSERVED = 4
    context: "{context}"

    analysis:
      subjects: []  # list elements in the image
      themes: []    # themes signaled
      originality: 4  # 1-5
"""
    return block


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Scaffold WRITE-* or CREATE-* evidence block for self-evidence.md"
    )
    ap.add_argument(
        "-u", "--user",
        default="grace-mar",
        help="User id (default: grace-mar)",
    )
    ap.add_argument(
        "-a", "--artifact",
        required=True,
        help="Path to artifact file (e.g. artifacts/write-0007-title.png or users/grace-mar/artifacts/create-0011.jpg)",
    )
    ap.add_argument(
        "-k", "--kind",
        choices=("write", "create"),
        required=True,
        help="Evidence kind: write (Writing Log) or create (Creation Log)",
    )
    ap.add_argument(
        "-t", "--title",
        default="(fill in title)",
        help="Title for the entry (default: placeholder)",
    )
    ap.add_argument(
        "-c", "--context",
        default="",
        help="Optional context (e.g. school, operator-submitted, prompt used)",
    )
    ap.add_argument(
        "--evidence-tier",
        type=int,
        default=4,
        help="Evidence tier (default: 4 = OBSERVED)",
    )
    ap.add_argument(
        "-o", "--output",
        default=None,
        help="Append block to this file instead of stdout",
    )
    args = ap.parse_args()

    user_id = args.user.strip()
    evidence_path = REPO_ROOT / "users" / user_id / "self-evidence.md"
    if not evidence_path.exists():
        print(f"Error: {evidence_path} not found", file=sys.stderr)
        sys.exit(1)

    content = evidence_path.read_text(encoding="utf-8")
    prefix = "WRITE" if args.kind == "write" else "CREATE"
    next_id = _next_id(content, prefix)

    if args.kind == "write":
        block = scaffold_write(
            evidence_path,
            args.artifact,
            args.title,
            args.context or "(fill in context)",
            args.evidence_tier,
            next_id,
        )
    else:
        block = scaffold_create(
            evidence_path,
            args.artifact,
            args.title,
            args.context or "",
            args.evidence_tier,
            next_id,
        )

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "a", encoding="utf-8") as f:
            f.write(block)
        print(f"Appended {next_id} block to {out_path}", file=sys.stderr)
    else:
        print(block, end="")


if __name__ == "__main__":
    main()
