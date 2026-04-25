#!/usr/bin/env python3
"""
Resolve coffee-conductor helpers for the fixed **D1–D5** menu.

Pure functions over event dicts shaped like ``audit_cadence_rhythm.parse_events()``
output: ``{"dt", "kind", "user", "line", "kv"}``.

The menu letters are now stable:

- ``D1`` → Toscanini
- ``D2`` → Furtwangler
- ``D3`` → Bernstein
- ``D4`` → Karajan
- ``D5`` → Kleiber

This module still helps with two advisory questions:

1. Which conductor was picked most recently on disk? (continuity)
2. Which conductor does the system recommend from dream + load signals? (recommendation)

Those helpers may be mentioned in prose around the menu, but they no longer determine the
lettering itself.
"""

from __future__ import annotations

from typing import Any

MENU_PICK_TO_CONDUCTOR = {
    "D1": "toscanini",
    "D2": "furtwangler",
    "D3": "bernstein",
    "D4": "karajan",
    "D5": "kleiber",
}
CONDUCTOR_TO_MENU_PICK = {slug: pick for pick, slug in MENU_PICK_TO_CONDUCTOR.items()}

# Legacy logs may still contain ``picked=D`` from the older single-line conductor menu.
_PICKED_CONDUCTOR = frozenset({"D", *MENU_PICK_TO_CONDUCTOR.keys()})


def normalize_conductor_slug(value: str) -> str:
    """Return first segment if legacy ``a+b`` stacks; else stripped value."""
    s = str(value).strip()
    if "+" in s:
        return s.split("+", 1)[0].strip()
    return s


def conductor_slug_for_menu_pick(pick: str) -> str | None:
    """Return conductor slug for ``D1``..``D5``; unknown picks → ``None``."""
    return MENU_PICK_TO_CONDUCTOR.get(str(pick).strip().upper())


def menu_pick_for_conductor_slug(slug: str) -> str | None:
    """Return menu pick for a conductor slug, normalizing legacy ``a+b`` stacks."""
    return CONDUCTOR_TO_MENU_PICK.get(normalize_conductor_slug(slug))


