#!/usr/bin/env python3
"""Insert or update script-maintained word counts in strategy-notebook markdown.

Scans ``docs/skill-work/work-strategy/strategy-notebook/**/*.md`` (with exclusions
below), computes a deterministic approximate word count of operator-facing body
text, and either:

* **YAML** — insert or update ``word_count: <int>`` inside leading ``---`` front matter, or
* **No front matter** — insert or update ``<!-- word_count: <int> -->`` after
  the first H1, or at file top if no H1.

WORK only; not Record. Excludes large raw-input captures. Do not hand-edit
``word_count``; run this script after bulk notebook edits.

Usage::

  python3 scripts/strategy/update_strategy_notebook_word_counts.py
  python3 scripts/strategy/update_strategy_notebook_word_counts.py --dry-run
  python3 scripts/strategy/update_strategy_notebook_word_counts.py --check
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"

# Dated day folders under raw-input (excludes large captures).
_RE_RAW_INPUT_DATED = re.compile(
    r"(?:^|/)raw-input/(\d{4}-\d{2}-\d{2})/"
)
# _aired-pending and similar
_RE_RAW_INPUT_PENDING = re.compile(r"(?:^|/)raw-input/_aired-pending/")

# Managed HTML word count (line-anchored for detection; in-place number swap for updates)
RE_MANAGED_WC = re.compile(
    r"^<!--\s*word_count:\s*(\d+)\s*-->\s*$", re.MULTILINE
)
RE_WC_NUM_ANYWHERE = re.compile(r"<!--\s*word_count:\s*(\d+)\s*-->")
RE_WC_IN_YAML = re.compile(
    r"^word_count:\s*(\d+)\s*$", re.MULTILINE
)
RE_LINK = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")

# Fenced code blocks (greedy, non-overlapping)
RE_FENCE = re.compile(r"^```[\w-]*\n.*?^```\s*$", re.MULTILINE | re.DOTALL)

# HTML comments (non-greedy, multiline)
RE_HTML_COMMENT = re.compile(r"<!--[\s\S]*?-->")

# Table divider line (GitHub / pipe tables)
RE_TABLE_DIV = re.compile(r"^\s*\|?[\s\-:|]+\|?\s*$", re.MULTILINE)

# first ATX H1 that is a single # (not ##)
RE_H1 = re.compile(r"^#\s+.+$", re.MULTILINE)


@dataclass
class RunStats:
    scanned: int = 0
    updated: int = 0
    skipped: int = 0
    skip_reasons: dict[str, int] = field(default_factory=dict)
    check_stale: int = 0
    would_update: int = 0

    def note_skip(self, reason: str) -> None:
        self.skipped += 1
        self.skip_reasons[reason] = self.skip_reasons.get(reason, 0) + 1


def _is_eligible_path(rel: Path) -> bool:
    """``rel`` is relative to strategy-notebook root."""
    s = str(rel).replace("\\", "/")
    if not s.lower().endswith(".md"):
        return False
    if _RE_RAW_INPUT_PENDING.search(s):
        return False
    if _RE_RAW_INPUT_DATED.search(s):
        return False
    if "/raw-input/" in s or s.startswith("raw-input/"):
        # Only raw-input/README.md at notebook root
        if s in ("raw-input/README.md", "raw-input\\README.md"):
            return True
        return False
    return True


def _split_front_matter(text: str) -> tuple[str | None, str] | None:
    """If file starts with ``---\n`` YAML, return (front_matter_inner, rest_body).

    If no valid closing ``---`` on its own line after start, return None.
    """
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None
    # Find end of first --- block: line that is only ---
    m = re.search(r"^---\s*$", text[3:], re.MULTILINE)
    if not m:
        return None
    end = 3 + m.start()
    inner = text[3:end]
    if inner.startswith("\n"):
        inner = inner[1:]
    elif inner.startswith("\r\n"):
        inner = inner[2:]
    after_close = 3 + m.end()
    if after_close < len(text) and text[after_close] == "\r" and after_close + 1 < len(text) and text[after_close + 1] == "\n":
        body = text[after_close + 2 :]
    elif after_close < len(text) and text[after_close] in "\n":
        body = text[after_close + 1 :]
    else:
        body = text[after_close:]
    return (inner, body)


def _strip_count_regions(text: str) -> str:
    """Remove regions that do not count as prose (fences, comments, table lines)."""
    t = text
    # Remove our managed count comment in body (non-YAML case)
    t = RE_MANAGED_WC.sub("", t)
    t = RE_FENCE.sub(" ", t)
    t = RE_HTML_COMMENT.sub(" ", t)
    t = RE_TABLE_DIV.sub(" ", t)
    # Link visible text: replace [a](b) with a
    t = RE_LINK.sub(r"\1", t)
    return t


def count_words_in_body(text: str) -> int:
    """Deterministic word count on stripped body (no front matter, no code, etc.)."""
    t = _strip_count_regions(text)
    if not t.strip():
        return 0
    # Split: whitespace runs; each token = one "word" (hyphenated stays one)
    return len([w for w in t.split() if w])


def _insert_yml_word_count(fm_inner: str, new_count: int) -> str:
    """``fm_inner`` is the content between opening ``---`` and closing ``---`` (no delimiters)."""
    if re.search(r"(?m)^word_count:\s*\d+\s*$", fm_inner):
        def _repl(m: re.Match) -> str:
            ending = m.group(1) or "\n"
            return f"word_count: {new_count}{ending}"

        return re.sub(
            r"(?m)^word_count:\s*\d+\s*(\r?\n|\Z)",
            _repl,
            fm_inner,
            count=1,
        )
    lines = fm_inner.splitlines(keepends=True)
    to_insert = f"word_count: {new_count}\n"
    best = -1
    for i, line in enumerate(lines):
        ls = line.lower().lstrip()
        if ls.startswith("title:") or ls.startswith("status:") or ls.startswith("kind:"):
            best = i
    if best >= 0:
        lines2 = list(lines)
        lines2.insert(best + 1, to_insert)
        return "".join(lines2)
    return to_insert + "".join(lines)


def _apply_yml_to_file(text: str, new_count: int) -> str:
    sp = _split_front_matter(text)
    if sp is None:
        raise ValueError("expected YAML front matter")
    inner, body = sp
    new_inner = _insert_yml_word_count(inner, new_count)
    if new_inner and not new_inner.endswith(("\n", "\r")):
        new_inner += "\n"
    return "---\n" + new_inner + "---\n" + body


def build_updated_content(content: str) -> str:
    """Return full file text with ``word_count`` set to current deterministic count."""
    sp = _split_front_matter(content)
    if sp is not None:
        _inner, body = sp
        n = count_words_in_body(body)
        return _apply_yml_to_file(content, n)
    n = count_words_in_body(content)
    return _apply_html_to_file(content, n)


def _apply_html_to_file(text: str, new_count: int) -> str:
    new_line = f"<!-- word_count: {new_count} -->"
    if RE_WC_NUM_ANYWHERE.search(text):
        return RE_WC_NUM_ANYWHERE.sub(new_line, text, count=1)

    m = RE_H1.search(text)
    if m:
        pos = m.end()
        if pos < len(text) and text[pos : pos + 2] == "\r\n":
            pos += 2
        elif pos < len(text) and text[pos] == "\n":
            pos += 1
        ins = f"{new_line}\n"
        return text[:pos] + ins + text[pos:]
    return f"{new_line}\n" + text


def _normalize_final_newline(s: str) -> str:
    if not s:
        return s
    if not s.endswith("\n"):
        return s + "\n"
    return s


def _read_stored_count(content: str) -> int | None:
    sp = _split_front_matter(content)
    if sp is not None:
        inner, _ = sp
        m = RE_WC_IN_YAML.search(inner)
        if m:
            return int(m.group(1))
        return None
    m = RE_WC_NUM_ANYWHERE.search(content)
    if m:
        return int(m.group(1))
    return None


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def iter_markdown_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for p in sorted(root.rglob("*.md")):
        try:
            rel = p.relative_to(root)
        except ValueError:
            continue
        if _is_eligible_path(rel):
            out.append(p)
    return out


def _expected_count(content: str) -> int:
    sp = _split_front_matter(content)
    if sp is not None:
        return count_words_in_body(sp[1])
    return count_words_in_body(content)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_NOTEBOOK,
        help="Strategy notebook root (default: .../strategy-notebook)",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes but do not write",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if any file is missing or has stale word_count",
    )
    args = ap.parse_args()
    if args.dry_run and args.check:
        print("error: use only one of --dry-run or --check", file=sys.stderr)
        return 2

    root: Path = args.root.resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    stats = RunStats()
    stale_paths: list[Path] = []

    paths = iter_markdown_files(root)

    if args.check:
        for path in paths:
            stats.scanned += 1
            c = path.read_text(encoding="utf-8")
            n = _expected_count(c)
            st = _read_stored_count(c)
            if st is None or st != n:
                stats.check_stale += 1
                stale_paths.append(path)
        print(
            f"check: scanned {stats.scanned} eligible files, "
            f"stale or missing word_count: {stats.check_stale}"
        )
        if stale_paths:
            for p in stale_paths[:20]:
                c = p.read_text(encoding="utf-8")
                n = _expected_count(c)
                st = _read_stored_count(c)
                print(
                    f"  {_display_path(p)}  stored={st!s}  expected={n}",
                    file=sys.stderr,
                )
            if len(stale_paths) > 20:
                print(f"  ... and {len(stale_paths) - 20} more", file=sys.stderr)
        return 1 if stats.check_stale else 0

    for path in paths:
        stats.scanned += 1
        c = path.read_text(encoding="utf-8")
        new_c = build_updated_content(c)
        n_old = _normalize_final_newline(c)
        n_new = _normalize_final_newline(new_c)
        n_exp = _expected_count(c)
        if n_old == n_new:
            stats.note_skip("unchanged")
            continue
        rel = _display_path(path)
        if args.dry_run:
            stats.would_update += 1
            print(f"would update: {rel}  word_count -> {n_exp}")
        else:
            path.write_text(n_new, encoding="utf-8")
            stats.updated += 1
            print(f"updated: {rel}  word_count {n_exp}")

    print(
        f"summary: scanned={stats.scanned} updated={stats.updated} "
        f"dry_run_would={stats.would_update} "
        f"unchanged={stats.skip_reasons.get('unchanged', 0)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
