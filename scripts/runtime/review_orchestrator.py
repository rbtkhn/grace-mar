#!/usr/bin/env python3
"""
Multi-pass review packet for operator decision (read-only).

Does not write self.md, EVIDENCE, recursion-gate.md, or auto-approve merges.
See docs/orchestration/review-orchestrator.md.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
_RUNTIME = Path(__file__).resolve().parent
for _p in (_SCRIPTS, _RUNTIME):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from observation_store import by_id  # noqa: E402
from uncertainty_envelope import (  # noqa: E402
    compute_envelope,
    synthetic_observation_from_text,
)

try:
    from recursion_gate_review import parse_review_candidates
except ImportError:
    from scripts.recursion_gate_review import parse_review_candidates  # type: ignore

from policy_mode_config import load_defaults, mode_summary_lines, resolve_mode  # noqa: E402


def _candidate_synthetic_text(row: dict) -> str:
    parts = [
        (row.get("summary") or "").strip(),
        (row.get("suggested_entry") or "")[:1500],
        (row.get("example_from_exchange") or "")[:800],
    ]
    return "\n\n".join(p for p in parts if p)


def _pre_gate_boundary_notes(observations: list[dict], lane: str) -> list[str]:
    notes: list[str] = []
    work_lanes = ("work-", "strategy", "politics", "jiang", "dev", "xavier")
    looks_work = any(w in (lane or "").lower() for w in work_lanes)
    any_mut = any(o.get("record_mutation_candidate") for o in observations)
    any_refs = any(o.get("source_refs") for o in observations)
    if looks_work and any_mut:
        notes.append(
            "Lane and mutation flags suggest **work-layer** planning; durable Record changes still require "
            "explicit gate YAML targeting SELF / IX / EVIDENCE — not implied by runtime lane alone."
        )
    elif any_mut and not any_refs:
        notes.append(
            "**Record mutation** intent without `source_refs` on observations: strengthen provenance before staging."
        )
    if any_refs:
        notes.append("At least one observation carries **source_refs** — trace before promotion.")
    if not notes:
        notes.append("No strong boundary signal; classify target surface when drafting the gate candidate.")
    return notes


def _contradiction_pass_observations(observations: list[dict], env: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    union: set[str] = set()
    for o in observations:
        for c in o.get("contradiction_refs") or []:
            if c:
                union.add(c)
    if union:
        lines.append(f"Contradiction refs present: {', '.join(sorted(union))}.")
    else:
        lines.append("No `contradiction_refs` on selected observations.")
    if env.get("evidence_state") == "conflicted":
        lines.append("Uncertainty envelope: **conflicted** — do not promote without resolving tensions.")
    else:
        lines.append("Uncertainty envelope: not in **conflicted** evidence state (still review narrative strength).")
    return lines


def _contradiction_pass_candidate(row: dict, env: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    if row.get("has_conflict_markers"):
        lines.append("Gate YAML / text flags **conflict or contradiction** markers — manual review.")
    else:
        lines.append("No automated conflict markers on candidate row.")
    cs = row.get("constitution_check_status")
    if cs:
        lines.append(f"Constitution check status: `{cs}`.")
    cr = row.get("constitution_rule_ids")
    if cr:
        lines.append(f"Constitution rule ids: `{cr}`.")
    if row.get("duplicate_hints"):
        lines.append(f"Duplicate hints: {row['duplicate_hints']!r} — resolve before merge.")
    if env.get("evidence_state") == "conflicted":
        lines.append("Synthetic gate-text envelope: **conflicted** — treat narrative as contested.")
    return lines


def _operator_questions(
    mode: str,
    env: dict[str, Any],
    *,
    candidate_id: str | None = None,
) -> list[str]:
    qs: list[str] = []
    promo = env.get("promotion_recommendation", "")
    if promo in ("hold", "block"):
        qs.append("What additional **primary evidence** (companion-sourced or artifact) would justify staging?")
    if env.get("fabricated_history_risk") in ("medium", "high"):
        qs.append("Can every **historical / biographical** claim be tied to an approved Record line or citation?")
    if env.get("evidence_state") == "conflicted":
        qs.append("Which **contradiction ref** should be resolved first, and how?")
    qs.append("Does the **target surface** (SELF vs SELF-LIBRARY vs SKILLS vs EVIDENCE vs work-layer) match intent?")
    if mode == "candidate_review" and candidate_id:
        qs.append(f"Re-read `### {candidate_id}` in recursion-gate.md for edits before approve.")
    if len(qs) < 3:
        qs.append("Would a second operator pass (e.g. gate-review-pass skill) change the call?")
    return qs[:8]


def build_review_packet_markdown(
    *,
    mode: str,
    built_iso: str,
    target_label: str,
    observations: list[dict],
    env: dict[str, Any],
    candidate_row: dict | None,
    gate_text_derived: bool,
) -> str:
    lines: list[str] = [
        "# Review Packet",
        "",
        f"Built: {built_iso}",
        f"Mode: {mode}",
        f"Target: {target_label}",
        "",
    ]
    if gate_text_derived:
        lines.extend(
            [
                "_Note: uncertainty scoring for candidate mode uses **gate-text-derived** synthetic observation(s); "
                "ledger-backed observations were not supplied._",
                "",
            ]
        )

    # Evidence pass
    lines.extend(["## Evidence Pass", ""])
    n = len(observations)
    lines.append(f"- **Observation count:** {n}")
    total_refs = sum(len(o.get("source_refs") or []) for o in observations)
    lines.append(f"- **Supporting refs (source_refs count):** {total_refs}")
    if observations:
        kinds = {}
        for o in observations:
            k = o.get("source_kind") or "?"
            kinds[k] = kinds.get(k, 0) + 1
        lines.append(f"- **source_kind mix:** {kinds}")
        ts = [o.get("timestamp") for o in observations if o.get("timestamp")]
        if ts:
            lines.append(f"- **Recency (timestamps):** oldest `{min(ts)}` → newest `{max(ts)}`")
    lines.append(f"- **Evidence sufficiency (PR 1 envelope):** `{env['evidence_state']}`")
    lines.append("")

    # Contradiction pass
    lines.extend(["## Contradiction Pass", ""])
    if mode == "pre_gate":
        for x in _contradiction_pass_observations(observations, env):
            lines.append(f"- {x}")
    else:
        assert candidate_row is not None
        for x in _contradiction_pass_candidate(candidate_row, env):
            lines.append(f"- {x}")
    lines.append("")

    # Boundary pass
    lines.extend(["## Boundary Pass", ""])
    if mode == "pre_gate" and observations:
        lane = observations[0].get("lane") or ""
        for note in _pre_gate_boundary_notes(observations, lane):
            lines.append(f"- {note}")
    elif candidate_row:
        br = candidate_row.get("boundary_review") or {}
        lines.append(f"- **profile_target:** `{candidate_row.get('profile_target', '')}`")
        lines.append(f"- **mind_category:** `{candidate_row.get('mind_category', '')}`")
        lines.append(f"- **territory:** `{candidate_row.get('territory', '')}`")
        lines.append(f"- **proposal_class:** `{candidate_row.get('proposal_class', '')}`")
        lines.append(
            f"- **boundary_review target_surface:** `{br.get('target_surface', '')}` → "
            f"suggested `{br.get('suggested_surface', '')}` (confidence: {br.get('confidence', '')})"
        )
        if br.get("misfiled_warning"):
            lines.append(f"- **Misfiled warning:** {br['misfiled_warning']}")
        for h in br.get("hint_reasons") or []:
            lines.append(f"- Hint: {h}")
        lines.append(f"- **risk_tier:** `{candidate_row.get('risk_tier', '')}`")
    else:
        lines.append("- (No boundary metadata for this packet.)")
    lines.append("")

    # Promotion-risk pass (explicit section)
    lines.extend(["## Promotion-Risk Pass", ""])
    lines.append(f"- **Fabricated-history risk:** `{env['fabricated_history_risk']}`")
    lines.append(f"- **Promotion recommendation:** `{env.get('promotion_recommendation', '')}`")
    lines.append("- **Reasons (envelope):**")
    for r in env.get("reasons", [])[:14]:
        lines.append(f"  - {r}")
    if candidate_row:
        rt = candidate_row.get("risk_tier", "")
        lines.append(
            f"- **Scope / prematurity (gate risk_tier):** `{rt}` — defer or escalate when `manual_escalate`."
        )
    else:
        lines.append(
            "- **Scope / prematurity:** If staging to gate, confirm IX target and provenance before merge."
        )
    lines.append("")

    # Synthesis
    promo = env.get("promotion_recommendation", "allow_with_review")
    lines.extend(
        [
            "## Synthesis",
            "",
            f"- **Recommended action:** `{promo}`",
            "- **Rationale:** Derived from PR 1 uncertainty envelope "
            "+ contradiction/boundary signals (advisory; companion decides).",
            "",
        ]
    )

    # Operator questions
    cid = candidate_row.get("id") if candidate_row else None
    lines.extend(["## Operator Questions", ""])
    for q in _operator_questions(mode, env, candidate_id=cid):
        lines.append(f"- {q}")
    lines.append("")
    lines.append("---")
    lines.append("_Review orchestrator output is not canonical. Merge only via companion-approved gate pipeline._")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(
        description="Build a multi-pass Markdown review packet (pre_gate or candidate_review). Read-only."
    )
    p.add_argument("--mode", required=True, choices=("pre_gate", "candidate_review"))
    p.add_argument("--lane", default=None)
    p.add_argument("--mixed-lane", action="store_true")
    p.add_argument("--id", action="append", dest="ids", default=None)
    p.add_argument("--candidate", default=None, help="CANDIDATE-NNNN for candidate_review")
    p.add_argument("--user", "-u", default="grace-mar")
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root (default: auto-detected; use for tests)",
    )
    p.add_argument("-o", "--output", type=Path, default=None)
    p.add_argument(
        "--context-mode",
        choices=("compact", "medium", "deep"),
        default=None,
        help="Append a suggested build_budgeted_context.py command using this budget mode (optional)",
    )
    p.add_argument(
        "--policy-mode",
        default=None,
        help="Append Policy mode envelope section (default: GRACE_MAR_POLICY_MODE or operator_only)",
    )
    args = p.parse_args()
    repo_root = args.repo_root.resolve() if args.repo_root else None

    built = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if args.mode == "pre_gate":
        ids = args.ids or []
        if not ids:
            print("error: pre_gate requires at least one --id", file=sys.stderr)
            return 2
        if not args.mixed_lane and not (args.lane and args.lane.strip()):
            print("error: pre_gate requires --lane or --mixed-lane", file=sys.stderr)
            return 2
        lane = (args.lane or "").strip()
        observations: list[dict] = []
        for oid in ids:
            raw = by_id(oid)
            if raw is None:
                print(f"error: missing observation {oid}", file=sys.stderr)
                return 2
            if not args.mixed_lane and raw.get("lane") != lane:
                print(
                    f"error: {oid} lane {raw.get('lane')!r} != {lane!r} (use --mixed-lane)",
                    file=sys.stderr,
                )
                return 2
            observations.append(raw)
        env = compute_envelope(observations)
        target_label = ", ".join(ids)
        md = build_review_packet_markdown(
            mode="pre_gate",
            built_iso=built,
            target_label=target_label,
            observations=observations,
            env=env,
            candidate_row=None,
            gate_text_derived=False,
        )
    else:
        cid = (args.candidate or "").strip()
        if not cid or not cid.startswith("CANDIDATE-"):
            print("error: candidate_review requires --candidate CANDIDATE-NNNN", file=sys.stderr)
            return 2
        rows = parse_review_candidates(user_id=args.user, repo_root=repo_root)
        candidate_row = next((r for r in rows if r.get("id") == cid), None)
        if candidate_row is None:
            print(f"error: candidate not found in active gate section: {cid}", file=sys.stderr)
            return 2
        text = _candidate_synthetic_text(candidate_row)
        observations = [synthetic_observation_from_text(text, record_mutation_candidate=True)]
        env = compute_envelope(observations)
        target_label = cid
        md = build_review_packet_markdown(
            mode="candidate_review",
            built_iso=built,
            target_label=target_label,
            observations=observations,
            env=env,
            candidate_row=candidate_row,
            gate_text_derived=True,
        )

    pdefs = load_defaults()
    pol = resolve_mode(args.policy_mode, pdefs)
    md += "\n## Policy mode envelope\n\n"
    md += f"Active policy mode: **`{pol}`** (declared for this packet; does not replace gate review).\n\n"
    md += "\n".join(mode_summary_lines(pol, pdefs)) + "\n"
    md += "\nSee `docs/policy-modes.md`.\n"

    if args.context_mode:
        lane_hint = (args.lane or "").strip() or "work-strategy"
        md += (
            "\n## Suggested budgeted context\n\n"
            f"Lane **`{lane_hint}`** — run `build_budgeted_context.py` in **`{args.context_mode}`** budget class "
            "to assemble a bounded context block with explicit inclusion/exclusion reporting "
            "(see `docs/runtime/context-budgeting.md`). Add `--policy-mode {pol}` to match this envelope.\n\n"
            "```bash\n"
            f"python3 scripts/prepared_context/build_budgeted_context.py \\\n"
            f"  --lane {lane_hint} \\\n"
            f"  --policy-mode {pol} \\\n"
            f"  --mode {args.context_mode} \\\n"
            "  --query \"(add search terms)\" \\\n"
            "  -o prepared-context/budgeted-review-context.md\n"
            "```\n"
        )

    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(md, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    else:
        print(md, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
