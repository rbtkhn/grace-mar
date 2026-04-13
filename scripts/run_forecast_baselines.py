#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import pandas as pd


@dataclass
class ForecastResult:
    name: str
    values: List[float]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def timestamp_for_filename(iso_ts: str) -> str:
    # ISO may end with +00:00; normalize to Z before replacing colons in the time portion.
    s = iso_ts.replace("+00:00", "Z")
    return s.replace(":", "-")


def build_receipt(
    *,
    timestamp: str,
    series_name: str,
    artifact_path: str,
    summary_path: str,
    source_path: str,
    method: str,
    horizon: int,
    status: str,
    notes: str = "",
) -> dict[str, Any]:
    return {
        "receipt_type": "forecast_run",
        "version": "v1",
        "timestamp": timestamp,
        "lane": "work-forecast",
        "series_name": series_name,
        "artifact_path": artifact_path,
        "summary_path": summary_path,
        "source_path": source_path,
        "method": method,
        "horizon": horizon,
        "status": status,
        "notes": notes,
    }


def write_receipt(receipt: dict[str, Any], receipt_dir: str) -> Path:
    receipt_root = Path(receipt_dir)
    receipt_root.mkdir(parents=True, exist_ok=True)

    filename = (
        f"forecast_run."
        f"{receipt['series_name']}."
        f"{timestamp_for_filename(receipt['timestamp'])}.json"
    )
    path = receipt_root / filename
    path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    return path


def load_series(csv_path: str, time_col: str, value_col: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if time_col not in df.columns:
        raise ValueError(f"Missing time column: {time_col}")
    if value_col not in df.columns:
        raise ValueError(f"Missing value column: {value_col}")

    df = df[[time_col, value_col]].copy()
    df[time_col] = pd.to_datetime(df[time_col], errors="raise")
    df[value_col] = pd.to_numeric(df[value_col], errors="raise")
    df = df.sort_values(time_col).reset_index(drop=True)

    if df.empty:
        raise ValueError("Input series is empty.")
    if len(df) < 3:
        raise ValueError("Input series must contain at least 3 observations.")

    return df


def last_value_forecast(values: pd.Series, horizon: int) -> ForecastResult:
    last_value = float(values.iloc[-1])
    return ForecastResult(name="last_value", values=[last_value] * horizon)


def moving_average_forecast(
    values: pd.Series,
    horizon: int,
    window: int = 7,
) -> ForecastResult:
    effective_window = min(window, len(values))
    avg = float(values.tail(effective_window).mean())
    return ForecastResult(name="moving_average", values=[avg] * horizon)


def linear_trend_forecast(values: pd.Series, horizon: int) -> ForecastResult:
    y = values.astype(float).tolist()
    n = len(y)

    if n < 2:
        return ForecastResult(name="linear_trend", values=[float(y[-1])] * horizon)

    x = list(range(n))
    x_mean = sum(x) / n
    y_mean = sum(y) / n
    denom = sum((xi - x_mean) ** 2 for xi in x)

    if denom == 0:
        return ForecastResult(name="linear_trend", values=[float(y[-1])] * horizon)

    slope = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y)) / denom
    intercept = y_mean - slope * x_mean

    forecast = [float(intercept + slope * (n + i)) for i in range(horizon)]
    return ForecastResult(name="linear_trend", values=forecast)


def seasonal_naive_forecast(
    values: pd.Series,
    horizon: int,
    season_length: int = 7,
) -> ForecastResult:
    if len(values) < season_length:
        return last_value_forecast(values, horizon)

    tail = values.tail(season_length).astype(float).tolist()
    forecast: List[float] = []
    for i in range(horizon):
        forecast.append(float(tail[i % season_length]))
    return ForecastResult(name="seasonal_naive", values=forecast)


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


def split_history_holdout(
    df: pd.DataFrame,
    value_col: str,
    horizon: int,
) -> Tuple[pd.Series, List[float]]:
    if len(df) <= horizon + 2:
        raise ValueError(
            "Not enough observations for requested horizon. "
            "Need at least horizon + 3 rows."
        )

    history = df.iloc[:-horizon][value_col]
    holdout = df.iloc[-horizon:][value_col].astype(float).tolist()
    return history, holdout


