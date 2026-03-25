#!/usr/bin/env python3
"""
Validate work-dev control-plane YAML against JSON schemas and repo paths.

Usage:
  python scripts/work_dev/validate_control_plane.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

try:
    import jsonschema
except ImportError:
    jsonschema = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

FILES = (
    ("integration_status.yaml", "integration_status.schema.json", "items"),
    ("known_gaps.yaml", "known_gaps.schema.json", "items"),
    ("target_registry.yaml", "target_registry.schema.json", "segments"),
    ("proof_ledger.yaml", "proof_ledger.schema.json", "entries"),
)


def _skip_path_check(p: str) -> bool:
    s = p.replace("\\", "/")
    return "[" in s or "*" in s


def path_exists(repo_root: Path, rel: str) -> bool:
    rel = rel.replace("\\", "/")
    if "[" in rel or "*" in rel:
        return True
    p = repo_root / rel
    return p.is_file() or p.is_dir()


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate work-dev control plane YAML.")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args()
    root = args.repo_root.resolve()
    control_plane = root / "docs" / "skill-work" / "work-dev" / "control-plane"
    schema_dir = root / "schemas" / "work_dev"

    errors: list[str] = []
    integration_ids: set[str] = set()

    for yaml_name, schema_name, _ in FILES:
        ypath = control_plane / yaml_name
        spath = schema_dir / schema_name
        if not ypath.is_file():
            errors.append(f"missing {ypath.relative_to(root)}")
            continue
        if not spath.is_file():
            errors.append(f"missing schema {spath.relative_to(root)}")
            continue
        data = yaml.safe_load(ypath.read_text(encoding="utf-8"))
        schema = json.loads(spath.read_text(encoding="utf-8"))
        if jsonschema is not None:
            try:
                jsonschema.validate(instance=data, schema=schema)
            except jsonschema.ValidationError as e:
                errors.append(f"{yaml_name}: {e.message}")
        else:
            if not isinstance(data, dict) or data.get("version") != 1:
                errors.append(f"{yaml_name}: expected version 1 object")

    # Reload integration ids and cross-refs
    integ = yaml.safe_load((control_plane / "integration_status.yaml").read_text(encoding="utf-8"))
    for it in integ.get("items") or []:
        iid = it.get("id")
        if isinstance(iid, str):
            if iid in integration_ids:
                errors.append(f"duplicate integration id: {iid}")
            integration_ids.add(iid)
        for rel in it.get("source_of_truth") or []:
            if isinstance(rel, str) and not _skip_path_check(rel) and not path_exists(root, rel):
                errors.append(f"missing source_of_truth path: {rel}")

    gaps = yaml.safe_load((control_plane / "known_gaps.yaml").read_text(encoding="utf-8"))
    gap_ids: set[str] = set()
    for g in gaps.get("items") or []:
        gid = g.get("id")
        if isinstance(gid, str):
            if gid in gap_ids:
                errors.append(f"duplicate gap id: {gid}")
            gap_ids.add(gid)
        for rid in g.get("related_integration_ids") or []:
            if rid and rid not in integration_ids:
                errors.append(f"gap {gid} references unknown integration id: {rid}")

    tr = yaml.safe_load((control_plane / "target_registry.yaml").read_text(encoding="utf-8"))
    sids: set[str] = set()
    for seg in tr.get("segments") or []:
        sid = seg.get("id")
        if isinstance(sid, str):
            if sid in sids:
                errors.append(f"duplicate segment id: {sid}")
            sids.add(sid)

    pl = yaml.safe_load((control_plane / "proof_ledger.yaml").read_text(encoding="utf-8"))
    pids: set[str] = set()
    for e in pl.get("entries") or []:
        pid = e.get("id")
        if isinstance(pid, str):
            if pid in pids:
                errors.append(f"duplicate proof id: {pid}")
            pids.add(pid)

    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    if errors:
        print("validate_control_plane: FAILED", file=sys.stderr)
        return 1
    print("validate_control_plane: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
