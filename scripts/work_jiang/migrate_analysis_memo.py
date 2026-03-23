#!/usr/bin/env python3
"""
Lazy migration for analysis memos / sidecar JSON (memo_format_version / schema_version).

v1 -> v2: currently no structural change; ensures keys exist and bumps version fields.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def _major(ver: str) -> int:
    try:
        return int(str(ver).strip().split(".")[0])
    except (ValueError, IndexError):
        return 1


def _norm_schema_to(v_to: str) -> str:
    v = str(v_to).strip()
    if v == "2":
        return "2.0"
    return v


def migrate_json(path: Path, *, dry_run: bool, v_from: str, v_to: str) -> bool:
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    ver = str(data.get("schema_version") or data.get("analysis_json_version") or "1.0")
    target_maj = _major(v_to)
    if _major(ver) >= target_maj:
        print(f"skip (already >= {v_to}): {path} (schema_version={ver})")
        return False
    if _major(ver) < _major(v_from):
        print(f"skip (below --from): {path} (schema_version={ver})")
        return False
    target = _norm_schema_to(v_to)
    data["schema_version"] = target
    if "analysis_json_version" in data:
        data["analysis_json_version"] = target
    # v1 -> v2: ensure optional top-level keys exist for downstream tools
    for k in REQUIRED_V2_KEYS:
        data.setdefault(k, [])
    if not isinstance(data.get("summary"), str):
        data["summary"] = str(data.get("summary") or "")
    if dry_run:
        print(f"would migrate: {path}")
        return True
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"migrated: {path}")
    return True


REQUIRED_V2_KEYS = (
    "key_claims",
    "predictions",
    "divergences_from_prior",
    "open_questions",
    "cross_links",
)


def migrate_md(path: Path, *, dry_run: bool, v_from: str, v_to: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        print(f"skip (no front matter): {path}")
        return False
    end = text.find("\n---\n", 3)
    if end == -1:
        return False
    raw_fm = text[4:end]
    body = text[end + 5 :]
    try:
        fm = yaml.safe_load(raw_fm) or {}
    except yaml.YAMLError:
        return False
    v = str(fm.get("memo_format_version") or "1")
    if v != str(v_from):
        print(f"skip memo_format_version={v} (want {v_from}): {path}")
        return False
    try:
        fm["memo_format_version"] = int(float(str(v_to)))
    except ValueError:
        fm["memo_format_version"] = v_to
    if dry_run:
        print(f"would migrate md: {path}")
        return True
    new_head = "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n"
    path.write_text(new_head + body, encoding="utf-8")
    print(f"migrated md: {path}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from", dest="v_from", default="1")
    parser.add_argument("--to", dest="v_to", default="2")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("paths", nargs="*", type=Path, help="Files or directories")
    args = parser.parse_args()

    targets: list[Path] = []
    for p in args.paths:
        if p.is_dir():
            targets.extend(p.rglob("*.json"))
            targets.extend(p.rglob("*-analysis.md"))
        else:
            targets.append(p)

    n = 0
    for p in targets:
        if not p.exists():
            continue
        if p.suffix == ".json" and "analysis" in p.name:
            if migrate_json(p, dry_run=args.dry_run, v_from=args.v_from, v_to=args.v_to):
                n += 1
        elif p.suffix == ".md" and "analysis" in p.name:
            if migrate_md(p, dry_run=args.dry_run, v_from=args.v_from, v_to=args.v_to):
                n += 1

    print(f"done; touched {n} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
