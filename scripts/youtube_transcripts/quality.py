from __future__ import annotations


def compute_quality(
    text: str,
    duration_seconds: float | None,
    tier: str,
    coverage_seconds: float | None,
) -> float:
    """
    Heuristic 0..1: tier base × time coverage × text density.
    """
    base = {
        "tier1_api": 0.95,
        "tier2_manual": 0.82,
        "tier2_auto": 0.65,
        "tier3_whisper": 0.55,
        "none": 0.2,
    }.get(tier, 0.5)

    cov_factor = 1.0
    if duration_seconds and duration_seconds > 0 and coverage_seconds is not None:
        cov_factor = min(1.0, max(0.0, float(coverage_seconds) / float(duration_seconds)))
    elif duration_seconds and duration_seconds > 0:
        # chars/sec heuristic ~5–20 for speech
        char_rate = len(text) / float(duration_seconds)
        cov_factor = min(1.0, char_rate / 10.0)

    density = 1.0 if not text else min(1.0, len(text.strip()) / 50.0)
    score = base * (0.55 + 0.45 * cov_factor) * (0.75 + 0.25 * density)
    return max(0.0, min(1.0, score))


def tier_from_parts(source_tier: str, sub_kind: str | None) -> str:
    if source_tier == "ytdlp":
        return "tier2_manual" if sub_kind == "manual" else "tier2_auto"
    if source_tier == "whisper":
        return "tier3_whisper"
    return "tier1_api"