def last_coffee_pick_conductor_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Most recent ``coffee_pick`` with a conductor-bearing ``picked=`` value."""
    candidates: list[dict[str, Any]] = []
    for e in events:
        if e.get("kind") != "coffee_pick":
            continue
        kv = e.get("kv") or {}
        picked = str(kv.get("picked", "")).strip()
        if picked not in _PICKED_CONDUCTOR:
            continue
        cond = kv.get("conductor")
        if cond is None or not str(cond).strip():
            continue
        candidates.append(e)
    if not candidates:
        return None
    return max(candidates, key=lambda x: x["dt"])


def last_logged_conductor(events: list[dict[str, Any]]) -> str | None:
    """Normalized conductor slug from last qualifying ``coffee_pick``, or ``None``."""
    ev = last_coffee_pick_conductor_event(events)
    if ev is None:
        return None
    c = (ev.get("kv") or {}).get("conductor")
    if c is None:
        return None
    return normalize_conductor_slug(str(c))


def focus_for_last_conductor(events: list[dict[str, Any]]) -> str | None:
    """Last ``focus=`` or ``arc=`` on a qualifying ``coffee_pick`` (``focus`` wins)."""
    ev = last_coffee_pick_conductor_event(events)
    if ev is None:
        return None
    kv = ev.get("kv") or {}
    if "focus" in kv and str(kv.get("focus", "")).strip():
        return str(kv["focus"]).strip()
    if "arc" in kv and str(kv.get("arc", "")).strip():
        return str(kv["arc"]).strip()
    return None


def recommended_conductor_from_menu_recommendation(letter: str) -> str:
    """Map session-load letter to conductor slug; unknown letter → ``furtwangler``."""
    m = {"A": "toscanini", "B": "kleiber", "C": "bernstein"}
    key = str(letter).strip().upper()[:1]
    return m.get(key, "furtwangler")


def _dream_implies_risky_worktree_seam(dream: dict[str, Any]) -> bool:
    if dream.get("risky_worktree") is True:
        return True
    wt = str(dream.get("worktreeAdvice") or "").lower()
    if not wt.strip():
        return False
    # seam / merge / conflict / explicit worktree caution
    markers = ("seam", "merge", "conflict", "risky", "dirty", "rebase", "worktree")
    return any(m in wt for m in markers)


def _dream_implies_steward_or_tomorrow(dream: dict[str, Any]) -> bool:
    if str(dream.get("tomorrow_inherits") or "").strip():
        return True
    sh = str(dream.get("steward_hint") or "").strip().lower()
    if sh and sh not in ("false", "0", "no", ""):
        return True
    st = str(dream.get("steward") or "").strip().lower()
    if st and st not in ("false", "0", "no", ""):
        return True
    summary = str(dream.get("summary") or "").lower()
    return "steward" in summary and "gate" in summary


def _dream_implies_long_arc_balance(dream: dict[str, Any]) -> bool:
    text = " ".join(
        str(dream.get(key) or "")
        for key in ("summary", "tomorrow_inherits", "dream_to_coffee_menu", "long_arc_hint")
    ).lower()
    if not text.strip():
        return False
    markers = ("month", "meta", "balance", "blend", "arc", "shape", "architecture", "polish")
    return any(marker in text for marker in markers)


def system_recommended_conductor(
    *,
    dream: dict[str, Any] | None = None,
    assess: dict[str, Any] | None = None,
) -> str:
    """Layered conductor recommendation from dream + load signals.

    Order: (1) risky worktree / ``worktreeAdvice`` → **toscanini**;
    (2) ``tomorrow_inherits`` or steward-style hint → **kleiber**;
    (3) long-arc / balance hints → **karajan**;
    (4) ``assess["recommended"]`` → A/B/C map;
    (5) **furtwangler**.
    """
    if dream:
        if _dream_implies_risky_worktree_seam(dream):
            return "toscanini"
        if _dream_implies_steward_or_tomorrow(dream):
            return "kleiber"
        if _dream_implies_long_arc_balance(dream):
            return "karajan"
    if assess:
        rec = assess.get("recommended")
        if isinstance(rec, str) and rec.strip():
            letter = rec.strip().upper()[:1]
            if letter in ("A", "B", "C"):
                return recommended_conductor_from_menu_recommendation(letter)
    return "furtwangler"


def system_recommended_menu_pick(
    *,
    dream: dict[str, Any] | None = None,
    assess: dict[str, Any] | None = None,
) -> str:
    """Menu pick for the current recommendation helper."""
    slug = system_recommended_conductor(dream=dream, assess=assess)
    pick = menu_pick_for_conductor_slug(slug)
    if pick is None:
        raise ValueError(f"Unknown conductor slug: {slug}")
    return pick


def conductor_for_d1_continuation(events: list[dict[str, Any]]) -> str | None:
    """Backward-compatible alias for older D1 continuity wording."""
    return last_logged_conductor(events)


def focus_for_d1_continuation(events: list[dict[str, Any]]) -> str | None:
    """Backward-compatible alias for older D1 continuity wording."""
    return focus_for_last_conductor(events)


def d2_conductor_from_menu_recommendation(letter: str) -> str:
    """Backward-compatible alias for session-load recommendation helper."""
    return recommended_conductor_from_menu_recommendation(letter)


def d2_conductor_resolved(
    *,
    dream: dict[str, Any] | None = None,
    assess: dict[str, Any] | None = None,
) -> str:
    """Backward-compatible alias for recommendation helper."""
    return system_recommended_conductor(dream=dream, assess=assess)


def d2_conductor_from_assess_load(assess: dict[str, Any]) -> str:
    """Backward-compatible alias for assess-only recommendation helper."""
    return system_recommended_conductor(dream=None, assess=assess)
