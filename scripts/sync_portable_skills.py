#!/usr/bin/env python3
"""
Assemble .cursor/skills/*/SKILL.md from skills-portable/*/SKILL.md + optional CURSOR_APPENDIX.md.

Usage:
    python3 scripts/sync_portable_skills.py
    python3 scripts/sync_portable_skills.py --dry-run
    python3 scripts/sync_portable_skills.py --verify
    python3 scripts/sync_portable_skills.py --skill massie-x-news-search-draft
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
_MANIFEST = _REPO / "skills-portable" / "manifest.yaml"
_GENERATOR = "sync_portable_skills.py"


def _load_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore
    except ImportError:
        print("PyYAML required: pip install pyyaml", file=sys.stderr)
        sys.exit(1)
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}, text
    raw = m.group(1)
    body = text[m.end() :]
    try:
        import yaml  # type: ignore

        meta = yaml.safe_load(raw)
        return (meta if isinstance(meta, dict) else {}), body
    except Exception as e:
        print(f"YAML frontmatter parse error: {e}", file=sys.stderr)
        sys.exit(1)


def _dump_frontmatter(meta: dict) -> str:
    import yaml  # type: ignore

    # Wide width so `description` stays one physical line (hosts break on wrapped YAML).
    s = yaml.dump(
        meta,
        default_flow_style=False,
        sort_keys=False,
        allow_unicode=True,
        width=2000,
    ).rstrip()
    return f"---\n{s}\n---\n"


def _verify_skill(portable_body: str, forbidden: list[str], skill_name: str) -> list[str]:
    errs: list[str] = []
    for sub in forbidden:
        if sub in portable_body:
            errs.append(f"{skill_name}: portable body must not contain {sub!r}")
    return errs


def _verify_description_one_line(meta: dict, skill_name: str) -> list[str]:
    errs: list[str] = []
    d = meta.get("description")
    if d is None:
        return [f"{skill_name}: missing description"]
    if not isinstance(d, str):
        return [f"{skill_name}: description must be a string"]
    if "\n" in d:
        errs.append(f"{skill_name}: description must be a single line (contains newline)")
    return errs


def sync_one(
    entry: dict,
    *,
    dry_run: bool,
    verify_only: bool,
) -> tuple[str, list[str]]:
    """Returns (status, errors). status in ok, skip, write."""
    name = entry.get("name")
    src_rel = entry.get("source")
    tgt_rel = entry.get("target")
    apx_rel = entry.get("appendix")
    forbidden = entry.get("verify_forbidden_substrings") or []

    if not name or not src_rel or not tgt_rel:
        return "skip", [f"bad manifest entry: {entry!r}"]

    src = _REPO / "skills-portable" / src_rel
    tgt = _REPO / tgt_rel
    apx = _REPO / apx_rel if apx_rel else None

    if not src.is_file():
        return "skip", [f"missing source {src}"]

    raw = src.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(raw)
    errs = _verify_description_one_line(meta, name)
    errs += _verify_skill(body, forbidden, name)
    if meta.get("portable") is not True:
        errs.append(f"{name}: portable: true required in source frontmatter")

    if verify_only:
        return ("ok" if not errs else "error"), errs

    if errs:
        return "error", errs

    meta_out = dict(meta)
    meta_out["portable_source"] = f"skills-portable/{src_rel}"
    meta_out["synced_by"] = _GENERATOR

    appendix_block = ""
    if apx and apx.is_file():
        apx_text = apx.read_text(encoding="utf-8").strip()
        appendix_block = f"\n\n## Cursor / grace-mar instance\n\n{apx_text}\n"
    elif apx_rel:
        appendix_block = f"\n\n## Cursor / grace-mar instance\n\n_(appendix missing: {apx_rel})_\n"

    out = _dump_frontmatter(meta_out) + body.lstrip("\n") + appendix_block

    if dry_run:
        print(f"[dry-run] would write {tgt} ({len(out)} bytes)")
        return "ok", []

    tgt.parent.mkdir(parents=True, exist_ok=True)
    tgt.write_text(out, encoding="utf-8")
    print(f"Wrote {tgt}")
    return "ok", []


def main() -> int:
    p = argparse.ArgumentParser(description="Assemble Cursor skills from skills-portable/.")
    p.add_argument("--dry-run", action="store_true", help="Print actions only")
    p.add_argument("--verify", action="store_true", help="Validate only; no writes")
    p.add_argument("--skill", metavar="NAME", help="Sync a single manifest name")
    args = p.parse_args()

    if not _MANIFEST.is_file():
        print(f"Missing {_MANIFEST}", file=sys.stderr)
        return 1

    data = _load_yaml(_MANIFEST)
    skills = data.get("skills") or []
    if not isinstance(skills, list):
        print("manifest skills: must be a list", file=sys.stderr)
        return 1

    all_errs: list[str] = []
    for entry in skills:
        if not isinstance(entry, dict):
            continue
        if args.skill and entry.get("name") != args.skill:
            continue
        status, errs = sync_one(entry, dry_run=args.dry_run, verify_only=args.verify)
        all_errs.extend(errs)
        if status == "error":
            for e in errs:
                print(e, file=sys.stderr)

    if all_errs:
        return 1
    if args.verify:
        print("verify: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