def quantile_band_from_point(
    point_forecast: List[float],
    history_values: pd.Series,
) -> Dict[str, List[float]]:
    std = float(history_values.tail(min(14, len(history_values))).std(ddof=0))
    if math.isnan(std):
        std = 0.0

    low = [float(v - std) for v in point_forecast]
    mid = [float(v) for v in point_forecast]
    high = [float(v + std) for v in point_forecast]

    return {
        "0.1": low,
        "0.5": mid,
        "0.9": high,
    }


def choose_default_method(
    benchmark_rows: List[Dict[str, float]],
    forecasts_by_name: Dict[str, ForecastResult],
) -> ForecastResult:
    valid_rows = [row for row in benchmark_rows if not math.isnan(row["mae"])]
    if not valid_rows:
        return forecasts_by_name["moving_average"]

    best = min(valid_rows, key=lambda row: row["mae"])
    return forecasts_by_name[best["baseline_name"]]


def build_artifact(
    *,
    series_name: str,
    series_description: str,
    time_unit: str,
    full_df: pd.DataFrame,
    time_col: str,
    history_values: pd.Series,
    horizon: int,
    selected_forecast: ForecastResult,
    all_forecasts: Dict[str, ForecastResult],
    benchmark_rows: List[Dict[str, float]],
    source_path: str,
) -> Dict[str, Any]:
    quantiles = quantile_band_from_point(selected_forecast.values, history_values)

    assumptions = [
        "Recent pattern remains informative over the forecast horizon.",
        "No major regime change is expected during the forecast horizon.",
    ]

    invalidators = [
        "Major schedule or workflow shift",
        "Data collection breakage or missing observations",
        "External shock that changes the recent pattern",
    ]

    return {
        "artifact_type": "forecast_artifact",
        "version": "v1",
        "series_name": series_name,
        "series_description": series_description,
        "time_unit": time_unit,
        "history_window": {
            "start": str(full_df[time_col].iloc[0].date()),
            "end": str(full_df[time_col].iloc[-1].date()),
            "n_observations": int(len(full_df)),
        },
        "forecast_horizon": horizon,
        "method": {
            "name": selected_forecast.name,
            "version": "v1",
            "config": {
                "available_methods": list(all_forecasts.keys()),
            },
        },
        "point_forecast": [round(v, 4) for v in selected_forecast.values],
        "quantile_forecast": {
            k: [round(v, 4) for v in vals]
            for k, vals in quantiles.items()
        },
        "covariates": [],
        "benchmark_results": [
            {
                "baseline_name": row["baseline_name"],
                "mae": None if math.isnan(row["mae"]) else round(row["mae"], 4),
                "rmse": None if math.isnan(row["rmse"]) else round(row["rmse"], 4),
                "mape": None if math.isnan(row["mape"]) else round(row["mape"], 4),
                "notes": row["notes"],
            }
            for row in benchmark_rows
        ],
        "assumptions": assumptions,
        "invalidators": invalidators,
        "operator_note": (
            "Baseline forecast artifact for WORK-layer planning use only. "
            "Not a Record fact."
        ),
        "receipt_id": "",
        "source_artifacts": [source_path],
        "candidate_methods": {
            name: [round(v, 4) for v in result.values]
            for name, result in all_forecasts.items()
        },
    }


