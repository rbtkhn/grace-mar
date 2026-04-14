#!/usr/bin/env python3
"""
Validate config/operator_shell_manifest.yaml: schema basics, allowlisted paths, optional on-disk checks.

  python3 scripts/validate_operator_shell_manifest.py
  python3 scripts/validate_operator_shell_manifest.py --allow-missing-files
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_REL = Path("config/operator_shell_manifest.yaml")
ALLOWED_TOP = frozenset({"artifacts", "docs"})
REQUIRED_ENTRY_KEYS = frozenset({"id", "title", "path"})


def _load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as e:
        raise SystemExit(
            "PyYAML is required (pip install pyyaml). " + str(e)
        ) from e
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _path_errors(repo_root: Path, rel: str, *, field: str) -> list[str]:
    errs: list[str] = []
    if not rel or not isinstance(rel, str):
        return [f"{field}: must be a non-empty string"]
    p = Path(rel)
    if p.is_absolute():
        return [f"{field}: absolute paths are not allowed ({rel!r})"]
    if ".." in p.parts:
        return [f"{field}: '..' not allowed ({rel!r})"]
    full = (repo_root / rel).resolve()
    try:
        rel_to_root = full.relative_to(repo_root.resolve())
    except ValueError:
        return [f"{field}: resolves outside repo ({rel!r})"]
    if not rel_to_root.parts or rel_to_root.parts[0] not in ALLOWED_TOP:
        errs.append(
            f"{field}: must be under artifacts/ or docs/ (got {rel!r})"
        )
    return errs


def validate_operator_shell_manifest(
    repo_root: Path,
    *,
    require_files: bool,
) -> tuple[list[str], list[str]]:
    """Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    manifest_path = repo_root / MANIFEST_REL
    if not manifest_path.is_file():
        return [f"Missing {MANIFEST_REL}"], []

    try:
        data = _load_yaml(manifest_path)
    except Exception as e:
        return [f"Invalid YAML: {e}"], []

    if not isinstance(data, dict):
        return ["Root must be a mapping"], []

    sv = data.get("schema_version")
    if not isinstance(sv, str) or not sv.strip():
        errors.append("schema_version must be a non-empty string")

    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("entries must be a non-empty list")

    ids_seen: set[str] = set()
    for i, ent in enumerate(entries or []):
        prefix = f"entries[{i}]"
        if not isinstance(ent, dict):
            errors.append(f"{prefix}: must be a mapping")
            continue
        missing = REQUIRED_ENTRY_KEYS - set(ent.keys())
        if missing:
            errors.append(f"{prefix}: missing keys {sorted(missing)}")
        eid = ent.get("id")
        if isinstance(eid, str):
            if eid in ids_seen:
                errors.append(f"duplicate entry id: {eid!r}")
            ids_seen.add(eid)
        path_val = ent.get("path")
        if isinstance(path_val, str):
            pe = _path_errors(repo_root, path_val, field=f"{prefix}.path")
            errors.extend(pe)
            if not pe:
                full = (repo_root / path_val).resolve()
                if require_files and not full.is_file():
                    errors.append(
                        f"{prefix}: path file missing on disk: {path_val!r}"
                    )
                elif not require_files and not full.is_file():
                    warnings.append(
                        f"{prefix}: file not found (ok with --allow-missing-files): {path_val!r}"
                    )
        elif "path" in ent:
            errors.append(f"{prefix}.path: must be a string")

        doc_val = ent.get("doc")
        if doc_val is None:
            pass
        elif isinstance(doc_val, str) and doc_val.strip():
            de = _path_errors(repo_root, doc_val, field=f"{prefix}.doc")
            errors.extend(de)
            if not de:
                dfull = (repo_root / doc_val).resolve()
                if require_files and not dfull.is_file():
                    errors.append(
                        f"{prefix}: doc file missing on disk: {doc_val!r}"
                    )
                elif not require_files and not dfull.is_file():
                    warnings.append(
                        f"{prefix}: doc not found (ok with --allow-missing-files): {doc_val!r}"
                    )
        elif doc_val is not None:
            errors.append(f"{prefix}.doc: must be a string or null")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root (default: parent of scripts/)",
    )
    ap.add_argument(
        "--allow-missing-files",
        action="store_true",
        help="Allow primary path / doc files to be absent on disk (warn only).",
    )
    args = ap.parse_args()
    root = args.repo_root.resolve()
    errs, warns = validate_operator_shell_manifest(
        root, require_files=not args.allow_missing_files
    )
    for w in warns:
        print(f"WARNING: {w}", file=sys.stderr)
    if errs:
        print("operator_shell_manifest validation FAILED:", file=sys.stderr)
        for e in errs:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("operator_shell_manifest: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
