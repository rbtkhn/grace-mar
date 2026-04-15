#!/usr/bin/env python3
"""
Capability shift detector — automated rolling-disruption sensor.

Fetches public changelogs from two source categories and diffs against
documented capability assumptions to flag when a release may have
compressed a gap the system was built on.

Source categories:
  model     — LLM provider changelogs (Anthropic, OpenAI, xAI, Google, DeepSeek, Qwen)
  ecosystem — frameworks and adjacent systems (Open Brain, AutoGen, CrewAI, LangChain)

Exposes detect_shifts() and format_alert_one_liner() for import by
harness_warmup.py.

Read-only operator tooling — no file writes (except optional cache).

Usage:
  python scripts/detect_capability_shift.py -u grace-mar
  python scripts/detect_capability_shift.py -u grace-mar --category model
  python scripts/detect_capability_shift.py -u grace-mar --category ecosystem
  python scripts/detect_capability_shift.py -u grace-mar --json
  python scripts/detect_capability_shift.py -u grace-mar --offline
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ASSUMPTIONS_PATH = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "capability-assumptions.yaml"
CACHE_PATH = REPO_ROOT / "docs" / "skill-work" / "work-dev" / ".capability-shift-cache.json"
LAST_CHECK_PATH = REPO_ROOT / "docs" / "skill-work" / "work-dev" / ".capability-shift-last-check"

_FETCH_TIMEOUT = 15
_USER_AGENT = "grace-mar-capability-shift-detector/1.0"


# ---------------------------------------------------------------------------
# YAML-lite parser (avoids PyYAML dependency)
# ---------------------------------------------------------------------------

def _parse_assumptions_yaml(text: str) -> dict:
    """Minimal parser for capability-assumptions.yaml structure."""
    sources: list[dict] = []
    assumptions: list[dict] = []

    current_section: str | None = None
    current_item: dict | None = None
    current_list_key: str | None = None

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("#") or not stripped:
            continue

        if stripped == "sources:":
            current_section = "sources"
            current_item = None
            current_list_key = None
            continue
        if stripped == "assumptions:":
            if current_section == "sources" and current_item:
                sources.append(current_item)
            current_section = "assumptions"
            current_item = None
            current_list_key = None
            continue

        if current_section == "sources":
            if stripped.startswith("- name:"):
                if current_item is not None:
                    sources.append(current_item)
                current_item = {"name": _yaml_val(stripped, "name")}
                current_list_key = None
            elif current_item is not None:
                for key in ("url", "parser", "enabled", "category"):
                    if stripped.startswith(f"{key}:"):
                        val = _yaml_val(stripped, key)
                        if key == "enabled":
                            current_item[key] = val.lower() in ("true", "yes", "1")
                        else:
                            current_item[key] = val
            continue

        if current_section == "assumptions":
            if stripped.startswith("- id:"):
                if current_item is not None:
                    assumptions.append(current_item)
                current_item = {"id": _yaml_val(stripped, "id"), "keywords": [], "affects": [], "gap_ids": []}
                current_list_key = None
            elif current_item is not None:
                for key in ("assumption", "notes", "last_validated"):
                    if stripped.startswith(f"{key}:"):
                        current_item[key] = _yaml_val(stripped, key)
                        current_list_key = None

                if stripped.startswith("keywords:"):
                    current_item["keywords"] = _yaml_inline_list(stripped, "keywords")
                    current_list_key = "keywords" if not current_item["keywords"] else None
                elif stripped.startswith("affects:"):
                    current_item["affects"] = _yaml_inline_list(stripped, "affects")
                    current_list_key = "affects" if not current_item["affects"] else None
                elif stripped.startswith("gap_ids:"):
                    current_item["gap_ids"] = _yaml_inline_list(stripped, "gap_ids")
                    current_list_key = "gap_ids" if not current_item["gap_ids"] else None
                elif stripped.startswith("- ") and current_list_key:
                    current_item[current_list_key].append(stripped[2:].strip().strip('"').strip("'"))
            continue

    if current_section == "sources" and current_item:
        sources.append(current_item)
    if current_section == "assumptions" and current_item:
        assumptions.append(current_item)

    return {"sources": sources, "assumptions": assumptions}


def _yaml_val(line: str, key: str) -> str:
    after = line.split(f"{key}:", 1)[1].strip()
    return after.strip('"').strip("'")


def _yaml_inline_list(line: str, key: str) -> list[str]:
    after = line.split(f"{key}:", 1)[1].strip()
    if after.startswith("["):
        inner = after.strip("[]")
        if not inner.strip():
            return []
        return [item.strip().strip('"').strip("'") for item in inner.split(",") if item.strip()]
    return []


# ---------------------------------------------------------------------------
# Changelog fetching
# ---------------------------------------------------------------------------

def _strip_html(text: str) -> str:
    """Remove HTML tags and decode entities — rough but sufficient for keyword matching."""
    text = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def fetch_changelog(source: dict) -> dict:
    """Fetch a single provider changelog. Returns {name, url, text, error, fetched_at}."""
    result: dict = {
        "name": source["name"],
        "url": source.get("url", ""),
        "text": "",
        "error": None,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }
    if not source.get("enabled", True):
        result["error"] = "disabled"
        return result

    url = source.get("url", "")
    if not url:
        result["error"] = "no url"
        return result

    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=_FETCH_TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, TimeoutError) as exc:
        result["error"] = str(exc)[:200]
        return result

    if source.get("parser") == "html":
        result["text"] = _strip_html(raw)
    else:
        result["text"] = raw[:50000]

    return result


def fetch_all_changelogs(sources: list[dict]) -> list[dict]:
    results = []
    for src in sources:
        results.append(fetch_changelog(src))
    return results


# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------

def save_cache(changelogs: list[dict], path: Path = CACHE_PATH) -> None:
    path.write_text(json.dumps(changelogs, indent=2, default=str), encoding="utf-8")


def load_cache(path: Path = CACHE_PATH) -> list[dict]:
    if not path.is_file():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []


def save_last_check(path: Path = LAST_CHECK_PATH) -> None:
    path.write_text(datetime.now(timezone.utc).isoformat() + "\n", encoding="utf-8")


def load_last_check(path: Path = LAST_CHECK_PATH) -> datetime | None:
    if not path.is_file():
        return None
    try:
        return datetime.fromisoformat(path.read_text(encoding="utf-8").strip())
    except (ValueError, OSError):
        return None


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------

def match_shifts(
    changelogs: list[dict],
    assumptions: list[dict],
    threshold: float = 0.3,
) -> list[dict]:
    """Match changelog text against assumption keywords.

    Returns a list of alerts sorted by relevance (highest match score first).
    threshold: minimum fraction of keywords that must match (0.0–1.0).
    """
    alerts: list[dict] = []

    for assumption in assumptions:
        keywords = assumption.get("keywords", [])
        if not keywords:
            continue

        for changelog in changelogs:
            text = changelog.get("text", "").lower()
            if not text or changelog.get("error"):
                continue

            hits = [kw for kw in keywords if kw.lower() in text]
            score = len(hits) / len(keywords) if keywords else 0.0

            if score >= threshold:
                is_variant = assumption["id"] in _VARIANT_ASSUMPTION_IDS
                alerts.append({
                    "assumption_id": assumption["id"],
                    "assumption": assumption.get("assumption", ""),
                    "provider": changelog["name"],
                    "matched_keywords": hits,
                    "score": round(score, 2),
                    "total_keywords": len(keywords),
                    "affects": assumption.get("affects", []),
                    "gap_ids": assumption.get("gap_ids", []),
                    "notes": assumption.get("notes", ""),
                    "action": _recommend_action(score, is_variant=is_variant),
                    "alert_class": "variant" if is_variant else "base",
                })

    alerts.sort(key=lambda a: a["score"], reverse=True)
    return alerts


_VARIANT_ASSUMPTION_IDS = frozenset({"ASSUME-015"})


def _recommend_action(score: float, *, is_variant: bool = False) -> str:
    if is_variant:
        return "monitor" if score >= 0.3 else "no action"
    if score >= 0.7:
        return "review"
    if score >= 0.5:
        return "monitor"
    return "no action"


# ---------------------------------------------------------------------------
# Public API (importable)
# ---------------------------------------------------------------------------

def _filter_sources(sources: list[dict], category: str) -> list[dict]:
    """Filter sources by category. 'all' returns everything."""
    if category == "all":
        return sources
    return [s for s in sources if s.get("category", "model") == category]


def detect_shifts(
    user_id: str = "grace-mar",
    *,
    offline: bool = False,
    threshold: float = 0.3,
    category: str = "all",
    assumptions_path: Path = ASSUMPTIONS_PATH,
    cache_path: Path = CACHE_PATH,
) -> dict:
    """Run capability shift detection. Returns a summary dict.

    category: 'model' | 'ecosystem' | 'all' (default 'all').
    Importable by harness_warmup.py and other scripts.
    """
    if not assumptions_path.is_file():
        return {"user_id": user_id, "alerts": [], "error": "assumptions file not found"}

    config = _parse_assumptions_yaml(assumptions_path.read_text(encoding="utf-8"))
    all_sources = config.get("sources", [])
    sources = _filter_sources(all_sources, category)
    assumptions = config.get("assumptions", [])

    if offline:
        all_cached = load_cache(cache_path)
        if not all_cached:
            return {"user_id": user_id, "alerts": [], "error": "no cache available (run without --offline first)"}
        if category != "all":
            source_names = {s["name"] for s in sources}
            changelogs = [c for c in all_cached if c.get("name") in source_names]
        else:
            changelogs = all_cached
    else:
        changelogs = fetch_all_changelogs(sources)
        if category == "all":
            try:
                save_cache(changelogs, cache_path)
                save_last_check()
            except OSError:
                pass
        else:
            existing = load_cache(cache_path)
            existing_names = {c["name"] for c in changelogs}
            merged = [c for c in existing if c.get("name") not in existing_names] + changelogs
            try:
                save_cache(merged, cache_path)
                save_last_check()
            except OSError:
                pass

    fetch_errors = [c for c in changelogs if c.get("error") and c["error"] != "disabled"]

    alerts = match_shifts(changelogs, assumptions, threshold=threshold)

    return {
        "user_id": user_id,
        "category": category,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "sources_checked": len([c for c in changelogs if not c.get("error")]),
        "sources_total": len(sources),
        "fetch_errors": [{
            "name": c["name"],
            "error": c["error"],
        } for c in fetch_errors],
        "assumption_count": len(assumptions),
        "alerts": alerts,
        "alert_count": len(alerts),
    }


def format_alert_one_liner(result: dict) -> str:
    """One-line summary for warmup integration."""
    cat = result.get("category", "all")
    cat_label = f" [{cat}]" if cat != "all" else ""
    if result.get("error"):
        return f"Capability shift{cat_label}: ERROR — {result['error']}"
    n = result.get("alert_count", 0)
    checked = result.get("sources_checked", 0)
    total = result.get("sources_total", 0)
    errors = len(result.get("fetch_errors", []))
    if n == 0 and errors == 0:
        return f"Capability shift{cat_label} ({checked}/{total} sources): no alerts"
    if n == 0 and errors > 0:
        err_names = ", ".join(e["name"] for e in result["fetch_errors"][:3])
        return f"Capability shift{cat_label} ({checked}/{total} sources): no alerts ({errors} fetch errors: {err_names})"
    alerts = result.get("alerts", [])
    review_count = sum(1 for a in alerts if a["action"] == "review")
    monitor_count = sum(1 for a in alerts if a["action"] == "monitor")
    variant_count = sum(1 for a in alerts if a.get("alert_class") == "variant")
    parts = []
    if review_count:
        parts.append(f"{review_count} REVIEW")
    if monitor_count:
        parts.append(f"{monitor_count} monitor")
    if variant_count:
        parts.append(f"{variant_count} variant")
    return f"Capability shift{cat_label} ({checked}/{total} sources): {', '.join(parts)} — run detect_capability_shift.py for details"


def format_text_report(result: dict) -> str:
    lines: list[str] = []

    if result.get("error"):
        lines.append(f"Capability Shift Detector — ERROR: {result['error']}")
        return "\n".join(lines)

    cat = result.get("category", "all")
    cat_label = f" [{cat}]" if cat != "all" else ""
    lines.append(f"Capability Shift Detector{cat_label} — {result.get('checked_at', '?')[:19]}")
    lines.append(f"  Sources: {result.get('sources_checked', 0)}/{result.get('sources_total', 0)} fetched")

    if result.get("fetch_errors"):
        for fe in result["fetch_errors"]:
            lines.append(f"  FETCH ERROR: {fe['name']} — {fe['error'][:100]}")

    lines.append(f"  Assumptions checked: {result.get('assumption_count', 0)}")
    lines.append(f"  Alerts: {result.get('alert_count', 0)}")
    lines.append("")

    alerts = result.get("alerts", [])
    if not alerts:
        lines.append("  No capability shifts detected.")
        return "\n".join(lines)

    for alert in alerts:
        action_tag = alert["action"].upper()
        class_tag = f" (variant)" if alert.get("alert_class") == "variant" else ""
        lines.append(
            f"  [{action_tag}]{class_tag} {alert['assumption_id']} — {alert['assumption'][:80]}"
        )
        lines.append(
            f"    Provider: {alert['provider']} | "
            f"Score: {alert['score']} ({len(alert['matched_keywords'])}/{alert['total_keywords']} keywords)"
        )
        lines.append(f"    Matched: {', '.join(alert['matched_keywords'][:6])}")
        if alert.get("affects"):
            lines.append(f"    Affects: {', '.join(alert['affects'][:4])}")
        if alert.get("notes"):
            lines.append(f"    Notes: {alert['notes'][:120]}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Capability shift detector — rolling-disruption sensor.",
        epilog="Two source categories: model (LLM providers) and ecosystem (frameworks, adjacent systems).",
    )
    ap.add_argument("-u", "--user", default=os.getenv("GRACE_MAR_USER_ID", "grace-mar"))
    ap.add_argument("--json", action="store_true", help="Output JSON instead of text")
    ap.add_argument("--offline", action="store_true", help="Use cached changelogs (no network)")
    ap.add_argument(
        "--category",
        choices=("all", "model", "ecosystem"),
        default="all",
        help="Source category: model (LLM providers) | ecosystem (frameworks) | all (default)",
    )
    ap.add_argument(
        "--threshold",
        type=float,
        default=0.3,
        help="Keyword match threshold 0.0–1.0 (default 0.3)",
    )
    args = ap.parse_args()

    result = detect_shifts(
        args.user,
        offline=args.offline,
        threshold=args.threshold,
        category=args.category,
    )

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    else:
        print(format_text_report(result))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
