#!/usr/bin/env python3
"""
Create a new governed instance directory tree from a companion-self template checkout.

This is not a substitute for ``git clone`` + remote setup; it copies a local template
root to a new folder and seeds ``users/<instance>/seed-phase/`` from
``users/_template/seed-phase/``.

**Warning:** Running with ``--template`` pointing at a private **instance** repo (e.g.
grace-mar with live ``users/<id>/``) may copy Record data. Prefer a clean **template**
checkout (companion-self) as ``--template``.

Usage:
  python3 scripts/companion_factory.py new my-instance \\
      --template /path/to/companion-self \\
      --output-dir /path/to/parent

Next step (printed after success):
  python3 scripts/validate-seed-phase.py users/<instance>/seed-phase --allow-placeholders
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def _default_copy_ignore(src: str, names: list[str]) -> set[str]:
    skip = {
        ".git",
        "__pycache__",
        ".venv",
        "venv",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "node_modules",
    }
    return {n for n in names if n in skip or n.endswith(".pyc")}


def cmd_new(instance_name: str, template: Path, output_dir: Path) -> int:
    if not instance_name.replace("-", "").replace("_", "").isalnum():
        print(
            "Instance name should be alphanumeric with optional - or _ only.",
            file=sys.stderr,
        )
        return 1

    dest = (output_dir / instance_name).resolve()
    if dest.exists():
        print(f"Already exists: {dest}", file=sys.stderr)
        return 1

    tpl = template.resolve()
    if not tpl.is_dir():
        print(f"Not a directory: {tpl}", file=sys.stderr)
        return 1

    tmpl_seed = tpl / "users" / "_template" / "seed-phase"
    if not tmpl_seed.is_dir():
        print(f"Missing template seed-phase scaffold: {tmpl_seed}", file=sys.stderr)
        return 1

    print(f"Copying template {tpl} -> {dest} (ignoring .git, venv, caches)...")
    shutil.copytree(tpl, dest, ignore=_default_copy_ignore)

    inst_seed = dest / "users" / instance_name / "seed-phase"
    inst_seed.mkdir(parents=True, exist_ok=True)

    for f in sorted(tmpl_seed.glob("*.json")):
        shutil.copy2(f, inst_seed / f.name)
    for name in ("README.md", "seed_dossier.md"):
        p = tmpl_seed / name
        if p.is_file():
            shutil.copy2(p, inst_seed / name)

    manifest_path = inst_seed / "seed-phase-manifest.json"
    if manifest_path.is_file():
        man = json.loads(manifest_path.read_text(encoding="utf-8"))
        man["user_slug"] = instance_name
        manifest_path.write_text(json.dumps(man, indent=2) + "\n", encoding="utf-8")

    ver = "unknown"
    tf = dest / "template-manifest.json"
    if tf.is_file():
        ver = str(json.loads(tf.read_text(encoding="utf-8")).get("templateVersion") or "unknown")

    meta = {
        "instance_id": instance_name,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "template_version": ver,
        "status": "seed-phase",
    }
    (dest / "instance-metadata.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    rel_seed = f"users/{instance_name}/seed-phase"
    print(f"Created instance at {dest}")
    print("Next:")
    print(f"  cd {dest}")
    print(f"  python3 scripts/validate-seed-phase.py {rel_seed} --allow-placeholders")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Companion factory — new instance from template directory.")
    sub = ap.add_subparsers(dest="command", required=True)

    new_p = sub.add_parser("new", help="Copy template to a new instance directory")
    new_p.add_argument("instance_name", help="New user id / folder name under users/")
    new_p.add_argument(
        "--template",
        type=Path,
        required=True,
        help="Root of companion-self (or template) checkout to copy from",
    )
    new_p.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Parent directory where <instance_name> will be created",
    )

    args = ap.parse_args()
    if args.command == "new":
        return cmd_new(args.instance_name, args.template, args.output_dir)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
