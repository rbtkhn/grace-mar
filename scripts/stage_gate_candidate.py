#!/usr/bin/env python3
"""
Insert a pending RECURSION-GATE candidate from stdin or a file.

Writes one `### CANDIDATE-XXXX` + ```yaml``` block **immediately before** `## Processed`.
Stages only; Record files are unchanged until companion approval and merge.

Examples:

  echo "Note from session" | python scripts/stage_gate_candidate.py -u grace-mar
  python scripts/stage_gate_candidate.py -u grace-mar -f ./note.md --mind curiosity
  python scripts/stage_gate_candidate.py -u grace-mar --dry-run --summary "Test" <<< "body"

Work-politics territory (optional):

  python scripts/stage_gate_candidate.py -u grace-mar --territory work-politics <<< "milestone text"
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCORE_SCRIPT = REPO_ROOT / "scripts" / "score_gate_candidates.py"
_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import profile_dir, read_path
from gate_block_parser import iter_candidate_yaml_blocks

try:
    from recursion_gate_territory import TERRITORY_WORK_POLITICS
except ImportError:
    from scripts.recursion_gate_territory import TERRITORY_WORK_POLITICS

DEFAULT_USER = "grace-mar"

# Merge via process_approved_candidates.py moves block to Processed without SELF/EVIDENCE/prompt merge.
PROPOSAL_CLASS_RUNTIME_OBSERVATION = "RUNTIME_OBSERVATION_PROPOSAL"

_STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "be", "because", "for", "from", "has",
    "have", "how", "in", "is", "it", "its", "not", "of", "on", "or",
    "that", "the", "their", "this", "to", "was", "with", "you", "your",
})


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", (text or "").lower())
            if len(t) >= 4 and t not in _STOPWORDS}


def _extract_yaml_scalar(yaml_body: str, key: str) -> str:
    m = re.search(rf"^{re.escape(key)}:\s*(.+)$", yaml_body, re.MULTILINE)
    return (m.group(1).strip().strip('"').strip("'") if m else "")


def convergence_check(
    gate_content: str,
    new_summary: str,
    new_body: str,
    *,
    min_overlap: int = 3,
) -> dict[str, object]:
    """Check whether the new candidate's content overlaps with existing candidates.

    Returns a dict with:
      sighting: "first" | "recurring"
      prior_count: number of overlapping prior candidates
      prior_ids: list of candidate IDs with significant overlap
    """
    new_tokens = _tokenize(f"{new_summary} {new_body}")
    if not new_tokens:
        return {"sighting": "first", "prior_count": 0, "prior_ids": []}

    prior_ids: list[str] = []
    for cid, _title, yaml_body in iter_candidate_yaml_blocks(gate_content):
        existing_text = " ".join(
            _extract_yaml_scalar(yaml_body, k)
            for k in ("summary", "suggested_entry", "prompt_addition")
        )
        existing_tokens = _tokenize(existing_text)
        shared = new_tokens & existing_tokens
        if len(shared) >= min_overlap:
            prior_ids.append(cid)

    return {
        "sighting": "recurring" if prior_ids else "first",
        "prior_count": len(prior_ids),
        "prior_ids": prior_ids,
    }


def _candidate_ids(content: str) -> list[int]:
    nums: list[int] = []
    for m in re.finditer(r"\bCANDIDATE-(\d+)\b", content):
        nums.append(int(m.group(1)))
    return nums


def next_candidate_id(content: str) -> str:
    nums = _candidate_ids(content)
    n = max(nums) + 1 if nums else 1
    return f"CANDIDATE-{n:04d}"


def _yaml_double_quoted(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _literal_block(s: str, base_indent: str = "    ") -> str:
    """YAML literal block content for `key: |` (lines indented under operator)."""
    if not s.strip():
        return base_indent + "(empty)\n"
    lines = []
    for line in s.splitlines():
        lines.append(base_indent + line)
    return "\n".join(lines) + "\n"


def _yaml_scalar_or_literal(key: str, value: str | None, *, max_inline: int = 240) -> list[str]:
    """Emit `key: value` as quoted scalar or block literal."""
    if value is None or not str(value).strip():
        return [f"{key}: null"]
    s = str(value).strip()
    if "\n" in s or len(s) > max_inline:
        lines = [f"{key}: |"]
        lines.append(_literal_block(s, "  ").rstrip("\n"))
        return lines
    return [f"{key}: {_yaml_double_quoted(s)}"]


def _runtime_work_yaml_lines(props: dict[str, Any]) -> list[str]:
    """YAML for PR4 work proposal (candidate_type, target_surface, proposed_change, …)."""
    lines: list[str] = []
    lines.append(f"candidate_type: {props['candidate_type']}")
    lines.append(f"target_surface: {props['target_surface']}")
    tp = props.get("target_path")
    if tp is None or (isinstance(tp, str) and not tp.strip()):
        lines.append("target_path: null")
    else:
        lines.append(f"target_path: {_yaml_double_quoted(str(tp).strip())}")
    lines.extend(_yaml_scalar_or_literal("proposed_change", props.get("proposed_change"), max_inline=4000))
    conf = props.get("confidence")
    if conf is None:
        lines.append("confidence: null")
    else:
        lines.append(f"confidence: {float(conf)}")
    lines.extend(_yaml_scalar_or_literal("why_now", props.get("why_now")))
    lines.extend(_yaml_scalar_or_literal("review_notes", props.get("review_notes")))
    return lines


def _provenance_yaml_lines(provenance: dict[str, Any]) -> list[str]:
    """Optional RECURSION-GATE YAML extension for runtime observation lineage (non-breaking)."""
    out: list[str] = []
    oids = provenance.get("source_observation_ids") or []
    if oids:
        out.append("source_observation_ids:")
        for oid in oids:
            out.append(f"  - {_yaml_double_quoted(str(oid))}")
    if provenance.get("timeline_anchor"):
        out.append(f"timeline_anchor: {_yaml_double_quoted(str(provenance['timeline_anchor']))}")
    if provenance.get("compression_artifact_id"):
        out.append(
            "compression_artifact_id: "
            + _yaml_double_quoted(str(provenance["compression_artifact_id"]))
        )
    if provenance.get("lane_origin"):
        out.append(f"lane_origin: {_yaml_double_quoted(str(provenance['lane_origin']))}")
    srefs = provenance.get("supporting_evidence_refs") or []
    if srefs:
        out.append("supporting_evidence_refs:")
        for r in srefs:
            out.append(f"  - {_yaml_double_quoted(str(r))}")
    crefs = provenance.get("contradiction_refs") or []
    if crefs:
        out.append("contradiction_refs:")
        for r in crefs:
            out.append(f"  - {_yaml_double_quoted(str(r))}")
    return out


def _slug_title(text: str, max_len: int = 56) -> str:
    one = " ".join(text.splitlines()[:1]).strip() or "staged paste"
    one = re.sub(r"\s+", " ", one)
    if len(one) > max_len:
        one = one[: max_len - 1].rstrip() + "…"
    return one


def build_block(
    *,
    candidate_id: str,
    title: str,
    summary: str,
    body: str,
    mind_category: str,
    channel_key: str,
    territory: str | None,
    timestamp: str,
    proposal_class: str | None = None,
    convergence: dict[str, object] | None = None,
    warrant: str | None = None,
    provenance: dict[str, Any] | None = None,
    runtime_work_proposal: dict[str, Any] | None = None,
) -> str:
    summary_one = summary.strip().replace("\n", " ")[:500]
    if len(summary_one) > 200:
        summary_one = summary_one[:197] + "..."

    op_literal = _literal_block(body.rstrip("\n"))

    effective_proposal_class = (
        PROPOSAL_CLASS_RUNTIME_OBSERVATION if runtime_work_proposal is not None else proposal_class
    )
    signal_type = "operator_runtime_observation_stage" if runtime_work_proposal is not None else "operator_paste"
    source_line = (
        "source: operator — scripts/stage_candidate_from_observations.py"
        if runtime_work_proposal is not None
        else "source: operator — scripts/stage_gate_candidate.py"
    )

    lines = [
        f"### {candidate_id} ({title})",
        "",
        "```yaml",
        "status: pending",
        f"timestamp: {timestamp}",
        f"channel_key: {channel_key}",
    ]
    if territory:
        lines.append(f"territory: {territory}")
    if effective_proposal_class:
        lines.append(f"proposal_class: {effective_proposal_class}")
    lines.extend(
        [
            source_line,
            "source_exchange:",
            "  operator: |",
        ]
    )
    lines.append(op_literal.rstrip("\n"))
    convergence_lines: list[str] = []
    if convergence:
        sighting = convergence.get("sighting", "first")
        prior_ids = convergence.get("prior_ids", [])
        convergence_lines.append(f"convergence: {sighting}")
        if prior_ids:
            convergence_lines.append(f"convergence_prior: {', '.join(str(p) for p in prior_ids)}")

    lines.extend(
        [
            f"mind_category: {mind_category}",
            f"signal_type: {signal_type}",
            "priority_score: 3",
            f"summary: {_yaml_double_quoted(summary_one)}",
        ]
    )
    lines.extend(convergence_lines)
    if warrant:
        lines.append(f"warrant: {_yaml_double_quoted(warrant.strip()[:300])}")
    if provenance:
        lines.extend(_provenance_yaml_lines(provenance))
    if runtime_work_proposal:
        lines.extend(_runtime_work_yaml_lines(runtime_work_proposal))
        se = (runtime_work_proposal.get("proposal_summary") or summary_one).strip()
        if len(se) > 500:
            se = se[:497] + "..."
        lines.extend(
            [
                "profile_target: WORK — manual apply (see proposed_change and target_surface).",
                f"suggested_entry: {_yaml_double_quoted(se)}",
                "prompt_section: OPERATOR_WORK",
                "prompt_addition: none",
            ]
        )
    else:
        lines.extend(
            [
                "profile_target: IX-A. KNOWLEDGE",
                "suggested_entry: \"See source_exchange.operator (staged paste).\"",
                "prompt_section: YOUR KNOWLEDGE",
                "prompt_addition: none",
            ]
        )
    lines.extend(["```", ""])
    return "\n".join(lines)


def insert_before_processed(full_md: str, block: str) -> str:
    m = re.search(r"^## Processed\s*$", full_md, re.MULTILINE)
    if not m:
        raise ValueError("recursion-gate.md must contain a ## Processed heading")
    return full_md[: m.start()] + block + full_md[m.start() :]


def main() -> int:
    ap = argparse.ArgumentParser(description="Stage a pending candidate from paste/file into recursion-gate.md")
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER)
    ap.add_argument("-f", "--file", type=Path, default=None, help="Read body from file (default: stdin)")
    ap.add_argument("--summary", default=None, help="One-line summary (default: first line of body)")
    ap.add_argument("--title", default=None, help="Short title for header (default: derived from summary)")
    ap.add_argument(
        "--mind",
        choices=("knowledge", "curiosity", "personality"),
        default="knowledge",
        help="mind_category (default: knowledge)",
    )
    ap.add_argument(
        "--territory",
        choices=("companion", "work-politics"),
        default="companion",
        help="companion = default Record channel; work-politics = territory + wap channel_key prefix",
    )
    ap.add_argument(
        "--channel-key",
        default=None,
        help="Override channel_key (default: operator:cursor:stage-paste or operator:wap:stage-paste)",
    )
    ap.add_argument("--dry-run", action="store_true", help="Print block to stdout; do not write")
    ap.add_argument(
        "--proposal-class",
        default=None,
        help="Optional YAML proposal_class (e.g. SIMULATION_RESULT for fork simulations)",
    )
    ap.add_argument(
        "--warrant",
        default=None,
        help="Optional invalidation condition (LoreSpec-inspired): the assumption that, if changed, means this entry should be revisited",
    )
    ap.add_argument(
        "--auto-score",
        action="store_true",
        help="After writing, run score_gate_candidates.py for this user (heuristic hints)",
    )
    args = ap.parse_args()

    if args.file:
        body = args.file.read_text(encoding="utf-8")
    else:
        body = sys.stdin.read()

    summary = args.summary
    if not summary:
        for line in body.splitlines():
            if line.strip():
                summary = line.strip()
                break
        else:
            summary = "(staged paste — empty body)"

    title = args.title or _slug_title(summary)

    if args.territory == "work-politics":
        territory = TERRITORY_WORK_POLITICS
        channel_key = args.channel_key or "operator:wap:stage-paste"
    else:
        territory = None
        channel_key = args.channel_key or "operator:cursor:stage-paste"

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    gate_path = profile_dir(args.user) / "recursion-gate.md"
    if not gate_path.exists():
        print(f"Missing {gate_path}", file=sys.stderr)
        return 1

    full = read_path(gate_path)
    if "## Candidates" not in full or "## Processed" not in full:
        print(f"{gate_path}: need ## Candidates and ## Processed", file=sys.stderr)
        return 1

    cid = next_candidate_id(full)
    conv = convergence_check(full, summary, body)
    block = build_block(
        candidate_id=cid,
        title=title,
        summary=summary,
        body=body,
        mind_category=args.mind,
        channel_key=channel_key,
        territory=territory,
        timestamp=ts,
        proposal_class=args.proposal_class,
        warrant=args.warrant,
        convergence=conv,
    )

    if args.dry_run:
        print(block)
        print(f"# Would insert {cid} before ## Processed", file=sys.stderr)
        return 0

    try:
        new_full = insert_before_processed(full, block)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1

    gate_path.write_text(new_full, encoding="utf-8")
    print(f"{gate_path}: inserted {cid}")
    if args.auto_score and SCORE_SCRIPT.is_file():
        subprocess.run(
            [sys.executable, str(SCORE_SCRIPT), "-u", args.user],
            check=False,
        )
    elif args.auto_score:
        print(f"Missing {SCORE_SCRIPT}, skipping --auto-score", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
