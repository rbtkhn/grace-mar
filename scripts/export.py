#!/usr/bin/env python3
"""
Unified export CLI (v1): subprocess dispatch to scripts/export_*.py.

Contract: [docs/EXPORT-CLI.md](../docs/EXPORT-CLI.md) and README (Unified export CLI).

  python scripts/export.py [-u USER] {fork|prp|identity|manifest|bundle|all} [-- EXTRA...]

When EXTRA omits -u/--user, this CLI prepends -u <resolved> (env GRACE_MAR_USER_ID, else
repo default: grace-mar when users/grace-mar exists, else _template).

G1: ``all`` forwards to export_runtime_bundle.py only (same as bundle).

Non-goals: export_view, export_gate_… — use those scripts directly.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"

SUBCOMMAND_SCRIPTS: dict[str, str] = {
    "fork": "export_fork.py",
    "prp": "export_prp.py",
    "identity": "export_user_identity.py",
    "manifest": "export_manifest.py",
    "bundle": "export_runtime_bundle.py",
    "all": "export_runtime_bundle.py",
}


def _default_user_id() -> str:
    env = __import__("os").environ.get("GRACE_MAR_USER_ID", "").strip()
    if env:
        return env
    if (REPO_ROOT / "users" / "grace-mar").is_dir():
        return "grace-mar"
    return "_template"


def _argv_has_user_flag(argv: list[str]) -> bool:
    i = 0
    while i < len(argv):
        if argv[i] in ("-u", "--user"):
            return True
        if argv[i] == "--":
            break
        i += 1
    return False


def _parse_export_cli(argv: list[str]) -> tuple[str | None, str, list[str]]:
    """
    Options: -u/--user (only before subcommand).
    Then: SUBCOMMAND [--] [child args...]
    If ``--`` is present, only tokens after it go to the child; else all tokens
    after subcommand go to the child. Inject -u when child argv has no user flag.
    """
    i = 0
    explicit_user: str | None = None
    while i < len(argv):
        if argv[i] in ("-u", "--user"):
            if i + 1 >= len(argv):
                print("export.py: -u requires a value", file=sys.stderr)
                sys.exit(2)
            explicit_user = argv[i + 1]
            i += 2
            continue
        break

    if i >= len(argv):
        return explicit_user, "__missing__", []

    sub = argv[i]
    i += 1
    rest = argv[i:]
    if rest and rest[0] == "--":
        child = list(rest[1:])
    else:
        child = list(rest)

    resolved = explicit_user or _default_user_id()
    if not _argv_has_user_flag(child):
        child = ["-u", resolved] + child
    return explicit_user, sub, child


def _print_help() -> None:
    du = _default_user_id()
    print(
        f"""usage: python scripts/export.py [-u USER] {{fork|prp|identity|manifest|bundle|all}} [-- EXTRA...]

Unified export CLI — runs the existing script under scripts/ via subprocess.
Resolved default user when the child argv has no -u: GRACE_MAR_USER_ID, else {du!r} (repo heuristic).

Subcommands:
  fork      -> export_fork.py
  prp       -> export_prp.py
  identity  -> export_user_identity.py
  manifest  -> export_manifest.py
  bundle    -> export_runtime_bundle.py
  all       -> export_runtime_bundle.py (G1: same as bundle)

Examples:
  python scripts/export.py fork -- -o out.json
  python scripts/export.py fork -- --format json-ld -o x.jsonld
  python scripts/export.py -u grace-mar prp -- -o prompt.txt

Non-goals: export_view, export_gate_to_review_queue, … (invoke those scripts directly).
"""
    )


def _run_child(script_name: str, child_argv: list[str]) -> int:
    script_path = SCRIPTS_DIR / script_name
    if not script_path.is_file():
        print(
            f"export.py: missing {script_path.relative_to(REPO_ROOT)} — "
            "see docs/EXPORT-CLI.md if this is a template checkout without export modules.",
            file=sys.stderr,
        )
        return 2
    cmd = [sys.executable, str(script_path), *child_argv]
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT))
    return int(proc.returncode)


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv in (["-h"], ["--help"]):
        _print_help()
        return 0

    _explicit, sub, child_argv = _parse_export_cli(argv)
    if sub == "__missing__":
        print(
            "export.py: subcommand required (fork|prp|identity|manifest|bundle|all).\n"
            "Try: python scripts/export.py --help",
            file=sys.stderr,
        )
        return 2

    if sub not in SUBCOMMAND_SCRIPTS:
        print(f"export.py: unknown subcommand {sub!r}", file=sys.stderr)
        print("Try: python scripts/export.py --help", file=sys.stderr)
        return 2

    script = SUBCOMMAND_SCRIPTS[sub]
    return _run_child(script, child_argv)


if __name__ == "__main__":
    sys.exit(main())