def write_markdown_summary(
    summary_path: Path,
    artifact_path: Path,
    series_name: str,
    horizon: int,
    selected_method: str,
    benchmark_rows: List[Dict[str, float]],
    selected_values: List[float],
) -> None:
    lines = [
        f"# Forecast Summary — {series_name}",
        "",
        f"- Artifact: `{artifact_path}`",
        f"- Selected method: `{selected_method}`",
        f"- Horizon: `{horizon}`",
        "",
        "## Selected point forecast",
        "",
        ", ".join(f"{v:.2f}" for v in selected_values),
        "",
        "## Benchmark results",
        "",
        "| Method | MAE | RMSE | MAPE | Notes |",
        "|---|---:|---:|---:|---|",
    ]

    for row in benchmark_rows:
        mae_str = "n/a" if math.isnan(row["mae"]) else f"{row['mae']:.4f}"
        rmse_str = "n/a" if math.isnan(row["rmse"]) else f"{row['rmse']:.4f}"
        mape_str = "n/a" if math.isnan(row["mape"]) else f"{row['mape']:.2f}"
        lines.append(
            f"| {row['baseline_name']} | {mae_str} | {rmse_str} | {mape_str} | {row['notes']} |"
        )

    lines.extend(
        [
            "",
            "## Boundary note",
            "",
            "This artifact is a WORK-layer planning object. It does not update Record surfaces directly.",
            "",
        ]
    )

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run baseline forecasts and write a Grace-Mar forecast artifact."
    )
    parser.add_argument("--input", required=True, help="Path to CSV file.")
    parser.add_argument("--series-name", required=True, help="Series name.")
    parser.add_argument("--time-col", required=True, help="Timestamp column name.")
    parser.add_argument("--value-col", required=True, help="Value column name.")
    parser.add_argument("--horizon", type=int, required=True, help="Forecast horizon.")
    parser.add_argument("--out", required=True, help="Artifact JSON output path.")
    parser.add_argument(
        "--summary-out",
        default="",
        help="Optional markdown summary output path. If omitted, inferred from --out.",
    )
    parser.add_argument(
        "--series-description",
        default="",
        help="Optional human-readable series description.",
    )
    parser.add_argument(
        "--time-unit",
        default="day",
        choices=["day", "week", "month", "quarter", "year", "custom"],
        help="Time unit for the series.",
    )
    parser.add_argument(
        "--moving-average-window",
        type=int,
        default=7,
        help="Window size for moving average baseline.",
    )
    parser.add_argument(
        "--season-length",
        type=int,
        default=7,
        help="Season length for seasonal naive baseline.",
    )
    parser.add_argument(
        "--receipt-dir",
        default="artifacts/receipts/forecast",
        help="Directory for forecast receipt JSON files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    df = load_series(args.input, args.time_col, args.value_col)
    history_values, holdout = split_history_holdout(df, args.value_col, args.horizon)

    forecasts = {
        "last_value": last_value_forecast(history_values, args.horizon),
        "moving_average": moving_average_forecast(
            history_values,
            args.horizon,
            window=args.moving_average_window,
        ),
        "linear_trend": linear_trend_forecast(history_values, args.horizon),
        "seasonal_naive": seasonal_naive_forecast(
            history_values,
            args.horizon,
            season_length=args.season_length,
        ),
    }

    benchmark_rows: List[Dict[str, float]] = []
    for name, result in forecasts.items():
        benchmark_rows.append(
            {
                "baseline_name": name,
                "mae": mae(holdout, result.values),
                "rmse": rmse(holdout, result.values),
                "mape": mape(holdout, result.values),
                "notes": "Baseline backtest on holdout window.",
            }
        )

    selected = choose_default_method(benchmark_rows, forecasts)

    run_timestamp = utc_now_iso()

    artifact = build_artifact(
        series_name=args.series_name,
        series_description=args.series_description,
        time_unit=args.time_unit,
        full_df=df,
        time_col=args.time_col,
        history_values=history_values,
        horizon=args.horizon,
        selected_forecast=selected,
        all_forecasts=forecasts,
        benchmark_rows=benchmark_rows,
        source_path=args.input,
    )
    artifact["forecast_generated_at"] = run_timestamp

    artifact_path = Path(args.out)
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    if args.summary_out:
        summary_path = Path(args.summary_out)
    else:
        summary_path = artifact_path.with_suffix(".summary.md")

    write_markdown_summary(
        summary_path=summary_path,
        artifact_path=artifact_path,
        series_name=args.series_name,
        horizon=args.horizon,
        selected_method=selected.name,
        benchmark_rows=benchmark_rows,
        selected_values=selected.values,
    )

    receipt = build_receipt(
        timestamp=run_timestamp,
        series_name=args.series_name,
        artifact_path=str(artifact_path),
        summary_path=str(summary_path),
        source_path=args.input,
        method=selected.name,
        horizon=args.horizon,
        status="completed",
        notes="Baseline forecast run completed successfully.",
    )
    receipt_path = write_receipt(receipt, args.receipt_dir)

    artifact["receipt_id"] = receipt_path.stem
    artifact_path.write_text(json.dumps(artifact, indent=2), encoding="utf-8")

    print(f"Wrote artifact: {artifact_path}")
    print(f"Wrote summary:  {summary_path}")
    print(f"Wrote receipt:  {receipt_path}")
    print(f"Selected method: {selected.name}")


if __name__ == "__main__":
    main()
