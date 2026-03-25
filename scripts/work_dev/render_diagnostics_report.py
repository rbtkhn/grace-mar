#!/usr/bin/env python3
"""Render markdown report from diagnostics JSON."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def render(data: dict) -> str:
    tmpl = (
        REPO_ROOT / "docs" / "skill-work" / "work-dev" / "product" / "diagnostics_report_template.md"
    ).read_text(encoding="utf-8")
    lines = []
    for f in data.get("findings") or []:
        lines.append(f"- **{f.get('category')}** ({f.get('severity')}): {f.get('detail')}")
    body = "\n".join(lines) if lines else "- _(no findings)_\n"
    return (
        "<!-- GENERATED diagnostics report -->\n\n"
        + tmpl.replace("{{system_name}}", str(data.get("system_name")))
        .replace("{{generated_at}}", str(data.get("generated_at")))
        .replace("{{overall_score}}", str(data.get("overall_score")))
        .replace("{{findings_body}}", body)
        .replace("{{external_snippets}}", "Use proof-ledger external_summary_ok lines only when bounded.")
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", type=Path, required=True)
    ap.add_argument("-o", "--output", type=Path, required=True)
    args = ap.parse_args()
    data = json.loads(args.input.read_text(encoding="utf-8"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(data), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
