#!/usr/bin/env python3
"""
Staleness scorer for RECURSION-GATE pending candidates.

For each pending candidate, reports wall-clock age, active-day-adjusted age
(days with cadence events since the candidate was staged), superseded-by-merge
hints, and warrant-drift flags.

Read-only operator tooling — no Record writes, no gate merges.  Optionally
annotates the gate file with blockquote lines (same pattern as
score_gate_candidates.py); use --dry-run to preview without writing.

Usage:
  python scripts/score_gate_staleness.py -u grace-mar --dry-run
  python scripts/score_gate_staleness.py -u grace-mar
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from gate_block_parser import iter_candidate_yaml_blocks, split_gate_sections  # noqa: E402
from repo_io import fork_root, read_path, REPO_ROOT  # noqa: E402

_STOPWORDS = frozenset(
    "the a an is are was were be been being have has had do does did will would "
    "shall should may might can could this that these those with from into for "
    "and but not".split()
)

_TIME_SENSITIVE_RE = re.compile(
    r"\b(current|while|assumes|until|temporary|right now|at this stage|for now)\b",
    re.IGNORECASE,
)

EVENTS_PATH = REPO_ROOT / "docs" / "skill-work" / "work-cadence" / "work-cadence-events.md"

_EVENT_LINE_RE = re.compile(
    r"- \*\*(\d{4}-\d{2}-\d{2}) \d{2}:\d{2} UTC\*\* — (\w+) \(([^)]+)\)"
)


def _yaml_get(yaml_body: str, key: str) -> str:
    m = re.search(rf'^{key}:\s*"?(.+?)"?\s*$', yaml_body, re.MULTILINE)
    return m.group(1).strip().strip('"') if m else ""


def _tokenize(text: str) -> set[str]:
    return {
        t
        for t in re.findall(r"[a-z0-9]+", (text or "").lower())
        if len(t) >= 4 and t not in _STOPWORDS
    }


def parse_cadence_active_days(user_id: str, since: datetime) -> int:
    """Count distinct calendar days with at least one cadence event for user_id since `since`."""
    if not EVENTS_PATH.is_file():
        return 0
    since_date = since.date()
    days: set[str] = set()
    for line in EVENTS_PATH.read_text(encoding="utf-8").splitlines():
        m = _EVENT_LINE_RE.match(line.strip())
        if not m:
            continue
        date_str, _kind, user = m.group(1), m.group(2), m.group(3)
        if user.strip() != user_id:
            continue
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            continue
        if d >= since_date:
            days.add(date_str)
    return len(days)


def _parse_ix_entries_since(self_content: str, since: datetime) -> list[tuple[str, set[str]]]:
    """Extract (entry_id, token_set) for IX entries with date >= since."""
    entries: list[tuple[str, set[str]]] = []
    since_str = since.strftime("%Y-%m-%d")
    for m in re.finditer(
        r"- id:\s*((?:LEARN|CUR|PER)-\d+).*?(?=\n  - id:|\n##|\Z)",
        self_content,
        re.DOTALL,
    ):
        block = m.group(0)
        entry_id = m.group(1)
        date_m = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", block)
        if not date_m:
            continue
        if date_m.group(1) < since_str:
            continue
        topic = re.search(r'topic:\s*"?(.+?)"?\s*$', block, re.MULTILINE)
        tokens = _tokenize(topic.group(1) if topic else block)
        entries.append((entry_id, tokens))
    return entries


def score_candidate(
    cid: str,
    yaml_body: str,
    self_content: str,
    user_id: str,
    now: datetime,
) -> dict:
    ts_str = _yaml_get(yaml_body, "timestamp")
    try:
        ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        ts = now
    wall_days = (now - ts).days
    active_days = parse_cadence_active_days(user_id, ts)

    suggested = _yaml_get(yaml_body, "suggested_entry")
    summary = _yaml_get(yaml_body, "summary")
    candidate_tokens = _tokenize(f"{suggested} {summary}")
    superseded_by: list[str] = []
    if candidate_tokens:
        for entry_id, entry_tokens in _parse_ix_entries_since(self_content, ts):
            overlap = candidate_tokens & entry_tokens
            if len(overlap) >= 3:
                superseded_by.append(entry_id)

    warrant = _yaml_get(yaml_body, "warrant")
    warrant_drift = bool(warrant and _TIME_SENSITIVE_RE.search(warrant))

    return {
        "candidate_id": cid,
        "wall_days": wall_days,
        "active_days": active_days,
        "superseded_by": superseded_by,
        "warrant_drift": warrant_drift,
        "warrant_text": warrant,
    }


def format_staleness_line(r: dict) -> str:
    parts = [f"{r['wall_days']}d wall / {r['active_days']}d active"]
    if r["superseded_by"]:
        parts.append(f"possibly superseded by {', '.join(r['superseded_by'][:3])}")
    if r["warrant_drift"]:
        snippet = r["warrant_text"][:60]
        parts.append(f'warrant references "{snippet}"')
    return f"> **Staleness**: {' · '.join(parts)}\n"


_CANDIDATE_BLOCK_RE = re.compile(
    r"(### CANDIDATE-\d+[^\n]*\n)\s*(?:> \*\*Staleness\*\*[^\n]*\n\s*)?(```yaml\n.*?```)",
    re.DOTALL,
)


def annotate_active_section(
    active: str,
    results: dict[str, dict],
) -> tuple[str, int]:
    scored = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal scored
        heading = m.group(1)
        fence = m.group(2)
        cid_m = re.match(r"### (CANDIDATE-\d+)", heading)
        if not cid_m:
            return m.group(0)
        cid = cid_m.group(1)
        if cid not in results:
            return m.group(0)
        line = format_staleness_line(results[cid])
        scored += 1
        return heading + line + fence

    new_active = _CANDIDATE_BLOCK_RE.sub(repl, active)
    return new_active, scored


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Staleness scorer for pending RECURSION-GATE candidates."
    )
    ap.add_argument("-u", "--user", default="grace-mar", help="Fork id under users/")
    ap.add_argument("--dry-run", action="store_true", help="Print preview; do not write")
    args = ap.parse_args()

    user_id = args.user
    gate_path = fork_root(user_id) / "recursion-gate.md"
    self_path = fork_root(user_id) / "self.md"

    if not gate_path.is_file():
        print(f"No recursion-gate.md at {gate_path}", file=sys.stderr)
        return 1

    gate_content = read_path(gate_path)
    self_content = read_path(self_path)
    active, _processed = split_gate_sections(gate_content)
    now = datetime.now(timezone.utc)

    results: dict[str, dict] = {}
    for cid, _title, yaml_body in iter_candidate_yaml_blocks(active):
        status = _yaml_get(yaml_body, "status").lower()
        if status and status != "pending":
            continue
        results[cid] = score_candidate(cid, yaml_body, self_content, user_id, now)

    if not results:
        print("No pending candidates found.")
        return 0

    for cid, r in results.items():
        print(f"{cid}: {format_staleness_line(r).strip()}")

    if args.dry_run:
        print(f"\n[dry-run] Would annotate {len(results)} candidate(s) in {gate_path}")
        return 0

    marker = re.search(r"^## Processed\s*$", gate_content, re.MULTILINE)
    if marker:
        tail = gate_content[marker.start():]
        new_active, n = annotate_active_section(active, results)
        new_full = new_active + tail
    else:
        new_active, n = annotate_active_section(gate_content, results)
        new_full = new_active

    gate_path.write_text(new_full, encoding="utf-8")
    print(f"\nUpdated {gate_path} — annotated {n} candidate(s) with staleness data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
