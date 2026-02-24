#!/usr/bin/env python3
"""
Unified export hook for downstream integrations.

Targets:
  openclaw    — Record → USER.md + manifest (OpenClaw session continuity)
  intersignal — Record → symbolic_identity.json + manifest (Familiar nodes, Mesh Cache)
  curriculum  — Record → curriculum_profile.json (adaptive curriculum engines)

Usage:
    python integrations/export_hook.py --target openclaw --user pilot-001
    python integrations/export_hook.py --target intersignal -u pilot-001 -o ../intersignal-mesh/
"""

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def run_export(
    target: str,
    output_dir: Path | None,
    user_id: str = "pilot-001",
    openclaw_format: str = "md+manifest",
) -> int:
    scripts = REPO_ROOT / "scripts"
    profile_dir = REPO_ROOT / "users" / user_id
    out = output_dir or profile_dir

    if target == "openclaw":
        out.mkdir(parents=True, exist_ok=True)
        fmt = openclaw_format.strip().lower()
        if fmt in {"md", "md+manifest", "json+md", "full-prp"}:
            r = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "export_user_identity.py"),
                    "-u",
                    user_id,
                    "--format",
                    "markdown",
                    "-o",
                    str(out / "USER.md"),
                ],
                cwd=REPO_ROOT,
            )
            if r.returncode != 0:
                return r.returncode

        if fmt in {"json+md"}:
            r_json = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "export_user_identity.py"),
                    "-u",
                    user_id,
                    "--format",
                    "json",
                    "-o",
                    str(out / "USER.json"),
                ],
                cwd=REPO_ROOT,
            )
            if r_json.returncode != 0:
                return r_json.returncode

        if fmt in {"md+manifest", "json+md", "full-prp"}:
            r_manifest = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "export_manifest.py"),
                    "-u",
                    user_id,
                    "-o",
                    str(out),
                ],
                cwd=REPO_ROOT,
            )
            if r_manifest.returncode != 0:
                return r_manifest.returncode

        if fmt in {"full-prp"}:
            r_prp = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "export_prp.py"),
                    "-u",
                    user_id,
                    "-o",
                    str(out / "OPENCLAW-PRP.txt"),
                ],
                cwd=REPO_ROOT,
            )
            if r_prp.returncode != 0:
                return r_prp.returncode

        if fmt in {"fork-json"}:
            r_fork = subprocess.run(
                [
                    sys.executable,
                    str(scripts / "export_fork.py"),
                    "-u",
                    user_id,
                    "-o",
                    str(out / "fork-export.json"),
                ],
                cwd=REPO_ROOT,
            )
            if r_fork.returncode != 0:
                return r_fork.returncode

    elif target == "intersignal":
        cmd = [
            sys.executable,
            str(scripts / "export_symbolic.py"),
            "-u", user_id,
            "-o", str(out),
        ]
        r = subprocess.run(cmd, cwd=REPO_ROOT)
        if r.returncode != 0:
            return r.returncode

        cmd2 = [
            sys.executable,
            str(scripts / "export_manifest.py"),
            "-u", user_id,
            "-o", str(out),
        ]
        r2 = subprocess.run(cmd2, cwd=REPO_ROOT)
        if r2.returncode != 0:
            return r2.returncode

    elif target == "curriculum":
        cmd = [
            sys.executable,
            str(scripts / "export_curriculum.py"),
            "-u", user_id,
            "-o", str(out),
        ]
        r = subprocess.run(cmd, cwd=REPO_ROOT)
        if r.returncode != 0:
            return r.returncode

    else:
        print(f"Unknown target: {target}", file=sys.stderr)
        return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export Grace-Mar Record for downstream integrations"
    )
    parser.add_argument(
        "--target", "-t",
        choices=["openclaw", "intersignal", "curriculum"],
        required=True,
        help="Integration target",
    )
    parser.add_argument("--user", "-u", default="pilot-001", help="User id")
    parser.add_argument("--output", "-o", default=None, help="Output directory (default: users/[id]/)")
    parser.add_argument(
        "--openclaw-format",
        choices=["md", "md+manifest", "json+md", "full-prp", "fork-json"],
        default="md+manifest",
        help="OpenClaw export shape (openclaw target only)",
    )
    args = parser.parse_args()
    out = Path(args.output) if args.output else None
    return run_export(args.target, out, args.user, openclaw_format=args.openclaw_format)


if __name__ == "__main__":
    sys.exit(main())
