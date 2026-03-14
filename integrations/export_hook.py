#!/usr/bin/env python3
"""
Unified export hook for downstream integrations.

Targets:
  openclaw    — Record → USER.md + manifest (OpenClaw session continuity)
  intersignal — Record → symbolic_identity.json + manifest (Familiar nodes, Mesh Cache)
  curriculum  — Record → curriculum_profile.json (adaptive curriculum engines)

Usage:
    python integrations/export_hook.py --target openclaw --user grace-mar
    python integrations/export_hook.py --target intersignal -u grace-mar -o ../intersignal-mesh/
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))
try:
    from export_runtime_bundle import export_runtime_bundle
except ImportError:
    from scripts.export_runtime_bundle import export_runtime_bundle


def _prepend_constitution_prefix(out_dir: Path) -> int:
    """
    Prepend machine-readable constitution summary to USER.md for OpenClaw.
    Advisory-only context for downstream agents; does not alter canonical Record.
    """
    user_md = out_dir / "USER.md"
    intent_json = out_dir / "intent_snapshot.json"
    if not user_md.exists() or not intent_json.exists():
        return 0
    try:
        intent = json.loads(intent_json.read_text(encoding="utf-8"))
    except Exception:
        return 0
    if not isinstance(intent, dict) or not intent.get("ok"):
        return 0
    goals = intent.get("goals") or {}
    rules = intent.get("tradeoff_rules") or []
    escalations = intent.get("escalation_rules") or []
    lines = [
        "## CONSTITUTIONAL CONTEXT (INTENT)",
        "",
        "Use these as alignment constraints for downstream reasoning.",
        f"- primary_goal: {goals.get('primary') or ''}",
        f"- secondary_goal: {goals.get('secondary') or ''}",
        f"- tertiary_goal: {goals.get('tertiary') or ''}",
        f"- tradeoff_rule_count: {len(rules)}",
    ]
    if rules:
        for rule in rules[:5]:
            lines.append(
                "- rule "
                f"{rule.get('id')}: prioritize={rule.get('prioritize') or ''}; "
                f"deprioritize={rule.get('deprioritize') or ''}; "
                f"applies_to={','.join(rule.get('applies_to') or ['all'])}; "
                f"strategy={rule.get('conflict_strategy') or 'escalate_to_human'}"
            )
    if escalations:
        lines.append(f"- escalation_rules: {len(escalations)}")
    lines.extend(["", "---", ""])
    prefix = "\n".join(lines)
    original = user_md.read_text(encoding="utf-8")
    if "## CONSTITUTIONAL CONTEXT (INTENT)" in original:
        return 0
    user_md.write_text(prefix + original, encoding="utf-8")
    return 0


def run_export(
    target: str,
    output_dir: Path | None,
    user_id: str = "grace-mar",
    openclaw_format: str = "md+manifest",
) -> int:
    scripts = REPO_ROOT / "scripts"
    profile_dir = REPO_ROOT / "users" / user_id
    out = output_dir or profile_dir

    if target == "openclaw":
        out.mkdir(parents=True, exist_ok=True)
        fmt = openclaw_format.strip().lower()
        bundle_dir = out / "runtime-bundle"
        export_runtime_bundle(
            user_id=user_id,
            output_dir=bundle_dir,
            runtime_mode="adjunct_runtime",
            include_user_json=(fmt == "json+md"),
        )
        copy_map = {}
        if fmt in {"md", "md+manifest", "json+md", "full-prp"}:
            copy_map[bundle_dir / "record" / "USER.md"] = out / "USER.md"
        if fmt in {"json+md"}:
            copy_map[bundle_dir / "record" / "USER.json"] = out / "USER.json"
        if fmt in {"md+manifest", "json+md", "full-prp"}:
            copy_map[bundle_dir / "policy" / "manifest.json"] = out / "manifest.json"
            copy_map[bundle_dir / "policy" / "llms.txt"] = out / "llms.txt"
        if fmt in {"md", "md+manifest", "json+md", "full-prp"}:
            copy_map[bundle_dir / "policy" / "intent_snapshot.json"] = out / "intent_snapshot.json"
        if fmt in {"full-prp"}:
            copy_map[bundle_dir / "record" / "grace-mar-llm.txt"] = out / "OPENCLAW-PRP.txt"
        if fmt in {"fork-json"}:
            copy_map[bundle_dir / "record" / "fork-export.json"] = out / "fork-export.json"

        for src, dst in copy_map.items():
            if not src.exists():
                print(f"Missing bundle file: {src}", file=sys.stderr)
                return 1
            dst.write_bytes(src.read_bytes())
        if fmt in {"md", "md+manifest", "json+md", "full-prp"}:
            _prepend_constitution_prefix(out)

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
    parser.add_argument("--user", "-u", default="grace-mar", help="User id")
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
