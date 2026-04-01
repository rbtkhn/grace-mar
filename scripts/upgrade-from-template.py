#!/usr/bin/env python3
"""Deterministic sync-pack upgrade path from companion-self template."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List


SYNC_PACK_FILES = [
    "README.md",
    "ENABLE-SYNC-PACK.md",
    "SYNC-CONTRACT.template.md",
    "SYNC-LOG.template.md",
    "SYNC-DAILY.template.md",
    "INITIAL-GOOD-MORNING.md",
]


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _repo_commit(repo_path: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_path), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def _template_source_base() -> dict:
    return {
        "schemaVersion": "1.1.0",
        "recordType": "templateAppliedProvenance",
        "companionSelfCommit": "",
        "templateVersion": "",
        "syncedAt": "",
        "syncedBy": "",
        "syncedPaths": [],
        "templateUpstream": {
            "repo": "https://github.com/rbtkhn/companion-self",
            "ref": "main",
        },
        "notes": (
            "Top-level fields describe the last applied template merge. "
            "Narrow auxiliary refreshes should append to auxiliarySyncEvents "
            "rather than replacing this baseline."
        ),
        "auxiliarySyncEvents": [],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Upgrade grace-mar sync-pack from companion-self.")
    ap.add_argument(
        "--template-root",
        default="../companion-self",
        help="Path to companion-self repository root.",
    )
    ap.add_argument("--dry-run", action="store_true", help="Show changes without writing files.")
    args = ap.parse_args()

    grace_root = Path.cwd().resolve()
    template_root = (grace_root / args.template_root).resolve()
    src_dir = template_root / "docs" / "skill-work" / "self-work" / "sync-pack"
    dst_dir = grace_root / "docs" / "skill-work" / "self-work" / "sync-pack"
    if not src_dir.exists():
        raise SystemExit(f"Template sync-pack not found: {src_dir}")
    if not dst_dir.exists():
        raise SystemExit(f"Destination sync-pack not found: {dst_dir}")

    copied: List[str] = []
    changed: List[str] = []
    for name in SYNC_PACK_FILES:
        src = src_dir / name
        dst = dst_dir / name
        if not src.exists():
            continue
        src_text = src.read_text(encoding="utf-8")
        dst_text = dst.read_text(encoding="utf-8") if dst.exists() else ""
        if src_text != dst_text:
            changed.append(name)
            if not args.dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
            copied.append(name)

    template_version = _read_json(template_root / "template-version.json").get("templateVersion", "")
    commit_hash = _repo_commit(template_root)
    source_payload = {
        "kind": "sync_pack_upgrade",
        "companionSelfCommit": commit_hash,
        "templateVersion": template_version,
        "syncedAt": datetime.now(timezone.utc).isoformat(),
        "syncedBy": "scripts/upgrade-from-template.py",
        "syncedPaths": [f"docs/skill-work/self-work/sync-pack/{name}" for name in changed],
    }
    if not args.dry_run and changed:
        template_source_path = grace_root / "template-source.json"
        existing = _read_json(template_source_path)
        merged = _template_source_base()
        merged.update(existing)
        merged.setdefault("templateUpstream", {"repo": "https://github.com/rbtkhn/companion-self", "ref": "main"})
        merged.setdefault("auxiliarySyncEvents", [])
        merged["auxiliarySyncEvents"] = list(merged.get("auxiliarySyncEvents") or [])
        merged["auxiliarySyncEvents"].append(source_payload)
        template_source_path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")

    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(f"{mode}: {len(changed)} sync-pack file(s) changed.")
    for name in changed:
        print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

