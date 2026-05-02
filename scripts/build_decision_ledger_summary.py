#!/usr/bin/env python3
"""Build a derived summary from the work-dev decision ledger."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LEDGER = REPO_ROOT / "docs" / "skill-work" / "work-dev" / "decision-ledger.md"
DEFAULT_OUTPUT = REPO_ROOT / "artifacts" / "work-dev" / "decision-ledger-summary.md"


@dataclass(frozen=True)
class DecisionRow:
    decision_id: str
    status: str
    decision: str
    rationale: str
    affected_surfaces: str
    source_receipt: str
    revisit_trigger: str


def _split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped.strip("|").split("|")]


def parse_decisions(text: str) -> list[DecisionRow]:
    rows: list[DecisionRow] = []
    in_decisions = False
    for line in text.splitlines():
        if line.strip() == "## Decisions":
            in_decisions = True
            continue
        if in_decisions and line.startswith("## "):
            break
        if not in_decisions:
            continue
        cells = _split_table_row(line)
        if len(cells) != 7:
            continue
        if cells[0] in {"Decision ID", "-------------"}:
            continue
        if set(cells[0]) <= {"-"}:
            continue
        rows.append(DecisionRow(*cells))
    return rows


def render_summary(rows: list[DecisionRow], *, generated_at: str) -> str:
    active = [row for row in rows if row.status == "active"]
    watch = [row for row in rows if row.status in {"watch", "revisit"}]
    retired = [row for row in rows if row.status == "retired"]

    lines = [
        "# Decision Ledger Summary",
        "",
        "**Derived artifact.** Source: `docs/skill-work/work-dev/decision-ledger.md`. Not Record authority.",
        "",
        f"Generated: {generated_at}",
        "",
        "## Counts",
        "",
        f"- Active: {len(active)}",
        f"- Watch / revisit: {len(watch)}",
        f"- Retired: {len(retired)}",
        f"- Total: {len(rows)}",
        "",
        "## Active Decisions",
        "",
    ]
    if active:
        for row in active:
            lines.append(f"- **{row.decision_id}:** {row.decision}")
            lines.append(f"  - Revisit: {row.revisit_trigger}")
    else:
        lines.append("- None.")

    lines.extend(["", "## Watch / Revisit", ""])
    if watch:
        for row in watch:
            lines.append(f"- **{row.decision_id}:** {row.decision}")
            lines.append(f"  - Trigger: {row.revisit_trigger}")
    else:
        lines.append("- None.")

    lines.extend(["", "## Recent Source Receipts", ""])
    for row in rows[-5:]:
        lines.append(f"- **{row.decision_id}:** {row.source_receipt}")
    if not rows:
        lines.append("- None.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    text = DEFAULT_LEDGER.read_text(encoding="utf-8")
    rows = parse_decisions(text)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    DEFAULT_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUTPUT.write_text(render_summary(rows, generated_at=generated_at), encoding="utf-8")
    print(f"wrote {DEFAULT_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
