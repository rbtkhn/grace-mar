"""
Illustrations for coffee **D1** vs **D2** conductor resolution.

**D2 does not *correct* D1; it *cross-cuts* it** — different question (system load /
dream vs “continue last emphasis”). Repeating **Kleiber** in the log reinforces one
**mode** of attention; **rotating** the slug **changes** the mode; **D2** can still
**point elsewhere** (e.g. **Bernstein** when ``recommended: C``).
"""

from __future__ import annotations

from datetime import datetime, timezone
from scripts.audit_cadence_rhythm import parse_events
from scripts.cadence_conductor_resolution import (
    conductor_for_d1_continuation,
    d2_conductor_from_assess_load,
    d2_conductor_from_menu_recommendation,
    d2_conductor_resolved,
    focus_for_d1_continuation,
    last_coffee_pick_conductor_event,
    normalize_conductor_slug,
)


def _ts(*, day: int = 1, hour: int = 12, minute: int = 0) -> datetime:
    return datetime(2026, 4, day, hour, minute, tzinfo=timezone.utc)


def _pick(
    dt: datetime,
    *,
    picked: str = "D1",
    conductor: str = "kleiber",
    focus: str | None = None,
    arc: str | None = None,
) -> dict:
    kv: dict[str, str] = {"picked": picked, "conductor": conductor}
    if focus is not None:
        kv["focus"] = focus
    if arc is not None:
        kv["arc"] = arc
    return {"dt": dt, "kind": "coffee_pick", "user": "grace-mar", "kv": kv, "line": ""}


def test_illustration_normalize_legacy_stack():
    assert normalize_conductor_slug("kleiber+toscanini") == "kleiber"


def test_illustration_three_kleiber_repetition():
    events = [
        _pick(_ts(day=1, hour=9), conductor="kleiber"),
        _pick(_ts(day=1, hour=10), conductor="kleiber"),
        _pick(_ts(day=1, hour=11), conductor="kleiber"),
    ]
    assert conductor_for_d1_continuation(events) == "kleiber"
    assert last_coffee_pick_conductor_event(events)["kv"]["conductor"] == "kleiber"


def test_illustration_rotation_tracks_newest():
    events = [
        _pick(_ts(day=1, hour=8), conductor="kleiber"),
        _pick(_ts(day=2, hour=9), conductor="karajan"),
        _pick(_ts(day=2, hour=10), conductor="karajan"),
    ]
    assert conductor_for_d1_continuation(events) == "karajan"


def test_illustration_d2_abc_map():
    assert d2_conductor_from_menu_recommendation("A") == "toscanini"
    assert d2_conductor_from_menu_recommendation("B") == "kleiber"
    assert d2_conductor_from_menu_recommendation("C") == "bernstein"
    assert d2_conductor_from_menu_recommendation("Z") == "furtwangler"


def test_illustration_orthogonal_d1_kleiber_d2_bernstein():
    """D1 continues Kleiber; D2 from load says C → Bernstein — not a 'fix' of D1."""
    events = [_pick(_ts(), conductor="kleiber")]
    assert conductor_for_d1_continuation(events) == "kleiber"
    d2 = d2_conductor_resolved(
        dream=None,
        assess={"recommended": "C", "line": "Session load: … (recommended: C)"},
    )
    assert d2 == "bernstein"


def test_illustration_focus_tracks_like_conductor():
    events = [
        _pick(_ts(day=1, hour=8), focus="ritter-april", conductor="kleiber"),
        _pick(_ts(day=2, hour=9), focus="mercouris", conductor="kleiber"),
    ]
    assert focus_for_d1_continuation(events) == "mercouris"


def test_illustration_dream_worktree_seam_overrides_assess_b():
    dream = {"worktreeAdvice": "merge conflict risk on feature seam"}
    assess = {"recommended": "B"}
    assert d2_conductor_resolved(dream=dream, assess=assess) == "toscanini"
    assert d2_conductor_from_assess_load(assess) == "kleiber"


def test_illustration_dream_tomorrow_inherits_kleiber():
    assert (
        d2_conductor_resolved(
            dream={"tomorrow_inherits": "Carry: daily brief"},
            assess={"recommended": "C"},
        )
        == "kleiber"
    )


def test_illustration_outcome_parsed_from_snippet(tmp_path):
    user = "grace-mar"
    log = tmp_path / "work-cadence-events.md"
    log.write_text(
        "# Cadence events\n\n_(Append below this line.)_\n"
        f"- **2026-04-20 12:00 UTC** — coffee_pick ({user}) ok=true picked=D1 conductor=kleiber\n"
        f"- **2026-04-20 12:30 UTC** — coffee_conductor_outcome ({user}) ok=true verdict=promote\n",
        encoding="utf-8",
    )
    events = parse_events(user, events_path=log)
    kinds = [e["kind"] for e in events]
    assert "coffee_conductor_outcome" in kinds
    outcomes = [e for e in events if e["kind"] == "coffee_conductor_outcome"]
    assert outcomes[-1]["kv"].get("verdict") == "promote"
