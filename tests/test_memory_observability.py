from __future__ import annotations

from datetime import datetime, timezone

from scripts import build_memory_observability as mbo


def test_parse_cadence_event_timestamps_for_user_only():
    text = "\n".join(
        [
            "- **2026-04-30 22:54 UTC** - coffee (grace-mar) ok=true mode=work-start",
            "- **2026-04-30 23:51 UTC** - coffee (demo) ok=true mode=minimal",
            "- **2026-05-01 00:10 UTC** - bridge (grace-mar) ok=true",
        ]
    )

    rows = mbo.parse_cadence_event_times(text, "grace-mar")

    assert [r.isoformat() for r in rows] == [
        "2026-04-30T22:54:00+00:00",
        "2026-05-01T00:10:00+00:00",
    ]


def test_classify_age_thresholds():
    assert mbo._classify_age(None, ok_h=24, watch_h=72) == "missing"
    assert mbo._classify_age(23.9, ok_h=24, watch_h=72) == "ok"
    assert mbo._classify_age(48, ok_h=24, watch_h=72) == "watch"
    assert mbo._classify_age(73, ok_h=24, watch_h=72) == "stale"


def test_render_markdown_has_exactly_one_recommended_next_action():
    now = datetime(2026, 5, 1, tzinfo=timezone.utc)
    report = {
        "generated_at": now.isoformat(),
        "user_id": "grace-mar",
        "overall_status": "watch",
        "recommended_next_action": "Run bridge at the next session boundary.",
        "deferred_v2": ["learning signals"],
        "surfaces": {
            "cadence": {
                "name": "cadence events",
                "path": "docs/skill-work/work-cadence/work-cadence-events.md",
                "status": "ok",
                "observed_at": now.isoformat(),
                "age_hours": 0,
                "detail": "1 event(s) found",
            },
            "last_dream": {
                "name": "last dream",
                "path": "users/grace-mar/last-dream.json",
                "status": "ok",
                "observed_at": now.isoformat(),
                "age_hours": 0,
                "detail": "ok=True",
            },
            "night_handoff": {
                "name": "night handoff",
                "path": "users/grace-mar/daily-handoff/night-handoff.json",
                "status": "missing",
                "observed_at": None,
                "age_hours": None,
                "detail": "missing file",
            },
            "bridge_state": {
                "name": "bridge state",
                "path": "users/grace-mar/daily-handoff/last-bridge-state.json",
                "status": "watch",
                "observed_at": None,
                "age_hours": None,
                "detail": "missing file",
            },
        },
    }

    md = mbo.render_markdown(report)

    assert md.count("Recommended next action:") == 1
    assert "## Continuity surface summary" in md
    assert "`missing`" in md


def test_observability_one_liner_is_compact():
    report = {
        "overall_status": "missing",
        "recommended_next_action": "Refresh the night handoff.",
    }

    line = mbo.format_observability_one_liner(report)

    assert line == "Memory observability: missing - Refresh the night handoff."


def test_json_report_contains_expected_top_level_keys():
    now = datetime(2026, 5, 1, tzinfo=timezone.utc)
    report = mbo.build_report("grace-mar", now=now)

    assert set(report) == {
        "generated_at",
        "user_id",
        "surfaces",
        "overall_status",
        "recommended_next_action",
        "deferred_v2",
    }
    assert set(report["surfaces"]) == {"cadence", "last_dream", "night_handoff", "bridge_state"}
