#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List


def load_json_files(root: Path) -> List[dict[str, Any]]:
    if not root.exists():
        return []

    rows: List[dict[str, Any]] = []
    for path in sorted(root.rglob("*.json")):
        try:
            rows.append(json.loads(path.read_text(encoding="utf-8")))
        except Exception:
            continue
    return rows


def summarize_receipts(receipts: List[dict[str, Any]]) -> Dict[str, Any]:
    total = len(receipts)
    by_status = Counter(r.get("status", "unknown") for r in receipts)
    by_method = Counter(r.get("method", "unknown") for r in receipts)
    by_series = Counter(r.get("series_name", "unknown") for r in receipts)

    return {
        "total_receipts": total,
        "by_status": dict(by_status),
        "by_method": dict(by_method),
        "by_series": dict(by_series),
    }


def summarize_artifacts(artifacts: List[dict[str, Any]]) -> Dict[str, Any]:
    total = len(artifacts)
    with_quantiles = 0
    with_covariates = 0
    with_benchmarks = 0
    by_method: Counter[str] = Counter()

    for artifact in artifacts:
        method = artifact.get("method", {})
        method_name = method.get("name", "unknown") if isinstance(method, dict) else "unknown"
        by_method[method_name] += 1

        quantiles = artifact.get("quantile_forecast", {})
        covariates = artifact.get("covariates", [])
        benchmarks = artifact.get("benchmark_results", [])

        if isinstance(quantiles, dict) and len(quantiles) > 0:
            with_quantiles += 1
        if isinstance(covariates, list) and len(covariates) > 0:
            with_covariates += 1
        if isinstance(benchmarks, list) and len(benchmarks) > 0:
            with_benchmarks += 1

    return {
        "total_artifacts": total,
        "with_quantiles": with_quantiles,
        "with_covariates": with_covariates,
        "with_benchmarks": with_benchmarks,
        "by_method": dict(by_method),
    }


def write_markdown_report(
    out_path: Path,
    receipt_summary: Dict[str, Any],
    artifact_summary: Dict[str, Any],
) -> None:
    lines = [
        "# Forecast Observability Report",
        "",
        "## Receipts",
        "",
        f"- Total receipts: {receipt_summary['total_receipts']}",
        "",
        "### Receipts by status",
        "",
    ]

    for key, value in sorted(receipt_summary["by_status"].items()):
        lines.append(f"- {key}: {value}")

    lines.extend(
        [
            "",
            "### Receipts by method",
            "",
        ]
    )
    for key, value in sorted(receipt_summary["by_method"].items()):
        lines.append(f"- {key}: {value}")

    lines.extend(
        [
            "",
            "### Receipts by series",
            "",
        ]
    )
    for key, value in sorted(receipt_summary["by_series"].items()):
        lines.append(f"- {key}: {value}")

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            f"- Total artifacts: {artifact_summary['total_artifacts']}",
            f"- Artifacts with quantiles: {artifact_summary['with_quantiles']}",
            f"- Artifacts with covariates: {artifact_summary['with_covariates']}",
            f"- Artifacts with benchmarks: {artifact_summary['with_benchmarks']}",
            "",
            "### Artifacts by selected method",
            "",
        ]
    )

    for key, value in sorted(artifact_summary["by_method"].items()):
        lines.append(f"- {key}: {value}")

    lines.extend(
        [
            "",
            "## Boundary note",
            "",
            "Forecast artifacts and receipts are WORK-layer legibility objects. They do not update Record surfaces directly.",
            "",
        ]
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a lightweight observability report for forecast artifacts and receipts."
    )
    parser.add_argument(
        "--receipts-dir",
        default="artifacts/receipts/forecast",
        help="Directory containing forecast receipt JSON files.",
    )
    parser.add_argument(
        "--artifacts-dir",
        default="artifacts/forecast",
        help="Directory containing forecast artifact JSON files.",
    )
    parser.add_argument(
        "--out",
        default="artifacts/forecast/observability-report.md",
        help="Output markdown report path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    receipts = load_json_files(Path(args.receipts_dir))
    artifacts = [
        row
        for row in load_json_files(Path(args.artifacts_dir))
        if row.get("artifact_type") == "forecast_artifact"
    ]

    receipt_summary = summarize_receipts(receipts)
    artifact_summary = summarize_artifacts(artifacts)

    out_path = Path(args.out)
    write_markdown_report(out_path, receipt_summary, artifact_summary)

    print(f"Wrote observability report: {out_path}")


if __name__ == "__main__":
    main()
