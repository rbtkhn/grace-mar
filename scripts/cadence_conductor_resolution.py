#!/usr/bin/env python3
"""
Resolve coffee-conductor helpers for the **single D — Conductor** menu line.

The Step 2 menu uses one **D**; the same resolution applies when the operator
invokes **D** / a name fragment **without** a full **coffee** session (see
``.cursor/skills/coffee/SKILL.md`` § *Conductor only*). The five masters are
disambiguated by the **Conductor MCQ** letters **A.–E.**, by ``conductor=`` (cadence log), by **last pick** (bare **D**), or by **name prefix** after **D** in chat. Use ``format_conductor_mcq_block`` / ``build_conductor_mcq_for_user`` for the five selectable rows + continuity.

Legacy ``D1``..``D5`` in old logs are still recognized.

Pure functions over event dicts shaped like ``audit_cadence_rhythm.parse_events()``
output: ``{"dt", "kind", "user", "line", "kv"}``.

This module still helps with two advisory questions:

1. Which conductor was picked most recently on disk? (continuity)
2. Which conductor does the system recommend from dream + load signals? (recommendation)
"""

from __future__ import annotations

import unicodedata
from typing import Any

MENU_PICK_TO_CONDUCTOR = {
    "D1": "toscanini",
    "D2": "furtwangler",
    "D3": "bernstein",
    "D4": "karajan",
    "D5": "kleiber",
}
# Display order in coffee menu text (Toscanini / Furtwängler / Karajan / Kleiber / Bernstein)
_CONDUCTOR_MENU: list[tuple[str, str]] = [
    ("Toscanini", "toscanini"),
    ("Furtwängler", "furtwangler"),
    ("Karajan", "karajan"),
    ("Kleiber", "kleiber"),
    ("Bernstein", "bernstein"),
]
KNOWN_CONDUCTOR_SLUGS = frozenset(s for _n, s in _CONDUCTOR_MENU)

# Conductor MCQ: one row of **A**–**E** (not main `coffee` menu letters). Fixed order =
# menu order (Toscanini … Bernstein).
_CONDUCTOR_MCQ_ROWS: tuple[tuple[str, str, str, str], ...] = (
    ("A", "toscanini", "Toscanini", "Precision — verify claims and seams; cut flourish that outruns the material."),
    ("B", "furtwangler", "Furtwängler", "Flow — hold tension open; listen for the line under the line before closing."),
    ("C", "karajan", "Karajan", "Elegance — long-arc balance and proportion; remove what blurs the whole."),
    ("D", "kleiber", "Kleiber", "Selectivity — one or two deep hotspots; refuse the rest explicitly this round."),
    ("E", "bernstein", "Bernstein", "Vitality — stakes, pulse, and language that can carry heat live."),
)
CONDUCTOR_SUBMENU_LETTER_TO_SLUG: dict[str, str] = {
    letter: slug for letter, slug, _name, _attr in _CONDUCTOR_MCQ_ROWS
}

# Legacy: D1..D5 → different letters; new logs use picked=D with conductor=.
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
    """Map legacy ``D1``..``D5`` to slug. Bare ``D`` has no slug without ``conductor=``."""
    p = str(pick).strip().upper()
    if p == "D":
        return None
    return MENU_PICK_TO_CONDUCTOR.get(p)


