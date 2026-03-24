#!/usr/bin/env python3
"""
Promote reviewed lens memos from analysis/pending/ to analysis/.

Requires review_status: approved in the memo frontmatter.
Lens → filename: civ-mem → *-civmem-analysis.md, psy-hist → *-psy-hist-analysis.md

Usage:
    python3 scripts/work_jiang/promote_reviewed_memo.py --id civ-21 --lens civ-mem
    python3 scripts/work_jiang/promote_reviewed_memo.py --id geo-12 --lens psy-hist --force
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

_WJ = Path(__file__).resolve().parent
ROOT = _WJ.parent.parent

WORK_JIANG = ROOT / "research" / "external" / "work-jiang"
PENDING_DIR = WORK_JIANG / "analysis" / "pending"
ANALYSIS_DIR = WORK_JIANG / "analysis"
SOURCES_YAML = WORK_JIANG / "metadata" / "sources.yaml"

LENS_TO_SUFFIX = {"civ-mem": "civmem", "psy-hist": "psy-hist"}


def load_sources() -> list[dict]:
    if not SOURCES_YAML.exists():
        return []
    with SOURCES_YAML.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return (data or {}).get("sources", [])


def resolve_source(source_id: str) -> dict | None:
    for s in load_sources():
        if s.get("source_id") == source_id:
            return s
    return None


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body)."""
    if not content.strip().startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        fm = {}
    return fm, parts[2].lstrip("\n")


def has_approved(fm: dict, body: str) -> bool:
    if (fm.get("review_status") or "").strip().lower() == "approved":
        return True
    if "review_status: approved" in body[:2000]:
        return True
    return False


def normalize_frontmatter(fm: dict, source: dict) -> dict:
    out = dict(fm)
    out["analysis_id"] = source["source_id"]
    out["video_id"] = source.get("video_id") or ""
    out["source_id"] = source["source_id"]
    out["canonical_url"] = source.get("canonical_url") or (
        f"https://www.youtube.com/watch?v={out['video_id']}" if out["video_id"] else ""
    )
    out["series"] = source.get("series") or ""
    out["episode"] = source.get("episode") or 0
    out["status"] = "complete"
    out["review_status"] = "approved"
    return out


def serialize_frontmatter(fm: dict) -> str:
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"


def promote(source_id: str, lens: str, force: bool) -> int:
    suffix = LENS_TO_SUFFIX.get(lens)
    if not suffix:
        print(f"❌ Invalid --lens: {lens} (use civ-mem or psy-hist)", file=sys.stderr)
        return 1

    source = resolve_source(source_id)
    if not source:
        print(f"❌ Source not found: {source_id}", file=sys.stderr)
        return 1

    pending_path = PENDING_DIR / f"{source_id}-{suffix}-analysis.md"
    target_path = ANALYSIS_DIR / f"{source_id}-{suffix}-analysis.md"

    if not pending_path.exists():
        print(f"❌ Not found in pending: {pending_path}", file=sys.stderr)
        return 1

    if target_path.exists() and not force:
        print(f"❌ Target exists: {target_path}. Use --force to overwrite.", file=sys.stderr)
        return 1

    content = pending_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    if not has_approved(fm, body):
        print("❌ Set review_status: approved in the memo first.", file=sys.stderr)
        return 1

    fm_norm = normalize_frontmatter(fm, source)
    new_content = serialize_frontmatter(fm_norm) + body

    target_path.write_text(new_content, encoding="utf-8")
    pending_path.unlink()

    print(f"✅ Promoted {source_id} ({lens}) → {target_path}")

    # Run build_source_registry and rebuild_all
    for cmd in [
        [sys.executable, str(ROOT / "scripts/work_jiang/build_source_registry.py")],
        [sys.executable, str(ROOT / "scripts/work_jiang/rebuild_all.py")],
    ]:
        print(f"   Running: {' '.join(cmd)}")
        r = subprocess.run(cmd, cwd=str(ROOT))
        if r.returncode != 0:
            print(f"   Warning: command exited {r.returncode}", file=sys.stderr)

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote reviewed lens memo to analysis/")
    parser.add_argument("--id", required=True, help="Source ID, e.g. civ-21, geo-12")
    parser.add_argument("--lens", required=True, choices=["civ-mem", "psy-hist"], help="Lens type")
    parser.add_argument("--force", action="store_true", help="Overwrite existing target")
    args = parser.parse_args()
    return promote(args.id, args.lens, args.force)


if __name__ == "__main__":
    raise SystemExit(main())
