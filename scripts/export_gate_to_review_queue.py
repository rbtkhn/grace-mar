#!/usr/bin/env python3
"""
Bridge: copy a RECURSION-GATE candidate into the material change-review queue.

Reads users/<id>/recursion-gate.md via gate_block_parser, writes:
  - review-queue/proposals/proposal-gate-<id>.json
  - review-queue/derived/gate-escalation-<id>.json  (proposedStateRef target)
  - updates change_review_queue.json and change_event_log.json

Usage:
  python3 scripts/export_gate_to_review_queue.py --user grace-mar --candidate-id CANDIDATE-0042
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Tuple

try:
    from gate_block_parser import iter_candidate_yaml_blocks, pending_candidates_region
except ImportError:
    from scripts.gate_block_parser import iter_candidate_yaml_blocks, pending_candidates_region

try:
    from repo_io import REPO_ROOT, profile_dir
except ImportError:
    from scripts.repo_io import REPO_ROOT, profile_dir


def _extract_scalar(yaml_body: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", yaml_body, re.MULTILINE)
    if not m:
        return ""
    return m.group(1).strip().strip("\"'")


def _mind_to_scope(yaml_body: str) -> str:
    mc = _extract_scalar(yaml_body, "mind_category").lower()
    if mc == "curiosity":
        return "curiosity"
    if mc == "personality":
        return "preference"
    if mc == "knowledge":
        return "identity"
    return "preference"


def _find_candidate(gate_text: str, candidate_id: str) -> Tuple[str, str, str]:
    region = pending_candidates_region(gate_text)
    for cid, title, yaml_body in iter_candidate_yaml_blocks(region):
        if cid == candidate_id:
            return cid, title, yaml_body
    raise ValueError(f"Candidate {candidate_id} not found in pending Candidates section of recursion-gate.md")


def _proposal_slug(candidate_id: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", candidate_id).strip("-")
    return f"proposal-gate-{safe}"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a gate candidate to the change-review queue.")
    parser.add_argument("--user", "-u", required=True, help="Fork id (e.g. grace-mar)")
    parser.add_argument("--candidate-id", required=True, help="e.g. CANDIDATE-0042")
    args = parser.parse_args()

    user = args.user
    candidate_id = args.candidate_id.strip()
    if not re.match(r"^CANDIDATE-\d+$", candidate_id):
        print("ERROR: --candidate-id must look like CANDIDATE-<digits>", file=sys.stderr)
        return 2

    gate_path = profile_dir(user) / "recursion-gate.md"
    if not gate_path.is_file():
        print(f"ERROR: missing gate file: {gate_path}", file=sys.stderr)
        return 2

    gate_text = gate_path.read_text(encoding="utf-8")
    try:
        cid, title, yaml_body = _find_candidate(gate_text, candidate_id)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    review_root = profile_dir(user) / "review-queue"
    review_root.mkdir(parents=True, exist_ok=True)
    for sub in ("proposals", "decisions", "diffs", "derived"):
        (review_root / sub).mkdir(parents=True, exist_ok=True)

    proposal_id = _proposal_slug(cid)
    derived_name = f"gate-escalation-{cid}.json"
    derived_rel = f"derived/{derived_name}"
    derived_path = review_root / derived_rel

    summary_line = _extract_scalar(yaml_body, "summary") or title or f"Escalated {cid}"
    pri_scope = _mind_to_scope(yaml_body)

    derived_doc: Dict[str, Any] = {
        "schemaVersion": "1.0.0",
        "kind": "gate_escalation_snapshot",
        "candidateId": cid,
        "exportedAt": _utc_now(),
        "title": title,
        "yamlBody": yaml_body,
    }
    derived_path.write_text(json.dumps(derived_doc, indent=2) + "\n", encoding="utf-8")

    prior_ref = f"users/{user}/recursion-gate.md#{cid}"
    proposal: Dict[str, Any] = {
        "schemaVersion": "1.0.0",
        "proposalId": proposal_id,
        "userSlug": user,
        "createdAt": _utc_now(),
        "primaryScope": pri_scope,
        "secondaryScopes": [],
        "changeType": "refinement",
        "priorStateRef": prior_ref,
        "proposedStateRef": derived_rel,
        "supportingEvidence": [
            {
                "type": "policy_signal",
                "ref": f"session-gate-export-{cid}",
                "summary": summary_line[:500],
            }
        ],
        "riskLevel": "medium",
        "status": "proposed",
        "notes": f"Escalated from recursion-gate candidate {cid}. Review YAML in {derived_rel}.",
    }

    proposal_path = review_root / "proposals" / f"{proposal_id}.json"
    if proposal_path.is_file():
        print(f"ERROR: proposal already exists: {proposal_path}", file=sys.stderr)
        return 2
    proposal_path.write_text(json.dumps(proposal, indent=2) + "\n", encoding="utf-8")

    queue_path = review_root / "change_review_queue.json"
    if queue_path.is_file():
        queue = json.loads(queue_path.read_text(encoding="utf-8"))
    else:
        queue = {
            "schemaVersion": "1.0.0",
            "userSlug": user,
            "queueGeneratedAt": _utc_now(),
            "items": [],
        }

    items = queue.get("items") or []
    if any(x.get("proposalId") == proposal_id for x in items):
        print(f"ERROR: queue already references {proposal_id}", file=sys.stderr)
        return 2

    items.append(
        {
            "proposalId": proposal_id,
            "status": "proposed",
            "priority": "medium",
            "summary": summary_line[:400] if summary_line else f"Gate escalation {cid}",
        }
    )
    queue["items"] = items
    queue["queueGeneratedAt"] = _utc_now()
    queue["userSlug"] = user
    queue_path.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")

    event_path = review_root / "change_event_log.json"
    if event_path.is_file():
        event_log = json.loads(event_path.read_text(encoding="utf-8"))
    else:
        event_log = {"schemaVersion": "1.0.0", "userSlug": user, "events": []}

    ev_id = f"event-gate-export-{cid.lower()}"
    ref_path = f"proposals/{proposal_id}.json"
    event_log.setdefault("events", []).append(
        {
            "eventId": ev_id,
            "timestamp": _utc_now(),
            "eventType": "proposal_created",
            "ref": ref_path,
            "summary": f"Exported {cid} from recursion-gate to change-review.",
        }
    )
    event_path.write_text(json.dumps(event_log, indent=2) + "\n", encoding="utf-8")

    print(f"Wrote {proposal_path.relative_to(REPO_ROOT)}")
    print(f"Updated queue and event log under {review_root.relative_to(REPO_ROOT)}")
    print(
        "Validate (strict mode requires decisions/diffs; use --allow-empty after export):",
        f"python3 scripts/validate-change-review.py {review_root.relative_to(REPO_ROOT)} --allow-empty",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
