#!/usr/bin/env python3
"""
Check harness invariants (run before model upgrades or when auditing the stack).

Runs governance_checker and optionally warns if core surface exceeds line thresholds.
See docs/IMPLEMENTABLE-INSIGHTS.md — small auditable surface, no autonomous merge.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Optional: warn if core files exceed these lines (auditable surface)
LINE_LIMITS = {
    REPO_ROOT / "bot" / "core.py": 2000,
    REPO_ROOT / "bot" / "prompt.py": 800,
}


def run_governance_check() -> bool:
    """Return True if governance check passes."""
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "governance_checker.py")],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr or result.stdout, file=sys.stderr)
        return False
    print("Governance check: OK")
    return True


def check_line_limits() -> bool:
    """Warn (don't fail) if core files exceed suggested line count. Return True."""
    all_ok = True
    for path, limit in LINE_LIMITS.items():
        if not path.exists():
            continue
        n = len(path.read_text(encoding="utf-8", errors="ignore").splitlines())
        if n > limit:
            print(f"Harness surface: {path.relative_to(REPO_ROOT)} has {n} lines (suggested ≤ {limit})", file=sys.stderr)
            all_ok = False
    if all_ok:
        print("Harness surface: within suggested limits")
    return True  # never fail on line count, only warn


def main() -> int:
    if not run_governance_check():
        return 1
    check_line_limits()
    return 0


if __name__ == "__main__":
    sys.exit(main())
