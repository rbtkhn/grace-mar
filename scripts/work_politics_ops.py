#!/usr/bin/env python3
"""
Structured operator state for work-politics (CLI: wap).

Builds a dashboard-friendly snapshot from WAP docs and the canonical gate.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

try:
    from recursion_gate_review import parse_review_candidates
    from recursion_gate_territory import TERRITORY_WAP
except ImportError:
    from scripts.recursion_gate_review import parse_review_candidates
    from scripts.recursion_gate_territory import TERRITORY_WAP

REPO_ROOT = Path(__file__).resolve().parent.parent
WAP_DIR = REPO_ROOT / "docs" / "skill-work" / "work-politics"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _file_age_days(path: Path) -> int | None:
    if not path.exists():
        return None
    return max(0, int((datetime.now(timezone.utc).timestamp() - path.stat().st_mtime) // 86400))


def _parse_markdown_table(content: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    headers: list[str] | None = None
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or line.count("|") < 2:
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not headers:
            headers = cells
            continue
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if len(cells) != len(headers):
            headers = cells
            continue
        rows.append({headers[idx]: cells[idx] for idx in range(len(headers))})
    return rows


def _parse_currency_amount(amount: str) -> float | None:
    match = re.search(r"\$([\d,]+(?:\.\d+)?)", amount or "")
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def _parse_date(text: str) -> datetime | None:
    cleaned = re.sub(r"[*_`]", "", (text or "")).strip()
    cleaned = cleaned.replace("–", "-")
    if " - " in cleaned:
        cleaned = cleaned.split(" - ", 1)[0].strip()
    if " — " in cleaned:
        cleaned = cleaned.split(" — ", 1)[0].strip()
    if "," in cleaned and re.search(r",\s*\d{1,2}:\d{2}\s*[AP]M$", cleaned):
        cleaned = re.sub(r",\s*\d{1,2}:\d{2}\s*[AP]M$", "", cleaned).strip()
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(cleaned, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def _days_until(date_text: str) -> int | None:
    dt = _parse_date(date_text)
    if not dt:
        return None
    return int((dt - datetime.now(timezone.utc)).days)


def _extract_primary_date() -> dict[str, object]:
    calendar_path = WAP_DIR / "calendar-2026.md"
    content = _read(calendar_path)
    match = re.search(r"\*\*Primary election day:\*\* .*?\*\*(\w+ \d{1,2}, \d{4})\*\*", content)
    label = match.group(1) if match else "May 19, 2026"
    return {
        "label": label,
        "days_until": _days_until(label),
    }


def _calendar_rows(limit: int = 4) -> list[dict[str, object]]:
    rows = _parse_markdown_table(_read(WAP_DIR / "calendar-2026.md"))
    upcoming: list[dict[str, object]] = []
    for row in rows:
        date_text = row.get("Date", "")
        days_until = _days_until(date_text)
        if days_until is None:
            continue
        upcoming.append(
            {
                "date": date_text,
                "event": row.get("Event", ""),
                "decision": row.get("Decision / action", ""),
                "days_until": days_until,
            }
        )
    upcoming.sort(key=lambda row: row["days_until"])
    return [row for row in upcoming if row["days_until"] >= -1][:limit]


def _revenue_summary() -> dict[str, object]:
    rows = _parse_markdown_table(_read(WAP_DIR / "revenue-log.md"))
    total_revenue = 0.0
    revenue_events = 0
    btc_commitments = 0
    for row in rows:
        amount = row.get("Amount", "")
        if "BTC" in amount:
            btc_commitments += 1
        dollar_amount = _parse_currency_amount(amount)
        if dollar_amount is None:
            continue
        if row.get("Type"):
            total_revenue += dollar_amount
            revenue_events += 1
    return {
        "total_revenue_usd": total_revenue,
        "revenue_events": revenue_events,
        "btc_commitments": btc_commitments,
    }


def _brief_sources() -> list[dict[str, str]]:
    return _parse_markdown_table(_read(WAP_DIR / "brief-source-registry.md"))


def _content_queue() -> list[dict[str, str]]:
    return _parse_markdown_table(_read(WAP_DIR / "content-queue.md"))


def _brief_readiness() -> dict[str, object]:
    rows = _brief_sources()
    status_counts: dict[str, int] = {}
    needs_refresh: list[str] = []
    for row in rows:
        status = row.get("Status", "").strip()
        status_counts[status] = status_counts.get(status, 0) + 1
        if status == "needs_refresh":
            needs_refresh.append(row.get("Source", ""))
    return {
        "sources": rows,
        "status_counts": status_counts,
        "needs_refresh": needs_refresh,
    }


def _content_summary() -> dict[str, object]:
    rows = _content_queue()
    status_counts: dict[str, int] = {}
    next_items: list[dict[str, str]] = []
    for row in rows:
        status = row.get("Status", "").strip()
        status_counts[status] = status_counts.get(status, 0) + 1
        if status in {"draft", "review", "idea"}:
            next_items.append(row)
    return {
        "items": rows,
        "status_counts": status_counts,
        "next_items": next_items[:4],
    }


def _doc_statuses() -> list[dict[str, object]]:
    files = [
        ("Principal profile", WAP_DIR / "principal-profile.md"),
        ("Opposition brief", WAP_DIR / "opposition-brief.md"),
        ("Calendar", WAP_DIR / "calendar-2026.md"),
        ("Revenue log", WAP_DIR / "revenue-log.md"),
        ("Brief source registry", WAP_DIR / "brief-source-registry.md"),
        ("Content queue", WAP_DIR / "content-queue.md"),
    ]
    out: list[dict[str, object]] = []
    for label, path in files:
        content = _read(path)
        out.append(
            {
                "label": label,
                "path": str(path.relative_to(REPO_ROOT)),
                "age_days": _file_age_days(path),
                "has_placeholders": "*(Add" in content or "[DATE RANGE]" in content,
            }
        )
    return out


def _wap_gate_items(user_id: str) -> list[dict]:
    rows = parse_review_candidates(user_id)
    return [row for row in rows if row.get("territory") == TERRITORY_WAP]


def _territory_blockers(user_id: str) -> list[dict[str, str]]:
    blockers: list[dict[str, str]] = []
    for doc in _doc_statuses():
        if doc["label"] == "Opposition brief" and doc["has_placeholders"]:
            blockers.append(
                {
                    "kind": "research_gap",
                    "title": "Opposition brief still has placeholder sections",
                    "action": "Refresh Gallrein, Trump/MAGA, and spending lines before relying on the brief heavily.",
                }
            )
        if doc["age_days"] is not None and doc["age_days"] >= 14 and doc["label"] in {"Principal profile", "Revenue log"}:
            blockers.append(
                {
                    "kind": "freshness",
                    "title": f"{doc['label']} may be stale",
                    "action": f"Review `{doc['path']}` and confirm it still matches the live campaign context.",
                }
            )
    wap_items = _wap_gate_items(user_id)
    if not wap_items:
        blockers.append(
            {
                "kind": "gate_rhythm",
                "title": "No live WAP candidates in RECURSION-GATE",
                "action": "Confirm this is a doc-only week or stage one WAP milestone so audit continuity stays current.",
            }
        )
    if _brief_readiness()["needs_refresh"]:
        blockers.append(
            {
                "kind": "brief_readiness",
                "title": "Weekly brief sources are not fully ready",
                "action": "Refresh items marked `needs_refresh` in `brief-source-registry.md` before generating the next brief.",
            }
        )
    content_counts = _content_summary()["status_counts"]
    if content_counts.get("review", 0) == 0:
        blockers.append(
            {
                "kind": "content_ops",
                "title": "No content currently in review",
                "action": "Promote one queued idea or draft so Jonathan has something concrete to review/post next.",
            }
        )
    return blockers


def _next_actions(user_id: str) -> list[str]:
    actions: list[str] = []
    upcoming = _calendar_rows()
    if upcoming:
        first = upcoming[0]
        actions.append(f"Prepare for {first['event']} on {first['date']}.")
    for blocker in _territory_blockers(user_id)[:3]:
        actions.append(blocker["action"])
    return actions[:4]


def get_wap_snapshot(user_id: str = "grace-mar") -> dict[str, object]:
    primary = _extract_primary_date()
    brief = _brief_readiness()
    content = _content_summary()
    pending_items = _wap_gate_items(user_id)
    return {
        "territory": TERRITORY_WAP,
        "principal": {
            "name": "Thomas Massie",
            "district": "KY-4",
            "phase": "Primary",
        },
        "campaign_status": {
            "primary_date": primary["label"],
            "days_until_primary": primary["days_until"],
            "upcoming_dates": _calendar_rows(),
        },
        "doc_statuses": _doc_statuses(),
        "revenue": _revenue_summary(),
        "brief_readiness": brief,
        "content_queue": content,
        "gate": {
            "pending_items": pending_items,
            "pending_count": len(pending_items),
        },
        "territory_blockers": _territory_blockers(user_id),
        "next_actions": _next_actions(user_id),
        "workspace_path": str((WAP_DIR / "workspace.md").relative_to(REPO_ROOT)),
    }


__all__ = ["get_wap_snapshot"]
