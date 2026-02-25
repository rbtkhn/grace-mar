#!/usr/bin/env python3
"""
Export the cognitive fork to a single portable JSON file.

Reads SELF.md, EVIDENCE.md, and LIBRARY.md for the given user and optionally
FORK-MANIFEST.json, then writes a structured JSON export for backup, portability,
or external tooling.

Usage:
    python scripts/export_fork.py
    python scripts/export_fork.py --user grace-mar --output fork-export.json
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _parse_self_summary(content: str) -> dict:
    """Minimal summary: name, age, lexile, IX counts."""
    data = {"name": "?", "age": 0, "lexile_output": "?", "ix_a_count": 0, "ix_b_count": 0, "ix_c_count": 0}
    if m := re.search(r"name:\s*(\S+)", content):
        data["name"] = m.group(1)
    if m := re.search(r"age:\s*(\d+)", content):
        data["age"] = int(m.group(1))
    if m := re.search(r'lexile_output:\s*["\']?([^"\'\n]+)', content):
        data["lexile_output"] = m.group(1).strip()
    data["ix_a_count"] = len(re.findall(r"id:\s+LEARN-\d+", content))
    data["ix_b_count"] = len(re.findall(r"id:\s+CUR-\d+", content))
    data["ix_c_count"] = len(re.findall(r"id:\s+PER-\d+", content))
    return data


def _parse_evidence_summary(content: str) -> dict:
    """Counts of READ, WRITE, CREATE entries."""
    return {
        "read_count": len(re.findall(r"id:\s+READ-\d+", content)),
        "write_count": len(re.findall(r"id:\s+WRITE-\d+", content)),
        "create_count": len(re.findall(r"id:\s+CREATE-\d+", content)),
    }


def export_fork(user_id: str = "grace-mar", include_raw: bool = True) -> dict:
    """Build the fork export structure."""
    profile_dir = REPO_ROOT / "users" / user_id
    self_path = profile_dir / "SELF.md"
    evidence_path = profile_dir / "EVIDENCE.md"
    library_path = profile_dir / "LIBRARY.md"
    manifest_path = profile_dir / "FORK-MANIFEST.json"

    self_raw = _read(self_path)
    evidence_raw = _read(evidence_path)
    library_raw = _read(library_path)

    out = {
        "version": "1.0",
        "format": "grace-mar-fork-export",
        "generated_at": datetime.now().isoformat(),
        "user_id": user_id,
        "summary": {
            "self": _parse_self_summary(self_raw) if self_raw else {},
            "evidence": _parse_evidence_summary(evidence_raw) if evidence_raw else {},
        },
    }
    if include_raw:
        out["self"] = {"raw": self_raw}
        out["evidence"] = {"raw": evidence_raw}
        out["library"] = {"raw": library_raw}
    if manifest_path.exists():
        try:
            out["manifest"] = json.loads(manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            out["manifest"] = None
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Export fork to portable JSON")
    parser.add_argument("--user", "-u", default="grace-mar", help="User id (e.g. grace-mar)")
    parser.add_argument("--output", "-o", default=None, help="Output file (default: stdout)")
    parser.add_argument("--no-raw", action="store_true", help="Omit raw file contents (summary + manifest only)")
    args = parser.parse_args()
    data = export_fork(user_id=args.user, include_raw=not args.no_raw)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}", file=__import__("sys").stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
