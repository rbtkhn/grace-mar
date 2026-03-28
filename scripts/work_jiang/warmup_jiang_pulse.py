#!/usr/bin/env python3
"""
Read-only 'momentum' snippets for operator good morning / good night — Predictive History lane.

Pulls `users/<id>/work-jiang.md` **Instance work context (YAML)** (see skills-modularity §2a) plus
STATUS / CHAPTER-QUEUE hints and rotates optional sparks from
research/external/work-jiang/metadata/warmup-sparks.yaml (operator-editable).

Does not write the Record or touch the gate.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
SPARKS_PATH = WORK_DIR / "metadata" / "warmup-sparks.yaml"
STATUS_PATH = WORK_DIR / "STATUS.md"
CHAPTER_QUEUE_PATH = WORK_DIR / "CHAPTER-QUEUE.md"

# Primary: <!-- work_jiang.context.yaml WORK_JIANG_CONTEXT_V1 --> ... <!-- /work_jiang.context.yaml WORK_JIANG_CONTEXT_V1 -->
_INSTANCE_CONTEXT_V1_RE = re.compile(
    r"<!--\s*work_jiang\.context\.yaml\s+WORK_JIANG_CONTEXT_V1\s*-->\s*```yaml\s*\n(.*?)```\s*<!--\s*/work_jiang\.context\.yaml\s+WORK_JIANG_CONTEXT_V1\s*-->",
    re.DOTALL | re.IGNORECASE,
)
# Legacy fenced blocks (older work-jiang.md shapes)
_LEGACY_HEARTBEAT_RE = re.compile(
    r"<!--\s*WORK-JIANG-HEARTBEAT-START\s*-->\s*```yaml\s*\n(.*?)```\s*<!--\s*WORK-JIANG-HEARTBEAT-END\s*-->",
    re.DOTALL | re.IGNORECASE,
)
_LEGACY_CONTAINER_RE = re.compile(
    r"<!--\s*WORK-JIANG-CONTAINER-START\s*-->\s*```yaml\s*\n(.*?)```\s*<!--\s*WORK-JIANG-CONTAINER-END\s*-->",
    re.DOTALL | re.IGNORECASE,
)

DEFAULT_MORNING_SPARKS = [
    "What is the single sharpest claim you could defend from yesterday's corpus work—in one sentence?",
    "Open the first chapter in CHAPTER-QUEUE: what is the smallest next action you could ship in 25 minutes?",
    "Name one tension between two lecture series (Geo-Strategy vs Civilization) worth a footnote someday.",
    "If a skeptical editor challenged one Jiang thesis today, which claim would you pick to defend first?",
]

DEFAULT_NIGHT_SPARKS = [
    "Name one concrete thing that moved Predictive History forward today (file, validator, note—anything).",
    "What should the next session open on in the Jiang lane—one line?",
    "One sentence you're glad is documented somewhere in research/external/work-jiang/ tonight.",
]


def _load_yaml_sparks() -> tuple[list[str], list[str]]:
    morning, night = list(DEFAULT_MORNING_SPARKS), list(DEFAULT_NIGHT_SPARKS)
    if not SPARKS_PATH.is_file():
        return morning, night
    try:
        import yaml

        data = yaml.safe_load(SPARKS_PATH.read_text(encoding="utf-8")) or {}
        m = data.get("morning") or []
        n = data.get("night") or []
        if isinstance(m, list) and all(isinstance(x, str) and x.strip() for x in m):
            morning = [x.strip() for x in m]
        if isinstance(n, list) and all(isinstance(x, str) and x.strip() for x in n):
            night = [x.strip() for x in n]
    except Exception:
        pass
    return morning, night


def _ordinal_day() -> int:
    return datetime.now(timezone.utc).timetuple().tm_yday


def _pick_spark(lines: list[str]) -> str:
    if not lines:
        return ""
    return lines[_ordinal_day() % len(lines)]


def _parse_instance_work_context_yaml(work_jiang_md: str) -> dict[str, str]:
    m = (
        _INSTANCE_CONTEXT_V1_RE.search(work_jiang_md)
        or _LEGACY_HEARTBEAT_RE.search(work_jiang_md)
        or _LEGACY_CONTAINER_RE.search(work_jiang_md)
    )
    if not m:
        return {}
    raw = m.group(1).strip()
    out: dict[str, str] = {}
    for key in ("status", "edge", "notes"):
        km = re.search(rf"^{key}:\s*(.+)$", raw, re.MULTILINE)
        if km:
            val = km.group(1).strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            out[key] = val[:220]
    return out


def _first_status_next_action(status_md: str) -> str:
    if "## Next actions" not in status_md:
        return ""
    tail = status_md.split("## Next actions", 1)[1]
    for line in tail.splitlines():
        m = re.match(r"^\s*\d+\.\s+(.+)$", line)
        if m:
            return m.group(1).strip()[:200]
    return ""


def _first_chapter_next_action(queue_md: str) -> tuple[str, str]:
    """Return (chapter_id, next_action) from first ## chNN block."""
    parts = re.split(r"^##\s+(ch\d+)\s", queue_md, maxsplit=1, flags=re.MULTILINE)
    if len(parts) < 3:
        return "", ""
    cid = parts[1]
    block = parts[2].split("##", 1)[0]
    m = re.search(r"\*\*Next action:\*\*\s*(.+)$", block, re.MULTILINE)
    action = m.group(1).strip()[:200] if m else ""
    return cid, action


