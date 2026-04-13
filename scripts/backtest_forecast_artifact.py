#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def mae(actual: List[float], predicted: List[float]) -> float:
    if len(actual) != len(predicted) or not actual:
        return math.nan
    return sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)


def rmse(actual: List[float], predicted: List[float]) -> float:
    if len(actual) != len(predicted) or not actual:
        return math.nan
    return math.sqrt(sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual))


def mape(actual: List[float], predicted: List[float]) -> float:
    if len(actual) != len(predicted) or not actual:
        return math.nan

    pairs = [(a, p) for a, p in zip(actual, predicted) if a != 0]
    if not pairs:
        return math.nan

    return 100.0 * sum(abs((a - p) / a) for a, p in pairs) / len(pairs)


def load_actuals(csv_path: str, time_col: str, value_col: str, horizon: int) -> List[float]:
    df = pd.read_csv(csv_path)
    if time_col not in df.columns:
        raise ValueError(f"Missing time column: {time_col}")
    if value_col not in df.columns:
        raise ValueError(f"Missing value column: {value_col}")

    df[time_col] = pd.to_datetime(df[time_col], errors="raise")
    df[value_col] = pd.to_numeric(df[value_col], errors="raise")
    df = df.sort_values(time_col).reset_index(drop=True)

    if len(df) < horizon:
        raise ValueError("Not enough observations to compare against forecast horizon.")

    return df.tail(horizon)[value_col].astype(float).tolist()


def evaluate_forecast(artifact: Dict[str, Any], actuals: List[float]) -> Dict[str, float]:
    predicted = artifact.get("point_forecast", [])
    if not isinstance(predicted, list):
        raise ValueError("Artifact point_forecast must be a list.")

    if len(predicted) != len(actuals):
        raise ValueError(
            f"Forecast length {len(predicted)} does not match actual length {len(actuals)}."
        )

    return {
        "mae": mae(actuals, predicted),
        "rmse": rmse(actuals, predicted),
        "mape": mape(actuals, predicted),
    }


def append_evaluation_to_artifact(
    artifact: Dict[str, Any], evaluation: Dict[str, float]
) -> Dict[str, Any]:
    existing = artifact.get("benchmark_results", [])
    existing.append(
        {
            "baseline_name": f"artifact::{artifact.get('method', {}).get('name', 'unknown')}",
            "mae": None if math.isnan(evaluation["mae"]) else round(evaluation["mae"], 4),
            "rmse": None if math.isnan(evaluation["rmse"]) else round(evaluation["rmse"], 4),
            "mape": None if math.isnan(evaluation["mape"]) else round(evaluation["mape"], 4),
            "notes": "Post-hoc artifact evaluation against supplied actuals.",
        }
    )
    artifact["benchmark_results"] = existing
    return artifact


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate a forecast artifact against actual observed values."
    )
    parser.add_argument("--artifact", required=True, help="Path to artifact JSON.")
    parser.add_argument("--actuals-csv", required=True, help="Path to actuals CSV.")
    parser.add_argument("--time-col", required=True, help="Timestamp column in CSV.")
    parser.add_argument("--value-col", required=True, help="Value column in CSV.")
    parser.add_argument(
        "--out",
        default="",
        help="Optional path to write updated artifact. If omitted, overwrite input artifact.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    artifact_path = Path(args.artifact)
    artifact = json.loads(artifact_path.read_text(encoding="utf-8"))

    horizon = artifact.get("forecast_horizon")
    if not isinstance(horizon, int) or horizon < 1:
        raise ValueError("Artifact forecast_horizon must be a positive integer.")

    actuals = load_actuals(args.actuals_csv, args.time_col, args.value_col, horizon)
    evaluation = evaluate_forecast(artifact, actuals)
    updated = append_evaluation_to_artifact(artifact, evaluation)

    out_path = Path(args.out) if args.out else artifact_path
    out_path.write_text(json.dumps(updated, indent=2), encoding="utf-8")

    print(f"Wrote evaluated artifact: {out_path}")
    print(
        "Metrics:",
        {
            key: None if math.isnan(val) else round(val, 4)
            for key, val in evaluation.items()
        },
    )


if __name__ == "__main__":
    main()
