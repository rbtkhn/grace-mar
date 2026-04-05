#!/usr/bin/env python3
"""
Compare grace-mar with companion-self on template paths. work-companion-self Phase 1.

Reports: (a) what template has that instance lacks (pull needed); (b) what instance has diverged.
Does NOT overwrite anything. Per MERGING-FROM-COMPANION-SELF §4.

Paths listed in `docs/skill-work/work-companion-self/expected-template-drift.json` are
reported under **Expected drift** and omitted from the actionable **differ** bucket.

Uses grace-mar MERGING-FROM-COMPANION-SELF paths by default. Use --use-manifest to load
exact paths from companion-self template-manifest.json. Add --include-skill-work when you
explicitly want the broader docs/skill-work recursive audit.

Usage:
    python scripts/template_diff.py
    python scripts/template_diff.py --companion-self /path/to/companion-self
    GRACE_MAR_COMPANION_SELF=/path/to/repo python scripts/template_diff.py
    python scripts/template_diff.py --instance /path/to/grace-mar --brief
    python scripts/template_diff.py --use-manifest -o audit-report.md
    python scripts/template_diff.py --use-manifest --include-skill-work -o audit-report.md
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _default_companion_self_root() -> Path:
    """Prefer GRACE_MAR_COMPANION_SELF, else repo-local companion-self/ (see docs/merging-from-companion-self.md §0)."""
    env = os.environ.get("GRACE_MAR_COMPANION_SELF", "").strip()
    if env:
        return Path(env).expanduser().resolve()
    return REPO_ROOT / "companion-self"

# Grace-mar MERGING-FROM-COMPANION-SELF §1 (instance expects these paths)
TEMPLATE_FILES_GRACE_MAR = [
    "docs/conceptual-framework.md",
    "docs/architecture.md",
    "docs/identity-fork-protocol.md",
    "docs/self-template.md",
    "docs/skills-template.md",
    "docs/evidence-template.md",
    "docs/memory-template.md",
    "AGENTS.md",
]


def _skill_work_files(root: Path) -> list[Path]:
    """List .md and .yaml files under docs/skill-work/ (relative to root)."""
    skill_work = root / "docs" / "skill-work"
    if not skill_work.exists():
        return []
    out: list[Path] = []
    for p in skill_work.rglob("*"):
        if p.is_file() and p.suffix in (".md", ".yaml", ".txt"):
            out.append(p.relative_to(root))
    return sorted(out)


def _ensure_companion_self(path: Path) -> Path:
    """If path doesn't exist, clone companion-self. Returns path."""
    if path.exists():
        return path
    print("Cloning companion-self to", path, "...", file=sys.stderr)
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["git", "clone", "--depth", "1", "https://github.com/rbtkhn/companion-self.git", str(path)],
        check=True,
        capture_output=True,
    )
    return path


def _compare_file(template_path: Path, instance_path: Path) -> str:
    """Returns: same | differ | only_template | only_instance."""
    t_exists = template_path.exists()
    i_exists = instance_path.exists()
    if not t_exists and not i_exists:
        return "both_missing"  # shouldn't happen
    if not t_exists:
        return "only_instance"
    if not i_exists:
        return "only_template"
    t_content = template_path.read_bytes()
    i_content = instance_path.read_bytes()
    return "same" if t_content == i_content else "differ"


def _load_expected_drift(instance_root: Path) -> dict[str, str]:
    """
    Paths documented as intentionally not byte-identical to the template.
    Relative paths like docs/identity-fork-protocol.md -> human reason string.
    """
    p = instance_root / "docs/skill-work/work-companion-self/expected-template-drift.json"
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        raw = data.get("paths") or {}
        out: dict[str, str] = {}
        for key, val in raw.items():
            if not isinstance(key, str):
                continue
            if isinstance(val, dict):
                reason = val.get("reason") or val.get("merging_pointer") or ""
            else:
                reason = str(val)
            out[key] = reason.strip() or "(see expected-template-drift.json)"
        return out
    except (json.JSONDecodeError, TypeError):
        return {}


def _load_manifest_paths(companion_self_root: Path) -> list[str]:
    """Load paths from companion-self template-manifest.json if present."""
    manifest = companion_self_root / "template-manifest.json"
    if not manifest.exists():
        return []
    try:
        data = json.loads(manifest.read_text())
        paths = data.get("paths") or []
        return [p["path"] for p in paths if isinstance(p.get("path"), str)]
    except (json.JSONDecodeError, KeyError):
        return []


