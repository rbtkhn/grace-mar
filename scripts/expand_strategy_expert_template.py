#!/usr/bin/env python3
"""Materialize the four strategy-expert files from the bundle template.

Reads ``docs/skill-work/work-strategy/strategy-notebook/strategy-expert-template.md``
(anchors ``profile-template``, ``thread-template``, ``transcript-template``,
``mind-template``) and writes:

- ``strategy-expert-<expert_id>.md``
- ``strategy-expert-<expert_id>-thread.md``
- ``strategy-expert-<expert_id>-transcript.md``
- ``strategy-expert-<expert_id>-mind.md``

Companion links in the template (pointing at ``strategy-expert-template.md#...``) are
rewritten to sibling filenames. Placeholders ``<expert_id>`` and ``<Full name>`` are
filled from CLI args.

WORK only; not Record.

Example::

    python3 scripts/expand_strategy_expert_template.py --expert-id jane-doe --full-name "Jane Doe"
    python3 scripts/expand_strategy_expert_template.py --expert-id jane-doe --dry-run
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_BUNDLE = (
    REPO_ROOT
    / "docs/skill-work/work-strategy/strategy-notebook/strategy-expert-template.md"
)
DEFAULT_OUT = (
    REPO_ROOT / "docs/skill-work/work-strategy/strategy-notebook"
)

ANCHOR_PROFILE = "<a id=\"profile-template\"></a>"
ANCHOR_THREAD = "<a id=\"thread-template\"></a>"
ANCHOR_TRANSCRIPT = "<a id=\"transcript-template\"></a>"
ANCHOR_MIND = "<a id=\"mind-template\"></a>"

_RE_PROFILE_HEAD = re.compile(r"^[\s\n]*## Profile →[^\n]*\n\n", re.MULTILINE)
_RE_THREAD_HEAD = re.compile(r"^[\s\n]*## Thread →[^\n]*\n\n", re.MULTILINE)
_RE_TRANSCRIPT_HEAD = re.compile(r"^[\s\n]*## Transcript →[^\n]*\n\n", re.MULTILINE)
_RE_MIND_HEAD = re.compile(r"^[\s\n]*## Mind →[^\n]*\n\n", re.MULTILINE)


def _strip_bundle_section_trailer(s: str) -> str:
    """Remove a single trailing ``---`` line (bundle separator only), once."""
    lines = s.rstrip().split("\n")
    if len(lines) >= 1 and lines[-1].strip() == "---":
        lines = lines[:-1]
    return "\n".join(lines).rstrip() + "\n"


def _split_bundle(text: str) -> tuple[str, str, str, str]:
    if (
        ANCHOR_PROFILE not in text
        or ANCHOR_THREAD not in text
        or ANCHOR_TRANSCRIPT not in text
        or ANCHOR_MIND not in text
    ):
        raise ValueError(
            "Bundle must contain profile, thread, transcript, and mind anchors "
            f"({ANCHOR_PROFILE!r}, …, {ANCHOR_MIND!r})"
        )
    _, rest = text.split(ANCHOR_PROFILE, 1)
    profile_wrap, rest = rest.split(ANCHOR_THREAD, 1)
    thread_wrap, rest = rest.split(ANCHOR_TRANSCRIPT, 1)
    transcript_wrap, mind_wrap = rest.split(ANCHOR_MIND, 1)
    return profile_wrap, thread_wrap, transcript_wrap, mind_wrap


def _strip_profile_section(s: str) -> str:
    s2 = _RE_PROFILE_HEAD.sub("", s.lstrip())
    return _strip_bundle_section_trailer(s2)


def _strip_thread_section(s: str) -> str:
    s2 = _RE_THREAD_HEAD.sub("", s.lstrip())
    return _strip_bundle_section_trailer(s2)


def _strip_transcript_section(s: str) -> str:
    s2 = _RE_TRANSCRIPT_HEAD.sub("", s.lstrip())
    return _strip_bundle_section_trailer(s2)


def _strip_mind_section(s: str) -> str:
    s2 = _RE_MIND_HEAD.sub("", s.lstrip())
    return s2.rstrip() + "\n"


def _apply_substitutions(body: str, expert_id: str, full_name: str) -> str:
    out = body.replace("<expert_id>", expert_id)
    out = out.replace("<Full name>", full_name)
    out = out.replace("<full name>", full_name)
    out = out.replace(
        "](strategy-expert-template.md#transcript-template)",
        f"](strategy-expert-{expert_id}-transcript.md)",
    )
    out = out.replace(
        "](strategy-expert-template.md#thread-template)",
        f"](strategy-expert-{expert_id}-thread.md)",
    )
    out = out.replace(
        "](strategy-expert-template.md#profile-template)",
        f"](strategy-expert-{expert_id}.md)",
    )
    out = out.replace(
        "](strategy-expert-template.md#mind-template)",
        f"](strategy-expert-{expert_id}-mind.md)",
    )
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--expert-id",
        required=True,
        help="Slug, e.g. alexander-mercouris (letters, digits, hyphen)",
    )
    ap.add_argument(
        "--full-name",
        default="<full name>",
        help='Display name for the profile H1 (default: placeholder "<full name>")',
    )
    ap.add_argument("--bundle", type=Path, default=DEFAULT_BUNDLE, help="Path to bundle template")
    ap.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT,
        help="Directory for the four strategy-expert-*.md files",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths and sizes only; do not write",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="Overwrite if target files already exist",
    )
    args = ap.parse_args()

    eid = args.expert_id.strip()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", eid):
        print(
            "error: --expert-id must be lowercase slug (letters, digits, hyphens), "
            f"got {eid!r}",
            file=sys.stderr,
        )
        return 1

    if not args.bundle.is_file():
        print(f"error: bundle not found: {args.bundle}", file=sys.stderr)
        return 1

    text = args.bundle.read_text(encoding="utf-8")
    pw, tw, xw, mw = _split_bundle(text)
    profile_body = _apply_substitutions(_strip_profile_section(pw), eid, args.full_name)
    thread_body = _apply_substitutions(_strip_thread_section(tw), eid, args.full_name)
    transcript_body = _apply_substitutions(_strip_transcript_section(xw), eid, args.full_name)
    mind_body = _apply_substitutions(_strip_mind_section(mw), eid, args.full_name)

    paths = [
        args.out_dir / f"strategy-expert-{eid}.md",
        args.out_dir / f"strategy-expert-{eid}-thread.md",
        args.out_dir / f"strategy-expert-{eid}-transcript.md",
        args.out_dir / f"strategy-expert-{eid}-mind.md",
    ]
    bodies = [profile_body, thread_body, transcript_body, mind_body]

    for p in paths:
        if p.exists() and not args.force:
            try:
                disp = p.relative_to(REPO_ROOT)
            except ValueError:
                disp = p
            print(
                f"error: {disp} exists (use --force to overwrite)",
                file=sys.stderr,
            )
            return 1

    for p, body in zip(paths, bodies):
        try:
            display = p.relative_to(REPO_ROOT)
        except ValueError:
            display = p
        if args.dry_run:
            print(f"would write {display} ({len(body)} bytes)")
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(body, encoding="utf-8")
            print(f"wrote {display} ({len(body)} bytes)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
