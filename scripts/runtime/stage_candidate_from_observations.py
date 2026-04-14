#!/usr/bin/env python3
"""
Stage a RECURSION-GATE candidate from runtime observations with provenance YAML.

Writes ### CANDIDATE-NNNN + YAML (proposal_class RUNTIME_OBSERVATION_PROPOSAL).
Stages only; does not merge the Record. See docs/runtime/provenance-staging.md.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
_RUNTIME = REPO_ROOT / "scripts" / "runtime"
for p in (_SCRIPTS, _RUNTIME):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from observation_store import by_id  # noqa: E402
from repo_io import profile_dir, read_path  # noqa: E402
from search_scoring import parse_obs_timestamp  # noqa: E402
from policy_mode_config import load_defaults, resolve_mode, staging_decision  # noqa: E402
from stage_gate_candidate import (  # noqa: E402
    build_block,
    convergence_check,
    insert_before_processed,
    next_candidate_id,
)

try:
    from recursion_gate_territory import TERRITORY_WORK_POLITICS
except ImportError:
    from scripts.recursion_gate_territory import TERRITORY_WORK_POLITICS  # noqa: E402

DEFAULT_USER = "grace-mar"

CANDIDATE_TYPES = (
    "identity_update",
    "library_update",
    "skill_update",
    "evidence_link",
    "boundary_rule",
    "notebook_promotion",
    "correction",
    "other",
)
TARGET_SURFACES = ("SELF", "SELF-LIBRARY", "SKILLS", "EVIDENCE", "OTHER")

SCHEMA_PATH = REPO_ROOT / "schema-registry" / "recursion-gate-candidate.schema.json"

DEFAULT_REVIEW_NOTES = (
    "Runtime observations support this candidate, but no approval has occurred."
)


def _sort_obs_by_time(rows: list[dict]) -> list[dict]:
    def key(r: dict) -> tuple[float, str]:
        ts = r.get("timestamp") or ""
        dt = parse_obs_timestamp(ts) if ts else None
        if dt is not None:
            return (dt.timestamp(), ts)
        return (0.0, ts)

    return sorted(rows, key=key)


def _validate_payload(payload: dict) -> None:
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("warning: jsonschema not installed; skipping schema validation", file=sys.stderr)
        return
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator(schema).validate(payload)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Stage gate candidate with runtime observation provenance (RUNTIME_OBSERVATION_PROPOSAL)."
    )
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER)
    ap.add_argument("--lane", required=True, help="Lane all source observations must belong to (unless --allow-mixed-lane)")
    ap.add_argument(
        "--id",
        "--obs-id",
        action="append",
        dest="obs_ids",
        default=[],
        required=True,
        help="Runtime observation id(s); repeat flag",
    )
    ap.add_argument(
        "--candidate-type",
        required=True,
        choices=CANDIDATE_TYPES,
        help="Semantic candidate type",
    )
    ap.add_argument("--target-surface", required=True, choices=TARGET_SURFACES)
    ap.add_argument("--target-path", default=None, help="Optional path hint (repo-relative)")
    ap.add_argument(
        "--proposal-summary",
        "--summary",
        dest="proposal_summary",
        required=True,
        help="One-line summary for gate YAML",
    )
    ap.add_argument("--proposed-change", required=True, help="Proposed change (bounded; becomes YAML proposed_change)")
    ap.add_argument("--why-now", default=None, help="Why this is reviewable now")
    ap.add_argument("--review-notes", default=None, help="Reviewer-facing notes")
    ap.add_argument(
        "--timeline-anchor",
        default=None,
        help="Override timeline anchor obs_id (default: earliest observation by timestamp)",
    )
    ap.add_argument(
        "--confidence",
        type=float,
        default=None,
        help="Override aggregated confidence (0..1); default mean of observation confidences",
    )
    ap.add_argument(
        "--allow-mixed-lane",
        action="store_true",
        help="Allow observations whose lane differs from --lane",
    )
    ap.add_argument(
        "--mind",
        choices=("knowledge", "curiosity", "personality"),
        default="knowledge",
    )
    ap.add_argument(
        "--territory",
        choices=("companion", "work-politics"),
        default="companion",
    )
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument(
        "--policy-mode",
        default=None,
        help="Policy envelope (default: GRACE_MAR_POLICY_MODE or operator_only); see docs/policy-modes.md",
    )
    ap.add_argument(
        "--policy-ack",
        action="store_true",
        help="Acknowledge policy warn/hold (identity_bound SELF, high_risk_abstention) to proceed",
    )
    args = ap.parse_args()

    pdefs = load_defaults()
    pol = resolve_mode(args.policy_mode, pdefs)
    verb, reason = staging_decision(pol, args.target_surface, pdefs)
    if verb == "blocked":
        print(f"error: policy mode {pol}: {reason}", file=sys.stderr)
        return 2
    if verb in ("warn", "hold_hint") and not args.policy_ack:
        print(f"error: policy mode {pol}: {reason} Pass --policy-ack to proceed.", file=sys.stderr)
        return 2
    if verb in ("warn", "hold_hint") and args.policy_ack:
        print(f"warning: policy mode {pol} override acknowledged: {reason}", file=sys.stderr)

    obs_rows: list[dict] = []
    for oid in args.obs_ids:
        row = by_id(oid)
        if row is None:
            print(f"error: observation not found: {oid}", file=sys.stderr)
            return 2
        if not args.allow_mixed_lane and row.get("lane") != args.lane:
            print(f"error: observation outside lane {args.lane}: {oid}", file=sys.stderr)
            return 2
        obs_rows.append(row)

    sorted_rows = _sort_obs_by_time(obs_rows)
    anchor_id = args.timeline_anchor
    if anchor_id is None:
        anchor_id = sorted_rows[0].get("obs_id")
    else:
        ids_sel = {r.get("obs_id") for r in obs_rows}
        if anchor_id not in ids_sel:
            print(f"error: --timeline-anchor not among selected observations: {anchor_id}", file=sys.stderr)
            return 2

    supporting: list[str] = []
    contradictions: list[str] = []
    confidences: list[float] = []
    for r in obs_rows:
        supporting.extend(r.get("source_refs") or [])
        contradictions.extend(r.get("contradiction_refs") or [])
        conf = r.get("confidence")
        if isinstance(conf, (int, float)):
            confidences.append(float(conf))

    supporting_u = sorted(set(supporting))
    contradictions_u = sorted(set(contradictions))

    if args.confidence is not None:
        agg_conf = max(0.0, min(1.0, float(args.confidence)))
    elif confidences:
        agg_conf = sum(confidences) / len(confidences)
    else:
        agg_conf = None

    review_notes = args.review_notes.strip() if args.review_notes else DEFAULT_REVIEW_NOTES

    body_lines = ["## Provenance digest\n", f"Derived from runtime observations: {', '.join(args.obs_ids)}\n\n"]
    for r in sorted_rows:
        body_lines.append(f"### {r.get('obs_id')} ({r.get('title')})\n\n")
        body_lines.append((r.get("summary") or "") + "\n\n")
    body = "".join(body_lines)

    title = (args.proposal_summary.strip()[:56] + "…") if len(args.proposal_summary.strip()) > 56 else args.proposal_summary.strip()

    ts_wall = datetime.now(timezone.utc)
    ts = ts_wall.strftime("%Y-%m-%d %H:%M:%S")
    created_at = ts_wall.isoformat().replace("+00:00", "Z")

    tp = args.target_path
    if tp is not None and not str(tp).strip():
        tp = None

    gate_path = profile_dir(args.user) / "recursion-gate.md"
    if not gate_path.exists():
        print(f"Missing {gate_path}", file=sys.stderr)
        return 1
    full = read_path(gate_path)
    if "## Candidates" not in full or "## Processed" not in full:
        print(f"{gate_path}: need ## Candidates and ## Processed", file=sys.stderr)
        return 1

    cid = next_candidate_id(full)

    source_ids_ordered = [r.get("obs_id") for r in sorted_rows if r.get("obs_id")]
    payload = {
        "gate_candidate_id": cid,
        "created_at": created_at,
        "candidate_type": args.candidate_type,
        "target_surface": args.target_surface,
        "target_path": tp,
        "proposal_summary": args.proposal_summary.strip(),
        "proposed_change": args.proposed_change.strip(),
        "source_observation_ids": source_ids_ordered,
        "timeline_anchor": anchor_id,
        "lane_origin": args.lane,
        "supporting_evidence_refs": supporting_u,
        "contradiction_refs": contradictions_u,
        "confidence": agg_conf,
        "why_now": args.why_now.strip() if args.why_now else None,
        "review_notes": review_notes,
        "status": "pending",
    }

    try:
        _validate_payload(payload)
    except Exception as exc:
        print(f"error: schema validation failed: {exc}", file=sys.stderr)
        return 2

    provenance = {
        "source_observation_ids": source_ids_ordered,
        "timeline_anchor": anchor_id,
        "lane_origin": args.lane,
        "supporting_evidence_refs": supporting_u,
        "contradiction_refs": contradictions_u,
    }

    runtime_work = {
        "candidate_type": args.candidate_type,
        "target_surface": args.target_surface,
        "target_path": tp,
        "proposal_summary": args.proposal_summary.strip(),
        "proposed_change": args.proposed_change.strip(),
        "why_now": args.why_now.strip() if args.why_now else None,
        "review_notes": review_notes,
        "confidence": agg_conf,
    }

    if args.territory == "work-politics":
        territory = TERRITORY_WORK_POLITICS
        channel_key = "operator:wap:observation-stage"
    else:
        territory = None
        channel_key = "operator:cursor:observation-stage"

    conv = convergence_check(full, args.proposal_summary, body + args.proposed_change)
    block = build_block(
        candidate_id=cid,
        title=title,
        summary=args.proposal_summary.strip(),
        body=body,
        mind_category=args.mind,
        channel_key=channel_key,
        territory=territory,
        timestamp=ts,
        convergence=conv,
        provenance=provenance,
        runtime_work_proposal=runtime_work,
    )

    if args.dry_run:
        print(block)
        print(cid, file=sys.stderr)
        return 0

    new_full = insert_before_processed(full, block)
    gate_path.write_text(new_full, encoding="utf-8")
    print(cid)
    print(f"{gate_path}: inserted {cid}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
