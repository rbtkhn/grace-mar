#!/usr/bin/env python3
"""Advisory heuristic: URLs in daily-strategy-inbox vs source_url in raw-input YAML.

Does NOT enforce policy or CI-gate merges — surfaces possible misses when chat-first
capture omitted verbatim files. See docs/skill-work/work-strategy/strategy-notebook/raw-input/README.md.

Default mode considers **article-ish** URLs only (Substack `/p/`, `conflictsforum.substack.com`,
YouTube `watch?v=`). Use **`--all-urls`** for every `https://` in the inbox (noisy: wires, X, stubs).

Usage (repo root):
  python3 scripts/strategy_raw_input_gap_hint.py
  python3 scripts/strategy_raw_input_gap_hint.py --all-urls --verbose
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NOTEBOOK = REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
DEFAULT_INBOX = DEFAULT_NOTEBOOK / "daily-strategy-inbox.md"
DEFAULT_RAW = DEFAULT_NOTEBOOK / "raw-input"
RE_URL = re.compile(r"https://[^\s\]>)}]+")


def _article_capture_candidate(url: str) -> bool:
    u = url.lower()
    if "conflictsforum.substack.com" in u:
        return True
    if "substack.com" in u and "/p/" in u:
        return True
    if "youtube.com/watch?v=" in u:
        return True
    return False


def _urls_from_inbox(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8")
    found = set()
    for m in RE_URL.finditer(text):
        u = m.group(0).rstrip(".,);]")
        if "://" in u and len(u) > 12:
            found.add(u)
    return found


def _normalize(u: str) -> str:
    return u.rstrip("/")


def _source_urls_from_raw(raw_root: Path) -> set[str]:
    out: set[str] = set()
    if not raw_root.is_dir():
        return out
    for md in raw_root.rglob("*.md"):
        if md.name == "README.md":
            continue
        block = md.read_text(encoding="utf-8")
        if not block.startswith("---"):
            continue
        end = block.find("\n---", 3)
        if end < 0:
            continue
        fm_raw = block[3:end]
        for line in fm_raw.splitlines():
            line = line.strip()
            if line.startswith("source_url:"):
                val = line.split(":", 1)[1].strip().strip("\"'")
                if val and val.startswith("http"):
                    out.add(_normalize(val))
                break
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--inbox",
        type=Path,
        default=DEFAULT_INBOX,
        help="Path to daily-strategy-inbox.md",
    )
    ap.add_argument(
        "--raw-root",
        type=Path,
        default=DEFAULT_RAW,
        help="strategy-notebook raw-input root",
    )
    ap.add_argument(
        "--verbose",
        action="store_true",
        help="Note false-positive caveats",
    )
    ap.add_argument(
        "--all-urls",
        action="store_true",
        help="Consider every https URL in inbox (many reference links; noisy)",
    )
    args = ap.parse_args()

    inbox_urls = _urls_from_inbox(args.inbox)
    if not args.all_urls:
        inbox_urls = {u for u in inbox_urls if _article_capture_candidate(u)}
    raw_urls = _source_urls_from_raw(args.raw_root)

    hints: list[str] = []
    for iu in sorted(inbox_urls):
        ni = _normalize(iu)
        slug = ""
        if "/p/" in ni:
            slug = ni.split("/p/")[-1].split("?")[0].strip("/")
        matched = False
        for ru in raw_urls:
            if ni == ru or ni.startswith(ru) or ru.startswith(ni):
                matched = True
                break
            if slug and slug in ru:
                matched = True
                break
        if not matched:
            hints.append(iu)

    print(
        "strategy_raw_input_gap_hint.py — advisory only",
        file=sys.stderr,
    )
    mode = "all-urls" if args.all_urls else "article-ish (Substack /p/, conflictsforum, YouTube watch)"
    print(f"Mode: {mode}", file=sys.stderr)
    if not inbox_urls:
        rel = args.inbox.relative_to(REPO_ROOT) if args.inbox.is_file() else args.inbox
        print(f"No matching URLs in {rel}")
        return 0
    print(f"Inbox URLs: {len(inbox_urls)} | raw-input source_url: {len(raw_urls)}")
    if not hints:
        print("No obvious gaps (heuristic).")
        return 0
    print(f"Possible gaps ({len(hints)}) — inbox URLs not matched to raw-input YAML:")
    for u in hints:
        print(f"  - {u}")
    if args.verbose:
        print("\n(This script does not know intent — pasted stubs vs commentary URLs.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
