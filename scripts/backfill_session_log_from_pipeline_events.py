#!/usr/bin/env python3
"""
Append missing ## Pipeline merge (automated) lines to users/<id>/session-log.md
from pipeline-events.jsonl "applied" events.

Matches the line format produced by process_approved_candidates._append_session_log_for_merge:
  - {ts} | pipeline merge | {candidate_id} | approved by {actor}

Dedupes:
  - One line per candidate_id (first applied timestamp wins if duplicates in JSONL).
  - Skips candidate_ids already present in an existing pipeline-merge line.

Usage (repo root):
  python3 scripts/backfill_session_log_from_pipeline_events.py -u grace-mar
  python3 scripts/backfill_session_log_from_pipeline_events.py -u grace-mar --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
_SCRIPTS = REPO_ROOT / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from repo_io import profile_dir  # noqa: E402

SECTION = "## Pipeline merge (automated)"
# Optional footer at end of session-log.md (insert pipeline section before it)
END_FILE_FOOTER_RE = re.compile(r"(\n---\s*\n\nEND OF FILE[^\n]*\n?)\s*\Z", re.MULTILINE)

# Lines written by process_approved_candidates._append_session_log_for_merge
MERGE_LINE_RE = re.compile(
    r"^-\s+(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+\|\s+pipeline merge\s+\|\s+"
    r"(?P<cid>CANDIDATE-\d+)\s+\|\s+approved by\s+(?P<actor>.+)\s*$",
    re.IGNORECASE,
)


def _parse_ts(iso_ts: str) -> datetime:
    s = iso_ts.strip()
    if s.endswith("Z"):
        s = s[:-1]
    return datetime.fromisoformat(s)


def _format_ts(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def _read_applied_events(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get("event") != "applied":
            continue
        cid = obj.get("candidate_id")
        if not cid or not str(cid).upper().startswith("CANDIDATE-"):
            continue
        out.append(obj)
    return out


def _dedupe_applied_by_candidate(events: list[dict]) -> dict[str, dict]:
    """Keep earliest applied event per candidate_id (by ts)."""
    best: dict[str, tuple[datetime, dict]] = {}
    for e in events:
        cid = str(e["candidate_id"]).strip()
        try:
            dt = _parse_ts(str(e["ts"]))
        except (TypeError, ValueError):
            continue
        prev = best.get(cid)
        if prev is None or dt < prev[0]:
            best[cid] = (dt, e)
    return {cid: pair[1] for cid, pair in best.items()}


def _existing_merge_candidate_ids(session_text: str) -> set[str]:
    found: set[str] = set()
    in_section = False
    for line in session_text.splitlines():
        if line.strip() == SECTION:
            in_section = True
            continue
        if in_section:
            if line.startswith("## ") and SECTION not in line:
                break
            m = MERGE_LINE_RE.match(line.strip())
            if m:
                found.add(m.group("cid").upper())
    return found


def _build_merge_line(e: dict) -> str:
    dt = _parse_ts(str(e["ts"]))
    ts = _format_ts(dt)
    cid = str(e["candidate_id"]).strip()
    actor = (e.get("actor") or "").strip() or "operator"
    return f"- {ts} | pipeline merge | {cid} | approved by {actor}"


def _strip_footer(text: str) -> tuple[str, str]:
    m = END_FILE_FOOTER_RE.search(text)
    if not m:
        return text, ""
    return text[: m.start()], m.group(1)


def _ensure_section_and_append(existing: str, new_lines: list[str]) -> str:
    """Insert SECTION + bullets before END OF FILE footer if present; else append."""
    block = "\n".join(new_lines) + "\n"
    body, footer = _strip_footer(existing)

    if not body.strip():
        core = f"# SESSION LOG\n\n{SECTION}\n\n{block}"
        return core + footer

    if SECTION not in body:
        core = body.rstrip() + f"\n\n{SECTION}\n\n{block}"
        return core + footer

    # Same as process_approved_candidates: append merge lines at end of body (before footer).
    core = body.rstrip() + "\n" + block
    return core + footer


def run(user_id: str, *, apply: bool, events_path: Path | None) -> int:
    root = profile_dir(user_id)
    session_path = root / "session-log.md"
    pipe_path = events_path or (root / "pipeline-events.jsonl")

    applied = _read_applied_events(pipe_path)
    by_cand = _dedupe_applied_by_candidate(applied)

    session_text = session_path.read_text(encoding="utf-8") if session_path.is_file() else ""
    already = _existing_merge_candidate_ids(session_text)

    to_add: list[tuple[datetime, str]] = []
    for cid, e in sorted(by_cand.items(), key=lambda x: _parse_ts(str(x[1]["ts"]))):
        if cid.upper() in already:
            continue
        try:
            dt = _parse_ts(str(e["ts"]))
        except (TypeError, ValueError):
            continue
        to_add.append((dt, _build_merge_line(e)))

    to_add.sort(key=lambda x: x[0])
    new_lines = [ln for _, ln in to_add]

    if not new_lines:
        print("No new pipeline-merge lines to append (all applied candidates already logged or no applied events).")
        return 0

    print(f"Would append {len(new_lines)} line(s) under '{SECTION}' in {session_path}:")
    for ln in new_lines:
        print(f"  {ln}")

    if not apply:
        print("\nDry run only. Pass --apply to write.")
        return 0

    new_body = _ensure_section_and_append(session_text, new_lines)
    session_path.write_text(new_body, encoding="utf-8")
    print(f"\nWrote {session_path}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("-u", "--user", default="grace-mar", help="Fork id under users/")
    p.add_argument(
        "--events",
        type=Path,
        default=None,
        help="Override path to pipeline-events.jsonl (default: users/<id>/pipeline-events.jsonl)",
    )
    p.add_argument(
        "--apply",
        action="store_true",
        help="Write session-log.md; default is dry-run.",
    )
    args = p.parse_args()
    uid = str(args.user).strip() or "grace-mar"
    ev = args.events
    if ev is not None and not ev.is_absolute():
        ev = (REPO_ROOT / ev).resolve()
    return run(uid, apply=bool(args.apply), events_path=ev)


if __name__ == "__main__":
    raise SystemExit(main())
