#!/usr/bin/env python3
"""Swarm read model and operator-mediated promotion helpers."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SWARM_DIR = Path(__file__).resolve().parent
AUTO_RESEARCH_DIR = SWARM_DIR.parent
REPO_ROOT = AUTO_RESEARCH_DIR.parent
SHARED_DIR = AUTO_RESEARCH_DIR / "_shared"
SCRIPTS_DIR = REPO_ROOT / "scripts"

for path in (SHARED_DIR, SCRIPTS_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from artifact_promotion import promote_artifact_to_gate
from auto_dream import format_auto_dream_summary as _format_auto_dream_summary
from auto_dream import run_auto_dream as _run_auto_dream_job

STATE_PATH = SWARM_DIR / "swarm-state.json"
DEFAULT_USER = "grace-mar"
ARTIFACT_SOURCES = (
    {
        "lane": "self-proposals",
        "candidate_source": "auto-research/swarm",
        "accepted_dir": AUTO_RESEARCH_DIR / "self-proposals" / "accepted",
    },
    {
        "lane": "contradiction-digest",
        "candidate_source": "auto-research/swarm",
        "accepted_dir": SWARM_DIR / "accepted",
    },
)


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_relpath(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path.resolve())


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def list_swarm_artifacts() -> list[dict[str, Any]]:
    artifacts: list[dict[str, Any]] = []
    for source in ARTIFACT_SOURCES:
        accepted_dir = Path(source["accepted_dir"])
        if not accepted_dir.is_dir():
            continue
        for artifact_path in sorted(accepted_dir.glob("accepted-*.json")):
            payload = _load_json(artifact_path)
            proposal = payload.get("proposal") or {}
            candidate_bundle = proposal.get("candidate_bundle") or {}
            promoted_at = str(payload.get("promoted_to_gate_at") or "").strip()
            artifacts.append(
                {
                    "lane": source["lane"],
                    "candidate_source": source["candidate_source"],
                    "artifact_path": str(artifact_path.resolve()),
                    "artifact_relpath": _safe_relpath(artifact_path),
                    "artifact_name": artifact_path.name,
                    "hypothesis": str(proposal.get("hypothesis") or "").strip(),
                    "summary": str(candidate_bundle.get("summary") or "").strip(),
                    "scalar_at_accept": payload.get("scalar_at_accept"),
                    "promoted_to_gate_at": promoted_at,
                    "staged_candidate_id": str(payload.get("staged_candidate_id") or "").strip(),
                    "mtime": artifact_path.stat().st_mtime,
                }
            )
    artifacts.sort(key=lambda row: row["mtime"], reverse=True)
    return artifacts


def refresh_swarm_state(*, user_id: str = DEFAULT_USER) -> dict[str, Any]:
    artifacts = list_swarm_artifacts()
    pending = [row for row in artifacts if not row["promoted_to_gate_at"]]
    promoted = [row for row in artifacts if row["promoted_to_gate_at"]]
    state: dict[str, Any] = {
        "generated_at": _timestamp(),
        "user_id": user_id,
        "runner_status": "idle",
        "artifact_count": len(artifacts),
        "pending_artifact_count": len(pending),
        "promoted_artifact_count": len(promoted),
        "recent_artifacts": artifacts[:5],
        "recent_promotions": promoted[:5],
        "top_artifact": pending[0] if pending else (artifacts[0] if artifacts else None),
    }
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    return state


def read_swarm_state(*, user_id: str = DEFAULT_USER, refresh: bool = True) -> dict[str, Any]:
    if refresh or not STATE_PATH.exists():
        return refresh_swarm_state(user_id=user_id)
    return _load_json(STATE_PATH)


def format_swarm_status(state: dict[str, Any]) -> str:
    recent = state.get("recent_artifacts") or []
    lines = [
        "Swarm status",
        f"user: {state.get('user_id', DEFAULT_USER)}",
        f"runner: {state.get('runner_status', 'unknown')}",
        f"accepted artifacts: {state.get('artifact_count', 0)}",
        f"pending promotion: {state.get('pending_artifact_count', 0)}",
        f"promoted: {state.get('promoted_artifact_count', 0)}",
    ]
    if recent:
        top = recent[0]
        scalar = top.get("scalar_at_accept")
        scalar_text = f"{float(scalar):.2f}" if isinstance(scalar, (int, float)) else "n/a"
        lines.extend(
            [
                "",
                f"latest: {top['artifact_relpath']}",
                f"lane: {top['lane']}",
                f"scalar: {scalar_text}",
                f"summary: {top.get('summary') or '(no summary)'}",
            ]
        )
    else:
        lines.extend(["", "No accepted artifacts found yet."])
    return "\n".join(lines)


def format_last_artifact(summary: dict[str, Any] | None) -> str:
    if not summary:
        return "No swarm-visible artifacts found yet."
    lines = [
        "Latest swarm artifact",
        f"path: {summary['artifact_relpath']}",
        f"lane: {summary['lane']}",
    ]
    scalar = summary.get("scalar_at_accept")
    if isinstance(scalar, (int, float)):
        lines.append(f"scalar_at_accept: {scalar:.2f}")
    if summary.get("summary"):
        lines.append(f"summary: {summary['summary']}")
    if summary.get("hypothesis"):
        lines.append(f"hypothesis: {summary['hypothesis']}")
    if summary.get("staged_candidate_id"):
        lines.append(f"staged_candidate: {summary['staged_candidate_id']}")
    elif summary.get("promoted_to_gate_at"):
        lines.append("staged_candidate: recorded without candidate id")
    else:
        lines.append("staged_candidate: not promoted yet")
    return "\n".join(lines)


def get_latest_artifact(*, pending_first: bool = True) -> dict[str, Any] | None:
    artifacts = list_swarm_artifacts()
    if not artifacts:
        return None
    if not pending_first:
        return artifacts[0]
    for artifact in artifacts:
        if not artifact["promoted_to_gate_at"]:
            return artifact
    return artifacts[0]


def resolve_artifact_reference(reference: str) -> dict[str, Any]:
    ref = (reference or "").strip()
    if not ref or ref.lower() in {"latest", "last"}:
        artifact = get_latest_artifact()
        if artifact is None:
            raise ValueError("No accepted artifact found to promote")
        return artifact

    requested = Path(ref)
    candidates = list_swarm_artifacts()
    if requested.is_absolute():
        absolute = requested.resolve()
    else:
        absolute = (REPO_ROOT / requested).resolve()
    for artifact in candidates:
        if Path(artifact["artifact_path"]).resolve() == absolute:
            return artifact
    for artifact in candidates:
        if artifact["artifact_relpath"] == ref or artifact["artifact_name"] == ref:
            return artifact
    raise ValueError(f"Unknown swarm artifact reference: {reference}")


def promote_swarm_artifact(
    artifact_reference: str,
    *,
    review_note: str,
    user_id: str = DEFAULT_USER,
    dry_run: bool = False,
) -> dict[str, Any]:
    artifact = resolve_artifact_reference(artifact_reference)
    result = promote_artifact_to_gate(
        Path(artifact["artifact_path"]),
        user_id=user_id,
        review_note=review_note,
        dry_run=dry_run,
        lane_name="swarm",
        candidate_source=str(artifact["candidate_source"]),
        extra_auto_research_metadata={
            "swarm_origin_lane": artifact["lane"],
        },
    )
    state = refresh_swarm_state(user_id=user_id)
    result["swarm_state"] = state
    return result


def run_auto_dream(
    *,
    user_id: str = DEFAULT_USER,
    dry_run: bool = False,
) -> dict[str, Any]:
    return _run_auto_dream_job(
        user_id=user_id,
        apply=not dry_run,
        emit_event=not dry_run,
        write_artifacts=not dry_run,
    )


def format_auto_dream_status(summary: dict[str, Any]) -> str:
    return _format_auto_dream_summary(summary)


def main() -> int:
    parser = argparse.ArgumentParser(description="Swarm read model and promotion helpers")
    parser.add_argument("--user", "-u", default=DEFAULT_USER, help="User id (default: grace-mar)")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Refresh swarm-state.json and print a summary")
    sub.add_parser("last", help="Show the latest accepted artifact visible to the swarm bridge")
    dream = sub.add_parser("dream", help="Run bounded autoDream maintenance and print a summary")
    dream.add_argument("--dry-run", action="store_true", help="Inspect maintenance output without writing files")

    promote = sub.add_parser("promote", help="Promote an accepted artifact through the shared gate helper")
    promote.add_argument("artifact", help="Artifact path, filename, or 'latest'")
    promote.add_argument("--review-note", default="", help="Required unless --dry-run is used")
    promote.add_argument("--dry-run", action="store_true", help="Render candidate block without writing")

    args = parser.parse_args()
    try:
        if args.command == "status":
            print(format_swarm_status(refresh_swarm_state(user_id=args.user)))
            return 0
        if args.command == "last":
            print(format_last_artifact(get_latest_artifact()))
            return 0
        if args.command == "dream":
            print(format_auto_dream_status(run_auto_dream(user_id=args.user, dry_run=args.dry_run)))
            return 0
        if args.command == "promote":
            result = promote_swarm_artifact(
                args.artifact,
                review_note=args.review_note,
                user_id=args.user,
                dry_run=args.dry_run,
            )
            if args.dry_run:
                print(result["candidate_block"])
            else:
                print(
                    f"{result['gate_path']}: inserted {result['candidate_id']} from {result['artifact_relpath']}"
                )
            return 0
    except ValueError as exc:
        raise SystemExit(str(exc))
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
