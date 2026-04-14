#!/usr/bin/env python3
"""
Emit a session checkpoint Markdown file under artifacts/handoffs/checkpoints/.

Runtime work artifact only — does not update SELF, SKILLS, EVIDENCE, or the gate.
See docs/runtime/long-horizon-work.md.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

_RUNTIME = Path(__file__).resolve().parent
if str(_RUNTIME) not in sys.path:
    sys.path.insert(0, str(_RUNTIME))

from checkpoint_handoff_common import seeds_from_memory_brief, slug  # noqa: E402
from policy_mode_config import load_defaults, resolve_mode  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

GATE_RELEVANCE = ("none", "maybe later", "candidate likely")


def _build_markdown(
    *,
    built: str,
    lane: str,
    title: str,
    policy_mode: str,
    status: str,
    gate_relevance: str,
    objective: str,
    established: list[str],
) -> str:
    def bullets(items: list[str], default: str = "- _(edit)_") -> str:
        if not items:
            return f"{default}\n"
        return "".join(f"- {b}\n" for b in items)

    est = bullets(established)
    return f"""# Session Checkpoint

Built: {built}
Lane: {lane}
Title: {title}
Policy mode: {policy_mode}
Status: {status}

## Current objective
{objective}

## What seems established
{est}## What remains uncertain
- _(edit)_

## Contradictions / tensions
- _(edit)_

## Decisions made
- _(edit)_

## Decisions deferred
- _(edit)_

## Next safest step
_(One bounded next move.)_

## Gate relevance
{gate_relevance}

## Boundary reminder
This checkpoint is a runtime work artifact.
It does not update SELF, SELF-LIBRARY, SKILLS, or EVIDENCE.
"""


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Write a session checkpoint under artifacts/handoffs/checkpoints/.",
    )
    ap.add_argument("--lane", required=True, help="Work lane (e.g. work-strategy)")
    ap.add_argument("--title", required=True, help="Short title for this checkpoint")
    ap.add_argument(
        "--from-memory-brief",
        type=Path,
        default=None,
        help="Optional memory brief .md to seed objective and established bullets",
    )
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT, help="Repository root")
    ap.add_argument("--status", default="in-progress", help="Status line (default: in-progress)")
    ap.add_argument(
        "--gate-relevance",
        choices=GATE_RELEVANCE,
        default="none",
        help="Visibility for drift toward durable proposals (default: none)",
    )
    ap.add_argument(
        "--policy-mode",
        default=None,
        help="Policy envelope (default: GRACE_MAR_POLICY_MODE or operator_only)",
    )
    args = ap.parse_args()

    root = args.repo_root.resolve()
    pdefs = load_defaults()
    policy_resolved = resolve_mode(args.policy_mode, pdefs)
    lane = args.lane.strip()
    title = args.title.strip()
    built = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    objective = f"_(edit)_ What this work run is trying to accomplish — {title!r}."
    established: list[str] = []
    if args.from_memory_brief is not None:
        mb = args.from_memory_brief.resolve()
        objective, established = seeds_from_memory_brief(mb)

    lane_slug = slug(lane)
    title_slug = slug(title)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    base = f"{day}_{lane_slug}_{title_slug}"
    out_dir = root / "artifacts" / "handoffs" / "checkpoints"
    out_dir.mkdir(parents=True, exist_ok=True)

    candidate = out_dir / f"{base}.md"
    n = 0
    while candidate.is_file():
        n += 1
        candidate = out_dir / f"{base}-{n}.md"

    body = _build_markdown(
        built=built,
        lane=lane,
        title=title,
        policy_mode=policy_resolved,
        status=args.status,
        gate_relevance=args.gate_relevance,
        objective=objective,
        established=established,
    )
    candidate.write_text(body, encoding="utf-8")
    print(f"wrote {candidate}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