def _corpus_oneliner(status_md: str) -> str:
    """First bullet under ## Corpus if present."""
    if "## Corpus" not in status_md:
        return ""
    tail = status_md.split("## Corpus", 1)[1].split("##", 1)[0]
    for line in tail.splitlines():
        s = line.strip()
        if s.startswith("- "):
            return s[2:].strip()[:180]
    return ""


def build_morning_pulse_lines(user_id: str) -> list[str]:
    profile = ROOT / "users" / user_id / "work-jiang.md"
    wj = profile.read_text(encoding="utf-8") if profile.is_file() else ""
    ctx = _parse_instance_work_context_yaml(wj)
    status = STATUS_PATH.read_text(encoding="utf-8") if STATUS_PATH.is_file() else ""
    queue = CHAPTER_QUEUE_PATH.read_text(encoding="utf-8") if CHAPTER_QUEUE_PATH.is_file() else ""

    morning_sparks, _ = _load_yaml_sparks()
    spark = _pick_spark(morning_sparks)

    next_status = _first_status_next_action(status)
    ch_id, ch_next = _first_chapter_next_action(queue)
    corpus = _corpus_oneliner(status)

    lines = [
        "## Predictive History — morning momentum",
        "",
        "_Operator lane — not Voice knowledge until merged through the gate._",
        "",
    ]
    if ctx.get("status"):
        edge = ctx.get("edge", "")
        lines.append(
            f"- **Instance context:** `{ctx['status']}`" + (f" — {edge}" if edge else "")
        )
    else:
        lines.append(
            "- **Instance context:** (add `## Instance work context (YAML)` with "
            "`work_jiang.context.yaml` / `WORK_JIANG_CONTEXT_V1` markers in "
            "`users/{0}/work-jiang.md`)".format(user_id)
        )
    if ctx.get("notes"):
        lines.append(f"- **Notes:** {ctx['notes']}")
    if corpus:
        lines.append(f"- **Corpus snapshot:** {corpus}")
    if next_status:
        lines.append(f"- **Production nudge (STATUS):** {next_status}")
    if ch_id and ch_next:
        lines.append(f"- **Chapter front ({ch_id}):** {ch_next}")
    if spark:
        lines.append(f"- **Spark:** {spark}")
    lines.extend(
        [
            "",
            f"- **Dive:** [`research/external/work-jiang/README.md`](research/external/work-jiang/README.md) · "
            f"verify block in `.cursor/skills/work-jiang-feature-checklist/SKILL.md` after metadata edits.",
            "",
        ]
    )
    return lines


def build_night_pulse_lines(user_id: str) -> list[str]:
    profile = ROOT / "users" / user_id / "work-jiang.md"
    wj = profile.read_text(encoding="utf-8") if profile.is_file() else ""
    ctx = _parse_instance_work_context_yaml(wj)
    status = STATUS_PATH.read_text(encoding="utf-8") if STATUS_PATH.is_file() else ""
    queue = CHAPTER_QUEUE_PATH.read_text(encoding="utf-8") if CHAPTER_QUEUE_PATH.is_file() else ""

    _, night_sparks = _load_yaml_sparks()
    spark = _pick_spark(night_sparks)

    next_status = _first_status_next_action(status)
    ch_id, ch_next = _first_chapter_next_action(queue)

    lines = [
        "## Predictive History — night closeout",
        "",
        "_Same membrane: research lane only; no merge in this workflow._",
        "",
    ]
    if ctx.get("status"):
        lines.append(f"- **Where the lane rests:** `{ctx['status']}`")
    if next_status or (ch_id and ch_next):
        lever = next_status or f"{ch_id}: {ch_next}"
        lines.append(f"- **Tomorrow's first lever (suggested):** {lever}")
    else:
        lines.append("- **Tomorrow's first lever:** skim `STATUS.md` or `CHAPTER-QUEUE.md` and pick one line to execute.")
    if spark:
        lines.append(f"- **Spark:** {spark}")
    lines.append(
        f"- **Quick win ritual:** `python3 scripts/work_jiang/rebuild_all.py` if you touched metadata today "
        f"(CI-shaped confidence before sleep)."
    )
    lines.append("")
    return lines


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("-u", "--user", default="grace-mar", help="Fork id under users/")
    p.add_argument("--morning", action="store_true", help="Print morning block only")
    p.add_argument("--night", action="store_true", help="Print night block only")
    args = p.parse_args()
    uid = (args.user or "grace-mar").strip()
    if args.morning and args.night:
        print("\n".join(build_morning_pulse_lines(uid)))
        print()
        print("\n".join(build_night_pulse_lines(uid)))
    elif args.night:
        print("\n".join(build_night_pulse_lines(uid)))
    else:
        print("\n".join(build_morning_pulse_lines(uid)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
