#!/usr/bin/env python3
"""
Measure cognitive growth rate and cognitive density of the fork.

Uses SELF.md, EVIDENCE.md, and optionally git history.

Growth rate:
  - IX entries per day (from date: fields in SELF.md)
  - Pipeline throughput (applied events per week, if PIPELINE-EVENTS.jsonl exists)
  - Optional: IX accumulation over time from git history

Cognitive density:
  - Words per IX entry (elaboration)
  - Evidence backing (% of IX entries with evidence_id or curated_by)
  - Topic diversity (unique concepts / total entries)
  - Channel balance (IX-A : IX-B : IX-C)
"""

import json
import re
import subprocess
from collections import defaultdict
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROFILE_DIR = REPO_ROOT / "users" / "pilot-001"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def parse_ix_entries(content: str) -> list[dict]:
    """Extract IX entries (LEARN, CUR, PER) with date, topic/observation, evidence_id."""
    entries = []

    def add_entry(prefix: str, eid: str, date: str, text: str, block: str) -> None:
        channel = "A" if prefix == "LEARN" else ("B" if prefix == "CUR" else "C")
        words = len(re.findall(r"\w+", text))
        her_m = re.search(r'her_understanding:\s*["\']([^"\']+)["\']', block)
        if her_m:
            words += len(re.findall(r"\w+", her_m.group(1)))
        entries.append({
            "id": eid,
            "date": date,
            "channel": channel,
            "topic": text[:120],
            "word_count": max(words, 1),
            "has_evidence": "evidence_id:" in block,
            "curated": "curated_by:" in block,
        })

    for prefix in ("LEARN", "CUR"):
        pattern = rf'id:\s+{prefix}-(\d+).*?date:\s*(\d{{4}}-\d{{2}}-\d{{2}}).*?topic:\s*["\']([^"\']+)["\']'
        for m in re.finditer(pattern, content, re.DOTALL):
            block = content[m.start() : m.start() + 1200]
            add_entry(prefix, f"{prefix}-{m.group(1)}", m.group(2), m.group(3), block)

    pattern = r'id:\s+PER-(\d+).*?date:\s*(\d{4}-\d{2}-\d{2}).*?observation:\s*["\']([^"\']+)["\']'
    for m in re.finditer(pattern, content, re.DOTALL):
        block = content[m.start() : m.start() + 800]
        add_entry("PER", f"PER-{m.group(1)}", m.group(2), m.group(3), block)

    return entries


def pipeline_throughput(events_path: Path) -> dict:
    """Count applied events per week from PIPELINE-EVENTS.jsonl."""
    if not events_path.exists():
        return {}
    by_week: dict[str, int] = defaultdict(int)
    for line in events_path.read_text().strip().splitlines():
        if not line:
            continue
        try:
            row = json.loads(line)
            if row.get("event") in ("applied", "approved"):
                ts = row.get("ts", "")
                if ts:
                    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    week = dt.strftime("%Y-W%W")
                    by_week[week] += 1
        except (json.JSONDecodeError, ValueError):
            pass
    return dict(by_week)


def growth_from_git(self_path: Path) -> list[tuple[str, int, int, int]]:
    """Get (commit_date, ix_a, ix_b, ix_c) from git history. Returns empty if not a git repo."""
    try:
        result = subprocess.run(
            ["git", "log", "--format=%H %ai", "--", str(self_path)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode != 0:
            return []
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []
    history = []
    seen = set()
    for line in result.stdout.strip().splitlines():
        parts = line.split(maxsplit=2)
        if len(parts) < 3:
            continue
        commit, date_str = parts[0], parts[1]
        if commit in seen:
            continue
        seen.add(commit)
        try:
            show = subprocess.run(
                ["git", "show", f"{commit}:users/pilot-001/SELF.md"],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=5,
            )
            if show.returncode != 0:
                continue
            content = show.stdout
            a = len(re.findall(r"id:\s+LEARN-\d+", content))
            b = len(re.findall(r"id:\s+CUR-\d+", content))
            c = len(re.findall(r"id:\s+PER-\d+", content))
            history.append((date_str[:10], a, b, c))
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            continue
    return history[:20]  # limit to recent commits


def main() -> None:
    self_path = PROFILE_DIR / "SELF.md"
    evidence_path = PROFILE_DIR / "EVIDENCE.md"
    events_path = PROFILE_DIR / "PIPELINE-EVENTS.jsonl"

    content = _read(self_path)
    entries = parse_ix_entries(content)

    if not entries:
        print("No IX entries found in SELF.md")
        return

    # Growth rate from dates
    dates = [e["date"] for e in entries]
    if dates:
        min_d, max_d = min(dates), max(dates)
        try:
            d_min = datetime.strptime(min_d, "%Y-%m-%d")
            d_max = datetime.strptime(max_d, "%Y-%m-%d")
            span_days = max((d_max - d_min).days, 1)
            entries_per_day = len(entries) / span_days
        except ValueError:
            span_days = 1
            entries_per_day = len(entries)
    else:
        span_days = 0
        entries_per_day = 0

    # Pipeline throughput
    by_week = pipeline_throughput(events_path)

    # Density
    total_words = sum(e["word_count"] for e in entries)
    avg_words = total_words / len(entries)
    with_evidence = sum(1 for e in entries if e["has_evidence"] or e["curated"])
    evidence_pct = 100 * with_evidence / len(entries)
    topics = [e["topic"].lower() for e in entries]
    all_words = re.findall(r"\w+", " ".join(topics))
    unique_words = len(set(all_words))
    diversity = unique_words / len(all_words) if all_words else 0
    by_channel = defaultdict(int)
    for e in entries:
        by_channel[e["channel"]] += 1
    a, b, c = by_channel["A"], by_channel["B"], by_channel["C"]
    total_ix = a + b + c
    balance = f"{a}:{b}:{c}" if total_ix else "—"

    # Git history (optional)
    git_history = growth_from_git(self_path)

    print("Cognitive Growth & Density")
    print("=" * 50)
    print("\nGrowth rate")
    print("-" * 30)
    print(f"IX entries:           {len(entries)} total")
    print(f"Date span:            {min_d} to {max_d} ({span_days} days)")
    print(f"Entries per day:      {entries_per_day:.2f}")
    if by_week:
        recent = sorted(by_week.items(), reverse=True)[:4]
        print(f"Pipeline (applied/wk): {dict(recent)}")
    else:
        print("Pipeline:             (no PIPELINE-EVENTS.jsonl)")
    if git_history:
        first = git_history[-1]
        last = git_history[0]
        delta = (last[1] + last[2] + last[3]) - (first[1] + first[2] + first[3])
        print(f"Git history:          {first[0]} → {last[0]}, ΔIX = {delta}")

    print("\nCognitive density")
    print("-" * 30)
    print(f"Words per entry:      {avg_words:.1f} avg")
    print(f"Evidence backing:     {with_evidence}/{len(entries)} ({evidence_pct:.0f}%)")
    print(f"Topic diversity:      {diversity:.2f} (unique/total words)")
    print(f"Channel balance:      IX-A:IX-B:IX-C = {balance}")

    print()


if __name__ == "__main__":
    main()
