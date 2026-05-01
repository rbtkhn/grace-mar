#!/usr/bin/env python3
"""Export local continuity-block events into a derived WORK artifact."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_INPUT = REPO_ROOT / "runtime" / "observability" / "continuity_blocks.jsonl"
DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "work-dev" / "continuity-observability" / "continuity-blocks.md"


def _repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


def load_events(path: Path) -> tuple[list[dict[str, Any]], int]:
    """Return valid continuity block events plus invalid line count."""
    if not path.is_file():
        return [], 0

    events: list[dict[str, Any]] = []
    invalid = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw:
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            invalid += 1
            continue
        if isinstance(obj, dict) and obj.get("event") == "continuity_block":
            events.append(obj)
        else:
            invalid += 1
    return events, invalid


def summarize_events(events: list[dict[str, Any]]) -> dict[str, Counter[str]]:
    return {
        "reason": Counter(str(e.get("reason") or "unknown") for e in events),
        "source": Counter(str(e.get("source") or "unknown") for e in events),
        "user_id": Counter(str(e.get("user_id") or "unknown") for e in events),
    }


def render_markdown(
    events: list[dict[str, Any]],
    *,
    invalid_lines: int,
    input_path: Path,
    repo_root: Path,
    generated_at: str | None = None,
) -> str:
    generated_at = generated_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    summary = summarize_events(events)
    lines = [
        "<!-- GENERATED FILE — do not edit by hand. Source: scripts/work_dev/export_continuity_blocks.py -->\n\n",
        "# Continuity Block Observability\n\n",
        "**Status:** WORK-derived operator artifact. **Not** Record. **Not** EVIDENCE. **Gate effect:** none.\n\n",
        f"- Generated: `{generated_at}`\n",
        f"- Source feed: `{_repo_rel(input_path, repo_root)}`\n",
        f"- Continuity block events: `{len(events)}`\n",
        f"- Invalid / ignored lines: `{invalid_lines}`\n\n",
    ]

    if not events:
        lines.append("No continuity block events were observed in the local feed.\n")
        return "".join(lines)

    lines.append("## By Reason\n\n")
    for reason, count in summary["reason"].most_common():
        lines.append(f"- `{reason}`: {count}\n")

    lines.append("\n## By Source\n\n")
    for source, count in summary["source"].most_common():
        lines.append(f"- `{source}`: {count}\n")

    lines.append("\n## Recent Events\n\n")
    lines.append("| ts | user_id | source | reason |\n")
    lines.append("|---|---|---|---|\n")
    for event in events[-10:]:
        ts = str(event.get("ts") or "")
        user_id = str(event.get("user_id") or "")
        source = str(event.get("source") or "")
        reason = str(event.get("reason") or "").replace("|", "\\|")
        lines.append(f"| `{ts}` | `{user_id}` | `{source}` | {reason} |\n")
    return "".join(lines)


def export_continuity_blocks(input_path: Path, output_path: Path, *, repo_root: Path = REPO_ROOT) -> str:
    events, invalid = load_events(input_path)
    markdown = render_markdown(events, invalid_lines=invalid, input_path=input_path, repo_root=repo_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    return markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Export continuity-block JSONL into a derived WORK artifact.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    export_continuity_blocks(args.input, args.output)
    print(f"export_continuity_blocks: OK -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
