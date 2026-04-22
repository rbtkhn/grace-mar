#!/usr/bin/env python3
"""Validate strategy-expert-*.md files for required profile headings.

Checks that each expert file (excluding the template) contains the required
top-level markdown headings from the cognitive profile schema. Does not
validate content quality — only structural presence. WORK only; not Record.

Exit 0 if ok; 1 if any error (prints to stderr).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from strategy_expert_corpus import RE_IN_FOLDER_MONTH_THREAD  # noqa: E402

DEFAULT_DIR = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook"
)

SKIP_FILES = {
    # Bundle: profile + thread + transcript templates in one file (anchors).
    "strategy-expert-template.md",
}

def _is_companion_file(name: str) -> bool:
    return (
        name.endswith("-thread.md")
        or name.endswith("-transcript.md")
        or name.endswith("-mind.md")
    )

REQUIRED_HEADINGS = [
    "Identity",
    "Convergence fingerprint",
    "Tension fingerprint",
    "Signature mechanisms",
    "Failure modes / overreads",
    "Active weave cues",
    "Published sources",
    "Seed",
]

RECOMMENDED_HEADINGS = [
    "Recurrent claims",
    "Predictive drift / accuracy notes",
    "Knot-use guidance",
    "History resonance defaults",
]

# strategy-state-iran official `voices/*/profile.md` — office-holder routing, not full cognitive profile.
VOICE_REQUIRED_HEADINGS = [
    "Identity",
]

_RE_HEADING = re.compile(r"^#{1,3}\s+(.+?)(?:\s*\(.*\))?\s*$", re.MULTILINE)


def _extract_headings(text: str) -> set[str]:
    """Return the set of heading texts found in a markdown file."""
    headings: set[str] = set()
    for m in _RE_HEADING.finditer(text):
        raw = m.group(1).strip()
        raw = re.sub(r"\*\*", "", raw)
        raw = raw.strip()
        headings.add(raw)
    return headings


def _has_thread_companion(expert_dir: Path, expert_id: str) -> bool:
    if (expert_dir / "thread.md").is_file():
        return True
    return any(
        p.is_file() and RE_IN_FOLDER_MONTH_THREAD.match(p.name)
        for p in expert_dir.glob(f"{expert_id}-thread-*.md")
    )


def _validate_voice_profile(path: Path, text: str, headings: set[str]) -> list[str]:
    """Lighter schema for official-voice folders under `voices/*/profile.md`."""
    errs: list[str] = []
    for req in VOICE_REQUIRED_HEADINGS:
        found = any(req.lower() in h.lower() for h in headings)
        if not found:
            errs.append(f"missing required heading: {req!r}")
    if not _has_thread_companion(path.parent, path.parent.name):
        errs.append(
            f"companion thread missing (expected thread.md or "
            f"{path.parent.name}-thread-YYYY-MM.md under {path.parent})"
        )
    return errs


def validate_expert_file(path: Path) -> list[str]:
    """Return a list of error strings for one expert file."""
    errs: list[str] = []
    text = path.read_text(encoding="utf-8")
    headings = _extract_headings(text)

    is_voice_profile = (
        path.name == "profile.md" and path.parent.parent.name == "voices"
    )
    if is_voice_profile:
        return _validate_voice_profile(path, text, headings)

    for req in REQUIRED_HEADINGS:
        found = any(req.lower() in h.lower() for h in headings)
        if not found:
            errs.append(f"missing required heading: {req!r}")

    for rec in RECOMMENDED_HEADINGS:
        found = any(rec.lower() in h.lower() for h in headings)
        if not found:
            print(
                f"warning: {path.name}: recommended heading missing: {rec!r}",
                file=sys.stderr,
            )

    if path.name == "profile.md" and path.parent.parent.name == "experts":
        expert_id = path.parent.name
        transcript_path = path.parent / "transcript.md"
        if not _has_thread_companion(path.parent, expert_id):
            errs.append(
                f"companion thread missing (expected thread.md or "
                f"{expert_id}-thread-YYYY-MM.md under {path.parent})"
            )
    else:
        thread_path = path.parent / path.name.replace(".md", "-thread.md")
        transcript_path = path.parent / path.name.replace(".md", "-transcript.md")
        if not thread_path.is_file():
            errs.append(f"companion file missing: {thread_path}")

    if not transcript_path.is_file():
        print(
            f"warning: {path.name}: companion file missing: {transcript_path}",
            file=sys.stderr,
        )

    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--dir",
        type=Path,
        default=DEFAULT_DIR,
        help="Directory containing strategy-expert-*.md files",
    )
    args = ap.parse_args()

    expert_files = sorted(args.dir.glob("experts/*/profile.md"))
    if not expert_files:
        expert_files = sorted(args.dir.glob("voices/*/profile.md"))
    if not expert_files:
        expert_files = sorted(
            p
            for p in args.dir.glob("strategy-expert-*.md")
            if p.name not in SKIP_FILES and not _is_companion_file(p.name)
        )

    if not expert_files:
        print("error: no expert files found", file=sys.stderr)
        return 1

    total_errors = 0
    for path in expert_files:
        errs = validate_expert_file(path)
        if errs:
            for e in errs:
                print(f"error: {path.name}: {e}", file=sys.stderr)
            total_errors += len(errs)

    if total_errors:
        print(
            f"\n{total_errors} error(s) in {len(expert_files)} files",
            file=sys.stderr,
        )
        return 1

    print(f"ok: {len(expert_files)} expert profiles validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
