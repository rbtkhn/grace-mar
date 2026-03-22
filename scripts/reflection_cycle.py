#!/usr/bin/env python3
"""
Reflection & Proposal Cycle — evidence-grounded candidates for RECURSION-GATE.

  python scripts/reflection_cycle.py -u grace-mar --dry-run
  python scripts/reflection_cycle.py -u grace-mar --append

Requires: pip install -e ".[reflect]" and OPENAI_API_KEY for non-dry runs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))
if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))

from stage_gate_candidate import (  # noqa: E402
    insert_before_processed,
    next_candidate_id,
)
from repo_io import read_path  # noqa: E402


def _emit_event(user_id: str, event_type: str, candidate_id: str, merge: dict) -> None:
    from emit_pipeline_event import append_pipeline_event

    append_pipeline_event(user_id, event_type, candidate_id, merge=merge)


def _next_cycle_id(rp_dir: Path) -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    pat = re.compile(rf"^REFLECT-{today}-(\d{{3}})\.md$")
    seq = 0
    if rp_dir.exists():
        for p in rp_dir.iterdir():
            m = pat.match(p.name)
            if m:
                seq = max(seq, int(m.group(1)))
    return f"REFLECT-{today}-{seq + 1:03d}"


def _write_reflect_artifact(
    *,
    rp_dir: Path,
    cycle_id: str,
    result,
    bundle_meta: dict,
    raw_appendix: str | None,
) -> Path:
    rp_dir.mkdir(parents=True, exist_ok=True)
    path = rp_dir / f"{cycle_id}.md"
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines = [
        f"# {cycle_id}",
        "",
        f"- **Generated:** {ts}",
        f"- **Lookback days:** {bundle_meta.get('lookback_days')}",
        f"- **User:** {bundle_meta.get('user_id')}",
        "",
        "## Aggregate summary",
        "",
        result.aggregate_summary,
        "",
        "## Qualitative insights",
        "",
    ]
    for ins in result.qualitative_insights:
        lines.append(f"- {ins}")
    lines.extend(["", "## Critique / validation notes", ""])
    for n in result.critique_notes:
        lines.append(f"- {n}")
    lines.extend(["", "## Proposals (JSON)", "", "```json"])
    lines.append(json.dumps(result.proposals, indent=2, ensure_ascii=False))
    lines.extend(["```", ""])
    if raw_appendix:
        lines.extend(["## Raw model output", "", "```json", raw_appendix, "```", ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _update_index(
    rp_dir: Path,
    cycle_id: str,
    n_props: int,
    avg_conf: float,
    notes: str,
) -> None:
    idx = rp_dir / "index.md"
    date_s = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    row = f"| {cycle_id} | {date_s} | {n_props} | | {avg_conf:.2f} | {notes} |"
    if not idx.exists():
        header = """# Reflection Cycles

