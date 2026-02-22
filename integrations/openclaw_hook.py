#!/usr/bin/env python3
"""
OpenClaw integration hook: export Record for session continuity.

Aligns with docs/OPENCLAW-INTEGRATION.md:
  - Record (SELF + SKILLS) populates OpenClaw USER.md / SOUL.md
  - Run on schedule or post-integration to keep identity in sync

Usage:
    python integrations/openclaw_hook.py --user pilot-001
    python integrations/openclaw_hook.py -u pilot-001 -o ../openclaw/

For unified export with --target, use: integrations/export_hook.py
"""

import sys
from pathlib import Path

# Delegate to unified export hook
from export_hook import run_export


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Export Grace-Mar Record for OpenClaw")
    parser.add_argument("--user", "-u", default="pilot-001", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output directory (default: users/[id]/)")
    args = parser.parse_args()
    out = Path(args.output) if args.output else None
    return run_export("openclaw", out, args.user)


if __name__ == "__main__":
    sys.exit(main())
