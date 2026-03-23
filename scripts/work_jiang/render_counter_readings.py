"""Render COUNTER-READINGS.md from counter-readings/registry/counter-readings.jsonl."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
REG = WORK_DIR / "counter-readings" / "registry" / "counter-readings.jsonl"
OUT = WORK_DIR / "COUNTER-READINGS.md"


def load_rows() -> list[dict]:
    rows = []
    with REG.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> int:
    rows = load_rows()
    lines = [
        "# Counter-readings — work-jiang",
        "",
        "Rival frameworks paired with thesis, chapters, claims, and concepts. Not canonical Record; research scaffolding.",
        "",
        f"**Rows:** {len(rows)}",
        "",
    ]
    for r in sorted(rows, key=lambda x: x.get("counter_id") or ""):
        cid = r.get("counter_id")
        tt = r.get("target_type")
        tid = r.get("target_id")
        fw = r.get("framework") or ""
        cl = r.get("claim") or ""
        sb = r.get("source_basis") or ""
        st = r.get("strength") or ""
        stat = r.get("status") or ""
        notes = (r.get("notes") or "").strip()
        lines.append(f"## `{cid}` — {tt} `{tid}`")
        lines.append("")
        lines.append(f"- **Framework:** {fw}")
        lines.append(f"- **Counter-claim:** {cl}")
        lines.append(f"- **Source basis:** {sb}")
        lines.append(f"- **Strength:** {st} · **Status:** {stat}")
        if notes:
            lines.append(f"- **Notes:** {notes}")
        lines.append("")

    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
