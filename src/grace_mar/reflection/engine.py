"""LLM chain for reflection cycles (evidence-grounded proposals)."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Any

from grace_mar.reflection.collect import ReflectionBundle


@dataclass
class ReflectionResult:
    """Output of a reflection run (before writing files)."""

    aggregate_summary: str
    qualitative_insights: list[str]
    proposals: list[dict[str, Any]]
    raw_model_json: str | None = None
    critique_notes: list[str] = field(default_factory=list)


SYSTEM = """You are a Grace-Mar pipeline analyst. You ONLY use evidence from the bundled excerpts.
You must not invent facts not present in the excerpts. Output valid JSON only.
Mind categories for mergeable candidates MUST be one of: knowledge, curiosity, personality.
profile_target MUST be one of: IX-A. KNOWLEDGE, IX-B. CURIOSITY, IX-C. PERSONALITY (or close match).
Proposals targeting skills.md, JSON files, or SELF-LIBRARY structural edits must set reflection_axis
to skills, intent, or library and include in suggested_entry explicit text that operator merge to
those files is MANUAL (not automated by process_approved_candidates)."""


USER_TEMPLATE = """Analyze the following operator bundle for fork `{user_id}` (lookback {days} days).

Return a JSON object with exactly these keys:
- "aggregate_summary": string (counts, themes, deltas you can justify from excerpts)
- "qualitative_insights": array of short strings (patterns, gaps, contradictions)
- "proposals": array of at most {max_p} objects, each with:
  - "summary": string (one line)
  - "suggested_entry": string (what would enter the Record or operator note — multiline ok in JSON string)
  - "mind_category": "knowledge" | "curiosity" | "personality"
  - "profile_target": string (IX-A / IX-B / IX-C style)
  - "prompt_section": string (YOUR KNOWLEDGE / YOUR CURIOSITY / YOUR PERSONALITY)
  - "prompt_addition": string (often "none")
  - "source_exchange": string (operator-facing narrative; cite what in the bundle supports this)
  - "evidence_citations": array of at least 2 strings, each like `path/to/file:lines X-Y` or describe event line from jsonl
  - "rationale": string
  - "confidence": number 0-1
  - "priority_score": integer 0-100
  - "reflection_axis": string (record | skills | intent | library | governance)
  - "risk_level": "low" | "medium" | "high"
  - "impact_level": "low" | "medium" | "high"
  - "channel_key": "reflection-cycle"
  - "signal_type": "reflection-cycle"

Rules:
- Every proposal MUST have at least 2 evidence_citations pointing to content in the bundle.
- Maximum {max_p} proposals total.
- Prefer high-signal, non-duplicate refinements.

--- BUNDLE ---

{bundle_text}
"""


def _parse_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    m = re.search(r"\{[\s\S]*\}\s*$", text)
    if m:
        text = m.group(0)
    return json.loads(text)


def _validate_and_trim_proposals(
    proposals: list[dict[str, Any]],
    *,
    max_n: int,
    min_citations: int = 2,
) -> tuple[list[dict[str, Any]], list[str]]:
    notes: list[str] = []
    out: list[dict[str, Any]] = []
    for p in proposals:
        cites = p.get("evidence_citations") or []
        if not isinstance(cites, list):
            cites = [str(cites)]
        cites = [str(c).strip() for c in cites if str(c).strip()]
        if len(cites) < min_citations:
            notes.append(f"dropped proposal (insufficient citations): {p.get('summary', '')[:60]}")
            continue
        mc = str(p.get("mind_category") or "").lower()
        if mc not in ("knowledge", "curiosity", "personality"):
            notes.append(f"fixed mind_category for: {p.get('summary', '')[:40]}")
            p["mind_category"] = "knowledge"
        out.append(p)
    out.sort(key=lambda x: int(x.get("priority_score") or 0), reverse=True)
    return out[:max_n], notes


def run_reflection_engine(
    bundle: ReflectionBundle,
    *,
    dry_run: bool,
    max_proposals: int,
    model: str | None = None,
) -> ReflectionResult:
    if dry_run:
        return ReflectionResult(
            aggregate_summary="(dry-run) No LLM call.",
            qualitative_insights=[
                "(dry-run) Review bundle size and slices before enabling API.",
            ],
            proposals=[
                {
                    "summary": "(dry-run) Example reflection proposal",
                    "suggested_entry": "Operator: replace with real run after OPENAI_API_KEY is set.",
                    "mind_category": "knowledge",
                    "profile_target": "IX-A. KNOWLEDGE",
                    "prompt_section": "YOUR KNOWLEDGE",
                    "prompt_addition": "none",
                    "source_exchange": "Dry-run stub — no model call.",
                    "evidence_citations": [
                        "users/grace-mar/session-transcript.md:lines 1-2 (placeholder)",
                        "users/grace-mar/pipeline-events.jsonl:tail (placeholder)",
                    ],
                    "rationale": "Placeholder for CI and local testing without API costs.",
                    "confidence": 0.1,
                    "priority_score": 1,
                    "reflection_axis": "record",
                    "risk_level": "low",
                    "impact_level": "low",
                    "channel_key": "reflection-cycle",
                    "signal_type": "reflection-cycle",
                }
            ],
            raw_model_json=None,
            critique_notes=["dry-run"],
        )

    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError(
            'Install OpenAI support: pip install -e ".[reflect]"'
        ) from e

    client = OpenAI()
    model = model or os.getenv("GRACE_MAR_REFLECT_MODEL", "gpt-4o-mini").strip()
    bundle_text = bundle.as_prompt_context()
    user_msg = USER_TEMPLATE.format(
        user_id=bundle.user_id,
        days=bundle.lookback_days,
        max_p=max_proposals,
        bundle_text=bundle_text,
    )
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content or "{}"
    data = _parse_json_object(raw)
    proposals = data.get("proposals") or []
    if not isinstance(proposals, list):
        proposals = []
    proposals, notes = _validate_and_trim_proposals(proposals, max_n=max_proposals)
    return ReflectionResult(
        aggregate_summary=str(data.get("aggregate_summary") or ""),
        qualitative_insights=[str(x) for x in (data.get("qualitative_insights") or []) if str(x).strip()],
        proposals=proposals,
        raw_model_json=raw,
        critique_notes=notes,
    )
