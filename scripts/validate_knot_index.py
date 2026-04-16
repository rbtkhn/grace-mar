#!/usr/bin/env python3
"""Validate docs/skill-work/work-strategy/strategy-notebook/knot-index.yaml.

Checks: schema keys, unique paths, paths exist under repo root, basenames contain
``knot``, ISO dates, optional ``knot_label`` kebab-case, list types for
clusters/patterns, optional v4 fields (``weave_count``, ``seam_integrity``,
``qoi_check``, ``kac_check``). WORK only; not Record.

Optional: ``--warn-days-md`` / ``--strict-days-md`` — each indexed knot file's
basename should appear in ``chapters/YYYY-MM/days.md`` for weave continuity
(see STRATEGY-NOTEBOOK-ARCHITECTURE). Warnings only by default; strict fails CI.

Exit 0 if ok; 1 if any error (prints to stderr).
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_INDEX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/knot-index.yaml"
)

# Lowercase kebab: segments of [a-z0-9]+ separated by single hyphens.
_RE_KNOT_LABEL = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def _parse_date(s: str) -> bool:
    try:
        datetime.strptime(s, "%Y-%m-%d")
    except (TypeError, ValueError):
        return False
    return True


def validate_knot_index_data(data: Any, *, repo_root: Path) -> list[str]:
    """Return a list of error strings (empty if valid)."""
    errs: list[str] = []
    if not isinstance(data, dict):
        return ["root must be a mapping"]

    if "schema_version" not in data:
        errs.append("missing schema_version")
    elif not isinstance(data["schema_version"], int):
        errs.append("schema_version must be an integer")

    knots = data.get("knots")
    if knots is None:
        return errs + ["missing knots key"]
    if not isinstance(knots, list):
        return errs + ["knots must be a list"]

    paths_seen: dict[str, int] = {}
    wave_seen: dict[tuple[str, str], int] = {}

    for i, row in enumerate(knots):
        prefix = f"knots[{i}]"
        if not isinstance(row, dict):
            errs.append(f"{prefix}: entry must be a mapping")
            continue

        path_s = row.get("path")
        if not path_s or not isinstance(path_s, str):
            errs.append(f"{prefix}: path is required (string)")
            continue

        if path_s in paths_seen:
            errs.append(
                f"{prefix}: duplicate path {path_s!r} (also at index {paths_seen[path_s]})"
            )
        else:
            paths_seen[path_s] = i

        p = repo_root / path_s
        if not p.is_file():
            errs.append(f"{prefix}: path does not exist: {path_s}")

        base = Path(path_s).name.lower()
        if "knot" not in base:
            errs.append(
                f"{prefix}: basename must contain substring 'knot': {Path(path_s).name!r}"
            )

        date_s = row.get("date")
        if not date_s or not isinstance(date_s, str):
            errs.append(f"{prefix}: date is required (YYYY-MM-DD string)")
        elif not _parse_date(date_s):
            errs.append(f"{prefix}: invalid date {date_s!r} (expected YYYY-MM-DD)")

        kl = row.get("knot_label")
        if kl is not None:
            if not isinstance(kl, str):
                errs.append(f"{prefix}: knot_label must be a string when present")
            elif not kl:
                errs.append(f"{prefix}: knot_label must be non-empty when present")
            elif not _RE_KNOT_LABEL.match(kl):
                errs.append(
                    f"{prefix}: knot_label must be kebab-case "
                    f"(lowercase [a-z0-9] segments separated by single hyphens): {kl!r}"
                )
            elif isinstance(date_s, str) and _parse_date(date_s):
                key = (date_s, kl)
                if key in wave_seen:
                    errs.append(
                        f"{prefix}: duplicate (date, knot_label) "
                        f"{date_s!r}, {kl!r} (also index {wave_seen[key]})"
                    )
                else:
                    wave_seen[key] = i

        for key in ("clusters", "patterns"):
            v = row.get(key)
            if v is None:
                continue
            if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
                errs.append(f"{prefix}: {key} must be a list of strings when present")
                break

        note = row.get("note")
        if note is not None and not isinstance(note, str):
            errs.append(f"{prefix}: note must be a string when present")

        wc = row.get("weave_count")
        if wc is not None:
            if isinstance(wc, bool):
                errs.append(
                    f"{prefix}: weave_count must be a non-negative int when present "
                    f"(not bool)"
                )
            elif not isinstance(wc, int):
                errs.append(
                    f"{prefix}: weave_count must be a non-negative int when present"
                )
            elif wc < 0:
                errs.append(f"{prefix}: weave_count must be >= 0")

        si = row.get("seam_integrity")
        if si is not None:
            if isinstance(si, bool):
                errs.append(
                    f"{prefix}: seam_integrity must be a number in [0, 1] when present "
                    f"(not bool)"
                )
            elif isinstance(si, int):
                if si not in (0, 1):
                    errs.append(
                        f"{prefix}: seam_integrity int must be 0 or 1 when present"
                    )
            elif isinstance(si, float):
                if si < 0.0 or si > 1.0:
                    errs.append(
                        f"{prefix}: seam_integrity must be in [0.0, 1.0], got {si!r}"
                    )
            else:
                errs.append(
                    f"{prefix}: seam_integrity must be a number in [0, 1] when present"
                )

        for chk in ("qoi_check", "kac_check"):
            v = row.get(chk)
            if v is not None and not isinstance(v, bool):
                errs.append(f"{prefix}: {chk} must be a boolean when present")

        allowed = {
            "path",
            "date",
            "knot_label",
            "clusters",
            "patterns",
            "note",
            "weave_count",
            "seam_integrity",
            "qoi_check",
            "kac_check",
        }
        extra = set(row.keys()) - allowed
        if extra:
            errs.append(f"{prefix}: unknown keys: {sorted(extra)}")

    return errs


def days_md_link_warnings(data: Any, *, repo_root: Path) -> list[str]:
    """Return warnings when a knot basename is missing from the month's days.md.

    Skips rows that fail basic path/date sanity (handled by validate_knot_index_data).
    """
    warns: list[str] = []
    knots = data.get("knots") if isinstance(data, dict) else None
    if not isinstance(knots, list):
        return warns

    notebook = (
        repo_root
        / "docs/skill-work/work-strategy/strategy-notebook/chapters"
    )

    for i, row in enumerate(knots):
        prefix = f"knots[{i}]"
        if not isinstance(row, dict):
            continue
        path_s = row.get("path")
        date_s = row.get("date")
        if not path_s or not isinstance(path_s, str):
            continue
        if not date_s or not isinstance(date_s, str) or not _parse_date(date_s):
            continue
        p = repo_root / path_s
        if not p.is_file():
            continue

        ym = date_s[:7]
        days_path = notebook / ym / "days.md"
        basename = Path(path_s).name

        if not days_path.is_file():
            warns.append(
                f"{prefix}: {days_path.relative_to(repo_root)} missing — "
                f"cannot verify weave link for {basename!r}"
            )
            continue

        text = days_path.read_text(encoding="utf-8")
        if basename not in text:
            warns.append(
                f"{prefix}: knot basename {basename!r} not found in "
                f"{days_path.relative_to(repo_root)} (add Signal bullet / link?)"
            )

    return warns


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--index",
        type=Path,
        default=DEFAULT_INDEX,
        help="Path to knot-index.yaml",
    )
    ap.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root for resolving path entries",
    )
    ap.add_argument(
        "--warn-days-md",
        action="store_true",
        help=(
            "After validation, warn if each knot's basename is not referenced in "
            "chapters/YYYY-MM/days.md (weave continuity). Exit 0 unless combined "
            "with --strict-days-md."
        ),
    )
    ap.add_argument(
        "--strict-days-md",
        action="store_true",
        help="Treat --warn-days-md findings as errors (exit 1).",
    )
    args = ap.parse_args()

    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        print("error: PyYAML required (pip install pyyaml)", file=sys.stderr)
        return 1

    if not args.index.is_file():
        print(f"error: missing {args.index}", file=sys.stderr)
        return 1

    data = yaml.safe_load(args.index.read_text(encoding="utf-8"))
    root = args.repo_root.resolve()
    errs = validate_knot_index_data(data, repo_root=root)
    if errs:
        for e in errs:
            print(f"error: {e}", file=sys.stderr)
        return 1

    n = len(data.get("knots") or [])
    if args.warn_days_md or args.strict_days_md:
        dw = days_md_link_warnings(data, repo_root=root)
        for w in dw:
            print(f"warning: {w}", file=sys.stderr)
        if dw and args.strict_days_md:
            print(
                f"error: {len(dw)} days.md weave link issue(s) (--strict-days-md)",
                file=sys.stderr,
            )
            return 1

    print(f"ok: {args.index} ({n} knots)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
