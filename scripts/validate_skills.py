#!/usr/bin/env python3
"""
Validate skill metadata across .cursor/skills/ and skills-portable/.

Template-portable (companion-self + grace-mar). Read-only unless --fix is used.

Usage:
  python3 scripts/validate_skills.py
  python3 scripts/validate_skills.py --json
  python3 scripts/validate_skills.py --fix
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FRONTMATTER = {"name", "description"}
PORTABLE_REQUIRED = {"portable", "version"}

CURSOR_SKILLS_DIR = ".cursor/skills"
PORTABLE_SKILLS_DIR = "skills-portable"
MANIFEST_FILE = "skills-portable/manifest.yaml"


def _parse_frontmatter(path: Path) -> dict[str, Any] | None:
    """Extract YAML frontmatter from a SKILL.md file."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    if not text.startswith("---"):
        return None

    end = text.find("---", 3)
    if end < 0:
        return None

    block = text[3:end].strip()
    result: dict[str, Any] = {}
    for line in block.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip("'\"")
        if val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            result[key] = items
        elif val.lower() == "true":
            result[key] = True
        elif val.lower() == "false":
            result[key] = False
        else:
            result[key] = val
    return result


def _load_manifest_names() -> set[str]:
    """Load skill names from the portable manifest YAML."""
    manifest_path = REPO_ROOT / MANIFEST_FILE
    if not manifest_path.exists():
        return set()
    text = manifest_path.read_text(encoding="utf-8")
    names: set[str] = set()
    for m in re.finditer(r"^\s*-\s*name:\s*(.+)$", text, re.MULTILINE):
        names.add(m.group(1).strip())
    return names


def _cursor_skill_dirs() -> list[Path]:
    """List all skill directories under .cursor/skills/."""
    base = REPO_ROOT / CURSOR_SKILLS_DIR
    if not base.exists():
        return []
    return sorted(d for d in base.iterdir() if d.is_dir() and (d / "SKILL.md").exists())


def _portable_skill_dirs() -> list[Path]:
    """List all skill directories under skills-portable/ (excluding _ prefixed)."""
    base = REPO_ROOT / PORTABLE_SKILLS_DIR
    if not base.exists():
        return []
    return sorted(
        d for d in base.iterdir()
        if d.is_dir() and not d.name.startswith("_") and (d / "SKILL.md").exists()
    )


def _all_cursor_skill_names() -> set[str]:
    """Collect all skill directory names under .cursor/skills/."""
    base = REPO_ROOT / CURSOR_SKILLS_DIR
    if not base.exists():
        return set()
    return {d.name for d in base.iterdir() if d.is_dir() and (d / "SKILL.md").exists()}


def validate(*, verbose: bool = False) -> list[dict[str, str]]:
    """Run all checks. Returns list of {path, level, message} dicts."""
    errors: list[dict[str, str]] = []
    known_skill_names = _all_cursor_skill_names()

    for skill_dir in _cursor_skill_dirs():
        skill_path = skill_dir / "SKILL.md"
        rel = str(skill_path.relative_to(REPO_ROOT))
        fm = _parse_frontmatter(skill_path)

        if fm is None:
            errors.append({"path": rel, "level": "error", "message": "Missing or unparseable frontmatter"})
            continue

        for field in REQUIRED_FRONTMATTER:
            if field not in fm or not fm[field]:
                errors.append({"path": rel, "level": "error", "message": f"Missing required field: {field}"})

        if fm.get("name") and fm["name"] != skill_dir.name:
            errors.append({
                "path": rel, "level": "warn",
                "message": f"name '{fm['name']}' does not match directory '{skill_dir.name}'"
            })

        requires = fm.get("requires")
        if isinstance(requires, list):
            for dep in requires:
                if dep not in known_skill_names:
                    errors.append({
                        "path": rel, "level": "error",
                        "message": f"requires '{dep}' but no .cursor/skills/{dep}/ exists"
                    })

    manifest_names = _load_manifest_names()
    for skill_dir in _portable_skill_dirs():
        skill_path = skill_dir / "SKILL.md"
        rel = str(skill_path.relative_to(REPO_ROOT))
        fm = _parse_frontmatter(skill_path)

        if fm is None:
            errors.append({"path": rel, "level": "error", "message": "Missing or unparseable frontmatter"})
            continue

        for field in REQUIRED_FRONTMATTER | PORTABLE_REQUIRED:
            if field not in fm or (fm[field] == "" if isinstance(fm[field], str) else fm[field] is None):
                errors.append({"path": rel, "level": "error", "message": f"Missing required portable field: {field}"})

        if fm.get("portable") is not True:
            errors.append({"path": rel, "level": "error", "message": "portable: must be true for skills in skills-portable/"})

        if skill_dir.name not in manifest_names:
            errors.append({"path": rel, "level": "warn", "message": f"'{skill_dir.name}' not listed in {MANIFEST_FILE}"})

    for name in manifest_names:
        source_dir = REPO_ROOT / PORTABLE_SKILLS_DIR / name
        if not (source_dir / "SKILL.md").exists():
            errors.append({
                "path": MANIFEST_FILE, "level": "error",
                "message": f"Manifest lists '{name}' but {PORTABLE_SKILLS_DIR}/{name}/SKILL.md does not exist"
            })

    return errors


def format_text(errors: list[dict[str, str]]) -> str:
    if not errors:
        return "All skills valid."
    lines = []
    for e in errors:
        marker = "ERROR" if e["level"] == "error" else "WARN"
        lines.append(f"[{marker}] {e['path']}: {e['message']}")
    lines.append(f"\n{len(errors)} issue(s) found.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skill metadata.")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--fix", action="store_true", help="Interactive fix mode (not yet implemented)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.fix:
        print("--fix mode is not yet implemented. Run without --fix to see issues.")
        return 1

    errors = validate(verbose=args.verbose)

    if args.json:
        print(json.dumps(errors, indent=2))
    else:
        print(format_text(errors))

    error_count = sum(1 for e in errors if e["level"] == "error")
    return 1 if error_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
