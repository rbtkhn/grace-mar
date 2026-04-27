#!/usr/bin/env python3
"""Emit ritter-pages-manifest.yaml and scaffold ritter-page-*.md from primary raw-input captures.

Run from repo root after adding new Substack / JF / Ritter's Rant verbatim files:
  python3 scripts/strategy/build_ritter_refined_pages.py

Scaffolds are structural only (empty Chronicle / Reflection / Foresight). After ingest, run
`scripts/strategy/assemble_ritter_pages_verbatim.py` to embed ~80% expert verbatim in Chronicle
and generated WORK analysis in Reflection/Foresight per
`docs/skill-work/work-strategy/strategy-notebook/refined-page-template.md` (Ritter extended modes; compat stub: `experts/ritter/ritter-page-template.md`).

Idempotent: overwrites manifest; overwrites ritter-page scaffolds that still contain
the marker SCOUT_REFINED_PAGE_SCAFFOLD (or use --force to overwrite all).

Transcript backlinks: lines may be ``Verbatim (~triage note):`` as well as ``Verbatim:``;
any line starting with ``Verbatim`` should be treated as the verbatim header when inserting
``Refined page:`` after raw-input captures.
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
RITTER = NOTEBOOK / "experts" / "ritter"
MANIFEST_PATH = RITTER / "ritter-pages-manifest.yaml"

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
    if s.startswith("substack-ritter-"):
        s = s[len("substack-ritter-") :]
    s = re.sub(r"-\d{4}-\d{2}-\d{2}$", "", s)
    return s


def _mode_and_preamble_date(fm: dict, stem: str) -> tuple[str, str, str]:
    """Returns (mode_letter, preamble_label, date_str YYYY-MM-DD)."""
    series = (fm.get("series") or "").strip()
    pub = str((fm.get("pub_date") or "")).strip()
    if "judging freedom" in series.lower() or stem.startswith("judging-freedom"):
        return "B", "Aired", pub
    if "ritter's rant" in series.lower() or stem.startswith("ritter-rant"):
        return "C", "Aired", pub
    return "A", "Published", pub


def _display_title(fm: dict, stem: str, body: str) -> str:
    et = (fm.get("episode_title") or "").strip()
    if et:
        return et
    series = (fm.get("series") or "").strip()
    if series:
        return re.sub(r"\s*\(Substack\)\s*$", "", series).strip() or series
    title = (fm.get("title") or "").strip()
    if title:
        return title
    for line in body.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].replace("(operator capture)", "").strip()
    return _slug_from_stem(stem).replace("-", " ").title()


def collect_primaries() -> list[Path]:
    paths: list[Path] = []
    paths.extend(sorted(RAW.glob("**/substack-ritter*.md")))
    paths.extend(sorted(RAW.glob("**/judging-freedom*.md")))
    paths.extend(sorted(RAW.glob("**/ritter-rant*.md")))
    out: list[Path] = []
    seen: set[str] = set()
    for p in paths:
        if "transcript-ritter" in p.name:
            continue
        key = str(p.resolve())
        if key in seen:
            continue
        text = p.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        if p.name.startswith("substack-ritter"):
            thread_ok = fm.get("thread") in (None, "ritter")
        else:
            thread_ok = fm.get("thread") == "ritter"
        if not thread_ok:
            continue
        seen.add(key)
        out.append(p)
    return sorted(out, key=lambda x: (x.parent.name, x.name))


def voice_date_for(p: Path, fm: dict) -> str:
    pub_day = (fm.get("pub_date") or "").strip()
    folder = _folder_date(p)
    for candidate in (pub_day, folder):
        if candidate and re.match(r"^\d{4}-\d{2}-\d{2}$", str(candidate)):
            return str(candidate)
    return folder


def build_entries(paths: list[Path]) -> list[dict]:
    by_date: dict[str, list[Path]] = defaultdict(list)
    prelim: list[tuple[Path, dict, str]] = []
    for p in paths:
        text = p.read_text(encoding="utf-8")
        fm = _parse_frontmatter(text)
        body = text.split("---", 2)[-1] if text.startswith("---") else text
        vd = voice_date_for(p, fm)
        by_date[vd].append(p)
        prelim.append((p, fm, vd))

    entries: list[dict] = []
    for p, fm, vd in prelim:
        stem = p.stem
        slug = _slug_from_stem(stem)
        mode, prem_label, _ = _mode_and_preamble_date(fm, stem)
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", vd):
            vd = _folder_date(p)
        collision = len(by_date[vd]) > 1
        page_name = f"ritter-page-{vd}-{slug}.md"
        rel_raw = f"raw-input/{p.parent.name}/{p.name}"
        href = f"../../{rel_raw}"
        title = _display_title(fm, stem, body)
        source_url = (fm.get("source_url") or "").strip() or "Not yet pinned"
        capture_mode = {
            "A": "Mode A — Substack",
            "B": "Mode B — Judging Freedom / interview (see raw-input series)",
            "C": "Mode C — YouTube (see raw-input source_url)",
        }[mode]
        preamble_val = (fm.get("pub_date") or "").strip() or vd
        entries.append(
            {
                "raw_input_relative": str(p.relative_to(NOTEBOOK)).replace("\\", "/"),
                "voice_date": vd,
                "page_filename": page_name,
                "collision": collision,
                "slug": slug,
                "mode": mode,
                "capture_mode": capture_mode,
                "preamble_label": prem_label,
                "preamble_date": str(preamble_val),
                "display_title": title,
                "source_url": source_url,
                "href_verbatim": href,
            }
        )
    entries.sort(key=lambda e: (e["voice_date"], e["page_filename"]))
    return entries


def render_scaffold(e: dict) -> str:
    vd = e["voice_date"]
    title_suffix = f" (*{e['display_title']}*)" if e.get("display_title") else ""
    prem = e["preamble_label"]
    pdate = e["preamble_date"]
    cap = e["capture_mode"]
    lines = [
        f"# Ritter strategy page — {vd}{title_suffix}",
        "",
        "WORK only; not Record.",
        "",
        f"**Expert:** `ritter` · **{prem}:** {pdate} · **Capture:** {cap} · **Artifact:** strategy-page file (`ritter-page-…` under `experts/ritter/`). Optional: echo in `thread.md` fence for watches / cross-expert duplication.",
        "",
        SCAFFOLD_MARKER,
        "",
        "---",
        "",
        "### Chronicle",
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
        "- **Inbox / triage:** [daily-strategy-inbox.md](../../daily-strategy-inbox.md) (search `thread:ritter`, "
        + vd
        + ")",
        "- **`thread:ritter`** · **verify:** primary capture on disk + voice date + inbox row (SS | / JF | / YT | as applicable)",
        f"- **Canonical primary:** {e['source_url']}",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Overwrite existing scaffolds even if edited")
    args = parser.parse_args()

    if yaml is None:
        print("build_ritter_refined_pages: need PyYAML", file=sys.stderr)
        return 1

    paths = collect_primaries()
    entries = build_entries(paths)

    backlog = [
        {
            "note": "Substack *The Consequences of Incompetence* (2026-04-19) — listed in inbox/transcript; no verbatim raw-input file yet.",
            "action": "Ingest substack-ritter-…-2026-04-19.md then re-run this script and fill refined page.",
            "status": "backlog_no_raw_input",
        }
    ]

    manifest = {
        "generated_by": "scripts/strategy/build_ritter_refined_pages.py",
        "primary_capture_count": len(entries),
        "backlog": backlog,
        "pages": entries,
    }
    MANIFEST_PATH.write_text(yaml.safe_dump(manifest, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {MANIFEST_PATH.relative_to(REPO_ROOT)}")

    written = 0
    skipped = 0
    for e in entries:
        out = RITTER / e["page_filename"]
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
