#!/usr/bin/env python3
"""Enforce docs/layer-map.json forbiddenCrossings globs from repo root."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    p = ROOT / "docs" / "layer-map.json"
    if not p.is_file():
        print("layer-enforcer: missing docs/layer-map.json")
        return 1
    cfg = json.loads(p.read_text(encoding="utf-8"))
    bad: list[str] = []
    for pat in cfg.get("forbiddenCrossings", []):
        hits = list(ROOT.glob(pat))
        if hits:
            bad.append(f"{pat} -> {hits}")
    if bad:
        print("layer-enforcer:\n" + "\n".join(bad))
        return 1
    print("layer-enforcer: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
