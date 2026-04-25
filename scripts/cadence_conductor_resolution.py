#!/usr/bin/env python3
"""
Resolve **D1** continuation (conductor + optional focus) and **D2** conductor from
operational signals.

Pure functions over event dicts shaped like ``audit_cadence_rhythm.parse_events()``
output: ``{"dt", "kind", "user", "line", "kv"}``.

**D2 cross-cuts D1:** D1 answers "which movement continues last emphasis"; D2 answers
"what does the system recommend *this* session from dream + load" — orthogonal questions.
Repetition of one D1 slug reinforces one *mode*; rotation changes the mode; D2 can still
point elsewhere (e.g. Bernstein when ``recommended: C``).

``last-dream.json`` keys read for layered D2 (aligned with
``docs/skill-work/work-coffee/CONDUCTOR-PASS.md``):

- **Toscanini (1):** ``worktreeAdvice`` text suggesting seam/merge/worktree risk; or
  synthetic ``risky_worktree=true`` for tests.
- **Kleiber (5):** non-empty ``tomorrow_inherits``; or ``steward_hint`` / ``steward``
  truthy strings; or ``summary`` containing both "steward" and "gate".

Optional: wire ``operator_coffee.py`` to print D2 from ``d2_conductor_resolved`` — not
required for callers of this module.
"""

from __future__ import annotations

from typing import Any

# D1 menu accepts these ``picked=`` values for conductor continuation.
_PICKED_D1 = frozenset({"D1", "D2", "D"})


def normalize_conductor_slug(value: str) -> str:
    """Return first segment if legacy ``a+b`` stacks; else stripped value."""
    s = str(value).strip()
    if "+" in s:
        return s.split("+", 1)[0].strip()
    return s


def last_coffee_pick_conductor_event(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    """Most recent ``coffee_pick`` with ``picked`` in D1/D2/D and ``conductor=``."""
    candidates: list[dict[str, Any]] = []
    for e in events:
        if e.get("kind") != "coffee_pick":
            continue
        kv = e.get("kv") or {}
        picked = str(kv.get("picked", "")).strip()
        if picked not in _PICKED_D1:
            continue
        cond = kv.get("conductor")
        if cond is None or not str(cond).strip():
            continue
        candidates.append(e)
    if not candidates:
        return None
    return max(candidates, key=lambda x: x["dt"])


def conductor_for_d1_continuation(events: list[dict[str, Any]]) -> str | None:
    """Normalized conductor slug from last qualifying ``coffee_pick``, or ``None``."""
    ev = last_coffee_pick_conductor_event(events)
    if ev is None:
        return None
    c = (ev.get("kv") or {}).get("conductor")
    if c is None:
        return None
    return normalize_conductor_slug(str(c))


def focus_for_d1_continuation(events: list[dict[str, Any]]) -> str | None:
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


def d2_conductor_from_menu_recommendation(letter: str) -> str:
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


def d2_conductor_resolved(
    *,
    dream: dict[str, Any] | None = None,
    assess: dict[str, Any] | None = None,
) -> str:
    """Layered D2 resolution: dream signals first, then ``assess['recommended']``, else default.

    Order: (1) risky worktree / ``worktreeAdvice`` → **toscanini**;
    (2) ``tomorrow_inherits`` or steward-style hint → **kleiber**;
    (3) ``assess["recommended"]`` → A/B/C map;
    (4) **furtwangler**.
    """
    if dream:
        if _dream_implies_risky_worktree_seam(dream):
            return "toscanini"
        if _dream_implies_steward_or_tomorrow(dream):
            return "kleiber"
    if assess:
        rec = assess.get("recommended")
        if isinstance(rec, str) and rec.strip():
            letter = rec.strip().upper()[:1]
            if letter in ("A", "B", "C"):
                return d2_conductor_from_menu_recommendation(letter)
    return "furtwangler"


def d2_conductor_from_assess_load(assess: dict[str, Any]) -> str:
    """D2 from session load only (no dream)."""
    return d2_conductor_resolved(dream=None, assess=assess)
