#!/usr/bin/env python3
"""Update markdown links to use lowercase filenames after rename."""
from pathlib import Path
import re
import subprocess

REPO = Path(__file__).resolve().parent.parent


def get_rename_map():
    out = subprocess.run(
        ["git", "diff", "--name-status", "HEAD"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    renames = {}
    for line in out.stdout.strip().splitlines():
        if not line.startswith("R") or "\t" not in line:
            continue
        parts = line.split("\t", 2)
        if len(parts) < 3:
            old, new = parts[0].split(" -> ", 1) if " -> " in parts[0] else (parts[0], parts[1])
        else:
            _, old, new = parts[0], parts[1], parts[2]
        new = new.replace(".lc-tmp", "")  # in case any temp left
        if old != new and old:
            renames[old] = new
        # also map basename for link updates
        old_base = Path(old).name
        new_base = Path(new).name
        if old_base != new_base:
            renames[old_base] = new_base
    return renames


def main():
    renames = get_rename_map()
    # Sort by length descending so we replace longer (path) before shorter (basename)
    for old in sorted(renames.keys(), key=len, reverse=True):
        new = renames[old]
        if old == new:
            continue
        for md in REPO.rglob("*.md"):
            if ".git" in str(md) or "repos/" in str(md):
                continue
            try:
                text = md.read_text(encoding="utf-8")
            except Exception:
                continue
            if old in text:
                new_text = text.replace(old, new)
                if new_text != text:
                    md.write_text(new_text, encoding="utf-8")
                    print(f"Updated {md}: {old} -> {new}")


if __name__ == "__main__":
    main()
