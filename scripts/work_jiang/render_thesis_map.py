"""Render THESIS-MAP.md from metadata/thesis-map.yaml."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
WORK_DIR = ROOT / "research" / "external" / "work-jiang"
META = WORK_DIR / "metadata" / "thesis-map.yaml"
OUT = WORK_DIR / "THESIS-MAP.md"


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate(data: dict) -> list[str]:
    errors: list[str] = []
    thesis = data.get("thesis") or {}
    if not thesis.get("master_claim"):
        errors.append("thesis.master_claim is required")
    if not thesis.get("subclaims"):
        errors.append("thesis.subclaims must contain at least one subclaim")
    return errors


def render(data: dict) -> str:
    t = data["thesis"]
    lines = [
        "# THESIS MAP",
        "",
        "## Master claim",
        "",
        t["master_claim"],
        "",
        "## Subclaims",
        "",
    ]
    for sc in t.get("subclaims") or []:
        lines.append(f"### {sc.get('id')} — {sc.get('claim', '')}")
        lines.append("")
        lc = sc.get("linked_claim_ids") or []
        if lc:
            lines.append(f"- **Linked claims:** {', '.join(f'`{x}`' for x in lc)}")
        ss = sc.get("support_sources") or []
        sa = sc.get("support_analysis") or []
        if ss:
            lines.append(f"- **Support sources:** {', '.join(ss)}")
        if sa:
            lines.append(f"- **Support analysis:** {', '.join(sa)}")
        vuln = sc.get("vulnerabilities") or []
        if vuln:
            lines.append("- **Vulnerabilities:**")
            for v in vuln:
                lines.append(f"  - {v}")
        lines.append("")
    lines.append(
        "*Generated from `metadata/thesis-map.yaml` — run "
        "`python scripts/work_jiang/render_thesis_map.py` after edits.*"
    )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    data = load_yaml(META)
    errors = validate(data)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1
    OUT.write_text(render(data), encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
