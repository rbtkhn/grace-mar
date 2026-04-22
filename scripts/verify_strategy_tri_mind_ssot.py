#!/usr/bin/env python3
"""Fail if tri-mind expert mind SSOT paths are missing (flat or experts/<id>/mind.md)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

# Tri-mind B/M/M and any expert whose mind file is linked from skill-strategy lens URLs.
TRI_MIND_IDS = ("barnes", "mearsheimer", "mercouris")


def main() -> int:
    errors: list[str] = []
    for expert_id in TRI_MIND_IDS:
        flat = NOTEBOOK / f"strategy-expert-{expert_id}-mind.md"
        folder = NOTEBOOK / "experts" / expert_id / "mind.md"
        if flat.is_file():
            target = flat.resolve()
            if not target.is_file():
                errors.append(f"{expert_id}: {flat} is broken (resolves to missing {target})")
            continue
        if folder.is_file():
            errors.append(
                f"{expert_id}: missing flat bookmark {flat.name} — add: "
                f"ln -sf experts/{expert_id}/mind.md strategy-notebook/{flat.name}"
            )
            continue
        errors.append(f"{expert_id}: no mind at {flat} or {folder}")

    if errors:
        print("verify_strategy_tri_mind_ssot: FAILED", file=sys.stderr)
        for line in errors:
            print(f"  {line}", file=sys.stderr)
        return 1
    print("verify_strategy_tri_mind_ssot: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
