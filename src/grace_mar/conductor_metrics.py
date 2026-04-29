"""Compose conductor-session-metrics envelope (derived WORK artifact only)."""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

_REPO_SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"
if str(_REPO_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_REPO_SCRIPTS))

from cadence_conductor_resolution import KNOWN_CONDUCTOR_SLUGS, normalize_conductor_slug  # noqa: E402

from grace_mar.conductor_evaluator import evaluate_markdown_menu

SCHEMA_VERSION = "conductor-session-metrics.v1"

_ALLOWED_ORIGINS = frozenset({"coffee", "conductor_only", "inferred"})


def build_metrics_payload(
    *,
    body_markdown: str,
    conductor_slug: str,
    session_origin: str,
    user: str,
    continuity_signal: float | None = None,
    recommendation_signal: float | None = None,
    warnings: list[str] | None = None,
    repo_root: Path | None = None,
) -> dict[str, object]:
    """Return dict aligned with schema-registry/conductor-session-metrics.v1.json."""
    slug = normalize_conductor_slug(conductor_slug)
    if slug not in KNOWN_CONDUCTOR_SLUGS:
        raise ValueError(f"unknown conductor_slug: {conductor_slug!r}")
    if session_origin not in _ALLOWED_ORIGINS:
        raise ValueError(f"invalid session_origin: {session_origin!r}")

    w = list(warnings or [])
    lines, scores = evaluate_markdown_menu(slug, body_markdown, repo_root=repo_root)
    if len(lines) == 0:
        w.append("no A–E option lines parsed from markdown.")

    merged_notes = {
        "discrimination": scores.score_notes.get("discrimination", ""),
        "grounding": scores.score_notes.get("grounding", ""),
        "actionability": scores.score_notes.get("actionability", ""),
        "fidelity": scores.score_notes.get("fidelity", ""),
    }

    created = datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")

    return {
        "schema_version": SCHEMA_VERSION,
        "created_at": created,
        "user": user,
        "conductor_slug": slug,
        "session_origin": session_origin,
        "action_mcq_count": len(lines),
        "grounding_reference_count": scores.grounding_reference_count,
        "discrimination_score": scores.discrimination_score,
        "grounding_score": scores.grounding_score,
        "actionability_score": scores.actionability_score,
        "fidelity_score": scores.fidelity_score,
        "continuity_signal": continuity_signal,
        "recommendation_signal": recommendation_signal,
        "warnings": w,
        "evaluation": {"method": "heuristic_v1", "deterministic": True},
        "score_notes": merged_notes,
    }