def _strip_accents(s: str) -> str:
    return "".join(
        c
        for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def conductor_submenu_letter_to_slug(letter: str) -> str | None:
    """Map **Conductor MCQ** letter **A**–**E** to slug. Not main-menu **A**–**E**."""
    k = str(letter).strip().upper()[:1]
    return CONDUCTOR_SUBMENU_LETTER_TO_SLUG.get(k)


def _display_name_for_slug(slug: str) -> str:
    for _L, s, display, _attr in _CONDUCTOR_MCQ_ROWS:
        if s == normalize_conductor_slug(slug):
            return display
    return slug


def _continuity_kicker(
    slug: str,
    *,
    last_slug: str | None,
    recommended_slug: str | None,
) -> str:
    """One short clause for the MCQ line (continuity + advisory)."""
    s = normalize_conductor_slug(slug)
    last = normalize_conductor_slug(last_slug) if last_slug else None
    rec = normalize_conductor_slug(recommended_slug) if recommended_slug else None
    if last and last == s:
        return "Continuity: same card as your last `coffee_pick`."
    if last and last != s and rec == s:
        return (
            f"Continuity: pivot from **{_display_name_for_slug(last)}**; "
            "advisory (dream/load) also leans here today."
        )
    if last and last != s:
        return f"Continuity: pivot from last **{_display_name_for_slug(last)}** toward this mode."
    if rec == s:
        return "Advisory: dream / session-load tips this card today (no prior pick match)."
    return "Open entry: no prior conductor in this chain."


def format_conductor_mcq_block(
    *,
    last_slug: str | None = None,
    focus_text: str | None = None,
    recommended_slug: str | None = None,
) -> str:
    """Return the 5-line **Conductor MCQ** (markdown) with attribute + continuity kickers."""
    lines: list[str] = [
        "**Conductor MCQ** — letters **A**–**E** name the five masters (*not* the main Build/Steward/Strategy line). "
        "Reply with one letter, a name prefix (`klei`, `tos`, …), or bare main-menu **D** to continue last.",
    ]
    if focus_text and str(focus_text).strip():
        lines.append(
            f"*Last cadence `focus` / `arc`:* **{str(focus_text).strip()}**"
        )
    for letter, slug, display, attr in _CONDUCTOR_MCQ_ROWS:
        kick = _continuity_kicker(
            slug,
            last_slug=last_slug,
            recommended_slug=recommended_slug,
        )
        lines.append(f"**{letter}.** **{display}** — {attr} *({kick})*")
    return "\n".join(lines)


def build_conductor_mcq_for_user(user_id: str) -> str:
    """Load cadence (and optional dream + session load) and format the Conductor MCQ."""
    import json
    from pathlib import Path

    try:
        from audit_cadence_rhythm import parse_events
    except ImportError:
        from scripts.audit_cadence_rhythm import parse_events

    events = parse_events(user_id)
    last = last_logged_conductor(events)
    focus = focus_for_last_conductor(events)

    dream: dict[str, Any] | None = None
    try:
        p = Path(__file__).resolve().parent.parent / "users" / user_id / "last-dream.json"
        if p.is_file():
            dream = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, TypeError):
        dream = None

    try:
        from assess_session_load import assess_load
    except ImportError:
        from scripts.assess_session_load import assess_load

    assess = assess_load(user_id)
    rec_slug = system_recommended_conductor(dream=dream, assess=assess)

    return format_conductor_mcq_block(
        last_slug=last,
        focus_text=focus,
        recommended_slug=rec_slug,
    )


def resolve_d_conductor(
    name_fragment: str | None,
    *,
    last_conductor_slug: str | None = None,
) -> tuple[str | None, str | None]:
    """Resolve **D** in operator chat: empty fragment → last logged conductor; else prefix match on slug or name.

    A **single** character **A**–**E** is the Conductor MCQ row (not main-menu letters).
    Returns ``(slug, err)`` with ``err`` in ``(None, "no_prior", "no_match", "ambiguous")``.
    """
    frag = (name_fragment or "").strip()
    if not frag:
        if last_conductor_slug and str(last_conductor_slug).strip():
            return normalize_conductor_slug(str(last_conductor_slug)), None
        return None, "no_prior"
    if len(frag) == 1 and frag.upper() in CONDUCTOR_SUBMENU_LETTER_TO_SLUG:
        return CONDUCTOR_SUBMENU_LETTER_TO_SLUG[frag.upper()], None
    frag_l = frag.lower()
    fstrip = _strip_accents(frag).lower()
    matches: list[str] = []
    for display, slug in _CONDUCTOR_MENU:
        s = normalize_conductor_slug(slug)
        dnorm = _strip_accents(display).lower()
        dcompact = dnorm.replace(" ", "")
        if (
            s.startswith(frag_l)
            or s.startswith(frag_l.replace("w", "v"))
            or dcompact.startswith(frag_l)
            or dnorm.startswith(frag_l)
            or (fstrip and s.startswith(fstrip))
        ):
            if s not in matches:
                matches.append(s)
    if len(matches) == 1:
        return matches[0], None
    if not matches:
        return None, "no_match"
    return None, "ambiguous"


def menu_pick_for_conductor_slug(slug: str) -> str | None:
    """Return ``D`` for any known conductor slug (new log convention); else ``None``."""
    s = normalize_conductor_slug(slug)
    if s in KNOWN_CONDUCTOR_SLUGS:
        return "D"
    return None


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
