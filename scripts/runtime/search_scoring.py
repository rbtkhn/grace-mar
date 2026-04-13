"""Deterministic keyword scoring for runtime observation search (PR2)."""

from __future__ import annotations

from datetime import datetime, timezone


def tokenize(text: str) -> list[str]:
    return [t for t in text.lower().split() if t]


def parse_obs_timestamp(s: str | None) -> datetime | None:
    if not s or not isinstance(s, str):
        return None
    t = s.strip()
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(t)
    except ValueError:
        return None


def parse_cli_datetime(s: str | None) -> datetime | None:
    """Parse CLI --since / --until values (ISO date-time)."""
    if not s or not str(s).strip():
        return None
    return parse_obs_timestamp(s.strip())


def recency_bonus(obs_ts: str | None, *, now: datetime | None = None) -> float:
    """0..1 linear decay over 7 days."""
    dt = parse_obs_timestamp(obs_ts)
    if dt is None:
        return 0.0
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    now = now or datetime.now(timezone.utc)
    age_sec = (now - dt).total_seconds()
    if age_sec < 0:
        return 1.0
    week = 7 * 24 * 3600
    return max(0.0, 1.0 - age_sec / week)


def confidence_bonus(conf: object) -> float:
    """Small bump; keeps scores interpretable vs keyword matches."""
    if isinstance(conf, (int, float)):
        return 0.25 * max(0.0, min(1.0, float(conf)))
    return 0.0


def score_observation(
    obs: dict,
    query: str,
    *,
    bonus_tags: list[str],
) -> float:
    """
    PR2 minimal formula (no embeddings):
    - exact phrase in title: +10
    - all query terms in title: +7
    - exact phrase in summary: +6
    - all query terms in summary: +4
    - +2 per CLI tag present on observation
    - recency 0..1, confidence bump
    """
    score = 0.0
    q = query.strip().lower()
    terms = tokenize(query)

    title = (obs.get("title") or "").lower()
    summary = (obs.get("summary") or "").lower()
    obs_tags = [t.lower() for t in (obs.get("tags") or [])]

    if q:
        if q in title:
            score += 10.0
        if terms and all(t in title for t in terms):
            score += 7.0
        if q in summary:
            score += 6.0
        if terms and all(t in summary for t in terms):
            score += 4.0

    for tag in bonus_tags:
        if tag.lower() in obs_tags:
            score += 2.0

    score += recency_bonus(obs.get("timestamp"))
    score += confidence_bonus(obs.get("confidence"))

    return score


def ts_sort_key(obs: dict) -> float:
    dt = parse_obs_timestamp(obs.get("timestamp"))
    if dt is None:
        return 0.0
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.timestamp()
