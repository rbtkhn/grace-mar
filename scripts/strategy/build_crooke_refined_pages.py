#!/usr/bin/env python3
"""Emit crooke-pages-manifest.yaml and scaffold crooke-page-*.md from Substack raw-input captures.

Run from repo root:
  python3 scripts/strategy/build_crooke_refined_pages.py

Scaffolds match docs/skill-work/work-strategy/strategy-notebook/refined-page-template.md
(Mode C — Substack; audit_refined_pages.py-friendly).

Idempotent: overwrites manifest; overwrites crooke-page files that still contain
<!-- SCOUT_REFINED_PAGE_SCAFFOLD --> (or use --force to overwrite all).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
RAW = NOTEBOOK / "raw-input"
CROOKE = NOTEBOOK / "experts" / "crooke"
MANIFEST_PATH = CROOKE / "crooke-pages-manifest.yaml"

SCAFFOLD_MARKER = "<!-- SCOUT_REFINED_PAGE_SCAFFOLD -->"


def _parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    if yaml is None:
        raise RuntimeError("PyYAML required: pip install pyyaml")
    data = yaml.safe_load(parts[1])
    return data if isinstance(data, dict) else {}


def _folder_date(p: Path) -> str:
    return p.parent.name


def _slug_from_stem(stem: str) -> str:
    s = stem
    if s.startswith("substack-crooke-"):
        s = s[len("substack-crooke-") :]
    s = re.sub(r"-\d{4}-\d{2}-\d{2}$", "", s)
    return s


def _display_title(fm: dict, stem: str, body: str) -> str:
    title = (fm.get("title") or "").strip()
    if title:
        return title
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].replace("(operator capture)", "").strip()
    # skip URL-only first line if present
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith("http") and not line.startswith("---"):
            if line.startswith("# "):
                return line[2:].strip()
            break
    return _slug_from_stem(stem).replace("-", " ").title()


def collect_primaries() -> list[Path]:
    paths = sorted(RAW.glob("**/substack-crooke*.md"))
    out: list[Path] = []
    seen: set[str] = set()
    for p in paths:
        key = str(p.resolve())
        if key in seen:
            continue
        text = p.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        if fm.get("thread") not in (None, "crooke"):
            continue
        seen.add(key)
        out.append(p)
    return sorted(out, key=lambda x: (x.parent.name, x.name))


def voice_date_for(p: Path, fm: dict) -> str:
    raw_pub = fm.get("pub_date")
    pub_day = str(raw_pub).strip() if raw_pub is not None else ""
    folder = _folder_date(p)
    for candidate in (pub_day, folder):
        if candidate and re.match(r"^\d{4}-\d{2}-\d{2}$", str(candidate)):
            return str(candidate)
    return folder


def build_entries(paths: list[Path]) -> list[dict]:
    by_date: dict[str, list[Path]] = defaultdict(list)
    prelim: list[tuple[Path, dict, str, str]] = []
    for p in paths:
        text = p.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        body = text.split("---", 2)[-1] if text.startswith("---") else text
        vd = voice_date_for(p, fm)
        by_date[vd].append(p)
        prelim.append((p, fm, vd, body))

    entries: list[dict] = []
    for p, fm, vd, body in prelim:
        stem = p.stem
        slug = _slug_from_stem(stem)
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", vd):
            vd = _folder_date(p)
        collision = len(by_date[vd]) > 1
        page_name = f"crooke-page-{vd}-{slug}.md"
        rel_raw = str(p.relative_to(NOTEBOOK)).replace("\\", "/")
        href = f"../../{rel_raw}"
        title = _display_title(fm, stem, body)
        raw_url = fm.get("source_url")
        source_url = (str(raw_url).strip() if raw_url is not None else "") or "Not yet pinned"
        raw_pub = fm.get("pub_date")
        preamble_val = (str(raw_pub).strip() if raw_pub is not None else "") or vd
        entries.append(
            {
                "raw_input_relative": rel_raw,
                "voice_date": vd,
                "page_filename": page_name,
                "collision": collision,
                "slug": slug,
                "display_title": title,
                "source_url": source_url,
                "href_verbatim": href,
                "preamble_date": str(preamble_val),
            }
        )
    entries.sort(key=lambda e: (e["voice_date"], e["page_filename"]))
    return entries


def render_scaffold(e: dict) -> str:
    vd = e["voice_date"]
    disp = (e.get("display_title") or "").strip()
    title_suffix = f" (*{disp}*)" if disp else ""
    pdate = e["preamble_date"]
    lines = [
        f"# Crooke refined page — {vd}{title_suffix}",
        "",
        "WORK only; not Record.",
        "",
        f"**Expert:** `crooke` · **Published:** {pdate} · **Capture:** Mode C — Substack · **Artifact:** refined page (standalone file under `experts/crooke/`). Not a `strategy-page` HTML fence in `thread.md` unless you duplicate judgment there during EOD compose.",
        "",
        SCAFFOLD_MARKER,
        "",
        "---",
        "",
        "### Verbatim",
        "",
        "",
        "",
        "### Reflection",
        "",
        "",
        "",
        "### Foresight",
        "",
        "",
        "",
        "---",
        "",
        "### Appendix",
        "",
        f"- **Full verbatim (capture):** [{e['raw_input_relative']}]({e['href_verbatim']})",
        "- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:crooke`, "
        + vd
        + ")",
        "- **`thread:crooke`** · **verify:** primary capture on disk + `pub_date` + inbox row; Conflicts Forum tier as analyst commentary unless wire-backed.",
        f"- **Canonical primary:** {e['source_url']}",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing crooke-page files even if scaffold marker was removed",
    )
    args = parser.parse_args()

    if yaml is None:
        print("build_crooke_refined_pages: need PyYAML", file=sys.stderr)
        return 1

    paths = collect_primaries()
    entries = build_entries(paths)

    manifest = {
        "generated_by": "scripts/strategy/build_crooke_refined_pages.py",
        "primary_capture_count": len(entries),
        "pages": entries,
    }
    MANIFEST_PATH.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {MANIFEST_PATH.relative_to(REPO_ROOT)}")

    written = 0
    skipped = 0
    for e in entries:
        out = CROOKE / e["page_filename"]
        if out.is_file() and not args.force:
            body = out.read_text(encoding="utf-8")
            if SCAFFOLD_MARKER not in body:
                skipped += 1
                continue
        out.write_text(render_scaffold(e), encoding="utf-8")
        written += 1
    print(f"Scaffolds written: {written}, skipped (edited): {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
