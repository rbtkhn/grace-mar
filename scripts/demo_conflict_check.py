#!/usr/bin/env python3
"""
Demonstrate personality contradiction detection (staging layer).

Full governed workflow: docs/CONTRADICTION-ENGINE-SPEC.md (sidecars, UI, merge).
This script shows what runs today: bot/conflict_check.py + conflict_rules.yaml.

Usage (from repo root):
  python3 scripts/demo_conflict_check.py
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "bot"))

from conflict_check import (  # noqa: E402
    check_conflicts,
    format_conflicts_for_yaml,
    _load_self_personality_summary,
)


def main() -> None:
    print("=" * 60)
    print("Grace-Mar — conflict check demo (personality opposites)")
    print("=" * 60)
    summary = _load_self_personality_summary()
    preview = (summary[:200] + "…") if len(summary) > 200 else summary
    print("\n1) Personality text loaded from users/grace-mar/self.md (traits + IX-C):")
    print(f"   ({len(summary)} chars) {preview!r}\n")

    # Candidate that should clash if profile has "independent"
    clash_yaml = """
mind_category: personality
suggested_ix_section: IX-C
summary: Observed dependent behavior in group work; prefers heavy scaffolding
suggested_entry: "Often relies on partner prompts before starting — dependent in pairs"
""".strip()

    print("2) Staged candidate YAML (personality, implies 'dependent'):")
    print("   " + "\n   ".join(clash_yaml.split("\n")) + "\n")

    conflicts = check_conflicts(clash_yaml)
    print(f"3) check_conflicts() → {len(conflicts)} hit(s)")
    for c in conflicts:
        print(f"   - rule={c['rule']} pair={c['pair']}")
        print(f"     {c['existing_hint']} vs {c['new_hint']}")

    if conflicts:
        print("\n4) YAML fragment appended to gate candidate (conflicts_detected):")
        print(format_conflicts_for_yaml(conflicts))

    safe_yaml = """
mind_category: personality
summary: Still independent; worked solo on science fair for two weeks
suggested_entry: "Independent self-starter on long projects"
""".strip()
    print("\n5) Control candidate (reinforces 'independent'):")
    print("   " + "\n   ".join(safe_yaml.split("\n")))
    safe = check_conflicts(safe_yaml)
    print(f"   → {len(safe)} conflict(s) (expected 0)\n")

    print("=" * 60)
    print("Done. Staging path: bot/core.py uses this before recursion-gate append.")
    print("=" * 60)


if __name__ == "__main__":
    main()
