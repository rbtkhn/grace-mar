"""Render INTELLECTUAL-CHRONOLOGY.md from metadata/chronology.yaml (read-only)."""
from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
CHRONO = WORK_DIR / "metadata" / "chronology.yaml"
OUT = WORK_DIR / "INTELLECTUAL-CHRONOLOGY.md"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main() -> int:
    doc = load_yaml(CHRONO)
    periods = doc.get("periods") or []
    lines = [
        "# Intellectual chronology — work-jiang",
        "",
        "Hand-curated periods over the Geo-Strategy lecture arc. Sources `geo-01` … `geo-12` are partitioned below.",
        "",
    ]
    for p in periods:
        pid = p.get("period_id")
        label = p.get("label") or ""
        lines.append(f"## `{pid}` — {label}")
        lines.append("")
        src = p.get("source_ids") or []
        lines.append(f"- **Sources:** {', '.join(f'`{s}`' for s in src)}")
        dc = p.get("dominant_concepts") or []
        lines.append(f"- **Dominant concepts:** {', '.join(f'`{c}`' for c in dc)}")
        dq = p.get("dominant_claims") or []
        lines.append(f"- **Dominant claims:** {', '.join(f'`{c}`' for c in dq)}")
        lines.append("- **Shifts:**")
        for x in p.get("shifts") or []:
            lines.append(f"  - {x}")
        lines.append("- **Continuities:**")
        for x in p.get("continuities") or []:
            lines.append(f"  - {x}")
        if p.get("tensions"):
            lines.append("- **Tensions:**")
            for x in p.get("tensions") or []:
                lines.append(f"  - {x}")
        ch = p.get("chapter_ids") or []
        if ch:
            lines.append(f"- **Chapter hooks:** {', '.join(f'`{c}`' for c in ch)}")
        note = (p.get("notes") or "").strip()
        if note:
            lines.append(f"- **Notes:** {note}")
        lines.append("")

    OUT.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