| Cycle ID | Date | Proposals | Accepted | Avg Confidence | Notes |
|----------|------|-----------|----------|----------------|-------|
"""
        idx.write_text(header + row + "\n", encoding="utf-8")
        return
    content = idx.read_text(encoding="utf-8")
    idx.write_text(content.rstrip() + "\n" + row + "\n", encoding="utf-8")


def _apply_rate_limits_on_proposals(
    proposals: list[dict],
    *,
    profile_dir: Path,
    force: bool,
) -> tuple[list[dict], list[str]]:
    from grace_mar.reflection.constants import MAX_HIGH_RISK_PER_MONTH
    from grace_mar.reflection.rate_limit import allow_high_risk_proposal

    notes: list[str] = []
    out = [dict(p) for p in proposals]
    ok, msg = allow_high_risk_proposal(profile_dir=profile_dir, force=force)
    if not ok:
        for p in out:
            if str(p.get("risk_level") or "").lower() == "high":
                p["risk_level"] = "medium"
                notes.append(f"downgraded high risk (30d cap): {msg}")

    high_idx = [i for i, p in enumerate(out) if str(p.get("risk_level") or "").lower() == "high"]
    if len(high_idx) > MAX_HIGH_RISK_PER_MONTH:
        high_idx.sort(key=lambda i: int(out[i].get("priority_score") or 0), reverse=True)
        for i in high_idx[MAX_HIGH_RISK_PER_MONTH:]:
            out[i]["risk_level"] = "medium"
        notes.append("downgraded excess high-risk proposals in this batch")

    return out, notes


def main() -> int:
    ap = argparse.ArgumentParser(description="Reflection cycle — stage evidence-grounded gate candidates")
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar").strip() or "grace-mar")
    ap.add_argument("--deep", action="store_true", help=f"Use {45} day lookback (overrides --days)")
    ap.add_argument("--days", type=int, default=None, help="Lookback days (default 14, or 45 if --deep)")
    ap.add_argument("--dry-run", action="store_true", help="Write artifacts only; no gate append or events")
    ap.add_argument("--append", action="store_true", help="Append top candidates to recursion-gate.md")
    ap.add_argument("--append-all", action="store_true", help="Append up to 5 proposals (vs default top 3)")
    ap.add_argument("--force", action="store_true", help="Bypass high-risk rate limits")
    ap.add_argument("--transcript-chars", type=int, default=120_000)
    ap.add_argument("--max-events", type=int, default=400)
    args = ap.parse_args()

    from grace_mar.reflection.constants import (
        DEFAULT_APPEND_TOP_N,
        DEFAULT_LOOKBACK_DAYS,
        DEEP_LOOKBACK_DAYS,
        MAX_PROPOSALS_PER_CYCLE,
    )
    from grace_mar.reflection.collect import collect_bundle
    from grace_mar.reflection.engine import run_reflection_engine
    from grace_mar.reflection.format_gate import build_reflection_candidate_block

    days = DEEP_LOOKBACK_DAYS if args.deep else (args.days if args.days is not None else DEFAULT_LOOKBACK_DAYS)
    profile_dir = REPO_ROOT / "users" / args.user
    gate_path = profile_dir / "recursion-gate.md"
    if not gate_path.exists():
        print(f"Missing {gate_path}", file=sys.stderr)
        return 1

    bundle = collect_bundle(
        user_id=args.user,
        repo_root=REPO_ROOT,
        lookback_days=days,
        transcript_tail_chars=args.transcript_chars,
        max_jsonl_lines=args.max_events,
        max_processed_chars=80_000,
        negative_examples_max_chars=4000,
    )
    bundle.meta["user_id"] = args.user
    bundle.meta["lookback_days"] = days

    result = run_reflection_engine(
        bundle,
        dry_run=args.dry_run,
        max_proposals=MAX_PROPOSALS_PER_CYCLE,
    )
    result.proposals, extra_notes = _apply_rate_limits_on_proposals(
        result.proposals,
        profile_dir=profile_dir,
        force=args.force,
    )
    result.critique_notes.extend(extra_notes)

    rp_dir = profile_dir / "reflection-proposals"
    cycle_id = _next_cycle_id(rp_dir)
    artifact = _write_reflect_artifact(
        rp_dir=rp_dir,
        cycle_id=cycle_id,
        result=result,
        bundle_meta=bundle.meta,
        raw_appendix=result.raw_model_json,
    )
    print(artifact)

    confs = [float(p.get("confidence") or 0) for p in result.proposals]
    avg_c = sum(confs) / len(confs) if confs else 0.0
    _update_index(rp_dir, cycle_id, len(result.proposals), avg_c, "dry-run" if args.dry_run else "run")

    if args.dry_run:
        print("Dry-run: skipped gate append and pipeline events.", file=sys.stderr)
        return 0

    top_n = MAX_PROPOSALS_PER_CYCLE if args.append_all else DEFAULT_APPEND_TOP_N
    to_append = sorted(
        result.proposals,
        key=lambda x: int(x.get("priority_score") or 0),
        reverse=True,
    )[:top_n]

    if args.append and to_append:
        full_analysis_rel = f"reflection-proposals/{cycle_id}.md"
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        full = read_path(gate_path)
        high_risk_n = sum(1 for p in to_append if str(p.get("risk_level") or "").lower() == "high")
        for prop in to_append:
            cid = next_candidate_id(full)
            block = build_reflection_candidate_block(
                candidate_id=cid,
                reflection_cycle_id=cycle_id,
                timestamp=ts,
                title_summary=str(prop.get("summary") or "")[:80],
                proposal=prop,
                full_analysis_rel=full_analysis_rel,
            )
            full = insert_before_processed(full, block)
        gate_path.write_text(full, encoding="utf-8")
        print(f"Appended {len(to_append)} candidate(s) to {gate_path}", file=sys.stderr)

        merge = {
            "event_schema": 2,
            "reflection_cycle_id": cycle_id,
            "proposals_created": len(to_append),
            "dry_run": False,
            "lookback_days": days,
            "trigger": "reflection_cycle",
            "high_risk_proposals": high_risk_n,
            "artifact": str(artifact.relative_to(REPO_ROOT)),
        }
        _emit_event(args.user, "reflection_cycle_run", "none", merge=merge)
        print("Emitted reflection_cycle_run pipeline event.", file=sys.stderr)
    elif not args.append:
        print("No --append: gate unchanged. Use --append to stage top proposals.", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
