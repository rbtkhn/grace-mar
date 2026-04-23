#!/usr/bin/env python3
"""Fail if manifest-listed strategy expert primaries lack refined page files or transcript backlinks.

Default **Ritter**; use `--expert mearsheimer` for Mearsheimer. Checks each refined page file for
required spine headings. When a **`**Words:**`** line is present, validates word-count match (±5
tokens) and optional Reflection+Foresight share advisory for legacy verbatim-leaning pages; when
omitted (optional bookkeeping), those checks are skipped. There is **no** word-count ceiling or soft-cap
warning on page length.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
RITTER = NOTEBOOK / "experts" / "ritter"
MEARSHEIMER = NOTEBOOK / "experts" / "mearsheimer"


def _expert_paths(expert: str) -> tuple[Path, Path, str]:
    if expert == "ritter":
        return (
            RITTER / "ritter-pages-manifest.yaml",
            RITTER / "transcript.md",
            "verify_ritter_refined_pages",
        )
    if expert == "mearsheimer":
        return (
            MEARSHEIMER / "mearsheimer-pages-manifest.yaml",
            MEARSHEIMER / "transcript.md",
            "verify_mearsheimer_refined_pages",
        )
    raise ValueError(expert)

WORDS_DECL_RE = re.compile(r"^\*\*Words:\*\*\s*(\d+)", re.MULTILINE)
WORDS_LINE_RE = re.compile(r"(?m)^\*\*Words:\*\*\s*\d+.*\n?", re.MULTILINE)
REQUIRED_H3 = (
    "### Chronicle",
    "### Reflection",
    "### Foresight",
    "### Appendix",
)
# Legacy headings (still accepted until pages are regenerated)
LEGACY_H3_MAP = {
    "### Chronicle": ("### Signal",),
    "### Reflection": ("### Judgment",),
    "### Foresight": ("### Open",),
    "### Appendix": ("### Technical appendix",),
}


def _word_count(s: str) -> int:
    return len(re.findall(r"\S+", s))


def _has_heading(text: str, canonical: str) -> bool:
    if canonical in text:
        return True
    for legacy in LEGACY_H3_MAP.get(canonical, ()):
        if legacy in text:
            return True
    return False


def _section_body(text: str, start_h3: str, end_h3: str | None) -> str | None:
    i = text.find(start_h3)
    if i < 0:
        return None
    start = i + len(start_h3)
    if end_h3 is None:
        return text[start:]
    j = text.find(end_h3, start)
    if j < 0:
        return text[start:]
    return text[start:j]


def _reflection_block(text: str) -> str | None:
    """Body of Reflection (or legacy Judgment) through start of Foresight/Open."""
    for pair in (
        ("### Reflection", "### Foresight"),
        ("### Judgment", "### Open"),
    ):
        block = _section_body(text, pair[0], pair[1])
        if block is not None:
            return block
    return None


def _foresight_block(text: str) -> str | None:
    for pair in (
        ("### Foresight", "### Appendix"),
        ("### Foresight", "### Technical appendix"),
        ("### Open", "### Appendix"),
        ("### Open", "### Technical appendix"),
    ):
        if pair[0] not in text:
            continue
        block = _section_body(text, pair[0], pair[1])
        if block is not None:
            return block
    return None


def _chronicle_body(text: str) -> str | None:
    for start, end in (
        ("### Chronicle", "### Reflection"),
        ("### Signal", "### Judgment"),
    ):
        if start not in text:
            continue
        block = _section_body(text, start, end)
        if block is not None:
            return block
    return None


def verify_page_content(page_fn: str, raw: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for h3 in REQUIRED_H3:
        if not _has_heading(raw, h3):
            errors.append(f"{page_fn}: missing {h3} (or accepted legacy heading)")

    m = WORDS_DECL_RE.search(raw)
    if m:
        declared = int(m.group(1))
        without_words = WORDS_LINE_RE.sub("", raw, count=1)
        actual = _word_count(without_words)
        if abs(declared - actual) > 5:
            errors.append(
                f"{page_fn}: **Words:** declares {declared} but body counts ~{actual} "
                f"(±5 tolerance; strip **Words:** line for count)"
            )

    # Advisory: Reflection+Foresight share vs Chronicle (only when **Words:** present—long Chronicle is expected)
    if m is not None:
        chronicle = _chronicle_body(raw)
        refl_b = _reflection_block(raw)
        fore_b = _foresight_block(raw)
        if chronicle is not None and refl_b is not None and fore_b is not None:
            c_w = _word_count(chronicle)
            r_w = _word_count(refl_b)
            f_w = _word_count(fore_b)
            denom = c_w + r_w + f_w
            if denom > 0:
                share = (r_w + f_w) / denom
                if share > 0.35:
                    warnings.append(
                        f"{page_fn}: Reflection+Foresight ~{share:.0%} of "
                        f"(Chronicle+Reflection+Foresight) words — check ~80/20 target (advisory)"
                    )

    return errors, warnings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--expert",
        choices=("ritter", "mearsheimer"),
        default="ritter",
        help="Which expert manifest + transcript to verify (default: ritter).",
    )
    ap.add_argument(
        "--no-page-shape",
        action="store_true",
        help="Only check manifest files + transcript backlinks (legacy behavior).",
    )
    args = ap.parse_args()

    manifest_path, transcript_path, tool_label = _expert_paths(args.expert)
    expert_dir = manifest_path.parent

    if yaml is None:
        print(f"{tool_label}: need PyYAML", file=sys.stderr)
        return 1
    if not manifest_path.is_file():
        print(f"{tool_label}: missing {manifest_path}", file=sys.stderr)
        return 1
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    pages = manifest.get("pages") or []
    transcript = transcript_path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    for entry in pages:
        raw_rel = entry.get("raw_input_relative", "")
        page_fn = entry.get("page_filename", "")
        raw_path = NOTEBOOK / raw_rel
        page_path = expert_dir / page_fn
        if not raw_path.is_file():
            errors.append(f"missing raw-input: {raw_rel}")
        if not page_path.is_file():
            errors.append(f"missing refined page: {page_fn}")
        if page_fn and page_fn not in transcript:
            errors.append(f"transcript.md missing backlink for {page_fn}")

    # Shape checks for on-disk pages (independent of manifest errors above)
    if not args.no_page_shape:
        for entry in pages:
            page_fn = entry.get("page_filename", "")
            if not page_fn:
                continue
            page_path = expert_dir / page_fn
            if not page_path.is_file():
                continue
            text = page_path.read_text(encoding="utf-8")
            e2, w2 = verify_page_content(page_fn, text)
            errors.extend(e2)
            warnings.extend(w2)

    for w in warnings:
        print(f"{tool_label}: warning: {w}", file=sys.stderr)

    if errors:
        print(f"{tool_label}: FAILED", file=sys.stderr)
        for line in errors:
            print(f"  {line}", file=sys.stderr)
        return 1
    print(f"{tool_label}: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
