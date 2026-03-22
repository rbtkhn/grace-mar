"""Rate limits for high-risk reflection proposals."""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path


def _parse_iso_ts(raw: str) -> datetime | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        return None


def count_high_risk_recent(
    *,
    profile_dir: Path,
    days: int = 30,
    now: datetime | None = None,
) -> int:
    """Count reflection proposals with risk_level high in gate (pending + processed excerpts)."""
    gate = profile_dir / "recursion-gate.md"
    if not gate.exists():
        return 0
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=days)
    text = gate.read_text(encoding="utf-8", errors="replace")
    blocks = re.findall(r"```yaml\n(.*?)```", text, re.DOTALL)
    n = 0
    for block in blocks:
        if "signal_type: reflection-cycle" not in block and "reflection-cycle" not in block:
            continue
        if "risk_level: high" not in block.lower():
            continue
        ts_m = re.search(r"^timestamp:\s*(.+)$", block, re.MULTILINE)
        if not ts_m:
            continue
        dt = _parse_iso_ts(ts_m.group(1))
        if dt and dt >= cutoff:
            n += 1
    return n


def count_high_risk_in_index_month(
    index_path: Path,
    *,
    now: datetime | None = None,
) -> int:
    """Rough count from index.md table rows mentioning high risk in notes (v0.1 optional)."""
    if not index_path.exists():
        return 0
    # v0.1: pipeline-events is more reliable; return 0
    return 0


def pipeline_high_risk_events_last_month(
    events_path: Path,
    *,
    now: datetime | None = None,
) -> int:
    """Count reflection_cycle_run events with high_risk_proposals >= 1 in last 30 days."""
    if not events_path.exists():
        return 0
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=30)
    n = 0
    for line in events_path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("event") != "reflection_cycle_run":
            continue
        ts = _parse_iso_ts(str(ev.get("ts") or ""))
        if not ts or ts < cutoff:
            continue
        merge = {k: ev[k] for k in ev if k not in ("ts", "event", "candidate_id", "event_id", "fork_id", "envelope_version")}
        if merge.get("high_risk_proposals", 0) and int(merge.get("high_risk_proposals") or 0) > 0:
            n += 1
    return n


def allow_high_risk_proposal(
    *,
    profile_dir: Path,
    force: bool,
) -> tuple[bool, str]:
    if force:
        return True, "force"
    n = count_high_risk_recent(profile_dir=profile_dir, days=30)
    if n >= 1:
        return False, f"high-risk reflection cap: {n} in last 30 days (max 1)"
    return True, "ok"
