"""Build RECURSION-GATE markdown blocks for reflection proposals."""

from __future__ import annotations

import re
from typing import Any


def _yaml_double_quoted(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _literal_block(s: str, base_indent: str = "    ") -> str:
    if not s.strip():
        return base_indent + "(empty)\n"
    lines = []
    for line in s.splitlines():
        lines.append(base_indent + line)
    return "\n".join(lines) + "\n"


def _slug_title(text: str, max_len: int = 52) -> str:
    one = " ".join(text.splitlines()[:1]).strip() or "reflection"
    one = re.sub(r"\s+", " ", one)
    if len(one) > max_len:
        one = one[: max_len - 1].rstrip() + "…"
    return one


def build_reflection_candidate_block(
    *,
    candidate_id: str,
    reflection_cycle_id: str,
    timestamp: str,
    title_summary: str,
    proposal: dict[str, Any],
    full_analysis_rel: str,
) -> str:
    """
    Build one ```yaml``` block compatible with CANDIDATE-\\d+ parsers.

    `proposal` must include: summary, suggested_entry, mind_category, profile_target,
    prompt_section, prompt_addition (or defaults applied), channel_key, signal_type,
    source_exchange (multiline operator narrative), evidence_citations (list[str]),
    rationale, confidence, priority_score, reflection_axis, risk_level, impact_level.
    """
    summary = str(proposal.get("summary") or "").strip()
    suggested = str(proposal.get("suggested_entry") or "").strip()
    mc = str(proposal.get("mind_category") or "knowledge").strip().lower()
    if mc not in ("knowledge", "curiosity", "personality"):
        mc = "knowledge"
    pt = str(proposal.get("profile_target") or "IX-A. KNOWLEDGE").strip()
    ps = str(proposal.get("prompt_section") or "YOUR KNOWLEDGE").strip()
    pa = str(proposal.get("prompt_addition") or "none").strip()
    ck = str(proposal.get("channel_key") or "reflection-cycle").strip()
    st = str(proposal.get("signal_type") or "reflection-cycle").strip()
    se = str(proposal.get("source_exchange") or "").rstrip()
    citations = proposal.get("evidence_citations") or []
    if isinstance(citations, str):
        citations = [citations]
    cit_lines = "\n".join(f"- {c}" for c in citations if str(c).strip())
    rationale = str(proposal.get("rationale") or "").strip()
    conf = proposal.get("confidence")
    try:
        conf_f = float(conf) if conf is not None else 0.0
    except (TypeError, ValueError):
        conf_f = 0.0
    try:
        pri = int(proposal.get("priority_score") or 50)
    except (TypeError, ValueError):
        pri = 50
    axis = str(proposal.get("reflection_axis") or "record").strip()
    risk = str(proposal.get("risk_level") or "medium").strip()
    impact = str(proposal.get("impact_level") or "medium").strip()

    summary_one = summary.replace("\n", " ")[:500]
    if len(summary_one) > 200:
        summary_one = summary_one[:197] + "..."

    title = _slug_title(title_summary or summary)

    op_literal = _literal_block(se if se else "(reflection cycle — see rationale)")

    lines = [
        f"### {candidate_id} (Reflection — {title})",
        "",
        "```yaml",
        "status: pending",
        f"timestamp: {timestamp}",
        f"channel_key: {ck}",
        f"signal_type: {st}",
        f"reflection_cycle_id: {reflection_cycle_id}",
        "source: operator — reflection_cycle.py",
        "source_exchange:",
        "  operator: |",
    ]
    lines.append(op_literal.rstrip("\n"))
    lines.extend(
        [
            f"mind_category: {mc}",
            f"priority_score: {pri}",
            f"summary: {_yaml_double_quoted(summary_one)}",
            f"profile_target: {pt}",
            "suggested_entry: |",
        ]
    )
    lines.append(_literal_block(suggested, base_indent="    ").rstrip("\n"))
    lines.extend(
        [
            f"prompt_section: {ps}",
            f"prompt_addition: {pa}",
            "evidence_citations: |",
        ]
    )
    lines.append(
        _literal_block(cit_lines if cit_lines.strip() else "- (none)", base_indent="    ").rstrip("\n")
    )
    lines.extend(
        [
            f"rationale: {_yaml_double_quoted(rationale[:800])}",
            f"confidence: {conf_f:.2f}",
            f"reflection_axis: {axis}",
            f"risk_level: {risk}",
            f"impact_level: {impact}",
            f"full_analysis: {full_analysis_rel}",
            "```",
            "",
        ]
    )
    return "\n".join(lines)
