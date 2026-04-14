#!/usr/bin/env python3
"""
Shadow Merge Simulator — non-mutating counterfactual preview for RECURSION-GATE candidates.

Produces a Markdown "Shadow Merge Report" describing likely surface impact, propagation,
and governance risks. Does **not** merge, approve, or edit self.md, self-archive.md,
self-skills.md, SELF-LIBRARY files, recursion-gate.md, or bot/prompt.py — only writes
the path given by --output (and may print to stderr).

See docs/orchestration/shadow-merge-simulator.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_SHADOW_MERGE_DIR = REPO_ROOT / "artifacts" / "shadow-merges"
_SCRIPTS = REPO_ROOT / "scripts"
_RUNTIME = Path(__file__).resolve().parent
for _p in (_SCRIPTS, _RUNTIME):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from recursion_gate_review import (  # noqa: E402
    _extract_block,
    _extract_scalar,
    parse_review_candidates,
)
from uncertainty_envelope import compute_envelope  # noqa: E402

from observation_store import by_id as obs_by_id  # noqa: E402

DEFAULT_USER = "grace-mar"

REPORT_SURFACES = ("SELF", "SELF-LIBRARY", "SKILLS", "EVIDENCE")

# YAML staging surfaces (schema + runtime staging)
YAML_TARGET_SURFACES = frozenset({"SELF", "SELF-LIBRARY", "SKILLS", "EVIDENCE", "OTHER"})

# Keyword best-fit (second signal alongside boundary_review / YAML target)
SURFACE_KEYWORDS: dict[str, frozenset[str]] = {
    "SELF": frozenset(
        {
            "identity",
            "self-knowledge",
            "personality",
            "preference",
            "value",
            "voice",
            "style",
            "temperament",
            "narrative",
            "ix-a",
            "ix-b",
            "ix-c",
        }
    ),
    "SELF-LIBRARY": frozenset(
        {
            "library",
            "reference",
            "corpus",
            "shelf",
            "domain",
            "civilization",
            "civilizational",
            "civ-mem",
            "source",
            "tradition",
            "archive",
            "reading",
            "roman",
            "imperial",
            "encyclopedia",
            "codex",
            "lib-",
        }
    ),
    "SKILLS": frozenset(
        {
            "skill",
            "capability",
            "workflow",
            "operator",
            "doctrine",
            "competence",
            "tooling",
            "procedure",
            "self-skills",
            "think",
            "write",
            "steward",
        }
    ),
    "EVIDENCE": frozenset(
        {
            "evidence",
            "artifact",
            "receipt",
            "activity",
            "observation",
            "log",
            "happened",
            "trace",
            "submission",
            "read-",
            "act ",
        }
    ),
}

PROPAGATION_HINTS: dict[str, list[str]] = {
    "SELF": [
        "Identity-facing prompt behavior and self-knowledge summaries may render differently.",
        "Voice calibration paths may shift if IX slices change.",
    ],
    "SELF-LIBRARY": [
        "Library retrieval and reference ranking may shift (`users/<id>/self-library.md`, index builds).",
        "Domain shelves and return-to sources may surface differently.",
    ],
    "SKILLS": [
        "Skill cards, capability doctrine, and prompt scaffolds may shift.",
        "Memory briefs and operator dashboards may quote revised skill language.",
    ],
    "EVIDENCE": [
        "Evidence summaries and downstream receipts may render differently.",
        "Review packets may inherit revised evidence framing.",
    ],
}


@dataclass
class ShadowCandidate:
    """Normalized inputs for scoring (from gate row, JSON file, or CLI)."""

    candidate_id: str
    proposal_summary: str = ""
    proposed_change: str = ""
    yaml_target: str = ""
    why_now: str = ""
    supporting_evidence_refs: list[str] = field(default_factory=list)
    contradiction_refs: list[str] = field(default_factory=list)
    source_observation_ids: list[str] = field(default_factory=list)
    confidence: float | None = None


def infer_best_fit_surface(candidate: ShadowCandidate) -> tuple[str, dict[str, int]]:
    """
    Keyword-based best-fit surface; weak +1 toward declared target when it maps to a bucket.
    """
    text = " ".join(
        [
            candidate.proposal_summary or "",
            candidate.proposed_change or "",
            candidate.why_now or "",
            " ".join(candidate.supporting_evidence_refs),
        ]
    ).lower()
    scores: dict[str, int] = {s: 0 for s in REPORT_SURFACES}
    for surface, keywords in SURFACE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[surface] += 1

    decl = (candidate.yaml_target or "").strip().upper()
    if decl in REPORT_SURFACES:
        scores[decl] += 1

    best_surface = max(scores.items(), key=lambda kv: kv[1])[0]
    if all(v == 0 for v in scores.values()):
        best_surface = decl if decl in REPORT_SURFACES else "SELF"
    return best_surface, scores


def narrative_risk_keyword_overlay(candidate: ShadowCandidate) -> tuple[str, str | None]:
    """Decisive language with weak supporting structure → higher narrative risk (heuristic)."""
    text = (
        (candidate.proposal_summary or "") + " " + (candidate.proposed_change or "")
    ).lower()
    evidence_count = len(candidate.supporting_evidence_refs)
    contradiction_count = len(candidate.contradiction_refs)
    decisive_terms = ("always", "permanent", "definitive", "must", "locked", "canonical", "forever")
    decisive_hits = sum(1 for t in decisive_terms if t in text)
    if evidence_count == 0 and decisive_hits >= 2:
        return "high", "Decisive/durable wording with no supporting_evidence_refs in payload — review certainty."
    if contradiction_count and decisive_hits:
        return "high", "Decisive wording alongside contradiction refs — risk of overstated certainty."
    if evidence_count == 0 and decisive_hits:
        return "medium", "Decisive tone without explicit supporting evidence refs in payload."
    return "low", None


def sketch_classify_risk_vs_keywords(
    resolved_primary: str,
    best_keyword_fit: str,
    contradiction_refs: list[str],
    supporting_evidence_refs: list[str],
) -> tuple[str, str | None]:
    """Sketch-style mismatch signal between resolved surface and keyword best-fit."""
    rp = resolved_primary if resolved_primary in REPORT_SURFACES else None
    bk = best_keyword_fit if best_keyword_fit in REPORT_SURFACES else None
    if not rp or not bk or rp == bk:
        return "low", None
    ccount = len(contradiction_refs)
    scount = len(supporting_evidence_refs)
    if ccount or scount == 0:
        return "high", (
            f"Resolved surface **{rp}** vs keyword best-fit **{bk}** with weak support or conflicts — "
            "confirm ontology before merge."
        )
    return "medium", (
        f"Resolved surface **{rp}** vs keyword best-fit **{bk}** — content may fit another canonical bucket."
    )


def _find_candidate_row(
    user_id: str, candidate_id: str, *, repo_root: Path | None
) -> dict | None:
    for row in parse_review_candidates(user_id=user_id, repo_root=repo_root):
        if row["id"] == candidate_id:
            return row
    return None


def _extract_source_observation_ids(yaml_body: str) -> list[str]:
    lines = yaml_body.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith("source_observation_ids:"):
            i += 1
            while i < len(lines):
                ln = lines[i]
                if not ln.strip():
                    i += 1
                    continue
                m = re.match(r"^(\s*)-\s+(.+)$", ln)
                if m:
                    val = m.group(2).strip()
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]
                    elif val.startswith("'") and val.endswith("'"):
                        val = val[1:-1]
                    out.append(val)
                    i += 1
                    continue
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s", ln):
                    break
                i += 1
            break
        i += 1
    return out


def _extract_yaml_string_list(yaml_body: str, key: str) -> list[str]:
    """Parse `key:` followed by indented `- "item"` lines (same shape as source_observation_ids)."""
    prefix = f"{key}:"
    lines = yaml_body.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith(prefix):
            i += 1
            while i < len(lines):
                ln = lines[i]
                if not ln.strip():
                    i += 1
                    continue
                m = re.match(r"^(\s*)-\s+(.+)$", ln)
                if m:
                    val = m.group(2).strip()
                    if val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]
                    elif val.startswith("'") and val.endswith("'"):
                        val = val[1:-1]
                    out.append(val)
                    i += 1
                    continue
                if re.match(r"^[A-Za-z_][A-Za-z0-9_]*:\s", ln):
                    break
                i += 1
            break
        i += 1
    return out


def shadow_candidate_from_gate_row(
    row: dict,
    *,
    yaml_target: str,
    proposal_summary: str,
    proposed_change: str,
    raw_block: str,
) -> ShadowCandidate:
    return ShadowCandidate(
        candidate_id=str(row.get("id") or "UNKNOWN"),
        proposal_summary=proposal_summary,
        proposed_change=proposed_change,
        yaml_target=yaml_target,
        why_now=_extract_scalar(raw_block, "why_now"),
        supporting_evidence_refs=_extract_yaml_string_list(raw_block, "supporting_evidence_refs"),
        contradiction_refs=_extract_yaml_string_list(raw_block, "contradiction_refs"),
        source_observation_ids=_extract_source_observation_ids(raw_block),
        confidence=_parse_confidence_scalar(raw_block),
    )


def _parse_confidence_scalar(raw_block: str) -> float | None:
    s = _extract_scalar(raw_block, "confidence")
    if not s or s.lower() == "null":
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _map_boundary_bucket(surface: str) -> str:
    s = (surface or "").strip().upper()
    if s in ("SELF-KNOWLEDGE", "SELF"):
        return "SELF"
    if "CIV-MEM" in s or s in ("SELF-LIBRARY", "CIV-MEM / SELF-LIBRARY"):
        return "SELF-LIBRARY"
    if s == "WORK-LAYER":
        return "WORK-LAYER"
    if s == "SKILLS":
        return "SKILLS"
    if s == "EVIDENCE":
        return "EVIDENCE"
    return s or "SELF"


def _resolve_primary_surface(
    *,
    yaml_target: str,
    row: dict | None,
) -> str:
    yt = (yaml_target or "").strip().upper()
    if yt in YAML_TARGET_SURFACES and yt != "OTHER":
        return yt
    if yt == "OTHER":
        return "OTHER"
    if row is None:
        return "SELF"
    br = row.get("boundary_review") or {}
    pc = (row.get("proposal_class") or "").upper()
    pt = (row.get("profile_target") or "").upper()

    if pc.startswith("CIV_MEM") or "CIV-MEM" in pc:
        return "SELF-LIBRARY"
    if pc.startswith("SELF_LIBRARY") or "SELF-LIBRARY" in pc:
        return "SELF-LIBRARY"
    if "SKILL" in pc or "SELF-SKILL" in pt or "SKILLS" in pt:
        return "SKILLS"
    if "EVIDENCE" in pt or "ARCHIVE" in pt or "§" in pt:
        return "EVIDENCE"
    if br.get("target_surface") == "WORK-LAYER":
        return "WORK-LAYER"

    return "SELF"


def _surface_order(primary: str) -> tuple[str, ...]:
    if primary not in REPORT_SURFACES:
        return REPORT_SURFACES
    rest = [s for s in REPORT_SURFACES if s != primary]
    return (primary, *rest)


def _surface_diff_lines(
    surface: str,
    primary: str,
    row: dict | None,
    proposed_change: str,
    yaml_target: str,
) -> list[str]:
    lines: list[str] = []
    pc = (row.get("proposal_class") if row else "") or ""
    pt = (row.get("profile_target") if row else "") or ""
    has_prompt = bool(row and row.get("has_prompt_change"))

    if surface == "SELF":
        if primary in ("SELF", "WORK-LAYER") or (
            yaml_target == "SELF" and primary == "OTHER"
        ):
            lines.append("Expected: IX-A/B/C or narrative block edits aligned with `profile_target` and `suggested_entry`.")
            if pt:
                lines.append(f"- Anchors: `{pt[:120]}{'…' if len(pt) > 120 else ''}`")
        else:
            lines.append("No direct SELF edit expected if merge routes elsewhere — watch for interpretation drift in Voice/prompt.")
        if row and row.get("has_multi_target"):
            lines.append("- **Multi-target** flags: reconcile sections so Voice prompt slices stay coherent.")

    elif surface == "SELF-LIBRARY":
        if primary == "SELF-LIBRARY" or pc.startswith(("CIV_MEM", "SELF_LIBRARY")):
            lines.append("Expected: library index / CIV-MEM pointer rows or READ/LIB entries as per proposal.")
            if "LIB-" in (row.get("summary") or "") + proposed_change:
                lines.append("- LIB-id references may need index sync (`scripts/build_library_index.py` → `artifacts/library-index.md`).")
        else:
            lines.append("No direct SELF-LIBRARY file edit expected unless content is corpus-like (see Classification risk).")

    elif surface == "SKILLS":
        if primary == "SKILLS" or "SKILL" in pc.upper():
            lines.append("Expected: `users/<id>/self-skills.md` capability lines or skill-card sources.")
            lines.append("- Regenerate skill cards after merge: `python scripts/build_skill_cards.py` → `artifacts/skill-cards/`.")
        else:
            lines.append("No SKILLS file change expected unless proposal explicitly targets capability index.")

    elif surface == "EVIDENCE":
        if primary == "EVIDENCE":
            lines.append("Expected: dated `self-archive.md` spine entry or stub per merge protocol.")
        else:
            lines.append("EVIDENCE spine usually unchanged for pure IX edits; supporting refs may still need narration alignment.")

    if has_prompt and surface == "SELF" and (surface == primary or primary == "WORK-LAYER"):
        lines.append("- **bot/prompt.py** may need a coordinated slice if `prompt_addition` ships with this merge.")

    if not lines:
        lines.append("No strong direct signal for this surface in v1 heuristics — treat as low-touch unless content says otherwise.")

    return lines


def _propagation_lines(
    row: dict | None,
    primary: str,
    env: dict[str, Any] | None,
) -> list[str]:
    pk = primary if primary in REPORT_SURFACES else "SELF"
    out: list[str] = [
        "These are **likely** touch points, not guarantees:",
    ]
    for hint in PROPAGATION_HINTS.get(pk, []):
        out.append(f"- {hint}")
    if pk == "SKILLS":
        out.append(
            "- **scripts/compress_active_lane.py** → **artifacts/context/** — active-lane compression may reflect revised capability language."
        )
    if pk == "SELF-LIBRARY":
        out.append(
            "- **scripts/build_library_index.py** → **artifacts/library-index.md** — library overview may shift after library edits."
        )
    if pk == "SELF":
        out.append(
            "- **Identity-facing prompt behavior** — `bot/prompt.py` slices tied to IX may shift with merge content."
        )
    if pk == "EVIDENCE":
        out.append(
            "- **Gate board / review dashboards** — **artifacts/gate-board.md**, **artifacts/review-dashboard.md** may reflect new evidence framing after merge."
        )
    if row and row.get("has_prompt_change"):
        out.append("- **bot/prompt.py** — prompt_addition or section mapping may require an edit in the same merge batch.")
    if primary in ("SKILLS",):
        out.append("- **artifacts/skill-cards/** — rebuild after `self-skills.md` changes (`scripts/build_skill_cards.py`).")
    if primary in ("SELF", "SELF-LIBRARY", "EVIDENCE"):
        out.append("- **artifacts/review-dashboard.md**, **artifacts/gate-board.md** — derived gate views change after queue/processed state changes post-merge (not by this simulator).")
    out.append("- **scripts/runtime/memory_brief.py** — lane ranking / brief emphasis may shift if this merge reorders capability or identity themes.")
    out.append("- **prepared-context/** — compression and quotes may pull revised boundary language on next budgeted build.")
    if env:
        out.append("- **Uncertainty sidecars** — envelope-style signals may feed review packets and briefs; advisory only.")
    return out


def _classification_risk(
    row: dict | None,
    primary: str,
    yaml_target: str,
) -> tuple[str, list[str]]:
    lines: list[str] = []
    level = "low"
    if row:
        br = row.get("boundary_review") or {}
        if br.get("misfiled_warning"):
            level = "medium"
            lines.append(br["misfiled_warning"])
        yb = _map_boundary_bucket(yaml_target) if yaml_target else ""
        sug = _map_boundary_bucket(str(br.get("suggested_surface") or ""))
        if (
            yaml_target
            and yb in REPORT_SURFACES
            and sug in REPORT_SURFACES
            and yb != sug
        ):
            level = "high" if level == "medium" else "medium"
            lines.append(
                f"Declared YAML/target bucket **{yb}** vs boundary suggested **{sug}** — confirm ontology before merge."
            )
        if row.get("has_multi_target"):
            level = "medium"
            lines.append("Multi-target prompt/profile hints increase classification surface area.")

    if not lines:
        lines.append("No strong misfile signal in v1 heuristics — still verify `proposal_class` vs intended durable home.")

    return level, lines


def _narrative_risk(
    row: dict | None,
    env: dict[str, Any] | None,
) -> tuple[str, list[str]]:
    lines: list[str] = []
    level = "low"
    if row:
        if row.get("has_conflict_markers"):
            level = "medium"
            lines.append("Gate text flags **conflict / contradiction / advisory** — resolve before treating narrative as settled.")
        if row.get("duplicate_hints"):
            level = "medium"
            lines.append(f"Duplicate / overlap hints: {row.get('duplicate_hints')}")
        if row.get("advisory_flagged"):
            level = "high"
            lines.append("Pipeline advisory flagged — treat certainty claims with extra skepticism.")
    if env:
        fh = env.get("fabricated_history_risk")
        ev = env.get("evidence_state")
        if fh == "high":
            level = "high"
        elif fh == "medium" and level == "low":
            level = "medium"
        if fh in ("high", "medium"):
            lines.append(
                f"Uncertainty envelope: evidence_state=`{ev}`, fabricated_history_risk=`{fh}` (advisory signals, not approval)."
            )
        if env.get("conflicting_refs"):
            lines.append(f"Conflicting refs in envelope: {env.get('conflicting_refs')}")
        if env.get("missing_evidence_refs"):
            lines.append(f"Missing evidence signals: {env.get('missing_evidence_refs')}")
    if not lines:
        lines.append("No extra narrative-risk flags beyond standard gate review.")
    return level, lines


def _conditions(primary: str, row: dict | None) -> list[str]:
    xs = [
        "Companion intent matches the stated `summary` and durable home for this fact or capability.",
        "No unresolved contradiction with existing SELF or EVIDENCE (or contradiction is explicitly preserved with provenance).",
    ]
    if primary == "SKILLS":
        xs.append("The change belongs in governed capability (`self-skills.md`), not only in a work-layer habit.")
    if primary == "SELF-LIBRARY":
        xs.append("Corpus or LIB references stay on the library side of the identity/library boundary.")
    if row and row.get("has_prompt_change"):
        xs.append("Prompt deltas are reviewed for Voice tone and knowledge-boundary compliance.")
    return xs


def _operator_question(primary: str, row: dict | None) -> str:
    if primary == "SKILLS":
        return (
            "If this change were merged, would it clarify **governed capability** — or bake a **work-layer preference** "
            "into durable doctrine too early?"
        )
    if primary == "SELF-LIBRARY":
        return (
            "Would approval keep reference/corpus material in the **library plane** — or let it behave like **identity fact**?"
        )
    if primary == "WORK-LAYER":
        return (
            "Does this stay clearly in **WORK / operator** territory — or would merge accidentally **promote** it into SELF?"
        )
    return (
        "If this change were true, would it **clarify** the fork — or **compress ambiguity** and read more certain than the evidence?"
    )


def _load_observations_by_ids(oids: list[str]) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    missing: list[str] = []
    for oid in oids:
        r = obs_by_id(oid)
        if r:
            rows.append(r)
        else:
            missing.append(oid)
    return rows, missing


def shadow_candidate_from_json_payload(payload: dict[str, Any]) -> ShadowCandidate:
    why = payload.get("why_now")
    return ShadowCandidate(
        candidate_id=str(payload.get("gate_candidate_id") or payload.get("candidate_id") or "FILE-PROPOSAL"),
        proposal_summary=str(payload.get("proposal_summary") or payload.get("summary") or ""),
        proposed_change=str(payload.get("proposed_change") or ""),
        yaml_target=str(payload.get("target_surface") or ""),
        why_now=str(why).strip() if why is not None else "",
        supporting_evidence_refs=[str(x) for x in (payload.get("supporting_evidence_refs") or [])],
        contradiction_refs=[str(x) for x in (payload.get("contradiction_refs") or [])],
        source_observation_ids=[str(x) for x in (payload.get("source_observation_ids") or [])],
        confidence=payload.get("confidence") if isinstance(payload.get("confidence"), (int, float)) else None,
    )


def _level_rank(level: str) -> int:
    return {"low": 0, "medium": 1, "high": 2}.get(level, 0)


def _max_level(a: str, b: str) -> str:
    return a if _level_rank(a) >= _level_rank(b) else b


def build_report_markdown(
    *,
    built_iso: str,
    mode: str,
    sc: ShadowCandidate,
    row: dict | None,
    env: dict[str, Any] | None,
    missing_obs: list[str],
) -> str:
    primary = _resolve_primary_surface(yaml_target=sc.yaml_target, row=row)
    br = (row.get("boundary_review") if row else {}) or {}
    best_fit, kw_scores = infer_best_fit_surface(sc)
    proposed_change = sc.proposed_change
    yaml_target = sc.yaml_target

    lines: list[str] = [
        "# Shadow Merge Report",
        "",
        f"Built: {built_iso}",
        f"Candidate: {sc.candidate_id}",
        f"Target surface (resolved): **{primary}**",
        f"Predicted best-fit (keywords): **{best_fit}**",
        f"Keyword score signals: {kw_scores}",
        f"Mode: {mode}",
        "",
    ]
    if primary in REPORT_SURFACES and best_fit in REPORT_SURFACES and primary != best_fit:
        lines.append(
            f"**Claimed vs best-fit:** resolved target **{primary}** differs from keyword best-fit **{best_fit}** — reconcile before merge."
        )
        lines.append("")

    lines.extend(
        [
            "**Boundary:**",
            "This report is a **non-mutating preview**. It does not update SELF, SELF-LIBRARY, SKILLS, EVIDENCE, or `recursion-gate.md`.",
            "",
            "## Proposed change",
            "",
            f"**Summary:** {sc.proposal_summary or '_(none)_'}",
            "",
            "### Proposed change body",
            "",
            proposed_change.strip() or "_(empty)_",
            "",
            "## Surface diff preview",
            "",
        ]
    )

    for surf in _surface_order(primary if primary in REPORT_SURFACES else "SELF"):
        lines.append(f"### {surf}")
        for bullet in _surface_diff_lines(surf, primary, row, proposed_change, yaml_target):
            lines.append(f"- {bullet}")
        lines.append("")

    lines.append("## Propagation effects")
    lines.append("")
    for p in _propagation_lines(row, primary, env):
        lines.append(f"- {p}")
    lines.append("")

    cr_level, cr_expl = _classification_risk(row, primary, yaml_target)
    sk_level, sk_reason = sketch_classify_risk_vs_keywords(
        primary,
        best_fit,
        sc.contradiction_refs,
        sc.supporting_evidence_refs,
    )
    if sk_reason:
        cr_level = _max_level(cr_level, sk_level)
        cr_expl.append(sk_reason)

    lines.append("## Classification risk")
    lines.append("")
    lines.append(f"- **Level:** {cr_level}")
    for e in cr_expl:
        lines.append(f"- {e}")
    if yaml_target:
        lines.append(f"- YAML `target_surface` (when present): `{yaml_target}`")
    if br:
        lines.append(
            f"- Boundary review (heuristic): target=`{br.get('target_surface')}` suggested=`{br.get('suggested_surface')}` "
            f"confidence=`{br.get('confidence')}`"
        )
    lines.append("")

    nr_level, nr_expl = _narrative_risk(row, env)
    kw_nr_level, kw_nr_reason = narrative_risk_keyword_overlay(sc)
    nr_level = _max_level(nr_level, kw_nr_level)
    if kw_nr_reason:
        nr_expl.append(kw_nr_reason)

    lines.append("## Narrative risk")
    lines.append("")
    lines.append(f"- **Level:** {nr_level}")
    for e in nr_expl:
        lines.append(f"- {e}")
    if missing_obs:
        lines.append(
            f"- **Observation IDs not found in ledger:** {', '.join(missing_obs)} — envelope omitted partial IDs."
        )
    lines.append("")

    lines.append("## Support snapshot")
    lines.append("")
    lines.append(f"- **supporting_evidence_refs (payload/YAML):** {len(sc.supporting_evidence_refs)}")
    lines.append(f"- **contradiction_refs (payload/YAML):** {len(sc.contradiction_refs)}")
    lines.append(f"- **source_observation_ids:** {len(sc.source_observation_ids)} listed")
    lines.append(
        f"- **confidence (payload/YAML):** {sc.confidence if sc.confidence is not None else 'n/a'}"
    )
    if env:
        lines.append(
            f"- **Uncertainty envelope (advisory):** evidence_state=`{env.get('evidence_state')}` "
            f"fabricated_history_risk=`{env.get('fabricated_history_risk')}` "
            f"promotion_recommendation=`{env.get('promotion_recommendation')}`"
        )
    lines.append("")

    lines.append("## What would have to be true for this merge to be clearly correct?")
    lines.append("")
    for c in _conditions(primary, row):
        lines.append(f"- {c}")
    lines.append("")

    lines.append("## Operator question")
    lines.append("")
    lines.append(_operator_question(primary, row))
    lines.append("")

    return "\n".join(lines)


def _default_output_path(candidate_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9._-]+", "-", candidate_id).strip("-") or "shadow-report"
    DEFAULT_SHADOW_MERGE_DIR.mkdir(parents=True, exist_ok=True)
    return DEFAULT_SHADOW_MERGE_DIR / f"{safe}.md"


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Shadow Merge Simulator — write a non-mutating Markdown preview report."
    )
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", DEFAULT_USER).strip() or DEFAULT_USER)
    ap.add_argument("--repo-root", type=Path, default=None, help="Repository root (for tests; default: cwd inference)")
    ap.add_argument("--candidate", default=None, help="CANDIDATE-NNNN from pending gate section")
    ap.add_argument(
        "--proposal-file",
        type=Path,
        default=None,
        help="JSON file (schema-aligned gate candidate payload; see schema-registry/recursion-gate-candidate.schema.json)",
    )
    ap.add_argument("--target-surface", default=None, help="Proposal mode: SELF | SELF-LIBRARY | SKILLS | EVIDENCE | OTHER")
    ap.add_argument("--proposal-summary", default=None, help="Proposal mode: one-line summary")
    ap.add_argument("--proposed-change", default=None, help="Proposal mode: proposed change body")
    ap.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help=f"Write Markdown report here (default: {DEFAULT_SHADOW_MERGE_DIR}/<candidate-id>.md)",
    )
    args = ap.parse_args()

    repo_root = args.repo_root.resolve() if args.repo_root else None

    has_proposal = (
        bool(args.target_surface and str(args.target_surface).strip())
        and args.proposal_summary is not None
        and args.proposed_change is not None
    )
    proposal_any = (
        bool(args.target_surface and str(args.target_surface).strip())
        or args.proposal_summary is not None
        or args.proposed_change is not None
    )
    if proposal_any and not has_proposal:
        print(
            "error: proposal mode requires --target-surface, --proposal-summary, and --proposed-change together",
            file=sys.stderr,
        )
        return 2

    modes = sum(
        1
        for x in (
            bool(args.candidate and str(args.candidate).strip()),
            bool(args.proposal_file),
            has_proposal,
        )
        if x
    )
    if modes != 1:
        print(
            "error: specify exactly one of: --candidate, --proposal-file PATH, or proposal mode "
            "(--target-surface + --proposal-summary + --proposed-change)",
            file=sys.stderr,
        )
        return 2

    built = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row: dict | None = None
    raw_block = ""
    sc: ShadowCandidate
    mode = "simulation_only"

    if args.candidate:
        candidate_id = args.candidate.strip()
        row = _find_candidate_row(args.user, candidate_id, repo_root=repo_root)
        if row is None:
            print(
                f"error: candidate not found in active gate section: {candidate_id}",
                file=sys.stderr,
            )
            return 2
        raw_block = row.get("raw_block") or ""
        yaml_target = _extract_scalar(raw_block, "target_surface")
        proposal_summary = (
            _extract_scalar(raw_block, "proposal_summary").strip()
            or (row.get("summary") or "").strip()
        )
        proposed_change = _extract_block(raw_block, "proposed_change").strip() or (
            (row.get("suggested_entry") or "")[:4000]
        )
        sc = shadow_candidate_from_gate_row(
            row,
            yaml_target=yaml_target,
            proposal_summary=proposal_summary,
            proposed_change=proposed_change,
            raw_block=raw_block,
        )
        mode = "simulation_only"
    elif args.proposal_file:
        path = args.proposal_file
        if not path.is_absolute():
            path = (repo_root if repo_root else REPO_ROOT) / path
        if not path.is_file():
            print(f"error: proposal file not found: {path}", file=sys.stderr)
            return 2
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"error: invalid JSON: {exc}", file=sys.stderr)
            return 2
        if not isinstance(payload, dict):
            print("error: proposal JSON must be an object", file=sys.stderr)
            return 2
        sc = shadow_candidate_from_json_payload(payload)
        mode = "simulation_only (proposal file)"
    else:
        yaml_target = (args.target_surface or "").strip()
        proposal_summary = (args.proposal_summary or "").strip()
        proposed_change = (args.proposed_change or "").strip()
        sc = ShadowCandidate(
            candidate_id="DIRECT-PROPOSAL",
            proposal_summary=proposal_summary,
            proposed_change=proposed_change,
            yaml_target=yaml_target,
        )
        mode = "simulation_only (proposal text)"

    if not sc.proposal_summary.strip() and not sc.proposed_change.strip():
        print("error: candidate/proposal has no proposal_summary or proposed_change content", file=sys.stderr)
        return 2

    env: dict[str, Any] | None = None
    obs_rows, missing_obs = _load_observations_by_ids(sc.source_observation_ids)
    if obs_rows:
        env = compute_envelope(obs_rows)

    md = build_report_markdown(
        built_iso=built,
        mode=mode,
        sc=sc,
        row=row,
        env=env,
        missing_obs=missing_obs,
    )

    out = args.output
    if out is None:
        out = _default_output_path(sc.candidate_id)
    else:
        out = Path(out)
        if not out.is_absolute():
            out = REPO_ROOT / out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"wrote {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
