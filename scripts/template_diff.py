#!/usr/bin/env python3
"""
Compare grace-mar with companion-self on template paths. skill-work-companion-self Phase 1.

Reports: (a) what template has that instance lacks (pull needed); (b) what instance has diverged.
Does NOT overwrite anything. Per MERGING-FROM-COMPANION-SELF §4.

Uses grace-mar MERGING-FROM-COMPANION-SELF paths by default. Use --use-manifest to load
paths from companion-self template-manifest.json (companion-self canonical paths).

Usage:
    python scripts/template_diff.py
    python scripts/template_diff.py --companion-self /path/to/companion-self
    python scripts/template_diff.py --instance /path/to/grace-mar --brief
    python scripts/template_diff.py --use-manifest -o audit-report.md
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Grace-mar MERGING-FROM-COMPANION-SELF §1 (instance expects these paths)
TEMPLATE_FILES_GRACE_MAR = [
    "docs/conceptual-framework.md",
    "docs/architecture.md",
    "docs/identity-fork-protocol.md",
    "docs/self-template.md",
    "docs/skills-template.md",
    "docs/evidence-template.md",
    "docs/memory-template.md",
    "agents.md",
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

    # docs/skill-work/ recursively
    t_skill = set(str(p) for p in _skill_work_files(companion_self_root))
    i_skill = set(str(p) for p in _skill_work_files(instance_root))
    all_skill = t_skill | i_skill
    for rel in sorted(all_skill):
        t = companion_self_root / rel
        i = instance_root / rel
        status = _compare_file(t, i)
        result[status].append(rel)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare grace-mar with companion-self on template paths. skill-work-companion-self Phase 1."
    )
    parser.add_argument(
        "--companion-self",
        "-c",
        type=Path,
        default=Path("/tmp/companion-self"),
        help="Path to companion-self repo (cloned if missing)",
    )
    parser.add_argument("--instance", "-i", type=Path, default=REPO_ROOT, help="Path to grace-mar (instance) repo")
    parser.add_argument("--clone", action="store_true", default=True, help="Clone companion-self if missing (default: True)")
    parser.add_argument("--no-clone", action="store_false", dest="clone", help="Do not clone; fail if companion-self missing")
    parser.add_argument("--use-manifest", "-m", action="store_true", help="Use companion-self template-manifest.json paths")
    parser.add_argument("--brief", "-b", action="store_true", help="Brief output (counts only)")
    parser.add_argument("--output", "-o", type=Path, help="Write report to file")
    args = parser.parse_args()

    cs_root = args.companion_self
    if args.clone and not cs_root.exists():
        cs_root = _ensure_companion_self(cs_root)
    elif not cs_root.exists():
        print("Error: companion-self not found at", cs_root, file=sys.stderr)
        sys.exit(1)

    result = run_diff(cs_root, args.instance, use_manifest=args.use_manifest, brief=args.brief)

    out_lines: list[str] = []

    def emit(s: str = "") -> None:
        out_lines.append(s)

    if args.brief:
        emit("same: " + str(len(result["same"])))
        emit("differ: " + str(len(result["differ"])))
        emit("only_template (pull needed): " + str(len(result["only_template"])))
        emit("only_instance (instance additions): " + str(len(result["only_instance"])))
        out = "\n".join(out_lines)
        if args.output:
            args.output.write_text(out)
        print(out)
        return

    emit("## skill-work-companion-self — Template Diff Report")
    emit()
    emit("Companion-self: " + str(cs_root))
    emit("Instance (grace-mar): " + str(args.instance))
    emit("Paths: " + ("companion-self template-manifest.json" if args.use_manifest else "grace-mar MERGING-FROM-COMPANION-SELF"))
    emit()

    if result["only_template"]:
        emit("### Pull needed (in template, not in instance)")
        for p in result["only_template"]:
            emit("  - " + p)
        emit()

    if result["differ"]:
        emit("### Differ (both exist, content differs)")
        for p in result["differ"]:
            emit("  - " + p)
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

    emit("Summary: same=%d differ=%d only_template=%d only_instance=%d" % (
        len(result["same"]),
        len(result["differ"]),
        len(result["only_template"]),
        len(result["only_instance"]),
    ))

    out = "\n".join(out_lines)
    if args.output:
        args.output.write_text(out)
    print(out)


if __name__ == "__main__":
    main()
