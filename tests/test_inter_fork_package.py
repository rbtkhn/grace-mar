from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from export_inter_fork_package import (  # noqa: E402
    build_candidate_payload,
    build_change_proposal_payload,
    export_inter_fork_package,
)
from import_inter_fork_package import import_inter_fork_package  # noqa: E402


def _profile_lookup(repo_root: Path):
    return lambda user: repo_root / "users" / user


def _seed_gate(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Gate\n\n## Candidates\n\n## Processed\n", encoding="utf-8")


def _seed_review_queue(root: Path) -> None:
    review = root / "review-queue"
    (review / "proposals").mkdir(parents=True, exist_ok=True)
    (review / "decisions").mkdir(parents=True, exist_ok=True)
    (review / "diffs").mkdir(parents=True, exist_ok=True)
    (review / "change_review_queue.json").write_text('{"queue": []}\n', encoding="utf-8")
    (review / "change_event_log.json").write_text('{"events": []}\n', encoding="utf-8")


def test_export_inter_fork_package_writes_under_sender_namespace(tmp_path: Path) -> None:
    sender_root = tmp_path / "users" / "sender-a"
    sender_root.mkdir(parents=True, exist_ok=True)
    out_path = export_inter_fork_package(
        sender_fork_id="sender-a",
        intended_recipient_fork_id="recipient-b",
        package_kind="evidence_share",
        summary="Share a lightweight review note",
        body="A short imported note.",
        payload=build_candidate_payload(
            suggested_target_surface="skills",
            claim="This may be a reusable review tactic.",
            review_notes="Treat as pending only.",
        ),
        repo_root=tmp_path,
        profile_lookup=_profile_lookup(tmp_path),
        validate_schema=False,
    )

    assert out_path == sender_root / "artifacts" / "inter-fork" / "packages" / f"{json.loads(out_path.read_text(encoding='utf-8'))['packageId']}.json"
    payload = json.loads(out_path.read_text(encoding="utf-8"))
    assert payload["senderForkId"] == "sender-a"
    assert payload["intendedRecipientForkId"] == "recipient-b"
    assert payload["routingHint"] == "candidate_import"


def test_import_candidate_package_only_mutates_recipient_namespace(tmp_path: Path) -> None:
    sender_root = tmp_path / "users" / "sender-a"
    recipient_root = tmp_path / "users" / "recipient-b"
    sender_root.mkdir(parents=True, exist_ok=True)
    _seed_gate(sender_root / "recursion-gate.md")
    _seed_gate(recipient_root / "recursion-gate.md")
    _seed_review_queue(recipient_root)

    package_path = export_inter_fork_package(
        sender_fork_id="sender-a",
        intended_recipient_fork_id="recipient-b",
        package_kind="evidence_share",
        summary="Share a lightweight review note",
        body="Imported note body",
        supporting_refs=["docs/state-proposals.md"],
        payload=build_candidate_payload(
            suggested_target_surface="skills",
            claim="Could be reviewed as a possible SKILLS update.",
            review_notes="Keep as pending until recipient review.",
        ),
        repo_root=tmp_path,
        profile_lookup=_profile_lookup(tmp_path),
        validate_schema=False,
    )

    sender_before = (sender_root / "recursion-gate.md").read_text(encoding="utf-8")
    result = import_inter_fork_package(
        package_path=package_path,
        recipient_fork_id="recipient-b",
        repo_root=tmp_path,
        profile_lookup=_profile_lookup(tmp_path),
        validate_schema=False,
    )

    sender_after = (sender_root / "recursion-gate.md").read_text(encoding="utf-8")
    recipient_gate = (recipient_root / "recursion-gate.md").read_text(encoding="utf-8")
    assert sender_before == sender_after
    assert "INTER_FORK_PACKAGE" in recipient_gate
    assert "sender-a" in recipient_gate
    assert result["importMode"] == "candidate_import"
    copied = recipient_root / "artifacts" / "inter-fork" / "imports"
    assert any(path.name.endswith(".receipt.json") for path in copied.iterdir())
    assert any(path.name.endswith(".json") and not path.name.endswith(".receipt.json") for path in copied.iterdir())


def test_import_change_proposal_package_updates_review_queue(tmp_path: Path) -> None:
    sender_root = tmp_path / "users" / "sender-a"
    recipient_root = tmp_path / "users" / "recipient-b"
    sender_root.mkdir(parents=True, exist_ok=True)
    _seed_gate(recipient_root / "recursion-gate.md")
    _seed_review_queue(recipient_root)

    package_path = export_inter_fork_package(
        sender_fork_id="sender-a",
        intended_recipient_fork_id="recipient-b",
        package_kind="change_proposal_review",
        summary="Recommend an extended skills review",
        body="Material recommendation that should become a review-queue proposal.",
        payload=build_change_proposal_payload(
            primary_scope="pedagogy",
            secondary_scopes=["expression"],
            change_type="refinement",
            target_surface="skills",
            materiality="high",
            review_type="extended",
            risk_level="medium",
            prior_state_ref="REPLACE_WITH_PRIOR_GOVERNED_STATE_REF",
            proposed_state_ref="REPLACE_WITH_PROPOSED_STATE_REF",
            proposal_class="skills",
            notes="Imported from another fork for recipient review.",
        ),
        repo_root=tmp_path,
        profile_lookup=_profile_lookup(tmp_path),
        validate_schema=False,
    )

    result = import_inter_fork_package(
        package_path=package_path,
        recipient_fork_id="recipient-b",
        repo_root=tmp_path,
        profile_lookup=_profile_lookup(tmp_path),
        validate_schema=False,
    )

    proposals = list((recipient_root / "review-queue" / "proposals").glob("proposal-*.json"))
    assert len(proposals) == 1
    proposal = json.loads(proposals[0].read_text(encoding="utf-8"))
    assert proposal["userSlug"] == "recipient-b"
    assert proposal["targetSurface"] == "skills"
    queue = json.loads((recipient_root / "review-queue" / "change_review_queue.json").read_text(encoding="utf-8"))
    assert queue["schemaVersion"] == "1.0.0"
    assert queue["items"][0]["proposalId"] == proposal["proposalId"]
    event_log = json.loads((recipient_root / "review-queue" / "change_event_log.json").read_text(encoding="utf-8"))
    assert event_log["events"][0]["eventType"] == "proposal_created"
    assert result["importMode"] == "change_proposal_review"


def test_import_rejects_recipient_mismatch(tmp_path: Path) -> None:
    sender_root = tmp_path / "users" / "sender-a"
    sender_root.mkdir(parents=True, exist_ok=True)
    package_path = export_inter_fork_package(
        sender_fork_id="sender-a",
        intended_recipient_fork_id="recipient-b",
        package_kind="pointer_bundle",
        summary="Pointer bundle",
        body="A pointer only package.",
        payload=build_candidate_payload(
            suggested_target_surface="work_layer",
            claim="See linked material.",
            review_notes="",
        ),
        repo_root=tmp_path,
        profile_lookup=_profile_lookup(tmp_path),
        validate_schema=False,
    )

    with pytest.raises(ValueError, match="recipient does not match"):
        import_inter_fork_package(
            package_path=package_path,
            recipient_fork_id="other-recipient",
            repo_root=tmp_path,
            profile_lookup=_profile_lookup(tmp_path),
            validate_schema=False,
        )
