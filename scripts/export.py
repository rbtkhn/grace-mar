#!/usr/bin/env python3
"""
Unified export CLI (v1): subprocess dispatch to scripts/export_*.py.

Contract: [docs/EXPORT-CLI.md](../docs/EXPORT-CLI.md) and README (Unified export CLI).
Export classes: [docs/portable-record/export-contract.md](../docs/portable-record/export-contract.md).

  python scripts/export.py [-u USER] {fork|prp|identity|manifest|bundle|emulation|all} [-- EXTRA...]
  python scripts/export.py [-u USER] --export-class {tool_bootstrap|full|task_limited|capability|emulation} [-- EXTRA...]

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
    "emulation": "export_emulation_bundle.py",
    "all": "export_runtime_bundle.py",
}

EXPORT_CLASS_ROUTES: dict[str, tuple[str, list[str]]] = {
    "tool_bootstrap": ("export_prp.py", []),
    "full": ("export_runtime_bundle.py", ["--mode", "portable_bundle_only"]),
    "task_limited": ("export_fork.py", ["--format", "coach-handoff"]),
    "capability": ("export_capability.py", []),
    "emulation": ("export_emulation_bundle.py", ["--mode", "portable_bundle_only"]),
}

EXPORT_CLASS_UNSUPPORTED: dict[str, str] = {
    "internal": "not exportable by definition — internal-only content stays in the governed Record",
}

ALL_EXPORT_CLASSES = sorted(set(EXPORT_CLASS_ROUTES) | set(EXPORT_CLASS_UNSUPPORTED))


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
    Options: -u/--user and --export-class (only before subcommand).
    Then: SUBCOMMAND [--] [child args...]
    If ``--`` is present, only tokens after it go to the child; else all tokens
    after subcommand go to the child. Inject -u when child argv has no user flag.
    """
    i = 0
    explicit_user: str | None = None
    export_class: str | None = None
    while i < len(argv):
        if argv[i] in ("-u", "--user"):
            if i + 1 >= len(argv):
                print("export.py: -u requires a value", file=sys.stderr)
                sys.exit(2)
            explicit_user = argv[i + 1]
            i += 2
            continue
        if argv[i] == "--export-class":
            if i + 1 >= len(argv):
                print("export.py: --export-class requires a value", file=sys.stderr)
                sys.exit(2)
            export_class = argv[i + 1]
            i += 2
            continue
        break

    if export_class is not None:
        rest = argv[i:]
        if rest and rest[0] == "--":
            child = list(rest[1:])
        else:
            child = list(rest)
        resolved = explicit_user or _default_user_id()
        if not _argv_has_user_flag(child):
            child = ["-u", resolved] + child
        return explicit_user, f"__class__{export_class}", child

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
    classes = ", ".join(ALL_EXPORT_CLASSES)
    print(
        f"""usage: python scripts/export.py [-u USER] {{fork|prp|identity|manifest|bundle|emulation|all}} [-- EXTRA...]
       python scripts/export.py [-u USER] --export-class {{tool_bootstrap|full|task_limited|capability|emulation}} [-- EXTRA...]

Unified export CLI — runs the existing script under scripts/ via subprocess.
Resolved default user when the child argv has no -u: GRACE_MAR_USER_ID, else {du!r} (repo heuristic).

Subcommands:
  fork      -> export_fork.py
  prp       -> export_prp.py
  identity  -> export_user_identity.py
  manifest  -> export_manifest.py
  bundle    -> export_runtime_bundle.py
  emulation -> export_emulation_bundle.py
  all       -> export_runtime_bundle.py (G1: same as bundle)

Export classes (--export-class):
  tool_bootstrap  -> export_prp.py (compact prompt for bootstrapping a new tool)
  full            -> export_runtime_bundle.py --mode portable_bundle_only (broad governed profile)
  task_limited    -> export_fork.py --format coach-handoff (filtered for a specific role)
  capability      -> export_capability.py (SKILLS + EVIDENCE portfolio with rationale companions)
  emulation       -> export_emulation_bundle.py --mode portable_bundle_only (runtime-ready composition over existing exports)
  internal        -> not exportable by definition

Known classes: {classes}

Examples:
  python scripts/export.py fork -- -o out.json
  python scripts/export.py --export-class tool_bootstrap -- -o prompt.txt
  python scripts/export.py --export-class full -- -o /tmp/bundle
  python scripts/export.py -u grace-mar --export-class task_limited -- -o handoff.json
  python scripts/export.py --export-class emulation -- -o /tmp/emulation-bundle

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

    if sub.startswith("__class__"):
        cls_name = sub[len("__class__"):]
        if cls_name in EXPORT_CLASS_UNSUPPORTED:
            reason = EXPORT_CLASS_UNSUPPORTED[cls_name]
            print(f"export.py: export class {cls_name!r} is {reason}.", file=sys.stderr)
            return 2
        if cls_name not in EXPORT_CLASS_ROUTES:
            print(
                f"export.py: unknown export class {cls_name!r}. "
                f"Known classes: {', '.join(ALL_EXPORT_CLASSES)}",
                file=sys.stderr,
            )
            return 2
        script, extra_args = EXPORT_CLASS_ROUTES[cls_name]
        return _run_child(script, extra_args + child_argv)

    if sub == "__missing__":
        print(
            "export.py: subcommand or --export-class required.\n"
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
