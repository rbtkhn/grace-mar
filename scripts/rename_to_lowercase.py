#!/usr/bin/env python3
"""
Rename all files in the repo to lowercase (for consistency).
Uses two-step git mv to handle case-insensitive filesystems (e.g. macOS).
Excludes: .git, repos/
"""
from pathlib import Path
import subprocess
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
EXCLUDE_PREFIXES = (".git/", "repos/")
SKIP_NAMES = (".ds_store",)  # skip untracked / ignore list


def git_tracked_files():
    out = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return set(out.stdout.strip().splitlines())


def main():
    tracked = git_tracked_files()
    to_rename = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(REPO_ROOT)
        except ValueError:
            continue
        rel_str = str(rel).replace("\\", "/")
        if rel_str not in tracked:
            continue
        if any(rel_str.startswith(p) for p in EXCLUDE_PREFIXES):
            continue
        if rel.name.lower() in SKIP_NAMES:
            continue
        if rel.name != rel.name.lower():
            new_name = rel.parent / rel.name.lower()
            if new_name != rel:
                to_rename.append((rel, new_name))

    if not to_rename:
        print("No files to rename.")
        return 0

    print(f"Will rename {len(to_rename)} files to lowercase.")
    # Phase 1: rename to temp (avoid case-insensitive collision)
    suffix = ".lc-tmp"
    for rel, new_rel in to_rename:
        old_path = REPO_ROOT / rel
        if not old_path.exists():
            print(f"Skip (gone): {rel}")
            continue
        tmp_path = REPO_ROOT / (str(rel) + suffix)
        try:
            subprocess.run(
                ["git", "mv", str(rel), str(tmp_path)],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Phase 1 failed for {rel}: {e.stderr.decode()}")
            return 1

    # Phase 2: rename temp to final lowercase
    for rel, new_rel in to_rename:
        tmp_path = REPO_ROOT / (str(rel) + suffix)
        if not tmp_path.exists():
            print(f"Skip tmp (gone): {tmp_path}")
            continue
        try:
            subprocess.run(
                ["git", "mv", str(tmp_path), str(new_rel)],
                cwd=REPO_ROOT,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            print(f"Phase 2 failed for {tmp_path} -> {new_rel}: {e.stderr.decode()}")
            return 1

    print("All renames done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
