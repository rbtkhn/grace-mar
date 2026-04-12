#!/usr/bin/env python3
"""
Emit derived skill cards (JSON + optional Markdown) from skills-portable + manifest.

Does not read generated .cursor/skills/*/SKILL.md — canonical source is portable SKILL.md.

Usage:
  python3 scripts/build_skill_cards.py
  python3 scripts/build_skill_cards.py --out-dir artifacts/skill-cards
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "skills-portable" / "manifest.yaml"
SCHEMA_PATH = REPO_ROOT / "schema-registry" / "skill-card.v1.json"
RUNTIME_SNIPPET_MAX = 800
OPERATOR_VIEW_MAX = 1200


def _load_manifest() -> list[dict]:
    try:
        import yaml  # type: ignore
    except ImportError:
        print("PyYAML required: pip install pyyaml", file=sys.stderr)
        sys.exit(1)
    raw = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    skills = raw.get("skills") if isinstance(raw, dict) else None
    if not isinstance(skills, list):
        return []
    return [s for s in skills if isinstance(s, dict)]


def _split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}, text
    body = text[m.end() :]
    try:
        import yaml  # type: ignore

        meta = yaml.safe_load(m.group(1))
        return (meta if isinstance(meta, dict) else {}), body
    except Exception:
        return {}, text


def _first_heading_title(body: str) -> str | None:
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# ") and not line.startswith("##"):
            return line[2:].strip()
    return None


def _normalize_snippet(s: str) -> str:
    s = re.sub(r"\s+", " ", s.strip())
    if len(s) > RUNTIME_SNIPPET_MAX:
        return s[: RUNTIME_SNIPPET_MAX - 1] + "…"
    return s


def _operator_view(appendix_rel: str | None, skill_id: str) -> str:
    if not appendix_rel:
        return f"See skills-portable/{skill_id}/SKILL.md (no appendix in manifest)."
    ap = REPO_ROOT / appendix_rel
    if not ap.exists():
        return f"Appendix missing at {appendix_rel}; see skills-portable/{skill_id}/SKILL.md."
    text = ap.read_text(encoding="utf-8").strip()
    if len(text) > OPERATOR_VIEW_MAX:
        return text[: OPERATOR_VIEW_MAX - 1] + "…"
    return text


def build_card_for_skill(row: dict) -> dict:
    name = str(row.get("name", "")).strip()
    source_rel = str(row.get("source", "")).strip()
    appendix_rel = str(row.get("appendix", "") or "").strip() or None
    if not name or not source_rel:
        raise ValueError(f"Invalid manifest row: {row!r}")

    if source_rel.startswith("skills-portable/"):
        portable = REPO_ROOT / source_rel
    else:
        portable = REPO_ROOT / "skills-portable" / source_rel
    if not portable.exists():
        raise FileNotFoundError(f"Portable skill not found: {portable}")

    text = portable.read_text(encoding="utf-8")
    meta, body = _split_frontmatter(text)
    purpose = str(meta.get("description", "")).strip() or "(no description in frontmatter)"
    title = _first_heading_title(body) or name
    snippet = _normalize_snippet(body)
    mtime = datetime.fromtimestamp(portable.stat().st_mtime, tz=timezone.utc)
    last_updated = mtime.strftime("%Y-%m-%dT%H:%M:%SZ")

    source_path = f"skills-portable/{name}/SKILL.md"

    return {
        "skill_id": name,
        "title": title,
        "purpose": purpose,
        "runtime_snippet": snippet,
        "operator_view": _operator_view(appendix_rel, name),
        "source_path": source_path,
        "last_updated": last_updated,
    }


def _write_markdown(card: dict, path: Path) -> None:
    lines = [
        f"# Skill card — {card['skill_id']}",
        "",
        f"**Title:** {card['title']}",
        "",
        f"**Purpose:** {card['purpose']}",
        "",
        "## Runtime snippet",
        "",
        card["runtime_snippet"],
        "",
        "## Operator view",
        "",
        card["operator_view"],
        "",
        f"**Canonical source:** `{card['source_path']}`",
        "",
        f"*last_updated: {card['last_updated']}*",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build derived skill card JSON/MD from portable skills.")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=REPO_ROOT / "artifacts" / "skill-cards",
        help="Output directory for *.json and *.md",
    )
    parser.add_argument("--markdown", action="store_true", help="Also write .md alongside .json")
    args = parser.parse_args()

    rows = _load_manifest()
    if not rows:
        print("No skills in manifest.", file=sys.stderr)
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)

    for row in rows:
        card = build_card_for_skill(row)
        out_json = args.out_dir / f"{card['skill_id']}.json"
        out_json.write_text(json.dumps(card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.markdown:
            _write_markdown(card, args.out_dir / f"{card['skill_id']}.md")

    print(f"Wrote {len(rows)} skill card(s) to {args.out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
