#!/usr/bin/env python3
"""
Generate a standard **daily brief** for work-politics + work-strategy:

  - WAP snapshot (calendar, gate, blockers)
  - Work-strategy focus (operator markdown)
  - Optional RSS ingest (configurable), dual keyword scores: **W** (campaign), **S** (product/AI/governance)
  - Per-feed `locale` (e.g. fr, de, es, ar, en) plus `wap_keyword_phrases_by_locale` / `strategy_keyword_phrases_by_locale`
    in config — extra phrase lists for scoring **only** (no translation API; zero-API mode).

Config (default):
  docs/skill-work/work-strategy/daily-brief-config.json

Legacy fallback:
  docs/skill-work/work-politics/daily-brief-feeds.json (feeds only; built-in keyword lists)

Does not call paid news APIs. Output is operator WORK product — not Voice, not SELF.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WAP_DIR = REPO_ROOT / "docs" / "skill-work" / "work-politics"
STRATEGY_DIR = REPO_ROOT / "docs" / "skill-work" / "work-strategy"
DEFAULT_CONFIG = STRATEGY_DIR / "daily-brief-config.json"
LEGACY_FEEDS_JSON = WAP_DIR / "daily-brief-feeds.json"
STRATEGY_FOCUS_MD = STRATEGY_DIR / "daily-brief-focus.md"
DEFAULT_UA = "Grace-Mar-work-daily-brief/1.0 (+local research; contact: operator)"

DEFAULT_WAP_PHRASES: tuple[str, ...] = (
    "massie",
    "gallrein",
    "kentucky",
    "ky-4",
    "ky4",
    "ky-04",
    "trump",
    "iran",
    "war power",
    "congress",
    "house",
    "senate",
    "fec",
    "primary",
    "election",
    "campaign",
    "republican",
    "fourth district",
    "rep. thomas",
    "thomas massie",
)

DEFAULT_STRATEGY_PHRASES: tuple[str, ...] = (
    "openai",
    "anthropic",
    "google",
    "artificial intelligence",
    "machine learning",
    " llm",
    "language model",
    "ai agent",
    "ai governance",
    "regulation",
    "school",
    "education",
    "student",
    "privacy",
    "identity",
    "open source",
    " api",
    "telegram",
    "chatgpt",
    "memory",
    "lock-in",
    "portable",
    "companion",
    "bitcoin",
    "cryptocurrency",
    "supreme court",
    "antitrust",
    "startup",
    "venture",
    "show hn",
    "hn ",
)

try:
    from work_politics_ops import get_wap_snapshot
except ImportError:
    from scripts.work_politics_ops import get_wap_snapshot


def _default_config_path() -> Path:
    if DEFAULT_CONFIG.exists():
        return DEFAULT_CONFIG
    return LEGACY_FEEDS_JSON


def _phrases_tuple(raw: object, fallback: tuple[str, ...]) -> tuple[str, ...]:
    if isinstance(raw, list) and raw:
        return tuple(str(x).lower() for x in raw)
    return fallback


def _locale_phrase_map(data: dict, key: str) -> dict[str, tuple[str, ...]]:
    """Map locale code -> extra keyword phrases (merged at score time with global lists)."""
    raw = data.get(key) if isinstance(data, dict) else None
    if not isinstance(raw, dict):
        return {}
    out: dict[str, tuple[str, ...]] = {}
    for k, v in raw.items():
        lc = str(k).lower().strip()
        if not lc or not isinstance(v, list):
            continue
        out[lc] = tuple(str(x).lower() for x in v)
    return out


def _load_full_config(
    path: Path,
) -> tuple[
    list[dict[str, str]],
    tuple[str, ...],
    tuple[str, ...],
    dict[str, tuple[str, ...]],
    dict[str, tuple[str, ...]],
]:
    if not path.exists():
        return [], DEFAULT_WAP_PHRASES, DEFAULT_STRATEGY_PHRASES, {}, {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return [], DEFAULT_WAP_PHRASES, DEFAULT_STRATEGY_PHRASES, {}, {}
    feeds_raw = data.get("feeds") if isinstance(data, dict) else None
    feeds: list[dict[str, str]] = []
    if isinstance(feeds_raw, list):
        for row in feeds_raw:
            if not isinstance(row, dict):
                continue
            url = str(row.get("url", "")).strip()
            name = str(row.get("name", "")).strip() or url
            loc = str(row.get("locale", "en") or "en").strip().lower() or "en"
            if url:
                feeds.append({"name": name, "url": url, "locale": loc})
    wap_t = data.get("wap_keyword_phrases") if isinstance(data, dict) else None
    strat_t = data.get("strategy_keyword_phrases") if isinstance(data, dict) else None
    wap = _phrases_tuple(wap_t, DEFAULT_WAP_PHRASES)
    strat = _phrases_tuple(strat_t, DEFAULT_STRATEGY_PHRASES)
    wap_loc = _locale_phrase_map(data, "wap_keyword_phrases_by_locale")
    strat_loc = _locale_phrase_map(data, "strategy_keyword_phrases_by_locale")
    return feeds, wap, strat, wap_loc, strat_loc


def _extract_strategy_focus() -> str:
    if not STRATEGY_FOCUS_MD.exists():
        return "_No `docs/skill-work/work-strategy/daily-brief-focus.md` yet._"
    text = STRATEGY_FOCUS_MD.read_text(encoding="utf-8")
    m = re.search(r"## Active focus\s*\n+(.*?)(?=\n## |\Z)", text, re.DOTALL | re.IGNORECASE)
    body = (m.group(1).strip() if m else text)[:4000]
    if not body.strip():
        return "_Edit `daily-brief-focus.md` § Active focus._"
    out: list[str] = []
    for ln in body.splitlines():
        s = ln.strip()
        if not s:
            continue
        out.append(s if s.startswith("- ") else f"- {s}")
    return "\n".join(out)


def _local_tag(tag: str) -> str:
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _text(elem: ET.Element | None) -> str:
    if elem is None or elem.text is None:
        return ""
    return html.unescape((elem.text or "").strip())


def _atom_link(entry: ET.Element) -> str:
    for link in entry:
        if _local_tag(link.tag) != "link":
            continue
        href = link.attrib.get("href", "")
        if href:
            return href
    return ""


def _parse_rss_items(root: ET.Element, feed_label: str) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    channel = root.find("channel")
    if channel is None:
        return items
    for node in channel:
        if _local_tag(node.tag) != "item":
            continue
        title_el = node.find("title")
        link_el = node.find("link")
        date_el = node.find("pubDate")
        title = _text(title_el)
        link = _text(link_el)
        pub_raw = _text(date_el)
        sort_date: datetime | None = None
        if pub_raw:
            try:
                sort_date = parsedate_to_datetime(pub_raw)
                if sort_date.tzinfo is None:
                    sort_date = sort_date.replace(tzinfo=timezone.utc)
            except (TypeError, ValueError, OverflowError):
                sort_date = None
        if title and link:
            items.append(
                {
                    "feed": feed_label,
                    "title": title,
                    "link": link,
                    "sort_date": sort_date,
                    "text_blob": f"{title} {link}".lower(),
                }
            )
    return items


def _parse_atom_items(root: ET.Element, feed_label: str) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    for node in root.iter():
        if _local_tag(node.tag) != "entry":
            continue
        title = ""
        sort_date: datetime | None = None
        link = ""
        for child in node:
            lt = _local_tag(child.tag)
            if lt == "title":
                title = _text(child) or html.unescape("".join(child.itertext())).strip()
            elif lt == "link":
                link = child.attrib.get("href", "")
            elif lt == "updated":
                raw = _text(child)
                if raw:
                    try:
                        sort_date = datetime.fromisoformat(raw.replace("Z", "+00:00"))
                    except ValueError:
                        sort_date = None
        if not link:
            link = _atom_link(node)
        if title and link:
            items.append(
                {
                    "feed": feed_label,
                    "title": title,
                    "link": link,
                    "sort_date": sort_date,
                    "text_blob": f"{title} {link}".lower(),
                }
            )
    return items


def _parse_feed_xml(data: bytes, feed_label: str) -> list[dict[str, object]]:
    try:
        root = ET.fromstring(data)
    except ET.ParseError:
        return []
    root_tag = _local_tag(root.tag).lower()
    if root_tag == "rss":
        return _parse_rss_items(root, feed_label)
    if root_tag == "feed":
        return _parse_atom_items(root, feed_label)
    return []


def _fetch_feed(url: str, timeout: int = 20) -> bytes | None:
    req = urllib.request.Request(url, headers={"User-Agent": DEFAULT_UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except (urllib.error.URLError, OSError, TimeoutError, ValueError):
        return None


def _score_keywords(hay: str, phrases: tuple[str, ...]) -> int:
    score = 0
    for phrase in phrases:
        if phrase.lower() in hay:
            score += 1
    return score


def _filter_recent(items: list[dict[str, object]], max_age_hours: int) -> list[dict[str, object]]:
    if max_age_hours <= 0:
        return items
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    in_window: list[dict[str, object]] = []
    undated: list[dict[str, object]] = []
    for it in items:
        sd = it.get("sort_date")
        if isinstance(sd, datetime):
            if sd >= cutoff:
                in_window.append(it)
        else:
            undated.append(it)
    if in_window:
        return in_window + undated
    dated_out = [it for it in items if isinstance(it.get("sort_date"), datetime)]
    dated_out.sort(key=lambda x: x.get("sort_date"), reverse=True)
    return undated + dated_out[:24]


def build_daily_brief(
    user_id: str,
    *,
    fetch_feeds: bool,
    config_path: Path,
    max_age_hours: int,
    max_items_display: int,
) -> str:
    assembled = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    feeds, wap_phrases, strategy_phrases, wap_by_locale, strategy_by_locale = _load_full_config(config_path)
    snapshot = get_wap_snapshot(user_id)
    primary = snapshot["campaign_status"]
    gate = snapshot["gate"]
    blockers = snapshot["territory_blockers"]
    cfg_rel = config_path.relative_to(REPO_ROOT)

    lines = [
        "# Daily brief — work-politics & work-strategy",
        "",
        f"**Date:** {day}  ",
        f"**Assembled:** {assembled}  ",
        f"**Recency window (RSS):** last **{max_age_hours}h** (undated items may appear)  ",
        f"**Config:** `{cfg_rel}`  ".strip(),
        "",
        "_Operator WORK product. Complete synthesis below; cite sources before any public use._",
        "",
        "## 1. Work-politics (WAP) snapshot",
        "",
        f"- **Primary:** {primary.get('primary_date')} — **days until:** {primary.get('days_until_primary')}",
        f"- **WAP gate:** {gate.get('pending_count', 0)} pending candidate(s)",
        "",
        "### Upcoming (from calendar)",
        "",
    ]
    for row in (primary.get("upcoming_dates") or [])[:5]:
        lines.append(f"- **{row.get('date')}** — {row.get('event')} — {row.get('decision')}")
    if not (primary.get("upcoming_dates") or []):
        lines.append("- _(none parsed — see calendar-2026.md)_")
    lines.extend(["", "### Territory signals (from docs)", ""])
    for b in blockers[:5]:
        lines.append(f"- **{b.get('kind')}:** {b.get('title')}")

    lines.extend(
        [
            "",
            "## 1b. Work-strategy focus",
            "",
            "_From `docs/skill-work/work-strategy/daily-brief-focus.md` § Active focus._",
            "",
        ]
    )
    for line in _extract_strategy_focus().splitlines():
        lines.append(line)
    lines.extend(
        [
            "",
            "_Product / integration context: [work-dev/workspace.md](../work-dev/workspace.md), [work-strategy/README.md](../../work-strategy/README.md)._",
            "",
            "## 2. Headlines (ingested RSS)",
            "",
        ]
    )

    fetch_errors: list[str] = []
    all_items: list[dict[str, object]] = []

    if fetch_feeds:
        if not feeds:
            lines.append(
                "_No feeds in config._ Add RSS URLs to "
                f"`{cfg_rel}`."
            )
            lines.append("")
        for fdef in feeds:
            raw = _fetch_feed(fdef["url"])
            if raw is None:
                fetch_errors.append(fdef["name"])
                continue
            parsed = _parse_feed_xml(raw, fdef["name"])
            loc = str(fdef.get("locale", "en") or "en").strip().lower() or "en"
            for it in parsed:
                it["locale"] = loc
            all_items.extend(parsed)
        if fetch_errors:
            lines.append(f"_Fetch failed for: {', '.join(fetch_errors)}._")
            lines.append("")
    else:
        lines.append("_`--no-fetch`: RSS skipped._")
        lines.append("")

    all_items = _filter_recent(all_items, max_age_hours if fetch_feeds else 0)
    for it in all_items:
        blob = str(it.get("text_blob", ""))
        loc = str(it.get("locale", "en") or "en").strip().lower() or "en"
        w_extra = wap_by_locale.get(loc, ())
        s_extra = strategy_by_locale.get(loc, ())
        it["score_w"] = _score_keywords(blob, wap_phrases) + _score_keywords(blob, w_extra)
        it["score_s"] = _score_keywords(blob, strategy_phrases) + _score_keywords(blob, s_extra)
        it["score_sum"] = int(it["score_w"]) + int(it["score_s"])

    def _sort_key(x: dict[str, object]) -> tuple[int, int, int, float]:
        sd = x.get("sort_date")
        ts = float(sd.timestamp()) if isinstance(sd, datetime) else 0.0
        return (int(x.get("score_sum", 0)), int(x.get("score_w", 0)), int(x.get("score_s", 0)), ts)

    all_items.sort(key=_sort_key, reverse=True)

    if fetch_feeds and all_items:
        lines.append(
            "Ranked by **W+S** (global keyword lists + `wap_keyword_phrases_by_locale` / "
            "`strategy_keyword_phrases_by_locale` for each feed `locale`) then recency. "
            "Tune phrases in config JSON."
        )
        lines.append("")
        shown = 0
        for it in all_items:
            if shown >= max_items_display:
                break
            title = it.get("title", "")
            link = it.get("link", "")
            feed = it.get("feed", "")
            loc = str(it.get("locale", "en") or "en").strip().lower() or "en"
            sw = int(it.get("score_w", 0))
            ss = int(it.get("score_s", 0))
            sd = it.get("sort_date")
            date_note = ""
            if isinstance(sd, datetime):
                date_note = f" · _{sd.strftime('%Y-%m-%d %H:%M UTC')}_"
            loc_note = f" · _{loc}_" if loc != "en" else ""
            lines.append(f"- **[W:{sw} S:{ss}]** [{title}]({link}) — _{feed}_{loc_note}{date_note}")
            shown += 1
        lines.append("")
    elif fetch_feeds and not all_items and feeds:
        lines.append("_No items parsed or all outside recency window._ Try `--max-age-hours` or check feed URLs.")
        lines.append("")

    # Top titles per lane
    top_w = sorted(all_items, key=lambda x: (int(x.get("score_w", 0)), int(x.get("score_sum", 0))), reverse=True)
    top_s = sorted(all_items, key=lambda x: (int(x.get("score_s", 0)), int(x.get("score_sum", 0))), reverse=True)
    w_titles = [str(x.get("title", "")) for x in top_w[:3] if int(x.get("score_w", 0)) > 0]
    s_titles = [str(x.get("title", "")) for x in top_s[:3] if int(x.get("score_s", 0)) > 0]
    if not w_titles and all_items:
        w_titles = [str(all_items[0].get("title", ""))]
    if not s_titles and all_items:
        s_titles = [str(all_items[0].get("title", ""))]

    lines.extend(["## 3. Lead themes (auto-stub — replace after reading)", ""])
    lines.append("### WAP/campaign angle")
    if w_titles and any(w_titles):
        for t in w_titles:
            if t:
                lines.append(f"- {t}")
        lines.append("")
        lines.append("**Replace:** 2–3 sentences for principal, district, opposition narrative.")
    else:
        lines.append("_No W-scored headlines — pull from principal X, local news, [brief-source-registry](../work-politics/brief-source-registry.md)._")
    lines.extend(["", "### Work-strategy angle (product / governance / tech)", ""])
    if s_titles and any(s_titles):
        for t in s_titles:
            if t:
                lines.append(f"- {t}")
        lines.append("")
        lines.append("**Replace:** 2–3 sentences for Record/Voice positioning, OpenClaw, schools, or policy hooks.")
    else:
        lines.append("_No S-scored headlines — scan [work-dev/integration-status](../work-dev/integration-status.md) or add feeds._")

    lines.extend(
        [
            "",
            "## 4. Triangulation (when lead is political)",
            "",
            "For **campaign-facing** copy, use [work-politics analytical-lenses](../work-politics/analytical-lenses/template-three-lenses.md) on a shared fact summary.",
            "",
            "| Structural | Operational / diplomatic | Institutional |",
            "|---|---|---|",
            "| _TBD_ | _TBD_ | _TBD_ |",
            "",
            "**Product / strategy thread:** _TBD (no three-lens requirement — use work-dev + INTENT as needed)._",
            "",
            "## 5. Operator synthesis",
            "",
            "**WAP:** _paragraph_",
            "",
            "**Work-strategy:** _paragraph_",
            "",
            "## 6. Next actions (WAP snapshot)",
            "",
        ]
    )
    for a in (snapshot.get("next_actions") or [])[:4]:
        lines.append(f"- {a}")
    if not (snapshot.get("next_actions") or []):
        lines.append("- _TBD_")

    lines.extend(
        [
            "",
            "---",
            "",
            f"_Generated by `scripts/generate_wap_daily_brief.py`; config `{cfg_rel}`._",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Daily brief: work-politics + work-strategy (RSS optional)"
    )
    parser.add_argument("-u", "--user", default="grace-mar", help="User id for gate snapshot")
    parser.add_argument("-o", "--output", default="", help="Write markdown to this path")
    parser.add_argument("--no-fetch", action="store_true", help="Skip RSS")
    parser.add_argument(
        "--config",
        default="",
        help=f"JSON config (default: {DEFAULT_CONFIG.relative_to(REPO_ROOT)} if present, else legacy WAP feeds JSON)",
    )
    parser.add_argument(
        "--feeds",
        default="",
        help="(Deprecated) Alias: use as --config path for JSON file",
    )
    parser.add_argument("--max-age-hours", type=int, default=36, help="RSS recency window (default 36h; 0 = off)")
    parser.add_argument("--max-items", type=int, default=20, help="Max headline lines (default 20)")
    args = parser.parse_args()
    if args.feeds and not args.config:
        config_path = Path(args.feeds)
    elif args.config:
        config_path = Path(args.config)
    else:
        config_path = _default_config_path()
    text = build_daily_brief(
        args.user,
        fetch_feeds=not args.no_fetch,
        config_path=config_path,
        max_age_hours=args.max_age_hours,
        max_items_display=args.max_items,
    )
    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
