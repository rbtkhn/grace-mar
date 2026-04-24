#!/usr/bin/env python3
"""
Create interface artifact metadata JSON (Interface Artifact Spec v1).

Default output:
  artifacts/work-dev/interface-artifacts/iface-YYYYMMDD-XXXXXXXX.json

Does not stage to recursion-gate or touch Record surfaces.

Usage (from repo root):
  python3 scripts/work_dev/new_interface_artifact.py \
    --title "Example Interface Artifact" \
    --artifact-kind html-visualizer \
    --generated-path artifacts/work-dev/interface-artifacts/example.html \
    --source-input docs/skill-work/work-strategy/strategy-notebook \
    --intended-use "Example protocol smoke test"
"""

from __future__ import annotations

import argparse
import json
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path

from validate_interface_artifact import ALLOWED_ARTIFACT_KIND, validate_interface_artifact

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_OUTPUT_DIR = REPO_ROOT / "artifacts" / "work-dev" / "interface-artifacts"

_FORBIDDEN_NAMES = frozenset(
    {
        "self.md",
        "self-archive.md",
        "self-library.md",
        "recursion-gate.md",
    }
)


def _expand_list(values: list[str] | None) -> list[str]:
    if not values:
        return []
    out: list[str] = []
    for value in values:
        for part in value.split(","):
            stripped = part.strip()
            if stripped:
                out.append(stripped)
    return out


def _forbidden_write_path(path: Path) -> bool:
    try:
        resolved = path.resolve()
        rel = resolved.relative_to(REPO_ROOT)
    except ValueError:
        return False
    return len(rel.parts) >= 2 and rel.parts[0] == "users" and rel.name in _FORBIDDEN_NAMES


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="artifact title")
    parser.add_argument(
        "--artifact-kind",
        required=True,
        choices=sorted(ALLOWED_ARTIFACT_KIND),
        help="artifactKind enum value",
    )
    parser.add_argument(
        "--generated-path",
        action="append",
        required=True,
        default=None,
        metavar="PATH",
        help="generated artifact path (repeat or comma-separated)",
    )
    parser.add_argument(
        "--source-input",
        action="append",
        required=True,
        default=None,
        metavar="PATH",
        help="source input path (repeat or comma-separated)",
    )
    parser.add_argument(
        "--intended-use",
        required=True,
        help="human-facing intended use for the artifact",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="metadata JSON output path; relative paths resolve to repo root",
    )
    parser.add_argument(
        "--canonical-record-access",
        default="none",
        choices=("none", "read-only"),
        help="canonicalRecordAccess (default: none)",
    )
    parser.add_argument(
        "--source-contract-ref",
        default="",
        help="optional governing doc path for the artifact",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    artifact_id = f"iface-{datetime.now(timezone.utc):%Y%m%d}-{secrets.token_hex(4)}"
    data: dict[str, object] = {
        "artifactId": artifact_id,
        "title": args.title,
        "artifactKind": args.artifact_kind,
        "status": "draft",
        "sourceInputs": _expand_list(args.source_input),
        "generatedPaths": _expand_list(args.generated_path),
        "intendedUse": args.intended_use,
        "mutationScope": "runtime-only",
        "canonicalRecordAccess": args.canonical_record_access,
        "recordAuthority": "none",
        "gateEffect": "none",
        "inspectionStatus": "not-inspected",
        "relatedWorkbenchReceipt": None,
        "typicalNextStep": "inspect-in-workbench",
    }
    if args.source_contract_ref:
        data["sourceContractRef"] = args.source_contract_ref

    if args.output is None:
        out_path = DEFAULT_OUTPUT_DIR / f"{artifact_id}.json"
    else:
        out_path = args.output
        if not out_path.is_absolute():
            out_path = REPO_ROOT / out_path

    if _forbidden_write_path(out_path):
        print(f"refuse: will not write to protected path: {out_path}", file=sys.stderr)
        return 1

    errors = validate_interface_artifact(data)
    if errors:
        for error in errors:
            print(f"invalid: {error}", file=sys.stderr)
        return 1

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
