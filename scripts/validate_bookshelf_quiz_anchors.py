#!/usr/bin/env python3
"""Validate bookshelf-quiz-anchors.yaml against bookshelf-catalog.yaml.

WORK only; not Record. The anchor file is a curated quiz layer over the
Bookshelf catalog, not a replacement catalog.
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
RESEARCH = REPO / "docs" / "skill-work" / "work-strategy" / "history-notebook" / "research"
CATALOG = RESEARCH / "bookshelf-catalog.yaml"
ANCHORS = RESEARCH / "bookshelf-quiz-anchors.yaml"

RE_HNSRC = re.compile(r"^HNSRC-\d{4}$")
SOURCE_KINDS = {"primary", "secondary", "mixed"}


def _load_yaml(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level YAML must be a mapping")
    return data


def validate(catalog_path: Path, anchors_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    try:
        catalog = _load_yaml(catalog_path)
        anchors_doc = _load_yaml(anchors_path)
    except (FileNotFoundError, ValueError) as exc:
        return [f"ERROR: {exc}"], []

    items = catalog.get("items")
    if not isinstance(items, list):
        return ["ERROR: catalog top-level 'items' must be a list"], []
    catalog_ids = {str(x.get("id")) for x in items if isinstance(x, dict) and x.get("id")}

    anchors = anchors_doc.get("anchors")
    if not isinstance(anchors, list):
        return ["ERROR: anchors top-level 'anchors' must be a list"], []

    seen: set[str] = set()
    for i, raw in enumerate(anchors):
        if not isinstance(raw, dict):
            errors.append(f"anchors[{i}]: expected mapping")
            continue
        aid = str(raw.get("id") or "").strip()
        if not aid:
            errors.append(f"anchors[{i}]: id required")
        elif aid in seen:
            errors.append(f"duplicate anchor id: {aid}")
        seen.add(aid)

        source_kind = str(raw.get("source_kind") or "").strip()
        if source_kind not in SOURCE_KINDS:
            errors.append(f"{aid or f'anchors[{i}]'}: source_kind must be one of {sorted(SOURCE_KINDS)}")

        shelf_refs = raw.get("shelf_refs")
        if not isinstance(shelf_refs, list) or not shelf_refs:
            errors.append(f"{aid or f'anchors[{i}]'}: shelf_refs must be a non-empty list")
        else:
            for ref in shelf_refs:
                if not isinstance(ref, str) or not RE_HNSRC.match(ref):
                    errors.append(f"{aid}: invalid shelf ref {ref!r}")
                elif ref not in catalog_ids:
                    errors.append(f"{aid}: unknown shelf ref {ref}")

        for key in ("citation_label", "visible_prompt_label"):
            value = str(raw.get(key) or "").strip()
            if not value:
                errors.append(f"{aid or f'anchors[{i}]'}: {key} required")
            if "HNSRC" in value:
                errors.append(f"{aid or f'anchors[{i}]'}: {key} must not expose HNSRC ids")

        quiz_uses = raw.get("quiz_uses")
        if not isinstance(quiz_uses, list) or not quiz_uses:
            warnings.append(f"{aid or f'anchors[{i}]'}: quiz_uses should list at least one safe use")

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--catalog", type=Path, default=CATALOG)
    ap.add_argument("--anchors", type=Path, default=ANCHORS)
    ap.add_argument("--strict", action="store_true", help="Exit non-zero on warnings as well as errors")
    args = ap.parse_args()

    errors, warnings = validate(args.catalog, args.anchors)
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    for e in errors:
        print(e, file=sys.stderr)

    if errors:
        print(f"validate_bookshelf_quiz_anchors: {len(errors)} error(s)", file=sys.stderr)
        return 1
    if args.strict and warnings:
        print(f"validate_bookshelf_quiz_anchors: {len(warnings)} warning(s) (--strict)", file=sys.stderr)
        return 1
    print("ok: bookshelf-quiz-anchors.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
