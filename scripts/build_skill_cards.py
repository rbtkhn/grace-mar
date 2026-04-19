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


def _build_cmc_strategy_card(out_dir: Path, markdown: bool) -> bool:
    """Build THINK-CIVILIZATIONAL-STRATEGY card from CMC + strategy artifacts."""
    cmc_paths = (
        REPO_ROOT / "research" / "repos" / "civilization_memory",
        REPO_ROOT / "repos" / "civilization_memory",
        REPO_ROOT.parent / "civilization_memory",
    )
    import os

    env_path = os.getenv("CIVILIZATION_MEMORY_PATH", "").strip()
    if env_path:
        cmc_paths = (Path(env_path).resolve(),) + cmc_paths

    cmc_root = None
    for p in cmc_paths:
        if p.is_dir():
            cmc_root = p
            break

    strategy_surface = REPO_ROOT / "docs" / "skill-work" / "work-strategy" / "civilizational-strategy-surface.md"
    case_index = REPO_ROOT / "docs" / "skill-work" / "work-strategy" / "case-index.md"
    cmc_routing = REPO_ROOT / "docs" / "cmc-routing.md"

    primitives = []
    if cmc_root:
        content_dir = cmc_root / "content"
        if content_dir.is_dir():
            for scholar in sorted(content_dir.glob("**/*SCHOLAR*.md"))[:5]:
                rel = str(scholar.relative_to(cmc_root))
                primitives.append(f"SCHOLAR: {rel}")
            for template in sorted(content_dir.glob("**/CIV-MIND-*.md"))[:3]:
                rel = str(template.relative_to(cmc_root))
                primitives.append(f"CIV-MIND: {rel}")

    strategy_refs = []
    if strategy_surface.exists():
        strategy_refs.append(str(strategy_surface.relative_to(REPO_ROOT)))
    if case_index.exists():
        strategy_refs.append(str(case_index.relative_to(REPO_ROOT)))
    if cmc_routing.exists():
        strategy_refs.append(str(cmc_routing.relative_to(REPO_ROOT)))

    snippet = (
        "Civilizational strategy thinking surface: bridges CMC SCHOLAR ledgers, "
        "case-index families, and strategy-notebook judgment into reusable patterns. "
        "Lookup: python3 scripts/cmc_lookup.py. "
        "Ingest: python3 scripts/ingest_from_cmc.py. "
        "Lecture: python3 scripts/cmc_lecture_helper.py."
    )

    operator_lines = [
        "THINK-CIVILIZATIONAL-STRATEGY connects CMC primitives to operator strategy work:",
        "",
    ]
    if primitives:
        operator_lines.append("CMC primitives available:")
        for p in primitives:
            operator_lines.append(f"  - {p}")
        operator_lines.append("")
    if strategy_refs:
        operator_lines.append("Strategy surfaces:")
        for r in strategy_refs:
            operator_lines.append(f"  - {r}")
        operator_lines.append("")
    operator_lines.extend([
        "Scripts:",
        "  - scripts/cmc_lookup.py — CLI lookup with --civilization filter",
        "  - scripts/ingest_from_cmc.py — SCHOLAR to gate staging",
        "  - scripts/cmc_lecture_helper.py — lecture reflection + gate staging",
    ])

    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    card = {
        "skill_id": "THINK-CIVILIZATIONAL-STRATEGY",
        "title": "Civilizational Strategy (CIV-MEM bridge)",
        "purpose": "Bridge CMC SCHOLAR ledgers, case-index mechanisms, and strategy-notebook judgment into reusable civilizational patterns for work-strategy.",
        "runtime_snippet": _normalize_snippet(snippet),
        "operator_view": "\n".join(operator_lines),
        "source_path": "docs/skill-work/work-strategy/civilizational-strategy-surface.md",
        "last_updated": now,
        "card_type": "THINK-CIVILIZATIONAL-STRATEGY",
        "cmc_available": cmc_root is not None,
        "cmc_primitives": primitives,
        "strategy_refs": strategy_refs,
    }

    out_json = out_dir / "THINK-CIVILIZATIONAL-STRATEGY.json"
    out_json.write_text(json.dumps(card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if markdown:
        _write_markdown(card, out_dir / "THINK-CIVILIZATIONAL-STRATEGY.md")
    return True


def _validate_card(card: dict) -> list[str]:
    """Validate a card against the JSON schema. Returns list of error messages (empty = valid)."""
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        return ["jsonschema not installed; skipping validation"]
    if not SCHEMA_PATH.is_file():
        return [f"schema not found: {SCHEMA_PATH}"]
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [e.message for e in validator.iter_errors(card)]


def _completeness_score(card: dict) -> dict[str, bool]:
    """Check which quality fields are populated."""
    return {
        "has_purpose": bool(card.get("purpose") and card["purpose"] != "(no description in frontmatter)"),
        "has_snippet": bool(card.get("runtime_snippet")),
        "has_operator_view": bool(card.get("operator_view")),
        "has_source_path": bool(card.get("source_path")),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build derived skill card JSON/MD from portable skills.")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=REPO_ROOT / "artifacts" / "skill-cards",
        help="Output directory for *.json and *.md",
    )
    parser.add_argument("--markdown", action="store_true", help="Also write .md alongside .json")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate each card against skill-card.v1.json schema; exit 1 if any fail",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Print completeness report (purpose, snippet, operator_view coverage) as JSON",
    )
    args = parser.parse_args()

    rows = _load_manifest()
    if not rows:
        print("No skills in manifest.", file=sys.stderr)
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)

    cards: list[dict] = []
    validation_errors: dict[str, list[str]] = {}

    for row in rows:
        card = build_card_for_skill(row)
        cards.append(card)
        out_json = args.out_dir / f"{card['skill_id']}.json"
        out_json.write_text(json.dumps(card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.markdown:
            _write_markdown(card, args.out_dir / f"{card['skill_id']}.md")
        if args.check:
            errs = _validate_card(card)
            if errs:
                validation_errors[card["skill_id"]] = errs

    if _build_cmc_strategy_card(args.out_dir, args.markdown):
        print(f"Wrote {len(rows) + 1} skill card(s) to {args.out_dir} (including THINK-CIVILIZATIONAL-STRATEGY)", file=sys.stderr)
    else:
        print(f"Wrote {len(rows)} skill card(s) to {args.out_dir}", file=sys.stderr)

    if args.report:
        report_rows = []
        for card in cards:
            comp = _completeness_score(card)
            report_rows.append({"skill_id": card["skill_id"], **comp})
        total = len(report_rows)
        complete_count = sum(1 for r in report_rows if all(r[k] for k in r if k != "skill_id"))
        report = {
            "total_cards": total,
            "fully_complete": complete_count,
            "completeness_rate": round(complete_count / total, 4) if total > 0 else 0.0,
            "cards": report_rows,
        }
        print(json.dumps(report, indent=2))

    if args.check and validation_errors:
        print(f"\nSchema validation failed for {len(validation_errors)} card(s):", file=sys.stderr)
        for sid, errs in validation_errors.items():
            for e in errs:
                print(f"  {sid}: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
