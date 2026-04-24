#!/usr/bin/env python3
"""Create a safe export bundle JSON for external runtime complements (membrane v1).

Stdlib only. Does not read users/, recursion-gate, or Record trees unless
explicitly listed via --include-doc.

Output: runtime/runtime-complements/exports/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
EXPORTS = REPO_ROOT / "runtime" / "runtime-complements" / "exports"

DEFAULT_BOUNDARY_NOTICE = (
    "External runtimes may use this bundle for runtime context only. "
    "This bundle is not permission to write canonical Grace-Mar state. "
    "Any persistent change must return as a staged runtime observation "
    "and pass through the normal gate."
)

DEFAULT_MEMBRANE = (
    "Runtime complement export (membrane v1). This bundle is optional WORK/runtime "
    "context. Grace-Mar canonical memory remains the gated Record only. See "
    "docs/runtime/runtime-complements.md."
)


def _ts_compact() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _rel_posix(root: Path, p: Path) -> str:
    try:
        return p.resolve().relative_to(root).as_posix()
    except ValueError:
        return p.resolve().as_posix()


def read_doc(root: Path, rel: str) -> tuple[dict[str, Any], str | None]:
    """Return ({path, content} or {path, missing: true}, None) or (None, error)."""
    p = (root / rel).resolve()
    if not p.is_file():
        return {"path": rel, "missing": True}, f"not found: {rel}"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"path": rel, "missing": True, "error": str(e)}, str(e)
    return {"path": rel, "content": text}, None


def main() -> int:
    ap = argparse.ArgumentParser(
        description=(
            "Write a namespaced export bundle for runtime complements "
            "(read-only, explicit paths)."
        )
    )
    ap.add_argument(
        "--name",
        required=True,
        help="Bundle name label (e.g. demo, strategy-console).",
    )
    ap.add_argument(
        "--include-doc",
        action="append",
        default=[],
        metavar="PATH",
        help="Repo-relative path to a single file to include (repeatable).",
    )
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=EXPORTS,
        help="Output directory (default: runtime/runtime-complements/exports).",
    )
    ap.add_argument(
        "--no-default-text",
        action="store_true",
        help=(
            "Omit default membrane blurb when no files are included "
            "(boundary_notice still set)."
        ),
    )
    args = ap.parse_args()

    root = REPO_ROOT
    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    ts = _ts_compact()
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "-", args.name)
    bundle_id = f"runtime-complement-export_{ts}_{safe}.json"
    out_path = out_dir / bundle_id

    included: list[dict[str, Any]] = []
    missing: list[str] = []
    for rel in args.include_doc:
        rel = rel.strip()
        if not rel or ".." in rel:
            missing.append(f"(rejected): {rel!r}")
            continue
        item, _err = read_doc(root, rel)
        if item.get("missing"):
            missing.append(rel)
        included.append(item)

    if not any("content" in i for i in included) and not args.no_default_text:
        if not any(i.get("path") == "_membrane" for i in included):
            included.append({"path": "_membrane", "content": DEFAULT_MEMBRANE})
    body: dict[str, Any] = {
        "kind": "runtime_complement_export",
        "bundle_id": bundle_id.replace(".json", ""),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "name": args.name,
        "repo_root": str(root),
        "included_files": included,
        "missing_files": missing,
        "boundary_notice": DEFAULT_BOUNDARY_NOTICE,
    }
    out_path.write_text(
        json.dumps(body, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(_rel_posix(root, out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
