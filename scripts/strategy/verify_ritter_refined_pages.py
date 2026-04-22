#!/usr/bin/env python3
"""Fail if manifest-listed Ritter primaries lack refined page files or transcript backlinks.

Also checks each ritter-page for required spine headings, **Words:** line, optional word-count
match, soft-cap advisory (warn only), and optional Reflection+Foresight share heuristic.
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
MANIFEST_PATH = RITTER / "ritter-pages-manifest.yaml"
TRANSCRIPT_PATH = RITTER / "transcript.md"

SOFT_CAP_WORDS = 3000
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
    if not m:
        errors.append(f"{page_fn}: missing **Words:** line in preamble")
    else:
        declared = int(m.group(1))
        without_words = WORDS_LINE_RE.sub("", raw, count=1)
        actual = _word_count(without_words)
        if abs(declared - actual) > 5:
            errors.append(
                f"{page_fn}: **Words:** declares {declared} but body counts ~{actual} "
                f"(±5 tolerance; strip **Words:** line for count)"
            )

    total_w = _word_count(raw)
    if total_w > SOFT_CAP_WORDS:
        refl = _reflection_block(raw) or ""
        if "Soft cap" not in refl and "pruning" not in refl.lower():
            warnings.append(
                f"{page_fn}: over soft cap ({total_w} > {SOFT_CAP_WORDS}) "
                f"without **Soft cap — pruning** cue in Reflection"
            )

    # Advisory: Reflection+Foresight share vs Chronicle (heuristic ~35% ceiling)
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
        "--no-page-shape",
        action="store_true",
        help="Only check manifest files + transcript backlinks (legacy behavior).",
    )
    args = ap.parse_args()

    if yaml is None:
        print("verify_ritter_refined_pages: need PyYAML", file=sys.stderr)
        return 1
    if not MANIFEST_PATH.is_file():
        print(f"verify_ritter_refined_pages: missing {MANIFEST_PATH}", file=sys.stderr)
        return 1
    manifest = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    pages = manifest.get("pages") or []
    transcript = TRANSCRIPT_PATH.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    for entry in pages:
        raw_rel = entry.get("raw_input_relative", "")
        page_fn = entry.get("page_filename", "")
        raw_path = NOTEBOOK / raw_rel
        page_path = RITTER / page_fn
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
            page_path = RITTER / page_fn
            if not page_path.is_file():
                continue
            text = page_path.read_text(encoding="utf-8")
            e2, w2 = verify_page_content(page_fn, text)
            errors.extend(e2)
            warnings.extend(w2)

    for w in warnings:
        print(f"verify_ritter_refined_pages: warning: {w}", file=sys.stderr)

    if errors:
        print("verify_ritter_refined_pages: FAILED", file=sys.stderr)
        for line in errors:
            print(f"  {line}", file=sys.stderr)
        return 1
    print("verify_ritter_refined_pages: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
