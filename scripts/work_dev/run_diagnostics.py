#!/usr/bin/env python3
"""Run a lightweight diagnostics pass from a YAML config (work-dev product surface)."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def run_diagnostics(config_path: Path, repo_root: Path) -> dict:
    cfg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if not isinstance(cfg, dict):
        raise ValueError("config must be a mapping")
    system_name = str(cfg.get("system_name") or "grace-mar")
    findings = []
    scores: dict[str, float] = {}
    for dim in ("truth_source", "library_boundary", "continuity", "provenance"):
        ok = bool(cfg.get("canonical_truth_source"))
        scores[dim] = 1.0 if ok else 0.5
        findings.append(
            {
                "id": f"FIND-{dim}",
                "category": dim,
                "severity": "info" if ok else "watch",
                "detail": "canonical paths declared" if ok else "fill canonical_truth_source",
            }
        )
    overall = sum(scores.values()) / max(len(scores), 1)
    return {
        "system_name": system_name,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scores": scores,
        "overall_score": round(overall, 3),
        "findings": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    ap.add_argument("--json-out", type=Path, default=None)
    args = ap.parse_args()
    out = run_diagnostics(args.config, args.repo_root)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    else:
        print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
