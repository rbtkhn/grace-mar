# Forecast Summary — operator_daily_messages

- Artifact: `artifacts/forecast/operator_daily_messages.2026-04-12.v1.json`
- Selected method: `seasonal_naive`
- Horizon: `7`

## Selected point forecast

16.00, 19.00, 18.00, 20.00, 17.00, 15.00, 14.00

## Benchmark results

| Method | MAE | RMSE | MAPE | Notes |
|---|---:|---:|---:|---|
| last_value | 4.0000 | 4.4721 | 21.24 | Baseline backtest on holdout window. |
| moving_average | 1.8571 | 2.2361 | 9.96 | Baseline backtest on holdout window. |
| linear_trend | 1.8605 | 2.2056 | 10.25 | Baseline backtest on holdout window. |
| seasonal_naive | 1.0000 | 1.0000 | 5.63 | Baseline backtest on holdout window. |

## Boundary note

This artifact is a WORK-layer planning object. It does not update Record surfaces directly.
