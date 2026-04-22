#!/usr/bin/env python3
"""Validate History Notebook bookshelf-catalog.yaml (HNSRC-* seed rows).

Checks: unique ids, required era, optional eras (multi-bucket; must include era),
candidate_hn_chapters ⊆ book-architecture.yaml, duplicate (title, author) warnings,
optional hn_volume vs era heuristic.

Exit 0 on success; exit 1 if --strict and any error, or on duplicate ids / bad era / bad hn-*.

WORK-only; not Record.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

REPO = Path(__file__).resolve().parent.parent
CATALOG = (
    REPO
    / "docs"
    / "skill-work"
    / "work-strategy"
    / "history-notebook"
    / "research"
    / "bookshelf-catalog.yaml"
)
HN_ARCH = REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / "book-architecture.yaml"

RE_HNSRC = re.compile(r"^HNSRC-\d{4}$")
ERAS = frozenset({"ancient", "medieval", "colonial", "industrial", "modern"})
ERA_TO_VOLUME = {
    "ancient": "vol-i",
    "medieval": "vol-ii",
    "colonial": "vol-iii",
    "industrial": "vol-iv",
    "modern": "vol-v",
}


def load_valid_hn_ids(path: Path) -> set[str]:
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    chapters = data.get("chapters") or []
    return {c["id"] for c in chapters if isinstance(c, dict) and "id" in c}


def validate_catalog(
    catalog_path: Path,
    arch_path: Path,
    *,
    strict: bool,
) -> tuple[list[str], list[str]]:
    """Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    if not catalog_path.is_file():
        return [f"ERROR: missing {catalog_path}"], []

    data = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
    items = data.get("items")
    if not isinstance(items, list):
        return ["ERROR: top-level 'items' must be a list"], []

    valid_hn = load_valid_hn_ids(arch_path)
    if not arch_path.is_file():
        errors.append(f"ERROR: missing {arch_path}")
        return errors, warnings

    seen_ids: set[str] = set()
    seen_pairs: dict[tuple[str, str], str] = {}

    for i, raw in enumerate(items):
        if not isinstance(raw, dict):
            errors.append(f"items[{i}]: expected mapping, got {type(raw).__name__}")
            continue
        sid = raw.get("id")
        if not sid or not isinstance(sid, str):
            errors.append(f"items[{i}]: missing string id")
            continue
        if not RE_HNSRC.match(sid):
            errors.append(f"items[{i}]: id must match HNSRC-NNNN, got {sid!r}")
        if sid in seen_ids:
            errors.append(f"duplicate id: {sid}")
        seen_ids.add(sid)

        title = (raw.get("title") or "").strip()
        author = (raw.get("author") or "").strip()
        if not title:
            errors.append(f"{sid}: title required")
        if not author:
            errors.append(f"{sid}: author required")

        era = raw.get("era")
        if era not in ERAS:
            errors.append(f"{sid}: era must be one of {sorted(ERAS)}, got {era!r}")

        eras_field = raw.get("eras")
        if eras_field is not None:
            if not isinstance(eras_field, list):
                errors.append(f"{sid}: eras must be a list when set, got {type(eras_field).__name__}")
            elif len(eras_field) == 0:
                errors.append(f"{sid}: eras must be non-empty when set")
            else:
                seen_era: set[str] = set()
                for e in eras_field:
                    if not isinstance(e, str):
                        errors.append(f"{sid}: each eras entry must be a string")
                        continue
                    if e not in ERAS:
                        errors.append(f"{sid}: unknown era in eras {e!r}")
                        continue
                    if e in seen_era:
                        errors.append(f"{sid}: duplicate era in eras: {e!r}")
                    seen_era.add(e)
                if isinstance(era, str) and era in ERAS and era not in seen_era:
                    errors.append(
                        f"{sid}: primary era={era!r} must be included in eras when eras is set"
                    )
                if len(eras_field) == 1 and isinstance(era, str) and eras_field[0] == era:
                    warnings.append(
                        f"{sid}: eras has one entry matching era — drop eras or add more categories"
                    )

        pair = (title.lower(), author.lower())
        if title and author:
            if pair in seen_pairs:
                warnings.append(
                    f"duplicate title+author: {title!r} / {author!r} "
                    f"(also {seen_pairs[pair]})"
                )
            else:
                seen_pairs[pair] = sid

        for ch in raw.get("candidate_hn_chapters") or []:
            if not isinstance(ch, str):
                errors.append(f"{sid}: candidate_hn_chapters must be strings")
                continue
            if ch not in valid_hn:
                errors.append(f"{sid}: unknown hn chapter id {ch!r}")

        hv = raw.get("hn_volume")
        if era in ERA_TO_VOLUME and hv is not None and isinstance(hv, str):
            expected = ERA_TO_VOLUME[era]
            if hv != expected:
                warnings.append(
                    f"{sid}: hn_volume={hv!r} vs era={era!r} (typical {expected})"
                )

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--catalog",
        type=Path,
        default=CATALOG,
        help="Path to bookshelf-catalog.yaml",
    )
    ap.add_argument(
        "--architecture",
        type=Path,
        default=HN_ARCH,
        help="Path to book-architecture.yaml",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="Exit 1 if any warning (duplicate title+author) or any error",
    )
    args = ap.parse_args()

    errors, warnings = validate_catalog(args.catalog, args.architecture, strict=args.strict)

    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    for e in errors:
        print(e, file=sys.stderr)

    if errors:
        print(f"validate_bookshelf_catalog: {len(errors)} error(s)", file=sys.stderr)
        return 1
    if args.strict and warnings:
        print(f"validate_bookshelf_catalog: {len(warnings)} warning(s) (--strict)", file=sys.stderr)
        return 1

    print("ok: bookshelf-catalog.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
