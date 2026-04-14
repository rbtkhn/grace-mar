#!/usr/bin/env python3
"""
Emit artifacts/gate-board.md — Kanban-style derived view of recursion-gate.md.

Does not mutate the gate, review-queue, or Record. Classification is computed at
generation time only; the gate file remains authoritative.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from gate_block_parser import (  # noqa: E402
    iter_candidate_yaml_blocks,
    split_gate_sections,
    yaml_blob_provenance_fraction,
)
from operator_dashboard_common import extract_yaml_scalar  # noqa: E402
from recursion_gate_review import parse_review_candidates  # noqa: E402
def _users_dir(user_id: str, repo_root: Path) -> Path:
    return repo_root / "users" / user_id

# Pending sub-column precedence: contradiction → evidence → new → ready
_PROVENANCE_NEEDS_EVIDENCE = 0.34
_SUMMARY_SHORT_LEN = 10

_HAS_ARTIFACT_RE = re.compile(
    r"artifacts?:|artifact_path:|image_file:|create_entries:",
    re.IGNORECASE,
)
_CONFLICT_RE = re.compile(r"conflicts?:|contradiction|advisory_flagged", re.IGNORECASE)


def _status(yaml_body: str) -> str:
    return (extract_yaml_scalar(yaml_body, "status") or "pending").strip().lower()


def _fallback_conflict(yaml_body: str) -> bool:
    return bool(_CONFLICT_RE.search(yaml_body))


def _fallback_artifact(yaml_body: str) -> bool:
    return bool(_HAS_ARTIFACT_RE.search(yaml_body))


def _pending_bucket(
    yaml_body: str,
    row: dict[str, Any] | None,
) -> str:
    """Return column key for status: pending in active slice."""
    has_conflict = (
        row.get("has_conflict_markers", False) or row.get("advisory_flagged", False)
        if row
        else _fallback_conflict(yaml_body)
    )
    if has_conflict:
        return "needs_contradiction_check"

    prov = yaml_blob_provenance_fraction(yaml_body)
    has_art = row.get("has_artifact_payload", _fallback_artifact(yaml_body)) if row else _fallback_artifact(yaml_body)

    if prov < _PROVENANCE_NEEDS_EVIDENCE or (not has_art and prov < 0.5):
        return "needs_evidence"

    summary = (row.get("summary") if row else None) or extract_yaml_scalar(yaml_body, "summary") or ""
    summary = summary.strip()
    if len(summary) < _SUMMARY_SHORT_LEN:
        return "new"

    return "ready_for_review"


def _type_label(yaml_body: str, row: dict[str, Any] | None) -> str:
    for k in ("proposal_class", "candidate_type", "mind_category"):
        if row and row.get(k):
            return str(row[k])
        v = extract_yaml_scalar(yaml_body, k)
        if v:
            return v
    return "unknown"


def _surface_label(yaml_body: str, row: dict[str, Any] | None) -> str:
    if row and row.get("profile_target"):
        return str(row["profile_target"])[:72]
    if row and row.get("target_surface"):
        return str(row["target_surface"])[:72]
    v = extract_yaml_scalar(yaml_body, "profile_target") or extract_yaml_scalar(
        yaml_body, "target_surface"
    )
    return (v or "-")[:72]


def _lane_hint(yaml_body: str, row: dict[str, Any] | None) -> str:
    if row and row.get("territory_label"):
        return str(row["territory_label"])[:40]
    if row and row.get("territory"):
        return str(row["territory"])[:40]
    ck = extract_yaml_scalar(yaml_body, "channel_key") or ""
    if ck:
        return ck.split(":")[0][:40]
    return "-"


def _summary_one_line(yaml_body: str, row: dict[str, Any] | None) -> str:
    s = (row.get("summary") if row else None) or extract_yaml_scalar(yaml_body, "summary") or ""
    s = s.replace("\n", " ").strip()
    return s[:120]


def card_line(cid: str, yaml_body: str, row: dict[str, Any] | None) -> str:
    parts = [
        cid,
        _type_label(yaml_body, row),
        _surface_label(yaml_body, row),
        _lane_hint(yaml_body, row),
        _summary_one_line(yaml_body, row),
    ]
    line = " — ".join(parts)
    if row and isinstance(row.get("boundary_review"), dict):
        conf = row["boundary_review"].get("confidence")
        if conf == "low":
            line += f" — confidence: {conf}"
    return f"- {line}"


def classify_gate(
    *,
    user_id: str,
    active: str,
    processed: str,
    repo_root: Path | None = None,
) -> tuple[dict[str, list[str]], list[str]]:
    """
    Returns (columns -> list of markdown bullet lines), duplicate_notes).
    Column keys: new, needs_evidence, needs_contradiction_check, ready_for_review,
    approved, rejected, merged.
    """
    enriched: dict[str, dict[str, Any]] = {}
    for r in parse_review_candidates(user_id=user_id, repo_root=repo_root):
        enriched[str(r["id"])] = r

    columns: dict[str, list[str]] = {
        "new": [],
        "needs_evidence": [],
        "needs_contradiction_check": [],
        "ready_for_review": [],
        "approved": [],
        "rejected": [],
        "merged": [],
    }
    seen_active: set[str] = set()
    duplicates: list[str] = []

    for cid, _title, yaml_body in iter_candidate_yaml_blocks(active):
        seen_active.add(cid)
        st = _status(yaml_body)
        row = enriched.get(cid)
        if st == "approved":
            columns["approved"].append(card_line(cid, yaml_body, row))
        elif st == "rejected":
            columns["rejected"].append(card_line(cid, yaml_body, row))
        elif st == "pending":
            bucket = _pending_bucket(yaml_body, row)
            columns[bucket].append(card_line(cid, yaml_body, row))
        else:
            columns["ready_for_review"].append(card_line(cid, yaml_body, row))

    for cid, _title, yaml_body in iter_candidate_yaml_blocks(processed):
        if cid in seen_active:
            duplicates.append(cid)
            continue
        st = _status(yaml_body)
        row = enriched.get(cid)
        if st == "approved":
            columns["merged"].append(card_line(cid, yaml_body, row))
        elif st == "rejected":
            columns["rejected"].append(card_line(cid, yaml_body, row))
        elif st == "pending":
            columns["ready_for_review"].append(card_line(cid, yaml_body, row))
        else:
            columns["ready_for_review"].append(card_line(cid, yaml_body, row))

    return columns, duplicates


def render_board(
    *,
    user_id: str,
    generated_at: str,
    columns: dict[str, list[str]],
    duplicates: list[str],
) -> str:
    lines: list[str] = [
        "<!-- GENERATED — run: python3 scripts/build_gate_board.py -->\n\n",
        "# Gate Board\n\n",
        "**Boundary:** This is a **derived operator dashboard**. It does **not** replace "
        f"`users/{user_id}/recursion-gate.md`, `users/{user_id}/review-queue/`, or canonical "
        "change-review objects. **Editing this file does not change candidate status.** "
        "Status changes follow the normal gate and review flow.\n\n",
        f"- **Generated:** {generated_at}\n\n",
    ]
    section_order = [
        ("New", "new"),
        ("Needs evidence", "needs_evidence"),
        ("Needs contradiction check", "needs_contradiction_check"),
        ("Ready for review", "ready_for_review"),
        ("Approved", "approved"),
        ("Rejected", "rejected"),
        ("Merged", "merged"),
    ]
    for heading, key in section_order:
        lines.append(f"## {heading}\n\n")
        items = columns.get(key, [])
        if not items:
            lines.append("_None._\n\n")
        else:
            lines.extend(f"{item}\n" for item in items)
            lines.append("\n")

    if duplicates:
        lines.append("## Notes\n\n")
        lines.append(
            "_Duplicate candidate id in both active and processed regions (active wins): "
            + ", ".join(f"`{d}`" for d in duplicates)
            + "_\n"
        )
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Build gate-board.md Kanban view from recursion-gate.md (read-only)."
    )
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output path (default: <repo>/artifacts/gate-board.md)",
    )
    args = ap.parse_args()
    root = args.repo_root.resolve()
    uid = args.user.strip()
    gate_path = _users_dir(uid, root) / "recursion-gate.md"
    if not gate_path.is_file():
        print(f"missing {gate_path}", file=sys.stderr)
        return 1
    gate_text = gate_path.read_text(encoding="utf-8")
    active, processed = split_gate_sections(gate_text)

    columns, duplicates = classify_gate(
        user_id=uid, active=active, processed=processed, repo_root=root
    )
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md = render_board(user_id=uid, generated_at=ts, columns=columns, duplicates=duplicates)
    out = args.output if args.output is not None else root / "artifacts" / "gate-board.md"
    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
