#!/usr/bin/env python3
"""Validate docs/skill-work/work-strategy/strategy-notebook/knot-connections.yaml.

Checks: schema keys, paths exist on disk, both endpoints present in
knot-index.yaml, relation is allowed, reason is non-empty, no duplicate
(from, to, relation) triples, status enum if present. WORK only; not Record.

Exit 0 if ok; 1 if any error (prints to stderr).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_CONNECTIONS = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/knot-connections.yaml"
)

DEFAULT_INDEX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/knot-index.yaml"
)

ALLOWED_RELATIONS = frozenset(
    {
        "supports",
        "tension",
        "extends",
        "case-for",
        "mechanism-for",
        "same-watch",
        "sequence-next",
    }
)

ALLOWED_STATUS = frozenset({"active", "retired"})

ALLOWED_CONN_KEYS = frozenset(
    {"from", "to", "relation", "reason", "warrant", "status"}
)


def _load_index_paths(index_path: Path) -> set[str] | None:
    """Return the set of path strings from knot-index.yaml, or None on error."""
    if not index_path.is_file():
        return None
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        return None
    data = yaml.safe_load(index_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return None
    knots = data.get("knots")
    if not isinstance(knots, list):
        return None
    return {row["path"] for row in knots if isinstance(row, dict) and "path" in row}


def validate_connections(
    data: Any,
    *,
    repo_root: Path,
    index_paths: set[str] | None,
) -> list[str]:
    """Return a list of error strings (empty if valid)."""
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a mapping"]

    if "schema_version" not in data:
        errs.append("missing schema_version")
    elif not isinstance(data["schema_version"], int):
        errs.append("schema_version must be an integer")

    declared_relations = data.get("relations")
    if declared_relations is not None:
        if not isinstance(declared_relations, list):
            errs.append("relations must be a list")
        else:
            for r in declared_relations:
                if r not in ALLOWED_RELATIONS:
                    errs.append(f"declared relation {r!r} not in hardcoded allowed set")

    conns = data.get("connections")
    if conns is None:
        return errs + ["missing connections key"]
    if not isinstance(conns, list):
        return errs + ["connections must be a list"]

    seen_triples: dict[tuple[str, str, str], int] = {}

    for i, row in enumerate(conns):
        prefix = f"connections[{i}]"
        if not isinstance(row, dict):
            errs.append(f"{prefix}: entry must be a mapping")
            continue

        extra = set(row.keys()) - ALLOWED_CONN_KEYS
        if extra:
            errs.append(f"{prefix}: unknown keys: {sorted(extra)}")

        from_path = row.get("from")
        to_path = row.get("to")

        for label, val in [("from", from_path), ("to", to_path)]:
            if not val or not isinstance(val, str):
                errs.append(f"{prefix}: {label} is required (non-empty string)")

        if not isinstance(from_path, str) or not isinstance(to_path, str):
            continue

        for label, val in [("from", from_path), ("to", to_path)]:
            p = repo_root / val
            if not p.is_file():
                errs.append(f"{prefix}: {label} path does not exist: {val}")
            if index_paths is not None and val not in index_paths:
                errs.append(f"{prefix}: {label} not found in knot-index.yaml: {val}")

        rel = row.get("relation")
        if not rel or not isinstance(rel, str):
            errs.append(f"{prefix}: relation is required (non-empty string)")
        elif rel not in ALLOWED_RELATIONS:
            errs.append(f"{prefix}: unknown relation {rel!r}")

        reason = row.get("reason")
        if not reason or not isinstance(reason, str):
            errs.append(f"{prefix}: reason is required (non-empty string)")

        warrant = row.get("warrant")
        if warrant is not None:
            if not isinstance(warrant, list) or not all(
                isinstance(w, str) for w in warrant
            ):
                errs.append(f"{prefix}: warrant must be a list of strings when present")

        status = row.get("status")
        if status is not None:
            if not isinstance(status, str) or status not in ALLOWED_STATUS:
                errs.append(
                    f"{prefix}: status must be 'active' or 'retired' when present"
                )

        if isinstance(rel, str) and rel:
            triple = (from_path, to_path, rel)
            if triple in seen_triples:
                errs.append(
                    f"{prefix}: duplicate (from, to, relation) — "
                    f"also at index {seen_triples[triple]}"
                )
            else:
                seen_triples[triple] = i

    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--connections",
        type=Path,
        default=DEFAULT_CONNECTIONS,
        help="Path to knot-connections.yaml",
    )
    ap.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help="Path to knot-index.yaml (for cross-reference checks)",
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root for resolving path entries",
    )
    args = ap.parse_args()

    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        print("error: PyYAML required (pip install pyyaml)", file=sys.stderr)
        return 1

    if not args.connections.is_file():
        print(f"error: missing {args.connections}", file=sys.stderr)
        return 1

    data = yaml.safe_load(args.connections.read_text(encoding="utf-8"))
    index_paths = _load_index_paths(args.index)
    if index_paths is None:
        print(
            f"warning: could not load {args.index}; skipping index cross-checks",
            file=sys.stderr,
        )

    errs = validate_connections(
        data,
        repo_root=args.repo_root.resolve(),
        index_paths=index_paths,
    )
    if errs:
        for e in errs:
            print(f"error: {e}", file=sys.stderr)
        return 1

    n = len(data.get("connections") or [])
    print(f"ok: {args.connections} ({n} connections)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
