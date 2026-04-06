#!/usr/bin/env python3
"""
Generate a confidence dashboard (Plotly radar HTML) from seed_confidence_map.json.

Usage:
  python3 scripts/generate-confidence-report.py users/demo/seed-phase

Optional deps: pip install -r scripts/requirements-seed-phase-dashboard.txt
Without plotly: script exits 1 with install hint.

PNG export requires kaleido; if missing, HTML is still written and a note is printed.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate seed-phase confidence radar report.")
    ap.add_argument("directory", type=Path, help="seed-phase directory")
    args = ap.parse_args()

    seed_dir = (REPO_ROOT / args.directory).resolve() if not args.directory.is_absolute() else args.directory
    if not seed_dir.is_dir():
        print(f"Not a directory: {seed_dir}", file=sys.stderr)
        return 1

    conf_path = seed_dir / "seed_confidence_map.json"
    if not conf_path.is_file():
        print(f"Missing {conf_path}", file=sys.stderr)
        return 1

    data = json.loads(conf_path.read_text(encoding="utf-8"))
    cm = data.get("confidence_map") or {}
    if not isinstance(cm, dict):
        print("seed_confidence_map.json: confidence_map must be an object", file=sys.stderr)
        return 1

    categories = [k for k in cm if k != "overall"]
    if not categories:
        print("No confidence dimensions besides overall", file=sys.stderr)
        return 1
    values = [float(cm[k]) for k in categories]
    overall = float(cm.get("overall", 0.0))

    try:
        import plotly.graph_objects as go
    except ImportError:
        print(
            "plotly is required. pip install -r scripts/requirements-seed-phase-dashboard.txt",
            file=sys.stderr,
        )
        return 1

    theta = categories + [categories[0]]
    r = values + [values[0]]
    fig = go.Figure(
        go.Scatterpolar(
            r=r,
            theta=theta,
            fill="toself",
            name="Confidence",
            line=dict(color="#00d4ff"),
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
        title=f"Seed phase confidence radar — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        showlegend=False,
    )

    html_path = seed_dir / "confidence-report.html"
    fig.write_html(str(html_path))

    png_path = seed_dir / "confidence-report.png"
    try:
        fig.write_image(str(png_path))
        png_msg = str(png_path)
    except Exception as e:  # noqa: BLE001 — kaleido / orca optional
        print(f"PNG skipped ({e}). Install kaleido for PNG export.", file=sys.stderr)
        png_msg = "(not written)"

    try:
        display = html_path.relative_to(REPO_ROOT)
    except ValueError:
        display = html_path
    print(f"Wrote {display}; PNG: {png_msg}")
    print(f"Overall readiness score (from confidence_map): {overall:.2f} / 1.0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
