#!/usr/bin/env python3
"""
OpenClaw integration hook: export Record for session continuity.

Aligns with docs/OPENCLAW-INTEGRATION.md:
  - Record (SELF + SKILLS) populates OpenClaw USER.md / SOUL.md
  - Run on schedule or post-integration to keep identity in sync

Usage:
    python integrations/openclaw_hook.py --user pilot-001
    python integrations/openclaw_hook.py -u pilot-001 -o ../openclaw/
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_export(output_dir: Path | None, user_id: str = "pilot-001") -> int:
    """Run export_user_identity and export_manifest; optionally write to output_dir."""
    scripts = REPO_ROOT / "scripts"
    out = output_dir or (REPO_ROOT / "users" / user_id)

    # Export identity
    cmd = [sys.executable, str(scripts / "export_user_identity.py"), "-u", user_id, "-o", str(out / "USER.md")]
    r = subprocess.run(cmd, cwd=REPO_ROOT)
    if r.returncode != 0:
        return r.returncode

    # Export manifest (agent discoverability)
    cmd2 = [sys.executable, str(scripts / "export_manifest.py"), "-u", user_id, "-o", str(out)]
    r2 = subprocess.run(cmd2, cwd=REPO_ROOT)
    if r2.returncode != 0:
        return r2.returncode

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Grace-Mar Record for OpenClaw")
    parser.add_argument("--user", "-u", default="pilot-001", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output directory (default: users/[id]/)")
    args = parser.parse_args()
    out = Path(args.output) if args.output else None
    return run_export(out, args.user)


if __name__ == "__main__":
    sys.exit(main())