def run_diff(
    companion_self_root: Path,
    instance_root: Path,
    use_manifest: bool = False,
    include_skill_work: bool = False,
    brief: bool = False,
) -> dict[str, list[str]]:
    """Compare template paths. Returns {same, differ, only_template, only_instance} -> list of paths."""
    result: dict[str, list[str]] = {
        "same": [],
        "differ": [],
        "only_template": [],
        "only_instance": [],
    }

    if use_manifest:
        template_files = _load_manifest_paths(companion_self_root)
        if not template_files:
            template_files = TEMPLATE_FILES_GRACE_MAR
    else:
        template_files = TEMPLATE_FILES_GRACE_MAR

    for rel in template_files:
        t = companion_self_root / rel
        i = instance_root / rel
        status = _compare_file(t, i)
        result[status].append(rel)

    if include_skill_work:
        t_skill = set(str(p) for p in _skill_work_files(companion_self_root))
        i_skill = set(str(p) for p in _skill_work_files(instance_root))
        all_skill = t_skill | i_skill
        for rel in sorted(all_skill):
            t = companion_self_root / rel
            i = instance_root / rel
            status = _compare_file(t, i)
            result[status].append(rel)

    for key in result:
        result[key] = sorted(set(result[key]))

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare grace-mar with companion-self on template paths. work-companion-self Phase 1."
    )
    parser.add_argument(
        "--companion-self",
        "-c",
        type=Path,
        default=None,
        help=(
            "Path to companion-self repo (cloned if missing unless --no-clone). "
            "Default: $GRACE_MAR_COMPANION_SELF or ./companion-self under grace-mar root."
        ),
    )
    parser.add_argument("--instance", "-i", type=Path, default=REPO_ROOT, help="Path to grace-mar (instance) repo")
    parser.add_argument("--clone", action="store_true", default=True, help="Clone companion-self if missing (default: True)")
    parser.add_argument("--no-clone", action="store_false", dest="clone", help="Do not clone; fail if companion-self missing")
    parser.add_argument("--use-manifest", "-m", action="store_true", help="Use exact companion-self template-manifest.json paths")
    parser.add_argument(
        "--include-skill-work",
        action="store_true",
        help="Additionally compare docs/skill-work/ recursively in both repos",
    )
    parser.add_argument("--brief", "-b", action="store_true", help="Brief output (counts only)")
    parser.add_argument("--output", "-o", type=Path, help="Write report to file")
    args = parser.parse_args()

    cs_root = args.companion_self if args.companion_self is not None else _default_companion_self_root()
    if args.clone and not cs_root.exists():
        cs_root = _ensure_companion_self(cs_root)
    elif not cs_root.exists():
        print("Error: companion-self not found at", cs_root, file=sys.stderr)
        sys.exit(1)

    result = run_diff(
        cs_root,
        args.instance,
        use_manifest=args.use_manifest,
        include_skill_work=args.include_skill_work,
        brief=args.brief,
    )

    expected_map = _load_expected_drift(args.instance.resolve())
    differ_raw = list(result["differ"])
    expected_paths: list[tuple[str, str]] = []
    actionable_differ: list[str] = []
    for rel in differ_raw:
        if rel in expected_map:
            expected_paths.append((rel, expected_map[rel]))
        else:
            actionable_differ.append(rel)
    result["differ"] = sorted(actionable_differ)
    expected_paths.sort(key=lambda x: x[0])

    out_lines: list[str] = []

    def emit(s: str = "") -> None:
        out_lines.append(s)

    if args.brief:
        emit("same: " + str(len(result["same"])))
        emit("differ: " + str(len(result["differ"])))
        emit("expected_drift: " + str(len(expected_paths)))
        emit("only_template (pull needed): " + str(len(result["only_template"])))
        emit("only_instance (instance additions): " + str(len(result["only_instance"])))
        out = "\n".join(out_lines)
        if args.output:
            args.output.write_text(out)
        print(out)
        return

    emit("## work-companion-self — Template Diff Report")
    emit()
    emit("Companion-self: " + str(cs_root))
    emit("Instance (grace-mar): " + str(args.instance))
    path_scope = "companion-self template-manifest.json" if args.use_manifest else "grace-mar MERGING-FROM-COMPANION-SELF"
    if args.include_skill_work:
        path_scope += " + docs/skill-work recursive"
    emit("Paths: " + path_scope)
    emit()

    if result["only_template"]:
        emit("### Pull needed (in template, not in instance)")
        for p in result["only_template"]:
            emit("  - " + p)
        emit()

    if result["differ"]:
        emit("### Differ (both exist, content differs — review)")
        for p in result["differ"]:
            emit("  - " + p)
        emit()

    if expected_paths:
        emit("### Expected drift (policy-documented; not a parity defect)")
        for p, reason in expected_paths:
            emit("  - **" + p + "** — " + reason)
        emit()
        emit(
            "Machine list: `docs/skill-work/work-companion-self/expected-template-drift.json`"
        )
        emit()

    if result["only_instance"]:
        emit("### Instance additions (in instance, not in template)")
        for p in result["only_instance"]:
            emit("  - " + p)
        emit()

    if result["same"]:
        emit("### Same (no action)")
        for p in result["same"][:15]:
            emit("  - " + p)
        if len(result["same"]) > 15:
            emit("  ... and " + str(len(result["same"]) - 15) + " more")
        emit()

    emit(
        "Summary: same=%d differ=%d expected_drift=%d only_template=%d only_instance=%d"
        % (
            len(result["same"]),
            len(result["differ"]),
            len(expected_paths),
            len(result["only_template"]),
            len(result["only_instance"]),
        )
    )

    out = "\n".join(out_lines)
    if args.output:
        args.output.write_text(out)
    print(out)


if __name__ == "__main__":
    main()
