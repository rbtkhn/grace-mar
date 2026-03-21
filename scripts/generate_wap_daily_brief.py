#!/usr/bin/env python3
"""
Generate a standard **daily brief** for work-politics + work-strategy.

**Preferred entrypoint:** `scripts/generate_work_politics_daily_brief.py` (this file remains as implementation + legacy alias).

  - Work-politics snapshot (calendar, gate, blockers)
  - Work-strategy focus (operator markdown)
  - Optional RSS ingest (configurable), dual keyword scores: **W** (campaign), **S** (product/AI/governance)
  - Per-feed `locale` (e.g. fr, de, es, ar, en) plus `wap_keyword_phrases_by_locale` / `strategy_keyword_phrases_by_locale`
    in config — extra phrase lists for scoring **only** (no translation API; zero-API mode).
  - Optional **`ingest_caps`**: per-feed `max_items` and/or `tier` (1–3) with `default_max_items_per_feed` + `max_items_by_tier`
    so high-volume feeds do not dominate before W+S ranking.

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

# Cross-language “story” anchors (substring match on title+URL blob). Merged with config `story_anchor_phrases`.
DEFAULT_STORY_ANCHORS: tuple[str, ...] = (
    "trump",
    "biden",
    "iran",
    "israel",
    "gaza",
    "hamas",
    "nato",
    "otan",
    "ukraine",
    "russia",
    "putin",
    "china",
    "syria",
    "yemen",
    "lebanon",
    "iraq",
    "afghanistan",
    "kiev",
    "kyiv",
    "tehran",
    "hezbollah",
    "massie",
    "gallrein",
    "kentucky",
    "congress",
    "senate",
    "netanyahu",
    "venezuela",
    "taiwan",
    "north korea",
    "guerre",
    "krieg",
    "guerra",
    "حرب",
    "إيران",
    "ترامب",
    "إسرائيل",
    "غزة",
    "أوكرانيا",
    "روسيا",
    "الناتو",
    "حماس",
    "طهران",
    "واشنطن",
    "الكونغرس",
    "diplomatie",
    "diplomacy",
    "sanctions",
    "sanktionen",
    "sanciones",
    "pentagon",
    "pentagone",
    "washington",
    "moyen-orient",
    "nahost",
    "oriente medio",
    "middle east",
)

DEFAULT_STORY_DEDUPE: dict[str, object] = {
    "enabled": True,
    "min_anchors": 2,
    "jaccard_min": 0.38,
    "min_shared_anchors": 2,
    "max_items_for_clustering": 260,
    "max_alsos_per_cluster": 4,
}

# Before global W+S ranking: max items kept per feed (after recency sort within feed).
DEFAULT_INGEST_CAPS: dict[str, object] = {
    "default_max_items_per_feed": 12,
    "max_items_by_tier": {1: 14, 2: 10, 3: 6},
}

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


def _merge_story_anchors(data: dict) -> tuple[str, ...]:
    extra = data.get("story_anchor_phrases") if isinstance(data, dict) else None
    merged: list[str] = []
    seen: set[str] = set()
    for p in DEFAULT_STORY_ANCHORS:
        pl = p.lower()
        if pl not in seen:
            seen.add(pl)
            merged.append(pl)
    if isinstance(extra, list):
        for x in extra:
            pl = str(x).lower().strip()
            if pl and pl not in seen:
                seen.add(pl)
                merged.append(pl)
    return tuple(merged)


def _load_story_dedupe(data: dict) -> dict[str, object]:
    out = dict(DEFAULT_STORY_DEDUPE)
    raw = data.get("story_dedupe") if isinstance(data, dict) else None
    if isinstance(raw, dict):
        for k in out:
            if k in raw:
                out[k] = raw[k]
    return out


def _normalize_tier_caps(raw: object, defaults: dict[int, int]) -> dict[int, int]:
    out = dict(defaults)
    if not isinstance(raw, dict):
        return out
    for k, v in raw.items():
        try:
            ki = int(k)
            out[ki] = int(v)
        except (TypeError, ValueError):
            continue
    return out


def _load_ingest_caps(data: dict) -> dict[str, object]:
    base = dict(DEFAULT_INGEST_CAPS)
    raw_tm = base["max_items_by_tier"]
    if not isinstance(raw_tm, dict):
        tier_defaults: dict[int, int] = {1: 14, 2: 10, 3: 6}
    else:
        tier_defaults = {int(k): int(v) for k, v in raw_tm.items()}
    raw = data.get("ingest_caps") if isinstance(data, dict) else None
    if not isinstance(raw, dict):
        base["max_items_by_tier"] = tier_defaults
        return base
    if "default_max_items_per_feed" in raw:
        try:
            base["default_max_items_per_feed"] = max(1, int(raw["default_max_items_per_feed"]))
        except (TypeError, ValueError):
            pass
    base["max_items_by_tier"] = _normalize_tier_caps(raw.get("max_items_by_tier"), tier_defaults)
    return base


def _effective_feed_cap(feed: dict[str, object], caps: dict[str, object], override: int | None) -> int:
    if override is not None and override > 0:
        return override
    explicit = feed.get("max_items")
    if explicit is not None:
        try:
            v = int(explicit)
            if v > 0:
                return v
        except (TypeError, ValueError):
            pass
    tier_map = caps.get("max_items_by_tier")
    if isinstance(tier_map, dict):
        try:
            tr = int(feed.get("tier", 2))
        except (TypeError, ValueError):
            tr = 2
        if tr in tier_map:
            try:
                return max(1, int(tier_map[tr]))
            except (TypeError, ValueError):
                pass
    try:
        return max(1, int(caps.get("default_max_items_per_feed", 12)))
    except (TypeError, ValueError):
        return 12


def _sort_feed_items_by_recency(items: list[dict[str, object]]) -> list[dict[str, object]]:
    """Newest first; undated last (stable within groups)."""

    def _key(it: dict[str, object]) -> tuple[int, float]:
        sd = it.get("sort_date")
        if isinstance(sd, datetime):
            return (0, sd.timestamp())
        return (1, 0.0)

    return sorted(items, key=_key, reverse=True)


def _load_full_config(
    path: Path,
) -> tuple[
    list[dict[str, object]],
    tuple[str, ...],
    tuple[str, ...],
    dict[str, tuple[str, ...]],
    dict[str, tuple[str, ...]],
    tuple[str, ...],
    dict[str, object],
    dict[str, object],
]:
    if not path.exists():
        return (
            [],
            DEFAULT_WAP_PHRASES,
            DEFAULT_STRATEGY_PHRASES,
            {},
            {},
            DEFAULT_STORY_ANCHORS,
            dict(DEFAULT_STORY_DEDUPE),
            dict(DEFAULT_INGEST_CAPS),
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return (
            [],
            DEFAULT_WAP_PHRASES,
            DEFAULT_STRATEGY_PHRASES,
            {},
            {},
            DEFAULT_STORY_ANCHORS,
            dict(DEFAULT_STORY_DEDUPE),
            dict(DEFAULT_INGEST_CAPS),
        )
    feeds_raw = data.get("feeds") if isinstance(data, dict) else None
    feeds: list[dict[str, object]] = []
    if isinstance(feeds_raw, list):
        for row in feeds_raw:
            if not isinstance(row, dict):
                continue
            url = str(row.get("url", "")).strip()
            name = str(row.get("name", "")).strip() or url
            loc = str(row.get("locale", "en") or "en").strip().lower() or "en"
            tier = 2
            tr = row.get("tier")
            if tr is not None:
                try:
                    tier = int(tr)
                except (TypeError, ValueError):
                    tier = 2
            max_items_raw = row.get("max_items")
            if url:
                feeds.append(
                    {
                        "name": name,
                        "url": url,
                        "locale": loc,
                        "tier": tier,
                        "max_items": max_items_raw,
                    }
                )
    wap_t = data.get("wap_keyword_phrases") if isinstance(data, dict) else None
    strat_t = data.get("strategy_keyword_phrases") if isinstance(data, dict) else None
    wap = _phrases_tuple(wap_t, DEFAULT_WAP_PHRASES)
    strat = _phrases_tuple(strat_t, DEFAULT_STRATEGY_PHRASES)
    wap_loc = _locale_phrase_map(data, "wap_keyword_phrases_by_locale")
    strat_loc = _locale_phrase_map(data, "strategy_keyword_phrases_by_locale")
    story_anchors = _merge_story_anchors(data) if isinstance(data, dict) else DEFAULT_STORY_ANCHORS
    story_dedupe = _load_story_dedupe(data) if isinstance(data, dict) else dict(DEFAULT_STORY_DEDUPE)
    ingest_caps = _load_ingest_caps(data) if isinstance(data, dict) else dict(DEFAULT_INGEST_CAPS)
    return feeds, wap, strat, wap_loc, strat_loc, story_anchors, story_dedupe, ingest_caps


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


def _story_anchor_set(blob: str, phrases: tuple[str, ...]) -> frozenset[str]:
    """Which anchor phrases appear as substrings in blob (already lowercased)."""
    matched: set[str] = set()
    for phrase in phrases:
        if phrase in blob:
            matched.add(phrase)
    return frozenset(matched)


def _jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a and not b:
        return 1.0
    u = len(a | b)
    if u == 0:
        return 0.0
    return len(a & b) / u


class _UnionFind:
    def __init__(self, n: int) -> None:
        self._p = list(range(n))

    def find(self, x: int) -> int:
        while self._p[x] != x:
            self._p[x] = self._p[self._p[x]]
            x = self._p[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self._p[rb] = ra


def _cluster_story_items(
    items: list[dict[str, object]],
    story_anchors: tuple[str, ...],
    opts: dict[str, object],
) -> tuple[list[list[dict[str, object]]], list[dict[str, object]]]:
    """
    Group items that likely cover the same story (anchor overlap).
    Returns (multi-item clusters, singletons). Clusters sorted by max score_sum.
    """
    max_n = int(opts.get("max_items_for_clustering", 260) or 260)
    min_anchors = int(opts.get("min_anchors", 2) or 2)
    jaccard_min = float(opts.get("jaccard_min", 0.38) or 0.38)
    min_shared = int(opts.get("min_shared_anchors", 2) or 2)

    n = min(len(items), max_n)
    asets: list[frozenset[str]] = []
    for it in items:
        blob = str(it.get("text_blob", ""))
        asets.append(_story_anchor_set(blob, story_anchors))

    # Eligible row indices 0..n-1 with enough anchors
    eligible_pos = [i for i in range(n) if len(asets[i]) >= min_anchors]
    m = len(eligible_pos)
    if m < 2:
        return [], list(items)

    uf = _UnionFind(m)
    for a in range(m):
        for b in range(a + 1, m):
            ia, ib = eligible_pos[a], eligible_pos[b]
            sa, sb = asets[ia], asets[ib]
            inter = len(sa & sb)
            if inter < min_shared:
                continue
            if _jaccard(sa, sb) < jaccard_min:
                continue
            uf.union(a, b)

    buckets: dict[int, list[int]] = {}
    for pos in range(m):
        root = uf.find(pos)
        buckets.setdefault(root, []).append(eligible_pos[pos])

    multi: list[list[int]] = [sorted(set(g)) for g in buckets.values() if len(g) >= 2]
    in_multi: set[int] = set()
    for g in multi:
        in_multi.update(g)

    clusters: list[list[dict[str, object]]] = []
    for g in multi:
        cluster_items = [items[i] for i in g]

        def _prim_key(x: dict[str, object]) -> tuple[int, int, int, float]:
            sd = x.get("sort_date")
            ts = float(sd.timestamp()) if isinstance(sd, datetime) else 0.0
            return (int(x.get("score_sum", 0)), int(x.get("score_w", 0)), int(x.get("score_s", 0)), ts)

        cluster_items.sort(key=_prim_key, reverse=True)
        clusters.append(cluster_items)

    clusters.sort(
        key=lambda c: (
            int(c[0].get("score_sum", 0)),
            int(c[0].get("score_w", 0)),
            len(c),
        ),
        reverse=True,
    )

    singletons: list[dict[str, object]] = []
    covered = set(in_multi)
    for i, it in enumerate(items):
        if i not in covered:
            singletons.append(it)

    return clusters, singletons


def _cluster_label(cluster: list[dict[str, object]], story_anchors: tuple[str, ...]) -> str:
    union_a: set[str] = set()
    for it in cluster:
        blob = str(it.get("text_blob", ""))
        union_a |= set(_story_anchor_set(blob, story_anchors))
    if not union_a:
        return "cluster"
    # Short readable label (Latin-heavy; Arabic anchors may appear)
    parts = sorted(union_a)[:5]
    return " · ".join(parts)


def _headline_md_line(it: dict[str, object], *, also: bool = False) -> str:
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
    if also:
        return (
            f"- **Also** — [{title}]({link}) — _{feed}_{loc_note} · "
            f"_W:{sw} S:{ss}_{date_note}"
        )
    return f"- **[W:{sw} S:{ss}]** [{title}]({link}) — _{feed}_{loc_note}{date_note}"


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
    story_dedupe_enabled: bool = True,
    max_per_feed_override: int | None = None,
) -> str:
    assembled = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    feeds, wap_phrases, strategy_phrases, wap_by_locale, strategy_by_locale, story_anchors, story_dedupe, ingest_caps = (
        _load_full_config(config_path)
    )
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
        "## 1. Work-politics snapshot",
        "",
        f"- **Primary:** {primary.get('primary_date')} — **days until:** {primary.get('days_until_primary')}",
        f"- **Work-politics gate:** {gate.get('pending_count', 0)} pending candidate(s)",
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
            raw = _fetch_feed(str(fdef["url"]))
            if raw is None:
                fetch_errors.append(str(fdef["name"]))
                continue
            parsed = _parse_feed_xml(raw, str(fdef["name"]))
            loc = str(fdef.get("locale", "en") or "en").strip().lower() or "en"
            for it in parsed:
                it["locale"] = loc
            parsed = _sort_feed_items_by_recency(parsed)
            cap = _effective_feed_cap(fdef, ingest_caps, max_per_feed_override)
            all_items.extend(parsed[:cap])
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

    dedupe_effective = (
        fetch_feeds
        and bool(all_items)
        and story_dedupe_enabled
        and bool(story_dedupe.get("enabled", True))
    )
    if dedupe_effective:
        clusters, singletons_render = _cluster_story_items(all_items, story_anchors, story_dedupe)
    else:
        clusters = []
        singletons_render = list(all_items)

    if fetch_feeds and all_items:
        lines.append(
            "Ranked by **W+S** (global keyword lists + `wap_keyword_phrases_by_locale` / "
            "`strategy_keyword_phrases_by_locale` for each feed `locale`) then recency. "
            "Each feed is **recency-sorted** then **capped** (`ingest_caps`: per-feed `max_items` and/or `tier` → "
            "`max_items_by_tier`; CLI `--max-per-feed N` overrides all feeds). "
            "Optional **same-story** grouping uses `story_anchor_phrases` overlap (Jaccard + shared anchors). "
            "Tune phrases in config JSON."
        )
        lines.append("")
        if dedupe_effective:
            lines.append(
                "_Same-story clusters use anchor overlap on titles (proper nouns / crisis terms); "
                "not neural / semantic dedupe._"
            )
            lines.append("")
            shown = 0
            max_alsos = int(story_dedupe.get("max_alsos_per_cluster", 4) or 4)
            if clusters:
                lines.append("#### Same-story (multilingual)")
                lines.append("")
                for cl in clusters:
                    if shown >= max_items_display:
                        break
                    label = _cluster_label(cl, story_anchors)
                    lines.append(f"**{label}** — _{len(cl)} sources_")
                    lines.append("")
                    for j, it in enumerate(cl):
                        if shown >= max_items_display:
                            break
                        if j == 0:
                            lines.append(_headline_md_line(it, also=False))
                        elif j <= max_alsos:
                            lines.append(_headline_md_line(it, also=True))
                        else:
                            break
                        shown += 1
                    lines.append("")
            if clusters and singletons_render:
                lines.append("#### Other headlines")
                lines.append("")
            for it in singletons_render:
                if shown >= max_items_display:
                    break
                lines.append(_headline_md_line(it, also=False))
                shown += 1
            lines.append("")
        else:
            shown = 0
            for it in all_items:
                if shown >= max_items_display:
                    break
                lines.append(_headline_md_line(it, also=False))
                shown += 1
            lines.append("")
    elif fetch_feeds and not all_items and feeds:
        lines.append("_No items parsed or all outside recency window._ Try `--max-age-hours` or check feed URLs.")
        lines.append("")

    # Top titles per lane (dedupe: one line per cluster + singletons)
    if dedupe_effective:
        theme_pool: list[dict[str, object]] = [c[0] for c in clusters] + singletons_render
    else:
        theme_pool = list(all_items)
    top_w = sorted(
        theme_pool,
        key=lambda x: (int(x.get("score_w", 0)), int(x.get("score_sum", 0))),
        reverse=True,
    )
    top_s = sorted(
        theme_pool,
        key=lambda x: (int(x.get("score_s", 0)), int(x.get("score_sum", 0))),
        reverse=True,
    )
    w_titles = [str(x.get("title", "")) for x in top_w[:3] if int(x.get("score_w", 0)) > 0]
    s_titles = [str(x.get("title", "")) for x in top_s[:3] if int(x.get("score_s", 0)) > 0]
    if not w_titles and all_items:
        w_titles = [str(all_items[0].get("title", ""))]
    if not s_titles and all_items:
        s_titles = [str(all_items[0].get("title", ""))]

    lines.extend(["## 3. Lead themes (auto-stub — replace after reading)", ""])
    lines.append("### Work-politics / campaign angle")
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
            "**Work-politics:** _paragraph_",
            "",
            "**Work-strategy:** _paragraph_",
            "",
            "## 6. Next actions (work-politics snapshot)",
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
            f"_Generated by `scripts/generate_work_politics_daily_brief.py` (legacy alias: `generate_wap_daily_brief.py`); config `{cfg_rel}`._",
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
        help=f"JSON config (default: {DEFAULT_CONFIG.relative_to(REPO_ROOT)} if present, else legacy work-politics feeds JSON)",
    )
    parser.add_argument(
        "--feeds",
        default="",
        help="(Deprecated) Alias: use as --config path for JSON file",
    )
    parser.add_argument("--max-age-hours", type=int, default=36, help="RSS recency window (default 36h; 0 = off)")
    parser.add_argument("--max-items", type=int, default=20, help="Max headline lines (default 20)")
    parser.add_argument(
        "--no-story-dedupe",
        action="store_true",
        help="Disable same-story clustering (flat headline list)",
    )
    parser.add_argument(
        "--max-per-feed",
        type=int,
        default=0,
        metavar="N",
        help="Override ingest cap for every feed (0 = use config per-feed / tier)",
    )
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
        story_dedupe_enabled=not args.no_story_dedupe,
        max_per_feed_override=(args.max_per_feed if args.max_per_feed > 0 else None),
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
