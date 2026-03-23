#!/usr/bin/env python3
"""
Dry-run integration surface checks for OpenClaw / export / continuity paths.

Does not modify git, the Record, or continuity-log.jsonl. Verifies:
- user directory and continuity contract files exist
- key integration scripts compile
- continuity_read_log --dry-run succeeds
- integration modules load without executing main()

Usage:
  python scripts/check_integration_readiness.py
  python scripts/check_integration_readiness.py -u grace-mar
  python scripts/check_integration_readiness.py --verbose
"""

from __future__ import annotations

import argparse
import importlib.util
import os
import py_compile
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar"

INTEGRATION_SCRIPTS = (
    REPO_ROOT / "integrations" / "openclaw_hook.py",
    REPO_ROOT / "integrations" / "openclaw_stage.py",
)
CONTINUITY_SCRIPT = REPO_ROOT / "scripts" / "continuity_read_log.py"
CONTINUITY_FILES = ("session-log.md", "recursion-gate.md", "self-evidence.md")


def _load_module_no_main(path: Path, name: str) -> None:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run checks for export/stage/continuity integration surface."
    )
    parser.add_argument("-u", "--user", default=DEFAULT_USER, help="User id (default from env or grace-mar)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print each check as it passes")
    args = parser.parse_args()
    user = args.user.strip()
    verbose = args.verbose
    errors: list[str] = []
    warnings: list[str] = []

    def ok(msg: str) -> None:
        if verbose:
            print(f"ok: {msg}")

    user_dir = REPO_ROOT / "users" / user
    if not user_dir.is_dir():
        errors.append(f"User directory missing: {user_dir}")
    else:
        ok(f"user dir {user_dir}")
        for name in CONTINUITY_FILES:
            p = user_dir / name
            if not p.is_file():
                warnings.append(f"Continuity contract file missing: {p.relative_to(REPO_ROOT)}")
            else:
                ok(f"file {name}")

    for script in INTEGRATION_SCRIPTS:
        if not script.is_file():
            errors.append(f"Integration script missing: {script}")
        else:
            try:
                py_compile.compile(str(script), doraise=True)
            except py_compile.PyCompileError as e:
                errors.append(f"py_compile failed {script.name}: {e}")
            else:
                ok(f"py_compile {script.name}")

    if CONTINUITY_SCRIPT.is_file():
        rc = subprocess.run(
            [sys.executable, str(CONTINUITY_SCRIPT), "-u", user, "--dry-run"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if rc.returncode != 0:
            err = (rc.stderr or rc.stdout or "").strip()
            errors.append(f"continuity_read_log --dry-run failed (exit {rc.returncode}): {err[:500]}")
        else:
            ok("continuity_read_log --dry-run")
    else:
        errors.append(f"continuity script missing: {CONTINUITY_SCRIPT}")

    integrations_dir = str(REPO_ROOT / "integrations")
    if integrations_dir not in sys.path:
        sys.path.insert(0, integrations_dir)
    for path, mod_name in (
        (INTEGRATION_SCRIPTS[0], "openclaw_hook_check"),
        (INTEGRATION_SCRIPTS[1], "openclaw_stage_check"),
    ):
        if path.is_file():
            try:
                _load_module_no_main(path, mod_name)
            except Exception as e:
                errors.append(f"import {path.name}: {e}")
            else:
                ok(f"import {path.name}")

    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    for e in errors:
        print(f"error: {e}", file=sys.stderr)

    if errors:
        print("check_integration_readiness: FAILED", file=sys.stderr)
        return 1
    print("check_integration_readiness: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
