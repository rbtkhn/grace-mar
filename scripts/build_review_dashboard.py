#!/usr/bin/env python3
"""
Emit artifacts/review-dashboard.md — derived operator view of recursion-gate.md.

Does not mutate the gate or Record. Uses gate_block_parser for consistent slicing.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from gate_block_parser import iter_candidate_yaml_blocks  # noqa: E402
from operator_dashboard_common import extract_yaml_scalar  # noqa: E402
from repo_io import profile_dir  # noqa: E402


def _pending_structs(gate_text: str) -> list[dict[str, str | None]]:
    """All YAML blocks with status: pending anywhere in the gate file.

    Prefer blocks above ``## Processed`` in a healthy gate; some instances place
    blocks only under Processed — we still surface pending by YAML status.
    """
    out: list[dict[str, str | None]] = []
    for cid, title, body in iter_candidate_yaml_blocks(gate_text):
        st = (extract_yaml_scalar(body, "status") or "").strip().lower()
        if st != "pending":
            continue
        out.append(
            {
                "id": cid,
                "title": title or "",
                "status": st,
                "mind_category": extract_yaml_scalar(body, "mind_category"),
                "profile_target": extract_yaml_scalar(body, "profile_target"),
                "target_surface": extract_yaml_scalar(body, "target_surface"),
                "proposal_class": extract_yaml_scalar(body, "proposal_class"),
                "candidate_type": extract_yaml_scalar(body, "candidate_type"),
                "summary": (extract_yaml_scalar(body, "summary") or "")[:200],
                "timestamp": extract_yaml_scalar(body, "timestamp"),
            }
        )
    return out


def _processed_structs(processed_tail: str) -> list[dict[str, str | None]]:
    out: list[dict[str, str | None]] = []
    for cid, title, body in iter_candidate_yaml_blocks(processed_tail):
        st = (extract_yaml_scalar(body, "status") or "").strip().lower()
        out.append(
            {
                "id": cid,
                "title": title or "",
                "status": st,
                "mind_category": extract_yaml_scalar(body, "mind_category"),
                "summary": (extract_yaml_scalar(body, "summary") or "")[:160],
                "timestamp": extract_yaml_scalar(body, "timestamp"),
            }
        )
    return out


def render_markdown(
    *,
    user_id: str,
    pending: list[dict[str, str | None]],
    processed: list[dict[str, str | None]],
    generated_at: str,
) -> str:
    lines: list[str] = [
        "<!-- GENERATED — run: python3 scripts/build_review_dashboard.py -->\n\n",
        "# Review dashboard (Approval Inbox)\n\n",
        "**Derived operator artifact.** Not canonical; does not replace "
        f"`users/{user_id}/recursion-gate.md`. Regenerate after gate edits.\n\n",
        f"- **Generated:** {generated_at}\n",
        f"- **Pending count:** {len(pending)}\n\n",
        "## Pending candidates\n\n",
    ]
    if not pending:
        lines.append("_No pending candidates above `## Processed`._\n\n")
    else:
        by_mind = Counter(str(p.get("mind_category") or "unknown") for p in pending)
        by_tgt = Counter(str(p.get("profile_target") or p.get("target_surface") or "unknown") for p in pending)
        lines.append("### By mind_category (pending)\n\n")
        for k, v in sorted(by_mind.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- `{k}`: {v}\n")
        lines.append("\n### By profile_target / target_surface (pending)\n\n")
        for k, v in sorted(by_tgt.items(), key=lambda x: (-x[1], x[0]))[:20]:
            lines.append(f"- {k}: {v}\n")
        lines.append("\n### Pending list (compact)\n\n")
        lines.append("| ID | Status | Mind | Target | Summary |\n")
        lines.append("|---|--------|------|--------|--------|\n")
        for p in pending[:40]:
            mid = str(p.get("mind_category") or "")
            tgt = str(p.get("profile_target") or p.get("target_surface") or "")
            summ = str(p.get("summary") or "").replace("|", "\\|")
            lines.append(f"| {p.get('id')} | pending | {mid} | {tgt} | {summ} |\n")
        if len(pending) > 40:
            lines.append(f"\n_… {len(pending) - 40} more pending (see gate file)._\n")
        lines.append("\n")

    approved = [x for x in processed if x.get("status") == "approved"]
    rejected = [x for x in processed if x.get("status") == "rejected"]
    lines.append("## Recently processed (tail of file — not a full history API)\n\n")
    lines.append(f"- **Approved blocks (in Processed section):** {len(approved)}\n")
    lines.append(f"- **Rejected blocks (in Processed section):** {len(rejected)}\n\n")
    lines.append("### Last few approved (compact)\n\n")
    for p in approved[-8:]:
        lines.append(f"- **{p.get('id')}** — {p.get('summary') or p.get('title')}\n")
    if not approved:
        lines.append("_None parsed._\n")
    lines.append("\n### Last few rejected (compact)\n\n")
    for p in rejected[-8:]:
        lines.append(f"- **{p.get('id')}** — {p.get('summary') or p.get('title')}\n")
    if not rejected:
        lines.append("_None parsed._\n")

    lines.append(
        "\n## Contradiction / blocked review\n\n"
        "_No machine signal in v1 — use gate YAML and companion review. "
        "See docs/contradiction-policy.md if applicable._\n"
    )
    return "".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build review-dashboard.md from recursion-gate.md.")
    ap.add_argument("-u", "--user", default="grace-mar")
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = ap.parse_args()
    root = args.repo_root.resolve()
    uid = args.user.strip()
    gate_path = profile_dir(uid) / "recursion-gate.md"
    if not gate_path.is_file():
        print(f"missing {gate_path}", file=sys.stderr)
        return 1
    gate_text = gate_path.read_text(encoding="utf-8")
    marker = re.search(r"^## Processed\s*$", gate_text, re.MULTILINE)
    processed_tail = gate_text[marker.end() :] if marker else ""

    pending = _pending_structs(gate_text)
    processed = _processed_structs(processed_tail)

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    md = render_markdown(user_id=uid, pending=pending, processed=processed, generated_at=ts)
    out = root / "artifacts" / "review-dashboard.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
