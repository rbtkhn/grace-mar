#!/usr/bin/env python3
"""
Build a bounded prepared-context Markdown file from runtime observations by ID.

Explicit IDs and lane scope — no automatic session injection.
See docs/runtime/observation-expansion.md.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_RT = REPO_ROOT / "scripts" / "runtime"
if str(_RT) not in sys.path:
    sys.path.insert(0, str(_RT))

from observation_store import by_id  # noqa: E402
from uncertainty_envelope import compute_envelope, envelope_to_markdown_block  # noqa: E402


def _sentences_from_observations(rows: list[dict], max_sentences: int = 10) -> str:
    """Lightweight synthesis: stitch summary lines into short prose (bounded)."""
    chunks: list[str] = []
    for r in rows:
        t = (r.get("title") or "").strip()
        s = (r.get("summary") or "").strip()
        if t and s:
            chunks.append(f"{t}: {s}")
        elif s:
            chunks.append(s)
        elif t:
            chunks.append(t)
    text = " ".join(chunks)
    parts = re.split(r"(?<=[.!?])\s+", text)
    out = [p.strip() for p in parts if p.strip()]
    if len(out) > max_sentences:
        out = out[:max_sentences]
    return " ".join(out) if out else "(No summary text in selected observations.)"


def _key_points(rows: list[dict]) -> str:
    lines: list[str] = []
    for r in rows:
        oid = r.get("obs_id", "?")
        summ = (r.get("summary") or "").strip()
        if len(summ) > 200:
            summ = summ[:197] + "…"
        lines.append(f"- {summ} (`{oid}`)")
    return "\n".join(lines) if lines else "- (none)"


def _open_questions(rows: list[dict]) -> str:
    bullets: list[str] = []
    seen: set[str] = set()
    for r in rows:
        oid = r.get("obs_id", "?")
        conf = r.get("confidence")
        if isinstance(conf, (int, float)) and conf < 0.5:
            bullets.append(f"- Low confidence ({conf:g}) on `{oid}` — verify before any gate staging.")
        for c in r.get("contradiction_refs") or []:
            if c and c not in seen:
                seen.add(c)
                bullets.append(f"- Contradiction / review ref: {c} (see observations tying to this ref).")
    if not bullets:
        bullets.append(
            "- No explicit contradiction refs or sub-threshold confidence flags in this selection."
        )
        bullets.append(
            "- If promoting to Record, stage via recursion-gate.md — this file does not approve merges."
        )
    else:
        bullets.append("- Gate staging remains manual; this block is context only.")
    return "\n".join(bullets)


def main() -> int:
    p = argparse.ArgumentParser(description="Build prepared-context Markdown from runtime observation IDs.")
    p.add_argument("--lane", default=None, help="Lane label; required unless --mixed-lane")
    p.add_argument(
        "--mixed-lane",
        action="store_true",
        help="Allow observations from multiple lanes (no single-lane check)",
    )
    p.add_argument("--id", action="append", dest="ids", required=True, metavar="OBS_ID")
    p.add_argument("--output", "-o", type=Path, required=True)
    p.add_argument("--max-ids", type=int, default=8, dest="max_ids")
    args = p.parse_args()

    if not args.mixed_lane and not (args.lane and args.lane.strip()):
        print("error: --lane is required unless --mixed-lane", file=sys.stderr)
        return 2

    ids = args.ids
    if len(ids) > args.max_ids:
        print(f"error: at most {args.max_ids} id(s); got {len(ids)}", file=sys.stderr)
        return 2

    lane = (args.lane or "").strip()
    rows: list[dict] = []
    for oid in ids:
        raw = by_id(oid)
        if raw is None:
            print(f"error: missing observation id: {oid}", file=sys.stderr)
            return 2
        if not args.mixed_lane and raw.get("lane") != lane:
            print(
                f"error: observation {oid} has lane {raw.get('lane')!r}, expected {lane!r} "
                "(use --mixed-lane to allow)",
                file=sys.stderr,
            )
            return 2
        rows.append(raw)

    rows.sort(key=lambda r: r.get("timestamp") or "")

    built = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    lane_display = lane if lane else "(mixed lanes)"

    ids_block = "\n".join(f"- {r['obs_id']}" for r in rows)
    brief = _sentences_from_observations(rows)
    key_pts = _key_points(rows)
    open_q = _open_questions(rows)

    env = compute_envelope(rows)
    unc_block = envelope_to_markdown_block(env)

    content = f"""# Runtime Observation Context

Status: Runtime-only
Lane: {lane_display}
Built: {built}
Observation IDs:
{ids_block}

Boundary:
This file summarizes selected runtime observations for agent context.
It is not canonical Record truth.
It does not update SELF, SELF-LIBRARY, SKILLS, EVIDENCE, or recursion-gate.md.

## Compact Brief

{brief}

## Key Points

{key_pts}

## Open Questions / Uncertainties

{open_q}

{unc_block}
"""

    out = args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print(f"wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
