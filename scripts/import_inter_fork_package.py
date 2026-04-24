#!/usr/bin/env python3
"""
Import a bounded inter-fork collaboration package into recipient-owned review surfaces.

The importer is the only place where recipient-side writes happen. Sender forks do
not write directly into recipient namespaces.
"""

from __future__ import annotations

import argparse
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Any

try:
    import jsonschema
except ImportError:  # pragma: no cover - optional dependency
    jsonschema = None  # type: ignore[assignment]

try:
    from repo_io import DEFAULT_USER_ID, profile_dir
    from stage_gate_candidate import insert_before_processed, next_candidate_id
except ImportError:
    from scripts.repo_io import DEFAULT_USER_ID, profile_dir
    from scripts.stage_gate_candidate import insert_before_processed, next_candidate_id

REPO_ROOT = Path(__file__).resolve().parent.parent


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _utc_now_display() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _load_schema(repo_root: Path) -> dict:
    return json.loads((repo_root / "schema-registry" / "inter-fork-package-envelope.v1.json").read_text(encoding="utf-8"))


def _rel(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _yaml_escape(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _slug(text: str, max_len: int = 56) -> str:
    line = " ".join(text.splitlines()[:1]).strip() or "inter-fork import"
    if len(line) > max_len:
        return line[: max_len - 1].rstrip() + "…"
    return line


def _profile_target_label(target_surface: str) -> str:
    return {
        "self": "SELF — recipient review",
        "self_library": "SELF-LIBRARY — recipient review",
        "civ_mem": "CIV-MEM — recipient review",
        "skills": "SKILLS — recipient review",
        "evidence": "EVIDENCE — recipient review",
        "work_layer": "WORK — recipient review",
    }.get(target_surface, "RECIPIENT REVIEW")


def _priority_from_risk(risk_level: str) -> str:
    return "high" if risk_level == "high" else "medium" if risk_level == "medium" else "low"


def _proposal_class_for_surface(target_surface: str) -> str:
    return {
        "self": "identity",
        "self_library": "library",
        "civ_mem": "library",
        "skills": "skills",
        "evidence": "evidence",
        "work_layer": "policy",
    }.get(target_surface, "policy")


def _assert_recipient_owned(path: Path, recipient_root: Path) -> None:
    resolved = path.resolve()
    if recipient_root.resolve() not in (resolved, *resolved.parents):
        raise ValueError(f"Refusing to write outside recipient-owned namespace: {path}")


def _copy_package_into_recipient_namespace(
    package_path: Path,
    *,
    package_id: str,
    recipient_root: Path,
) -> Path:
    import_dir = recipient_root / "artifacts" / "inter-fork" / "imports"
    import_dir.mkdir(parents=True, exist_ok=True)
    copied_path = import_dir / f"{package_id}.json"
    _assert_recipient_owned(copied_path, recipient_root)
    copied_path.write_text(package_path.read_text(encoding="utf-8"), encoding="utf-8")
    return copied_path


def _receipt_path(*, package_id: str, recipient_root: Path) -> Path:
    receipt = recipient_root / "artifacts" / "inter-fork" / "imports" / f"{package_id}.receipt.json"
    _assert_recipient_owned(receipt, recipient_root)
    return receipt


def _build_candidate_block(
    *,
    package: dict[str, Any],
    copied_package_ref: str,
) -> str:
    summary = str(package["summary"]).strip()
    payload = package["payload"]
    target_surface = payload.get("suggestedTargetSurface", "work_layer")
    review_body = package.get("body", "").strip() or payload.get("claim", "").strip() or summary
    supporting_refs = [copied_package_ref, *[ref for ref in package.get("supportingRefs", []) if isinstance(ref, str) and ref.strip()]]
    title = _slug(summary)
    timestamp = _utc_now_display()
    lines = [
        f"### {{candidate_id}} ({title})",
        "",
        "```yaml",
        "status: pending",
        f"timestamp: {timestamp}",
        "channel_key: operator:inter-fork:import",
        "proposal_class: INTER_FORK_PACKAGE",
        "source: operator — scripts/import_inter_fork_package.py",
        "source_exchange:",
        "  operator: |",
    ]
    for line in review_body.splitlines() or [summary]:
        lines.append(f"    {line}")
    lines.extend(
        [
            "mind_category: knowledge",
            "signal_type: inter_fork_package_import",
            "priority_score: 3",
            f"summary: {_yaml_escape(summary[:200])}",
            f"source_fork_id: {_yaml_escape(str(package['senderForkId']))}",
            f"package_id: {_yaml_escape(str(package['packageId']))}",
            f"package_kind: {_yaml_escape(str(package['packageKind']))}",
            f"routing_hint: {_yaml_escape(str(package['routingHint']))}",
            f"profile_target: {_yaml_escape(_profile_target_label(str(target_surface)))}",
            f"suggested_entry: {_yaml_escape(payload.get('claim') or 'See imported inter-fork package and supporting refs.')}",
            "prompt_section: REVIEW_REQUIRED",
            "prompt_addition: none",
        ]
    )
    if payload.get("reviewNotes"):
        lines.append(f"review_notes: {_yaml_escape(str(payload['reviewNotes'])[:400])}")
    if supporting_refs:
        lines.append("supporting_evidence_refs:")
        for ref in supporting_refs:
            lines.append(f"  - {_yaml_escape(ref)}")
    lines.extend(["```", ""])
    return "\n".join(lines)


def _normalize_queue(queue: dict[str, Any] | None, *, user_slug: str) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    if isinstance(queue, dict):
        raw_items = queue.get("items")
        if not isinstance(raw_items, list):
            raw_items = queue.get("queue")
        if isinstance(raw_items, list):
            items = [item for item in raw_items if isinstance(item, dict)]
    return {
        "schemaVersion": "1.0.0",
        "userSlug": user_slug,
        "queueGeneratedAt": _utc_now_iso(),
        "items": items,
    }


def _normalize_event_log(event_log: dict[str, Any] | None, *, user_slug: str) -> dict[str, Any]:
    events: list[dict[str, Any]] = []
    if isinstance(event_log, dict) and isinstance(event_log.get("events"), list):
        events = [event for event in event_log["events"] if isinstance(event, dict)]
    return {
        "schemaVersion": "1.0.0",
        "userSlug": user_slug,
        "events": events,
    }


def _load_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _existing_supporting_refs(package: dict[str, Any], repo_root: Path) -> list[str]:
    refs: list[str] = []
    for ref in package.get("supportingRefs", []):
        if not isinstance(ref, str) or not ref.strip():
            continue
        candidate = repo_root / ref
        if candidate.exists():
            refs.append(ref)
    return refs


def _build_change_proposal(
    *,
    package: dict[str, Any],
    recipient_fork_id: str,
    copied_package_ref: str,
    repo_root: Path,
) -> dict[str, Any]:
    payload = package["payload"]
    extra_refs = _existing_supporting_refs(package, repo_root)
    supporting = [
        {
            "type": "manual_note",
            "ref": copied_package_ref,
            "summary": f"Imported inter-fork package from {package['senderForkId']}",
        }
    ]
    for ref in extra_refs:
        supporting.append(
            {
                "type": "manual_note",
                "ref": ref,
                "summary": f"Supporting ref forwarded by sender package: {ref}",
            }
        )
    notes = str(payload.get("notes", "")).strip()
    unresolved = [ref for ref in package.get("supportingRefs", []) if isinstance(ref, str) and ref.strip() and ref not in extra_refs]
    if unresolved:
        unresolved_text = "Sender refs not present in recipient repo: " + ", ".join(unresolved)
        notes = f"{notes}\n\n{unresolved_text}".strip()
    proposal = {
        "schemaVersion": "1.0.0",
        "proposalId": f"proposal-{package['packageId']}",
        "userSlug": recipient_fork_id,
        "createdAt": _utc_now_iso(),
        "primaryScope": payload["primaryScope"],
        "secondaryScopes": payload.get("secondaryScopes", []),
        "changeType": payload["changeType"],
        "priorStateRef": payload["priorStateRef"],
        "proposedStateRef": payload["proposedStateRef"],
        "supportingEvidence": supporting,
        "riskLevel": payload["riskLevel"],
        "status": "proposed",
        "targetSurface": payload["targetSurface"],
        "materiality": payload["materiality"],
        "reviewType": payload["reviewType"],
        "queueSummary": package["summary"],
        "proposalClass": payload.get("proposalClass") or _proposal_class_for_surface(payload["targetSurface"]),
    }
    if notes:
        proposal["notes"] = notes
    return proposal


def import_inter_fork_package(
    *,
    package_path: Path,
    recipient_fork_id: str,
    repo_root: Path = REPO_ROOT,
    profile_lookup: Callable[[str], Path] = profile_dir,
    validate_schema: bool = True,
    dry_run: bool = False,
) -> dict[str, Any]:
    package = json.loads(package_path.read_text(encoding="utf-8"))
    if validate_schema and jsonschema is not None:
        jsonschema.Draft202012Validator(_load_schema(repo_root)).validate(package)
    if package.get("format") != "grace-mar-inter-fork-package":
        raise ValueError("Unsupported inter-fork package format")
    if package.get("intendedRecipientForkId") != recipient_fork_id:
        raise ValueError("Package recipient does not match the importer recipient fork id")
    payload = package.get("payload") or {}
    if payload.get("mode") != package.get("routingHint"):
        raise ValueError("Package routingHint does not match payload.mode")

    recipient_root = profile_lookup(recipient_fork_id)
    receipt_path = _receipt_path(package_id=str(package["packageId"]), recipient_root=recipient_root)
    written_paths: list[str] = []
    copied_package_path = recipient_root / "artifacts" / "inter-fork" / "imports" / f"{package['packageId']}.json"
    copied_package_ref = _rel(copied_package_path, repo_root)

    if dry_run:
        if package["routingHint"] == "candidate_import":
            written_paths.append(_rel(recipient_root / "recursion-gate.md", repo_root))
        else:
            written_paths.extend(
                [
                    _rel(recipient_root / "review-queue" / "proposals" / f"proposal-{package['packageId']}.json", repo_root),
                    _rel(recipient_root / "review-queue" / "change_review_queue.json", repo_root),
                    _rel(recipient_root / "review-queue" / "change_event_log.json", repo_root),
                ]
            )
        written_paths.extend([copied_package_ref, _rel(receipt_path, repo_root)])
        return {"importMode": package["routingHint"], "writtenPaths": written_paths, "dryRun": True}

    copied_package_path = _copy_package_into_recipient_namespace(package_path, package_id=str(package["packageId"]), recipient_root=recipient_root)
    written_paths.append(_rel(copied_package_path, repo_root))

    if package["routingHint"] == "candidate_import":
        gate_path = recipient_root / "recursion-gate.md"
        gate_content = gate_path.read_text(encoding="utf-8")
        candidate_id = next_candidate_id(gate_content)
        block = _build_candidate_block(package=package, copied_package_ref=copied_package_ref).replace(
            "{candidate_id}",
            candidate_id,
        )
        gate_path.write_text(insert_before_processed(gate_content, block), encoding="utf-8")
        written_paths.append(_rel(gate_path, repo_root))
    else:
        review_dir = recipient_root / "review-queue"
        proposals_dir = review_dir / "proposals"
        proposals_dir.mkdir(parents=True, exist_ok=True)
        proposal = _build_change_proposal(
            package=package,
            recipient_fork_id=recipient_fork_id,
            copied_package_ref=copied_package_ref,
            repo_root=repo_root,
        )
        proposal_path = proposals_dir / f"{proposal['proposalId']}.json"
        _assert_recipient_owned(proposal_path, recipient_root)
        proposal_path.write_text(json.dumps(proposal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written_paths.append(_rel(proposal_path, repo_root))

        queue_path = review_dir / "change_review_queue.json"
        event_log_path = review_dir / "change_event_log.json"
        queue = _normalize_queue(_load_json_if_exists(queue_path), user_slug=recipient_fork_id)
        event_log = _normalize_event_log(_load_json_if_exists(event_log_path), user_slug=recipient_fork_id)
        queue["items"] = [item for item in queue["items"] if item.get("proposalId") != proposal["proposalId"]]
        queue["items"].append(
            {
                "proposalId": proposal["proposalId"],
                "status": proposal["status"],
                "priority": _priority_from_risk(proposal["riskLevel"]),
                "summary": proposal["queueSummary"],
                "proposalClass": proposal.get("proposalClass") or _proposal_class_for_surface(proposal["targetSurface"]),
                "targetSurface": proposal["targetSurface"],
                "materiality": proposal["materiality"],
                "reviewType": proposal["reviewType"],
                "riskLevel": proposal["riskLevel"],
                "requiresReclassification": False,
                "evidenceCount": len(proposal["supportingEvidence"]),
            }
        )
        event_log["events"].append(
            {
                "eventId": f"event-{uuid.uuid4()}",
                "timestamp": _utc_now_iso(),
                "eventType": "proposal_created",
                "ref": _rel(proposal_path, repo_root),
                "summary": f"Imported inter-fork package {package['packageId']} from {package['senderForkId']}",
            }
        )
        queue_path.write_text(json.dumps(queue, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        event_log_path.write_text(json.dumps(event_log, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written_paths.extend([_rel(queue_path, repo_root), _rel(event_log_path, repo_root)])

    receipt = {
        "schemaVersion": "1.0.0",
        "receiptKind": "inter_fork_import",
        "receiptId": f"ifimport-{uuid.uuid4()}",
        "createdAt": _utc_now_iso(),
        "recipientForkId": recipient_fork_id,
        "senderForkId": package["senderForkId"],
        "packageId": package["packageId"],
        "importMode": package["routingHint"],
        "canonicalSurfacesTouched": False,
        "humanReviewRequired": True,
        "writtenPaths": written_paths,
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    written_paths.append(_rel(receipt_path, repo_root))
    return {"importMode": package["routingHint"], "writtenPaths": written_paths, "dryRun": False}


def main() -> int:
    parser = argparse.ArgumentParser(description="Import an inter-fork package into recipient-owned review surfaces")
    parser.add_argument("-u", "--recipient", default=DEFAULT_USER_ID, help="Recipient fork id")
    parser.add_argument("-f", "--file", type=Path, required=True, help="Path to inter-fork package JSON")
    parser.add_argument("--dry-run", action="store_true", help="Print intended writes without mutating recipient surfaces")
    args = parser.parse_args()

    result = import_inter_fork_package(
        package_path=args.file,
        recipient_fork_id=args.recipient,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
