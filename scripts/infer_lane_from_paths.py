#!/usr/bin/env python3
"""
Infer dominant lane from a list of repo-relative paths using lanes.yaml ownership.

Prints one line: dominant lane name, or "mixed", or "unclassified".
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from check_lane_scope import (  # noqa: E402
    LANES_PATH,
    load_lanes,
    path_matches_glob,
)


def _norm(p: str) -> str:
    return p.replace("\\", "/").lstrip("./")


def lanes_matching_path(path: str, lanes_doc: dict) -> list[str]:
    path = _norm(path)
    lanes_cfg = lanes_doc.get("lanes") or {}
    hits: list[str] = []
    for name, cfg in lanes_cfg.items():
        owned = list(cfg.get("owned_paths") or [])
        if any(path_matches_glob(path, p) for p in owned):
            hits.append(name)
    return hits


def infer_dominant(files: list[str], lanes_doc: dict) -> str:
    if not files:
        return "unclassified"
    labels: list[str | None] = []
    for f in files:
        hs = lanes_matching_path(f, lanes_doc)
        if len(hs) == 0:
            labels.append(None)
        elif len(hs) == 1:
            labels.append(hs[0])
        else:
            return "mixed"
    if all(x is None for x in labels):
        return "unclassified"
    if any(x is None for x in labels):
        return "mixed"
    first = labels[0]
    assert first is not None
    if all(x == first for x in labels):
        return first
    return "mixed"


def main() -> int:
    ap = argparse.ArgumentParser(description="Infer lane from paths.")
    ap.add_argument("paths", nargs="*", help="Repo-relative paths")
    ap.add_argument("--files-from-stdin", action="store_true", help="Read paths from stdin, one per line")
    ap.add_argument("--lanes-yaml", type=Path, default=LANES_PATH)
    args = ap.parse_args()
    if args.files_from_stdin:
        paths = [ln.strip() for ln in sys.stdin if ln.strip()]
    else:
        paths = list(args.paths)
    doc = load_lanes(args.lanes_yaml)
    print(infer_dominant(paths, doc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
