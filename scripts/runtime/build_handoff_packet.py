#!/usr/bin/env python3
"""
Bundle checkpoints (and optional memory brief) into one handoff Markdown file.

Runtime work artifact only — not canonical Record. See docs/runtime/long-horizon-work.md.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_RUNTIME = Path(__file__).resolve().parent
if str(_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_RUNTIME))

from checkpoint_handoff_common import (  # noqa: E402
    extract_section,
    parse_field,
    section_bullets,
    slug,
)

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _matches_lane(path: Path, lane: str) -> bool:
    text = path.read_text(encoding="utf-8")
    body_lane = parse_field(text, "Lane:")
    if body_lane and body_lane.strip() == lane.strip():
        return True
    lane_slug = slug(lane)
    base = path.stem
    m = re.match(r"^(\d{4}-\d{2}-\d{2})_(.+)$", base)
    if not m:
        return False
    rest = m.group(2)
    return rest.startswith(lane_slug + "_")


def _collect_checkpoints(checkpoints_dir: Path, lane: str) -> list[Path]:
    out: list[Path] = []
    if not checkpoints_dir.is_dir():
        return out
    for p in checkpoints_dir.glob("*.md"):
        if _matches_lane(p, lane):
            out.append(p)

    def sort_key(pp: Path) -> tuple[str, float]:
        m = re.match(r"^(\d{4}-\d{2}-\d{2})_", pp.stem)
        day = m.group(1) if m else ""
        try:
            mtime = pp.stat().st_mtime
        except OSError:
            mtime = 0.0
        return (day, mtime)

    out.sort(key=sort_key, reverse=True)
    return out


def _review_gate_tag(text: str) -> str:
    """Return gate-relevance label from checkpoint body."""
    sec = extract_section(text, "Gate relevance").strip()
    if not sec:
        g = parse_field(text, "Gate relevance:")
        return (g or "none").strip()
    for line in sec.splitlines():
        line = line.strip()
        if line.startswith("- "):
            return line[2:].strip()
    return sec.splitlines()[0].strip() if sec else "none"


def _normalize_handoff_review(tag: str) -> str:
    low = tag.lower().strip()
    if low in ("none", "watch", "candidate likely"):
        return low
    if "candidate" in low:
        return "candidate likely"
    if "maybe" in low:
        return "watch"
    if low == "maybe later":
        return "watch"
    return "watch" if low and low != "none" else "none"


def _review_section_markdown(active: str) -> list[str]:
    opts = ("none", "watch", "candidate likely")
    lines = ["## Review / gate relevance", ""]
    for o in opts:
        mark = "**" + o + "**" if o == active else o
        lines.append(f"- {mark}")
    lines.append("")
    return lines


def main() -> int:
    ap = argparse.ArgumentParser(description="Build a handoff packet from checkpoints (+ optional brief).")
    ap.add_argument("--lane", required=True, help="Work lane (e.g. work-strategy)")
    ap.add_argument("--latest", type=int, default=3, help="Include N newest lane checkpoints (default: 3)")
    ap.add_argument(
        "--include-memory-brief",
        type=Path,
        default=None,
        help="Optional path to memory brief .md to append",
    )
    ap.add_argument(
        "--include-checkpoint",
        type=Path,
        action="append",
        default=[],
        help="Additional checkpoint file (repeatable)",
    )
    ap.add_argument("--output", "-o", type=Path, required=True, help="Output Markdown path")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help="Repository root")
    ap.add_argument(
        "--policy-mode",
        default=None,
        help="Policy mode line (default: from primary checkpoint or operator_only)",
    )
    args = ap.parse_args()

    root = args.repo_root.resolve()
    lane = args.lane.strip()
    checkpoints_dir = root / "artifacts" / "handoffs" / "checkpoints"

    pool = _collect_checkpoints(checkpoints_dir, lane)
    extra_paths = [p.resolve() for p in args.include_checkpoint]
    seen: set[Path] = set()
    ordered: list[Path] = []
    for p in pool:
        if p not in seen:
            seen.add(p)
            ordered.append(p)
    for p in extra_paths:
        if p.is_file() and p not in seen:
            seen.add(p)
            ordered.append(p)

    latest_n = max(0, args.latest)
    selected = ordered[:latest_n] if latest_n else []

    built = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    primary_text = selected[0].read_text(encoding="utf-8") if selected else ""

    objective = extract_section(primary_text, "Current objective").strip() or f"Lane `{lane}` — resume from checkpoints."
    established = section_bullets(extract_section(primary_text, "What seems established"))
    uncertain = section_bullets(extract_section(primary_text, "What remains uncertain"))
    contradictions = section_bullets(extract_section(primary_text, "Contradictions / tensions"))
    next_step = extract_section(primary_text, "Next safest step").strip() or "_(edit)_"
    review_raw = _review_gate_tag(primary_text)
    review = _normalize_handoff_review(review_raw)

    pol_line = (args.policy_mode or "").strip()
    if not pol_line and selected:
        pol_line = parse_field(primary_text, "Policy mode:") or ""
    if not pol_line:
        pol_line = "operator_only"

    lines: list[str] = [
        "# Handoff Packet",
        "",
        f"Built: {built}",
        f"Lane: {lane}",
        f"Policy mode: {pol_line}",
        "",
        "## Objective",
        objective,
        "",
        "## Recent checkpoints",
    ]
    if not selected:
        lines.append(
            "_No checkpoints matched this lane — use `--include-checkpoint` or create one with `checkpoint_session.py`._"
        )
    else:
        for p in selected:
            try:
                rel = p.relative_to(root)
            except ValueError:
                rel = p
            title = parse_field(p.read_text(encoding="utf-8"), "Title:") or p.name
            lines.append(f"- `{rel}` — {title}")

    lines.extend(
        [
            "",
            "## What is currently established",
        ]
    )
    if established:
        lines.extend(f"- {b}" for b in established)
    else:
        lines.append("- _(none synthesized — edit)_")

    lines.extend(["", "## Open uncertainties"])
    if uncertain:
        lines.extend(f"- {b}" for b in uncertain)
    else:
        lines.append("- _(edit)_")

    lines.extend(["", "## Unresolved contradictions"])
    if contradictions:
        lines.extend(f"- {b}" for b in contradictions)
    else:
        lines.append("- _(none listed)_")

    lines.extend(_review_section_markdown(review))
    lines.extend(["## Resume here", next_step, ""])

    if args.include_memory_brief is not None:
        mb = args.include_memory_brief.resolve()
        if mb.is_file():
            lines.extend(
                [
                    "## Included memory brief",
                    "",
                    "```markdown",
                    mb.read_text(encoding="utf-8").strip(),
                    "```",
                    "",
                ]
            )
        else:
            print(f"warning: memory brief not found: {mb}", file=sys.stderr)

    for cp in extra_paths:
        if cp in selected:
            continue
        if cp.is_file():
            try:
                rel = cp.relative_to(root)
            except ValueError:
                rel = cp
            lines.extend(
                [
                    f"## Additional checkpoint: `{rel}`",
                    "",
                    "```markdown",
                    cp.read_text(encoding="utf-8").strip(),
                    "```",
                    "",
                ]
            )

    if selected:
        cp = selected[0]
        try:
            rel = cp.relative_to(root)
        except ValueError:
            rel = cp
        lines.extend(
            [
                f"## Primary checkpoint (full): `{rel}`",
                "",
                "```markdown",
                cp.read_text(encoding="utf-8").strip(),
                "```",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary reminder",
            "This handoff packet is runtime-only and non-canonical.",
            "It does not update SELF, SELF-LIBRARY, SKILLS, or EVIDENCE.",
        ]
    )

    out = args.output.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
