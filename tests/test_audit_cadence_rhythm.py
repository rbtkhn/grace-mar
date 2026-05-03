"""Tests for conductor-aware cadence auditing."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from audit_cadence_rhythm import compute_conductor_audit, format_conductor_audit


def _write_events(path: Path, body: str) -> Path:
    path.write_text(body, encoding="utf-8")
    return path


def test_conductor_audit_counts_explicit_and_inferred_paths(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=karajan
- **2026-05-01 10:05 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true verdict=watch conductor=karajan notebook_ref=docs/a.md falsify=stay-narrow
- **2026-05-01 11:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=E conductor=bernstein
- **2026-05-01 11:05 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true verdict=watch falsify=needs-public-stakes
- **2026-05-01 12:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=E
- **2026-05-01 12:30 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true verdict=watch
""",
    )
    summary = compute_conductor_audit(
        "grace-mar",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )
    assert summary["explicit_pick_count"] == 2
    assert summary["explicit_picks_by_conductor"]["karajan"] == 1
    assert summary["explicit_picks_by_conductor"]["bernstein"] == 1
    assert summary["explicit_outcomes_by_conductor"]["karajan"] == 1
    assert summary["inferred_outcomes_by_conductor"]["bernstein"] == 1
    assert summary["closure"]["unattributed_outcomes"] == 1
    assert summary["closure"]["total_closed"] == 2
    assert summary["closure"]["open_pick_count"] == 0


def test_conductor_audit_tracks_open_picks_and_legacy_partial(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** â€” coffee_pick (grace-mar) ok=true conductor=kleiber
- **2026-05-01 10:10 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=toscanini
""",
    )
    summary = compute_conductor_audit(
        "grace-mar",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )
    assert summary["legacy_partial_picks_by_conductor"]["kleiber"] == 1
    assert summary["explicit_pick_count"] == 1
    assert summary["closure"]["open_pick_count"] == 1
    assert summary["open_picks"][0]["conductor"] == "toscanini"


def test_conductor_audit_evidence_richness_and_format(tmp_path: Path) -> None:
    events = _write_events(
        tmp_path / "cadence.md",
        """# Cadence events

_(Append below this line.)_
- **2026-05-01 10:00 UTC** â€” coffee_pick (grace-mar) ok=true picked=conductor conductor=kleiber
- **2026-05-01 10:05 UTC** â€” coffee_conductor_outcome (grace-mar) ok=true verdict=watch conductor=kleiber action=trim falsify=one-test notebook_ref=docs/x.md
""",
    )
    summary = compute_conductor_audit(
        "grace-mar",
        days=7,
        events_path=events,
        now=datetime(2026, 5, 3, 0, 0, tzinfo=timezone.utc),
    )
    assert summary["evidence_richness"] == {
        "verdict": 1,
        "action": 1,
        "notebook_ref": 1,
        "falsify": 1,
    }
    text = format_conductor_audit(summary)
    assert "5-conductor audit" in text
    assert "kleiber: picks=1 explicit_outcomes=1 inferred_outcomes=0 legacy_partial=0" in text
