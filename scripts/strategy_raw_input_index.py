"""Shared discovery for strategy-notebook ``raw-input/`` (per-expert, dated folders).

WORK-only; not Record. Used by ``strategy_expert_corpus`` and
``strategy_expert_transcript`` to avoid duplicating path walks.

**Doctrine:** Inbox is the capture registry; ``raw-input/`` is the verbatim body
store. This module only indexes on-disk files.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

from strategy_expert_corpus import RE_RAW_INPUT_MD_PATH, raw_input_paths_in_text
from strategy_expert_transcript import (
    _iter_raw_input_md_paths,
    iter_raw_input_yaml_documents,
)


def discover_raw_input_bullets_for_expert(
    notebook_dir: Path,
    expert_id: str,
    *,
    after_cutoff: date,
    month_filter_ym: str | None = None,
    max_bullets: int = 40,
) -> list[str]:
    """Build ``- [name](raw-input/...)`` lines for on-disk files tagged with ``thread:`` for this expert.

    ``after_cutoff``: include folder dates **strictly after** this date (same as triage
    7-day window: pass ``today - timedelta(days=7)``).
    When ``month_filter_ym`` is set (e.g. ``2026-04``), only files under
    ``raw-input/YYYY-MM-*`` for that month are included.
    """
    raw_root = notebook_dir / "raw-input"
    if not raw_root.is_dir():
        return []

    out: list[str] = []
    seen: set[str] = set()
    for path in _iter_raw_input_md_paths(raw_root, after_cutoff):
        try:
            rel = path.relative_to(notebook_dir)
        except ValueError:
            rel = path
        rel_s = str(rel).replace("\\", "/")
        if not rel_s.startswith("raw-input/"):
            continue
        parts = rel_s.split("/")
        if len(parts) < 3:
            continue
        folder_ymd = parts[1]
        if month_filter_ym:
            if len(folder_ymd) < 7 or folder_ymd[:7] != month_filter_ym:
                continue
        if rel_s in seen:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for fm, _body in iter_raw_input_yaml_documents(text):
            tid = (fm.get("thread") or "").strip()
            if tid != expert_id:
                continue
            seen.add(rel_s)
            name = path.name
            if path.is_file():
                out.append(f"- [{name}]({rel_s}) _on-disk_")
            if len(out) >= max_bullets:
                return out
            break
    return out


def merge_raw_input_bullet_lines(
    disk_lines: list[str],
    inbox_lines: list[str],
) -> list[str]:
    """De-dupe by ``raw-input/...`` path. *Disk* lines first, then inbox fills gaps."""
    by_path: dict[str, str] = {}
    order: list[str] = []
    for line in disk_lines + inbox_lines:
        ms = list(RE_RAW_INPUT_MD_PATH.finditer(line))
        if not ms:
            continue
        m = ms[0]
        rel = f"raw-input/{m.group(1)}/{m.group(2)}"
        if rel not in by_path:
            by_path[rel] = line.strip()
            order.append(rel)
    return [by_path[k] for k in order]
