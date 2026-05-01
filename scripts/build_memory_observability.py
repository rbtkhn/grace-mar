#!/usr/bin/env python3
"""
Build a conservative WORK-layer memory observability dashboard.

This script reads existing cadence and handoff continuity surfaces and writes
derived reports under artifacts/memory/. It does not edit self-memory, Record,
gate, coffee, dream, or runtime behavior.

V1 thresholds:
- cadence: <=24h ok, <=72h watch, >72h stale, none missing
- last dream / night handoff: <=36h ok, <=96h watch, >96h stale, missing/unparseable missing
- bridge state: present ok, absent watch because bridge is event-driven
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_USER = "grace-mar"
DEFAULT_MD = REPO_ROOT / "artifacts" / "memory" / "memory-observability.md"
DEFAULT_JSON = REPO_ROOT / "artifacts" / "memory" / "memory-observability.json"

STATUS_ORDER = {"ok": 0, "watch": 1, "stale": 2, "missing": 3}
DEFERRED_V2 = [
    "learning signals",
    "hot/warm/cold context priority tiers",
    "access tracking",
    "bridge event JSONL",
    "coffee/dream integration",
]


def _parse_iso_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    if raw.endswith(" UTC"):
        raw = raw[:-4] + "+00:00"
    for fmt in ("%Y-%m-%d %H:%M%z", "%Y-%m-%d %H:%M:%S%z"):
        try:
            return datetime.strptime(raw, fmt).astimezone(timezone.utc)
        except ValueError:
            pass
    try:
        dt = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _age_hours(dt: datetime | None, now: datetime) -> float | None:
    if dt is None:
        return None
    return max(0.0, (now - dt).total_seconds() / 3600.0)


def _classify_age(age_hours: float | None, *, ok_h: float, watch_h: float) -> str:
    if age_hours is None:
        return "missing"
    if age_hours <= ok_h:
        return "ok"
    if age_hours <= watch_h:
        return "watch"
    return "stale"


def parse_cadence_event_times(text: str, user_id: str = DEFAULT_USER) -> list[datetime]:
    """Parse cadence timestamps for a user from work-cadence-events.md text."""
    rows: list[datetime] = []
    pat = re.compile(r"^- \*\*(?P<ts>[^*]+)\*\* .+?\((?P<user>[^)]+)\)", re.MULTILINE)
    for m in pat.finditer(text):
        if m.group("user") != user_id:
            continue
        dt = _parse_iso_datetime(m.group("ts"))
        if dt is not None:
            rows.append(dt)
    return rows


def _read_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.is_file():
        return None, "missing file"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"unparseable: {exc}"
    if not isinstance(data, dict):
        return None, "unparseable: top-level JSON is not an object"
    return data, None


def _surface(
    *,
    name: str,
    path: Path,
    status: str,
    detail: str,
    observed_at: datetime | None = None,
    age_hours: float | None = None,
) -> dict[str, Any]:
    rel_path = path.relative_to(REPO_ROOT) if path.is_absolute() else path
    return {
        "name": name,
        "path": rel_path.as_posix(),
        "status": status,
        "observed_at": observed_at.isoformat() if observed_at else None,
        "age_hours": round(age_hours, 2) if age_hours is not None else None,
        "detail": detail,
    }


def build_report(user_id: str = DEFAULT_USER, *, now: datetime | None = None) -> dict[str, Any]:
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)

    cadence_path = REPO_ROOT / "docs" / "skill-work" / "work-cadence" / "work-cadence-events.md"
    cadence_text = cadence_path.read_text(encoding="utf-8") if cadence_path.is_file() else ""
    cadence_times = parse_cadence_event_times(cadence_text, user_id)
    last_cadence = max(cadence_times) if cadence_times else None
    cadence_age = _age_hours(last_cadence, now)
    cadence_status = _classify_age(cadence_age, ok_h=24, watch_h=72)

    last_dream_path = REPO_ROOT / "users" / user_id / "last-dream.json"
    last_dream, dream_err = _read_json(last_dream_path)
    last_dream_dt = _parse_iso_datetime(str(last_dream.get("generated_at"))) if last_dream else None
    dream_age = _age_hours(last_dream_dt, now)
    dream_status = "missing" if dream_err else _classify_age(dream_age, ok_h=36, watch_h=96)

    handoff_dir = REPO_ROOT / "users" / user_id / "daily-handoff"
    night_path = handoff_dir / "night-handoff.json"
    night_handoff, night_err = _read_json(night_path)
    night_dt = None
    if night_handoff:
        night_dt = _parse_iso_datetime(
            str(
                night_handoff.get("generated_at")
                or night_handoff.get("runIso")
                or night_handoff.get("created_at")
            )
        )
        if night_dt is None:
            try:
                night_dt = datetime.fromtimestamp(night_path.stat().st_mtime, timezone.utc)
            except OSError:
                night_dt = None
    night_age = _age_hours(night_dt, now)
    night_status = "missing" if night_err else _classify_age(night_age, ok_h=36, watch_h=96)

    bridge_path = handoff_dir / "last-bridge-state.json"
    bridge_state, bridge_err = _read_json(bridge_path)
    bridge_dt = None
    if bridge_state:
        bridge_dt = _parse_iso_datetime(str(bridge_state.get("runIso") or bridge_state.get("generated_at")))
        if bridge_dt is None:
            try:
                bridge_dt = datetime.fromtimestamp(bridge_path.stat().st_mtime, timezone.utc)
            except OSError:
                bridge_dt = None
    bridge_age = _age_hours(bridge_dt, now)
    bridge_status = "watch" if bridge_err else "ok"

    surfaces = {
        "cadence": _surface(
            name="cadence events",
            path=cadence_path,
            status=cadence_status,
            observed_at=last_cadence,
            age_hours=cadence_age,
            detail=f"{len(cadence_times)} event(s) found for {user_id}",
        ),
        "last_dream": _surface(
            name="last dream",
            path=last_dream_path,
            status=dream_status,
            observed_at=last_dream_dt,
            age_hours=dream_age,
            detail=dream_err or f"ok={last_dream.get('ok') if last_dream else None}",
        ),
        "night_handoff": _surface(
            name="night handoff",
            path=night_path,
            status=night_status,
            observed_at=night_dt,
            age_hours=night_age,
            detail=night_err or "night handoff present",
        ),
        "bridge_state": _surface(
            name="bridge state",
            path=bridge_path,
            status=bridge_status,
            observed_at=bridge_dt,
            age_hours=bridge_age,
            detail=bridge_err or "bridge state present",
        ),
    }

    overall = _overall_status(surfaces)
    recommended = _recommended_next_action(surfaces)
    return {
        "generated_at": now.isoformat(),
        "user_id": user_id,
        "surfaces": surfaces,
        "overall_status": overall,
        "recommended_next_action": recommended,
        "deferred_v2": DEFERRED_V2,
    }


def _overall_status(surfaces: dict[str, dict[str, Any]]) -> str:
    keys = ("cadence", "last_dream", "night_handoff")
    worst = max((surfaces[k]["status"] for k in keys), key=lambda s: STATUS_ORDER[s])
    bridge_status = surfaces["bridge_state"]["status"]
    if STATUS_ORDER[bridge_status] > STATUS_ORDER[worst] and bridge_status == "watch":
        return "watch" if worst == "ok" else worst
    return worst


def _recommended_next_action(surfaces: dict[str, dict[str, Any]]) -> str:
    if surfaces["cadence"]["status"] in {"stale", "missing"}:
        return "Run coffee or bridge to refresh cadence continuity before relying on handoff state."
    if surfaces["last_dream"]["status"] in {"stale", "missing"}:
        return "Run dream when closing the day so tomorrow's coffee inherits a fresh handoff."
    if surfaces["night_handoff"]["status"] in {"stale", "missing"}:
        return "Refresh the night handoff with a successful dream pass before treating it as current."
    if surfaces["bridge_state"]["status"] == "watch":
        return "Run bridge at the next session boundary if a transfer prompt or repo seal is needed."
    return "No urgent continuity action; keep using coffee for orientation and bridge at session boundaries."


def render_markdown(report: dict[str, Any]) -> str:
    surfaces = report["surfaces"]
    lines = [
        "# Memory observability\n\n",
        "**Status:** derived WORK-layer observability. Not Record truth and not self-memory.\n\n",
        f"**Generated:** {report['generated_at']}\n",
        f"**User:** `{report['user_id']}`\n",
        f"**Overall status:** `{report['overall_status']}`\n\n",
        "## Continuity surface summary\n\n",
        "| Surface | Status | Observed | Age (h) | Detail |\n",
        "|---------|--------|----------|---------|--------|\n",
    ]
    for key in ("cadence", "last_dream", "night_handoff", "bridge_state"):
        row = surfaces[key]
        observed = row["observed_at"] or "-"
        age = row["age_hours"] if row["age_hours"] is not None else "-"
        lines.append(f"| {row['name']} | `{row['status']}` | {observed} | {age} | {row['detail']} |\n")

    lines.extend(
        [
            "\n## Missing/stale inputs\n\n",
        ]
    )
    problem_rows = [r for r in surfaces.values() if r["status"] in {"stale", "missing"}]
    if not problem_rows:
        lines.append("- None at v1 thresholds.\n")
    else:
        for row in problem_rows:
            lines.append(f"- `{row['status']}`: {row['name']} at `{row['path']}` - {row['detail']}\n")

    lines.extend(
        [
            "\n## Deferred v2\n\n",
        ]
    )
    for item in report["deferred_v2"]:
        lines.append(f"- {item}\n")
    lines.append(f"\nRecommended next action: {report['recommended_next_action']}\n")
    return "".join(lines)


def format_observability_one_liner(report: dict[str, Any]) -> str:
    """Return a compact operator line for non-ok continuity health."""
    status = str(report.get("overall_status") or "missing")
    recommended = str(report.get("recommended_next_action") or "Review memory observability report.")
    return f"Memory observability: {status} - {recommended}"


def write_report(report: dict[str, Any], *, md_output: Path, json_output: Path) -> None:
    md_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    md_output.write_text(render_markdown(report), encoding="utf-8")
    json_output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Build derived memory observability dashboard.")
    ap.add_argument("-u", "--user", default=DEFAULT_USER)
    ap.add_argument("--md-output", default=str(DEFAULT_MD))
    ap.add_argument("--json-output", default=str(DEFAULT_JSON))
    ap.add_argument(
        "--quiet-ok",
        action="store_true",
        help="Print only the compact one-line status, and stay silent when overall_status is ok.",
    )
    args = ap.parse_args()

    report = build_report(args.user)
    write_report(report, md_output=Path(args.md_output), json_output=Path(args.json_output))
    if args.quiet_ok:
        if report["overall_status"] != "ok":
            print(format_observability_one_liner(report))
        return 0
    print(f"Wrote {args.md_output}")
    print(f"Wrote {args.json_output}")
    print(f"Overall status: {report['overall_status']}")
    print(f"Recommended next action: {report['recommended_next_action']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
