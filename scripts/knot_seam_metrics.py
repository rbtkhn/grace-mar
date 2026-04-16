#!/usr/bin/env python3
"""Read-only seam/weave metrics from knot-index + knot markdown files.

Counts outgoing markdown links to other `strategy-notebook-knot-*.md` files per
indexed knot (cross-weave links). Compares to optional `weave_count` in
`knot-index.yaml` when present.

WORK only; not Record. Default exit 0. With ``--strict-drift``, exit 1 if any
indexed ``weave_count`` disagrees with the computed link count.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_INDEX = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/knot-index.yaml"
)

# Markdown link target containing another knot basename (relative or bare filename).
_RE_KNOT_LINK = re.compile(
    r"\]\([^)]*(strategy-notebook-knot-[^)\s#]+\.md)",
    re.IGNORECASE,
)


def count_outgoing_knot_links(text: str, self_basename: str) -> int:
    """Count link targets that reference a strategy-notebook-knot file other than self."""
    n = 0
    seen: set[str] = set()
    for m in _RE_KNOT_LINK.finditer(text):
        target = m.group(1).split("/")[-1]
        if target.lower() == self_basename.lower():
            continue
        if target not in seen:
            seen.add(target)
            n += 1
    return n


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
        help="Repository root",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Print one JSON object per line (path, basename, computed_count, yaml_count, delta).",
    )
    ap.add_argument(
        "--strict-drift",
        action="store_true",
        help=(
            "Exit 1 when any row has weave_count set and it differs from computed "
            "(CI drift guard)."
        ),
    )
    args = ap.parse_args()
    root = args.repo_root.resolve()

    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        print("error: PyYAML required (pip install pyyaml)", file=sys.stderr)
        return 1

    if not args.index.is_file():
        print(f"error: missing {args.index}", file=sys.stderr)
        return 1

    data = yaml.safe_load(args.index.read_text(encoding="utf-8"))
    knots = data.get("knots") if isinstance(data, dict) else None
    if not isinstance(knots, list):
        print("error: knots must be a list", file=sys.stderr)
        return 1

    rows: list[dict[str, object]] = []
    for row in knots:
        if not isinstance(row, dict):
            continue
        path_s = row.get("path")
        if not path_s or not isinstance(path_s, str):
            continue
        p = root / path_s
        base = Path(path_s).name
        wc_yaml = row.get("weave_count")
        yaml_count: int | None
        if wc_yaml is None:
            yaml_count = None
        elif isinstance(wc_yaml, int):
            yaml_count = wc_yaml
        else:
            yaml_count = None

        computed = 0
        if p.is_file():
            text = p.read_text(encoding="utf-8")
            computed = count_outgoing_knot_links(text, base)

        delta: int | None = None
        if yaml_count is not None:
            delta = computed - yaml_count

        rows.append(
            {
                "path": path_s,
                "basename": base,
                "computed": computed,
                "yaml": yaml_count,
                "delta": delta,
            }
        )

    if args.strict_drift:
        bad = [r for r in rows if r["delta"] is not None and r["delta"] != 0]
        if bad:
            for r in bad:
                print(
                    f"error: weave_count drift {r['path']!r}: "
                    f"yaml={r['yaml']!r} computed={r['computed']!r} delta={r['delta']!r}",
                    file=sys.stderr,
                )
            print(
                f"error: {len(bad)} knot(s) with weave_count != computed links "
                f"(re-run `python3 scripts/knot_seam_metrics.py` and fix YAML)",
                file=sys.stderr,
            )
            return 1

    if args.json:
        import json

        for r in rows:
            print(json.dumps(r, ensure_ascii=False))
        return 0

    w_path = max(len(str(r["path"])) for r in rows) if rows else 10
    print(f"{'path':<{w_path}}  out_links  weave_count  delta")
    print("-" * (w_path + 32))
    for r in rows:
        y = "-" if r["yaml"] is None else str(r["yaml"])
        d = "-" if r["delta"] is None else str(r["delta"])
        print(
            f"{str(r['path']):<{w_path}}  {r['computed']!s:>9}  {y:>11}  {d:>5}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
